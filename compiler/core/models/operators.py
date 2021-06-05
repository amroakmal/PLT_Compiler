class Operators:
    def __init__(self, ops: str):
        self.operators = list(ops)

    def add_rule(self, store):
        index = 0

        while index < len(self.operators):
            if self.operators[index] != ' ':
                if self.operators[index] != '\\':
                    store.add_operator(f'{self.operators[index]}')
                else:
                    store.add_operator(f'{self.operators[index]}{self.operators[index + 1]}')
                    index += 1

            index += 1
