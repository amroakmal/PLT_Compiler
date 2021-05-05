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
