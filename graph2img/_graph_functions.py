class Tree:

    def __init__(self, root, Vertex, Edge):
        Queue = [root]
        Visited = set()
        self.vertex = Vertex
        self.edge = dict()
        while Queue:
            u = Queue.pop(0)
            Visited.add(u)
            self.edge[u] = []
            for (v, t) in Edge[u]:
                if v not in Visited:
                    self.edge[u].append((v, t))
                    Queue.append(v)
        self.num = dict()
        self.countNodes(root)
        for key in self.edge.keys():
            def firstElem(elem):
                return self.num[elem[0]]
            self.edge[key].sort(key=firstElem)
    
    def countNodes(self, root):
        self.num[root] = 1
        for (v, t) in self.edge[root]:
            self.num[root] += self.countNodes(v)
        return self.num[root]


class DisjointSet:

    def __init__(self, Vertex, Edge=None):
        self.parent = dict()
        for u in Vertex:
            self.parent[u] = u
        if Edge:
            for (u, v, t) in Edge:
                if self.find(u) != self.find(v):
                    self.union(u, v)
    
    def find(self, u):
        if self.parent[u] != u:
            self.parent[u] = self.find(self.parent[u])
        return self.parent[u]
    
    def union(self, u, v):
        self.parent[self.parent[v]] = self.parent[u]
    
    def isConnected(self):
        root = None
        for key in self.parent.keys():
            if root is None:
                root = self.find(key)
            elif root != self.find(key):
                return False
        return True


def isConnected(VertexSet, EdgeSet):
    
    return DisjointSet(VertexSet, EdgeSet).isConnected()


def isTree(EdgeSet):

    VertexSet = []

    for (u, v, t) in EdgeSet:
        if u not in VertexSet:
            VertexSet.append(u)
        if v not in VertexSet:
            VertexSet.append(v)
    
    if len(EdgeSet) + 1 == len(VertexSet):
        return isConnected(VertexSet, EdgeSet)
    
    return False