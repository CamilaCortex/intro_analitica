# Módulo 07: Pipelines y selección de modelos

> **Objetivo:** empaquetar el preprocesamiento y el modelo en **un solo objeto reproducible**, elegir hiperparámetros sin *data leakage* y dejar el modelo **guardado y listo para producción**.

**Duración sugerida:** 2 a 3 horas · **Basado en:** `sesion_7_pipelines.ipynb` del profesor · **Fases 4 y 5 de CRISP-DM**

## Contenido

| Archivo | Para qué sirve |
|---|---|
| `notebooks/01_pipelines_iris.ipynb` | `Pipeline`, PCA, `cross_validate`, `set_params` y `GridSearchCV` con Iris |
| `notebooks/02_pipeline_house_prices.ipynb` | `ColumnTransformer`, target en log, comparación con CV, *tuning*, guardar y cargar el modelo |
| `scripts/train.py` | Entrena, evalúa, reentrena con todo y guarda `models/house_price_model.joblib` + metadatos |
| `scripts/predecir.py` | Predicciones de una casa (JSON) o por lotes (CSV) con el modelo guardado |
| `../src/intro_analitica/pipeline.py` | `construir_preprocesamiento()` y `construir_pipeline()`, compartidos entre el notebook, el script y la API |
| `ejercicios/EJERCICIOS.md` | Actividad en salas: el `train.py` del equipo |
| `presentacion/07-Pipelines.pptx` | Diapositivas |

---

## 1. El problema que resuelve un Pipeline

**Sin pipeline** (módulo 06):

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

## 5. Cómo ejecutar

```bash
uv run python 07-Pipelines/scripts/train.py --buscar
uv run python 07-Pipelines/scripts/predecir.py --csv data/raw/house_prices/test.csv --salida reports/predicciones.csv
```

Resultado de referencia: **MAPE en test ≈ 9.7 %** y R² ≈ 0.90.

---

## Checklist del módulo

- [ ] Sé construir un `Pipeline` con `ColumnTransformer`
- [ ] Entiendo por qué el pipeline evita el *data leakage* dentro de la validación cruzada
- [ ] Sé usar `GridSearchCV` con la notación `paso__parametro`
- [ ] Guardo el modelo **con metadatos**
- [ ] El equipo tiene un `src/train.py` que reproduce su modelo con un comando

**Anterior:** [Módulo 06: Modelado](../06-Modelado-Metricas/) · **Siguiente:** [Módulo 08: API](../08-API-FastAPI/)
