import setuptools

# Code originally from https://github.com/aegirhall/console-menu/blob/develop/setup.py

import io
def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)



long_description = read("README.md", "CHANGELOG.md")



setuptools.setup(
    name="kusu",
    version="0.1.3",
    author="Kieran Wood",
    author_email="kieranw098@gmail.com",
    description="A set of utilities for developing python scripts",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Descent098/kusu",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)