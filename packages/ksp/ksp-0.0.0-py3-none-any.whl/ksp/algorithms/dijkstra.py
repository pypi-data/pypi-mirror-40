## Computes the shortest path from a source to a sink in the supplied graph.
#
# @param graph A digraph of class Graph.
# @param node_start The source node of the graph.
# @param node_end The sink node of the graph.
#
# @retval {} Dictionary of path and cost or if the node_end is not specified,
# the distances and previous lists are returned.
#
from ..datatypes.priority_dict import PriorityDictionary
from ..utils.config import INFINITY, UNDEFINDED
from .utils import path
# from ..datatypes.graph import AdjacencyDict

def dijkstra(graph, node_start, node_end=None):
    distances = {}
    previous = {}
    queue = PriorityDictionary()

    for v in graph:
        distances[v] = INFINITY
        previous[v] = UNDEFINDED
        queue[v] = INFINITY

    distances[node_start] = 0
    queue[node_start] = 0

    for v in queue:
        if v == node_end: break

        for u in graph[v]:
            cost_vu = distances[v] + graph[v][u]

            if cost_vu < distances[u]:
                distances[u] = cost_vu
                queue[u] = cost_vu
                previous[u] = v

    if node_end:
        return {'cost': distances[node_end],
                'path': path(previous, node_start, node_end)}
    else:
        return (distances, previous)
