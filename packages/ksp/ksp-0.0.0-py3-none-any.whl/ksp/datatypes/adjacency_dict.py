from ..utils.config import INFINITY, UNDEFINDED

import random
class AdjacencyDict(dict):
    def __init__(self, *args, **kwargs):
        super(AdjacencyDict, self).__init__(*args, **kwargs)

    ## Gets the edges of a specified node.
    #
    # @param self The object pointer.
    # @param node The node whose edges are being queried.
    # @retval {} A dictionary of the edges and thier cost if the node exist
    # within the graph or None if the node is not in the graph.
    #
    def __getitem__(self, node):
        if node in self:
            return super(AdjacencyDict, self).__getitem__(node)
        else:
            return None


    def add_node(self, node):
        if node in self:
            return False
        self[node] = {}
        return True

    ## Adds a edge to the graph.
    #
    # @post The two nodes specified exist within the graph and their exist an
    # edge between them of the specified value.
    #
    # @param self The object pointer.
    # @param source The node that the edge starts at.
    # @param target The node that the edge terminates at.
    # @param cost The cost of the edge, if the cost is not specified a random
    # cost is generated from 1 to 10.
    #
    def add_edge(self, source, target, cost=None):
        if not cost:
            cost = INFINITY

        self.add_node(source)
        self.add_node(target)

        self[source][target] = cost
        return

    ## Removes an edge from the graph.
    #
    # @param self The object pointer.
    # @param source The node that the edge starts at.
    # @param target The node that the edge terminates at.
    # @param cost The cost of the edge, if the cost is not specified all edges
    # between the nodes are removed.
    # @retval int The cost of the edge that was removed. If the nodes of the
    # edge does not exist, or the cost of the edge was found to be infinity, or
    # if the specified edge does not exist, then -1 is returned.
    #
    def remove_edge(self, source, target, cost=None):
        if not source in self:
            return -1

        if target in self[source]:

            if not cost:
                cost = self[source][target]

                if cost == INFINITY:
                    return -1
                else:
                    self[source][target] = INFINITY
                    return cost
            elif self[source][target] == cost:
                self[source][target] = INFINITY

                return cost
            else:
                return -1
        else:
            return -1
