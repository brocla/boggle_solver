from setuptools import setup, find_packages
import os

setup(
    name='Boggle',
    author='Kevin Brown',
    version='0.1.0',
    py_modules=['boggle', 'trie'],
    #packages=find_packages(),
    package_data={"boggle":["trie.pkl"]},
    #py_modules=['boggle'],
    install_requires=[
        'Click',
        #f"Boggle @ file://localhost/Users/micro/OneDrive/Documents/python/kcb/Boggle#egg=trie",
        #"'Boggle @ file://localhost/%s/' % os.getcwd().replace('\\', '/'),
    ],
    entry_points={
        'console_scripts': [
            'boggle = boggle:cli',
        ],
    },
)