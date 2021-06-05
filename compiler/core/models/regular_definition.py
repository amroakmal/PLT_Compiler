

class RegularDefinition:
    def __init__(self, key: str, value: str):
        self.key = key
        self.value = value

    def add_rule(self, store):
        store.put_regular_definition(self.key, self.value)
