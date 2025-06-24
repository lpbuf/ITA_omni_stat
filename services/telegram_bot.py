import requests
from typing import Any, Dict

from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID


def send_message(text: str, chat_id: str = TELEGRAM_CHAT_ID, **kwargs) -> Dict[str, Any]:
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text, **kwargs}
    response = requests.post(url, json=payload, timeout=10)
    response.raise_for_status()
    return response.json()