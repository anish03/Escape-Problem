import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import breadth_first_order


X = csr_matrix([[0, 8, 0, 3],
                [0, 0, 2, 5],
                [0, 0, 0, 0],
                [0, 0, 6, 0]])


def path(arr, s, t):
    """
    :param arr: Array of predecessors
    :param s: Source
    :param t: Sink
    :return: Shortest length path from source to sink
    """
    temp = [t]
    i = t
    while arr[i] != -9999:
        temp.append (arr[i])
        i = arr[i]
    return temp[::-1]


def find_bottleneck(G, arr):
    """
    :param arr: Shortest path array
    :return: capacity of bottleneck edge
    """
    min_val = np.inf
    for i in range(1, len(arr)):
        start, end = arr[i - 1], arr[i]
        if G[start][end] < min_val:
            min_val = G[start][end]
    return min_val


def augment(G, short_path, bottleneck_edge):
    """

    :param G: Residual Graph Gf
    :param short_path:
    :param bottleneck_edge:
    :return: Augmented Residual graph Gf'
    """
    for i in range(1, len(short_path)):
        if G[i - 1][i] > 0:
            pass
    return G


def edmonds_karp(G, s, t):
    """
    :param G: Network Graph
    :param s: Source
    :param t: Sink
    :return: Maximum flow through the network
    """
    flow = 0
    source, sink = s, t

    nodes, predecessor = breadth_first_order(G, 0, directed=True, return_predecessors=True)
    shortest_path = path(predecessor, source, sink)
    print shortest_path

    while len(shortest_path) > 1:
        flow += find_bottleneck(G, shortest_path)


edmonds_karp(X, 0, 2)