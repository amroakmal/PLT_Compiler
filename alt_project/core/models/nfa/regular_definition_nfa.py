from core.constants import Constants
from core.models.graph.graph import Graph
from core.models.stack import Stack
from core.utils.graph_util import GraphUtility


class RegularDefinitionNFA:
    def __init__(self, rules_cont):
        self.definitionNfa = {}
        self.definitions_to_nfa(rules_cont)

    def definitions_to_nfa(self, lexical_rules_store):
        for idx, val in enumerate(lexical_rules_store.get_regular_definitions_keys()):
            definition_key = lexical_rules_store.get_regular_definitions_keys()[idx]
            definition_value = lexical_rules_store.get_regular_definition(definition_key)

            definition_value = self.separate_rd_by_ors(definition_value)

            current_definition_nfa = self.create_nfa(definition_value)
            self.definitionNfa[definition_key] = current_definition_nfa

    def create_nfa(self, definition: str):

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

                node_name = definition[i: j]
                if len(node_name) == 1:
                    nfa.push(Graph(node_name))
                elif node_name in self.definitionNfa:
                    nfa.push(self.definitionNfa[node_name])

                i = j
            else:
                if c == Constants.PLUS:
                    # Plus operator
                    nfa.push(GraphUtility.plus_closure(nfa.pop()))
                elif c == Constants.KLEENE:
                    # Kleene Closure
                    nfa.push(GraphUtility.kleene_closure(nfa.pop()))
                elif c == '(':
                    operator.push(c)
                elif c == Constants.OR:
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

        merged_graph = GraphUtility.orr(merge)
        return merged_graph

    def separate_rd_by_ors(self, definition: str):

        expression = ''
        rangee = False

        start = '_'

        definition = definition.replace(" ", "")

        for c in definition:
            if c.isalpha() or c.isnumeric():
                if not rangee:
                    start = c
                    expression += c
                else:

                    rangee = False
                    separated = None

                    if c in Constants.ALPHABETS:
                        separated = Constants.ALPHABETS
                    elif c in Constants.ALPHABETS.upper():
                        separated = Constants.ALPHABETS.upper()
                    elif c in Constants.DIGITS:
                        separated = Constants.DIGITS

                    start_index = separated.index(start)
                    end_index = separated.index(c)

                    expression += '|'

                    iterator = start_index + 1

                    while iterator < end_index:
                        expression += separated[iterator]
                        expression += '|'
                        iterator += 1

                    expression += separated[end_index]

            else:
                if not rangee:
                    if c == '-':
                        rangee = True
                    else:
                        expression += c

        return expression

    def get_definition_nfa(self):
        return self.definitionNfa
