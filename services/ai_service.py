import requests
import os

import google.generativeai as genai


BOT_TOKEN = os.getenv("BOT_TOKEN")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(
    api_key=GEMINI_API_KEY
)

model = genai.GenerativeModel("gemini-1.5-flash")


def send_message(chat_id, text):

    url = f"https://tapi.bale.ai/bot{BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": chat_id,
        "text": text
    }

    try:

        response = requests.post(
            url,
            json=payload
        )

        print(response.text)

    except Exception as e:

        print("SEND MESSAGE ERROR:")
        print(e)


def generate_response(user_text, role="parent"):

    try:

        system_prompt = """
        تو یک دستیار هوشمند مدرسه هستی.
        به فارسی پاسخ بده.
        مودب و حرفه‌ای باش.
        """

        if role == "admin":

            system_prompt += """
            کاربر مدیر مدرسه است.
            """

        elif role == "teacher":

            system_prompt += """
            کاربر معلم است.
            """

        else:

            system_prompt += """
            کاربر ولی یا دانش‌آموز است.
            """

        final_prompt = f"""
        {system_prompt}

        پیام کاربر:
        {user_text}
        """

        response = model.generate_content(final_prompt)

        return response.text

    except Exception as e:

        print("========== GEMINI ERROR ==========")
        print(str(e))
        print("==================================")

    return f"ERROR: {str(e)}"