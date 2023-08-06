"""Unit tests for the invogen.accounts module."""

import pytest

from invogen.accounts import User, Customer


class TestUser:
    """Tests for the User class"""

    def test_user_init(self):
        """Test User inits correctly."""
        name = "username"
        email = "username@example.com"
        address = ["Address 1", "Address 2"]
        phone = "01234567890"
        account_number = "012345"
        sort_code = "012345"
        user = User(
            name=name,
            email=email,
            address=address,
            phone=phone,
            account_number=account_number,
            sort_code=sort_code,
        )
        assert user.name == name
        assert user.email == email
        assert user.address == address
        assert user.phone == phone
        assert user.account_number == account_number
        assert user.sort_code == sort_code

    def test_user_attrs(self, user):
        """Test User attributes can be set."""
        name = "username"
        email = "username@example.com"
        address = ["Address 1", "Address 2"]
        phone = "01234567890"
        account_number = "012345"
        sort_code = "012345"
        user.name = name
        user.email = email
        user.address = address
        user.phone = phone
        user.account_number = account_number
        user.sort_code = sort_code
        assert user.name == name
        assert user.email == email
        assert user.address == address
        assert user.phone == phone
        assert user.account_number == account_number
        assert user.sort_code == sort_code

    def test_user_sort_code_accepts_formatted_input(self, user):
        """Test User.sort_code accepts a formatted code."""
        user.sort_code = "01-23-45"
        assert user.sort_code == "012345"

    def test_user_info(self):
        """Test Customer.info returns correct dict"""
        user = User(
            name="username",
            email="name@example.com",
            address=["Address 1", "Address 2"],
            phone="01234 567890",
            account_number="123456",
            sort_code="123456",
        )
        expected_info = {
            "name": "username",
            "email": "name@example.com",
            "address": ["Address 1", "Address 2"],
            "phone": "01234 567890",
            "account_number": "123456",
            "sort_code": "123456",
        }
        assert user.info == expected_info

    def test_user_string(self):
        """Test string method works."""
        user = User(name="Test")
        assert str(user == "Test's account")

    def test_user_repr(self):
        """Test repr method works."""
        user = User(name="Test")
        assert repr(user) == "<User Test>"


class TestCustomer:
    """Tests for the Customer class"""

    def test_customer_init(self):
        """Test Customer inits correctly."""
        account_name = "account name"
        name = "name"
        address = ["Address 1", "Address 2"]
        number = 13
        customer = Customer(
            account_name=account_name,
            name=name,
            address=address,
            number=number,
        )
        assert customer.account_name == account_name
        assert customer.name == name
        assert customer.address == address
        assert customer.number == number

    def test_customer_attrs(self, customer):
        """Test Customer attributes can  be set."""
        account_name = "account name"
        name = "name"
        address = ["Address 1", "Address 2"]
        number = 13
        customer.account_name = account_name
        customer.name = name
        customer.address = address
        customer.number = number
        assert customer.account_name == account_name
        assert customer.name == name
        assert customer.address == address
        assert customer.number == number

    def test_default_customer_number_is_zero(self, customer):
        """Test the Customer.number is 0 if not set."""
        assert customer.number == 0

    def test_customer_number_is_not_int(self, customer):
        """Test TypeError raised if Customer.number is not int."""
        with pytest.raises(TypeError):
            customer.number = "13"

    def test_customer_info(self):
        """Test Customer.info returns correct dict"""
        customer = Customer(
            account_name="account name",
            name="name",
            email="name@example.com",
            address=["Address 1", "Address 2"],
            phone="01234 567890",
            number=13,
        )
        expected_info = {
            "account_name": "account name",
            "email": "name@example.com",
            "address": ["Address 1", "Address 2"],
            "phone": "01234 567890",
            "name": "name",
            "number": 13,
        }
        assert customer.info == expected_info

    def test_customer_string(self):
        """Test string method works."""
        customer = Customer(account_name="Test", name="Foobar ltd")
        assert str(customer) == "Foobar ltd (Test)"

    def test_customer_repr(self):
        """Test repr method works."""
        customer = Customer(account_name="Test", name="Foobar ltd")
        assert repr(customer) == "<Customer Foobar ltd (Test)>"
