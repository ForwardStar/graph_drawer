from __graph_functions__ import Tree

def line(VertexSet, EdgeSet):

    last = None
    last_dict = dict()

    for u in VertexSet:
        if last is None:
            last_dict[u] = None
            GraphMeta += "  \\node[node distance={20mm}, main] (" + str(u) + ") {$v_{" + str(u) + "}$};\n"
        else:
            last_dict[u] = last
            GraphMeta += "  \\node[node distance={20mm}, main] (" + str(u) + ") [right of=" + str(last) + "] {$v_{" + str(u) + "}$};\n"
        last = u

    for (u, v, t) in EdgeSet:
        if last_dict[u] == v or last_dict[v] == u:
            GraphMeta += "  \draw (" + str(u) + ") -- node[above] {" + str(t) + "} (" + str(v) + ");\n"
        else:
            GraphMeta += "  \draw (" + str(u) + ") to [bend left] node[above] {" + str(t) + "} (" + str(v) + ");\n"

    return GraphMeta


def tree(VertexSet, EdgeSet):

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
    GraphMeta += "  \\node[main] (" + str(root) + ") {$v_{" + str(root) + "}$};\n"
    while Queue:
        u = Queue.pop(0)
        GraphMeta += "  \\node[node distance={15mm}] (" + str(u * 100) + ") [below of=" + str(u) + "] {" + "};\n"
        left_last = str(u * 100)
        right_last = str(u * 100)
        count = 0
        for (v, t) in Graph.edge[u]:
            if count % 2 == 0:
                GraphMeta += "  \\node[node distance={" + str(Graph.num[v] * 10) + "mm}, main] (" + str(v) + ") [left of=" + str(left_last) + "] {$v_{" + str(v) + "}$};\n"
                left_last = v
            else:
                GraphMeta += "  \\node[node distance={" + str(Graph.num[v] * 10) + "mm}, main] (" + str(v) + ") [right of=" + str(right_last) + "] {$v_{" + str(v) + "}$};\n"
                right_last = v
            GraphMeta += "  \draw (" + str(u) + ") -- node[left] {" + str(t) + "} (" + str(v) + ");\n"
            Queue.append(v)
            count += 1
        
    return GraphMeta


def circle(VertexSet, EdgeSet, radius):

    count = 0
    VertexIdx = {}

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

    return GraphMeta


def LaTeXCode(EdgeSet, radius=3, isTree=False, isLine=False, root=None):

    VertexSet = []

    for (u, v, t) in EdgeSet:
        if u not in VertexSet:
            VertexSet.append(u)
        if v not in VertexSet:
            VertexSet.append(v)
    
    if isLine:
        GraphMeta = line(VertexSet, EdgeSet)

    elif isTree:
        GraphMeta = tree(VertexSet, EdgeSet)

    else:
        GraphMeta = circle(VertexSet, EdgeSet, radius)

    return "\\begin{figure}\n" \
        + "\centering\n" \
        + "\\begin{tikzpicture}[main/.style = {draw, circle, fill=white}]\n" \
        + GraphMeta \
        + "\end{tikzpicture}\n" \
        + "\end{figure}\n"