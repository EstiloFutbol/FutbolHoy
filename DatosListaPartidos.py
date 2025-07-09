import os
import json
import time
import requests
from datetime import datetime, timedelta, timezone
from typing import Dict, List

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
import os
import json
from datetime import datetime, timedelta
import requests

API_KEY = os.getenv('API_KEY')
if not API_KEY:
    raise RuntimeError('API_KEY environment variable not set')

HEADERS = {'x-apisports-key': API_KEY}
TODAY = datetime.utcnow()
START = TODAY - timedelta(days=7)
END = TODAY + timedelta(days=7)

result = {}

current = START
while current <= END:
    date_str = current.strftime('%Y-%m-%d')
    url = f'https://v3.football.api-sports.io/fixtures?date={date_str}'
    try:
        response = requests.get(url, headers=HEADERS, timeout=30)
        response.raise_for_status()
        data = response.json()
        result[date_str] = data.get('response', [])
    except Exception as exc:
        print(f'Failed to fetch {date_str}: {exc}')
        result[date_str] = []
    current += timedelta(days=1)

# Guardar los datos en un archivo JSON
with open('datos.json', 'w', encoding='utf-8') as f:
    json.dump(resultados, f, ensure_ascii=False, indent=2)

print("✅ Archivo datos.json generado correctamente.")
