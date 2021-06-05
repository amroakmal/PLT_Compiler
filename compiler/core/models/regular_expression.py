import re

from core.constants import Constants


class RegularExpression:
    def __init__(self, key: str, value: str):
        self.key = key
        self.value = value

    def add_rule(self, store):
        matches = re.finditer(Constants.REGEX_FORMATS[4], self.value)

        for matchNum, match in enumerate(matches, start=1):
            for group_num in range(0, len(match.groups())):
                group_num = group_num + 1
                store.add_symbol(match.group(group_num))

        store.put_regular_expression(self.key, self.value)
