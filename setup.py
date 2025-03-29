from setuptools import setup

setup(
    name='boggle',
    version='0.1.0',
    py_modules=['boggle'],
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'boggle = boggle:cli',
        ],
    },
)