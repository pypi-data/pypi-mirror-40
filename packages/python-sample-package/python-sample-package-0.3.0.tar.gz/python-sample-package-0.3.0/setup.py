from setuptools import setup, find_packages
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='python-sample-package',
    version='0.3.0',
    packages=find_packages(exclude=['tests*']),
    license='MIT',
    description='An example python package',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=['numpy'],
    url='https://github.com/iiddoo/python-sample-package.git',
    author='Ido Lev',
    author_email='iiddoolleevv@gmail.com',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
