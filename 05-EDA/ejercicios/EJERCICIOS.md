# Ejercicios: Módulo 05, EDA

> **Roten los roles.**

---

## Parte 1: Ejercicios guiados (20 min, primera parte de la clase)

Al final de `notebooks/01_eda_house_prices.ipynb`:

1. Precio por m² por barrio
2. Estacionalidad del **precio** (no del volumen)
3. *Outliers* extremos (k = 3) de `LotArea`
4. Plantear y validar una hipótesis propia

Soluciones en `soluciones/solucion_05.py`.

---

## Parte 2: Salas de Zoom, el EDA del proyecto del equipo (60 min)

> **Objetivo:** validar las hipótesis del *charter* y llegar a **5 hallazgos** que justifiquen las variables del modelo.
> **Viene de:** `data/processed/<archivo>_limpio.csv` (módulo 04) y las hipótesis de `docs/02_perfil_inicial.md` (módulo 03).
> **Va a:** módulo 06 (el *baseline* y los primeros modelos usan estas variables).

### Paso 1: EDA automático como punto de partida (10 min)

```bash
uv run python <ruta>/intro_analitica/05-EDA/scripts/reporte_eda.py \
    data/processed/<archivo>_limpio.csv --target <columna_objetivo> --salida reports/eda
```

Abran `reports/eda/resumen.md` y las figuras. ¿Qué les llama la atención?

### Paso 2: Repartir las hipótesis (5 min)

Cada integrante toma **una o dos hipótesis** del *charter* (y pueden agregar nuevas).

### Paso 3: Validar (30 min)

En `notebooks/05_eda.ipynb` (una sección por integrante, **o** un notebook por persona para evitar conflictos), para cada hipótesis:

```markdown
### H1: <enunciado>
**Cómo la valido:** <gráfico o tabla>
<código>
**Resultado:** Confirmada / Rechazada / No concluyente
**¿Controlé por otra variable?** <sí/no, cuál>
```

Mínimo por equipo: 1 análisis del target, 2 univariados, 3 bivariados y 1 revisión de *outliers*.

### Paso 4: Conclusiones (15 min)

Agreguen al README (o en `docs/04_eda.md`) la tabla:

| # | Hallazgo | Evidencia | Implicación para el modelo |
|---|---|---|---|
| 1 | | | |

Y una lista final: **variables candidatas para el modelo** (con la razón de cada una) y **variables que descartan** (con la razón).

### Entregable

- [ ] `notebooks/05_eda.ipynb` que corre de principio a fin
- [ ] 5 hallazgos con evidencia e implicación
- [ ] Hipótesis del *charter* marcadas como confirmadas, rechazadas o no concluyentes
- [ ] Lista de variables candidatas y descartadas
- [ ] PR unido a `main` (sin la carpeta `reports/`: está en el `.gitignore`)

### Reto opcional

Encuentren **una variable de confusión** en su dataset: una relación que cambia (o desaparece) cuando se controla por una tercera variable.

---

## Preguntas para la plenaria

1. ¿Qué hipótesis se cayó? ¿Qué aprendieron de eso?
2. ¿Qué hicieron con los *outliers*: los quitaron, los dejaron o los transformaron?
3. Muestren **una** gráfica que le explicarían a un gerente.

## Para la próxima sesión

Tengan claro el **tipo de problema** (regresión o clasificación) y la **métrica de éxito** del *charter*. En el **módulo 06** entrenarán el *baseline*.
