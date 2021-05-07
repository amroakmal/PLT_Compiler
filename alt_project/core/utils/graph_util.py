from core.constants import Constants
from core.models.graph.graph import Graph


class GraphUtility:
    @staticmethod
    def orr(one=None, two=None):
        if one is not None and two is None:
            newGraph = Graph(Constants.EPSILON)
            newGraph.getInitialNode().removeAllEdges(Constants.EPSILON)
            for graph in one:
                newGraph.getInitialNode().addEdge(Constants.EPSILON, graph.getInitialNode())
                graph.getInitialNode().setStart(False)
                graph.getDestination().addEdge(Constants.EPSILON, newGraph.getDestination())
                graph.getDestination().setEnd(False)

            return newGraph

        if one is not None and two is not None:
            newGraph = Graph(Constants.EPSILON)
            newGraph.getInitialNode().removeAllEdges(Constants.EPSILON)

            newGraph.getInitialNode().addEdge(Constants.EPSILON, one.getInitialNode())
            one.getInitialNode().setStart(False)
            one.getDestination().addEdge(Constants.EPSILON, newGraph.getDestination())
            one.getDestination().setEnd(False)

            newGraph.getInitialNode().addEdge(Constants.EPSILON, two.getInitialNode())
            two.getInitialNode().setStart(False)
            two.getDestination().addEdge(Constants.EPSILON, newGraph.getDestination())
            two.getDestination().setEnd(False)

            return newGraph

    @staticmethod
    def kleeneClosure(graph):

        newGraph = Graph(Constants.EPSILON)
        clonedGraph = Graph(graph)

        newGraph.getInitialNode().addEdge(Constants.EPSILON, clonedGraph.getInitialNode())
        clonedGraph.getInitialNode().setStart(False)
        clonedGraph.getDestination().addEdge(Constants.EPSILON, newGraph.getDestination())
        clonedGraph.getDestination().setEnd(False)
        clonedGraph.getDestination().addEdge(Constants.EPSILON, clonedGraph.getInitialNode())

        return newGraph

    @staticmethod
    def plusClosure(graph):

        newGraph = Graph(Constants.EPSILON)
        newGraph.getInitialNode().removeAllEdges(Constants.EPSILON)
        clonedGraph = Graph(graph)

        newGraph.getInitialNode().addEdge(Constants.EPSILON, clonedGraph.getInitialNode())
        clonedGraph.getInitialNode().setStart(False)
        clonedGraph.getDestination().addEdge(Constants.EPSILON, newGraph.getDestination())
        clonedGraph.getDestination().setEnd(False)
        clonedGraph.getDestination().addEdge(Constants.EPSILON, clonedGraph.getInitialNode())

        return newGraph

    @staticmethod
    def concatenate(firstGraph, secondGraph):
        first = Graph(firstGraph)
        second = Graph(secondGraph)

        first.getDestination().addEdge(Constants.EPSILON, second.getInitialNode())
        first.getDestination().setEnd(False)
        second.getInitialNode().setStart(False)
        first.setDestination(second.getDestination())
        return first
