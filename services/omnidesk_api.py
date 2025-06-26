from datetime import datetime
from typing import List, Dict, Any
import requests
from urllib.parse import quote

from config import OMNIDESK_USER, OMNIDESK_PASSWORD, BASE_URL


def fetch_stats(from_time: datetime, to_time: datetime) -> List[Dict[str, Any]]:
    """
    Запрашивает статистику лидерборда Omnidesk и возвращает плоский список
    уникальных записей по каждому сотруднику.
    Дубликаты (по staff_id) отбрасываются.
    """
    fmt = "%Y-%m-%d %H:%M"
    from_str = quote(from_time.strftime(fmt), safe='')
    to_str = quote(to_time.strftime(fmt), safe='')

    url = (
        f"{BASE_URL}/api/stats_leaderboard.json"
        f"?from_time={from_str}&to_time={to_str}"
    )

    resp = requests.get(
        url,
        auth=(OMNIDESK_USER, OMNIDESK_PASSWORD),
        headers={"Content-Type": "application/json"}
    )
    resp.raise_for_status()
    raw = resp.json()

    stats: List[Dict[str, Any]] = []
    seen_ids = set()

    # «выпрямляем» словарь и убираем дубликаты по staff_id
    for entry in raw.values():
        staff = entry.get("staff")
        if not isinstance(staff, dict):
            continue

        staff_id = staff.get("staff_id")
        if staff_id in seen_ids:
            continue
        seen_ids.add(staff_id)
        stats.append(staff)

    return stats