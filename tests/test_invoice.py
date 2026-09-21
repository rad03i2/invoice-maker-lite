from decimal import Decimal
from invoice_maker.core import Invoice, LineItem, InvoiceError
from invoice_maker.storage import Store
from invoice_maker.render import render_html, export

def sample(number="INV-001"):
    return Invoice(number,"Acme & Co","2026-09-01","2026-09-30","USD","10","5","Thanks",[LineItem.create("Design <work>",2,"25.125")])

def test_totals_rounding():
    x=sample(); x.validate()
    assert x.subtotal==Decimal("50.26")
    assert x.taxable==Decimal("45.26")
    assert x.tax==Decimal("4.53")
    assert x.total==Decimal("49.79")

def test_validation():
    x=sample(); x.due_date="2026-08-01"
    try: x.validate(); assert False
    except InvoiceError: pass

def test_store_roundtrip_and_status(tmp_path):
    with Store(tmp_path/"db.sqlite") as db:
        db.save(sample()); got=db.get("INV-001")
        assert got and got.customer=="Acme & Co" and got.total==Decimal("49.79")
        assert db.set_status("INV-001","paid")
        assert db.get("INV-001").status=="paid"
        assert len(db.list(customer="Acme"))==1

def test_duplicate_protected(tmp_path):
    with Store(tmp_path/"db.sqlite") as db:
        db.save(sample())
        try: db.save(sample()); assert False
        except ValueError: pass

def test_html_escapes_customer_content():
    page=render_html(sample())
    assert "Acme &amp; Co" in page and "Design &lt;work&gt;" in page

def test_export_overwrite_protection(tmp_path):
    out=tmp_path/"invoice.json"; export(sample(),out,"json")
    try: export(sample(),out,"json"); assert False
    except FileExistsError: pass
