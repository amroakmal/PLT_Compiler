from core.constants import Constants
from core.models.graph.graph import Graph
from core.models.stack import Stack
from core.utils.graph_util import GraphUtility
from core.utils.nfa_util import NfaUtility


class KeywordNFA:
    def __init__(self, rulesCont):
        self.keywordNfa = {}
        self.keywordToNfa(rulesCont)

    def keywordToNfa(self, lexicalRulesStore):
        for keyword in lexicalRulesStore.getKeywords():
            keywordCharacters = keyword.split('')
            characters = NfaUtility.addConcatSymbolToWords(keywordCharacters)
            postFixExpression = NfaUtility.infixToPostFix(characters)
            nfa = self.createNfa(postFixExpression)
            self.keywordNfa[keyword] = nfa
            nfa.getDestination().setNodeTypes(keyword)

    def createNfa(self, expression):
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

    def getKeywordNfa(self):
        return self.keywordNfa
