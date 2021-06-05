from .node import Node
from ...constants import Constants


class Graph:
    def __init__(self, inp=None):
        if inp is None:
            self.initial_node = Node(True, False)
            self.destination = None

        if isinstance(inp, str):
            self.initial_node = Node(True, False)
            self.destination = Node(False, True)
            self.initial_node.add_edge(inp, self.destination)

        elif isinstance(inp, Graph):
            old_to_new = {}
            self.initial_node = Node(inp.get_initial_node())
            old_to_new[inp.get_initial_node()] = self.initial_node
            visited = [False] * Node.id
            self.clone_dfs(inp.get_initial_node(), visited, old_to_new)
            self.destination = old_to_new[inp.get_destination()]

    def clone_dfs(self, node, visited, old_to_new):
        if visited[node.get_current_id()]:
            return
        visited[node.get_current_id()] = True

        for k, v in node.get_map().items():
            current = v
            for value in current:
                if value not in old_to_new:
                    old_to_new[value] = Node(value)

                if k not in old_to_new[node].get_map():
                    temp = old_to_new[node].get_map()
                    temp[k] = []

                temp = old_to_new[node].get_map()
                temp[k].append(old_to_new[value])
                self.clone_dfs(value, visited, old_to_new)

    def get_initial_node(self):
        return self.initial_node

    def get_destination(self):
        return self.destination

    def set_initial_node(self, initial_node):
        self.initial_node = initial_node

    def set_destination(self, destination):
        self.destination = destination

    def toString(self):
        out = ""
        visited = [0] * Node.id
        out += self.DFSPrintTree(self.initial_node, visited)
        return out

    def DFSPrintTree(self, node, visited):
        if visited[node.get_current_id()]:
            return ""

        visited[node.get_current_id()] = True
        out = str(node.get_current_id()) + "\n"

        for k, v in node.get_map().items():
            current = v
            for value in current:
                edge = k
                if edge == Constants.EPSILON:
                    edge = "eps"
                out += str(node.get_current_id()) + " " + str(value.get_current_id()) + " " + edge + "\n"
                out += self.DFSPrintTree(value, visited)

        return out
