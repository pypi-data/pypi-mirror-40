import io
from os import path
from setuptools import setup

current_path = path.abspath(path.dirname(__file__))

with io.open(path.join(current_path, 'README.md'), 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='xintool',
    version='0.0.7',
    description='python opensource tools',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='http://blog.jiangyixin.top',
    author='jiangyixin',
    author_email='jyx15221613915@gmail.com',
    keywords='tools library',
    packages=['xintool'],
    install_requires=[],
    entry_points={}
)