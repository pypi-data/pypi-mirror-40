'''
This is a placeholder for accessing the location of project root directory.
This is needed to be able to read config.yaml from this package,
when it is distributed with setuptools and installed.
'''
import os


def path():
    return os.path.dirname(__file__)
