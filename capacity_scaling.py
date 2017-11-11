import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import breadth_first_order


def initial_delta(G):
    """

    :param G: Input graph
    :return: delta (for capacity-scaling)
    """
    i = 1
    delta = 2 ** i
    while delta < G.max():
        i += 1
        delta = 2 ** i

    if delta > G.max():
        delta = 2 ** (i-1)
        return delta
    else:
        return delta



def scaled_graph(G,delta):
    """

    :param G: Input graph
    :param delta: delta (for capacity-scaling)
    :return: Graph after scaling
    """
    temp = G.copy()

    for i in range(G.shape[0]):
        for j in range(G.shape[1]):
            if G[i][j] < delta:
                temp[i][j] = 0

    return temp


def check_if_path_exists(G,src,sink,delta):
    """

    :param G: Input graph
    :param src: Graph source vertex
    :param sink: Graph sink vertex
    :param delta: delta (for capacity-scaling)
    :return: Boolean value : if a path between source and sink exists
    """

    nodes, predecessor = breadth_first_order(csr_matrix(G), 0, directed=True, return_predecessors=True)
    if src in nodes and sink in nodes:
        return True
    else:
        return False


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

def capacity_scaling(source,sink):

    """
    :param source: Source vertex of the network
    :param sink: Sink vertex of the network
    :return: Max flow in the network
    """

    delta = 2
    flow = 0

    x = np.array([ [0,3,3,4,0,0,0],
               [0,0,0,0,2,0,0],
               [0,10,0,0,1,0,0],
               [0,0,0,0,0,5,0],
               [0,0,0,1,0,1,2],
               [0,0,0,0,0,0,5],
               [0,0,0,0,0,0,0]
              ])


    delta = initial_delta(x)
    SG = scaled_graph(x,delta)
    paths = []

    while delta > 1:
        SG = scaled_graph(x,delta)
        if check_if_path_exists(SG,source,sink,delta):
            nodes, predecessor = breadth_first_order(csr_matrix(SG),0,directed=True,return_predecessors=True)
            shortest_path = path(predecessor,source,sink)
            bottleneck_edge = find_bottleneck(x,shortest_path)
            flow += bottleneck_edge
            x = augment(x,shortest_path,bottleneck_edge)
            delta = delta / 2

        else:
            delta = delta / 2
            SG = scaled_graph(x,delta)
            nodes, predecessor = breadth_first_order(csr_matrix(SG),0,directed=True,return_predecessors=True)
            shortest_path = path(predecessor,source,sink)
            bottleneck_edge = find_bottleneck(x,shortest_path)
            flow += bottleneck_edge
            x = augment(x,shortest_path,bottleneck_edge)

    return flow

max_flow = capacity_scaling(0,6)
print max_flow
