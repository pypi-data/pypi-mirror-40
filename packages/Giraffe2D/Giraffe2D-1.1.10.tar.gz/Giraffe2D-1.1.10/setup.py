from setuptools import setup



setup(
    name = "Giraffe2D",
    version = '1.1.10',
    description = "This Is A PyGame Powered And OpenGL Powered Game Engine", 
    install_requires=["wget", "pygame", "PyOpenGL"],
    package_dir = {'': 'Engine'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",

    ],
)
