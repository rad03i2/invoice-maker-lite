"""Core invoice model, validation and calculations."""
from __future__ import annotations
from dataclasses import dataclass, field, asdict
from datetime import date
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
import re
from typing import Iterable

MONEY = Decimal("0.01")
CURRENCY_RE = re.compile(r"^[A-Z]{3}$")

class InvoiceError(ValueError):
    """Raised for invalid invoice data."""

def money(value: object) -> Decimal:
    try:
        result = Decimal(str(value)).quantize(MONEY, rounding=ROUND_HALF_UP)
    except (InvalidOperation, ValueError) as exc:
        raise InvoiceError(f"Invalid monetary value: {value}") from exc
    if result < 0:
        raise InvoiceError("Monetary values cannot be negative")
    return result

@dataclass(frozen=True)
class LineItem:
    description: str
    quantity: Decimal
    unit_price: Decimal

    @classmethod
    def create(cls, description: str, quantity: object, unit_price: object) -> "LineItem":
        description = description.strip()
        if not description:
            raise InvoiceError("Item description is required")
        try:
            qty = Decimal(str(quantity))
        except InvalidOperation as exc:
            raise InvoiceError("Quantity must be numeric") from exc
        if qty <= 0:
            raise InvoiceError("Quantity must be greater than zero")
        return cls(description, qty, money(unit_price))

    @property
    def total(self) -> Decimal:
        return (self.quantity * self.unit_price).quantize(MONEY, rounding=ROUND_HALF_UP)

@dataclass
class Invoice:
    number: str
    customer: str
    issue_date: str
    due_date: str
    currency: str = "USD"
    tax_rate: Decimal = Decimal("0")
    discount: Decimal = Decimal("0")
    notes: str = ""
    items: list[LineItem] = field(default_factory=list)
    status: str = "draft"

    def validate(self) -> None:
        self.number = self.number.strip()
        self.customer = self.customer.strip()
        if not self.number or not self.customer:
            raise InvoiceError("Invoice number and customer are required")
        try:
            issued, due = date.fromisoformat(self.issue_date), date.fromisoformat(self.due_date)
        except ValueError as exc:
            raise InvoiceError("Dates must use YYYY-MM-DD") from exc
        if due < issued:
            raise InvoiceError("Due date cannot precede issue date")
        self.currency = self.currency.upper()
        if not CURRENCY_RE.fullmatch(self.currency):
            raise InvoiceError("Currency must be a three-letter ISO-style code")
        self.tax_rate = money(self.tax_rate)
        if self.tax_rate > 100:
            raise InvoiceError("Tax rate cannot exceed 100%")
        self.discount = money(self.discount)
        if self.status not in {"draft", "sent", "paid", "void"}:
            raise InvoiceError("Invalid invoice status")
        if not self.items:
            raise InvoiceError("At least one line item is required")
        if self.discount > self.subtotal:
            raise InvoiceError("Discount cannot exceed subtotal")

    @property
    def subtotal(self) -> Decimal:
        return sum((i.total for i in self.items), Decimal("0.00"))

    @property
    def taxable(self) -> Decimal:
        return self.subtotal - self.discount

    @property
    def tax(self) -> Decimal:
        return (self.taxable * self.tax_rate / 100).quantize(MONEY, rounding=ROUND_HALF_UP)

    @property
    def total(self) -> Decimal:
        return self.taxable + self.tax

    def to_dict(self) -> dict:
        return {"number": self.number, "customer": self.customer, "issue_date": self.issue_date,
                "due_date": self.due_date, "currency": self.currency, "tax_rate": str(self.tax_rate),
                "discount": str(self.discount), "notes": self.notes, "status": self.status,
                "items": [{"description": i.description, "quantity": str(i.quantity),
                           "unit_price": str(i.unit_price), "total": str(i.total)} for i in self.items],
                "subtotal": str(self.subtotal), "tax": str(self.tax), "total": str(self.total)}
