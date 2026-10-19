# Ejercicios: Módulo 06, Modelado y métricas

> **Roten los roles.**

---

## Parte 1: Ejercicios guiados (35 min, primera parte de la clase)

| Notebook | Ejercicios | Solución |
|---|---|---|
| `01_metricas.ipynb` | Métricas a mano · umbral con FN ≤ 1 · Ridge vs. lineal | `soluciones/solucion_06_metricas.py` |
| `02_baseline_house_prices.ipynb` | Más variables · sin *outliers* · RF regularizado · reflexión sobre el test | `soluciones/solucion_06_modelos.py` |

**Discusión del profesor (5 min):** ¿qué pesa más, el desempeño o la interpretabilidad? Piensen en un banco que niega un crédito: ¿qué le explica al cliente?

---

## Parte 2: Salas de Zoom, el *baseline* del proyecto (60 min)

> **Objetivo:** saber **cuánto mejor** que "no tener modelo" puede hacerlo el equipo, con la métrica que importa para su negocio.
> **Viene de:** la lista de variables candidatas del EDA (módulo 05) y el criterio de éxito del *charter* (módulo 03).
> **Va a:** módulo 07 (el mejor modelo de hoy se convierte en un pipeline reproducible).

### Paso 1: Elegir la métrica (10 min)

Respondan en `docs/05_modelado.md`:

1. ¿Es **regresión** o **clasificación**?
2. ¿Qué error es **más caro** para el negocio? (sobreestimar o subestimar; un FP o un FN)
3. Entonces, ¿cuál es la **métrica principal** y cuáles las secundarias? ¿Coincide con el *charter*?

### Paso 2: Comparación rápida con el script (10 min)

```bash
uv run python <ruta>/intro_analitica/06-Modelado-Metricas/scripts/baseline.py \
    data/processed/<archivo>_limpio.csv --target <target> --tipo <regresion|clasificacion> \
    --columnas <variables candidatas del EDA>
```

Copien la tabla en `docs/05_modelado.md`. ¿Algún modelo le gana **claramente** al *baseline*?

### Paso 3: Notebook de modelado (30 min)

Repártanse el trabajo en `notebooks/06_modelado.ipynb` (o un notebook por persona):

| Integrante | Tarea |
|---|---|
| A | Split train/val/test + *baseline* + modelo lineal/logístico |
| B | Árbol con curva de complejidad (`max_depth`) → detectar *overfitting* |
| C | Random Forest o Gradient Boosting + importancia de variables |

Al final, **una tabla comparativa** con la métrica principal en train y validación, y la brecha.

Si es **clasificación**: matriz de confusión + elegir el umbral con un argumento de negocio.

### Paso 4: Conclusión (10 min)

En `docs/05_modelado.md`:

- ¿Qué modelo eligen y **por qué** (desempeño, interpretabilidad, brecha)?
- ¿Cumple el criterio de éxito del *charter*? Si no, ¿qué harían en la siguiente iteración?
- Los 3 peores errores del modelo: ¿tienen algo en común?

> **No toquen el test** hasta que tengan el modelo elegido. Evalúen en test **una sola vez** y reporten ese número.

### Entregable

- [ ] `docs/05_modelado.md` con métrica justificada, tabla del script y conclusión
- [ ] `notebooks/06_modelado.ipynb` con *baseline*, al menos 3 modelos y la curva de complejidad
- [ ] Métrica en test del modelo elegido (una sola vez)
- [ ] PR unido a `main`

### Reto opcional

- Regresión: prueben el target en logaritmo. ¿Mejora?
- Clasificación desbalanceada: prueben `class_weight="balanced"` y comparen el recall.

---

## Preguntas para la plenaria

1. ¿Por cuánto le ganan al *baseline*? ¿Es suficiente para el negocio?
2. ¿Qué modelo eligieron y qué sacrificaron (interpretabilidad, velocidad)?
3. ¿Vieron *overfitting*? ¿Cómo lo detectaron?

## Para la próxima sesión

Tengan claro el modelo elegido y su preprocesamiento. En el **módulo 07** los empaquetarán en un `Pipeline` y en un script `train.py`.
