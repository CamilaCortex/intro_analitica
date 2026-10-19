# Módulo 05: Análisis exploratorio de datos (EDA)

> **Objetivo:** hacerle **preguntas** a los datos, validar hipótesis y salir con una lista justificada de variables para el modelo.

**Duración sugerida:** 2 horas · **Basado en:** la sección EDA de `sesion_3_preparacion_de_datos_desarrollo.ipynb` del profesor · **Fase 2 (y parte de la 3) de CRISP-DM**

## Contenido

| Archivo | Para qué sirve |
|---|---|
| `notebooks/01_eda_house_prices.ipynb` | EDA completo: target, univariado, bivariado, *outliers* y validación de 4 hipótesis |
| `scripts/reporte_eda.py` | EDA automático (figuras + `resumen.md`) para **cualquier** CSV |
| `../src/intro_analitica/eda.py` | `perfil_rapido`, `outliers_iqr`, `correlaciones_con_target`… |
| `ejercicios/EJERCICIOS.md` | Actividad en salas: el EDA del proyecto del equipo |
| `presentacion/05-EDA.pptx` | Diapositivas |

---

## 1. ¿Qué es (y qué no es) un EDA?

| No es | Sí es |
|---|---|
| 50 gráficas sin conclusión | 5-7 hallazgos con evidencia |
| Mirar los datos "a ver qué sale" | Partir de **preguntas e hipótesis** |
| Un paso que se hace una vez | Algo iterativo: cada hallazgo genera nuevas preguntas |

## 2. El recorrido, paso a paso

```
 1. TARGET            2. UNIVARIADO         3. BIVARIADO            4. OUTLIERS          5. HIPÓTESIS
 ¿Qué predigo?        Cada variable         Cada variable           ¿Error o realidad?   confirmar o rechazar con evidencia
 ¿Cómo se             sola: forma,          frente al target:       Detectar ≠
 distribuye?          rango, categorías     correlación, boxplots   eliminar
                                                                         │
                                                         6. CONCLUSIONES → variables para el modelo
```

## 3. ¿Qué gráfico uso?

| Pregunta | Tipo de variable | Gráfico |
|---|---|---|
| ¿Cómo se distribuye? | Numérica | Histograma, KDE, violín |
| ¿Cómo se distribuye? | Categórica | Barras (`value_counts`) |
| ¿Se relaciona con el target? | Numérica vs. numérica | *Scatter* + línea (`regplot`), correlación |
| ¿Se relaciona con el target? | Categórica vs. numérica | Boxplot / violín **ordenado por mediana** |
| ¿Hay *outliers*? | Numérica | Boxplot, regla IQR, *scatter* |
| ¿Cómo se relacionan todas? | Numéricas | *Heatmap* de correlación |
| ¿Cambia con el tiempo? | Fecha | Línea |

## 4. Conceptos clave

- **Asimetría (*skew*):** si la cola es larga a la derecha, la media es mayor que la mediana. El logaritmo suele "enderezarla".
- **Correlación de Pearson (r):** mide la relación **lineal** entre -1 y 1. Que r ≈ 0 **no** significa que no haya relación.
- **Multicolinealidad:** dos variables casi iguales (r ≈ ±1). En modelos lineales sobra una.
- **Regla IQR:** es *outlier* lo que está fuera de `[Q1 − 1.5·IQR, Q3 + 1.5·IQR]`. Es una **alerta**: en variables discretas marca demasiados casos.
- **Variable de confusión:** una tercera variable que esconde o crea una relación. En House Prices, "remodelada" parece no influir (r ≈ 0), pero **comparando casas de la misma edad** sí suma entre un 5 % y un 12 %.

## 5. Hallazgos de House Prices (resumen del notebook)

| # | Hallazgo | Implicación |
|---|---|---|
| 1 | Target asimétrico (≈ 1.9); con log ≈ 0.1 | Probar `log(SalePrice)` |
| 2 | `OverallQual` (0.79), `TotalSF` (0.78), `GrLivArea` (0.71) | Variables imprescindibles |
| 3 | El barrio suma hasta un 46 % a igual calidad | Incluir `Neighborhood` |
| 4 | `KitchenQual` escalonada (Fa < TA < Gd < Ex) | Ordinal |
| 5 | `HouseAge` ≈ `YearBuilt` (r ≈ -1) | Usar solo una en modelos lineales |
| 6 | 2 casas gigantes y baratas (`Edwards`, `Partial`) | Evaluar con y sin ellas |

## 6. Cómo ejecutar

```bash
# Primero, los datos limpios del módulo 04
uv run python 04-Preparacion-Datos/scripts/preparar_house_prices.py

# EDA automático → reports/eda_house_prices_limpio/
uv run python 05-EDA/scripts/reporte_eda.py data/processed/house_prices_limpio.csv --target SalePrice

# Soluciones
uv run python 05-EDA/ejercicios/soluciones/solucion_05.py
```

---

## Checklist del módulo

- [ ] Empiezo el EDA por el target
- [ ] Sé elegir el gráfico según el tipo de variable
- [ ] Distingo *detectar* un *outlier* de *eliminarlo*
- [ ] Valido hipótesis **controlando** por otras variables cuando hace falta
- [ ] El equipo tiene su EDA con 5 hallazgos y sus implicaciones

**Anterior:** [Módulo 04: Preparación](../04-Preparacion-Datos/) · **Siguiente:** [Módulo 06: Modelado](../06-Modelado-Metricas/)
