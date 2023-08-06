#
# python3 setup.py sdist bdist_wheel
# twine upload --repository-url https://upload.pypi.org/legacy/ dist/*
# pip install big-pkg -U
#
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="big_pkg",
    version="0.0.18",
    author="Zach Chen",
    author_email="zach_chen@joybien.com",
    description="A small example package for test v7",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
