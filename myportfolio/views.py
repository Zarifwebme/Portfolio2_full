from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from .models import Project, ContactMessage
import requests
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
        phone = (request.POST.get("phone") or "").strip()
        email = (request.POST.get("email") or "").strip()
        message_text = (request.POST.get("message") or "").strip()

        if not name or not message_text:
            messages.error(request, "Name va Message majburiy.")
            return redirect("contact")

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
                    messages.success(request, "Xabaringiz yuborildi ✅")
                else:
                    messages.warning(request, "Xabar saqlandi, lekin Telegramga yuborilmadi.")
            except Exception:
                messages.warning(request, "Xabar saqlandi, lekin Telegramga yuborilmadi.")
        else:
            messages.success(request, "Xabaringiz yuborildi ✅ (Telegram sozlanmagan)")

        return redirect("contact")

    return render(request, "contact.html")
