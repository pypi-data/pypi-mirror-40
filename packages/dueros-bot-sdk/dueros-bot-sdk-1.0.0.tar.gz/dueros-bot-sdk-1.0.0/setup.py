# encoding: utf8

from setuptools import setup
from setuptools import find_packages

setup(
    name='dueros-bot-sdk',
    version='v1.0.0',
    author='jack',
    author_email='mupdf@sina.com',
    description='DuerOS Bot Python SDK',
    keywords='DuerOS Bot SDK',
    license='MIT',
    url='https://github.com/hotbaby/dueros-bot-sdk',
    packages=find_packages(),
    install_requires=['pycryptodome >= 3.6.6', 'requests', 'pyOpenSSL'],
    classifiers=[
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
