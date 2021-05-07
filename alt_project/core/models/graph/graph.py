from .node import Node

class Graph:

    def __init__(self, inp=None):
        if inp is None:
            self.initialNode = Node(True, False, None)
            self.destination = None

        elif isinstance(inp, str):
            self.initialNode = Node(True, False, None)
            self.destination = Node(False, True, None)
            self.initialNode.addEdge(inp, self.destination)

        elif isinstance(inp, Graph):
            self.initialNode = Node(inp.initialNode, None, None)
            old_to_new = {
                inp.initialNode: self.initialNode
            }
            visited = [False] * Node.id
            self.clone_dfs(inp.initialNode, visited, old_to_new)
            self.destination = old_to_new.get(inp.destination)

    def clone_dfs(self, n, visited, old_to_new):
        if visited[n.getCurrentId()]:
            return
        visited[n.getCurrentId()] = True
        for k, v in n.getMap().items():
            for i in v:
                if i not in old_to_new:
                    old_to_new[i] = Node(i, None, None)
                old_to_new[n].getMap()[k] = [old_to_new[i]]
                self.clone_dfs(i, visited, old_to_new)

    def graph_to_string(self):
        out = ''
        visited = [False] * Node.id
        out += self.dfs_print_tree(self.initialNode, visited)
        return out

    def dfs_print_tree(self, n, visited):
        if visited[n.getCurrentId()]:
            return ''
        visited[n.getCurrentId()] = True
        out = str(n.getCurrentId()) + "\n"
        for k, v in n.getMap().items():
            for i in v:
                edge = k
                if edge == "\\L":
                    edge = "eps"
                out += str(n.getCurrentId()) + " " + str(i.getCurrentId()) + " " + edge + "\n"

                out += self.dfs_print_tree(i, visited)
        return out

    def getInitialNode(self):
        return self.initialNode

    def getDestination(self):
        if self.destination is None:
            print(self.graph_to_string())
        return self.destination

    def setInitialNode(self, initialNode):
        self.initialNode = initialNode

    def setDestination(self, destination):
        self.destination = destination
