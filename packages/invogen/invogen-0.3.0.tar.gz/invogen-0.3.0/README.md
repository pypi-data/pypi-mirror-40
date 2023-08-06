# Invogen #

[![PyPI](https://img.shields.io/pypi/v/invogen.svg)](https://pypi.org/project/invogen/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/invogen.svg)](https://pypi.org/project/invogen/)
[![GitHub](https://img.shields.io/github/license/samueljsb/InvoGen.svg)](#license)
[![Travis (.org) branch](https://img.shields.io/travis/samueljsb/InvoGen/master.svg)](https://travis-ci.org/samueljsb/InvoGen)
[![Coverage Status](https://coveralls.io/repos/github/samueljsb/InvoGen/badge.svg?branch=master)](https://coveralls.io/github/samueljsb/InvoGen?branch=master)
[![Build The Docs](https://readthedocs.org/projects/invogen/badge/?version=latest)](https://invogen.readthedocs.io/en/latest/?badge=latest)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

InvoGen is a package to generate beautiful invoices using Python.

## Getting Started ##

To install InvoGen, simply run

```sh
pip install invogen
```

## Using InvoGen ##

InvoGen is easy to use! In the command prompt or in a file type:

```python
from invogen import *

foobar_inc = Customer("test", name="Foobar Inc.")
invoice = Invoice(foobar_inc)
invoice.add_entry(InvoiceEntry(
    id_code="Test01",
    description="Some entry item",
    rate=5,
    quantity=1,
))
invoice.shipping = 3
```

You can get a printout of your invoice like this:

```python
>>> print(invoice)

Invoice for Foobar Inc. (test)
|   ID   |     Description      |   Rate   | Quantity |  Amount  |
+--------+----------------------+----------+----------+----------+
| Test01 | Some entry item      |     5.00 |        1 |     5.00 |
+--------+----------------------+----------+----------+----------+
                                             Sub-total:     5.00
                                              Shipping:     3.00
                                              Discount:    -0.00
                                           +---------------------+
                                                 Total:     8.00
```

To generate a PDF invoice using the default LaTeX template, use

```python
template = LatexTemplate("default.tex")
template.to_pdf(invoice)
```

*N.B.*
To use LaTeX templates, you will have to have LaTeX installed.
You can find out how to install LaTeX for your system [here](https://www.latex-project.org/get/).

## Documentation ##

Documentation can be found on [Read the Docs](https://invogen.readthedocs.io)

The docs are built with Sphinx and autodoc.
To build the docs as html yourself, use

```sh
cd docs
make html
```

## Testing ##

The tests are in `/test`.
To run the tests with coverage, use

```sh
pytest
```

## Contributing ##

Please feel free to fork and open a pull request if you would like to change something.

The dependencies can be installed using pip and [`requirements.txt`](./requirements.txt) or Pipenv and the [`Pipfile`](./Pipfile).

More templates would be especially welcome!

## Authors ##

* Samuel Searles-Bryant - [website](https://samueljsb.co.uk)

## License ##

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
