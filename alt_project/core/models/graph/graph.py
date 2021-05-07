import node


class Graph:

    def __init__(self, inp=None):
        if inp is None:
            self.initialNode = node.Node(True, False, None)

        elif isinstance(inp, str):
            self.initialNode = node.Node(True, False, None)
            self.destination = node.Node(False, True, None)
            self.initialNode.addEdge(inp, self.destination)

        elif isinstance(inp, Graph):
            self.initialNode = node.Node(inp.initialNode, None, None)
            old_to_new = {
                inp.initialNode: self.initialNode
            }
            visited = [False] * node.Node.id
            self.clone_dfs(inp.initialNode, visited, old_to_new)
            self.destination = old_to_new.get(inp.destination)

    def clone_dfs(self, n, visited, old_to_new):
        if visited[n.getCurrentId()]:
            return
        visited[n.getCurrentId()] = True
        for k, v in n.getMap():
            for i in v:
                if i not in old_to_new:
                    old_to_new[i] = node.Node(i, None, None)
                old_to_new[n].getMap()[k] = [old_to_new[i]]
                self.clone_dfs(i, visited, old_to_new)

    def bool_to_string(self):
        out = ''
        visited = [False] * node.Node.id
        out += self.dfs_print_tree(self.initialNode, visited)
        return out

    def dfs_print_tree(self, n, visited):
        if visited[n.getCurrentId()]:
            return ''
        visited[n.getCurrentId()] = True
        out = str(n.getCurrentId()) + "\n"
        for k, v in n.getMap():
            for i in v:
                edge = k
                if edge == "\\L":
                    edge = "eps"
                out += str(n.getCurrentId()) + " " + str(i.getCurrentId()) + " " + edge + "\n"
                print(n.getCurrentId() + " " + n.getNodeTypes() + " " + n.isStart() + " " + i.getCurrentId() + " "
                      + i.isEnd() + i.getNodeTypes())
                out += self.dfs_print_tree(i, visited)
        return out
