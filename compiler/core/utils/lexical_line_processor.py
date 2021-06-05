import re

from core.constants import Constants
from core.models.keywords import Keywords
from core.models.operators import Operators
from core.models.regular_definition import RegularDefinition
from core.models.regular_expression import RegularExpression


class LexicalLineProcessor:
    instance = None

    @staticmethod
    def get_instance():
        if LexicalLineProcessor.instance is None:
            LexicalLineProcessor.instance = LexicalLineProcessor()
        return LexicalLineProcessor.instance

    @staticmethod
    def process_line(line: str, store):
        line_rules = None

        for idx, reg in enumerate(Constants.REGEX_FORMATS):
            regex = re.compile(reg)
            match = regex.search(line)

            if match is not None:
                if idx == 0:
                    line_rules = RegularDefinition(match.group(1), match.group(2))
                    print('line:: ' + line + '  ---> type: def')
                    break
                if idx == 1:
                    line_rules = RegularExpression(match.group(1), match.group(2))
                    print('line:: ' + line + '  ---> type: exp')
                    break
                if idx == 2:
                    line_rules = Keywords(match.group(1))
                    print('line:: ' + line + '  ---> type: key')
                    break
                if idx == 3:
                    line_rules = Operators(match.group(1))
                    print('line:: ' + line + '  ---> type: op')
                    break

        if line_rules is None:
            return False

        line_rules.add_rule(store)
        return True