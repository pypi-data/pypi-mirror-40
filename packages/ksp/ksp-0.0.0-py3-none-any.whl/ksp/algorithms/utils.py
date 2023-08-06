from ..utils.config import UNDEFINDED
## Finds a paths from a source to a sink using a supplied previous node list.
#
# @param previous A list of node predecessors.
# @param node_start The source node of the graph.
# @param node_end The sink node of the graph.
#
# @retval [] Array of nodes if a path is found, an empty list if no path is
# found from the source to sink.
#
def path(previous, node_start, node_end):
    route = []

    node_curr = node_end
    while True:
        route.append(node_curr)
        if previous[node_curr] == node_start:
            route.append(node_start)
            break
        elif previous[node_curr] == UNDEFINDED:
            return []

        node_curr = previous[node_curr]

    route.reverse()
    return route
