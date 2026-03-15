# My Portfolio Django

Shaxsiy portfolio sayti Django asosida yozilgan loyiha.

## Asosiy imkoniyatlar

- Home, About, Projects, Contact sahifalari
- Admin panel orqali projectlarni boshqarish
- Contact form ma'lumotlarini bazaga saqlash
- Contact yuborilganda Telegram bot orqali xabar jo'natish (agar sozlangan bo'lsa)
- Ko'p tillilik (i18n): English, Uzbek, Russian
- Static va media fayllarni boshqarish
- CV faylini tilga qarab yuklab olish

## Texnologiyalar

- Python 3.11+
- Django 5+
- SQLite3
- Pillow (rasm upload uchun)
- requests (Telegram API uchun)
- python-dotenv (.env sozlamalari uchun)
- Bootstrap 5 (frontend)

## Loyiha tuzilmasi

```
myportfolidjnago/
├─ manage.py
├─ requirements.txt
├─ db.sqlite3
├─ myportfolio/              # app: models, views, urls, admin
├─ rootloyiha/               # project settings va root urls
├─ templates/                # HTML shablonlar
├─ static/                   # CSS, JS, CV, logo va boshqa staticlar
├─ media/                    # upload qilingan rasmlar
└─ locale/                   # tarjima fayllari (uz, ru)
```

## O'rnatish

1. Reponi clone qiling:

```bash
git clone https://github.com/Zarifwebme/Portfolio2_full.git
cd Portfolio2_full
```

2. Virtual environment yarating va aktiv qiling:

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Bog'liqliklarni o'rnating:

```bash
pip install -r requirements.txt
```

4. `.env` fayl yarating (loyiha rootida):

```env
SECRET_KEY=django-insecure-change-me
DEBUG=True
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=
```

Izoh:

- `TELEGRAM_BOT_TOKEN` va `TELEGRAM_CHAT_ID` bo'sh bo'lsa ham loyiha ishlaydi.
- Bu holatda contact form xabari bazaga saqlanadi, Telegramga yuborilmaydi.

5. Migratsiyalarni ishga tushiring:

```bash
python manage.py migrate
```

6. Admin user yarating (ixtiyoriy, lekin tavsiya etiladi):

```bash
python manage.py createsuperuser
```

7. Serverni ishga tushiring:

```bash
python manage.py runserver
```

8. Brauzerda oching:

- http://127.0.0.1:8000/
- Admin panel: http://127.0.0.1:8000/admin/

## Muhim sozlamalar

`rootloyiha/settings.py` ichida:

- `ALLOWED_HOSTS` lokal va production hostlar bilan berilgan
- `LANGUAGES` uchta tilni qo'llab-quvvatlaydi: `en`, `uz`, `ru`
- `LOCALE_PATHS` tarjima fayllari joylashuvini ko'rsatadi
- `STATICFILES_DIRS`, `STATIC_ROOT`, `MEDIA_ROOT` sozlangan

## Tarjima (i18n) buyruqlari

Tarjimalarni yangilash uchun odatiy Django buyruqlari:

```bash
python manage.py makemessages -l uz -l ru
python manage.py compilemessages
```

## Contact ishlash mantig'i

- Foydalanuvchi contact form yuboradi
- Ma'lumot `ContactMessage` modeliga saqlanadi
- Agar Telegram token/chat id mavjud bo'lsa, Telegram botga xabar yuboriladi
- Yuborish xatosida ham ma'lumot bazada saqlanib qoladi

## Admin orqali boshqarish

Admin paneldan:

- Project qo'shish/o'zgartirish/o'chirish
- Project tartibi (`order`) va faolligini (`is_active`) boshqarish
- Contact xabarlarini ko'rish va `is_read` holatini belgilash

## Production bo'yicha tavsiyalar

- `DEBUG=False` qiling
- Kuchli `SECRET_KEY` ishlating
- `ALLOWED_HOSTS` ni aniq domenlar bilan to'ldiring
- Static fayllar uchun:

```bash
python manage.py collectstatic
```

- Reverse proxy va HTTPS sozlang (masalan Nginx + Gunicorn)

## Muallif

Zarifjon Baxtiyorov

- GitHub: https://github.com/Zarifwebme
- LinkedIn: https://www.linkedin.com/in/zarifjon-baxtiyorov-b789a3267/
