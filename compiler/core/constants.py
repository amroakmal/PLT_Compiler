class RegexFormats:
    REGULAR_DEFINITION = r"^[ \t]*(\w+)(?: )*=(.+)$"
    REGULAR_EXPRESSION = r"^[ \t]*(\w+)(?: )*:(.+)$"
    KEYWORD = r"^[ \t]*\{(.+)\}$"
    OPERATOR = r"^[ \t]*\[(.+)\]$"
    '''
    match symbols on regex to make it easier to construct NFA for regular expressions
    '''
    SYMBOL = r"[^\\]([^\w\s\d\\\*\+\|\(\)])"


class Constants:
    REGEX_FORMATS = [
        RegexFormats.REGULAR_DEFINITION,
        RegexFormats.REGULAR_EXPRESSION,
        RegexFormats.KEYWORD,
        RegexFormats.OPERATOR,
        RegexFormats.SYMBOL
    ]

    # LEXICAL ANALYZER

    EPSILON = "\\L"
    CONCATENATE = "`"
    OR = "|"
    KLEENE = "*"
    PLUS = "+"

    ALPHABETS = "abcdefghijklmnopqrstuvwxyz"
    DIGITS = "0123456789"
    SEPARATOR = " "
    LEXICAL_SAVING_PATH = "output/lexemes.txt"

    # Valid Operators : * ( ) \\L Math Operators: \\+ \\* / - Comparison Operators
    # : \\= < > Add the \\, To split the regex correctly

    REGEX_OPERATOR = ["*", "+", "|", "`", "(", ")"]
