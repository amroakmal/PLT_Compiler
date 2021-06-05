from core.constants import Constants
from core.models.graph.graph import Graph
from core.models.graph.node import Node
from core.models.pair import Pair
from core.utils.dfa_util import DfaUtility


class DFAOptimizer:
    def __init__(self, dfa):
        self.DFAMinimized = Graph()
        self.finalStates = {}
        self.minimize_dfa(dfa)

    def minimize_dfa(self, dfa):
        node_parents = {}
        dfa_trans_table = dfa.get_dfa_trans_table()
        grouping = {}

        non_accepting_state = []
        accepting_state = []
        for string in dfa_trans_table.keys():
            node = dfa_trans_table[string]
            if node.is_end():
                accepting_state.append(node)
            else:
                non_accepting_state.append(node)

        grouping[non_accepting_state[0].get_current_id()] = non_accepting_state

        while len(accepting_state) != 0:
            partition = []
            i = 1
            while i < len(accepting_state):
                if accepting_state[i].get_node_types() == accepting_state[0].get_node_types():
                    partition.append(accepting_state.pop(i))
                    i -= 1
                i += 1

            partition.append(accepting_state.pop(0))
            self.init_node_parents(partition, node_parents)
            grouping[partition[0].get_current_id()] = partition

        self.init_node_parents(non_accepting_state, node_parents)
        new_grouping = grouping

        # Do.. While
        while True:
            grouping = new_grouping
            new_grouping = self.construct_groupings(grouping, node_parents)
            if not (len(new_grouping) != len(grouping)):
                break

        self.link_dfa_final_groupings(new_grouping, dfa)

    def link_dfa_final_groupings(self, final_groupings, dfa):
        self.DFAMinimized = Graph()
        trans_table = {}
        for partitionID in final_groupings.keys():
            node = Node()
            node.set_node_types(final_groupings[partitionID][0].get_node_types())
            if final_groupings[partitionID][0].is_end():
                node.set_end(True)

            trans_table[partitionID] = node

        initial_node_group_id = DfaUtility.findPartitionOfNode(dfa.get_dfa().get_initial_node(), final_groupings)
        initial_node = trans_table[initial_node_group_id]
        initial_node.set_start(True)

        self.DFAMinimized.set_initial_node(initial_node)
        for currentID in final_groupings.keys():
            first_node_of_group = final_groupings[currentID][0]
            for my_input in first_node_of_group.get_map().keys():
                self.update_final_states(my_input, currentID, final_groupings, trans_table)
                next_node = first_node_of_group.get_map()[my_input][0]
                groupings_id = DfaUtility.findPartitionOfNode(next_node, final_groupings)
                trans_table[currentID].add_edge(my_input, trans_table[groupings_id])

    def update_final_states(self, my_input, current_id, final_groupings, trans_table):
        for oldSource in final_groupings[current_id]:

            new_source = trans_table[DfaUtility.findPartitionOfNode(oldSource, final_groupings)]
            to_nodes = oldSource.get_map()[my_input]
            for oldDestination in to_nodes:
                new_destination = trans_table[DfaUtility.findPartitionOfNode(oldDestination, final_groupings)]
                key = str(new_source.get_current_id()) + Constants.SEPARATOR + my_input
                typee = oldDestination.get_node_types()
                self.finalStates[key] = Pair(new_destination, typee)

    def construct_groupings(self, groupings, node_parents):
        new_node_parents = {}
        new_groupings = {}

        for oldGroupID in groupings.keys():
            for node in groupings[oldGroupID]:
                group_match = False
                for newGroupID in new_groupings.keys():
                    new_grouping_parent = new_groupings[newGroupID][0]

                    group_match = DfaUtility.canFit(node, new_grouping_parent, node_parents)
                    if group_match:
                        new_groupings[newGroupID].append(node)
                        new_node_parents[node.get_current_id()] = newGroupID
                        break
                if not group_match:
                    new_partition = [node]
                    new_node_parents[node.get_current_id()] = node.get_current_id()
                    new_groupings[node.get_current_id()] = new_partition

        node_parents.update(new_node_parents)
        return new_groupings

    def get_final_states(self):
        return self.finalStates

    def get_dfa_minimized(self):
        return self.DFAMinimized

    def init_node_parents(self, partition, node_parent):
        for node in partition:
            node_parent[node.get_current_id()] = partition[0].get_current_id()
