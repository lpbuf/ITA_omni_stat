# 🤖 Omnidesk Telegram Bot

Бот собирает статистику с сайта Omnidesk и отправляет отчёты в Telegram.

---

## ⚙️ Загрузка настроек

При запуске бот читает файл `.env` и подтягивает оттуда:

OMNIDESK_USER=
OMNIDESK_PASSWORD=
TELEGRAM_TOKEN=
TELEGRAM_CHAT_ID=
TIMEZONE=Europe/Moscow
BASE_URL=
LOG_DIR=logs
LOG_LEVEL=INFo

Если чего-то не хватает, бот завершится с ошибкой — запуск без ключей невозможен.

---

## 🚀 Аргументы запуска

Можно передать флаг `--manual` и два параметра `--from`, `--to` в формате `YYYY-MM-DD HH:MM`:

```bash
python main.py --manual --from "2025-06-22 21:00" --to "2025-06-23 09:00"
