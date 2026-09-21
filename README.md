# Invoice Maker Lite

A small, local-first invoice manager for freelancers and developers. It creates validated invoices from the command line, stores them in SQLite, tracks lifecycle status, calculates discounts/tax with decimal arithmetic, and exports portable HTML or JSON without cloud services.

**Author:** Radwan Abdulhadi Ahmed · رضوان عبدالهادي أحمد · [@rad03i2](https://github.com/rad03i2)

## Why it exists
Many invoice tools require an account or subscription. Invoice Maker Lite is intentionally narrow: reliable local invoice records and printable exports using Python's standard library.

## Features
- Create invoices with multiple line items (`DESCRIPTION|QTY|PRICE`).
- Decimal money calculations with two-place, half-up rounding.
- Percentage tax and fixed discount calculations.
- SQLite persistence with customer/date indexes.
- Status workflow: `draft`, `sent`, `paid`, `void`.
- Search/list by status or partial customer name.
- HTML export suitable for browser printing / Save as PDF.
- JSON export for automation and interoperability.
- HTML escaping for customer-controlled text.
- Duplicate invoice protection and explicit overwrite controls.
- Atomic export replacement; no network calls, telemetry, or API keys.

## Requirements & installation
Python 3.10+.

```bash
git clone https://github.com/rad03i2/invoice-maker-lite.git
cd invoice-maker-lite
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -e .
invoice-maker --version
```

## Usage
```bash
invoice-maker new INV-2026-001 --customer "Example Studio" --issue 2026-09-21 --due 2026-10-05 --currency USD --tax 5 --discount 10 --item "Design|2|50" --item "Hosting|1|20"
invoice-maker list
invoice-maker list --status draft --customer Studio
invoice-maker show INV-2026-001 --json
invoice-maker status INV-2026-001 sent
invoice-maker export INV-2026-001 --format html --output invoice.html
invoice-maker export INV-2026-001 --format json --output invoice.json
invoice-maker status INV-2026-001 paid
invoice-maker delete INV-2026-001 --yes
```
Open the HTML export in a browser and use Print → Save as PDF when a PDF is needed.

## Configuration
By default the database is `~/.invoice-maker-lite/invoices.db`. Override it with `INVOICE_MAKER_DB` or per command with `--db PATH`. No `.env` file is required.

## Project structure
```text
src/invoice_maker/
  core.py       validation, line items, decimal calculations
  storage.py    SQLite persistence and queries
  render.py     escaped HTML and JSON exporters
  cli.py        command-line interface
tests/           functional/unit tests
examples/        safe example output
.github/workflows/ci.yml
```

## Testing
```bash
python -m pip install -e . pytest
python -m pytest -q
```
CI runs the same test suite on Python 3.10, 3.12 and 3.13 across Ubuntu, Windows and macOS.

## Preview / screenshots
The primary interface is the terminal and exported invoice. For a portfolio screenshot, create an invoice with fictional data, show `invoice-maker list`, then open the exported HTML beside it. Never publish real customer information.

## Security & privacy
All operations are local and the application performs no network requests. The SQLite database is not encrypted, so filesystem permissions and secure backups remain the user's responsibility. Exported HTML escapes user-provided customer/item text. See [SECURITY.md](SECURITY.md).

## Limitations
- HTML/JSON export only; PDF is produced through browser printing rather than a bundled PDF engine.
- No payment processing, email delivery, currency conversion, recurring billing, accounting integration, or cloud sync.
- One percentage tax rate and one fixed invoice-level discount.
- SQLite data is not encrypted and concurrent multi-user workflows are outside scope.
- Currency codes are syntax-validated as three letters; no external ISO registry is queried.

## Optional roadmap
Optional future work may include company profiles, CSV export/import, richer tax models, and an opt-in PDF dependency. These are not claimed as current features.

## Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md). Keep contributions tested and free of real customer data.

## License
MIT — see [LICENSE](LICENSE).

## Author
**Radwan Abdulhadi Ahmed**  
**رضوان عبدالهادي أحمد**  
GitHub: **[@rad03i2](https://github.com/rad03i2)**

---

# العربية — Invoice Maker Lite

أداة صغيرة ومحلية لإدارة الفواتير للمستقلين والمطورين. تنشئ فواتير موثقة من سطر الأوامر، وتحفظها في SQLite، وتتابع حالتها، وتحسب الخصم والضريبة بحساب عشري مناسب للأموال، وتصدر HTML أو JSON دون خدمات سحابية.

## لماذا هذا المشروع؟
الكثير من أدوات الفوترة تتطلب حسابًا أو اشتراكًا. يركز هذا المشروع على وظيفة محددة وموثوقة: حفظ الفواتير محليًا وإنشاء مخرجات قابلة للطباعة والأتمتة باستخدام Python ومكتبته القياسية.

## المزايا
- عدة بنود في الفاتورة مع الوصف والكمية وسعر الوحدة.
- حسابات مالية عشرية وتقريب إلى منزلتين.
- ضريبة مئوية وخصم ثابت على مستوى الفاتورة.
- تخزين SQLite محلي مع فهارس للعميل والتاريخ.
- حالات `draft` و`sent` و`paid` و`void`.
- تصفية حسب الحالة والبحث الجزئي باسم العميل.
- تصدير HTML قابل للطباعة أو الحفظ PDF من المتصفح، وتصدير JSON.
- تهريب محتوى المستخدم داخل HTML لمنع حقن الوسوم.
- حماية من تكرار رقم الفاتورة ومن استبدال ملفات التصدير دون تصريح.
- لا شبكة ولا تتبع ولا مفاتيح API.

## المتطلبات والتثبيت
يتطلب Python 3.10 أو أحدث. استنسخ المستودع، أنشئ بيئة افتراضية، ثم نفذ `python -m pip install -e .`.

## الاستخدام
أوامر قسم Usage أعلاه هي المرجع المباشر. لإنشاء فاتورة استخدم `invoice-maker new` مع `--customer` و`--issue` و`--due` وبند واحد على الأقل بصيغة `--item "الوصف|الكمية|السعر"`. استخدم `list` للعرض، و`show` للتفاصيل، و`status` لتغيير الحالة، و`export` للتصدير، و`delete --yes` للحذف الصريح.

## الإعداد
المسار الافتراضي لقاعدة البيانات هو `~/.invoice-maker-lite/invoices.db`. يمكن تغييره بمتغير البيئة `INVOICE_MAKER_DB` أو الخيار `--db PATH`. لا يحتاج المشروع إلى ملف `.env`.

## بنية المشروع
`core.py` للحساب والتحقق، و`storage.py` للتخزين، و`render.py` للتصدير، و`cli.py` لسطر الأوامر، بينما تغطي `tests/` الوظائف الأساسية و`examples/` مثالًا وهميًا آمنًا.

## الاختبارات
ثبّت pytest عبر `python -m pip install -e . pytest` ثم شغّل `python -m pytest -q`. إعداد CI يختبر عدة إصدارات Python على Linux وWindows وmacOS.

## المعاينة
لصورة عرض للمشروع استخدم بيانات وهمية، اعرض نتيجة `invoice-maker list` ثم افتح HTML المصدر بجانب الطرفية. لا تنشر بيانات عميل حقيقي.

## الخصوصية والأمان
كل العمليات محلية ولا توجد اتصالات شبكة. قاعدة SQLite غير مشفرة، لذلك تقع حماية ملفات الجهاز والنسخ الاحتياطية على المستخدم. يتم تهريب النصوص المدخلة قبل وضعها في HTML. راجع [SECURITY.md](SECURITY.md).

## القيود
لا توجد معالجة دفع أو إرسال بريد أو تحويل عملات أو فواتير متكررة أو مزامنة سحابية. PDF يعتمد على الطباعة من المتصفح. نموذج الضريبة الحالي نسبة واحدة والخصم قيمة ثابتة. قاعدة البيانات غير مشفرة، والتحقق من العملة شكلي لرمز من ثلاثة أحرف ولا يستدعي سجل ISO خارجيًا.

## تطوير اختياري
يمكن مستقبلًا إضافة ملفات تعريف للشركات وCSV ونماذج ضريبية أغنى أو محرك PDF اختياري. هذه ليست ميزات منفذة حاليًا.

## المساهمة والترخيص
راجع [CONTRIBUTING.md](CONTRIBUTING.md). المشروع مرخص تحت MIT كما في [LICENSE](LICENSE).

## المؤلف
**Radwan Abdulhadi Ahmed**  
**رضوان عبدالهادي أحمد**  
GitHub: **[@rad03i2](https://github.com/rad03i2)**
