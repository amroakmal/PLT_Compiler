from core.constants import Constants
from core.models.graph.graph import Graph
from core.models.stack import Stack
from core.models.graph.node import Node
from core.utils.dfa_util import DfaUtility


class DFAA:
    def __init__(self, nfa_combined):
        self.dfa = Graph()
        self.DFAStatesUnmarked = Stack()
        self.DFATransTable = {}

        s0 = [nfa_combined.get_initial_node()]
        eps_closure_s0 = self.epsilon_closure(s0)
        self.DFAStatesUnmarked.push(eps_closure_s0)
        self.DFATransTable[DfaUtility.createUnionID(eps_closure_s0)] = self.dfa.get_initial_node()
        self.construct_dfa(nfa_combined)

    def construct_dfa(self, nfa_combined):
        while not self.DFAStatesUnmarked.is_empty():
            t = self.DFAStatesUnmarked.pop()
            ts_id = DfaUtility.createUnionID(t)
            U = []
            for a in DfaUtility.getUnionInputs(t):
                U = self.epsilon_closure(self.move(t, a))
                new_node_types = DfaUtility.getNodeType(U)
                new_id = DfaUtility.createUnionID(U)
                if new_id not in self.DFATransTable.keys():
                    self.DFAStatesUnmarked.push(U)
                    node = Node()
                    node.set_node_types(new_node_types)
                    self.DFATransTable[new_id] = node

                    if nfa_combined.get_destination() in U:
                        node.set_end(True)

                temp = self.DFATransTable[ts_id]
                temp.add_edge(a, self.DFATransTable[new_id])

    def epsilon_closure(self, T):
        stack = Stack()
        epsilon_closure_out = T

        for node in epsilon_closure_out:
            stack.push(node)

        while not stack.is_empty():
            t = stack.pop()
            neighbours = t.get_map()

            for key in neighbours.keys():
                if key == Constants.EPSILON:
                    for node in neighbours[key]:
                        if node not in epsilon_closure_out:
                            epsilon_closure_out.append(node)
                            stack.push(node)

        return epsilon_closure_out

    def move(self, t, a):
        res = []
        for node in t:
            if a in node.get_map().keys():
                for nodeIterator in node.get_map()[a]:
                    if nodeIterator not in res:
                        res.append(nodeIterator)

        return res

    def get_dfa(self):
        return self.dfa

    def get_dfa_trans_table(self):
        return self.DFATransTable
