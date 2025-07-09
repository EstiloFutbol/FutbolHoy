import json
import random
import time
from datetime import datetime, timedelta, timezone
from typing import List, Dict

import requests
from bs4 import BeautifulSoup


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0 Safari/537.36"
    )
}

TODAY = datetime.now(timezone.utc)
START = TODAY - timedelta(days=7)
END = TODAY + timedelta(days=7)


def fetch_matches(date_str: str) -> List[Dict[str, str]]:
    """Fetch matches for a given date from fbref."""
    url = f"https://fbref.com/en/matches/{date_str}"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=30)
        resp.raise_for_status()
    except Exception as exc:
        print(f"Failed to fetch {url}: {exc}")
        return []

    soup = BeautifulSoup(resp.text, "html.parser")
    results = []
    competition = None

    for element in soup.select("h2, table.stats_table"):
        if element.name == "h2":
            competition = element.get_text(strip=True)
        elif element.name == "table":
            for row in element.select("tbody tr"):
                if "spacer" in row.get("class", []):
                    continue
                home = row.find("td", {"data-stat": "home"})
                away = row.find("td", {"data-stat": "away"})
                time_cell = row.find("td", {"data-stat": "time"})
                score_cell = row.find("td", {"data-stat": "score"})
                if not home or not away:
                    continue
                results.append({
                    "competition": competition or "",
                    "time": time_cell.get_text(strip=True) if time_cell else "",
                    "home_team": home.get_text(strip=True),
                    "away_team": away.get_text(strip=True),
                    "score": score_cell.get_text(strip=True) if score_cell else "",
                })
    return results


result: Dict[str, List[Dict[str, str]]] = {}
current = START
while current <= END:
    date_str = current.strftime("%Y-%m-%d")
    result[date_str] = fetch_matches(date_str)
    # Sleep a bit to avoid hitting the server too aggressively
    time.sleep(random.uniform(1, 3))
    current += timedelta(days=1)

with open("datos.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)
