from ._graph_functions import isTree
from ._generate_LaTeX_code import LaTeXCode
import sys
import os

headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}

def download(url, path):

    from tqdm import tqdm
    from urllib.request import urlopen, Request
    blocksize = 1024 * 8
    blocknum = 0
    retry_times = 0
    while True:
        try:
            with urlopen(Request(url, headers=headers), timeout=3) as resp:
                total = resp.info().get("content-length", None)
                with tqdm(
                    unit="B",
                    unit_scale=True,
                    miniters=1,
                    unit_divisor=1024,
                    total=total if total is None else int(total),
                ) as t, path.open("wb") as f:
                    block = resp.read(blocksize)
                    while block:
                        f.write(block)
                        blocknum += 1
                        t.update(len(block))
                        block = resp.read(blocksize)
            break
        except KeyboardInterrupt:
            if path.is_file():
                path.unlink()
            raise
        except:
            retry_times += 1
            if retry_times >= 20:
                break
            print("Timed out, retrying...")
    if retry_times >= 20:
        if path.is_file():
            path.unlink()
        raise ConnectionError("bad internet connection, check it and retry.")


def install_pdf2svg():

    print("Installing necessary components...")

    try:
        import requests
    except:
        print("Installing dependencies...")
        try:
            from pip._internal import main
            main(['install', 'requests'])
        except:
            os.system("pip3 install requests")
        import requests

    from pathlib2 import Path
    import re, platform, zipfile
    system_info = platform.architecture()

    if system_info[1] == 'WindowsPE':
        path = os.path.join(__file__[:-11], 'pdf2svg')
        base_url = "https://github.com/jalios/pdf2svg-windows/tree/master/"
        reg = None
        if system_info[0] == '32bit':
            base_url += "dist-32bits"
            reg = r'/jalios/pdf2svg-windows/blob/master/dist-32bits/[\w\-\_\+]+\.dll|/jalios/pdf2svg-windows/blob/master/dist-32bits/[\w\-\_\+]+\.exe'
        elif system_info[0] == '64bit':
            base_url += "dist-64bits"
            reg = r'/jalios/pdf2svg-windows/blob/master/dist-64bits/[\w\-\_\+]+\.dll|/jalios/pdf2svg-windows/blob/master/dist-64bits/[\w\-\_\+]+\.exe'
        else:
            os.rmdir(path)
            raise SystemError("error detecting system information:", system_info)
        
        web_contents = requests.session().get(base_url, headers=headers).content.decode('utf-8')
        files = re.compile(reg).findall(web_contents)
        for file in files:
            file = file.replace('blob', 'raw')
            url = "https://github.com" + file
            file = file.split('/')
            try:
                print("Downloading", file[-1])
                download(url, Path(os.path.join(path, file[-1])))
            except:
                os.rmdir(path)
        print("set PATH=%PATH%" + path)
        os.system("set PATH=%PATH%" + path)
    
    elif system_info[1] == 'ELF':
        url = "https://github.com/dawbarton/pdf2svg/archive/refs/heads/master.zip"
        print("Downloading pdf2svg.zip...")
        path = os.path.join(__file__[:-11], 'pdf2svg.zip')
        download(url, Path(path))

        zip_file = zipfile.ZipFile(path, 'r')
        path = os.path.join(__file__[:-11], 'pdf2svg')
        zip_file.extractall(path)
        path = __file__[:-11] + 'pdf2svg/'

        with open(os.path.join(__file__[:-11], 'pdf2svg') + "/install.sh", "w", encoding='utf-8') as f:
            f.writelines("chmod 755 -R " + path + " && " +
                        "cd " + path + "pdf2svg-master/ && " +
                        "./configure --prefix=" + path + " && " +
                        "make && " +
                        "make install")
        os.system("bash " + path + "install.sh")

    else:
        os.rmdir(path)
        raise SystemError("error detecting system information:", system_info)

