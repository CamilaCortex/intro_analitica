# Módulo 03: Del modelo al producto (pipelines y API)

> **Objetivo:** empaquetar la preparación de los datos y el modelo en **un solo objeto reproducible**, guardarlo y ponerlo a disposición de **cualquier aplicación** a través de una API.

**Sesión:** miércoles 11 de noviembre · **Fases de CRISP-DM:** 5. Evaluación y 6. Despliegue

Esta clase es principalmente una **demostración**: la profesora construye el pipeline y levanta la API con House Prices, y los equipos usan la segunda parte para cerrar su proyecto y preparar la sustentación. **La API no es obligatoria en el proyecto**: es una bonificación (ver la [rúbrica](../06-Proyecto-Final/rubrica.md)).

## Contenido

```
05-Pipelines-y-API/
├── README.md                              ← teoría paso a paso (estás aquí)
├── notebooks/
│   ├── 01_pipeline_house_prices.ipynb     ← ColumnTransformer, target en log, CV, GridSearch, guardar el modelo
│   ├── 02_consumir_api.ipynb              ← llamar a la API desde Python
│   └── complementario/pipelines_iris.ipynb← para profundizar: Pipeline, PCA y GridSearchCV paso a paso
├── scripts/
│   ├── train.py                           ← entrena y guarda models/house_price_model.joblib + metadatos
│   ├── predecir.py                        ← predicciones de una casa (JSON) o por lotes (CSV)
│   └── cliente.py                         ← consumir la API desde la terminal
├── api/                                   ← la API con FastAPI
│   ├── main.py      ← endpoints /health, /model-info, /predict, /predict/batch
│   ├── schemas.py   ← Pydantic: qué datos entran y salen, y sus reglas
│   ├── modelo.py    ← cargar el pipeline y predecir
│   └── config.py    ← rutas, puerto y límites
├── tests/test_api.py                      ← pruebas automáticas con pytest
├── ejemplos/                              ← casa.json, casas.json
├── ejercicios/EJERCICIOS.md               ← actividad de la clase: cierre del proyecto
└── presentacion/05-Pipelines-y-API.pptx
```

### Cómo se reparte la clase

| Bloque | Tiempo | Qué se hace |
|---|---|---|
| Explicación y demostración | 50 min | Pipelines, guardar el modelo y API en vivo con House Prices |
| Salas de Zoom | 50 min | Sección 6 del notebook, revisión con el checklist y esquema de la presentación |
| Plenaria | 15 min | Dudas sobre la sustentación |

---

# Parte A: Pipelines

## 1. El problema que resuelve un Pipeline

**Sin pipeline** (como en el notebook 2 del módulo 03):

```python
encoder.fit(X_train[cat])          # ¿me acordé de hacerlo solo en train?
X_tr = preparar(X_train)           # ¿y en validación?
X_te = preparar(X_test)            # ¿y en test?
modelo.fit(X_tr, np.log1p(y))      # ¿y deshacer el log?
joblib.dump(modelo)                # ¡olvidé guardar el encoder!
```

**Con pipeline:**

```python
pipeline.fit(X_train, y_train)     # todo se ajusta solo con train
pipeline.predict(X_nuevo)          # todo se transforma igual
joblib.dump(pipeline, "modelo.joblib")   # un solo archivo
```

## 2. Las piezas

```
Pipeline
├── "preprocesamiento": ColumnTransformer
│     ├── "num": Pipeline[ SimpleImputer(median) → StandardScaler ]      ← numéricas
│     ├── "cat": Pipeline[ SimpleImputer(most_frequent) → OneHotEncoder ] ← sin orden
│     └── "ord": Pipeline[ SimpleImputer(most_frequent) → OrdinalEncoder ] ← con orden
└── "modelo": TransformedTargetRegressor(log1p / expm1)
                └── HistGradientBoostingRegressor
```

| Pieza | Qué hace |
|---|---|
| `Pipeline([(nombre, paso), …])` | Encadena pasos; el último es el modelo |
| `ColumnTransformer` | Aplica un tratamiento distinto a cada grupo de columnas |
| `TransformedTargetRegressor` | Entrena con `log(y)` y devuelve la predicción en la escala original |
| `OneHotEncoder(handle_unknown="ignore")` | No falla si llega una categoría nueva en producción |

## 3. Selección de modelos e hiperparámetros

| Herramienta | Cuándo |
|---|---|
| `cross_validate(pipeline, X, y, cv=5)` | Estimar el desempeño con su variabilidad |
| `pipeline.set_params(modelo=OtroModelo())` | Cambiar el modelo y comparar |
| `GridSearchCV` | Probar **todas** las combinaciones (grillas pequeñas) |
| `RandomizedSearchCV` | Probar **n** combinaciones al azar (grillas grandes) |

