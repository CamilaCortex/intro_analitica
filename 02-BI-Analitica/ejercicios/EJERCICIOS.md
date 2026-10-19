# Ejercicios: Módulo 02, BI y Analítica

> **Roten los roles:** el relator anterior ahora es piloto.

---

## Parte 1: Ejercicios guiados (15 min, primera parte de la clase)

Están al final del notebook `notebooks/01_kpis_y_tipos_de_analisis.ipynb`:

1. KPI de precio mediano por m² por año.
2. Diagnóstico de `SaleCondition`.
3. Clasificar 4 preguntas en descriptivo, diagnóstico, predictivo o prescriptivo.

Soluciones en `soluciones/solucion_02.py`.

### Mini-actividad de dashboards (10 min)

Entren a la [galería de Tableau Public](https://public.tableau.com/app/discover/viz-of-the-day) o a la de [Power BI](https://community.fabric.microsoft.com/t5/Data-Stories-Gallery/bd-p/DataStoriesGallery) y elijan un dashboard:

- **Descriptivo:** ¿qué conclusiones se pueden sacar?
- **Diagnóstico:** ¿qué pudo motivar esos resultados? ¿Qué dato les falta para confirmarlo?

---

## Parte 2: Salas de Zoom, el problema y los KPIs del equipo (50 min)

> **Objetivo:** elegir el **tema y el dataset** del proyecto y definir **3 KPIs SMART**.
> **Viene de:** módulo 01 (el repositorio del equipo).
> **Va a:** módulo 03 (el *project charter* parte de este documento).

### Paso 1: Elegir el tema (15 min)

Cada integrante presenta en 1 minuto el tema y el dataset que trajo. Luego evalúen cada opción:

| Criterio | Pregunta | Opción A | Opción B | Opción C |
|---|---|---|---|---|
| Negocio | ¿Hay una decisión real que mejoraría? | | | |
| Datos | ¿Más de 500 filas? ¿Tiene una variable objetivo clara? | | | |
| Acceso | ¿Se puede descargar hoy mismo, sin pedir permisos? | | | |
| Interés | ¿Nos motiva trabajarlo durante el semestre? | | | |

Califiquen de 1 a 3 y elijan la opción con mayor puntaje.

> **Fuentes recomendadas:** [datos.gov.co](https://www.datos.gov.co/), [UCI](https://archive.ics.uci.edu/datasets), [Kaggle](https://www.kaggle.com/datasets).
> Eviten datasets de más de 50 MB (no caben en GitHub) o que exijan datos personales.

### Paso 2: Explorar 10 minutos (10 min)

El piloto descarga el dataset en `data/raw/` y corre:

```bash
uv run python <ruta>/intro_analitica/02-BI-Analitica/scripts/kpis.py \
    --csv data/raw/<archivo>.csv --valor <columna_numerica> --por <columna_categorica>
```

¿El resultado tiene sentido? ¿Hay algo que les sorprenda?

### Paso 3: Escribir el documento (25 min)

Creen `docs/01_problema_y_kpis.md` en una rama `docs/problema-kpis` con esta plantilla:

```markdown
# Problema y KPIs

## Tema
<una frase>

## Dataset
- Fuente: <enlace>
- Descargado el: <fecha>
- Tamaño: <filas> × <columnas>
- ¿Qué representa una fila?: <p.ej. "una venta", "un cliente-mes">

## ¿Quién toma la decisión y cuál es?
<p.ej. "El área comercial decide a qué clientes ofrecer un descuento">

## Preguntas por tipo de análisis
| Tipo | Pregunta |
|---|---|
| Descriptivo | |
| Diagnóstico | |
| Predictivo | |
| Prescriptivo | |

## KPIs (SMART)
| KPI | Fórmula | Meta | Periodo | Columnas que usa |
|---|---|---|---|---|
| | | | | |
| | | | | |
| | | | | |

## Primer cálculo
<pegar la salida de kpis.py y una conclusión de 2 líneas>
```

Abran el PR y que **otro integrante** lo apruebe.

### Entregable

- [ ] Dataset en `data/raw/` (si pesa menos de 50 MB) o, si es más grande, instrucciones de descarga en el README
- [ ] `docs/01_problema_y_kpis.md` completo, con una pregunta por cada tipo de análisis
- [ ] 3 KPIs SMART con fórmula y columnas
- [ ] PR unido a `main`

### Reto opcional

Hagan un "dashboard" de una sola figura en un notebook (`notebooks/00_kpis.ipynb`): 3 tarjetas de KPI y una gráfica de tendencia.

---

## Preguntas para la plenaria

1. ¿Qué tema eligieron y por qué descartaron los otros?
2. Lean su KPI favorito. El grupo responde: ¿es SMART?
3. ¿Encontraron alguna "trampa" como la de 2010 (periodos incompletos, grupos de distinto tamaño)?

## Para la próxima sesión

Lean el diccionario de datos de su dataset (si existe). En el **módulo 03** harán el *project charter* y el perfil inicial de los datos.
