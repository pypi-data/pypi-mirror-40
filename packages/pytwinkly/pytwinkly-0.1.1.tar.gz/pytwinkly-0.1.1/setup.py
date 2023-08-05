import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pytwinkly",
    version="0.1.1",
    author="Scott Jones",
    author_email="scott.jones4k@gmail.com",
    description="A package for integrating with twinkly lights",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/scottjones4k/pytwinkly",
    packages=setuptools.find_packages(),
    install_requires=[
        "requests",
    ],
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)