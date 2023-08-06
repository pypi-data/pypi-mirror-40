from distutils.core import setup
from setuptools import find_packages

setup(
    name = 'pyrainzplay',
    packages = ['pyrainzplay','pyrainzplay.scripts','pyrainzplay.funclib'],
    version = '0.0.6',
    license='Personal',
    description = 'Playground app for py first timers!',
    author = 'Rainz',
    author_email = 'cbludev@gmail.com',
    url = 'https://github.com/cbludev/pyrainzplay',
    download_url = 'https://github.com/cbludev/pyrainzplay/archive/0.0.6.zip',
    keywords = ['numpy'],
    install_requires=[
        'numpy',
    ],
)
