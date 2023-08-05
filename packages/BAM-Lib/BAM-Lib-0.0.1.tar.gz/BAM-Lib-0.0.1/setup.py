import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="BAM-Lib",
    version="0.0.1",
    author="Chris Siegel",
    author_email="c.siegel1991@gmail.com",
    description="a library for interacting with a fake microservice I've created",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/blarmon/BAM-Lib",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)