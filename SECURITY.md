# Security Policy

## Scope

Invoice Maker Lite stores invoice data locally in SQLite and exports HTML or JSON. Invoice records can contain sensitive customer and business information.

## Supported code

Security fixes target the current `main` branch and any current release explicitly published by the repository.

## Current protections

The implementation currently:

- performs no application-level network requests;
- escapes user-controlled strings in HTML exports;
- rejects duplicate invoice numbers unless overwrite is explicit;
- rejects existing export files unless overwrite is explicit;
- requires `--yes` before CLI deletion;
- writes exports through a temporary file before replacement.

## Important boundaries

The SQLite database is **not encrypted** by the application.

The project does not provide:

- user authentication;
- role-based access control;
- multi-user isolation;
- encrypted backups;
- automatic remote backup;
- secure deletion;
- payment verification;
- email delivery security.

Protect the host user account, filesystem permissions, and backups according to the sensitivity of the invoice data.

## Reporting a vulnerability

Use GitHub's private security reporting features when available.

A useful report includes affected version or commit, minimal reproduction steps with fictional data, impact, and any known mitigation.

Do not publish customer data, invoice databases, credentials, or sensitive business records in a public issue.

## Privacy

Local-only operation reduces unnecessary data transfer, but it does not by itself make invoice data secure. Anyone who can read the database file may be able to read stored invoice information.
