"""pyWeMo setup script."""

from os import path
from setuptools import setup, find_packages

CONST_DESC = 'Lightweight Python module to discover and control WeMo devices'

# Read the contents of the README file

THIS_DIRECTORY = path.abspath(path.dirname(__file__))
with open(path.join(THIS_DIRECTORY, 'README.rst'), encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()

setup(name='pywemo',
      version='0.4.36',
      description=CONST_DESC,
      long_description=LONG_DESCRIPTION,
      long_description_content_type='text/markdown',
      url='http://github.com/pavoni/pywemo',
      author='Greg Dowling',
      author_email='mail@gregdowling.com',
      license='MIT',
      install_requires=['netifaces>=0.10.0', 'requests>=2.0', 'six>=1.10.0'],
      packages=find_packages(),
      zip_safe=True)
