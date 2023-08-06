"""
    invogen
    -------

    A package to generate beautiful LaTeX invoices with Python

    :copyright: © 2018 Samuel Searles-Bryant.
    :license: MIT, see LICENSE for more details.
"""
__version__ = "0.3.0"

from invogen.invoice import Invoice, InvoiceEntry
from invogen.accounts import User, Customer
from invogen.template import LatexTemplate
