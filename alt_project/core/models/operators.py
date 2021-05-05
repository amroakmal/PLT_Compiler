class Operators:
    def __init__(self, ops: str):
        self.operators = list(ops)

    def addRule(self, store):
        index = 0

        while index < len(self.operators):
            if self.operators[index] != ' ':
                if self.operators[index] != '\\':
                    store.addOperator(f'{self.operators[index]}')
                else:
                    store.addOperator(f'{self.operators[index]}{self.operators[index + 1]}')
                    index += 1

            index += 1
