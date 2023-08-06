import os
from setuptools import setup


with open("README.txt") as f:
    read = f.read()


setup(
    name = "Giraffe2D",
    version = '1.1.12',
    description = "This Is A PyGame Powered And OpenGL Powered Game Engine", 
    install_requires=["wget", "pygame", "PyOpenGL"],
    py_modules="Giraffe2D",
    package_dir = {'': 'Engine'},
    url='https://github.com/CrypticCoding/Girrafee2D',
    author="Saugat Siddiky Jarif",
    author_email="saugatjarif@gmail.com",
    license="MIT",
    long_description=read,
    
)
