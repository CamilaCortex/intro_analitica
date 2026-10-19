# Ejercicios: Módulo 04, Preparación de datos

> **Roten los roles.**

---

## Parte 1: Ejercicios guiados (35 min, primera parte de la clase)

| Notebook | Ejercicio | Solución |
|---|---|---|
| `01_limpieza_integracion_transformacion.ipynb` | **Viajes:** join, fechas, monedas, destinos, imputación por grupo, costo por día | `soluciones/solucion_04_viajes.py` |
| `02_house_prices_preparacion.ipynb` | LotFrontage alternativo, `HasPool`/`GarageAge`, ordinales, reflexión | `soluciones/solucion_04_house_prices.py` |

**Actividad del profesor (5 min):** ¿qué harían con esta tabla? (está al final del notebook del módulo 03)

| ID | Fecha | Precio | Cliente | Ciudad |
|---|---|---|---|---|
| 1 | 2023/12/05 | 59.99 | Juan P. | Bogotá |
| 2 | 12-06-23 | NaN | Maria G | Bta |
| 3 | 2023/12/07 | -15 | | Medellin |
| 4 | 2023/12/05 | 89.90 | Carlos S. | bogotá |

---

## Parte 2: Salas de Zoom, la limpieza del dataset del equipo (60 min)

> **Objetivo:** escribir **el código de limpieza del proyecto** como funciones reutilizables, más un **registro de decisiones**.
> **Viene de:** `docs/02_perfil_inicial.md` (los problemas de calidad que encontraron en el módulo 03).
> **Va a:** módulo 05 (el EDA se hace sobre `data/processed/`).

### Paso 1: Repartir el trabajo (5 min)

Abran `docs/02_perfil_inicial.md` y repartan las columnas problemáticas en **tres grupos**, uno por integrante (por ejemplo: nulos, formatos/texto, duplicados/joins). Cada persona trabaja en **su propia rama**.

### Paso 2: Explorar en un notebook (20 min)

Cada integrante, en `notebooks/04_limpieza_<nombre>.ipynb`, para cada columna:

1. ¿**Por qué** falta o está mal el dato? (usen el diccionario si existe)
2. Prueben 2 alternativas y comparen (como `LotFrontage`: 0 vs. mediana por grupo).
3. Elijan una y escriban **en una frase** por qué.

### Paso 3: Pasar a funciones (20 min)

Creen `src/limpieza.py` con **una función por paso** (sigan el modelo de `src/intro_analitica/limpieza.py` del curso):

```python
"""Limpieza del dataset <nombre>. Cada función recibe un DataFrame y devuelve uno nuevo."""
import pandas as pd


def limpiar_fechas(df: pd.DataFrame) -> pd.DataFrame:
    """Convierte <columna> a datetime. Los formatos que no se pueden leer quedan como NaT."""
    df = df.copy()
    df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce")
    return df


def limpiar(df: pd.DataFrame) -> pd.DataFrame:
    """Pipeline completo de limpieza."""
    for paso in [limpiar_fechas]:   # ← agreguen sus funciones aquí
        df = paso(df)
    return df


if __name__ == "__main__":
    crudo = pd.read_csv("data/raw/<archivo>.csv")
    limpio = limpiar(crudo)
    limpio.to_csv("data/processed/<archivo>_limpio.csv", index=False)
    print(f"{crudo.shape} → {limpio.shape}")
```

> Para evitar conflictos, cada integrante agrega **sus** funciones y el último en hacer *merge* integra la lista de `limpiar()`.

Prueben: `uv run python src/limpieza.py`

### Paso 4: Registro de decisiones (15 min)

Creen `docs/03_decisiones_limpieza.md`:

```markdown
| Columna(s) | Problema | Decisión | Justificación | Responsable |
|---|---|---|---|---|
| | | | | |
```

### Entregable

- [ ] `src/limpieza.py` con funciones documentadas que se ejecuta de principio a fin
- [ ] `data/processed/<archivo>_limpio.csv` generado (¡pero **no** subido a git!)
- [ ] `docs/03_decisiones_limpieza.md` con al menos 5 decisiones justificadas
- [ ] Al menos 2 variables nuevas (*feature engineering*) con sentido de negocio
- [ ] 3 PR (uno por integrante) unidos a `main`

### Reto opcional

Escriban una prueba sencilla `tests/test_limpieza.py`:

```python
import pandas as pd
from src.limpieza import limpiar

def test_sin_nulos():
    df = limpiar(pd.read_csv("data/raw/<archivo>.csv"))
    assert df.isna().sum().sum() == 0
```

y ejecútenla con `uv run pytest`.

---

## Preguntas para la plenaria

1. ¿Cuál fue la decisión de limpieza más difícil? ¿Qué alternativas consideraron?
2. ¿Qué porcentaje de filas perdieron? ¿Es aceptable?
3. ¿Encontraron algún "nulo que significa algo" como el `PoolQC`?

## Para la próxima sesión

Tengan generado `data/processed/<archivo>_limpio.csv`. En el **módulo 05** harán el EDA sobre él.
