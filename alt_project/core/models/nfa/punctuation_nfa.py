from core.models.stack import Stack
from core.utils.nfa_util import NfaUtility


class PunctuationNFA:
    def __init__(self, rulesCont):
        self.punctuationNfa = {}
        self.punctuationToNfa(rulesCont)

    def punctuationToNfa(self, lexicalRulesStore):

        for operator in lexicalRulesStore.getOperators():
            operator = operator.replace("\\", "")
            operatorCharacters = operator.split("")
            characters = NfaUtility.addConcatSymbolToWords(operatorCharacters)
            postFixExpression = NfaUtility.infixToPostFix(characters)
            nfa = self.createNfa(postFixExpression)
            self.punctuationNfa[operator] = nfa
            nfa.getDestination().setNodeTypes(operator)

    def createNfa(self, expression):
        # create a stack
        nfa = Stack()

        # Scan all characters one by one
        for currentExpression in expression:
            nfa.push(Graph(currentExpression))

            return nfa.pop()

    def getPunctuationNfa(self):
        return self.punctuationNfa
