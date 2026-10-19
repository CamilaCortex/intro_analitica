# Módulo 04: Preparación de datos

> **Objetivo:** convertir datos "sucios" en un dataset confiable, **tomando cada decisión con criterio de negocio y dejándola documentada**.

**Duración sugerida:** 2 a 3 horas · **Basado en:** `sesion_3_preparacion_de_datos.ipynb` y `sesion_3_preparacion_de_datos_desarrollo.ipynb` del profesor · **Fase 3 de CRISP-DM**

## Contenido

| Archivo | Para qué sirve |
|---|---|
| `notebooks/01_limpieza_integracion_transformacion.ipynb` | Fundamentos con ejemplos pequeños: nulos, duplicados, fechas, *joins*, escalado, *encoding* + ejercicio de viajes |
| `notebooks/02_house_prices_preparacion.ipynb` | Caso real: los 19 tipos de nulos de House Prices, *feature engineering* y exportación |
| `scripts/preparar_house_prices.py` | La misma limpieza, ejecutable y repetible → `data/processed/house_prices_limpio.csv` |
| `../src/intro_analitica/limpieza.py` | Las funciones de limpieza (una por paso), documentadas |
| `ejercicios/EJERCICIOS.md` | Actividad en salas: la limpieza del dataset del equipo |
| `presentacion/04-Preparacion-Datos.pptx` | Diapositivas |

---

## 1. ¿Por qué importa tanto?

- *Garbage in, garbage out*: la calidad de los datos limita el mejor modelo posible.
- En proyectos reales, preparar los datos toma entre el **60 % y el 80 %** del tiempo.
- Cada decisión de limpieza **cambia los resultados**, así que debe ser explícita y reproducible.

## 2. Las tres tareas

```
  1. LIMPIEZA                2. INTEGRACIÓN             3. TRANSFORMACIÓN
  ─────────────              ───────────────            ─────────────────
  • Nulos                    • Joins (merge)            • Escalado (Standard, MinMax)
  • Duplicados               • Llaves distintas         • Encoding (one-hot, ordinal)
  • Formatos (fechas,        • Llaves compuestas        • Variables nuevas
    texto, monedas)          • Validar cardinalidad       (feature engineering)
  • Errores (precio < 0)
```

## 3. Paso a paso: ¿qué hago con un nulo?

```
                     ¿Por qué falta el dato?
                              │
        ┌─────────────────────┼──────────────────────┐
   "No existe"           "No se registró"       "Es inconsistente"
   (no tiene piscina)    (falla de captura)     (tiene sótano sin datos)
        │                     │                       │
   Codificar:            Imputar: mediana,       Eliminar la fila
   "No Pool", 0, -1      moda, por grupo…        (si son pocas)
```

| Estrategia | Cuándo | Cuidado con |
|---|---|---|
| Media | Simétrica, pocos nulos | *Outliers* |
| Mediana | Asimétrica (precios, ingresos) | Ignora otras variables |
| Moda | Categóricas | Infla la categoría más común |
| Valor fijo / centinela | El nulo **significa algo** | No usar el centinela en cálculos |
| Por grupo (`groupby().transform`) | El valor depende de otra variable | Grupos pequeños |
| Eliminar | Muy pocos y al azar | Sesgar la muestra |

## 4. Joins en una tabla

| `how=` | Conserva | Ejemplo |
|---|---|---|
| `inner` | Solo las llaves que están en ambas tablas | Clientes **con** ventas |
| `left` | Todo lo de la izquierda | Todos los clientes, tengan o no ventas |
| `right` | Todo lo de la derecha | Todas las ventas, aunque el cliente no exista |
| `outer` | Todo | Auditoría completa |

**Dos parámetros que te salvan:** `validate="one_to_many"` (avisa si la llave se repite donde no debería) e `indicator=True` (dice de qué tabla vino cada fila).

## 5. Transformaciones

| Transformación | Qué hace | ¿Lo necesitan los árboles? |
|---|---|---|
| `StandardScaler` | Deja media 0 y desviación 1 | No |
| `MinMaxScaler` | Deja los valores entre 0 y 1 | No |
| `OneHotEncoder` | Una columna 0/1 por categoría (sin orden) | Sí, hay que codificar |
| `OrdinalEncoder` | Categorías con orden → 0, 1, 2… (**tú das el orden**) | Sí |
| `LabelEncoder` | Pensado para el **target**, no para las variables de entrada | — |

## 6. *Data leakage* (fuga de información)

Los imputadores, escaladores y *encoders* **aprenden** de los datos. Si los ajustas con **todo** el dataset, el test "se filtra" en el entrenamiento y las métricas salen mejores de lo que serán en la realidad.

**Regla:** `fit` solo con train y `transform` en train y test. Los **Pipelines** (módulo 07) lo hacen automáticamente.

Por eso el script de este módulo **solo limpia** (reglas fijas que no aprenden de los datos) y deja el escalado y el *encoding* para el pipeline.

## 7. El caso House Prices en una tabla

| Columna(s) | Decisión | Por qué |
|---|---|---|
| `PoolQC`, `Alley`, `Fence`, `MiscFeature`, `FireplaceQu` | "No …" | Diccionario: NA = no tiene |
| `LotFrontage` | 0 | No hay ceros; se asume sin frente a la calle |
| `MasVnrArea` / `MasVnrType` | 0 / "None" | Sin área = sin enchape |
| `Bsmt*` | "No Basement" si `TotalBsmtSF == 0` | Nulos en bloque |
| `Garage*`, `GarageYrBlt` | "No Garage", -1 | Nulos en bloque; centinela |
| 8 filas inconsistentes | Eliminar | <1 % de los datos |
| **Nuevas:** `HouseAge`, `TotalSF`, `TotalBath`, `Remodeled`… | *Feature engineering* | Hablan el idioma del comprador |

## 8. Cómo ejecutar

```bash
# Generar data/processed/house_prices_limpio.csv
uv run python 04-Preparacion-Datos/scripts/preparar_house_prices.py

# Las soluciones
uv run python 04-Preparacion-Datos/ejercicios/soluciones/solucion_04_viajes.py
uv run python 04-Preparacion-Datos/ejercicios/soluciones/solucion_04_house_prices.py
```

---

## Checklist del módulo

- [ ] Antes de imputar, me pregunto **por qué** falta el dato
- [ ] Sé elegir el tipo de join y validarlo
- [ ] Sé cuándo escalar y cuándo no (árboles)
- [ ] Sé cuándo usar one-hot y cuándo ordinal
- [ ] Entiendo qué es el *data leakage* y por qué no escalo antes de dividir train/test
- [ ] El equipo tiene `src/limpieza.py` y su registro de decisiones

**Anterior:** [Módulo 03: CRISP-DM](../03-CRISP-DM/) · **Siguiente:** [Módulo 05: EDA](../05-EDA/)
