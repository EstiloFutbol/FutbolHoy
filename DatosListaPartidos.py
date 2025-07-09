import os
import json
import time
import requests
from datetime import datetime, timedelta, timezone
from typing import Dict, List

# ⚙️ Claves RapidAPI (modificables por entorno o hardcodeadas aquí)
RAPIDAPI_HOST = "api-football-v1.p.rapidapi.com"
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY", "c9700f3b0emsh770064a38cd34fdp161ed7jsncea2230ea135")

HEADERS = {
    "x-rapidapi-host": RAPIDAPI_HOST,
    "x-rapidapi-key": RAPIDAPI_KEY
}

BASE_URL = "https://api-football-v1.p.rapidapi.com/v2/fixtures/date"

# 🔁 Rango de fechas
HOY = datetime.utcnow()
INICIO = HOY - timedelta(days=7)
FIN = HOY + timedelta(days=7)

# 🧾 Resultados por fecha
resultados = {}

fecha_actual = INICIO
while fecha_actual <= FIN:
    fecha_str = fecha_actual.strftime("%Y-%m-%d")
    print(f"🔍 Consultando fixtures del {fecha_str}...")

    url = f"{BASE_URL}/{fecha_str}"

    try:
        response = requests.get(url, headers=HEADERS, timeout=30)
        response.raise_for_status()
        data = response.json()
        resultados[fecha_str] = data.get("api", {}).get("fixtures", [])
    except Exception as e:
        print(f"⚠️ Error al obtener datos del {fecha_str}: {e}")
        resultados[fecha_str] = []

    fecha_actual += timedelta(days=1)
    time.sleep(1)  # evitar límite de peticiones

# 💾 Guardar datos
with open("datos.json", "w", encoding="utf-8") as f:
    json.dump(resultados, f, ensure_ascii=False, indent=2)

print("✅ Archivo datos.json generado correctamente.")
