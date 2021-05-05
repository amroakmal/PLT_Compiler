from core.lexer import Lexer

from utils.io_manager import IOManager

if __name__ == '__main__':
    grammar = IOManager.read_file('grammar.txt')
    program = IOManager.read_file('program.txt')

    if Lexer.construct_lexical_rules(grammar):
        print("Generated DFA successfully !")
    else:
        print("Incorrect grammar format !")
