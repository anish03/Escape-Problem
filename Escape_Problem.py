# Escape problem

import os
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import breadth_first_order


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


def edmonds_karp(G, s, t):
    """
    :param G: Network Graph
    :param s: Source
    :param t: Sink
    :return: Maximum flow through the network
    """
    flow = 0
    source, sink = s, t

    nodes, predecessor = breadth_first_order(csr_matrix(G), 0, directed=True, return_predecessors=True)
    shortest_path = path(predecessor, source, sink)
    # print shortest_path

    while source in shortest_path:
        bottleneck_edge = find_bottleneck(G, shortest_path)
        flow += bottleneck_edge
        G = augment(G, shortest_path, bottleneck_edge)
        nodes, predecessor = breadth_first_order(csr_matrix(G), 0, directed=True, return_predecessors=True)
        shortest_path = path(predecessor, source, sink)

    return flow


def escape(d, st):
    # Total number of nodes = d * d * 2 + 2
    g = d * d * 2 + 2
    x1 = np.zeros((g, g), dtype=np.int)

    # Vin-Vout edges changed to 1
    for j in range(1, d * d * 2, 2):
        x1[j][j + 1] = 1

    # Sides to Sink
    # Upper + Lower
    for j in range(1, d + 1):
        x1[2 * j][g - 1] = 1
        x1[2 * (d - 1) * d + 2 * j][g - 1] = 1

    # Sides to Sink
    # left + right
    for j in range(d):
        x1[j * 2 * d + 2][g - 1] = 1
        x1[2 * d * (j + 1)][g - 1] = 1

    # Source to given vertices,
    # S to Vin
    for l in st:
        x1[0][(l[0] - 1) * 2 * d + (2 * (l[1] - 1)) + 1] = 1

    # From each vertex to its neighbours
    # Right
    for l in range(2, d * d * 2 + 1, 2):
        if l % (2 * d) != 0:
            x1[l][l + 1] = 1
            # x[l + 2][l - 1] = 1

    # Left
    for l in range(2, d * d * 2 + 1, 2):
        if (l - 2) % (2 * d) != 0:
            x1[l][l - 3] = 1

    # Up
    for l in range(2, d * d * 2 + 1, 2):
        if l - (2 * d) > 0:
            x1[l][l - (2 * d) - 1] = 1

    # Down
    for l in range(2, d * d * 2 + 1, 2):
        if l + (2 * d) < d * d * 2 + 1:
            x1[l][l + (2 * d) - 1] = 1

    max_flow = edmonds_karp(x1, 0, g - 1)

    return max_flow

if __name__ == '__main__':
    l = []
    file_path = os.path.join(os.curdir, r"Datasets\ds9.txt")
    with open(file_path) as f:
        for line in f:
            l.append((map(int, line.strip().split())))

    g1, g2, tc = l[0]
    grid_dimension = g1
    if g1 != g2:
        print "Invalid Grid dimensions: Not a square grid"
    else:
        start_vertices = []
        for k in xrange(tc):
            x, y = l[k + 1]
            start_vertices.append((x, y))
        # print start_vertices

        final_flow = escape(grid_dimension, start_vertices)
        print "Maximum Flow: ", final_flow
        print "Starting Escape vertices: ", tc
        print "possible" if final_flow == len(start_vertices) else "not possible"
