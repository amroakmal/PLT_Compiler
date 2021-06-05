from core.models.graph.graph import Graph
from core.models.stack import Stack
from core.utils.nfa_util import NfaUtility


class PunctuationNFA:
    def __init__(self, rules_cont):
        self.punctuation_nfa = {}
        self.punctuation_to_nfa(rules_cont)

    def punctuation_to_nfa(self, lexical_rules_store):

        for operator in lexical_rules_store.get_operators():
            operator = operator.replace("\\", "")
            operator_characters = list(operator)
            characters = NfaUtility.add_concat_symbol_to_words(operator_characters)
            post_fix_expression = NfaUtility.infix_to_post_fix(characters)
            nfa = self.create_nfa(post_fix_expression)
            self.punctuation_nfa[operator] = nfa
            nfa.get_destination().set_node_types(operator)

    def create_nfa(self, expression):
        # create a stack
        nfa = Stack()

        # Scan all characters one by one
        for currentExpression in expression:
            nfa.push(Graph(currentExpression))

            return nfa.pop()

    def get_punctuation_nfa(self):
        return self.punctuation_nfa
