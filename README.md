# Proyecto 1: Introducción a la Analítica

**Universidad de Medellín, Especialización en Analítica**

En este curso se construye un proyecto de ciencia de datos **de principio a fin**: se parte de una pregunta de negocio y se termina con un modelo evaluado y listo para usarse, siguiendo la metodología **CRISP-DM** y trabajando en equipo con **Git y GitHub**.


## Instructora

### **[María Camila Durango](https://www.linkedin.com/in/mar%C3%ADa-camila-durango-999224202/)**

MLOps Engineer y Software Engineer con 7 años de experiencia en desarrollo de producto. Trabaja en **Bancolombia** en desarrollo de software y arquitectura de sistemas de IA en producción.

## Objetivos del curso

Al finalizar serás capaz de:

- Configurar un **entorno reproducible** con `uv` y trabajar en equipo con **Git y GitHub**
- Traducir un **problema de negocio** en un objetivo de analítica con KPIs medibles
- Aplicar **CRISP-DM** de punta a punta
- **Limpiar, integrar y transformar** datos con criterio de negocio
- Hacer un **análisis exploratorio (EDA)** que genere hipótesis
- Entrenar y **evaluar modelos** con las métricas correctas y compararlos contra un *baseline*
- Empaquetar el preprocesamiento y el modelo en un **Pipeline** reproducible
- **Desplegar** el modelo como una **API REST** con FastAPI

## Mapa del curso

```
   ┌───────────────────────────── FUNDAMENTOS ──────────────────────────────┐
   │  00 Entornos (uv)   →   01 Git y GitHub                                │
   └────────────────────────────────────────────────────────────────────────┘
                                       │
   ┌─────────────────────────────── CRISP-DM ───────────────────────────────┐
   │  02 Del problema  →  03 Preparación  →  04 Modelado  →  05 Del modelo  │
   │     a los datos         y EDA             y métricas      al producto  │
   │     (negocio y          (limpieza y       (baseline y     (pipelines   │
   │     datos)              hallazgos)        métricas)       y API)       │
   └────────────────────────────────────────────────────────────────────────┘
                                       │
                               06 Proyecto final
```

| # | Módulo | Sesión | Qué aprenderás |
|---|--------|--------|----------------|
| | Introducción al curso | Lun 19 oct | Objetivos, metodología, fechas y equipos |
| 00 | [Entornos con uv](00-Entornos-uv/) | Mar 20 oct | Entornos virtuales, `pyproject.toml`, `uv.lock` y kernel de Jupyter |
| 01 | [Git y GitHub](01-Git-GitHub/) | Mié 21 oct | Repositorio del equipo, `pull`, `add`, `commit`, `push` y Conventional Commits |
| 02 | [Del problema a los datos](02-Problema-y-Datos/) | Lun 26 oct | BI y analítica, KPIs, tipos de análisis, CRISP-DM y calidad de los datos |
| 03 | [Preparación de datos y EDA](03-Preparacion-y-EDA/) | Mar 27 oct | Limpieza con criterio de negocio, *data leakage*, gráficos y hallazgos |
| 04 | [Modelado y métricas](04-Modelado-Metricas/) | Mié 28 oct | *Baseline*, regresión, clasificación, métricas y *overfitting* |
| | Trabajo autónomo | 29 oct al 10 nov | Avance intermedio el 4 de noviembre |
| 05 | [Del modelo al producto](05-Pipelines-y-API/) | Mié 11 nov | `Pipeline`, guardar el modelo y API con FastAPI (demostración) |
| 06 | [Proyecto final](06-Proyecto-Final/) | Mié 25 nov | Sustentación: plantilla, rúbrica, checklist y guía de la presentación |

## Cómo está organizado cada módulo

```
NN-Nombre-Modulo/
├── README.md              ← teoría explicada paso a paso (empieza aquí)
├── notebooks/             ← práctica guiada con House Prices
│   └── complementario/    ← para profundizar (no se ve en clase), cuando aplica
├── ejercicios/
│   ├── EJERCICIOS.md      ← práctica guiada y actividad en salas de Zoom
│   └── soluciones/        ← soluciones de los ejercicios guiados
└── presentacion/          ← diapositivas del módulo (.pptx)
```

