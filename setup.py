from setuptools import setup, find_packages
import os

setup(
    name='Boggle',
    author='Kevin Brown',
    version='0.1.0',
    py_modules=['boggle', 'trie'],
    package_data={"boggle":["trie.pkl"]},
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'boggle = boggle:cli',
        ],
    },
)