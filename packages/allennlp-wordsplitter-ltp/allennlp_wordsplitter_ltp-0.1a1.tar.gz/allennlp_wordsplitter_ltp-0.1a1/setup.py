#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
setuptools script file
"""

from setuptools import setup, find_packages

setup(
    name='allennlp_wordsplitter_ltp',
    namespace_packages=[],
    packages=find_packages('src'),
    package_dir={'': 'src'},

    description='LTP word splitter for AllenNLP',
    url='https://github.com/tanbro/allennlp_wordsplitter_ltp',
    author='liu xue yan',
    author_email='liu_xue_yan@foxmail.com',

    use_scm_version={
        # guess-next-dev:   automatically guesses the next development version (default)
        # post-release:     generates post release versions (adds postN)
        'version_scheme': 'guess-next-dev',
        'write_to': 'src/allennlp_wordsplitter_ltp/_version.py',
    },
    setup_requires=['setuptools_scm', 'setuptools_scm_git_archive'],

    install_requires=[
        'allennlp<0.9,>=0.7',
        'requests',
        'overrides',
    ],

    extras_require={
        'ltp': ['pyltp'],
    },

    tests_require=[],
)
