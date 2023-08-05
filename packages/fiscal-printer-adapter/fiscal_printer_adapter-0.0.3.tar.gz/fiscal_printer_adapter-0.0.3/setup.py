# -*- coding: utf-8 -*-

import setuptools
from scripts import __version__

#with open("README.md", "r") as fh:
#    long_description = fh.read()

setuptools.setup(
    name="fiscal_printer_adapter",
    version=__version__,
    author="jeo Software",
    author_email="jorge.obiols@gmail.com",
    description='A standarized fiscal printer interface',
    long_description="""
FISCAL PRINTER ADAPTER [![Build Status](https://travis-ci.org/jobiols/fiscal_printer_adapter.svg?branch=master)](https://travis-ci.org/jobiols/fiscal_printer_adapter) [![codecov](https://codecov.io/gh/jobiols/fiscal_printer_adapter/branch/master/graph/badge.svg)](https://codecov.io/gh/jobiols/fiscal_printer_adapter) [![CodeFactor](https://www.codefactor.io/repository/github/jobiols/fiscal_printer_adapter/badge)](https://www.codefactor.io/repository/github/jobiols/fiscal_printer_adapter)
----------------------

Este es un adaptador para impresoras fiscales
Objetivos:

- Proveer una interfase uniforme entre marcas y modelos de impresoras fiscales
- Permitir conectar impresoras a la maquina local via puerto serie o a una maquina remota via websocket donde
residira un servicio que redirecciona los datos a un puerto serie.
- implementar una arquitectura simple que permita agregar facilmente nuevas marcas y modelos de impresoras
- Soporte para python 2 y 3

**Ejemplo**

    # create a Fiscal Printer Adapter with brand and model
    fpa = FPA('epson', 'TMU220')

    # open serial connection in local computer to fiscal printer
    fpa.open('COM1', 9600)

    # open serial connection in remote computer to fiscal printer
    fpa.open('COM1', 9600, host='192.168.1.54', port=34144)

    """,
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