**Notación:** `paso__subpaso__parametro` (dos guiones bajos). Por ejemplo, `modelo__regressor__learning_rate`.

> **Parámetro vs. hiperparámetro:** los *parámetros* los aprende el modelo (los coeficientes de una regresión); los *hiperparámetros* los fijas tú antes de entrenar (la profundidad de un árbol).

## 4. El flujo de `train.py`

```
 cargar datos ─> split 80/20 ─> (GridSearchCV en train) ─> evaluar en test ─> ¿MAPE < 15 %?
                                                                                   │
                         models/house_price_model.joblib <── reentrenar con TODO <─┘
                         models/house_price_model.json   (versión, fecha, métricas, features)
```

### Cómo ejecutarlo

```bash
uv run python 05-Pipelines-y-API/scripts/train.py            # entrenar y guardar
uv run python 05-Pipelines-y-API/scripts/train.py --buscar   # con GridSearchCV (más lento)
uv run python 05-Pipelines-y-API/scripts/predecir.py --csv data/raw/house_prices/test.csv --salida reports/predicciones.csv
```

Resultado de referencia: **MAPE en test ≈ 9.7 %** y R² ≈ 0.90.

> **En el notebook del equipo** ya usan un pipeline: en la sección 5.3, `ColumnTransformer` prepara las variables y `make_pipeline` lo une con cada modelo. La sección 6.1 lo guarda con `joblib`. Este módulo explica en detalle lo que esas celdas hacen.

---

# Parte B: La API

## 5. ¿Qué es una API y por qué la necesitamos?

Una **API** (*Application Programming Interface*) es un "mesero": la aplicación (el cliente) hace un pedido en un formato acordado (JSON), la API lo lleva a la cocina (el modelo) y le devuelve el plato (la predicción).

```
 App web / móvil ──HTTP POST /predict──> API ──predict()──> Pipeline (.joblib)
                 <──── 200 + JSON ───────     <────────────
```

| En tiempo real (API): el de este módulo | Por lotes (*batch*) |
|---|---|
| Responde en milisegundos a cada solicitud | Procesa miles de registros de una vez (`scripts/predecir.py`) |
| Un usuario pide un avalúo en la web | Revaluar todo el portafolio cada mes |

## 6. ¿Por qué FastAPI?

- Rápido de escribir y de ejecutar.
- Valida los datos automáticamente con **Pydantic** (tipos y reglas).
- Genera documentación interactiva en `/docs` **sin escribir nada extra**.

## 7. Paso a paso

### Paso 1: Tener el modelo

```bash
uv run python 05-Pipelines-y-API/scripts/train.py
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
uv run uvicorn api.main:app --reload --app-dir 05-Pipelines-y-API
```

- Documentación: http://127.0.0.1:8000/docs
- Salud: http://127.0.0.1:8000/health

### Paso 5: Probarla

```bash
# Pruebas automáticas
uv run pytest -v

# Desde la terminal (en Windows, ejecútenlo en Git Bash)
curl -X POST http://127.0.0.1:8000/predict -H "Content-Type: application/json" -d @05-Pipelines-y-API/ejemplos/casa.json

# Desde Python
uv run python 05-Pipelines-y-API/scripts/cliente.py
```

## 8. Códigos de estado que usa esta API

| Código | Significa | Cuándo |
|---|---|---|
| **200** | OK | Predicción exitosa |
| **422** | Datos inválidos | Falta un campo, tipo incorrecto, valor fuera de rango, remodelación anterior a la construcción |
| **413** | Solicitud demasiado grande | Más de `MAX_BATCH` casas en `/predict/batch` |
| **503** | Servicio no disponible | El modelo no está cargado (no se ha entrenado) |

### Docker y la nube (fuera del alcance del curso)

```dockerfile
FROM python:3.14-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv
WORKDIR /app
COPY . .
RUN uv sync --frozen --no-dev
CMD ["uv", "run", "uvicorn", "api.main:app", "--app-dir", "05-Pipelines-y-API", "--host", "0.0.0.0", "--port", "8000"]
```

Con un contenedor, la API corre igual en cualquier servidor (AWS, GCP, Azure, Render…). Esto se profundiza en el curso de **MLOps**.

---

## Checklist del módulo

- [ ] Sé explicar qué problema resuelve un `Pipeline` y por qué evita el *data leakage*
- [ ] Entiendo qué hacen `ColumnTransformer` y `joblib.dump`
- [ ] Sé qué es una API y qué significan los códigos 200, 422 y 503
- [ ] Vi la API funcionando en `/docs`
- [ ] El equipo tiene la sección 6 del notebook y el esquema de la presentación final

**Anterior:** [Módulo 03: Modelado y métricas](../04-Modelado-Metricas/) · **Siguiente:** [Módulo 04: Proyecto final](../06-Proyecto-Final/)
