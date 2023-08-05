from setuptools import setup
from setuptools import find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='oreopy',
      version='0.0.2',
      author='Alexey Makridenko',
      author_email='makridenko.a@yandex.ru',
      long_description=long_description,
     )
