from ._graph_functions import isTree
from ._generate_LaTeX_code import LaTeXCode
import sys
import os

def check_optional():
    
    save_temp_files = False
    output_format = 'png'
    show = True

    for argv in sys.argv:
        if argv.startswith('--'):
            if argv == '--save-temp-files=true':
                save_temp_files = True
                sys.argv.remove(argv)
            elif argv.startswith('--output-format='):
                output_format = argv[16:]
                sys.argv.remove(argv)
            elif argv.startswith('--show=false'):
                show = False
                sys.argv.remove(argv)
            else:
                print("Unrecognized interpreter option:", argv)
                exit()

    if output_format != 'png' and output_format != 'svg':
        print("Unrecognized format:", output_format)
        exit()
    
    return save_temp_files, output_format, show


def read_graph():

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

    return EdgeSet


def generate_code(EdgeSet):

    completeLaTeXCode = ""

    if isTree(EdgeSet) and input("This is a tree. Do you want to draw it as a tree structure? (y/n) ").strip() == 'y':
        try:
            root = input("Input the root node: ").strip()
        except:
            root = None
        completeLaTeXCode = LaTeXCode(EdgeSet, isTree=True, root=root)
    else:
        if input("Draw in a circle or a line? (circle/line): ").strip() == "line":
            completeLaTeXCode = LaTeXCode(EdgeSet, isLine=True)
        else:
            try:
                radius = int(input("Input the radius of the graph: "))
            except:
                radius = 3
            completeLaTeXCode = LaTeXCode(EdgeSet, radius)

    return "\\documentclass[tikz]{standalone}\n" \
        + "\\usepackage{tikz}\n" \
        + "\\begin{document}\n" \
        + completeLaTeXCode \
        + "\end{document}\n"


def generate_temp_path(completeLaTeXCode):
    
    tempPath = 'temp'

    if not os.path.exists(tempPath):
        os.mkdir(tempPath)
    with open("temp/graph.tex", "w") as f:
        f.writelines(completeLaTeXCode)

    os.system("xelatex --version > temp/info.log")
    with open("temp/info.log", "r", encoding='utf-8') as file:
        if "XeTeX" not in str(file.readline()):
            raise ModuleNotFoundError("xelatex not found on your machine!")
    os.system("xelatex -output-directory=temp temp/graph.tex > temp/info.log")

    return tempPath


def generate_figure(tempPath, output_format):

    if output_format == 'svg':
        os.system("pdftocairo -svg temp/graph.pdf graph.svg")

    if output_format == 'png':
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

        images_from_path = convert_from_path("temp/graph.pdf", output_folder=tempPath, dpi=360)
        for image in images_from_path:
            if images_from_path.index(image) == 1:
                image.save("graph.png", 'PNG')


def main(save_temp_files=False, output_format='png', show=True):

    if save_temp_files == False and output_format == 'png':
        save_temp_files, output_format, show = check_optional()
    
    EdgeSet = read_graph()

    completeLaTeXCode = generate_code(EdgeSet)

    tempPath = generate_temp_path(completeLaTeXCode)

    generate_figure(tempPath, output_format)

    if not save_temp_files:
        for file in os.listdir(tempPath):
            os.remove(os.path.join(tempPath, file))
        os.rmdir(tempPath)

    if show and output_format == 'png':
        from PIL import Image
        img = Image.open("graph.png")
        img.show()