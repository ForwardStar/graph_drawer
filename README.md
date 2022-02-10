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

![](graph.png)

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

![](graph_tree.png)

# Installation from source

```sh
git clone https://github.com/ForwardStar/graph_drawer.git
cd graph_drawer
python setup.py install
```