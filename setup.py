import os

from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='PhrasePicker',
    version='0.1',
    packages=['utils'],
    url='https://github.com/WhiteAu/PhrasePicker',
    license='Apache 2.0',
    author='whiteau',
    author_email='',
    description='a toy project to pick out duplicate phrases from a passage',
    long_description=read('README.md'),
    install_requires=['nltk']
)
