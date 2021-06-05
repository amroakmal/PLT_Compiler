from core.constants import Constants
from core.models.graph.graph import Graph


class GraphUtility:
    @staticmethod
    def orr(one=None, two=None):
        if one is not None and two is None:
            new_graph = Graph(Constants.EPSILON)
            new_graph.get_initial_node().remove_all_edges(Constants.EPSILON)
            for graph in one:
                new_graph.get_initial_node().add_edge(Constants.EPSILON, graph.get_initial_node())
                graph.get_initial_node().set_start(False)
                graph.get_destination().add_edge(Constants.EPSILON, new_graph.get_destination())
                graph.get_destination().set_end(False)

            return new_graph

        if one is not None and two is not None:
            new_graph = Graph(Constants.EPSILON)
            new_graph.get_initial_node().remove_all_edges(Constants.EPSILON)

            new_graph.get_initial_node().add_edge(Constants.EPSILON, one.get_initial_node())
            one.get_initial_node().set_start(False)
            one.get_destination().add_edge(Constants.EPSILON, new_graph.get_destination())
            one.get_destination().set_end(False)

            new_graph.get_initial_node().add_edge(Constants.EPSILON, two.get_initial_node())
            two.get_initial_node().set_start(False)
            two.get_destination().add_edge(Constants.EPSILON, new_graph.get_destination())
            two.get_destination().set_end(False)

            return new_graph

    @staticmethod
    def kleene_closure(graph):

        new_graph = Graph(Constants.EPSILON)
        cloned_graph = Graph(graph)

        new_graph.get_initial_node().add_edge(Constants.EPSILON, cloned_graph.get_initial_node())
        cloned_graph.get_initial_node().set_start(False)
        cloned_graph.get_destination().add_edge(Constants.EPSILON, new_graph.get_destination())
        cloned_graph.get_destination().set_end(False)
        cloned_graph.get_destination().add_edge(Constants.EPSILON, cloned_graph.get_initial_node())

        return new_graph

    @staticmethod
    def plus_closure(graph):

        new_graph = Graph(Constants.EPSILON)
        new_graph.get_initial_node().remove_all_edges(Constants.EPSILON)
        cloned_graph = Graph(graph)

        new_graph.get_initial_node().add_edge(Constants.EPSILON, cloned_graph.get_initial_node())
        cloned_graph.get_initial_node().set_start(False)
        cloned_graph.get_destination().add_edge(Constants.EPSILON, new_graph.get_destination())
        cloned_graph.get_destination().set_end(False)
        cloned_graph.get_destination().add_edge(Constants.EPSILON, cloned_graph.get_initial_node())

        return new_graph

    @staticmethod
    def concatenate(first_graph, second_graph):
        first = Graph(first_graph)
        second = Graph(second_graph)

        first.get_destination().add_edge(Constants.EPSILON, second.get_initial_node())
        first.get_destination().set_end(False)
        second.get_initial_node().set_start(False)
        first.set_destination(second.get_destination())
        return first
