import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import breadth_first_order

x = np.array([[0, 3, 3, 4, 0, 0, 0],
               [0, 0, 0, 0, 2, 0, 0],
               [0, 10, 0, 0, 1, 0, 0],
               [0, 0, 0, 0, 0, 5, 0],
               [0, 0, 0, 1, 0, 1, 2],
               [0, 0, 0, 0, 0, 0, 5],
               [0, 0, 0, 0, 0, 0, 0]
               ])


def path(arr, s, t):
    """
    :param arr: Array of predecessors
    :param s: Source
    :param t: Sink
    :return: Shortest length path from source to sink
    """
    source_vertex = s
    temp = [t]
    i = t
    while arr[i] != -9999:
        temp.append(arr[i])
        i = arr[i]
    return temp[::-1]


def find_bottleneck(G, arr):
    """
    :param G: Input Graph
    :param arr: Shortest path array
    :return: capacity of bottleneck edge
    """
    min_val = np.inf
    for i in range(1, len(arr)):
        start, end = arr[i - 1], arr[i]
        if G[start][end] < min_val:
            min_val = G[start][end]
    return min_val


def augment(G1, short_path, bottleneck_edge):
    """

    :param G1: Residual Graph Gf
    :param short_path:
    :param bottleneck_edge:
    :return: Augmented Residual graph Gf'
    """
    for i in range(1, len(short_path)):
        start, end = short_path[i - 1], short_path[i]
        G1[start][end] -= bottleneck_edge
        G1[end][start] += bottleneck_edge
    return G1


def scale_graph(G1, delta):
    G1 = np.copy(G1)
    for i in range(len(G1)):
        for j in range(len(G1)):
            if G1[i][j] < delta:
                G1[i][j] = 0
    return G1


def capacity_scale(G, s, t):
    """
    :param G: Network Graph
    :param s: Source
    :param t: Sink
    :return: Maximum flow through the network
    """
    flow = 0
    source, sink = s, t
    delta = 2 ** len(bin(np.amax(G))[2:])
    while delta >= 1:
        G_delta = scale_graph(G, delta)
        nodes, predecessor = breadth_first_order(csr_matrix(G_delta), 0, directed=True, return_predecessors=True)
        shortest_path = path(predecessor, source, sink)
        while len(shortest_path) > 1:
            bottleneck_edge = find_bottleneck(G_delta, shortest_path)
            flow += bottleneck_edge
            G = augment(G, shortest_path, bottleneck_edge)
            G_delta = scale_graph(G, delta)
            nodes, predecessor = breadth_first_order(csr_matrix(G_delta), 0, directed=True, return_predecessors=True)
            shortest_path = path(predecessor, source, sink)
        delta /= 2
    return flow

max_flow = capacity_scale(x, 0, 6)
print max_flow

"""
Inputs
x = np.array ([[0, 3, 3, 4, 0, 0, 0],
               [0, 0, 0, 0, 2, 0, 0],
               [0, 10, 0, 0, 1, 0, 0],
               [0, 0, 0, 0, 0, 5, 0],
               [0, 0, 0, 1, 0, 1, 2],
               [0, 0, 0, 0, 0, 0, 5],
               [0, 0, 0, 0, 0, 0, 0]
               ])

x = np.array([[0, 8, 0, 3],
               [0, 0, 2, 5],
               [0, 0, 0, 0],
               [0, 0, 6, 0]])

"""