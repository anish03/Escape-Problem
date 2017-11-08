import pythonds as pds

class Graph:

    def __init__(self):
        self.vertices = {}
        self.numOfVertices = 0

    def addVertex(self,key):
        self.numOfVertices += 1
        vertex = Vertex(key)
        self.vertices[key] = vertex
        return vertex


class Vertex:

    def __init__(self,n):
        self.pathTo = {}
        self.color = 'white'

    def addNeighbor(self,nbr,weight=0):
        self.pathTo[nbr] = weight

    def setColor(self,color):
        self.color = color

    def getConnection(self):
        return self.pathTo.keys()


