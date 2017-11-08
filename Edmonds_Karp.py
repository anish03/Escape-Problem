g = {}
for _ in xrange(input("Enter no. of edges")):
    start, end, weight = raw_input("Enter input edge in the form (start, end and weight):").strip().split()
    if start not in g:
        g[start] = {}
    g[start][end] = weight
print g
