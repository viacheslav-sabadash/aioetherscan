# coding:utf-8
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aioetherscan",
    version="0.2.3",
    author="@viacheslav-sabadash",
    author_email="neoctobers@gmail.com",
    description="AioEtherscan.io API wrapper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/viacheslav-sabadash/aioetherscan",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
    ],
)
