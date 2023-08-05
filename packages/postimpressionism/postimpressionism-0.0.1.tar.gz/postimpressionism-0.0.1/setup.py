# -*- coding: utf-8 -*-
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='postimpressionism',
    version='0.0.1',
    url='https://github.com/AkiraDemenech/Postimpressionism',
    license='MIT License',
    author='Akira Demenech',
    author_email='akira.demenech@gmail.com',
    keywords='art image postproduction postimpressionism',
    description="An Art Exploration Package based on Modernist Avant-garde",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['postimpressionism'],
    install_requires=['numpy', 'pillow'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)