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
    def construct_lexical_rules(grammar: str):
        rules_store = LexicalRulesStore(grammar)

        if rules_store.is_valid():
            NFACombined = Lexer.getCombinedNFA(rules_store)
            DFA = DFAA(NFACombined)
            minimalDFA = DFAOptimizer(DFA)
            # tokenizer = Tokenizer(minimalDFA, rulesCont.getRegularExpressionsKeys())
            return True
        return False

    @staticmethod
    def getCombinedNFA(rules_cont):
        regular_definition = RegularDefinitionNFA(rules_cont)
        keyword = KeywordNFA(rules_cont)
        punctuation = PunctuationNFA(rules_cont)
        regex = RegularExpressionNFA(rules_cont, regular_definition.get_definition_nfa())
        NFACombined = NFA(regular_definition, keyword, punctuation, regex)
        combinedNFAs = NFACombined.get_combined_graph()
        return combinedNFAs
