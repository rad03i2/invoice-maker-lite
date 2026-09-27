# Architecture

Invoice Maker Lite is a small local-first Python CLI built around four focused modules: validation/calculation, SQLite storage, export rendering, and command orchestration.

## Data flow

~~~text
CLI input
  |
  v
Invoice + LineItem validation
  |
  +--> Decimal money calculations
  |
  v
SQLite Store
  |
  +--> list / search
  +--> status updates
  +--> delete
  |
  v
HTML or JSON export
~~~

## Components

### `src/invoice_maker/core.py`

Defines the invoice model and financial calculations.

Key behaviors:

- invoice number and customer are required;
- issue/due dates use `YYYY-MM-DD`;
- due date cannot precede issue date;
- currency is validated as exactly three letters;
- tax is a percentage between 0 and 100;
- discount is a fixed monetary amount;
- at least one line item is required;
- discount cannot exceed subtotal;
- monetary values are quantized to two decimal places with `ROUND_HALF_UP`.

The currency check is syntax validation only. The project does not query an ISO currency registry.

### `src/invoice_maker/storage.py`

Uses SQLite for local persistence.

Stored fields include invoice number, customer, issue and due dates, currency, tax rate, discount, notes, status, serialized line items, and created/updated timestamps.

The invoice number is the primary key. Duplicate numbers are rejected unless overwrite behavior is explicitly requested.

Indexes are created for customer lookup and invoice dates.

### `src/invoice_maker/render.py`

Exports invoices as HTML or JSON.

HTML uses `html.escape()` for customer-controlled text such as customer name, item descriptions, notes, and status.

Exports are written through a temporary sibling file and then replaced into the destination path. Existing outputs are rejected unless overwrite is explicit.

The project does not include a PDF rendering engine. PDF output is obtained by opening the HTML export in a browser and using Print → Save as PDF.

### `src/invoice_maker/cli.py`

Provides:

| Command | Purpose |
|---|---|
| `new` | Create and store an invoice |
| `list` | List/filter invoices |
| `show` | Show one invoice |
| `status` | Change lifecycle status |
| `export` | Write HTML or JSON |
| `delete` | Delete with explicit `--yes` |

Supported lifecycle states are `draft`, `sent`, `paid`, and `void`.

These are local record statuses. The application does not contact an external payment system to verify them.

## Storage location

Default:

~~~text
~/.invoice-maker-lite/invoices.db
~~~

Override with the `INVOICE_MAKER_DB` environment variable or per command with `--db PATH`.

The SQLite file is not encrypted by the application.

## Security boundaries

The project currently provides local-only behavior, escaped HTML output, duplicate invoice protection, explicit export overwrite behavior, and an explicit `--yes` requirement for deletion.

It does not provide database encryption, access control, multi-user concurrency coordination, automatic email delivery, cloud sync, remote backups, or external payment verification.

## Tests

The current test suite covers decimal rounding and totals, invalid date validation, SQLite round-trip, status updates, customer filtering, duplicate protection, HTML escaping, and export overwrite protection.
