from core.constants import Constants
from core.models.graph.graph import Graph
from core.models.stack import Stack
from core.utils.graph_util import GraphUtility
from core.utils.nfa_util import NfaUtility


class KeywordNFA:
    def __init__(self, rules_cont):
        self.keyword_nfa = {}
        self.keyword_to_nfa(rules_cont)

    def keyword_to_nfa(self, lexical_rules_store):
        for keyword in lexical_rules_store.get_keywords():
            keyword_characters = list(keyword)
            characters = NfaUtility.add_concat_symbol_to_words(keyword_characters)
            post_fix_expression = NfaUtility.infix_to_post_fix(characters)
            nfa = self.create_nfa(post_fix_expression)
            self.keyword_nfa[keyword] = nfa
            nfa.get_destination().set_node_types(keyword)

    def create_nfa(self, expression):
        # create a stack
        nfa = Stack()

        # Scan all characters one by one
        for currentExpression in expression:
            if currentExpression == Constants.CONCATENATE:
                right = nfa.pop()
                left = nfa.pop()
                nfa.push(GraphUtility.concatenate(left, right))
            else:
                nfa.push(Graph(currentExpression))

        return nfa.pop()

    def get_keyword_nfa(self):
        return self.keyword_nfa
