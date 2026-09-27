# Support

## Before opening an issue

1. Confirm Python 3.10 or newer is installed.
2. Install the package and test dependency:
   ~~~bash
   python -m pip install -e . pytest
   ~~~
3. Run:
   ~~~bash
   python -m pytest -q
   invoice-maker --version
   ~~~
4. Reproduce the problem with fictional invoice and customer data.

## Useful bug-report details

Include your operating system, Python version, exact CLI command, expected behavior, actual behavior, and stderr or traceback output where relevant.

Do not attach real invoice databases or customer records.

## Common questions

### Where is the database?

By default: `~/.invoice-maker-lite/invoices.db`.

Override it with `INVOICE_MAKER_DB` or `--db PATH`.

### Why can’t I export directly to PDF?

The current exporter supports HTML and JSON. Open the HTML file in a browser and use Print → Save as PDF.

### Why was my export refused?

Existing export files are protected unless `--overwrite` is supplied.

### Why was my invoice number rejected as a duplicate?

Invoice number is the SQLite primary key. Use a different number, or intentionally use overwrite behavior when creating the record.

### Does “paid” mean a payment was verified?

No. `paid` is a local lifecycle status set by the user.

## Security

Do not publish database files, customer data, or sensitive invoice contents in public issues. Follow [SECURITY.md](SECURITY.md).
