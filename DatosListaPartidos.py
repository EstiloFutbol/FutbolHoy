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

with open('datos.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False)
