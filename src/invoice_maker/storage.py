"""SQLite persistence for invoices."""
from __future__ import annotations
import json, sqlite3
from pathlib import Path
from .core import Invoice, LineItem

SCHEMA = """
CREATE TABLE IF NOT EXISTS invoices (
 number TEXT PRIMARY KEY, customer TEXT NOT NULL, issue_date TEXT NOT NULL, due_date TEXT NOT NULL,
 currency TEXT NOT NULL, tax_rate TEXT NOT NULL, discount TEXT NOT NULL, notes TEXT NOT NULL,
 status TEXT NOT NULL, items_json TEXT NOT NULL, created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
 updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP);
CREATE INDEX IF NOT EXISTS idx_invoice_customer ON invoices(customer);
CREATE INDEX IF NOT EXISTS idx_invoice_dates ON invoices(issue_date, due_date);
"""

class Store:
    def __init__(self, path: str | Path):
        self.path = Path(path).expanduser()
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(self.path)
        self.db.row_factory = sqlite3.Row
        self.db.executescript(SCHEMA)

    def close(self): self.db.close()
    def __enter__(self): return self
    def __exit__(self, *_): self.close()

    def save(self, inv: Invoice, overwrite: bool = False):
        inv.validate()
        items = json.dumps([{"description":i.description,"quantity":str(i.quantity),"unit_price":str(i.unit_price)} for i in inv.items])
        if overwrite:
            sql = """INSERT INTO invoices(number,customer,issue_date,due_date,currency,tax_rate,discount,notes,status,items_json)
            VALUES(?,?,?,?,?,?,?,?,?,?) ON CONFLICT(number) DO UPDATE SET customer=excluded.customer,issue_date=excluded.issue_date,
            due_date=excluded.due_date,currency=excluded.currency,tax_rate=excluded.tax_rate,discount=excluded.discount,notes=excluded.notes,
            status=excluded.status,items_json=excluded.items_json,updated_at=CURRENT_TIMESTAMP"""
        else:
            sql = "INSERT INTO invoices(number,customer,issue_date,due_date,currency,tax_rate,discount,notes,status,items_json) VALUES(?,?,?,?,?,?,?,?,?,?)"
        try:
            self.db.execute(sql,(inv.number,inv.customer,inv.issue_date,inv.due_date,inv.currency,str(inv.tax_rate),str(inv.discount),inv.notes,inv.status,items)); self.db.commit()
        except sqlite3.IntegrityError as exc:
            raise ValueError(f"Invoice {inv.number!r} already exists; use --overwrite") from exc

    def get(self, number: str) -> Invoice | None:
        row=self.db.execute("SELECT * FROM invoices WHERE number=?",(number,)).fetchone()
        return self._decode(row) if row else None

    def list(self, status: str | None=None, customer: str | None=None) -> list[Invoice]:
        sql,args="SELECT * FROM invoices WHERE 1=1",[]
        if status: sql+=" AND status=?"; args.append(status)
        if customer: sql+=" AND customer LIKE ?"; args.append(f"%{customer}%")
        sql+=" ORDER BY issue_date DESC, number DESC"
        return [self._decode(r) for r in self.db.execute(sql,args)]

    def set_status(self, number: str, status: str) -> bool:
        if status not in {"draft","sent","paid","void"}: raise ValueError("Invalid status")
        cur=self.db.execute("UPDATE invoices SET status=?,updated_at=CURRENT_TIMESTAMP WHERE number=?",(status,number)); self.db.commit(); return cur.rowcount>0

    def delete(self, number: str) -> bool:
        cur=self.db.execute("DELETE FROM invoices WHERE number=?",(number,)); self.db.commit(); return cur.rowcount>0

    @staticmethod
    def _decode(r) -> Invoice:
        return Invoice(r["number"],r["customer"],r["issue_date"],r["due_date"],r["currency"],r["tax_rate"],r["discount"],r["notes"],
                       [LineItem.create(x["description"],x["quantity"],x["unit_price"]) for x in json.loads(r["items_json"])],r["status"])
