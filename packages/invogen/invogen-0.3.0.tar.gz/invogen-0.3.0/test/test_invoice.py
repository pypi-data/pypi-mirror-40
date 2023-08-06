"""Unit tests for the invogen.invoice module."""

from decimal import Decimal

import pytest

from invogen.invoice import Invoice, InvoiceEntry
from invogen.accounts import Customer, User


class TestInvoice:
    """Tests for the Invoice class"""

    def test_invoice_init(self, customer, user):
        """Test Invoice inits correctly."""
        entry_1 = InvoiceEntry("id 1")
        entry_2 = InvoiceEntry("id 2")
        entries = [entry_1, entry_2]
        invoice = Invoice(user=user, customer=customer, entries=entries)
        assert invoice.user == user
        assert invoice.customer == customer
        assert invoice.entries == entries
        assert invoice.shipping == 0
        assert invoice.discount == 0

    def test_invoice_increments_customer_number(self):
        """Test that the customer account number increments."""
        customer = Customer(number=3)
        invoice = Invoice(customer=customer)
        assert invoice.customer.number == 4

    def test_invoice_attrs(self, invoice, customer, user):
        """Test Invoice attributes can be added."""
        invoice.user = user
        invoice.customer = customer
        entry_1 = InvoiceEntry("id 1")
        entry_2 = InvoiceEntry("id 2")
        invoice.add_entry(entry_1)
        invoice.add_entry(entry_2)
        invoice.shipping = 5
        invoice.discount = 9
        assert invoice.user == user
        assert invoice.customer == customer
        assert invoice.entries == [entry_1, entry_2]
        assert invoice.shipping == 5
        assert invoice.discount == 9

    def test_invoice_shipping_is_decimal(self, invoice):
        """Test Invoice.shipping and Invoice.discount are Decimal."""
        invoice.shipping = 5
        invoice.discount = 9
        assert isinstance(invoice.shipping, Decimal)
        assert isinstance(invoice.discount, Decimal)

    def test_invoice_discount_is_positive(self, invoice):
        """Test Invoice.discount is always >= 0."""
        invoice.discount = -3
        assert invoice.discount == 0

    def test_get_sub_total_of_invoice(self, invoice):
        """Test Invoice.sub_total can get."""
        invoice.add_entry(InvoiceEntry(rate=3, quantity=4))
        invoice.add_entry(InvoiceEntry(rate=5, quantity=6))
        assert invoice.sub_total == 42

    def test_sub_total_is_decimal(self, invoice):
        """Test Invoice.sub_total is a Decimal."""
        invoice.add_entry(InvoiceEntry(rate=3, quantity=4))
        assert isinstance(invoice.sub_total, Decimal)

    def test_get_total_of_invoice(self, invoice):
        """Test Invoice.total can get."""
        invoice.add_entry(InvoiceEntry(rate=3, quantity=4))
        invoice.add_entry(InvoiceEntry(rate=5, quantity=6))
        invoice.shipping = 5
        assert invoice.total == 47

    def test_total_is_decimal(self, invoice):
        """Test Invoice.total is a Decimal."""
        invoice.add_entry(InvoiceEntry(rate=3, quantity=4))
        assert isinstance(invoice.total, Decimal)

    def test_invoice_str(self, invoice):
        """Test string method works."""
        invoice = Invoice(
            customer=Customer(account_name="Test", name="Foobar ltd")
        )
        invoice.add_entry(InvoiceEntry("123", "Some stuff", 3, 4))
        invoice.add_entry(InvoiceEntry("124", "Some other stuff", 3, 5))
        invoice.shipping = 5
        invoice.discount = 10
        expected_str = "\n".join(
            [
                "Invoice for Foobar ltd (Test)",
                "|   ID   |     Description      |   Rate   | Quantity |"
                "  Amount  |",
                "+--------+----------------------+----------+----------+"
                "----------+",
                "| 123    | Some stuff           |     3.00 |        4 |"
                "    12.00 |",
                "| 124    | Some other stuff     |     3.00 |        5 |"
                "    15.00 |",
                "+--------+----------------------+----------+----------+"
                "----------+",
                "                                             Sub-total:"
                "    27.00",
                "                                              Shipping:"
                "     5.00",
                "                                              Discount:"
                "   -10.00",
                "                                           +-----------"
                "----------+",
                "                                                 Total:"
                "    22.00",
            ]
        )
        assert str(invoice) == expected_str


class TestInvoiceEntries:
    """Tests for the InvoiceEntry class"""

    def test_invoice_init(self):
        """Test InvoiceEntry.id_code inits correctly."""
        entry = InvoiceEntry(
            id_code="entry id",
            description="entry description",
            rate=1,
            quantity=2,
        )
        assert entry.id_code == "entry id"
        assert entry.description == "entry description"
        assert entry.rate == 1
        assert entry.quantity == 2

    def test_empty_invoice_is_decimal(self):
        """Test InvoiceEntry attrs are Decimal."""
        entry = InvoiceEntry()
        assert isinstance(entry.rate, Decimal)
        assert isinstance(entry.quantity, Decimal)
        assert isinstance(entry.amount, Decimal)

    def test_invoice_entry_rate_accepts_str(self):
        """Test InvoiceEntry.rate accepts string input."""
        _ = InvoiceEntry(rate="1")

    def test_invoice_entry_quantity_accepts_str(self):
        """Test InvoiceEntry.quantity accepts string input."""
        _ = InvoiceEntry(quantity="2")

    def test_empty_invoice_entry_amount_is_zero(self):
        """Test InvoiceEntry.amount is 0 for an empty entry."""
        entry = InvoiceEntry()
        assert entry.amount == 0

    @pytest.mark.parametrize(
        "rate, qty, amount", [(3, 4, 12), (0, 4, 0), (3, 0, 0), (30, 0.4, 12)]
    )
    def test_invoice_entry_amount(self, rate, qty, amount):
        """Test InvoiceEntry.amount returns the correct value."""
        entry = InvoiceEntry(rate=rate, quantity=qty)
        assert entry.amount == amount

    def test_invoice_entry_amount_is_decimal(self):
        """Test InvoiceEntry.amount is a Decimal."""
        entry = InvoiceEntry(rate=3, quantity=4)
        assert isinstance(entry.amount, Decimal)

    def test_invoice_entry_info(self):
        """Test InvoiceEntry.info returns the correct dict."""
        entry = InvoiceEntry(
            id_code="entry id",
            description="entry description",
            rate=3,
            quantity=4,
        )
        expected_info = {
            "id_code": "entry id",
            "description": "entry description",
            "rate": Decimal("3.00"),
            "quantity": Decimal("4"),
            "amount": Decimal("12.00"),
        }
        assert entry.info == expected_info

    def test_invoice_entry_str(self):
        """Test string method works."""
        entry = InvoiceEntry(
            id_code="id123",
            description="entry description",
            rate=3,
            quantity=4,
        )
        expected_str = "\n".join(
            [
                "|   ID   |     Description      |   Rate   | Quantity |"
                "  Amount  |",
                "+--------+----------------------+----------+----------+"
                "----------+",
                "| id123  | entry description    |     3.00 |        4 |"
                "    12.00 |",
            ]
        )
        assert str(entry) == expected_str

    def test_invoice_entry_latex(self):
        """Test latex method works."""
        entry = InvoiceEntry(
            id_code="id123",
            description="entry description",
            rate=3,
            quantity=4,
        )
        expected_latex = "id123 & entry description & 3.00 & 4 & 12.00"
        assert entry.latex() == expected_latex
