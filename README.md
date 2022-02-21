# Prerequisite

``xelatex`` and ``pdf2svg``. Installation on Linux:

```sh
# Ubuntu
sudo apt-get install texlive-xetex
sudo apt-get install poppler-utils
```

```sh
# CentOS
yum install texlive-xetex
yum install poppler-utils
```

For Windows, you only need to install texlive directly.

# Installation by pip

Install with pip:
```sh
pip install graph2img
```

Then write your edge information into ``graph.txt``. For example:
```
1 2 1
2 3 2
1 3 3
```

This will return a triangular graph.

Then run the program:
```sh
graph2img graph.txt
```

This will return a file ``graph.png``:

![](https://raw.githubusercontent.com/ForwardStar/graph_drawer/main/graph.png)

Or to draw a tree:
```
1 2 1
1 3 2
2 4 2
2 5 3
3 6 3
3 7 2
1 9 1
2 8 2
```

This will return a tree:

![](https://raw.githubusercontent.com/ForwardStar/graph_drawer/main/graph_tree.png)

# Options

Three options are provided:
```
--save-temp-files=true/false
--output-format=png/svg
--show=true/false
```

If you want to save the temporary files (like tex codes), set ``--save-temp-files`` as ``true``;

If you want to generate a svg format image, set ``-output-format`` as ``svg``;

If your system does not have a user interface, set ``--show`` as ``false``.

# Installation from source

```sh
git clone https://github.com/ForwardStar/graph_drawer.git
cd graph_drawer
python setup.py install
```