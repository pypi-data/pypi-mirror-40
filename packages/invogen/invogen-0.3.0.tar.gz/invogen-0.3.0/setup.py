"""Invogen"""

import setuptools

from invogen import __version__


__author__ = "Samuel Searles-Bryant"


with open("README.md", "r") as f:
    LONG_DESCRIPTION = f.read()


setuptools.setup(
    name="invogen",
    version=__version__,
    description="Generate beautiful invoices using Python.",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author=__author__,
    author_email="devel@samueljsb.co.uk",
    url="https://github.com/samueljsb/InvoGen",
    license="MIT",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=["Jinja2>=2.10"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    project_urls={
        "Documentation": "https://invogen.readthedocs.io",
        "Bug Reports": "https://github.com/samueljsb/InvoGen/issues",
    },
)
