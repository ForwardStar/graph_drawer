def LaTeXCode(EdgeSet, radius=3, isTree=False, root=None):

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
            

    GraphMeta = ""
    VertexSet = []
    VertexIdx = {}

    for (u, v, t) in EdgeSet:
        if u not in VertexSet:
            VertexSet.append(u)
        if v not in VertexSet:
            VertexSet.append(v)

    if isTree:
        Temp = dict()
        for (u, v, t) in EdgeSet:
            if u not in Temp:
                Temp[u] = [(v, t)]
            else:
                Temp[u].append((v, t))
            if v not in Temp:
                Temp[v] = [(u, t)]
            else:
                Temp[v].append((u, t))
        EdgeSet = Temp
        if root not in Temp:
            root = VertexSet[0]
        Graph = Tree(root, VertexSet, EdgeSet)
        Queue = [root]
        GraphMeta += "\\node[main] (" + str(root) + ") {$v_{" + str(root) + "}$};\n"
        while Queue:
            u = Queue.pop(0)
            GraphMeta += "\\node[node distance={15mm}] (" + str(u * 100) + ") [below of=" + str(u) + "] {" + "};\n"
            left_last = str(u * 100)
            right_last = str(u * 100)
            count = 0
            for (v, t) in Graph.edge[u]:
                if count % 2 == 0:
                    GraphMeta += "\\node[node distance={" + str(Graph.num[v] * 10) + "mm}, main] (" + str(v) + ") [left of=" + str(left_last) + "] {$v_{" + str(v) + "}$};\n"
                    left_last = v
                else:
                    GraphMeta += "\\node[node distance={" + str(Graph.num[v] * 10) + "mm}, main] (" + str(v) + ") [right of=" + str(right_last) + "] {$v_{" + str(v) + "}$};\n"
                    right_last = v
                GraphMeta += "  \draw (" + str(u) + ") -- node[left] {" + str(t) + "} (" + str(v) + ");\n"
                Queue.append(v)
                count += 1

    else:
        count = 0
        for u in VertexSet:
            GraphMeta += "  \coordinate[] (" + str(u) + ") at (" + str(count / len(VertexSet) * 360) + ":" + str(radius) + ");\n"
            GraphMeta += "  \\node at (" + str(u) + ")[main]{$v_{" + str(u) + "}$};\n"
            VertexIdx[u] = count
            count += 1

        for (u, v, t) in EdgeSet:
            if VertexIdx[u] + VertexIdx[v] == len(VertexSet):
                GraphMeta += "  \draw (" + str(u) + ") -- node[left] {" + str(t) + "} (" + str(v) + ");\n"
            else:
                GraphMeta += "  \draw (" + str(u) + ") -- node[above] {" + str(t) + "} (" + str(v) + ");\n"
        
        for u in VertexSet:
            GraphMeta += "  \\node at (" + str(u) + ")[main]{$v_{" + str(u) + "}$};\n"

    return "\\begin{figure}\n" \
        + "\centering\n" \
        + "\\begin{tikzpicture}[main/.style = {draw, circle, fill=white}]\n" \
        + GraphMeta \
        + "\end{tikzpicture}\n" \
        + "\end{figure}\n"

def isConnected(VertexSet, EdgeSet):

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

def main():
    import sys

    save_temp_files = False
    for argv in sys.argv:
        if argv.startswith('--') and argv != '--save-temp-files':
            print("Unrecognized interpreter option:", argv)
            exit()
        if argv == '--save-temp-files':
            save_temp_files = True
            sys.argv.remove(argv)

    EdgeSet = []
    try:
        GraphFile = "graph.txt"
        if len(sys.argv) >= 2:
            GraphFile = sys.argv[1]
        with open(GraphFile, "r") as f:
            while True:
                text = f.readline().split()
                if len(text) == 0:
                    break
                if len(text) != 2 and len(text) != 3:
                    print("Invalid format of input file.")
                u = text[0]
                v = text[1]
                if len(text) == 3:
                    t = text[2]
                else:
                    t = ""
                EdgeSet.append((u, v, t))
    except:
        print("Please create a 'graph.txt' file. Write graph data in the format (u, v, w) in it.")
        print("Sample:")
        print("1 2 1")
        print("2 3 2")
        print("1 3 3")
        print("This will return a triangular graph.")
        exit()

    completeLaTeXCode = ""

    if isTree(EdgeSet) and input("This is a tree. Do you want to draw it as a tree structure? (y/n) ").strip() == 'y':
        try:
            root = input("Input the root node: ").strip()
        except:
            root = None
        completeLaTeXCode = LaTeXCode(EdgeSet, isTree=True, root=root)
    else:
        try:
            radius = int(input("Input the radius of the graph: "))
        except:
            radius = 3
        completeLaTeXCode = LaTeXCode(EdgeSet, radius)

    completeLaTeXCode = "\\documentclass[tikz]{standalone}\n" \
        + "\\usepackage{tikz}\n" \
        + "\\begin{document}\n" \
        + completeLaTeXCode \
        + "\end{document}\n"

    import os
    tempPath = "temp"
    if not os.path.exists(tempPath):
        os.mkdir(tempPath)
    with open("temp/graph.tex", "w") as f:
        f.writelines(completeLaTeXCode)

    os.system("xelatex --version > temp/info.log")
    with open("temp/info.log", "r") as file:
        if not file.readline().startswith("XeTeX"):
            raise ModuleNotFoundError("xelatex not found on your machine!")
    os.system("xelatex -output-directory=temp temp/graph.tex > temp/info.log")

    try:
        from pdf2image import convert_from_path
    except:
        print("Installing dependencies...")
        try:
            from pip._internal import main
            main(['install', 'pdf2image'])
        except:
            os.system("pip3 install pdf2image")
        from pdf2image import convert_from_path

    def generate():
        images_from_path = convert_from_path("temp/graph.pdf", output_folder=tempPath, dpi=360)
        for image in images_from_path:
            if images_from_path.index(image) == 1:
                image.save("graph.png", 'PNG')

    generate()

    if not save_temp_files:
        for file in os.listdir(tempPath):
            os.remove(os.path.join(tempPath, file))
        os.rmdir(tempPath)

    from PIL import Image
    img = Image.open("graph.png")
    img.show()