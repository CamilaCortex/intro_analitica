# Ejercicios: Módulo 03, CRISP-DM

> **Roten los roles.**

---

## Parte 1: Ejercicios guiados (20 min, primera parte de la clase)

1. Los 4 ejercicios del final de `notebooks/01_comprension_negocio_y_datos.ipynb` (soluciones en `soluciones/solucion_03.py`).
2. **Actividad del profesor (5 min, en parejas):** caso e-commerce de moda. Si el modelo tiene AUC = 0.84, ¿qué riesgos ven? ¿Dónde podría fallar el proyecto?
3. **Discusión:** ¿qué pesa más, el desempeño o la interpretabilidad? Den un ejemplo donde gane cada uno.

---

## Parte 2: Salas de Zoom, *charter* y perfil del dataset del equipo (50 min)

> **Objetivo:** dejar por escrito **qué** van a resolver, **cómo** sabrán que lo lograron y **qué tan buenos** son sus datos.
> **Viene de:** `docs/01_problema_y_kpis.md` (módulo 02).
> **Va a:** módulo 04 (la limpieza ataca los problemas que encuentren hoy).

### Paso 1: Project charter (25 min)

1. Creen la rama `docs/charter`.
2. Copien la plantilla:
   ```bash
   cp <ruta>/intro_analitica/03-CRISP-DM/plantillas/project_charter.md docs/02_project_charter.md
   ```
3. Llénenla **entre los tres**. Las secciones más importantes son:
   - **2. Objetivo:** negocio → ciencia de datos → tipo de problema → variable objetivo.
   - **3. Criterios de éxito:** un KPI de negocio **y** una métrica del modelo con su umbral.
   - **6. Riesgos:** al menos 3.

> Si su problema es descriptivo (un dashboard), la "variable objetivo" es el KPI principal y el criterio de éxito es la pregunta que el dashboard debe responder.

### Paso 2: Perfil inicial (15 min)

```bash
uv run python <ruta>/intro_analitica/03-CRISP-DM/scripts/perfil_inicial.py \
    data/raw/<archivo>.csv --salida docs/02_perfil_inicial.md
# Si el CSV usa ";" como separador (frecuente en datos.gov.co):  --sep ";"
```

Abran `docs/02_perfil_inicial.md` y completen al final:

- **3 problemas de calidad** que encontraron (nulos, tipos mal leídos, categorías repetidas…).
- **3 hipótesis** que quieran validar en el EDA.

### Paso 3: Comprobación de realidad (10 min)

Respondan en el charter, en una sección nueva llamada **"9. Comprobación de realidad"**:

1. ¿La variable objetivo existe en los datos tal cual o hay que construirla?
2. ¿Tienen suficientes filas por grupo? (p.ej. si quieren predecir por municipio, ¿hay datos de todos?)
3. ¿Hay columnas que **no estarían disponibles al momento de predecir**? (*data leakage*: p.ej. usar "fecha de cancelación" para predecir si el cliente cancela)

### Entregable

- [ ] `docs/02_project_charter.md` completo (secciones 1 a 9)
- [ ] `docs/02_perfil_inicial.md` con 3 problemas y 3 hipótesis
- [ ] PR revisado por otro integrante y unido a `main`

### Reto opcional

Escriban el *charter* en versión "de ascensor": **3 frases** que le dirían a un gerente en 30 segundos. Pónganlo al inicio del README.

---

## Preguntas para la plenaria

1. Lean su objetivo de ciencia de datos y su criterio de éxito. ¿El grupo entiende **cómo** van a medirlo?
2. ¿Qué riesgo les preocupa más?
3. ¿Alguien encontró posibles casos de *data leakage*?

## Para la próxima sesión

Traigan identificados los problemas de calidad del perfil. En el **módulo 04** escribirán el código que los resuelve.
