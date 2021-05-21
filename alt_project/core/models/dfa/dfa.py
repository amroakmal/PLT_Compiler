from core.constants import Constants
from core.models.graph.graph import Graph
from core.models.stack import Stack
from core.models.graph.node import Node
from core.utils.dfa_util import DfaUtility


class DFAA:
    def __init__(self, NFACombined):
        self.dfa = Graph()
        self.DFAStatesUnmarked = Stack()
        self.DFATransTable = {}

        s0 = []
        s0.append(NFACombined.get_initial_node())
        epsClosureS0 = self.epsilonClosure(s0)
        self.DFAStatesUnmarked.push(epsClosureS0)
        self.DFATransTable[DfaUtility.createUnionID(epsClosureS0)] = self.dfa.get_initial_node()
        self.constructDFA(NFACombined)

    def constructDFA(self, NFACombined):
        while not self.DFAStatesUnmarked.is_empty():
            T = self.DFAStatesUnmarked.pop()
            TsID = DfaUtility.createUnionID(T)
            U = []
            for a in DfaUtility.getUnionInputs(T):
                U = self.epsilonClosure(self.move(T, a))
                newNodeTypes = DfaUtility.getNodeType(U)
                newID = DfaUtility.createUnionID(U)
                if newID not in self.DFATransTable.keys():
                    self.DFAStatesUnmarked.push(U)
                    node = Node()
                    node.set_node_types(newNodeTypes)
                    self.DFATransTable[newID] = node

                    # TODO: test this line

                    if NFACombined.get_destination() in U:
                        node.set_end(True)

                temp = self.DFATransTable[TsID]
                temp.add_edge(a, self.DFATransTable[newID])

    def epsilonClosure(self, T):
        stack = Stack()
        epsilonClosureOut = T

        for node in epsilonClosureOut:
            stack.push(node)

        while not stack.is_empty():
            t = stack.pop()
            neighbours = t.get_map()

            for key in neighbours.keys():
                if key == Constants.EPSILON:
                    for node in neighbours[key]:
                        if node not in epsilonClosureOut:
                            epsilonClosureOut.append(node)
                            stack.push(node)

        return epsilonClosureOut

    def move(self, t, a):
        res = []
        for node in t:
            if a in node.get_map().keys():
                for nodeIterator in node.get_map()[a]:
                    if nodeIterator not in res:
                        res.append(nodeIterator)

        return res

    def getDFA(self):
        return self.dfa

    def getDFATransTable(self):
        return self.DFATransTable
