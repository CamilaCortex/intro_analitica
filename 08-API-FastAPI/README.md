# Módulo 08: Despliegue del modelo con una API (FastAPI)

> **Objetivo:** que el modelo deje de vivir en un notebook y lo pueda usar **cualquier aplicación**, con validación de datos, manejo de errores y pruebas automáticas.

**Duración sugerida:** 3 horas · **Basado en:** [`api-example-udem-2026-01`](https://github.com/nicolasggiraldo/api-example-udem-2026-01) del profesor · **Fase 6 de CRISP-DM**

## Contenido

```
08-API-FastAPI/
├── api/
│   ├── main.py       ← la app: endpoints /health, /model-info, /predict, /predict/batch
│   ├── schemas.py    ← Pydantic: qué datos entran y salen, y sus reglas
│   ├── modelo.py     ← cargar el pipeline y predecir
│   └── config.py     ← rutas, puerto, límites (con variables de entorno)
├── tests/test_api.py ← 14 pruebas con pytest
├── scripts/cliente.py← consumir la API desde Python
├── notebooks/01_consumir_api.ipynb
├── ejemplos/         ← casa.json, casas.json
└── ejercicios/
```

---

## 1. ¿Qué es una API y por qué la necesitamos?

Una **API** (*Application Programming Interface*) es un "mesero": la aplicación (el cliente) hace un pedido en un formato acordado (JSON), la API lo lleva a la cocina (el modelo) y le devuelve el plato (la predicción).

```
 App web / móvil ──HTTP POST /predict──> API ──predict()──> Pipeline (.joblib)
                 <──── 200 + JSON ───────     <────────────
```

| En tiempo real (API): el de este módulo | Por lotes (*batch*) |
|---|---|
| Responde en milisegundos a cada solicitud | Procesa miles de registros de una vez (`07-Pipelines/scripts/predecir.py`) |
| Un usuario pide un avalúo en la web | Revaluar todo el portafolio cada mes |

## 2. ¿Por qué FastAPI?

- Rápido de escribir y de ejecutar.
- Valida los datos automáticamente con **Pydantic** (tipos y reglas).
- Genera documentación interactiva en `/docs` **sin escribir nada extra**.

## 3. Paso a paso

### Paso 1: Tener el modelo

```bash
uv run python 07-Pipelines/scripts/train.py
# → models/house_price_model.joblib + models/house_price_model.json
```

### Paso 2: Definir el contrato (`schemas.py`)

```python
class CasaEntrada(BaseModel):
    GrLivArea: int = Field(gt=0, description="Área habitable (pies²)")
    OverallQual: int = Field(ge=1, le=10)
    KitchenQual: Literal["Po", "Fa", "TA", "Gd", "Ex"]
    ...
```

Si llega `OverallQual = 15`, FastAPI responde **422** con el detalle del error y el modelo ni se entera.

### Paso 3: Los endpoints (`main.py`)

```python
@app.post("/predict", response_model=PrediccionSalida)
def predict(casa: CasaEntrada):
    precio = servicio.predecir([casa])[0]
    return PrediccionSalida(precio_estimado=precio, ...)
```

### Paso 4: Levantar el servidor

```bash
uv run uvicorn api.main:app --reload --app-dir 08-API-FastAPI
```

- Documentación: http://127.0.0.1:8000/docs
- Salud: http://127.0.0.1:8000/health

### Paso 5: Probarla

```bash
# Pruebas automáticas
uv run pytest -v

# Desde la terminal
curl -X POST http://127.0.0.1:8000/predict -H "Content-Type: application/json" -d @08-API-FastAPI/ejemplos/casa.json

# Desde Python
uv run python 08-API-FastAPI/scripts/cliente.py
```

## 4. Códigos de estado que usa esta API

| Código | Significa | Cuándo |
|---|---|---|
| **200** | OK | Predicción exitosa |
| **422** | Datos inválidos | Falta un campo, tipo incorrecto, valor fuera de rango, remodelación anterior a la construcción |
| **413** | Solicitud demasiado grande | Más de `MAX_BATCH` casas en `/predict/batch` |
| **503** | Servicio no disponible | El modelo no está cargado (no se ha entrenado) |

## 5. Qué cambiamos respecto al ejemplo del profesor (y por qué)

| Ejemplo original | Este módulo | Por qué |
|---|---|---|
| 2 variables (`lot_size`, `bedrooms`) | 14 variables + pipeline completo | Conecta con todo el curso |
| Errores devueltos con estado **200** y un mensaje | `HTTPException` con **422/503** | Los clientes detectan los errores por el código, no leyendo el texto |
| Validación con `if` dentro del endpoint | Reglas en Pydantic (`Field(gt=0)`, `Literal`) | Validación declarativa y documentada en `/docs` |
| `pickle` | `joblib` + metadatos `.json` | Trazabilidad: versión, fecha y métricas del modelo |
| Modelo cargado al importar | Cargado en el `lifespan` | Arranque controlado y API "degradada" si falta el modelo |
| Sin pruebas | 14 pruebas con pytest | Confianza para cambiar el código |

Se mantiene la idea del profesor de **separar responsabilidades** (`conf/` → `config.py`, `src/load_model.py` → `modelo.py`, `src/input_data.py` → `schemas.py`).

## 6. Siguiente paso (fuera del alcance del curso): Docker y la nube

```dockerfile
FROM python:3.14-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv
WORKDIR /app
COPY . .
RUN uv sync --frozen --no-dev
CMD ["uv", "run", "uvicorn", "api.main:app", "--app-dir", "08-API-FastAPI", "--host", "0.0.0.0", "--port", "8000"]
```

Con un contenedor, la API corre igual en cualquier servidor (AWS, GCP, Azure, Render…). Esto se profundiza en el curso de **MLOps**.

---

## Checklist del módulo

- [ ] Levanto la API y la pruebo desde `/docs`
- [ ] Entiendo el papel de Pydantic en la validación
- [ ] Sé qué significan los códigos 200, 422 y 503
- [ ] `uv run pytest` pasa todas las pruebas
- [ ] El equipo tiene su API con `/health` y `/predict` y al menos 3 pruebas

**Anterior:** [Módulo 07: Pipelines](../07-Pipelines/) · **Siguiente:** [Módulo 09: Proyecto final](../09-Proyecto-Final/)
