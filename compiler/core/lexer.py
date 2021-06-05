from core.models.ITokenizer import ITokenizer
from core.models.dfa.dfa import DFAA
from core.models.dfa.dfa_optimizer import DFAOptimizer
from core.models.nfa.keyword_nfa import KeywordNFA
from core.models.nfa.nfa import NFA

from core.models.nfa.punctuation_nfa import PunctuationNFA
from core.models.nfa.regular_definition_nfa import RegularDefinitionNFA
from core.models.nfa.regular_expression_nfa import RegularExpressionNFA
from core.stores.lexical_rules_store import LexicalRulesStore


class Lexer:
    @staticmethod
    def construct_lexical_rules(grammar: str, program: str):
        rules_store = LexicalRulesStore(grammar)

        if rules_store.is_valid():
            nfa_combined = Lexer.get_combined_nfa(rules_store)
            dfa = DFAA(nfa_combined)
            minimal_dfa = DFAOptimizer(dfa)
            tokenizer = ITokenizer(minimal_dfa, rules_store.get_regular_expressions_keys())
            lexemes = tokenizer.get_tokens(program)

            return lexemes
        return None

    @staticmethod
    def get_combined_nfa(rules_cont):
        regular_definition = RegularDefinitionNFA(rules_cont)
        keyword = KeywordNFA(rules_cont)

        punctuation = PunctuationNFA(rules_cont)
        regex = RegularExpressionNFA(rules_cont, regular_definition.get_definition_nfa())

        nfa_combined = NFA(regular_definition, keyword, punctuation, regex)
        combined_nfas = nfa_combined.get_combined_graph()

        return combined_nfas
