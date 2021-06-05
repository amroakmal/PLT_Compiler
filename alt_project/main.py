from core.lexer import Lexer
from utils.fns import get_next_token

from utils.io_manager import IOManager

if __name__ == '__main__':
    grammar = IOManager.read_file('grammar.txt')
    program = IOManager.read_file('program.txt')

    result1 = Lexer.construct_lexical_rules(grammar, program)

    if result1 is not None:
        print("successful !")
        print(get_next_token(result1))
    else:
        print("Failed !")
