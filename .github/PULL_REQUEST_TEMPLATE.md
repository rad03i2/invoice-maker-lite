## Summary

Describe the invoice workflow or repository problem and the focused change that solves it.

## Validation

- [ ] `python -m pytest -q`
- [ ] `invoice-maker --version`
- [ ] Tests were added or updated for behavior changes
- [ ] User-visible CLI changes are documented

## Data and financial safety

- [ ] No real customer data or invoice databases were committed
- [ ] Decimal money behavior remains intentional
- [ ] HTML escaping remains intact where relevant
- [ ] Overwrite and deletion behavior remain explicit
- [ ] Current feature claims match tested behavior

## Notes

Add compatibility, security, migration, or follow-up context here.
