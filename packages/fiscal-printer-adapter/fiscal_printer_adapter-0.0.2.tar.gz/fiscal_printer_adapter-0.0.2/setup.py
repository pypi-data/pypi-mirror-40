# -*- coding: utf-8 -*-

import setuptools
from scripts import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fiscal_printer_adapter",
    version=__version__,
    author="jeo Software",
    author_email="jorge.obiols@gmail.com",
    description='A standarized fiscal printer interface',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jobiols/fiscal_printer_adapter",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Testing :: Unit",
        "Topic :: System :: Software Distribution",
    ],
      keywords="odoo docker environment",
)
