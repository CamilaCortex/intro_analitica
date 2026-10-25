# Módulo 03: Preparación de datos y análisis exploratorio (EDA)

> **Objetivo:** convertir datos "sucios" en un dataset confiable, **tomando cada decisión con criterio de negocio**, y luego hacerles **preguntas** a los datos para salir con hallazgos que guíen el modelo.

**Sesión:** martes 27 de octubre · **Fases de CRISP-DM:** 3. Preparación de los datos (y parte de la 2)

## Contenido

| Archivo | Para qué sirve |
|---|---|
| `README.md` | Teoría paso a paso (estás aquí) |
| `notebooks/01_preparacion_house_prices.ipynb` | Caso real: los nulos de House Prices, uno por uno, con su decisión y su justificación |
| `notebooks/02_eda_house_prices.ipynb` | EDA completo: target, univariado, bivariado, *outliers* y validación de hipótesis |
| `notebooks/complementario/limpieza_integracion_transformacion.ipynb` | Para profundizar: duplicados, fechas, *joins*, escalado y *encoding* con ejemplos pequeños |
| `../src/intro_analitica/limpieza.py` | Las funciones de limpieza de House Prices, una por paso |
| `../src/intro_analitica/eda.py` | `perfil_rapido`, `outliers_iqr`, `correlaciones_con_target`… |
| `ejercicios/EJERCICIOS.md` | Actividad de la clase: secciones 3 y 4 del notebook del equipo |
| `ejercicios/soluciones/` | Soluciones de los ejercicios guiados |
| `presentacion/03-Preparacion-y-EDA.pptx` | Diapositivas |

### Cómo se reparte la clase

| Bloque | Tiempo | Qué se hace |
|---|---|---|
| Explicación | 40 min | Presentación: nulos con criterio, *data leakage*, qué es un EDA y qué gráfico usar |
| Práctica guiada | 15 min | Recorrido por los notebooks y Parte 1 de los ejercicios |
| Salas de Zoom | 45 min | Parte 2: limpieza y EDA del proyecto del equipo |
| Plenaria | 10 min | Cada equipo comparte su hallazgo más interesante |

---

# Parte A: Preparación de los datos

## 1. ¿Por qué importa tanto?

- *Garbage in, garbage out*: la calidad de los datos limita al mejor modelo posible.
- En proyectos reales, preparar los datos toma entre el **60 % y el 80 %** del tiempo.
- Cada decisión de limpieza **cambia los resultados**, así que debe ser explícita y quedar escrita.

## 2. Las tareas más frecuentes

| Tarea | Ejemplo | Código en pandas |
|---|---|---|
| Quitar duplicados | La misma venta registrada dos veces | `df = df.drop_duplicates()` |
| Rellenar nulos | Área de garaje vacía | `df["col"] = df["col"].fillna(valor)` |
| Corregir tipos | `"1.500,00"` leído como texto | `pd.to_numeric(...)`, `pd.to_datetime(...)` |
| Unificar textos | `"Medellín"`, `"medellin "`, `"MEDELLÍN"` | `df["col"].str.strip().str.lower()` |
| Quitar valores imposibles | Precio negativo, edad de 200 años | `df = df[df["precio"] > 0]` |
| Crear variables | Edad de la casa a partir del año de construcción | `df["edad"] = df["YrSold"] - df["YearBuilt"]` |

## 3. Paso a paso: ¿qué hago con un nulo?

La pregunta no es *"¿con qué relleno?"* sino ***"¿por qué falta el dato?"***

```
                     ¿Por qué falta el dato?
                              │
        ┌─────────────────────┼──────────────────────┐
   "No existe"           "No se registró"       "Es inconsistente"
   (no tiene piscina)    (falla de captura)     (tiene sótano pero sin datos)
        │                     │                       │
   Codificar:            Imputar: mediana,       Eliminar la fila
   "No tiene", 0         moda, por grupo         (si son pocas)
```

| Estrategia | Cuándo | Cuidado con |
|---|---|---|
| Mediana | Números asimétricos (precios, ingresos) | Ignora otras variables |
| Media | Números simétricos, pocos nulos | Se distorsiona con *outliers* |
| Moda (el valor más frecuente) | Categorías | Infla la categoría más común |
| Valor fijo ("No tiene", 0) | El nulo **significa algo** | Leer el diccionario de datos |
| Por grupo (`groupby().transform`) | El valor depende de otra variable (el frente de un lote depende del barrio) | Grupos pequeños |
| Eliminar filas | Muy pocas y al azar | Sesgar la muestra |

## 4. El caso House Prices en una tabla

| Columna(s) | Decisión | Por qué |
|---|---|---|
| `PoolQC`, `Alley`, `Fence`, `MiscFeature`, `FireplaceQu` | "No …" | Diccionario: NA = no tiene |
| `LotFrontage` | 0 | No hay ceros en los datos; se asume sin frente a la calle |
| `MasVnrArea` / `MasVnrType` | 0 / "None" | Sin área = sin enchape |
| `Bsmt*` | "No Basement" si `TotalBsmtSF == 0` | Los nulos vienen en bloque |
| `Garage*`, `GarageYrBlt` | "No Garage", -1 | Nulos en bloque; -1 marca "no aplica" |
| 8 filas inconsistentes | Eliminar | Menos del 1 % de los datos |
| **Nuevas:** `HouseAge`, `TotalSF`, `TotalBath`, `Remodeled` | Crear variables | Hablan el idioma del comprador |

## 5. *Data leakage*: no limpiar con información del futuro

