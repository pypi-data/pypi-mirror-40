## @package YenKSP
# Computes K-Shortest Paths using Yen's Algorithm.
#
# Yen's algorithm computes single-source K-shortest loopless paths for a graph
# with non-negative edge cost. The algorithm was published by Jin Y. Yen in 1971
# and implores any shortest path algorithm to find the best path, then proceeds
# to find K-1 deviations of the best path.

## Computes K paths from a source to a sink in the supplied graph.
#
# @param graph A digraph of class Graph.
# @param start The source node of the graph.
# @param sink The sink node of the graph.
# @param K The amount of paths being computed.
#
# @retval [] Array of paths, where [0] is the shortest, [1] is the next
# shortest, and so on.
#

from operator import itemgetter
from .dijkstra import dijkstra
from .utils import path
def yen(graph, source, target, max_k=2):
    distances, previous = dijkstra(graph, source)

    A = [{'cost': distances[target],
          'path': path(previous, source, target)}]
    B = []

    if not A[0]['path']: return A

    for k in range(1, max_k):
        for i in range(0, len(A[-1]['path']) - 1):
            node_spur = A[-1]['path'][i]
            path_root = A[-1]['path'][:i+1]

            edges_removed = []
            for path_k in A:
                curr_path = path_k['path']
                if len(curr_path) > i and path_root == curr_path[:i+1]:
                    cost = graph.remove_edge(curr_path[i], curr_path[i+1])
                    if cost == -1:
                        continue
                    edges_removed.append([curr_path[i], curr_path[i+1], cost])

            path_spur = dijkstra(graph, node_spur, target)

            if path_spur['path']:
                path_total = path_root[:-1] + path_spur['path']
                dist_total = distances[node_spur] + path_spur['cost']
                potential_k = {'cost': dist_total, 'path': path_total}

                if not (potential_k in B):
                    B.append(potential_k)

            for edge in edges_removed:
                graph.add_edge(edge[0], edge[1], edge[2])

        if len(B):
            B = sorted(B, key=itemgetter('cost'))
            A.append(B[0])
            B.pop(0)
        else:
            break

    return A
