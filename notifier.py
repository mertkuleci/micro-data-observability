import requests
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

def send_telegram_alert(message):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("Telegram credentials missing in .env file!")
        return False

    if len(message) > 4000:
        message = message[:3950] + "\n\n... [Truncated due to character limit]"

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }

    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("Telegram notification sent successfully.")
            return True
        else:
            print(f"Telegram error: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"Error sending notification: {e}")
        return False