# Módulo 02: Business Intelligence y Analítica de Datos

> **Objetivo:** entender **para qué** hacemos analítica: convertir datos en **decisiones**. Aprender a definir KPIs y a distinguir los 4 tipos de análisis.

**Duración sugerida:** 2 horas · **Basado en:** `sesion_1_intro_bi.pdf` del profesor

## Contenido

| Archivo | Para qué sirve |
|---|---|
| `README.md` | Teoría paso a paso |
| `notebooks/01_kpis_y_tipos_de_analisis.ipynb` | Los 4 tipos de análisis aplicados a una inmobiliaria (House Prices) |
| `scripts/kpis.py` | Calcula una tabla de KPIs agrupada por la columna que elijas, para cualquier CSV |
| `ejercicios/EJERCICIOS.md` | Actividad en salas: problema y KPIs del equipo |
| `presentacion/02-BI-Analitica.pptx` | Diapositivas |

---

## 1. Del dato a la decisión

```
  Datos  ──>  Información  ──>  Conocimiento  ──>  Decisión
  "1460 filas"  "Precio mediano:  "Las casas de calidad  "Invertir en remodelaciones
                 USD 163.000"      9-10 cuestan 2.5×"      de cocina y acabados"
```

El dato por sí solo no vale nada. **Vale lo que cambia en una decisión.**

## 2. BI vs. Analítica de Datos (BA)

| Aspecto | Business Intelligence | Analítica de Datos |
|---|---|---|
| Pregunta | ¿Qué pasó? ¿Por qué pasó? | ¿Qué pasará? ¿Qué debo hacer? |
| Orientación | Reporte, monitoreo | Descubrimiento, predicción |
| Usuarios | Negocio, gerencia | Analistas, científicos de datos |
| Herramientas | Power BI, Tableau, Looker Studio, Excel | Python, R, SQL, scikit-learn |
| Entregable típico | Dashboard | Modelo, segmentación, recomendación |

> No compiten: **BI dice dónde mirar y la analítica profundiza.**

## 3. Arquitectura típica de BI y ETL

```
 Fuentes                 ETL                       Almacén              Consumo
 ERP, CRM, web,   ──>  Extract (extraer)   ──>   Data warehouse  ──>  Dashboards
 IoT, Excel…           Transform (limpiar)                              Reportes
                       Load (cargar)                                    Modelos
```

**Ejemplo de transformación:** unificar clientes duplicados ("Juan P." y "juan p"), convertir monedas, estandarizar fechas. Esto lo haremos con pandas en el módulo 04.

## 4. KPIs: indicadores clave de desempeño

Un **KPI** es un número que dice si vamos bien o mal frente a un objetivo. Un buen KPI es **SMART**:

| Letra | Significa | Pregunta |
|---|---|---|
| **S** | Específico | ¿Mide una sola cosa clara? |
| **M** | Medible | ¿Se puede calcular con los datos? |
| **A** | Alcanzable | ¿La meta es realista? |
| **R** | Relevante | ¿Le importa al negocio? |
| **T** | Temporal | ¿En qué periodo? |

| Área | KPI | Fórmula |
|---|---|---|
| Ventas | Ingreso total mensual | Σ ventas del mes |
| Marketing | Costo de adquisición de clientes (CAC) | gasto en marketing / clientes nuevos |
| Logística | Tasa de entregas a tiempo | entregas a tiempo / total de entregas |
| Inmobiliaria | Precio mediano por m² | mediana(precio / área) |

Incorrecto: "Mejorar las ventas". Correcto: "Aumentar el ingreso mensual en un 5 % frente al mismo mes del año anterior, durante el segundo semestre de 2026".

## 5. Los 4 tipos de análisis

```
 Valor ▲
       │                                    ┌──────────────┐
       │                       ┌──────────┐ │ Prescriptivo │ ¿Qué debo hacer?
       │          ┌──────────┐ │Predictivo│ └──────────────┘
       │ ┌──────┐ │Diagnóst. │ └──────────┘  ¿Qué pasará?
       │ │Descr.│ └──────────┘ ¿Por qué pasó?
       │ └──────┘ ¿Qué pasó?
       └────────────────────────────────────────────────> Complejidad
```

| Tipo | Pregunta | Técnicas | Ejemplo inmobiliario |
|---|---|---|---|
| **Descriptivo** | ¿Qué pasó? | Conteos, promedios, dashboards | "Se vendieron 1460 casas; precio mediano de USD 163.000" |
| **Diagnóstico** | ¿Por qué pasó? | *Drill-down*, segmentación, correlación | "2010 parece un mal año… ¡pero solo hay datos hasta julio!" |
| **Predictivo** | ¿Qué pasará? | Regresión, series de tiempo, ML | "Esta casa de 150 m² valdrá unos USD 180.000" |
| **Prescriptivo** | ¿Qué hago? | Optimización, simulación, reglas | "Remodelar la cocina sube el precio esperado en un X %" |

## 6. Cuidado con las trampas del análisis descriptivo

En el notebook vas a ver un ejemplo real: las ventas de 2010 "se desploman"… pero el dataset **termina en julio de 2010**. Antes de concluir, siempre pregunta:

1. ¿El periodo está completo?
2. ¿Estoy comparando grupos del mismo tamaño?
3. ¿La media está distorsionada por valores extremos? (usa la **mediana**)
4. ¿Correlación o causalidad?

## 7. Paso a paso en el notebook

1. Cargar House Prices y entenderlo como el **negocio** de una inmobiliaria.
2. **Descriptivo:** tarjetas de KPIs y ventas por año y por mes.
3. **Diagnóstico:** encontrar por qué 2010 "cae" y por qué unos barrios son más caros.
4. **Predictivo:** una primera regresión de una sola variable (adelanto del módulo 06).
5. **Prescriptivo:** convertir hallazgos en recomendaciones.

## 8. Script reutilizable

```bash
# KPIs de precio por barrio (por defecto usa House Prices)
uv run python 02-BI-Analitica/scripts/kpis.py --por Neighborhood

# Con el dataset de tu equipo
uv run python 02-BI-Analitica/scripts/kpis.py --csv ruta/datos.csv --valor ventas --por region
```

---

## Checklist del módulo

- [ ] Sé explicar la diferencia entre BI y analítica con un ejemplo
- [ ] Puedo clasificar una pregunta en uno de los 4 tipos de análisis
- [ ] Sé escribir un KPI SMART
- [ ] El equipo tiene tema, dataset candidato y 3 KPIs (Parte 2)

**Anterior:** [Módulo 01: Git](../01-Git-GitHub/) · **Siguiente:** [Módulo 03: CRISP-DM](../03-CRISP-DM/)
