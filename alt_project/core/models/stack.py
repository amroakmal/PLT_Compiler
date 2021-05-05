class Stack:
    def __init__(self):
        self.items = []

    def peak(self):
        return self.items[-1]

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def get_items(self):
        return self.items

    def size(self):
        return len(self.items)

    def is_empty(self):
        if len(self.items) == 0:
            return True
        return False
