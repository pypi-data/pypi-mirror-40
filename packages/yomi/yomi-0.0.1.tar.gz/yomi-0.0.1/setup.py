from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='yomi',
    version='0.0.1',
    description='Tools for running tournaments of AI agents against each-other',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/bluecoconut/yomi',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=['numpy', 'pandas'],
    extras_require={  # Optional
        'dev': ['pytest', 'flake8'],
    }
)
