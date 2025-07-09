import json
import os
import time
from datetime import datetime, timedelta, timezone
from typing import Dict, List

import requests


API_KEY = os.getenv("API_KEY", "941084e84950203ffc04aaa2b7fcf1f3")
HEADERS = {
    "x-rapidapi-host": "api-football-v1.p.rapidapi.com",
    "x-rapidapi-key": API_KEY,
}
BASE_URL = "https://api-football-v1.p.rapidapi.com/v3/fixtures"

TODAY = datetime.now(timezone.utc)
START = TODAY - timedelta(days=7)
END = TODAY + timedelta(days=7)
MAX_CALLS = 100


def fetch_matches(date_str: str) -> List[Dict]:
    """Fetch matches for a given date from the API."""
    url = f"{BASE_URL}?date={date_str}&timezone=Europe/Madrid"
    resp = requests.get(url, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    return data.get("response", [])


result: Dict[str, List[Dict]] = {}
current = START
calls = 0
while current <= END and calls < MAX_CALLS:
    date_str = current.strftime("%Y-%m-%d")
    try:
        result[date_str] = fetch_matches(date_str)
        calls += 1
    except Exception as exc:
        print(f"Failed to fetch {date_str}: {exc}")
        result[date_str] = []
    time.sleep(0.5)
    current += timedelta(days=1)

with open("datos.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)
