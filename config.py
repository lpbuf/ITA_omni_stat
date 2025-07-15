from dotenv import load_dotenv
import os

load_dotenv()

OMNIDESK_USER = os.getenv("OMNIDESK_USER")
OMNIDESK_TOKEN = os.getenv("OMNIDESK_TOKEN")
BASE_URL = os.getenv("BASE_URL", "https://ita.omnidesk.ru")

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
TIMEZONE = os.getenv("TIMEZONE", "Europe/Moscow")

# Проверка обязательных переменных
required = [
    ("OMNIDESK_USER", OMNIDESK_USER),
    ("OMNIDESK_TOKEN", OMNIDESK_TOKEN),
    ("TELEGRAM_TOKEN", TELEGRAM_TOKEN),
    ("TELEGRAM_CHAT_ID", TELEGRAM_CHAT_ID),
]
missing = [name for name, val in required if not val]
if missing:
    raise RuntimeError(f"В .env не заданы обязательные переменные: {', '.join(missing)}")