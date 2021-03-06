from setuptools import setup, find_namespace_packages

setup(name='miniSearchEngine',
      packages=find_namespace_packages(include=["miniSearchEngine", "miniSearchEngine.*"]),
      version='1.0.0',
      description='Course Project for ZJU 2021 Information Retrieval and Web Search.',
      url='https://github.com/cuteyyt/searchEngine',
      author='youtan YIN, jiawei HUANG, bingyang FU',
      author_email='youtanyin@zju.edu.cn',
      license='Apache License Version 2.0, January 2004',
      install_requires=[
          "numpy",
          "pandas",
          "nltk",
          "easydict",
          "tqdm",
      ],
      entry_points={
          'console_scripts': [
              'construct_engine = miniSearchEngine.construct_engine.construct:main',
              'start_engine = miniSearchEngine.search_engine.interaction:start'
          ],
      },
      keywords=['search engine']
      )
