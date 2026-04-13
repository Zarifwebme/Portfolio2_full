from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse
from .models import Project, ContactMessage
import requests


def normalize_phone(phone):
    raw_phone = (phone or "").strip()
    if not raw_phone:
        return ""

    if not raw_phone.isdigit():
        return None

    if len(raw_phone) not in (9, 12):
        return None

    return raw_phone


def contact_response(request, *, success, message, status=200, telegram_sent=None):
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        payload = {"success": success, "message": message}
        if telegram_sent is not None:
            payload["telegram_sent"] = telegram_sent
        return JsonResponse(payload, status=status)

    if success:
        messages.success(request, message)
    else:
        messages.error(request, message)

    return redirect("contact")


def home(request):
    return render(request, "home.html")

def about(request):
    return render(request, "about.html")

def projects(request):
    qs = Project.objects.filter(is_active=True)
    complete = qs.filter(category="complete")
    small = qs.filter(category="small")
    return render(request, "projects.html", {"complete": complete, "small": small})


def contact(request):
    if request.method == "POST":
        name = (request.POST.get("name") or "").strip()
        phone = normalize_phone(request.POST.get("phone"))
        email = (request.POST.get("email") or "").strip()
        message_text = (request.POST.get("message") or "").strip()

        if not name or not message_text:
            return contact_response(request, success=False, message="Name va Message majburiy.", status=400)

        if phone is None:
            return contact_response(
                request,
                success=False,
                message="Telefon faqat 9 yoki 12 xonali raqam bo'lishi kerak.",
                status=400,
            )

        msg = ContactMessage.objects.create(
            name=name, phone=phone, email=email, message=message_text
        )

        bot = getattr(settings, "TELEGRAM_BOT_TOKEN", "")
        chat_id = getattr(settings, "TELEGRAM_CHAT_ID", "")

        if bot and chat_id:
            text = (
                "📩 Portfolio contact\n\n"
                f"👤 Name: {name}\n"
                f"📞 Phone: {phone}\n"
                f"✉️ Email: {email}\n\n"
                f"💬 Message:\n{message_text}\n\n"
                f"🆔 ID: {msg.id}"
            )
            try:
                r = requests.post(
                    f"https://api.telegram.org/bot{bot}/sendMessage",
                    json={"chat_id": chat_id, "text": text},
                    timeout=10,
                )
                if r.status_code == 200:
                    return contact_response(request, success=True, message="Xabaringiz yuborildi ✅", telegram_sent=True)
                else:
                    return contact_response(
                        request,
                        success=True,
                        message="Xabar saqlandi, lekin Telegramga yuborilmadi.",
                        telegram_sent=False,
                    )
            except Exception:
                return contact_response(
                    request,
                    success=True,
                    message="Xabar saqlandi, lekin Telegramga yuborilmadi.",
                    telegram_sent=False,
                )
        else:
            return contact_response(
                request,
                success=True,
                message="Xabaringiz yuborildi ✅ (Telegram sozlanmagan)",
                telegram_sent=False,
            )

        return contact_response(request, success=True, message="Xabaringiz yuborildi ✅", telegram_sent=True)

    return render(request, "contact.html")
