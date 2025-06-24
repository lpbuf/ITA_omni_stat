from datetime import datetime, date, time, timedelta
import argparse
import pytz
from apscheduler.schedulers.blocking import BlockingScheduler

from config import TIMEZONE
from services.omnidesk_api import fetch_stats
from services.telegram_bot import send_message
from utils.logger import get_logger

logger = get_logger(__name__)


def format_message(
    data: list[dict],
    from_time: datetime,
    to_time: datetime
) -> str:
    """Строит итоговое сообщение Markdown-форматом с жирным заголовком, списком и отступами."""
    header = f"*📊 Статистика за {from_time.strftime('%d.%m %H:%M')} – {to_time.strftime('%d.%m %H:%M')}:*"

    # Собираем полезные записи: >5 новых и не «без ответственного»
    entries = []
    for record in data:
        # пытаемся взять int из new_cases_in_total
        try:
            new_cases = int(record.get("new_cases_in_total", 0))
        except (ValueError, TypeError):
            continue

        name = record.get("staff_name", "").strip()
        if new_cases <= 5 or name.lower() == "без ответственного":
            continue

        # форматируем время первого ответа
        raw = record.get("first_response_time")
        try:
            secs = int(raw)
            m, s = divmod(secs, 60)
            frt = f"{m} м {s} с"
        except (ValueError, TypeError):
            frt = "-"

        entries.append({
            "name": name,
            "new": new_cases,
            "frt": frt,
        })

    # Если ни одной записи — сразу возвращаем «нет данных»
    if not entries:
        return "\n".join([header, "", "Нет сотрудников с более чем 5 обращениями ❌"])

    # сортировка по новым обращениям по убыванию
    entries.sort(key=lambda x: x["new"], reverse=True)

    # строим строки
    lines = [header, ""]
    for idx, e in enumerate(entries, start=1):
        lines += [
            f"{idx}. *{e['name']}*",
            f"    📧 {e['new']} новых",
            f"    ⏱ Первый ответ: {e['frt']}",
            ""  # пустая строка между записями
        ]
    # удаляем крайний пустой
    if lines[-1] == "":
        lines.pop()

    return "\n".join(lines)


def format_and_send(start: datetime, end: datetime):
    logger.info(f"Run report: {start} → {end}")
    stats = fetch_stats(start, end)
    text = format_message(stats, start, end)
    # убедимся, что text — строка
    if not isinstance(text, str):
        text = str(text)
    send_message(text, parse_mode="Markdown")


def schedule_jobs():
    tz = pytz.timezone(TIMEZONE)
    sched = BlockingScheduler(timezone=tz)

    # утро (10:01) — вчера 21:00 до сегодня 08:00
    sched.add_job(
        lambda: format_and_send(
            tz.localize(datetime.combine(date.today(), time(21))) - timedelta(days=1),
            tz.localize(datetime.combine(date.today(), time(8)))
        ),
        'cron', hour=10, minute=1, id='morning'
    )
    # вечер (23:01) — сегодня 09:00 до сегодня 21:00
    sched.add_job(
        lambda: format_and_send(
            tz.localize(datetime.combine(date.today(), time(9))),
            tz.localize(datetime.combine(date.today(), time(21)))
        ),
        'cron', hour=23, minute=1, id='evening'
    )

    logger.info("Scheduler started")
    sched.start()


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--manual", action="store_true", help="единовременный прогон")
    p.add_argument("--from", dest="from_ts", help="начало «YYYY-MM-DD HH:MM»")
    p.add_argument("--to",   dest="to_ts",   help="конец «YYYY-MM-DD HH:MM»")
    return p.parse_args()


if __name__ == "__main__":
    args = parse_args()
    tz = pytz.timezone(TIMEZONE)

    if args.manual:
        start = tz.localize(datetime.strptime(args.from_ts, "%Y-%m-%d %H:%M"))
        end   = tz.localize(datetime.strptime(args.to_ts,   "%Y-%m-%d %H:%M"))
        format_and_send(start, end)
    else:
        schedule_jobs()