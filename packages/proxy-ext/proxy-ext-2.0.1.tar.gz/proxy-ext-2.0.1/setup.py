# coding:utf-8
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="proxy-ext",
    version="2.0.1",
    author="@neoctobers",
    author_email="neoctobers@gmail.com",
    description="A Python proxy extension.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/neoctobers/py_proxy_ext",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'list-ext',
        'file-ext',
        'ip-query'
        'xprint',
    ],
)
