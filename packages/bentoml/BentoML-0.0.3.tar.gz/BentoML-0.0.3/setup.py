import os
import setuptools

# set __version__
exec(open('bentoml/version.py').read())

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="BentoML",
    version=__version__,
    author="atalaya.io",
    author_email="chaoyu@atalaya.io",
    description="BentoML: models to go",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/atalaya-io/BentoML",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)
