import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dyngraphplot",
    version="1.2.2",
    author="Tilemachos Pechlivanoglou",
    author_email="tppehli@gmail.com",
    description="A module for plotting dynamic force-directed graphs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tipech/dyngraphplot",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
