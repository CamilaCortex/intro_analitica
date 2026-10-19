# Ejercicios: Módulo 07, Pipelines

> **Roten los roles.**

---

## Parte 1: Ejercicios guiados (35 min, primera parte de la clase)

| Notebook | Ejercicios | Solución |
|---|---|---|
| `01_pipelines_iris.ipynb` | SVC en la grilla · quitar PCA · `RandomizedSearchCV` | `soluciones/solucion_07_iris.py` |
| `02_pipeline_house_prices.ipynb` | `TotalSF` en el pipeline · RF con log · robustez a nulos · importancia por permutación | `soluciones/solucion_07_house_prices.py` |

---

## Parte 2: Salas de Zoom, el `train.py` del equipo (60 min)

> **Objetivo:** que **cualquier persona** pueda reproducir el modelo del equipo con **un solo comando** y obtenga el mismo archivo `.joblib`.
> **Viene de:** el modelo elegido en `docs/05_modelado.md` (módulo 06) y `src/limpieza.py` (módulo 04).
> **Va a:** módulo 08 (la API carga el `.joblib` que generen hoy).

### Paso 1: Diseñar el pipeline en papel (10 min)

Entre los tres, completen este esquema en `docs/06_pipeline.md`:

```
Pipeline
├── preprocesamiento
│   ├── numéricas:   [ … ] → pasos: …
│   ├── categóricas: [ … ] → pasos: …
│   └── ordinales:   [ … ] → pasos: … (orden: … < … < …)
└── modelo: …  (¿target transformado? ¿hiperparámetros?)
```

### Paso 2: Construirlo (30 min)

| Integrante | Archivo | Tarea |
|---|---|---|
| A | `src/pipeline.py` | `construir_pipeline()` con el `ColumnTransformer` (usen como modelo `src/intro_analitica/pipeline.py` del curso) |
| B | `src/train.py` | Cargar datos → `limpiar()` → split → `fit` → métricas → guardar `.joblib` + `.json` |
| C | `notebooks/07_pipeline.ipynb` | `cross_validate` de 2-3 modelos con el pipeline + un `GridSearchCV` pequeño |

Esqueleto de `src/train.py`:

```python
"""Entrena el modelo del proyecto y lo guarda en models/."""
import json
from datetime import datetime

import joblib
import pandas as pd
from sklearn.model_selection import train_test_split

from src.limpieza import limpiar
from src.pipeline import construir_pipeline

TARGET = "<target>"
FEATURES = [...]

df = limpiar(pd.read_csv("data/raw/<archivo>.csv"))
X_train, X_test, y_train, y_test = train_test_split(df[FEATURES], df[TARGET], test_size=0.2, random_state=42)

pipeline = construir_pipeline().fit(X_train, y_train)
metricas = {...}  # su métrica principal en test

pipeline.fit(df[FEATURES], df[TARGET])  # reentrenar con todo
joblib.dump(pipeline, "models/modelo.joblib")
json.dump({"version": "1.0.0", "fecha": datetime.now().isoformat(), "features": FEATURES, "metricas": metricas},
          open("models/modelo.json", "w"), indent=2)
```

> Para que `from src.limpieza import …` funcione, agreguen un archivo vacío `src/__init__.py` y ejecuten desde la raíz con `uv run python -m src.train`.

### Paso 3: Prueba de reproducibilidad (10 min)

1. Cada integrante, en **su** computador: `git pull` → `uv sync` → `uv run python -m src.train`.
2. ¿Les dio a los tres **la misma métrica**? Si no, ¿qué semilla falta?

### Paso 4: Documentar (10 min)

Agreguen al README una sección **"Cómo entrenar el modelo"** con el comando y la métrica de referencia.

### Entregable

- [ ] `src/pipeline.py` con `ColumnTransformer` + modelo
- [ ] `src/train.py` que se ejecuta con un comando y guarda `models/modelo.joblib` + `models/modelo.json`
- [ ] Los 3 integrantes obtienen la misma métrica
- [ ] `docs/06_pipeline.md` con el diseño
- [ ] `models/` en el `.gitignore` (el modelo se **regenera**, no se sube)
- [ ] PR unido a `main`

### Reto opcional

Agreguen un script `src/predecir.py` que reciba un CSV y genere predicciones (como `07-Pipelines/scripts/predecir.py` del curso). Pruébenlo con 5 filas que **ustedes inventen**.

---

## Preguntas para la plenaria

1. ¿Qué tuvieron que cambiar para que el pipeline aceptara sus datos (tipos, columnas raras…)?
2. ¿Obtuvieron todos la misma métrica? ¿Qué aprendieron sobre las semillas?
3. ¿Cuánto mejoró el *tuning* frente a los hiperparámetros por defecto? ¿Valió la pena el tiempo?

## Para la próxima sesión

Tengan `models/modelo.joblib` generado. En el **módulo 08** lo servirán con una API.
