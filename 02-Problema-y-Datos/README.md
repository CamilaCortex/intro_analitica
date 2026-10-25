# Módulo 02: Del problema a los datos

> **Objetivo:** antes de escribir una línea de código de modelos, saber **qué problema** resuelve el proyecto, **cómo se medirá el éxito** y **qué tan buenos son los datos** para lograrlo.

**Sesión:** lunes 26 de octubre · **Fases de CRISP-DM:** 1. Comprensión del negocio y 2. Comprensión de los datos

## Contenido

| Archivo | Para qué sirve |
|---|---|
| `README.md` | Teoría paso a paso (estás aquí) |
| `notebooks/01_kpis_y_tipos_de_analisis.ipynb` | KPIs y los 4 tipos de análisis aplicados a una inmobiliaria (House Prices) |
| `notebooks/02_comprension_negocio_y_datos.ipynb` | Fases 1 y 2 de CRISP-DM con House Prices: objetivo, diccionario, nulos, target e hipótesis |
| `ejercicios/EJERCICIOS.md` | Actividad de la clase: secciones 1 y 2 del notebook del equipo |
| `ejercicios/soluciones/` | Soluciones de los ejercicios guiados de los notebooks |
| `presentacion/02-Problema-y-Datos.pptx` | Diapositivas |

### Cómo se reparte la clase

| Bloque | Tiempo | Qué se hace |
|---|---|---|
| Explicación | 40 min | Presentación: BI y analítica, KPIs, tipos de análisis y CRISP-DM |
| Práctica guiada | 15 min | Recorrido por los notebooks y Parte 1 de los ejercicios |
| Salas de Zoom | 45 min | Parte 2: el problema y los datos del proyecto del equipo |
| Plenaria | 10 min | Cada equipo presenta su problema en 1 minuto |

---

## 1. Del dato a la decisión

```
  Datos  ──>  Información  ──>  Conocimiento  ──>  Decisión
  "1460 filas"  "Precio mediano:  "Las casas de calidad  "Remodelar cocina y
                 USD 163.000"      9-10 cuestan 2.5×"      acabados antes de vender"
```

El dato por sí solo no vale nada. **Vale lo que cambia en una decisión.** Por eso todo proyecto empieza con una pregunta: *¿qué decisión queremos mejorar y quién la toma?*

## 2. BI y analítica de datos

| Aspecto | Business Intelligence (BI) | Analítica de datos |
|---|---|---|
| Pregunta | ¿Qué pasó? ¿Por qué pasó? | ¿Qué pasará? ¿Qué debo hacer? |
| Orientación | Reporte y monitoreo | Descubrimiento y predicción |
| Herramientas | Power BI, Tableau, Looker Studio, Excel | Python, R, SQL, scikit-learn |
| Entregable típico | Dashboard | Modelo, segmentación, recomendación |

No compiten: **BI dice dónde mirar y la analítica profundiza.**

## 3. KPIs: medir lo que importa

Un **KPI** (indicador clave de desempeño) es un número que dice si vamos bien o mal frente a un objetivo. Un buen KPI es **SMART**:

| Letra | Significa | Pregunta de control |
|---|---|---|
| **S** | Específico | ¿Mide una sola cosa clara? |
| **M** | Medible | ¿Se puede calcular con los datos que tenemos? |
| **A** | Alcanzable | ¿La meta es realista? |
| **R** | Relevante | ¿Le importa al negocio? |
| **T** | Temporal | ¿En qué periodo se mide? |

- Incorrecto: "Mejorar las ventas".
- Correcto: "Aumentar el ingreso mensual un 5 % frente al mismo mes del año anterior, durante el segundo semestre de 2026".

| Área | KPI | Fórmula |
|---|---|---|
| Ventas | Ingreso total mensual | suma de las ventas del mes |
| Marketing | Costo de adquisición de clientes | gasto en marketing / clientes nuevos |
| Logística | Tasa de entregas a tiempo | entregas a tiempo / total de entregas |
| Inmobiliaria | Precio mediano por m² | mediana(precio / área) |

