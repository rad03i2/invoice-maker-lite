# Invoice Maker Lite — English Guide

[← Back to the repository overview](README.md)

## Overview

Invoice Maker Lite is a local-first Python CLI for creating, storing, searching, tracking, and exporting invoices. It uses SQLite for records and Decimal arithmetic for money calculations.

The project intentionally stays narrow: invoice records and portable exports without cloud accounts, payment processing, or external runtime services.

## Installation

~~~bash
git clone https://github.com/rad03i2/invoice-maker-lite.git
cd invoice-maker-lite
python -m venv .venv
python -m pip install -e .
invoice-maker --version
~~~

## Create an invoice

~~~bash
invoice-maker new INV-2026-001   --customer "Example Studio"   --issue 2026-09-21   --due 2026-10-05   --currency USD   --tax 5   --discount 10   --notes "Thank you"   --item "Design|2|50"   --item "Hosting|1|20"
~~~

Each <code>--item</code> uses:

~~~text
DESCRIPTION|QTY|PRICE
~~~

At least one item is required.

## Validation and calculations

The current implementation requires:

- non-empty invoice number and customer;
- ISO-format dates (<code>YYYY-MM-DD</code>);
- due date on or after issue date;
- three-letter currency syntax;
- tax rate between 0 and 100;
- non-negative money values;
- positive item quantities;
- fixed discount no greater than subtotal.

Money is quantized to two decimal places using <code>ROUND_HALF_UP</code>.

## List and search

~~~bash
invoice-maker list
invoice-maker list --status draft
invoice-maker list --customer Studio
invoice-maker list --status sent --customer Studio
invoice-maker list --json
~~~

Customer filtering is a partial SQLite <code>LIKE</code> match.

## Show a record

~~~bash
invoice-maker show INV-2026-001
invoice-maker show INV-2026-001 --json
~~~

## Status workflow

Supported values:

- <code>draft</code>
- <code>sent</code>
- <code>paid</code>
- <code>void</code>

Set one:

~~~bash
invoice-maker status INV-2026-001 sent
~~~

These values are local workflow markers, not externally verified payment events.

## Export

### HTML

~~~bash
invoice-maker export INV-2026-001   --format html   --output invoice.html
~~~

The HTML is suitable for browser printing. To create a PDF, open the file and use Print → Save as PDF.

### JSON

~~~bash
invoice-maker export INV-2026-001   --format json   --output invoice.json
~~~

Existing output files are protected unless <code>--overwrite</code> is provided.

## Delete

~~~bash
invoice-maker delete INV-2026-001 --yes
~~~

The CLI requires the explicit <code>--yes</code> switch.

## Database

Default location:

~~~text
~/.invoice-maker-lite/invoices.db
~~~

Override it using <code>INVOICE_MAKER_DB</code> or the global <code>--db PATH</code> option.

The application does not encrypt the SQLite file.

## HTML safety

User-controlled customer, item, notes, and status text is escaped before HTML rendering.

This reduces HTML injection risk in generated invoice files but does not replace safe handling of the resulting documents.

## Tests

~~~bash
python -m pip install -e . pytest
python -m pytest -q
invoice-maker --version
~~~

CI runs on Ubuntu, Windows, and macOS with Python 3.10, 3.12, and 3.13.

## Current limitations

- HTML and JSON export only.
- PDF is created through browser printing.
- No payment processing.
- No automatic email delivery.
- No cloud sync.
- No currency conversion.
- One percentage tax rate.
- One fixed invoice-level discount.
- SQLite is unencrypted.
- No multi-user coordination.

## Architecture

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

## Author

**Radwan Abd alhady Ahmed**  
**رضوان عبدالهادي**  
GitHub: [@rad03i2](https://github.com/rad03i2)

## License

MIT — see [LICENSE](LICENSE).
