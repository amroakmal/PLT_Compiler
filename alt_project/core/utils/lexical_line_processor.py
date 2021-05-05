import re

from core.constants import Constants
from core.models.keywords import Keywords
from core.models.operators import Operators
from core.models.regular_definition import RegularDefinition
from core.models.regular_expression import RegularExpression


class LexicalLineProcessor:
    instance = None

    @staticmethod
    def getInstance():
        if LexicalLineProcessor.instance is None:
            LexicalLineProcessor.instance = LexicalLineProcessor()
        return LexicalLineProcessor.instance

    @staticmethod
    def processLine(line: str, store):
        lineRules = None

        for idx, reg in enumerate(Constants.REGEX_FORMATS):
            regex = re.compile(reg)
            match = regex.search(line)

            if match is not None:
                if idx == 0:
                    lineRules = RegularDefinition(match.group(1), match.group(2))
                    print('line:: ' + line + '  ---> type: def')
                    break
                if idx == 1:
                    lineRules = RegularExpression(match.group(1), match.group(2))
                    print('line:: ' + line + '  ---> type: exp')
                    break
                if idx == 2:
                    lineRules = Keywords(match.group(1))
                    print('line:: ' + line + '  ---> type: key')
                    break
                if idx == 3:
                    lineRules = Operators(match.group(1))
                    print('line:: ' + line + '  ---> type: op')
                    break

        if lineRules is None:
            return False

        lineRules.addRule(store)
        return True