En pandas, casi todos los KPIs se calculan con `groupby`: **agrupar** por una columna y **resumir** otra.

```python
df.groupby("Neighborhood")["SalePrice"].median()   # precio mediano por barrio
```

## 4. Los 4 tipos de análisis

| Tipo | Pregunta | Técnicas | Ejemplo inmobiliario |
|---|---|---|---|
| **Descriptivo** | ¿Qué pasó? | Conteos, promedios, dashboards | "Se vendieron 1460 casas; precio mediano de USD 163.000" |
| **Diagnóstico** | ¿Por qué pasó? | Segmentación, comparación de grupos, correlación | "2010 parece un mal año… pero solo hay datos hasta julio" |
| **Predictivo** | ¿Qué pasará? | Regresión, clasificación, series de tiempo | "Esta casa de 150 m² valdrá unos USD 180.000" |
| **Prescriptivo** | ¿Qué hago? | Optimización, simulación, reglas | "Remodelar la cocina sube el precio esperado un X %" |

Cada tipo agrega valor sobre el anterior, pero también complejidad. Un proyecto puede ser solo descriptivo y diagnóstico (un dashboard bien pensado) y ser muy útil.

### Antes de concluir, pregunta

1. ¿El periodo está **completo**? (la lección de 2010 en el notebook 1)
2. ¿Los grupos son **comparables**? (mismo tamaño, mismo periodo)
3. ¿La media está distorsionada por valores extremos? Usa la **mediana**.
4. ¿Es **correlación o causalidad**? Que dos cosas se muevan juntas no significa que una cause la otra.

## 5. CRISP-DM: el mapa del proyecto

**CRISP-DM** (*Cross-Industry Standard Process for Data Mining*) es la metodología más usada en proyectos de datos porque está **orientada al negocio** y es repetible. Tiene 6 fases, y volver a una fase anterior es normal: la iteración es parte del método.

```
   1. Negocio ──> 2. Datos ──> 3. Preparación ──> 4. Modelado ──> 5. Evaluación ──> 6. Despliegue
        ^            |              ^                  |               |
        └────────────┘              └──────────────────┘               |
        └──────────────────────────────────────────────────────────────┘
```

| Fase | Pregunta | Dónde la vemos en el curso |
|---|---|---|
| 1. Comprensión del negocio | ¿Qué problema resolvemos y cómo sabremos que lo logramos? | **Este módulo** |
| 2. Comprensión de los datos | ¿Qué datos tenemos y qué tan buenos son? | **Este módulo** |
| 3. Preparación de los datos | ¿Cómo los dejamos listos para analizar? | Módulo 03 |
| 4. Modelado | ¿Qué modelo usamos y con qué métrica? | Módulo 04 |
| 5. Evaluación | ¿Cumple el objetivo de **negocio**? | Módulos 04 y 05 |
| 6. Despliegue | ¿Cómo lo usa alguien en el día a día? | Módulo 05 |

> Los proyectos de datos rara vez fallan por el algoritmo. Fallan porque se resolvió el problema equivocado, porque los datos no servían y nadie lo notó a tiempo, o porque el modelo nunca se usó. Las fases 1 y 2 existen para evitarlo.

## 6. Fase 1: del negocio a un objetivo medible

El paso clave es **traducir** el problema de negocio en un objetivo de ciencia de datos con un **criterio de éxito** definido **antes** de modelar.

| Nivel | Ejemplo: retención de clientes | Ejemplo: inmobiliaria (el del curso) |
|---|---|---|
| Problema de negocio | Se están yendo muchos clientes | Los avalúos tardan y son poco consistentes |
| Objetivo de ciencia de datos | Predecir la probabilidad de que un cliente se vaya | Estimar el precio de venta (`SalePrice`) |
| Tipo de problema | Clasificación | Regresión |
| Criterio de éxito | Reducir la pérdida de clientes un 10 % en 3 meses | Error porcentual medio (MAPE) menor al 15 % |

