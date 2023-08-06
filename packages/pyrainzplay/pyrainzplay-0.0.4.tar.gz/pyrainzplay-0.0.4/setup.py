from distutils.core import setup
from setuptools import find_packages

setup(
    name = 'pyrainzplay',
    packages = find_packages(),
    version = '0.0.4',
    license='MIT',
    description = 'Playground app for py first timers!',
    author = 'Rainz',
    author_email = 'cbludev@gmail.com',
    url = 'https://github.com/cbludev/pyrainzplay',
    download_url = 'https://github.com/cbludev/pyrainzplay/archive/0.0.4.zip',
    keywords = ['numpy'],
    install_requires=[
        'numpy',
    ],
)
