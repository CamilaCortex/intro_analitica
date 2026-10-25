"""
Carga del modelo y predicción.

Separar esto de ``main.py`` (como hace el profesor con ``src/load_model.py``)
permite probar la lógica del modelo sin levantar el servidor, y cambiar la
forma de cargarlo (p.ej. desde la nube) sin tocar los endpoints.
"""

import json
from pathlib import Path

import joblib
import pandas as pd

from api import config
from api.schemas import CasaEntrada


class ModeloNoDisponible(RuntimeError):
    """El archivo del modelo no existe: hay que entrenarlo primero."""


class ServicioModelo:
    """Envuelve el pipeline de scikit-learn y sus metadatos."""

    def __init__(self, ruta_modelo: Path = config.MODEL_PATH, ruta_metadata: Path = config.METADATA_PATH):
        if not ruta_modelo.exists():
            raise ModeloNoDisponible(
                f"No se encontró el modelo en {ruta_modelo}. "
                "Entrénalo con: uv run python 05-Pipelines-y-API/scripts/train.py"
            )
        self.pipeline = joblib.load(ruta_modelo)
        self.metadata = json.loads(ruta_metadata.read_text(encoding="utf-8")) if ruta_metadata.exists() else {}
        self.version = str(self.metadata.get("version", "desconocida"))
        self.mape = float(self.metadata.get("metricas_test", {}).get("MAPE_%", 0.0))

    def predecir(self, casas: list[CasaEntrada]) -> list[float]:
        """Convierte las casas en un DataFrame y llama al pipeline.

        El pipeline hace TODO el preprocesamiento (imputar, escalar, one-hot…),
        por eso aquí basta con pasarle los datos "crudos".
        """
        datos = pd.DataFrame([casa.model_dump() for casa in casas])
        return [round(float(p), config.ROUND_DECIMALS) for p in self.pipeline.predict(datos)]

    def rango(self, precio: float) -> tuple[float, float]:
        """Rango orientativo: precio ± el MAPE obtenido en test."""
        margen = precio * self.mape / 100
        return (round(precio - margen, config.ROUND_DECIMALS), round(precio + margen, config.ROUND_DECIMALS))
