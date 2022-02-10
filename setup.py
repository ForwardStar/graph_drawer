import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
  long_description = fh.read()

setuptools.setup(
  name="graph2img",
  version="1.0.1",
  author="Haoxuan Xie",
  author_email="haoxuanxie@link.cuhk.edu.cn",
  url="https://github.com/ForwardStar/graph_drawer",
  py_modules=["graph2img"],
  description="graph2img: convert a graph to a png file.",
  long_description=long_description,
  long_description_content_type="text/markdown",
  license="LICENSE",
  classifiers=[
  "Programming Language :: Python :: 3.8",
  "License :: OSI Approved :: MIT License",
  "Operating System :: OS Independent",
  ],
  install_requires=['pdf2image>=1.6.0'],
  python_requires='>=3.6',
  entry_points={
      'console_scripts': [
          'graph2img = graph2img:main'
      ]
  },
)