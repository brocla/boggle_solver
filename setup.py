from setuptools import setup
import sysconfig
import os
import sys

# trie.pkl must land next to trie.py in site-packages
rel_purelib = os.path.relpath(sysconfig.get_path('purelib'), sys.prefix)

setup(
    name='Boggle',
    author='Kevin Brown',
    version='0.1.1',
    py_modules=['boggle', 'trie', 'helpers', 'is_boggleable'],
    data_files=[
        (rel_purelib, ['trie.pkl']),
    ],
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'boggle = boggle:cli',
            'is-boggleable = is_boggleable:cli',
        ],
    },
)
