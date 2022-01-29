def LaTeXCode(EdgeSet):
    GraphMeta = ""
    VertexSet = []
    VertexIdx = {}

    for (u, v, t) in EdgeSet:
        if u not in VertexSet:
            VertexSet.append(u)
        if v not in VertexSet:
            VertexSet.append(v)

    count = 0
    for u in VertexSet:
        GraphMeta += "  \coordinate[] (" + str(u) + ") at (" + str(count / len(VertexSet) * 360) + ":3);\n"
        GraphMeta += "  \\node at (" + str(u) + ")[main]{$v_" + str(u) + "$};\n"
        VertexIdx[u] = count
        count += 1

    for (u, v, t) in EdgeSet:
        if len(VertexSet) - max(VertexIdx[u], VertexIdx[v]) == min(VertexIdx[u], VertexIdx[v]):
            GraphMeta += "  \draw (" + str(u) + ") -- node[left, midway] {" + str(t) + "} (" + str(v) + ");\n"
        else:
            GraphMeta += "  \draw (" + str(u) + ") -- node[above, midway] {" + str(t) + "} (" + str(v) + ");\n"
    
    for u in VertexSet:
        GraphMeta += "  \\node at (" + str(u) + ")[main]{$v_" + str(u) + "$};\n"

    return "\\begin{figure}\n" \
        + "\centering\n" \
        + "\\begin{tikzpicture}[main/.style = {draw, circle, fill=white}]\n" \
        + GraphMeta \
        + "\end{tikzpicture}\n" \
        + "\end{figure}\n"

import sys
EdgeSet = []
try:
    GraphFile = "graph.txt"
    if len(sys.argv) == 2:
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

# print(LaTeXCode(EdgeSet))
completeLaTeXCode = "\\documentclass[tikz]{standalone}\n" \
    + "\\usepackage{tikz}\n" \
    + "\\begin{document}\n" \
    + LaTeXCode(EdgeSet) \
    + "\end{document}\n"

import os
tempPath = "temp"
if not os.path.exists(tempPath):
    os.mkdir(tempPath)
with open("temp/graph.tex", "w") as f:
    f.writelines(completeLaTeXCode)

os.system("xelatex -output-directory=temp temp/graph.tex > temp/info.log")

try:
    from pdf2image import convert_from_path
except:
    print("Installing dependencies...")
    from pip._internal import main
    main(['install', 'pdf2image'])
    from pdf2image import convert_from_path

def generate():
    images_from_path = convert_from_path("temp/graph.pdf", output_folder=tempPath, dpi=360)
    for image in images_from_path:
        if images_from_path.index(image) == 1:
            image.save("graph.png", 'PNG')

generate()

for file in os.listdir(tempPath):
    os.remove(os.path.join(tempPath, file))
os.rmdir(tempPath)

from PIL import Image
img = Image.open("graph.png")
img.show()