Algunas transformaciones **aprenden** de los datos: la mediana para imputar, la media para escalar, las categorías para codificar. Si se calculan con **todo** el dataset, la información de los datos de prueba se filtra en el entrenamiento y las métricas salen mejores de lo que serán en la realidad.

**Regla práctica para el proyecto:**

- En la **limpieza** (este módulo) usen reglas fijas que no dependen de otras filas: "NA significa no tiene", "precio > 0", "quitar duplicados".
- Las imputaciones con mediana o moda de las **variables del modelo**, el escalado y el *encoding* los hace el notebook del equipo **en la sección 5**, aprendiendo solo de los datos de entrenamiento.

---

# Parte B: Análisis exploratorio (EDA)

## 6. ¿Qué es (y qué no es) un EDA?

| No es | Sí es |
|---|---|
| 50 gráficas sin conclusión | 3 a 7 hallazgos con evidencia |
| Mirar los datos "a ver qué sale" | Partir de **preguntas e hipótesis** (las del módulo 02) |
| Un paso que se hace una vez | Algo iterativo: cada hallazgo genera nuevas preguntas |

## 7. El recorrido, paso a paso

```
 1. OBJETIVO        2. UNIVARIADO       3. BIVARIADO          4. OUTLIERS          5. HIPÓTESIS
 ¿Cómo se           Cada variable       Cada variable frente  ¿Error o realidad?   Confirmar o rechazar
 distribuye?        sola                al objetivo           Detectar ≠ eliminar  con evidencia
```

## 8. ¿Qué gráfico uso?

| Pregunta | Tipo de variable | Gráfico | seaborn |
|---|---|---|---|
| ¿Cómo se distribuye? | Numérica | Histograma | `sns.histplot` |
| ¿Cómo se distribuye? | Categórica | Barras | `sns.countplot` |
| ¿Se relaciona con el objetivo? | Numérica frente a numérica | Dispersión (*scatter*) | `sns.scatterplot` |
| ¿Se relaciona con el objetivo? | Categórica frente a numérica | Boxplot ordenado por mediana | `sns.boxplot` |
| ¿Hay *outliers*? | Numérica | Boxplot | `sns.boxplot` |
| ¿Cómo se relacionan todas? | Numéricas | Mapa de calor de correlación | `sns.heatmap` |
| ¿Cambia con el tiempo? | Fecha | Línea | `sns.lineplot` |

## 9. Conceptos clave

- **Asimetría:** si la cola es larga a la derecha (precios, ingresos), la media es mayor que la mediana. El logaritmo suele "enderezarla".
- **Correlación (r):** mide la relación **lineal** entre -1 y 1. Que r ≈ 0 **no** significa que no haya ninguna relación.
- **Regla IQR:** se marca como *outlier* lo que queda fuera de `[Q1 − 1.5·IQR, Q3 + 1.5·IQR]`. Es una **alerta** para revisar, no una orden de eliminar.
- **Variable de confusión:** una tercera variable que esconde o crea una relación. En House Prices, "remodelada" parece no influir en el precio, pero **comparando casas de la misma edad** sí suma entre un 5 % y un 12 %.

## 10. Hallazgos de House Prices (resumen del notebook 2)

| # | Hallazgo | Implicación para el modelo |
|---|---|---|
| 1 | El precio es asimétrico; con logaritmo queda casi simétrico | Probar `log(SalePrice)` |
| 2 | `OverallQual` (r = 0.79), `TotalSF` (0.78) y `GrLivArea` (0.71) son las más relacionadas | Variables imprescindibles |
| 3 | El barrio suma hasta un 46 % al precio a igual calidad | Incluir `Neighborhood` |
| 4 | `KitchenQual` es escalonada (Fa < TA < Gd < Ex) | Tratarla como ordinal |
| 5 | 2 casas gigantes y baratas (ventas parciales en `Edwards`) | Evaluar el modelo con y sin ellas |

## 11. Un hallazgo bien escrito

Un hallazgo tiene tres partes: **qué** se encontró, **con qué evidencia** y **qué implica**.

- Débil: "Hicimos un boxplot del precio por calidad."
- Bueno: "Las casas de calidad 9-10 cuestan casi el triple que las de calidad 5 (boxplot de precio por calidad). La calidad debe entrar al modelo, y conviene revisar cómo se asigna en los avalúos."

---

## Para profundizar (opcional)

El notebook `complementario/limpieza_integracion_transformacion.ipynb` cubre temas que no alcanzamos a ver en clase y que pueden necesitar en el proyecto:

- **Integración de tablas** con `pd.merge` (`inner`, `left`, `right`, `outer`) y los parámetros `validate` e `indicator`, que avisan si una llave se repite donde no debería.
- **Escalado** (`StandardScaler`, `MinMaxScaler`) y **codificación** de categóricas (`OneHotEncoder`, `OrdinalEncoder`).
- Fechas y textos con formatos distintos.

Su solución está en `ejercicios/soluciones/solucion_complementario_viajes.py`.

## Checklist del módulo

- [ ] Antes de rellenar un nulo, me pregunto **por qué** falta el dato
- [ ] Sé explicar qué es el *data leakage*
- [ ] Empiezo el EDA por la variable objetivo
- [ ] Sé elegir el gráfico según el tipo de variable
- [ ] Distingo *detectar* un *outlier* de *eliminarlo*
- [ ] El equipo tiene su registro de limpieza y 3 hallazgos en el notebook

**Anterior:** [Módulo 02: Del problema a los datos](../02-Problema-y-Datos/) · **Siguiente:** [Módulo 04: Modelado y métricas](../04-Modelado-Metricas/)
