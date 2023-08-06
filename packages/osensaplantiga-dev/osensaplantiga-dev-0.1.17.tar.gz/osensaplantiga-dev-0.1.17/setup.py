from setuptools import setup, find_packages

from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.txt'), encoding='utf-8') as f:
    long_description = f.read()

setup(
  name='osensaplantiga-dev',
  packages=find_packages(),
  install_requires=['pyserial', 'python-dateutil', 'xmodem', 'fastavro'],
  python_requires='>=3.6',
  version='0.1.17',
  description='OSENSA-Plantiga Python library',
  long_description=long_description,
  author='Plantiga',
  author_email='info@plantiga.com',
  license='MIT',
)
