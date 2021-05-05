import re

from core.constants import Constants


class RegularExpression:
    def __init__(self, key: str, value: str):
        self.key = key
        self.value = value

    def addRule(self, store):
        matches = re.finditer(Constants.REGEX_FORMATS[4], self.value)

        for matchNum, match in enumerate(matches, start=1):
            for groupNum in range(0, len(match.groups())):
                groupNum = groupNum + 1
                store.addSymbol(match.group(groupNum))

        store.putRegularExpression(self.key, self.value)
