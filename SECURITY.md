# Security / الأمان

Invoice Maker Lite is local-first and performs no network requests. Invoice data can contain sensitive customer information; the SQLite database is **not encrypted**. Protect the host account and filesystem, keep backups securely, and never use the repository for real customer records.

Do not publish suspected vulnerabilities with customer data or secrets. Report security issues privately to the maintainer through GitHub's available private reporting mechanism when enabled. Please include affected version, reproduction steps, impact, and a minimal non-sensitive example.

الأداة تعمل محليًا ولا ترسل طلبات شبكة، لكن قاعدة SQLite **غير مشفرة** وقد تحتوي بيانات حساسة. احمِ حساب الجهاز والملفات والنسخ الاحتياطية، ولا ترفع بيانات عملاء حقيقية إلى المستودع. عند الإبلاغ عن مشكلة أمنية استخدم قناة خاصة متاحة في GitHub ولا ترفق أسرارًا أو بيانات شخصية.
