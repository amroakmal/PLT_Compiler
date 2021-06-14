from core.lexer import Lexer
from Parsers import Parsers
from utils.fns import get_next_token

from utils.io_manager import IOManager

if __name__ == '__main__':
    grammar = IOManager.read_file('grammar.txt')
    program = IOManager.read_file('program.txt').lower()

    import os
    if os.path.exists("output.txt"):
        os.remove("output.txt")

    result1 = Lexer.construct_lexical_rules(grammar, program)

    # ------------------------------------------------------------
    file_out = open("tokens.txt", 'a')
    for pair in result1:
        file_out.write(pair.first + " ---> " + pair.second + '\n')
    file_out.close()
    # ------------------------------------------------------------

    if result1 is not None:
        print("Lexer successful !\n")
        P = Parsers(result1)
        P.parser_start()
    else:
        print("Lexer Failed !\n")
