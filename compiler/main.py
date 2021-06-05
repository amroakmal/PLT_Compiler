from core.lexer import Lexer
from Parsers import Parsers
from utils.fns import get_next_token

from utils.io_manager import IOManager

if __name__ == '__main__':
    grammar = IOManager.read_file('grammar.txt')
    program = IOManager.read_file('program.txt')

    import os
    if os.path.exists("output.txt"):
        os.remove("output.txt")

    result1 = Lexer.construct_lexical_rules(grammar, program)

    file_out = open("output.txt", 'a')
    if result1 is not None:
        file_out.write("successful !\n")
        file_out.close()
        P = Parsers(result1)
        P.parser_start()
    else:
        file_out.write("Failed !\n")
        file_out.close()
