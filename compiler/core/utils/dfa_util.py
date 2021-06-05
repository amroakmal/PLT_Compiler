from core.constants import Constants


class DfaUtility:
    @staticmethod
    def getUnionInputs(nfaNodes):
        possibleInputs = []

        for node in nfaNodes:
            for string in node.get_map().keys():
                if string not in possibleInputs and (string != Constants.EPSILON):
                    possibleInputs.append(string)

        return possibleInputs

    @staticmethod
    def getNodeType(nfaNodes):
        nodeTypes = ""
        length = len(nfaNodes)
        i = 0
        while i < length:
            if nfaNodes[i].get_node_types() != '':
                nodeTypes += nfaNodes[i].get_node_types()
                nodeTypes += Constants.SEPARATOR

            i += 1

        return nodeTypes[0: len(nodeTypes) - 1 if len(nodeTypes) > 0 else 0]

    @staticmethod
    def createUnionID(nfaNodes):
        length = len(nfaNodes)
        intArr = [0] * length
        i = 0

        while i < length:
            intArr[i] = nfaNodes[i].get_current_id()
            i += 1

        intArr.sort()

        string = ""
        i = 0
        while i < length - 1:
            if str(intArr[i]) not in string:
                string += str(intArr[i]) + Constants.SEPARATOR

            i += 1

        if str(intArr[length - 1]) not in string:
            string += str(intArr[length - 1])

        return string

    @staticmethod
    def findPartitionOfNode(node, groupings):
        for groupID in groupings.keys():
            for nodeIterator in groupings[groupID]:
                if nodeIterator == node:
                    return groupID

        return -1

    @staticmethod
    def canFit(node, newGroupingNode, nodeParent):
        expr1 = nodeParent[newGroupingNode.get_current_id()] != nodeParent[node.get_current_id()]
        expr2 = len(newGroupingNode.get_map().keys()) != len(node.get_map().keys())

        if expr1 or expr2:
            return False

        for item in node.get_map().keys():
            # TODO: HERE
            if item not in newGroupingNode.get_map().keys():
                return False
            nodeRes = node.get_map()[item][0]
            parentRes = newGroupingNode.get_map()[item][0]

            if nodeParent[nodeRes.get_current_id()] != nodeParent[parentRes.get_current_id()]:
                return False

        return True
