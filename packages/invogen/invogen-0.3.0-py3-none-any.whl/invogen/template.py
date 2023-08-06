"""
    invogen.template
    ----------------

    This module implements the template object.

    :copyright: © 2019 Samuel Searles-Bryant.
    :license: MIT, see LICENSE for more details.
"""

from os import remove
from subprocess import run, DEVNULL

import jinja2


class Template:
    """A base template using the default Jinja environment."""

    ENV_CONFIG = {"autoescape": True}

    def __init__(self, template_name):
        """
        Args:
            template_name (str): The filename of the template to be used.
        """
        environment = jinja2.Environment(
            **self.ENV_CONFIG,
            loader=jinja2.PackageLoader(__name__, "templates")
        )
        self.template = environment.get_template(template_name)

    @staticmethod
    def validate(invoice):
        """Ensure the invoice has all of the available attributes."""
        user_info = invoice.user.info
        customer_info = invoice.customer.info
        for attr in user_info:
            assert user_info[attr], "User has no {}".format(attr)
        for attr in customer_info:
            assert customer_info[attr], "Customer has no {}".format(attr)


class LatexTemplate(Template):
    """A LaTeX invoice template."""

    ENV_CONFIG = {
        "block_start_string": r"\BLOCK{",
        "block_end_string": r"}",
        "variable_start_string": r"\VAR{",
        "variable_end_string": r"}",
        "comment_start_string": r"\#{",
        "comment_end_string": r"}",
        "line_statement_prefix": r"%%",
        "line_comment_prefix": r"%#",
        "trim_blocks": True,
        "autoescape": False,
    }

    def to_pdf(self, invoice):
        """Generate a PDF of the invoice using LaTeX."""
        self.validate(invoice)
        temp_fname = "TEMP_{}.tex".format(__name__)
        job_name = "invoice_{}-{:03d}".format(
            invoice.customer.account_name, invoice.customer.number
        )
        output = self.template.render(
            invoice=invoice, user=invoice.user, customer=invoice.customer
        )

        with open(temp_fname, "w") as f:
            f.write(output)
        run(
            ["latexmk", "-pdf", "-jobname={}".format(job_name), temp_fname],
            stdout=DEVNULL,
            stderr=DEVNULL,
        )
        run(
            ["latexmk", "-jobname={}".format(job_name), "-c"],
            stdout=DEVNULL,
            stderr=DEVNULL,
        )
        remove(temp_fname)
