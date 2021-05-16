import os
from PLT_Compiler.alt_project.utils.io_manager import IOManager


class Tokenizer:

    SYMBOL_ERROR = "\0"

    def __init__(self, inp1=None, inp2=None):

        if isinstance(inp1, str):
            data = IOManager.read_file(inp1)
            tokens = data.split(os.linesep)
            self.savedLexems = []
            for token in tokens:
                self.savedLexems.append(("", token))
            self.validTokenization = True

        else:
            self.minimalDFA = inp1.getDFAMinimized()
            self.transitionTable = inp1.getFinalStates()
            self.regularExpressions = inp2;
            self.validTokenization = True;

    def getTokens(self, inp):
        start = self.minimalDFA.getInitialNode()
        idx = 0
        self.savedLexems = []
        self.validTokenization = True
        first = True

        while idx < len(inp) or first is True:
            first = False
            retvalue = self.addGenerations(inp, idx, idx, self.savedLexems, start)
            if retvalue == -1:
                idx = self.getUknownSymbol(inp, idx, self.savedLexems)
                self.validTokenization = False

            elif retvalue == -2:
                idx += 1
                self.savedLexems.append(("", ""))

            else:
                idx = retvalue + 1

        self.sanitizeLexems(self.savedLexems)
        return self.savedLexems

    def addGenerations(self, inp, startIdx, idx, lexems, currNode):
        if idx >= len(inp):
            return -2
        currentChar = inp[idx]
        if currentChar == ' ' or currentChar == '\n' or currentChar == '\r' or currentChar == '\t':
            return -2
        transition = str(currNode.getCurrentId()) + " " + inp[idx]
        nextTransition = self.transitionTable.get(transition)
        if nextTransition is not None:
            acceptanceStates = nextTransition.getValue().split(" ")
            acceptance = self.getAcceptanceState(acceptanceStates, inp[startIdx:idx + 1])
            retValue = self.addGenerations(inp, startIdx, idx + 1, lexems, nextTransition.getKey())
            if retValue == -1 or retValue == -2:
                if acceptance == "":
                    return -1
                lexems.append((inp[startIdx:idx + 1], acceptance))
                return idx
            else:
                return retValue
        return -1

    def getAcceptanceState(self, acceptanceStates, inp):
        if len(acceptanceStates) == 1:
            return acceptanceStates[0]
        for s in acceptanceStates:
            if inp == s:
                return inp
        for reg in self.regularExpressions:
            for s in acceptanceStates:
                if reg == s:
                    return reg
        return inp

    # returns index to the start of the new valid inputs
    def getUknownSymbol(self, inp, startIdx, lexems):
        appendedMatches = self.removeIncorrectMatches(lexems)
        idx = startIdx
        startNode = self.minimalDFA.getInitialNode()
        first = True
        retvalue = 0

        while retvalue != -2 or first is True:
            first = False
            retvalue = self.addGenerations(inp, idx, idx, lexems, startNode)
            if retvalue == -1:
                appendedMatches += inp[idx]
                idx += 1

            elif retvalue != -2:
                if self.isRegex(lexems[len(lexems) - 1][1]):
                    appendedMatches += lexems[len(lexems) - 1][0]
                    idx = retvalue + 1
                else:  # keyword or operator found so just pop it and break [ works like a separator ]
                    lexems.pop(len(lexems) - 1)
                    break
        self.removeIncorrectMatches(lexems)
        lexems.append((appendedMatches, self.SYMBOL_ERROR))
        return idx

    def removeIncorrectMatches(self, lexems):
        appendedMatches = ""
        while len(lexems) > 0:
            lastMatch = lexems[len(lexems) - 1]
            if not self.isRegex(lastMatch[1]):
                break
            appendedMatches += lastMatch[0]
            lexems.pop(len(lexems) - 1)
        return appendedMatches

    def isRegex(self, match):
        for reg in self.regularExpressions:
            if reg == match:
                return True

    def sanitizeLexems(self, lexems):
        idx = 0
        size = len(lexems)
        while idx < size:
            if lexems[idx][0] == "":
                lexems.pop(idx)
                size -= 1
            else:
                idx += 1

    def getSavedLexems(self):
        return self.savedLexems

    def getTransitionTable(self):
        return self.transitionTable

    def isValidTokenization(self):
        return self.validTokenization
