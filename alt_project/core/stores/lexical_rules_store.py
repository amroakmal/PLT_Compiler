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

        self.hasErrors = self.process_rules(grammar)

    def is_valid(self):
        return self.hasErrors

    def get_regular_definition(self, key: str):
        return self._regularDefinitions[key]

    def get_regular_expression(self, key: str):
        return self._regularExpressions[key]

    def get_keyword(self, idx: int):
        return self._keywords[idx]

    def get_operator(self, idx: int):
        return self._operators[idx]

    def process_rules(self, rules: str):
        lines = re.compile(r"\r?\n").split(rules)

        for line in lines:
            if line == '':
                continue
            if not LexicalLineProcessor.get_instance().process_line(line, self):
                return False

        return True

    def get_regular_definitions_keys(self):
        return self._regularDefinitionsKeys

    def get_regular_expressions_keys(self):
        return self._regularExpressionsKeys

    def get_symbols(self):
        return self._symbols

    # default functions for ParserLineProcessor to use

    def put_regular_definition(self, key: str, val: str):
        self._regularDefinitions[key] = val
        self._regularDefinitionsKeys.append(key)

    def put_regular_expression(self, key: str, val: str):
        self._regularExpressions[key] = val
        self._regularExpressionsKeys.append(key)

    def add_keyword(self, key: str):
        self._keywords.append(key)

    def add_operator(self, op: str):
        self._operators.append(op)

    def add_symbol(self, symbol: str):
        if symbol not in self._symbols:
            self._symbols.append(symbol)

    def get_operators(self):
        return self._operators

    def get_keywords(self):
        return self._keywords
