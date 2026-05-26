import requests

from config import BOT_TOKEN


def generate_response(user_message: str, role="parent"):

    text = user_message.strip()

    if "سلام" in text:

        if role == "admin":
            return "سلام مدیر مدرسه 👨‍💼"

        elif role == "student":
            return "سلام دانش‌آموز عزیز 🌟"

        else:
            return "سلام 👋\nبه ربات مدرسه خوش آمدید"

    elif "شهریه" in text:

        if role == "parent":
            return "برای امور مالی با دفتر مدرسه تماس بگیرید."

        else:
            return "شما دسترسی مالی ندارید."

    elif "تکلیف" in text:

        if role == "student":
            return "تکلیف امروز: حل صفحه ۱۲ ریاضی ✏️"

        else:
            return "این بخش مخصوص دانش‌آموزان است."

    else:
        return "پیام شما دریافت شد ✅"


def send_message(chat_id, text):

    url = f"https://tapi.bale.ai/bot{BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": chat_id,
        "text": text
    }

    try:

        response = requests.post(
            url,
            json=payload,
            timeout=10
        )

        return response.json()

    except Exception as e:

        print("SEND MESSAGE ERROR:")
        print(e)

        return None