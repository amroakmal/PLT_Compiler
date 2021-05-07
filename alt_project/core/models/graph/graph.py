from .node import Node


class Graph:
    def __init__(self, inp=None):
        if inp is None:
            self.initialNode = Node(True, False)
            self.destination = None

        if isinstance(inp, str):
            self.initialNode = Node(True, False)
            self.destination = Node(False, True)
            self.initialNode.addEdge(inp, self.destination)

        elif isinstance(inp, Graph):
            oldToNew = {}
            self.initialNode = Node(inp.getInitialNode())
            oldToNew[inp.getInitialNode()] = self.initialNode
            visited = [False] * Node.id
            self.cloneDFS(inp.getInitialNode(), visited, oldToNew)
            self.destination = oldToNew[inp.getDestination()]

    def cloneDFS(self, node, visited, oldToNew):
        if visited[node.getCurrentId()]:
            return
        visited[node.getCurrentId()] = True

        for k, v in node.getMap().items():
            current = v
            for value in current:
                if value not in oldToNew:
                    oldToNew[value] = Node(value)

                if k not in oldToNew[node].getMap():
                    temp = oldToNew[node].getMap()
                    temp[k] = []

                temp = oldToNew[node].getMap()
                temp[k].append(oldToNew[value])
                self.cloneDFS(value, visited, oldToNew)

    def getInitialNode(self):
        return self.initialNode

    def getDestination(self):
        return self.destination

    def setInitialNode(self, initialNode):
        self.initialNode = initialNode

    def setDestination(self, destination):
        self.destination = destination
