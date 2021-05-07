class Node:
    id = 0

    def __init__(self, input1=None, input2=None):
        if input1 is None and input2 is None:
            self.current_id = Node.id
            Node.id += 1
            self.map = {}
            self.start = False
            self.end = False
            self.node_types = ''
        if input1 is not None and input2 is None:
            self.current_id = Node.id
            Node.id += 1
            self.start = input1.is_start()
            self.end = input1.is_end()
            self.node_types = input1.get_node_types()
            self.map = {}
        if input1 is not None and input2 is not None:
            self.current_id = Node.id
            Node.id += 1
            self.map = {}
            self.start = input1
            self.end = input2
            self.node_types = ''

    def add_edge(self, word, destination):
        if word in self.map:
            # If the character already exists in my hashmap, just add the edge
            val = self.map[word]
            val.append(destination)
            self.map[word] = val
        else:
            # Else add the character and create a new edge list
            self.map[word] = [destination]

    def remove_all_edges(self, s):
        val = self.map[s]
        val.clear()
        self.map[s] = val

    def get_map(self):
        return self.map

    def is_start(self):
        return self.start

    def set_start(self, start):
        self.start = start

    def is_end(self):
        return self.end

    def set_end(self, end):
        self.end = end

    def get_current_id(self):
        return self.current_id

    def set_node_types(self, types):
        self.node_types = types

    def get_node_types(self):
        return self.node_types

    def compare_to(self, o):
        other_node = o
        return self.get_current_id() - other_node.get_current_id()
