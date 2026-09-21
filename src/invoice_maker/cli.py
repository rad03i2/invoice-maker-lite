"""Command line interface."""
from __future__ import annotations
import argparse, json, os, sys
from pathlib import Path
from . import __version__
from .core import Invoice, LineItem, InvoiceError
from .storage import Store
from .render import export

def default_db(): return Path(os.environ.get("INVOICE_MAKER_DB", Path.home()/".invoice-maker-lite"/"invoices.db"))
def parser():
    p=argparse.ArgumentParser(prog="invoice-maker",description="Local-first invoice maker")
    p.add_argument("--db",default=str(default_db())); p.add_argument("--version",action="version",version=f"invoice-maker {__version__} — Radwan Abdulhadi Ahmed / @rad03i2")
    s=p.add_subparsers(dest="cmd",required=True)
    n=s.add_parser("new"); n.add_argument("number"); n.add_argument("--customer",required=True); n.add_argument("--issue",required=True); n.add_argument("--due",required=True); n.add_argument("--currency",default="USD"); n.add_argument("--tax",default="0"); n.add_argument("--discount",default="0"); n.add_argument("--notes",default=""); n.add_argument("--item",action="append",required=True,metavar="DESCRIPTION|QTY|PRICE"); n.add_argument("--overwrite",action="store_true")
    l=s.add_parser("list"); l.add_argument("--status",choices=["draft","sent","paid","void"]); l.add_argument("--customer"); l.add_argument("--json",action="store_true")
    sh=s.add_parser("show"); sh.add_argument("number"); sh.add_argument("--json",action="store_true")
    st=s.add_parser("status"); st.add_argument("number"); st.add_argument("value",choices=["draft","sent","paid","void"])
    ex=s.add_parser("export"); ex.add_argument("number"); ex.add_argument("--format",choices=["html","json"],default="html"); ex.add_argument("--output",required=True); ex.add_argument("--overwrite",action="store_true")
    d=s.add_parser("delete"); d.add_argument("number"); d.add_argument("--yes",action="store_true")
    return p

def parse_item(raw):
    parts=raw.split("|")
    if len(parts)!=3: raise InvoiceError("--item must be DESCRIPTION|QTY|PRICE")
    return LineItem.create(*parts)

def main(argv=None):
    a=parser().parse_args(argv)
    try:
      with Store(a.db) as db:
        if a.cmd=="new":
            inv=Invoice(a.number,a.customer,a.issue,a.due,a.currency,a.tax,a.discount,a.notes,[parse_item(x) for x in a.item]); db.save(inv,a.overwrite); print(f"Created {inv.number}: {inv.total:.2f} {inv.currency}")
        elif a.cmd=="list":
            rows=db.list(a.status,a.customer)
            if a.json: print(json.dumps([x.to_dict() for x in rows],ensure_ascii=False,indent=2))
            else:
                for x in rows: print(f"{x.number:<16} {x.status:<6} {x.issue_date}  {x.customer}  {x.total:.2f} {x.currency}")
        elif a.cmd=="show":
            x=db.get(a.number)
            if not x: raise InvoiceError("Invoice not found")
            print(json.dumps(x.to_dict(),ensure_ascii=False,indent=2) if a.json else f"{x.number} | {x.customer} | {x.status}\n{x.issue_date} → {x.due_date}\nTotal: {x.total:.2f} {x.currency}")
        elif a.cmd=="status":
            if not db.set_status(a.number,a.value): raise InvoiceError("Invoice not found")
            print(f"{a.number}: {a.value}")
        elif a.cmd=="export":
            x=db.get(a.number)
            if not x: raise InvoiceError("Invoice not found")
            print(export(x,a.output,a.format,a.overwrite))
        elif a.cmd=="delete":
            if not a.yes: raise InvoiceError("Deletion requires --yes")
            if not db.delete(a.number): raise InvoiceError("Invoice not found")
            print(f"Deleted {a.number}")
      return 0
    except (InvoiceError,ValueError,FileExistsError,OSError) as e:
      print(f"error: {e}",file=sys.stderr); return 2

if __name__=="__main__": raise SystemExit(main())
