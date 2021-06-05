from utils.parser_generator import ParserGenerator


class Parsers:
    @staticmethod
    def parser_start():
        parser = ParserGenerator("input_CFG_LL.txt")
        parser.generate()
        pred_table = parser.get_predict_table()
        parser.print_table()
