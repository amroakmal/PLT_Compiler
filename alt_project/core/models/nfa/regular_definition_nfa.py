from core.models.stack import Stack


class RegularDefinitionNFA:
    def __init__(self, rulesCont):
        self.definitionNfa = {}
        self.definitionsToNfa(rulesCont)

    def definitionsToNfa(self, lexicalRulesStore):
        for idx, val in enumerate(lexicalRulesStore.getRegularDefinitionsKeys()):
            definitionKey = lexicalRulesStore.getRegularDefinitionsKeys()[idx]
            definitionValue = lexicalRulesStore.getRegularDefinition(definitionKey)

            definitionValue = self.separateRDByOrs(definitionValue)

            currentDefinitionNfa = self.createNfa(definitionValue)
            self.definitionNfa[definitionKey] = currentDefinitionNfa

    def createNfa(self, definition: str):

        nfa = Stack()
        operator = Stack()
        merge = []

        i = 0

        while i < len(definition):
            c = definition[i]
            if c.isalpha() or c.isnumeric():
                j = i

                while j < len(definition) and (definition[j].isalpha() or definition[j].isnumeric()):
                    j += 1

                nodeName = definition[i: j]
                if len(nodeName) == 1:
                    nfa.push(Graph(nodeName))
                elif nodeName in self.definitionNfa:
                    nfa.push(self.definitionNfa[nodeName])

                i = j
            else:
                if c == Constant.PLUS:
                    # Plus operator
                    nfa.push(GraphUtility.plusClosure(nfa.pop()))
                elif c == Constant.KLEENE:
                    # Kleene Closure
                    nfa.push(GraphUtility.kleeneClosure(nfa.pop()))
                elif c == '(':
                    operator.push(c)
                elif c == Constant.OR:
                    operator.push(c)
                elif c == ')':
                    # Pop until you find a ')'
                    merge.clear()
                    operator.push(c)

                    while operator.pop() != '(':
                        right = nfa.pop()
                        left = nfa.pop()
                        nfa.push(GraphUtility.orr(right, left))

                i += 1

        if nfa.size() == 1:
            return nfa.pop()

        merge.clear()

        while not nfa.is_empty():
            merge.append(nfa.pop())

        mergedGraph = GraphUtility.orr(merge)
        return mergedGraph

    def separateRDByOrs(self, definition: str):

        expression = ''
        rangee = False

        start = Character.MIN_VALUE

        definition = definition.replace(" ", "")

        for c in definition:
            if c.isalpha() or c.isnumeric():
                if not rangee:
                    start = c
                    expression += c
                else:

                    rangee = False
                    separated = None

                    if c in Constant.ALPHABETS:
                        separated = Constant.ALPHABETS
                    elif c in Constant.ALPHABETS.upper():
                        separated = Constant.ALPHABETS.upper()
                    elif c in Constant.DIGITS:
                        separated = Constant.DIGITS

                    # TODO: check if it fails, cuz index() doesnt return -1
                    startIndex = separated.index(start)
                    endIndex = separated.index(c)

                    expression += '|'

                    iterator = startIndex + 1

                    while iterator < endIndex:
                        expression += separated[iterator]
                        expression += '|'
                        iterator += 1

                    expression += separated[endIndex]

            else:
                if not rangee:
                    if c == '-':
                        rangee = True
                    else:
                        expression += c

        return expression

    def getDefinitionNfa(self):
        return self.definitionNfa
