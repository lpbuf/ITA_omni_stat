from datetime import datetime
from typing import List, Dict, Any
import requests
from urllib.parse import quote

from config import OMNIDESK_USER, OMNIDESK_PASSWORD, BASE_URL


def fetch_stats(from_time: datetime, to_time: datetime) -> List[Dict[str, Any]]:
    """
    Запрашивает статистику лидерборда Omnidesk и возвращает плоский список
    dict’ов вида {staff_id, staff_name, new_cases_in_total, first_response_time, …}
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

    # «выпрямляем» полученный словарь { "0": {"staff": {...}}, … } → [ {...}, … ]
    stats: List[Dict[str, Any]] = []
    for entry in raw.values():
        staff = entry.get("staff")
        if isinstance(staff, dict):
            stats.append(staff)

    return stats