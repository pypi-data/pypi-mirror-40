import setuptools
from distutils.core import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="checkword",
    version="0.0.3",
    author="Bakhrom Rakhmonov",
    author_email="alex960126@gmail.com",
    description="Package for checking text for existance of blacklisted or whitelisted words",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alexb007/checkword",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)