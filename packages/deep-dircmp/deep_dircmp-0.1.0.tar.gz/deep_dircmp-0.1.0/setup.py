import os
from setuptools import setup, find_packages

PACKAGE_NAME = 'deep_dircmp'


def read_package_variable(key):
    """Read the value of a variable from the package without importing."""
    module_path = os.path.join(PACKAGE_NAME, '__init__.py')
    with open(module_path) as module:
        for line in module:
            parts = line.strip().split(' ')
            if parts and parts[0] == key:
                return parts[-1].strip("'")
    raise KeyError("'{0}' not found in '{1}'".format(key, module_path))


version = read_package_variable('__version__')

setup(
    name=PACKAGE_NAME,
    version=version,
    description='A recursive directory comparison',
    author='Mitar',
    license='BSD',
    packages=find_packages(),
    url='https://github.com/mitar/python-deep-dircmp',
)