def check_optional():
    
    save_temp_files = False
    temp_path = 'temp'
    output_format = 'png'
    shape = "circle"
    show = True
    argv_remove_list = []

    for argv in sys.argv:
        if argv.startswith('--'):
            if argv == '--save-temp-files=true':
                save_temp_files = True
                argv_remove_list.append(argv)
            elif argv.startswith('--temp-path='):
                temp_path = argv[12:]
                argv_remove_list.append(argv)
            elif argv.startswith('--output-format='):
                output_format = argv[16:]
                argv_remove_list.append(argv)
            elif argv.startswith('--shape='):
                shape = argv[8:]
                argv_remove_list.append(argv)
            elif argv == 'show==false':
                show = False
                argv_remove_list.append(argv)
            else:
                print("Unrecognized interpreter option:", argv)
                exit()

    for argv in argv_remove_list:
        sys.argv.remove(argv)

    if output_format != 'png' and output_format != 'svg':
        print("Unrecognized format:", output_format)
        exit()
    
    return save_temp_files, temp_path, output_format, shape, show


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


def generate_code(EdgeSet, shape="circle"):

    completeLaTeXCode = ""

    if isTree(EdgeSet) and shape == "tree":
        try:
            root = input("Input the root node: ").strip()
        except:
            root = None
        completeLaTeXCode = LaTeXCode(EdgeSet, isTree=True, root=root)
    else:
        if shape == "line":
            completeLaTeXCode = LaTeXCode(EdgeSet, isLine=True)
        else:
            radius = 3
            completeLaTeXCode = LaTeXCode(EdgeSet, radius)

    return "\\documentclass[tikz]{standalone}\n" \
        + "\\usepackage{tikz}\n" \
        + "\\begin{document}\n" \
        + completeLaTeXCode \
        + "\end{document}\n"


def generate_temp_path(temp_path, completeLaTeXCode):
    
    tempPath = temp_path
    texPath = os.path.join(tempPath, "graph.tex").replace('\\', '/')
    infoPath = os.path.join(tempPath, "info.log").replace('\\', '/')

    if not os.path.exists(tempPath):
        os.mkdir(tempPath)
    with open(texPath, "w") as f:
        f.writelines(completeLaTeXCode)

    os.system("xelatex --version > " + infoPath)
    with open(infoPath, "r", encoding='utf-8') as file:
        if "XeTeX" not in str(file.readline()):
            raise ModuleNotFoundError("xelatex not found on your machine!")
    os.system("xelatex -output-directory=" + tempPath + " " + texPath + " > " + infoPath)

    return tempPath


def generate_figure(tempPath, output_format):

    pdfPath = os.path.join(tempPath, "graph.pdf").replace('\\', '/')
    infoPath = os.path.join(tempPath, "info.log").replace('\\', '/')

    if output_format == 'svg':
        # path = os.path.join(__file__[:-11], 'pdf2svg')
        # if not os.path.exists(path):
        #    os.mkdir(path)
        #    install_pdf2svg()
        os.system("pdf2svg > " + infoPath)
        with open(infoPath, "r", encoding='utf-8') as file:
            if not file.readline().startswith('Usage'):
                raise ModuleNotFoundError("pdf2svg not found on your machine, install from https://github.com/dawbarton/pdf2svg before use.")
        if len(sys.argv) >= 3:
            os.system("pdf2svg " + pdfPath + " " + sys.argv[2] + " all")
        else:
            os.system("pdf2svg " + pdfPath + " graph.svg all")

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

        images_from_path = convert_from_path(pdfPath, output_folder=tempPath, dpi=360)
        for image in images_from_path:
            if images_from_path.index(image) == 1:
                if len(sys.argv) >= 3:
                    image.save(sys.argv[2], 'PNG')
                else:
                    image.save("graph.png", 'PNG')


def main(save_temp_files=False, temp_path='temp', output_format='png', shape="circle", show=True):

    if save_temp_files == False and temp_path == 'temp' and output_format == 'png' and shape == "circle" and show:
        save_temp_files, temp_path, output_format, shape, show = check_optional()
    
    EdgeSet = read_graph()

    completeLaTeXCode = generate_code(EdgeSet, shape)

    tempPath = generate_temp_path(temp_path, completeLaTeXCode)

    generate_figure(tempPath, output_format)

    if not save_temp_files:
        for file in os.listdir(tempPath):
            os.remove(os.path.join(tempPath, file))
        os.rmdir(tempPath)

    if output_format == 'png':
        from PIL import Image
        if len(sys.argv) >= 3:
            img = Image.open(sys.argv[2])
        else:
            img = Image.open("graph.png")
        img.show()