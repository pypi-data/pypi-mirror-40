import sys
from distutils.core import setup

from setuptools import find_packages

if sys.version_info < (3,):
    sys.exit('Sorry, Python3 is required for thseq.')

with open('requirements.txt') as r:
    requires = [l.strip() for l in r]

setup(
    name='Lunas',
    version='0.1.0',
    author='Seann Zhang',
    author_email='pluiefox@live.com',
    packages=find_packages(),
    url='http://pypi.python.org/pypi/Lunas/',
    license='LICENSE.txt',
    description='A dataset processing pipeline and iterator for '
                'machine learning with minimal dependencies.',
    long_description=open('README.txt').read(),
    install_requires=requires,
)
