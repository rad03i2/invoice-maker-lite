<div dir="rtl" align="right">

# Invoice Maker Lite — الدليل العربي

[العودة إلى الصفحة الرئيسية](README.md)

## نظرة عامة

**Invoice Maker Lite** أداة سطر أوامر محلية ببايثون لإنشاء الفواتير وحفظها والبحث فيها ومتابعة حالتها وتصديرها. تستخدم SQLite للسجلات وDecimal للحسابات المالية.

المشروع متعمد أن يبقى بسيطًا ومحددًا: إدارة سجلات الفواتير محليًا من دون حساب سحابي أو معالجة دفع أو خدمات تشغيل خارجية.

## التثبيت

</div>

~~~bash
git clone https://github.com/rad03i2/invoice-maker-lite.git
cd invoice-maker-lite
python -m venv .venv
python -m pip install -e .
invoice-maker --version
~~~

<div dir="rtl" align="right">

## إنشاء فاتورة

</div>

~~~bash
invoice-maker new INV-2026-001   --customer "Example Studio"   --issue 2026-09-21   --due 2026-10-05   --currency USD   --tax 5   --discount 10   --item "Design|2|50"   --item "Hosting|1|20"
~~~

<div dir="rtl" align="right">

كل بند يستخدم الصيغة:

</div>

~~~text
DESCRIPTION|QTY|PRICE
~~~

<div dir="rtl" align="right">

ويجب وجود بند واحد على الأقل.

## التحقق والحسابات

التنفيذ الحالي يتحقق من:

- وجود رقم للفاتورة واسم للعميل.
- أن التاريخ بصيغة <code>YYYY-MM-DD</code>.
- أن تاريخ الاستحقاق لا يسبق تاريخ الإصدار.
- أن رمز العملة يتكون من ثلاثة أحرف.
- أن نسبة الضريبة بين 0 و100.
- أن القيم المالية ليست سالبة.
- أن كمية كل بند أكبر من صفر.
- أن الخصم الثابت لا يتجاوز المجموع الفرعي.

تُقرب الأموال إلى منزلتين عشريتين باستخدام Decimal و<code>ROUND_HALF_UP</code>.

## عرض السجلات والبحث

</div>

~~~bash
invoice-maker list
invoice-maker list --status draft
invoice-maker list --customer Studio
invoice-maker list --status sent --customer Studio
invoice-maker list --json
~~~

<div dir="rtl" align="right">

البحث باسم العميل جزئي باستخدام SQLite.

## حالات الفاتورة

الحالات المتاحة:

- <code>draft</code>
- <code>sent</code>
- <code>paid</code>
- <code>void</code>

</div>

~~~bash
invoice-maker status INV-2026-001 paid
~~~

<div dir="rtl" align="right">

هذه حالة محلية يحددها المستخدم وليست تحققًا من جهة دفع خارجية.

## التصدير

### HTML

</div>

~~~bash
invoice-maker export INV-2026-001 --format html --output invoice.html
~~~

<div dir="rtl" align="right">

يمكن فتح الملف في المتصفح واستخدام **طباعة → حفظ كـ PDF**.

### JSON

</div>

~~~bash
invoice-maker export INV-2026-001 --format json --output invoice.json
~~~

<div dir="rtl" align="right">

لا يتم استبدال ملف تصدير موجود إلا عند استخدام <code>--overwrite</code> صراحة.

## الحذف

</div>

~~~bash
invoice-maker delete INV-2026-001 --yes
~~~

<div dir="rtl" align="right">

يتطلب الحذف تأكيدًا صريحًا عبر <code>--yes</code>.

## قاعدة البيانات

المسار الافتراضي:

</div>

~~~text
~/.invoice-maker-lite/invoices.db
~~~

<div dir="rtl" align="right">

يمكن تغييره باستخدام <code>INVOICE_MAKER_DB</code> أو الخيار العام <code>--db PATH</code>.

قاعدة SQLite غير مشفرة بواسطة البرنامج.

## أمان HTML

يتم تهريب النصوص المدخلة من العميل والبنود والملاحظات قبل وضعها في HTML.

## الاختبارات

</div>

~~~bash
python -m pip install -e . pytest
python -m pytest -q
invoice-maker --version
~~~

<div dir="rtl" align="right">

يشغّل CI الاختبارات على Ubuntu وWindows وmacOS مع Python 3.10 و3.12 و3.13.

## الحدود الحالية

لا يوفر المشروع حاليًا:

- محرك PDF مدمج.
- معالجة أو تحقق دفع.
- إرسال بريد تلقائي.
- مزامنة سحابية.
- تحويل العملات.
- أكثر من نسبة ضريبة واحدة في الفاتورة.
- أكثر من خصم ثابت واحد على مستوى الفاتورة.
- تشفيرًا لقاعدة SQLite.
- تنسيق عمل متعدد المستخدمين.

## البنية التقنية

راجع [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

## المطور

**رضوان عبدالهادي**  
**Radwan Abd alhady Ahmed**  
GitHub: [@rad03i2](https://github.com/rad03i2)

## الترخيص

MIT — راجع [LICENSE](LICENSE).

</div>
