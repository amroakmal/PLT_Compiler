class Node:
    id = 0

    def __init__(self, input1=None, input2=None, input3=None):
        if input1 is None and input2 is None and input3 is None:
            self.currentId = Node.id
            Node.id += 1
            self.map = {}
            self.start = False
            self.end = False
            self.nodeTypes = ''
        if input1 is not None and input2 is None and input3 is None:
            print(input1)
            self.currentId = Node.id
            Node.id += 1
            self.start = input1.isStart()
            self.end = input1.isEnd()
            self.nodeTypes = input1.getNodeTypes()
            self.map = {}
        if input1 is not None and input2 is not None and input3 is None:
            self.currentId = Node.id
            Node.id += 1
            self.map = {}
            self.start = input1
            self.end = input2
            self.nodeTypes = ''

        self.currentId = Node.id
        Node.id += 1
        self.map = {}
        self.start = input1
        self.end = input2
        self.nodeTypes = ''

    def addEdge(self, word, destination):
        if word in self.map:
            # If the character already exists in my hashmap, just add the edge
            val = self.map[word]
            val.append(destination)
            self.map[word] = val
        else:
            # Else add the character and create a new edge list
            self.map[word] = [destination]

    def removeAllEdges(self, s):
        val = self.map[s]
        val.clear()
        self.map[s] = val

    def getMap(self):
        return self.map

    def isStart(self):
        return self.start

    def setStart(self, start):
        self.start = start

    def isEnd(self):
        return self.end

    def setEnd(self, end):
        self.end = end

    def getCurrentId(self):
        return self.currentId

    def setNodeTypes(self, types):
        self.nodeTypes = types

    def getNodeTypes(self):
        return self.nodeTypes

    def compareTo(self, o):
        otherNode = o
        return self.getCurrentId() - otherNode.getCurrentId()