Si el proyecto es descriptivo (un dashboard), la "variable objetivo" es el KPI principal y el criterio de éxito es la pregunta que el dashboard debe responder.

## 7. Fase 2: conocer los datos

Revisión mínima de cualquier dataset, en este orden:

1. **¿Qué representa una fila?** Es la primera pregunta, siempre. Define qué es un duplicado y cómo se agregan los datos.
2. **Diccionario de datos:** qué significa cada columna y en qué unidades está.
3. **Tipos:** ¿pandas leyó como texto una columna que debería ser numérica? (comas decimales, símbolos de moneda, "N/A")
4. **Nulos:** cuántos y **por qué** faltan. En House Prices, `PoolQC` tiene 99.5 % de nulos porque NA significa "no tiene piscina", no "dato perdido".
5. **Valores únicos:** pocos sugieren una categoría; todos distintos sugieren un identificador.
6. **La variable objetivo:** su distribución (regresión) o cuántos casos hay de cada clase (clasificación).
7. **Hipótesis:** qué creemos que explica la variable objetivo. Se validan en el EDA del módulo 03.

> **Cuidado con el *data leakage* (fuga de información):** no usen columnas que solo se conocen **después** del resultado. Por ejemplo, "fecha de cancelación" para predecir si un cliente cancela. El modelo se verá excelente en las pruebas y fallará en la realidad.

## 8. El notebook del proyecto del equipo

Desde esta clase, cada equipo trabaja su proyecto en un solo notebook: **`notebooks/proyecto_equipo.ipynb`**, que se copia de [`06-Proyecto-Final/plantilla/`](../06-Proyecto-Final/plantilla/). Tiene 6 secciones, una o dos por clase, y al final es la base de la sustentación. Hoy se llenan las secciones 0, 1 y 2. Las instrucciones están en [`ejercicios/EJERCICIOS.md`](ejercicios/EJERCICIOS.md).

## 9. Paso a paso en los notebooks del módulo

**Notebook 1, KPIs y tipos de análisis:**

1. Cargar House Prices y verlo como el **negocio** de una inmobiliaria.
2. **Descriptivo:** KPIs y ventas por año y por mes.
3. **Diagnóstico:** por qué 2010 "cae" y por qué unos barrios son más caros.
4. **Predictivo:** una primera regresión con una sola variable (adelanto del módulo 04).
5. **Prescriptivo:** convertir hallazgos en recomendaciones.

**Notebook 2, comprensión del negocio y de los datos:**

1. **Fase 1:** el problema de la inmobiliaria en forma de objetivo y criterio de éxito.
2. **Fase 2:** dimensiones, diccionario, tipos, nulos, cardinalidad y variable objetivo.
3. Problemas de calidad e hipótesis.

---

## Para profundizar (opcional)

- Comparación de metodologías: KDD (académica), SEMMA (orientada a SAS) y CRISP-DM (orientada al negocio).
- Despliegue **en tiempo real** (una API responde a cada solicitud) frente a **por lotes** (se procesan muchos registros cada día o cada semana). Lo veremos en el módulo 05.
- Galerías de dashboards para inspirarse: [Tableau Public](https://public.tableau.com/app/discover/viz-of-the-day) y [Power BI Data Stories](https://community.fabric.microsoft.com/t5/Data-Stories-Gallery/bd-p/DataStoriesGallery).

## Checklist del módulo

- [ ] Sé explicar la diferencia entre BI y analítica con un ejemplo
- [ ] Puedo clasificar una pregunta en uno de los 4 tipos de análisis
- [ ] Sé escribir un KPI SMART
- [ ] Sé nombrar las 6 fases de CRISP-DM
- [ ] El equipo tiene problema, criterio de éxito, KPIs y perfil del dataset en su notebook

**Anterior:** [Módulo 01: Git y GitHub](../01-Git-GitHub/) · **Siguiente:** [Módulo 03: Preparación de datos y EDA](../03-Preparacion-y-EDA/)
