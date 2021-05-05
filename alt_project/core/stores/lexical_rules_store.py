import re

from core.utils.lexical_line_processor import LexicalLineProcessor


class LexicalRulesStore:
    def __init__(self, grammar: str):
        # init class attributes

        self._regularDefinitions = {}
        self._regularDefinitionsKeys = []
        self._regularExpressions = {}
        self._regularExpressionsKeys = []
        self._operators = []
        self._keywords = []
        self._symbols = []

        # regex search for each one of the elements and save them

        self.hasErrors = self.processRules(grammar)

    def isValid(self):
        return self.hasErrors

    def getRegularDefinition(self, key: str):
        return self._regularDefinitions[key]

    def getRegularExpression(self, key: str):
        return self._regularExpressions[key]

    def getKeyword(self, idx: int):
        return self._keywords[idx]

    def getOperator(self, idx: int):
        return self._operators[idx]

    def processRules(self, rules: str):
        lines = re.compile(r"\r?\n").split(rules)

        for line in lines:
            if line == '':
                continue
            if not LexicalLineProcessor.getInstance().processLine(line, self):
                return False

        return True

    def getRegularDefinitionsKeys(self):
        return self._regularDefinitionsKeys

    def getRegularExpressionsKeys(self):
        return self._regularExpressionsKeys

    def getSymbols(self):
        return self._symbols

    # default functions for ParserLineProcessor to use

    def putRegularDefinition(self, key: str, val: str):
        self._regularDefinitions[key] = val
        self._regularDefinitionsKeys.append(key)

    def putRegularExpression(self, key: str, val: str):
        self._regularExpressions[key] = val
        self._regularExpressionsKeys.append(key)

    def addKeyword(self, key: str):
        self._keywords.append(key)

    def addOperator(self, op: str):
        self._operators.append(op)

    def addSymbol(self, symbol: str):
        if symbol not in self._symbols:
            self._symbols.append(symbol)

    def getOperators(self):
        return self._operators

    def getKeywords(self):
        return self._keywords
