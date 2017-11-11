class Graph():
    pass


def breadth_first_search(g1, s, t):
    q = [s]

    while q:
        p = q.pop(0)
        for i in g[p]:
            q.append(i)


g = {}
l = raw_input("Enter vertices V (space separated)").strip().split()
for i in l:
    g[i] = {}
for _ in xrange(input("Enter no. of edges E (start, end and weight):")):
    start, end, weight = raw_input().strip().split()
    if start not in g:
        print "Unknown Vertex" + start + ": Edge" + start + end + "Not added"
    g[start][end] = weight
# print g
# breadth_first_search(g, 'a', 'b')



"""
Input
a b c d e

8

a b 1
a c 4
b c 3
b d 2
d b 1
d c 5
b e 2
e d -2
"""

