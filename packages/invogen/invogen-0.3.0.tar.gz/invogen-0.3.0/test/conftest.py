"""Pytest configuration for tests for the InvoGen package"""

import pytest

from invogen.accounts import User, Customer
from invogen.invoice import Invoice


@pytest.fixture
def user():
    return User()


@pytest.fixture
def customer():
    return Customer()


@pytest.fixture
def invoice():
    return Invoice()
