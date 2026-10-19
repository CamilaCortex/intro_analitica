"""
API REST para el modelo de precios de vivienda.

Levantar el servidor (desde la raíz del repo)::

    uv run uvicorn api.main:app --reload --app-dir 08-API-FastAPI
    # o
    uv run python 08-API-FastAPI/api/main.py

Luego abre http://127.0.0.1:8000/docs para probarla desde el navegador.

Endpoints
---------
GET  /health          → ¿está viva la API? ¿cargó el modelo?
GET  /model-info      → versión, fecha, variables y métricas del modelo
POST /predict         → precio de UNA casa
POST /predict/batch   → precios de VARIAS casas

Diferencias con el ejemplo del profesor (api-example-udem-2026-01):
    - Los errores devuelven el código HTTP correcto (422/503) en lugar de 200 con un mensaje.
    - La validación de negocio (área > 0, calidad entre 1 y 10…) vive en el esquema de Pydantic.
    - El modelo se carga al iniciar la app (lifespan) y no al importar el módulo,
      así las pruebas pueden usar otro modelo.
"""

import sys
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException

# Permite ejecutar este archivo directamente (python 08-API-FastAPI/api/main.py)
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from api import config  # noqa: E402
from api.modelo import ModeloNoDisponible, ServicioModelo  # noqa: E402
from api.schemas import (  # noqa: E402
    CasaEntrada,
    LoteEntrada,
    LoteSalida,
    PrediccionSalida,
)

estado: dict = {"servicio": None, "error": None}


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Se ejecuta UNA vez al arrancar: carga el modelo en memoria."""
    try:
        estado["servicio"] = ServicioModelo()
        estado["error"] = None
    except ModeloNoDisponible as error:
        # La API arranca igual, pero /health avisa y /predict responde 503.
        estado["servicio"], estado["error"] = None, str(error)
    yield
    estado["servicio"] = None


app = FastAPI(title=config.TITULO, description=config.DESCRIPCION, version=config.API_VERSION, lifespan=lifespan)


def obtener_servicio() -> ServicioModelo:
    if estado["servicio"] is None:
        # 503 = "Service Unavailable": el servidor funciona, pero no puede atender ahora
        raise HTTPException(status_code=503, detail=estado["error"] or "Modelo no cargado")
    return estado["servicio"]


@app.get("/health", tags=["Monitoreo"])
def health() -> dict:
    """Chequeo de salud: lo usan los balanceadores y los sistemas de monitoreo."""
    servicio = estado["servicio"]
    return {
        "status": "healthy" if servicio else "degraded",
        "api_version": config.API_VERSION,
        "modelo_cargado": servicio is not None,
        "version_modelo": servicio.version if servicio else None,
    }


@app.get("/model-info", tags=["Monitoreo"])
def model_info() -> dict:
    """Metadatos del modelo: qué es, cuándo se entrenó y qué tan bueno es."""
    return obtener_servicio().metadata


@app.post("/predict", response_model=PrediccionSalida, tags=["Predicción"])
def predict(casa: CasaEntrada) -> PrediccionSalida:
    """Estima el precio de una casa.

    Si los datos no cumplen el esquema (campo faltante, calidad 15, área negativa…),
    FastAPI responde **422** automáticamente, antes de llegar a esta función.
    """
    servicio = obtener_servicio()
    if casa.YearRemodAdd < casa.YearBuilt:
        # Regla que involucra DOS campos: se valida aquí
        raise HTTPException(status_code=422, detail="YearRemodAdd no puede ser anterior a YearBuilt")
    precio = servicio.predecir([casa])[0]
    return PrediccionSalida(precio_estimado=precio, rango_aproximado=servicio.rango(precio), version_modelo=servicio.version)


@app.post("/predict/batch", response_model=LoteSalida, tags=["Predicción"])
def predict_batch(lote: LoteEntrada) -> LoteSalida:
    """Estima el precio de varias casas en una sola llamada (más eficiente que llamar /predict N veces)."""
    servicio = obtener_servicio()
    if len(lote.casas) > config.MAX_BATCH:
        raise HTTPException(status_code=413, detail=f"Máximo {config.MAX_BATCH} casas por solicitud")
    predicciones = servicio.predecir(lote.casas)
    return LoteSalida(predicciones=predicciones, cantidad=len(predicciones), version_modelo=servicio.version)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("api.main:app", host=config.HOST, port=config.PORT, reload=False, app_dir=str(Path(__file__).resolve().parents[1]))
