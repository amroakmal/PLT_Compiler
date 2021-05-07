from core.utils.graph_util import GraphUtility


class NFA:
    def __init__(self, regular_definition, keyword, punctuation, regex):
        self.combined_nfa = []
        self.combined_graph = None
        self.combine(keyword, punctuation, regex)

    def add_to_list(self, keyword, punctuation, regex):
        for key, value in punctuation.get_punctuation_nfa().items():
            self.combined_nfa.append(value)

        for key, value in keyword.get_keyword_nfa().items():
            self.combined_nfa.append(value)

        for key, value in regex.get_reg_expression_nfa().items():
            self.combined_nfa.append(value)

    def get_combined_graph(self):
        return self.combined_graph

    def combine(self, keyword, punctuation, regex):
        self.add_to_list(keyword, punctuation, regex)
        self.combined_graph = GraphUtility.orr(self.combined_nfa)
