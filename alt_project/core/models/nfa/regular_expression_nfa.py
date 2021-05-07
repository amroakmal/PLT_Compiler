from core.constants import Constants
from core.models.graph.graph import Graph
from core.models.stack import Stack
from core.utils.graph_util import GraphUtility
from core.utils.nfa_util import NfaUtility


class RegularExpressionNFA:
    def __init__(self, rulesCont, definitionNfa):
        self.regExpressionNfa = {}
        self.definitionNfa = definitionNfa
        self.lexicalRulesStore = rulesCont
        self.backlashSymbols = self.generateSymbols()
        self.regexToNfa(rulesCont)

    def regexToNfa(self, lexicalRulesStore):
        for definitionKey in lexicalRulesStore.getRegularExpressionsKeys():
            definitionValue = lexicalRulesStore.getRegularExpression(definitionKey)
            definitionValue = definitionValue.replace(" ", "")

            words = self.separateRegularExpression(definitionValue)
            words = self.addConcatSymbolToRegex(words)
            postFixExpression = NfaUtility.infixToPostFix(words)
            nfa = self.createNfa(postFixExpression)
            self.regExpressionNfa[definitionKey] = nfa
            nfa.getDestination().setNodeTypes(definitionKey)

    def separateRegularExpression(self, regex):
        result = []
        symbols = self.lexicalRulesStore.getSymbols()

        i = 0
        while i < len(regex):
            # To keep track of the last valid definition/operator
            j = i + 1
            k = i + 1
            while k < len(regex):
                # K + 1 - > Substring is exclusive
                temp = regex[i: k + 1]
                if temp in self.definitionNfa or temp in symbols or temp in self.backlashSymbols:
                    # Don't break from the loop (Digit / Digit(s))
                    j = k + 1

                k += 1

            result.append(regex[i: j])
            i = j

        return result

    def addConcatSymbolToRegex(self, word):
        output = [word[0]]

        for w in word:

            # If current letter is ( and previous not equal | -> digit | (digits)
            if output[len(output) - 1] != Constants.OR and w == "(":
                output.append(Constants.CONCATENATE)

            # If 2 words
            if not NfaUtility.isRegexOperator(output[len(output) - 1]) and not NfaUtility.isRegexOperator(w):
                output.append(Constants.CONCATENATE)

                # If the previous is * or + and the next is not or
                if NfaUtility.isKleeneOrPlus(output[len(output) - 1]) and w != "|":
                    output.append(Constants.CONCATENATE)

            output.append(w)

        return output

    def createNfa(self, expression):
        # create a stack
        nfa = Stack()
        # Scan all characters one by one
        for currentExpression in expression:
            if NfaUtility.isRegexOperator(currentExpression):
                if currentExpression == Constants.KLEENE:
                    g = nfa.pop()
                    nfa.push(GraphUtility.kleeneClosure(g))
                elif currentExpression == Constants.PLUS:
                    g = nfa.pop()
                    nfa.push(GraphUtility.plusClosure(g))
                elif currentExpression == Constants.OR:
                    right = nfa.pop()
                    left = nfa.pop()
                    nfa.push(GraphUtility.orr(right, left))
                elif currentExpression == Constants.CONCATENATE:
                    right = nfa.pop()
                    left = nfa.pop()
                    nfa.push(GraphUtility.concatenate(left, right))

            else:
                if currentExpression in self.definitionNfa:
                    g = Graph(self.definitionNfa[currentExpression])
                    nfa.push(g)
                elif currentExpression in self.backlashSymbols and currentExpression != "\\L":
                    nodeName = currentExpression[1:]
                    nfa.push(Graph(nodeName))
                else:
                    nfa.push(Graph(currentExpression))

        return nfa.pop()

    def generateSymbols(self):
        result = []

        for s in self.lexicalRulesStore.getOperators():
            if s[0] == "\\":
                result.append(s)

        for s in self.lexicalRulesStore.getRegularExpressionsKeys():
            regularExpression = self.lexicalRulesStore.getRegularExpression(s)
            i = 0

            while i < len(regularExpression):
                c = regularExpression[i]
                if c == '\\':
                    result.append("\\" + regularExpression[i + 1])
                    i += 2
                else:
                    i += 1

        return NfaUtility.removeDuplicates(result)

    def getRegExpressionNfa(self):
        return self.regExpressionNfa

    def getBackSlashSymbols(self):
        return self.backlashSymbols
