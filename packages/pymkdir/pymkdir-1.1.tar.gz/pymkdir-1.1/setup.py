"""
Setup module to build distribution packages of regex4ocr.
"""
from setuptools import setup

setup(
    name="pymkdir",
    version="1.1",
    url="https://github.com/IgooorGP/pymkdir",
    license="MIT",
    author="Igor Grillo Peternella",
    author_email="igor.feq@gmail.com",
    description="Create python folders with __init__.py files automagically!",
    packages=["pymkdir"],
    entry_points={"console_scripts": ["pymkdir=pymkdir.main:python_mkdir"]},
    install_requires=[],
    long_description=open("README.md").read(),
    zip_safe=False,
)

