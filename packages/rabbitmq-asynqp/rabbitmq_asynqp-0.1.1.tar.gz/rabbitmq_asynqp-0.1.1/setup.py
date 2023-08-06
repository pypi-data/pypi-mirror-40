from distutils.core import setup

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='rabbitmq_asynqp',
    version='0.1.1',
    author='Akshay Agarwal',
    author_email='akshay2agarwal@gmail.com',
    packages=setuptools.find_packages(),
    scripts=['bin/example.py'],
    url='http://pypi.python.org/pypi/rabbitmq_asynqp/',
    license='LICENSE.txt',
    description='Implementation of rabbitmq with asynqp',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        "asynqp >= 0.5.1",
    ],
)
