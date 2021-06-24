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
          "pandas",
          "nltk",
          "jieba"
      ],
      entry_points={
          'console_scripts': [
              'construct_engine = miniSearchEngine.construct_engine.construct:main',
              'add_stopwords = miniSearchEngine.help.edit_stop_words:add',
              'remove_stopwords = miniSearchEngine.help.edit_stop_words:remove',
              'reset_stopwords = miniSearchEngine.help.edit_stop_words:reset'
          ],
      },
      keywords=['search engine']
      )
