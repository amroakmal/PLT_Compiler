

class RegularDefinition:
    def __init__(self, key: str, value: str):
        self.key = key
        self.value = value

    def addRule(self, store):
        store.putRegularDefinition(self.key, self.value)
