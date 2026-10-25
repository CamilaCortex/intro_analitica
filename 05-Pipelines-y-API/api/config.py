"""
Configuración de la API.

Igual que en el ejemplo del profesor (``conf/parameters.py``), los valores
"mágicos" viven en un solo lugar. La diferencia: aquí cada valor se puede
cambiar con una **variable de entorno**, sin tocar el código. Así la misma API
corre en tu computador, en un servidor o en un contenedor.

    MODEL_PATH=otro_modelo.joblib PORT=9000 uv run python 05-Pipelines-y-API/api/main.py
"""

import os
from pathlib import Path

from intro_analitica import config as config_curso

API_VERSION = "1.0.0"
TITULO = "API de avalúo de viviendas "
DESCRIPCION = (
    "Estima el precio de venta de una casa (USD) a partir de 14 características. "
    "Modelo: pipeline de scikit-learn entrenado en el módulo 05 con House Prices (Ames, Iowa)."
)

MODEL_PATH = Path(os.getenv("MODEL_PATH", config_curso.MODELS_DIR / "house_price_model.joblib"))
METADATA_PATH = MODEL_PATH.with_suffix(".json")

HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", "8000"))
ROUND_DECIMALS = int(os.getenv("ROUND_DECIMALS", "0"))
MAX_BATCH = int(os.getenv("MAX_BATCH", "100"))  # máximo de casas por solicitud en /predict/batch
