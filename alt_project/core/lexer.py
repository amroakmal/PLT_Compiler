from core.models.nfa.keyword_nfa import KeywordNFA
from core.models.nfa.nfa import NFA
from core.models.nfa.punctuation_nfa import PunctuationNFA
from core.models.nfa.regular_definition_nfa import RegularDefinitionNFA
from core.models.nfa.regular_expression_nfa import RegularExpressionNFA
from core.stores.lexical_rules_store import LexicalRulesStore


class Lexer:
    @staticmethod
    def construct_lexical_rules(grammar: str):
        rulesCont = LexicalRulesStore(grammar)

        if rulesCont.isValid():
            NFACombined = Lexer.getCombinedNFA(rulesCont)
            DFA = DFA(NFACombined)
            minimalDFA = DFAOptimizer(DFA)
            tokenizer = Tokenizer(minimalDFA, rulesCont.getRegularExpressionsKeys())
            return True
        return False

    @staticmethod
    def getCombinedNFA(rulesCont):
        regularDefinition = RegularDefinitionNFA(rulesCont)
        keyword = KeywordNFA(rulesCont)
        punctuation = PunctuationNFA(rulesCont)
        regex = RegularExpressionNFA(rulesCont, regularDefinition.getDefinitionNfa())
        NFACombined = NFA(regularDefinition, keyword, punctuation, regex)
        combinedNFAs = NFACombined.getCombinedGraph()
        return combinedNFAs
