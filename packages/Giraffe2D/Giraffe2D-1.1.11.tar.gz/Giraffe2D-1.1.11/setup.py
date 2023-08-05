from setuptools import setup



setup(
    name = "Giraffe2D",
    version = '1.1.11',
    description = "This Is A PyGame Powered And OpenGL Powered Game Engine", 
    install_requires=["wget", "pygame", "PyOpenGL"],
    py_modules=["Giraffe2D"],
    package_dir = {'': 'Engine'},
)
