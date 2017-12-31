# Escape Problem

![Escape Problem](https://github.com/anish03/CS255-Project/blob/master/Escape%20Problem/Escape%20Problem1.png)

* Implemented maximum flow through a network using Edmond Karp algorithm (using shortest path)

* Implemented maximum flow through a network using Capacity Scaling

* Implemented maximum flow through a network using Ford-Fulkerson (Depth first search)

* Solved the Escape Problem, by converting it into a max-flow network problem with unit capacity. Added an artificial source vertex and sink vertex.
Connected artificial source vertex to all 'starting vertices' in the grid & connected all the boundary vertices to the artificial sink vertex.
We then calculate the max-flow in order to determine whether it is possible for 'n' starting points to successfully escape the grid.

## Prerequisites

```
pip install numpy
pip install scipy

```

## Authors

* Neeraj Kulkarni - [xOmega](https://github.com/xOmega)

* Anish Narkhede - [anish03](https://github.com/anish03)
