import openai
from flask import Flask, request
import telegram
import os

# API Keys (Render-এর environment variables থেকে)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# টেলিগ্রাম বট সেটআপ
bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)

# Flask অ্যাপ তৈরি করুন
app = Flask(__name__)

# OpenAI-এর মাধ্যমে উত্তর পাওয়ার ফাংশন
def chat_with_gpt(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        api_key=OPENAI_API_KEY
    )
    return response["choices"][0]["message"]["content"]

# Webhook Route (টেলিগ্রাম মেসেজ প্রসেস করবে)
@app.route(f"/{TELEGRAM_BOT_TOKEN}", methods=["POST"])
def telegram_webhook():
    update = telegram.Update.de_json(request.get_json(), bot)
    if update.message:
        chat_response = chat_with_gpt(update.message.text)
        update.message.reply_text(chat_response)
    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)