import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="thebamlib",
    version="0.0.1",
    author="Chris Siegel (https://github.com/blarmon)",
    author_email="c.siegel1991@gmail.com",
    description="A python library that makes it easy to utilize the bank-account-microservice microservice.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/blarmon/bamlib",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)