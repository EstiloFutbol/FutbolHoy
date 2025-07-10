import json
import time
import requests
from datetime import datetime, timedelta

# ✅ API-Football v3 Key directa (no usar variables de entorno)
API_KEY = "147ad526b31203abbf6a9c42c43811c2"

HEADERS = {
    "x-apisports-key": API_KEY
}

BASE_URL = "https://v3.football.api-sports.io/fixtures"

# 🔁 Rango de fechas
HOY = datetime.utcnow().date()
INICIO = HOY - timedelta(days=7)
FIN = HOY + timedelta(days=7)

# 🧾 Resultados por fecha
resultados = {}

fecha_actual = INICIO
while fecha_actual <= FIN:
    fecha_str = fecha_actual.strftime("%Y-%m-%d")
    print(f"🔍 Consultando fixtures del {fecha_str}...")

    params = {
        "date": fecha_str
    }

    try:
        response = requests.get(BASE_URL, headers=HEADERS, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        resultados[fecha_str] = data.get("response", [])
    except Exception as e:
        print(f"⚠️ Error al obtener datos del {fecha_str}: {e}")
        resultados[fecha_str] = []

    fecha_actual += timedelta(days=1)
    time.sleep(1)  # evitar límites de rate

# 💾 Guardar datos
with open("datos.json", "w", encoding="utf-8") as f:
    json.dump(resultados, f, ensure_ascii=False, indent=2)

# 🧾 Resumen
total_partidos = sum(len(lista) for lista in resultados.values())
print(f"✅ Archivo datos.json generado correctamente con {total_partidos} partidos.")
