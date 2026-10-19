"""
Pruebas de la API con pytest y el TestClient de FastAPI.

Ejecutar (desde la raíz del repo)::

    uv run pytest -v

El TestClient simula solicitudes HTTP SIN levantar un servidor real: es rápido y
se puede correr en GitHub Actions.

Requiere el modelo entrenado (07-Pipelines/scripts/train.py). Si no existe, las
pruebas de predicción se saltan (skip) con un mensaje claro.
"""

import pytest
from fastapi.testclient import TestClient

from api import config
from api.main import app
from api.schemas import EJEMPLO_CASA

requiere_modelo = pytest.mark.skipif(
    not config.MODEL_PATH.exists(),
    reason="Primero entrena el modelo: uv run python 07-Pipelines/scripts/train.py",
)


@pytest.fixture(scope="module")
def cliente():
    # El "with" ejecuta el lifespan (carga del modelo)
    with TestClient(app) as c:
        yield c


def test_health_responde(cliente):
    respuesta = cliente.get("/health")
    assert respuesta.status_code == 200
    assert respuesta.json()["api_version"] == config.API_VERSION


@requiere_modelo
def test_health_modelo_cargado(cliente):
    assert cliente.get("/health").json()["modelo_cargado"] is True


@requiere_modelo
def test_model_info_tiene_metricas(cliente):
    info = cliente.get("/model-info").json()
    assert "metricas_test" in info
    assert info["metricas_test"]["MAPE_%"] < 15  # el criterio de negocio del charter


@requiere_modelo
def test_predict_casa_valida(cliente):
    respuesta = cliente.post("/predict", json=EJEMPLO_CASA)
    assert respuesta.status_code == 200
    cuerpo = respuesta.json()
    assert 50_000 < cuerpo["precio_estimado"] < 600_000  # rango razonable para Ames
    minimo, maximo = cuerpo["rango_aproximado"]
    assert minimo < cuerpo["precio_estimado"] < maximo


@requiere_modelo
def test_mas_calidad_mas_precio(cliente):
    """Prueba de "sentido común": a igualdad de lo demás, más calidad → más precio."""
    baja = cliente.post("/predict", json={**EJEMPLO_CASA, "OverallQual": 4}).json()["precio_estimado"]
    alta = cliente.post("/predict", json={**EJEMPLO_CASA, "OverallQual": 9}).json()["precio_estimado"]
    assert alta > baja


@requiere_modelo
def test_barrio_desconocido_no_falla(cliente):
    respuesta = cliente.post("/predict", json={**EJEMPLO_CASA, "Neighborhood": "Laureles"})
    assert respuesta.status_code == 200


@pytest.mark.parametrize(
    "cambio",
    [
        {"GrLivArea": -100},           # área negativa
        {"OverallQual": 15},           # fuera de 1-10
        {"KitchenQual": "Excelente"},  # categoría no permitida
        {"LotArea": "grande"},         # tipo incorrecto
    ],
)
def test_predict_datos_invalidos_422(cliente, cambio):
    respuesta = cliente.post("/predict", json={**EJEMPLO_CASA, **cambio})
    assert respuesta.status_code == 422


def test_predict_campo_faltante_422(cliente):
    incompleta = {k: v for k, v in EJEMPLO_CASA.items() if k != "GrLivArea"}
    assert cliente.post("/predict", json=incompleta).status_code == 422


@requiere_modelo
def test_remodelacion_antes_de_construccion_422(cliente):
    respuesta = cliente.post("/predict", json={**EJEMPLO_CASA, "YearBuilt": 2005, "YearRemodAdd": 1990})
    assert respuesta.status_code == 422


@requiere_modelo
def test_batch(cliente):
    casas = [EJEMPLO_CASA, {**EJEMPLO_CASA, "OverallQual": 9}, {**EJEMPLO_CASA, "GrLivArea": 1200}]
    respuesta = cliente.post("/predict/batch", json={"casas": casas})
    assert respuesta.status_code == 200
    assert respuesta.json()["cantidad"] == 3


def test_batch_vacio_422(cliente):
    assert cliente.post("/predict/batch", json={"casas": []}).status_code == 422
