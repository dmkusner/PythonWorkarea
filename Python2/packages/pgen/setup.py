import os
from setuptools import setup, find_packages

# Utility function to read the README file.
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "pgen",
    version = "1.0.0",
    author = "David Kusner",
    author_email = "dmkusner@gmail.com",
    description = ("Tools for password management"),
    packages=['pgen'],
    long_description=read('README'),
    install_requires = ['pandas>=0.16.0'],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'pgen=pgen.pgen:main',
            'pgenLookup=pgen.pgenLookup:main'
        ],
    }
)
