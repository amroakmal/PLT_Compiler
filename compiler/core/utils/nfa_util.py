from core.constants import Constants
from core.models.stack import Stack


class NfaUtility:
    @staticmethod
    def precedence(c):
        if c == Constants.KLEENE or c == Constants.PLUS:
            return 4
        if c == Constants.CONCATENATE:
            return 3
        if c == Constants.OR:
            return 2
        return -1

    @staticmethod
    def infix_to_post_fix(expression):

        result = []
        stack = Stack()

        for c in expression:
            if NfaUtility.precedence(c) > 0:
                while not stack.is_empty() and NfaUtility.precedence(stack.peek()) >= NfaUtility.precedence(c):
                    result.append(stack.pop())
                stack.push(c)
            elif c == ")":
                if len(expression) != 1:

                    while not stack.is_empty() and stack.peek() != "(":
                        result.append(stack.pop())

                    stack.pop()
                else:
                    stack.push(c)

            elif c == "(":
                stack.push(c)
            else:  # Character is neither operator nor (
                result.append(c)

        while not stack.is_empty():
            result.append(stack.pop())

        return result

    @staticmethod
    def add_concat_symbol_to_words(word):
        output = []
        for w in word:
            output.append(w)
            output.append(Constants.CONCATENATE)

        output.pop()
        return output

    @staticmethod
    def is_kleene_or_plus(character):
        return character == Constants.KLEENE or character == Constants.PLUS

    @staticmethod
    def is_regex_operator(character):
        for s in Constants.REGEX_OPERATOR:
            if s == character:
                return True

        return False

    @staticmethod
    def remove_duplicates(inp):
        result = []
        for s in inp:
            if s not in result:
                result.append(s)

        return result
