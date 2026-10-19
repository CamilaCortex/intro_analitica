# Módulo 06: Modelado y métricas

> **Objetivo:** entrenar modelos que le ganen a un ***baseline***, elegir la **métrica correcta** según el negocio y detectar el ***overfitting***.

**Duración sugerida:** 3 horas · **Basado en:** `sesion_6_modelo.ipynb` del profesor · **Fases 4 y 5 de CRISP-DM**

## Contenido

| Archivo | Para qué sirve |
|---|---|
| `notebooks/01_metricas.ipynb` | Tipos de ML, métricas de regresión y clasificación, umbral, paradoja de la *accuracy*, *over/underfitting* |
| `notebooks/02_baseline_house_prices.ipynb` | Train/val/test, *baseline*, 8 modelos, curva de complejidad, CV, importancia, análisis de errores, test final |
| `scripts/baseline.py` | Compara *baseline* + 3 modelos con CV para **cualquier** CSV (regresión o clasificación) |
| `../src/intro_analitica/metricas.py` | `metricas_regresion`, `tabla_comparativa`, `brecha_overfitting` |
| `ejercicios/EJERCICIOS.md` | Actividad en salas: el *baseline* del proyecto |
| `presentacion/06-Modelado-Metricas.pptx` | Diapositivas |

---

## 1. Tipos de aprendizaje

```
                       Machine Learning
             ┌───────────────┴────────────────┐
        Supervisado                     No supervisado
     (hay etiqueta "y")                (no hay etiqueta)
       ┌──────┴──────┐                 ┌──────┴──────┐
   Regresión    Clasificación      Clustering   Reducción de
   (número)     (categoría)        (segmentos)  dimensión (PCA)
```

## 2. Métricas de regresión

| Métrica | Fórmula (idea) | Unidades | Úsala cuando… |
|---|---|---|---|
| **MAE** | promedio de \|error\| | Las del target | Quieres un error "típico" y fácil de explicar |
| **RMSE** | √(promedio de error²) | Las del target | Los errores grandes son graves |
| **MAPE** | promedio de \|error / real\| × 100 | % | El negocio piensa en porcentajes (no sirve con targets cercanos a 0) |
| **R²** | 1 − SS_res / SS_tot | 0 a 1 | Comparar modelos sobre los mismos datos |

## 3. Métricas de clasificación

|  | Predicho 0 | Predicho 1 |
|---|:---:|:---:|
| **Real 0** | TN | FP (falsa alarma) |
| **Real 1** | FN (se escapó) | TP |

| Métrica | Pregunta | Prioriza cuando… |
|---|---|---|
| **Accuracy** | ¿Qué % acerté? | Clases balanceadas |
| **Precision** | De lo que marqué como positivo, ¿cuánto lo era? | Las falsas alarmas cuestan (spam) |
| **Recall** | De los positivos reales, ¿cuántos encontré? | Que se escape uno es grave (cáncer, fraude) |
| **F1** | Balance entre precision y recall | Clases desbalanceadas |
| **AUC-ROC** | ¿Qué tan bien ordena el riesgo? | Comparar modelos sin fijar un umbral |

> **El umbral (0.5 por defecto) es una decisión de negocio**, no técnica.
> **Paradoja de la accuracy:** con 99 % de casos negativos, decir siempre "no" da 99 % de accuracy… y 0 % de recall.

## 4. El flujo de modelado, paso a paso

```
 1. Dividir         2. Baseline         3. Modelos          4. Elegir con        5. Test
 train/val/test     (mediana o          lineal → árbol →    VALIDACIÓN y CV      UNA sola vez
 (60/20/20)         clase mayoritaria)  ensembles                                y se reporta
```

| Paso | Por qué |
|---|---|
| **Baseline** | Sin él no sabes si el modelo aporta algo |
| **Validación separada del test** | Si eliges mirando el test, el test deja de ser "nuevo" |
| **Validación cruzada** | Un solo split puede salir fácil o difícil por azar |
| ***Fit* del preprocesamiento solo en train** | Evita *data leakage* |

## 5. *Overfitting* vs. *underfitting*

| | *Underfitting* | Buen ajuste | *Overfitting* |
|---|---|---|---|
| Error train | Alto | Bajo | Muy bajo |
| Error validación | Alto | Bajo | Alto |
| Solución | Más complejidad o variables | | Más datos, modelo más simple, regularización (Ridge/Lasso), CV |

## 6. Resultados en House Prices

| Modelo | MAPE validación |
|---|---|
| Baseline (mediana) | ~31 % |
| Lineal (solo numéricas) | ~12.5 % |
| Lineal + categóricas + log(precio) | ~11 % |
| Random Forest / Gradient Boosting | ~10-11 % |
| **Gradient Boosting + log en TEST** | **~10 %** (criterio < 15 %) |

**Lecciones:** el *baseline* pone en perspectiva, el log del target ayuda a los modelos lineales, los *ensembles* memorizan mucho (brecha grande) pero generalizan bien, y la lineal queda a menos de un punto: **la interpretabilidad también cuenta**.

## 7. Cómo ejecutar

```bash
uv run python 06-Modelado-Metricas/scripts/baseline.py data/processed/house_prices_limpio.csv --target SalePrice
uv run python 06-Modelado-Metricas/ejercicios/soluciones/solucion_06_metricas.py
uv run python 06-Modelado-Metricas/ejercicios/soluciones/solucion_06_modelos.py
```

---

## Checklist del módulo

- [ ] Sé elegir la métrica según el costo de cada error
- [ ] Siempre comparo contra un *baseline*
- [ ] Separo validación (para elegir) de test (para reportar)
- [ ] Sé reconocer el *overfitting* en una curva de complejidad
- [ ] El equipo tiene su *baseline* y su primer modelo con métricas justificadas

**Anterior:** [Módulo 05: EDA](../05-EDA/) · **Siguiente:** [Módulo 07: Pipelines](../07-Pipelines/)
