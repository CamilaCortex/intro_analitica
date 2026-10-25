# Módulo 04: Modelado y métricas

> **Objetivo:** entrenar modelos que le ganen a un ***baseline***, elegir la **métrica correcta** según el negocio y detectar el ***overfitting***.

**Sesión:** miércoles 28 de octubre · **Fases de CRISP-DM:** 4. Modelado y 5. Evaluación

## Contenido

| Archivo | Para qué sirve |
|---|---|
| `README.md` | Teoría paso a paso (estás aquí) |
| `notebooks/01_metricas.ipynb` | Tipos de ML, métricas de regresión y clasificación, umbral, paradoja de la *accuracy*, *overfitting* |
| `notebooks/02_baseline_house_prices.ipynb` | Train/validación/test, *baseline*, modelos de complejidad creciente, validación cruzada, importancia de variables y análisis de errores |
| `../src/intro_analitica/metricas.py` | `metricas_regresion`, `tabla_comparativa`, `brecha_overfitting` |
| `ejercicios/EJERCICIOS.md` | Actividad de la clase: sección 5 del notebook del equipo |
| `ejercicios/soluciones/` | Soluciones de los ejercicios guiados |
| `presentacion/04-Modelado-Metricas.pptx` | Diapositivas |

### Cómo se reparte la clase

| Bloque | Tiempo | Qué se hace |
|---|---|---|
| Explicación | 40 min | Presentación: tipos de ML, métricas, *baseline* y *overfitting* |
| Práctica guiada | 15 min | Recorrido por los notebooks y Parte 1 de los ejercicios |
| Salas de Zoom | 45 min | Parte 2: el modelo del proyecto del equipo |
| Plenaria | 10 min | Cada equipo muestra su tabla: ¿le gana al *baseline*? |

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

## 7. El modelo en el notebook del equipo

La sección 5 de `proyecto_equipo.ipynb` hace este flujo con lo mínimo necesario:

| Paso | En el notebook | Qué decide el equipo |
|---|---|---|
| Variables | 5.1 | Qué columnas entran (las que el EDA mostró como importantes) |
| Dividir | 5.2 | Nada: 80 % train y 20 % test, con semilla fija |
| Preparar | 5.3 | Nada: imputación, escalado y *one-hot* automáticos y sin *leakage* |
| Comparar | 5.4 | Cuál métrica mirar según el negocio |
| Revisar errores | 5.5 | Qué modelo eligen y dónde se equivoca |

> En el notebook del equipo se usa solo train y test para que el flujo sea corto. El notebook 2 de este módulo muestra la versión completa con validación y validación cruzada; úsenla si quieren comparar más modelos sin "gastar" el test.

---

## Para profundizar (opcional)

- **Validación cruzada** (sección 6 del notebook 2): estima el desempeño con varios cortes de los datos, no con uno solo.
- **Modelos de *ensemble*** (Random Forest, Gradient Boosting): muchos árboles juntos; suelen mejorar el resultado a cambio de ser menos interpretables.
- **Curva ROC y elección del umbral** (secciones 3.3 y 3.4 del notebook 1), clave en clasificación cuando un tipo de error cuesta más que el otro.

Soluciones de los ejercicios guiados:

```bash
uv run python 04-Modelado-Metricas/ejercicios/soluciones/solucion_01_metricas.py
uv run python 04-Modelado-Metricas/ejercicios/soluciones/solucion_02_modelos.py
```

## Checklist del módulo

- [ ] Sé elegir la métrica según el costo de cada error
- [ ] Siempre comparo contra un *baseline*
- [ ] Separo validación (para elegir) de test (para reportar)
- [ ] Sé reconocer el *overfitting* en una curva de complejidad
- [ ] El equipo tiene en su notebook el *baseline*, dos modelos y la interpretación de los resultados

**Anterior:** [Módulo 03: Preparación de datos y EDA](../03-Preparacion-y-EDA/) · **Siguiente:** [Módulo 05: Del modelo al producto](../05-Pipelines-y-API/)