Cada clase sigue el mismo formato: **explicación** (40 min), **práctica guiada** (15 min), **salas de Zoom** en equipos de 3 (45 min) y **plenaria** (10 min).

### El hilo del proyecto: un solo notebook por equipo

Desde el módulo 02, cada equipo construye su proyecto en **un solo notebook**, [`notebooks/proyecto_equipo.ipynb`](06-Proyecto-Final/plantilla/), dentro de su repositorio. En cada clase se completa una parte, y al final ese notebook es la base de la sustentación.

| Módulo | Sesión | Secciones del notebook del equipo | Lo usa |
|---|---|---|---|
| 00 | 20 oct | Proyecto `uv` del equipo con `pyproject.toml` y `uv.lock` | 01 |
| 01 | 21 oct | Repositorio en GitHub con los 3 integrantes | todos |
| 02 | 26 oct | 0. Configuración · 1. El problema · 2. Los datos | 03 |
| 03 | 27 oct | 3. Limpieza · 4. EDA | 04 |
| 04 | 28 oct | 5. Modelo | 05 |
| 05 | 11 nov | 6. Conclusiones · esquema de la presentación | 06 |
| 06 | 25 nov | Sustentación | |

### Dataset guía: House Prices (Ames, Iowa)

Los notebooks de los módulos usan **un mismo caso de punta a punta** para que se vea el ciclo completo: entender el problema (02) → limpiar y explorar (03) → modelar (04) → empaquetar y desplegar (05). Los datos ya están en `data/raw/`, así que no hay que descargar nada.

## Stack tecnológico

- **Python 3.14**: lenguaje principal
- **uv**: gestor de entornos y dependencias (todo el curso)
- **pandas / NumPy**: manipulación de datos
- **matplotlib / seaborn**: visualización
- **scikit-learn / XGBoost**: modelado
- **FastAPI / Pydantic / Uvicorn**: API REST
- **pytest**: pruebas
- **Git / GitHub**: control de versiones y colaboración

## Inicio rápido

```bash
# 1) Instalar uv (solo la primera vez)
#    macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
#    Windows (PowerShell)
#    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# 2) Clonar el repositorio
git clone <url-del-repo>
cd intro_analitica

# 3) Crear el entorno e instalar todo (uv descarga Python 3.14 si no lo tienes)
uv sync

# 4) Verificar que todo quedó bien
uv run python -V
uv run python -c "import pandas, sklearn; print(pandas.__version__, sklearn.__version__)"

# 5) Abrir los notebooks
uv run jupyter lab
```

> **No hace falta "activar" el entorno.** `uv run <comando>` ejecuta el comando dentro de `.venv` automáticamente. Si usas VS Code, selecciona el intérprete `.venv` (ver [módulo 00](00-Entornos-uv/)).

## Estructura del repositorio

```
intro_analitica/
├── README.md
├── pyproject.toml          ← dependencias del curso (uv)
├── uv.lock                 ← versiones exactas (se genera con `uv sync`)
├── .python-version         ← 3.14
├── data/
│   ├── raw/                ← datos originales (no se modifican nunca)
│   └── processed/          ← datos generados por los notebooks (ignorado por git)
├── models/                 ← modelos entrenados (ignorado por git)
├── src/intro_analitica/    ← funciones reutilizables (config, datos, limpieza, eda, métricas, pipeline)
├── 00-Entornos-uv/ … 06-Proyecto-Final/
```

## Prerrequisitos

- Python básico (variables, funciones, listas, diccionarios)
- Nociones de estadística descriptiva
- Disposición para experimentar y depurar errores

## Fuentes de datos para los proyectos

- [Datos Abiertos Colombia](https://www.datos.gov.co/)
- [UCI Machine Learning Repository](https://archive.ics.uci.edu/datasets)
- [Kaggle Datasets](https://www.kaggle.com/datasets)
- [Google Dataset Search](https://datasetsearch.research.google.com/)
- [Google Trends](https://trends.google.com/trends/)
