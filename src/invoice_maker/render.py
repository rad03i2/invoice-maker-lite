"""Portable HTML and JSON invoice exporters."""
from __future__ import annotations
import html, json
from pathlib import Path
from .core import Invoice

def render_html(inv: Invoice) -> str:
    inv.validate()
    esc=html.escape
    rows="".join(f"<tr><td>{esc(i.description)}</td><td>{i.quantity}</td><td>{i.unit_price:.2f}</td><td>{i.total:.2f}</td></tr>" for i in inv.items)
    notes=f"<section><h2>Notes</h2><p>{esc(inv.notes)}</p></section>" if inv.notes else ""
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Invoice {esc(inv.number)}</title><style>body{{font:16px system-ui;max-width:850px;margin:40px auto;padding:0 20px;color:#172033}}header{{display:flex;justify-content:space-between}}table{{width:100%;border-collapse:collapse;margin:28px 0}}th,td{{padding:10px;border-bottom:1px solid #ddd;text-align:left}}.totals{{margin-left:auto;width:320px}}.totals p{{display:flex;justify-content:space-between}}@media print{{body{{margin:0}}}}</style></head><body><header><div><h1>INVOICE</h1><strong>{esc(inv.number)}</strong></div><div>Issued: {inv.issue_date}<br>Due: {inv.due_date}<br>Status: {esc(inv.status)}</div></header><h2>Bill to</h2><p>{esc(inv.customer)}</p><table><thead><tr><th>Description</th><th>Qty</th><th>Unit</th><th>Total</th></tr></thead><tbody>{rows}</tbody></table><div class="totals"><p><span>Subtotal</span><b>{inv.subtotal:.2f} {inv.currency}</b></p><p><span>Discount</span><b>{inv.discount:.2f}</b></p><p><span>Tax ({inv.tax_rate}%)</span><b>{inv.tax:.2f}</b></p><p><span>Total</span><b>{inv.total:.2f} {inv.currency}</b></p></div>{notes}</body></html>'''

def export(inv: Invoice, output: str|Path, fmt: str, overwrite: bool=False) -> Path:
    p=Path(output)
    if p.exists() and not overwrite: raise FileExistsError(f"{p} exists; use --overwrite")
    p.parent.mkdir(parents=True,exist_ok=True)
    content=render_html(inv) if fmt=="html" else json.dumps(inv.to_dict(),ensure_ascii=False,indent=2)
    tmp=p.with_suffix(p.suffix+".tmp"); tmp.write_text(content,encoding="utf-8"); tmp.replace(p); return p
