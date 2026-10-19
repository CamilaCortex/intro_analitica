"""
cliente.py: consume la API desde Python (como lo haría otra aplicación).

Primero levanta la API en otra terminal::

    uv run uvicorn api.main:app --reload --app-dir 08-API-FastAPI

Luego::

    uv run python 08-API-FastAPI/scripts/cliente.py
    uv run python 08-API-FastAPI/scripts/cliente.py --url http://127.0.0.1:8000 --archivo 08-API-FastAPI/ejemplos/casas.json

Con curl (desde la terminal) sería::

    curl -X POST http://127.0.0.1:8000/predict \
         -H "Content-Type: application/json" \
         -d @08-API-FastAPI/ejemplos/casa.json
"""

import argparse
import json
import sys
from pathlib import Path

import requests

CARPETA_EJEMPLOS = Path(__file__).resolve().parents[1] / "ejemplos"


def main() -> None:
    parser = argparse.ArgumentParser(description="Cliente de la API de avalúos")
    parser.add_argument("--url", default="http://127.0.0.1:8000")
    parser.add_argument("--archivo", type=Path, default=CARPETA_EJEMPLOS / "casa.json",
                        help="JSON con una casa (casa.json) o con {'casas': [...]} (casas.json)")
    args = parser.parse_args()

    # 1. ¿Está viva la API?
    try:
        salud = requests.get(f"{args.url}/health", timeout=5).json()
    except requests.ConnectionError:
        sys.exit(f"[ERROR] No hay API en {args.url}. Levántala con:\n   uv run uvicorn api.main:app --app-dir 08-API-FastAPI")
    print("/health →", salud)

    # 2. Predecir
    cuerpo = json.loads(args.archivo.read_text())
    endpoint = "/predict/batch" if "casas" in cuerpo else "/predict"
    respuesta = requests.post(f"{args.url}{endpoint}", json=cuerpo, timeout=10)

    print(f"POST {endpoint} → HTTP {respuesta.status_code}")
    if respuesta.ok:
        print(json.dumps(respuesta.json(), indent=2, ensure_ascii=False))
    else:
        print("[AVISO] Error:", json.dumps(respuesta.json(), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
