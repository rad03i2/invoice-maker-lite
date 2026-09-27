# Contributing

Thank you for improving Invoice Maker Lite. Keep contributions focused, local-first, testable, and safe for invoice data.

## Development setup

~~~bash
git clone https://github.com/rad03i2/invoice-maker-lite.git
cd invoice-maker-lite
python -m pip install -e . pytest
~~~

## Required validation

~~~bash
python -m pytest -q
invoice-maker --version
~~~

For behavior changes, add or update tests and document user-visible CLI changes.

## Financial calculations

Do not replace Decimal-based money handling with binary floating-point arithmetic for invoice totals.

Changes affecting tax, discount, rounding, or totals must include explicit regression tests.

## Data privacy

Use fictional customers and invoice numbers in tests, documentation, screenshots, and examples.

Do not commit invoice databases, customer records, generated real invoices, credentials, environment files, or private business data.

## Export behavior

Keep HTML escaping intact for user-controlled text. Changes to overwrite behavior or deletion behavior should be deliberate and tested.

## Pull requests

Explain the problem, the implementation, compatibility/security impact, tests performed, and documentation updated.

By contributing, you agree that your contribution is licensed under the repository's MIT License.
