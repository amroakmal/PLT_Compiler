import copy

from compiler.core.models.stack import Stack
from utils.parser_generator import ParserGenerator
from utils.fns import get_next_token


class Parsers:
    def __init__(self, lexer):
        self.lexer = lexer

    def parser_start(self):
        file_out = open("output.txt", 'a')
        parser = ParserGenerator("input_CFG_LL.txt")
        parser.generate()
        pred_table = parser.get_predict_table()
        non_terminals = parser.get_non_terminal()
        terminals = parser.get_terminal()
        productions = parser.get_mod_production()
        parser.print_first_follow()
        parser.print_table()

        file_out.write("\n{:<20}  | {:<20} | {:<20}\n".format("Stack", "Input", "Output"))
        s = Stack()
        left_der = []
        left_row = []
        l_count = 0
        s.push(non_terminals[0])
        left_row.insert(0, non_terminals[0])
        left_der.append(left_row)
        left_row = copy.deepcopy(left_row)
        inp = get_next_token(self.lexer).second
        while not s.is_empty():
            file_out.write("\n${:<20} | {:<20} | ".format(s.peek(), inp))
            if s.peek() not in non_terminals:
                if s.peek() == '\'' + inp + '\'':
                    s.pop()
                    l_count += 1
                    inp = get_next_token(self.lexer).second
                else:
                    if s.peek() == '\L':
                        s.pop()
                        l_count += 1
                    else:
                        file_out.write("Error: unmatched terminal is inserted {} and {}".format(s.peek(), get_next_token(self.lexer).first))
                        s.pop()
                        l_count += 1
            else:
                prod = pred_table[non_terminals.index(s.peek())][terminals.index('\'' + inp + '\'')]
                if prod < 0:
                    file_out.write("Error: input {} is incorrect".format(get_next_token(self.lexer).first))
                    left_row.pop(l_count)
                    while True:
                        if pred_table[non_terminals.index(s.peek())][terminals.index('\'' + inp + '\'')] > 0:
                            break
                        elif pred_table[non_terminals.index(s.peek())][terminals.index('\'' + inp + '\'')] == -2:
                            s.pop()
                            break
                        elif get_next_token(self.lexer).second == '$':
                            s.pop()
                            break
                        else:
                            inp = get_next_token(self.lexer).second
                else:
                    s.pop()
                    left_row.pop(l_count)
                    file_out.write("{:<20}".format(productions[prod]))
                    right = productions[prod].split("=", 1)[1].strip()
                    list_cand = right.split(" ")
                    left_row[l_count:l_count] = list_cand
                    left_der.append(left_row)
                    left_row = copy.deepcopy(left_row)
                    list_cand.reverse()
                    for x in list_cand:
                        s.push(x)

        if inp == '$':
            file_out.write('Accepted\n')
        else:
            file_out.write('Rejected\n')

        file_out.write("\n--> leftmost derivation sententials\n")
        for x in left_der:
            file_out.write(str(x))
            file_out.write("\n")
        file_out.write("\n--> Last raw after removing \'\\L\'\n")
        file_out.write(str(list(filter(('\L').__ne__, left_row))))
        file_out.close()

