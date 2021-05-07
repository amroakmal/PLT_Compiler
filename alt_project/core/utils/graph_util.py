class GraphUtility:
    @staticmethod
    def orr(one=None, two=None):
        if one is not None and two is None:
            newGraph = Graph(Constant.EPSILON)
            newGraph.getInitialNode().removeAllEdges(Constant.EPSILON)
            for graph in graphs:
                newGraph.getInitialNode().addEdge(Constant.EPSILON, graph.getInitialNode())
                graph.getInitialNode().setStart(False)
                graph.getDestination().addEdge(Constant.EPSILON, newGraph.getDestination())
                graph.getDestination().setEnd(False)

            return newGraph

        if one is not None and two is not None:
            newGraph = Graph(Constant.EPSILON)
            newGraph.getInitialNode().removeAllEdges(Constant.EPSILON)

            newGraph.getInitialNode().addEdge(Constant.EPSILON, one.getInitialNode())
            one.getInitialNode().setStart(False)
            one.getDestination().addEdge(Constant.EPSILON, newGraph.getDestination())
            one.getDestination().setEnd(False)

            newGraph.getInitialNode().addEdge(Constant.EPSILON, two.getInitialNode())
            two.getInitialNode().setStart(False)
            two.getDestination().addEdge(Constant.EPSILON, newGraph.getDestination())
            two.getDestination().setEnd(False)

            return newGraph

    @staticmethod
    def kleeneClosure(graph):

        newGraph = Graph(Constant.EPSILON)
        clonedGraph = Graph(graph)

        newGraph.getInitialNode().addEdge(Constant.EPSILON, clonedGraph.getInitialNode())
        clonedGraph.getInitialNode().setStart(False)
        clonedGraph.getDestination().addEdge(Constant.EPSILON, newGraph.getDestination())
        clonedGraph.getDestination().setEnd(False)
        clonedGraph.getDestination().addEdge(Constant.EPSILON, clonedGraph.getInitialNode())

        return newGraph

    @staticmethod
    def plusClosure(graph):

        newGraph = Graph(Constant.EPSILON)
        newGraph.getInitialNode().removeAllEdges(Constant.EPSILON)
        clonedGraph = Graph(graph)

        newGraph.getInitialNode().addEdge(Constant.EPSILON, clonedGraph.getInitialNode())
        clonedGraph.getInitialNode().setStart(False)
        clonedGraph.getDestination().addEdge(Constant.EPSILON, newGraph.getDestination())
        clonedGraph.getDestination().setEnd(False)
        clonedGraph.getDestination().addEdge(Constant.EPSILON, clonedGraph.getInitialNode())

        return newGraph

    @staticmethod
    def concatenate(firstGraph, secondGraph):
        first = Graph(firstGraph)
        second = Graph(secondGraph)

        first.getDestination().addEdge(Constant.EPSILON, second.getInitialNode())
        first.getDestination().setEnd(False)
        second.getInitialNode().setStart(False)
        first.setDestination(second.getDestination())
        return first
