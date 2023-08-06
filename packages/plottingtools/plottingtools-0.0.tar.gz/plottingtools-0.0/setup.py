from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='plottingtools',
      version='0.0',
      description='A collection of tools for plotting graphs that I have used often enough (or are complex enough) for me to add to a repo',
      long_description=long_description,
      author='Joshua Beard',
      author_email='joshuabeard92@gmail.com',
      packages=['plottingtools'],
      install_requires=['numpy', 'matplotlib'],
      url='https://github.com/JoshuaBeard/plottingtools',
      )
