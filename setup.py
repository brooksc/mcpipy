import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "mcpi",
    version = "1.0.1",
    author = "brooksc",
    description = ("Refer to mcpipy.com"),
    keywords = "raspberry pi minecraft python tutorial",
    url = "https://github.com/brooksc/mcpipy",
    packages=['mcpi', 'mcpi.examples'],
    long_description=read('README.md'),
)
