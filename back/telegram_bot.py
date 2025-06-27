import os
import requests
from flask import Flask, request
from dotenv import load_dotenv

load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000/ask")

app = Flask(__name__)

TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

@app.route(f"/webhook/{TELEGRAM_TOKEN}", methods=["POST"])
def telegram_webhook():
    data = request.get_json()
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")
        # Puedes usar el id de chat de Telegram como conversation_id
        payload = {"question": text, "conversation_id": str(chat_id)}
        try:
            r = requests.post(BACKEND_URL, json=payload, timeout=10)
            answer = r.json().get("answer", "Lo siento, hubo un error.")
        except Exception:
            answer = "Lo siento, hubo un error al conectar con el backend."
        send_telegram_message(chat_id, answer)
    return "ok"

def send_telegram_message(chat_id, text):
    url = f"{TELEGRAM_API_URL}/sendMessage"
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "HTML"}
    requests.post(url, json=payload)

if __name__ == "__main__":
    app.run(port=9000, debug=True)
