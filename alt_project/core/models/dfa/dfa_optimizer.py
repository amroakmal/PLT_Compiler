from core.constants import Constants
from core.models.graph.graph import Graph
from core.models.graph.node import Node
from core.models.pair import Pair
from core.utils.dfa_util import DfaUtility


class DFAOptimizer:
    def __init__(self, DFA):
        self.DFAMinimized = Graph()
        self.finalStates = {}
        self.minimizeDFA(DFA)

    def minimizeDFA(self, DFA):
        nodeParents = {}
        DFATransTable = DFA.getDFATransTable()
        grouping = {}

        nonAcceptingState = []
        acceptingState = []
        for string in DFATransTable.keys():
            node = DFATransTable[string]
            if node.is_end():
                acceptingState.append(node)
            else:
                nonAcceptingState.append(node)

        grouping[nonAcceptingState[0].get_current_id()] = nonAcceptingState

        while len(acceptingState) != 0:
            partition = []
            i = 1
            while i < len(acceptingState):
                if acceptingState[i].get_node_types() == acceptingState[0].get_node_types():
                    partition.append(acceptingState.pop(i))
                    i -= 1
                i += 1

            partition.append(acceptingState.pop(0))
            self.initNodeParents(partition, nodeParents)
            grouping[partition[0].get_current_id()] = partition

        self.initNodeParents(nonAcceptingState, nodeParents)
        newGrouping = grouping

        # Do.. While
        while True:
            grouping = newGrouping
            newGrouping = self.constructGroupings(grouping, nodeParents)
            if not (len(newGrouping) != len(grouping)):
                break

        self.linkDFAFinalGroupings(newGrouping, DFA)

    def linkDFAFinalGroupings(self, finalGroupings, DFA):
        self.DFAMinimized = Graph()
        transTable = {}
        for partitionID in finalGroupings.keys():
            node = Node()
            node.set_node_types(finalGroupings[partitionID][0].get_node_types())
            if finalGroupings[partitionID][0].is_end():
                node.set_end(True)

            transTable[partitionID] = node

        initialNodeGroupId = DfaUtility.findPartitionOfNode(DFA.getDFA().get_initial_node(), finalGroupings)
        initialNode = transTable[initialNodeGroupId]
        initialNode.set_start(True)

        self.DFAMinimized.set_initial_node(initialNode)
        for currentID in finalGroupings.keys():
            firstNodeOfGroup = finalGroupings[currentID][0]
            for input in firstNodeOfGroup.get_map().keys():
                self.updateFinalStates(input, currentID, finalGroupings, transTable)
                nextNode = firstNodeOfGroup.get_map()[input][0]
                groupingsID = DfaUtility.findPartitionOfNode(nextNode, finalGroupings)
                transTable[currentID].add_edge(input, transTable[groupingsID])

    def updateFinalStates(self, input, currentID, finalGroupings, transTable):
        for oldSource in finalGroupings[currentID]:

            newSource = transTable[DfaUtility.findPartitionOfNode(oldSource, finalGroupings)]
            toNodes = oldSource.get_map()[input]
            for oldDestination in toNodes:
                newDestination = transTable[DfaUtility.findPartitionOfNode(oldDestination, finalGroupings)]
                key = str(newSource.get_current_id()) + Constants.SEPARATOR + input
                type = oldDestination.get_node_types()
                self.finalStates[key] = Pair(newDestination, type)

    def constructGroupings(self, groupings, nodeParents):
        newNodeParents = {}
        newGroupings = {}

        for oldGroupID in groupings.keys():
            for node in groupings[oldGroupID]:
                groupMatch = False
                for newGroupID in newGroupings.keys():
                    newGroupingParent = newGroupings[newGroupID][0]

                    groupMatch = DfaUtility.canFit(node, newGroupingParent, nodeParents)
                    if groupMatch:
                        newGroupings[newGroupID].append(node)
                        newNodeParents[node.get_current_id()] = newGroupID
                        break
                if not groupMatch:
                    newPartition = []
                    newPartition.append(node)
                    newNodeParents[node.get_current_id()] = node.get_current_id()
                    newGroupings[node.get_current_id()] = newPartition

        nodeParents.update(newNodeParents)
        return newGroupings

    def getFinalStates(self):
        return self.finalStates

    def getDFAMinimized(self):
        return self.DFAMinimized

    def initNodeParents(self, partition, nodeParent):
        for node in partition:
            nodeParent[node.get_current_id()] = partition[0].get_current_id()
