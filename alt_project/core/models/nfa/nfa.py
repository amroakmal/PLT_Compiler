from core.utils.graph_util import GraphUtility


class NFA:
    def __init__(self, regularDefinition, keyword, punctuation, regex):
        self.combinedNfa = []
        self.combinedGraph = None
        self.combine(keyword, punctuation, regex)

    def addToList(self, keyword, punctuation, regex):
        for key, value in punctuation.getPunctuationNfa().items():
            self.combinedNfa.append(value)

        for key, value in keyword.getKeywordNfa().items():
            self.combinedNfa.append(value)

        for key, value in regex.getRegExpressionNfa().items():
            self.combinedNfa.append(value)

    def getCombinedGraph(self):
        return self.combinedGraph

    def combine(self, keyword, punctuation, regex):
        self.addToList(keyword, punctuation, regex)
        self.combinedGraph = GraphUtility.orr(self.combinedNfa)
