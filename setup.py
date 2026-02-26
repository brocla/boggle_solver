from setuptools import setup
import sysconfig
import os
import sys

# Get site-packages relative to sys.prefix
# On Windows this gives: Lib\site-packages
# On Linux/Mac this gives: lib/pythonX.Y/site-packages
purelib = sysconfig.get_path('purelib')
rel_purelib = os.path.relpath(purelib, sys.prefix)

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
