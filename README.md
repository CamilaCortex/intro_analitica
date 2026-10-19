# Proyecto 1: Introducción a la Analítica

**Universidad de Medellín, Especialización en Analítica**

En este curso se construye un proyecto de ciencia de datos **de principio a fin**: se parte de una pregunta de negocio y se termina con un modelo disponible como API, siguiendo la metodología **CRISP-DM** y trabajando en equipo con **Git y GitHub**.


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
   ┌──────────────── FUNDAMENTOS ────────────────┐
   │  00 Entornos (uv)   →   01 Git y GitHub     │
   └─────────────────────────────────────────────┘
                         │
   ┌──────────────────── CRISP-DM ─────────────────────────────────────┐
   │ 02 BI y Analítica → 03 CRISP-DM → 04 Preparación → 05 EDA         │
   │       (negocio)       (datos)       (limpieza)      (hipótesis)   │
   │                                         │                         │
   │               06 Modelado → 07 Pipelines → 08 API (FastAPI)       │
   │               (métricas)    (reproducible)   (despliegue)         │
   └───────────────────────────────────────────────────────────────────┘
                         │
                 09 Proyecto final
```

| # | Módulo | Qué aprenderás | Base del profesor |
|---|--------|----------------|-------------------|
| 00 | [Entornos con uv](00-Entornos-uv/) | Entornos virtuales, `pyproject.toml`, `uv.lock` y kernel de Jupyter | `pyproject.toml` y `uv` del ejemplo de API |
| 01 | [Git y GitHub](01-Git-GitHub/) | Commits, ramas, *pull requests*, conflictos y trabajo en equipo | Entrega final en GitHub |
| 02 | [BI y Analítica](02-BI-Analitica/) | BI vs. analítica, KPIs y los 4 tipos de análisis | `sesion_1_intro_bi.pdf` |
| 03 | [CRISP-DM](03-CRISP-DM/) | Comprensión del negocio y de los datos, *project charter* | `sesion_2_crisp_dm.pdf` |
| 04 | [Preparación de datos](04-Preparacion-Datos/) | Limpieza, integración (*joins*), escalado y *encoding* | `sesion_3_preparacion_de_datos` |
| 05 | [EDA](05-EDA/) | Distribuciones, *outliers*, correlaciones e hipótesis | `sesion_3` (parte EDA) |
| 06 | [Modelado y métricas](06-Modelado-Metricas/) | *Baseline*, regresión, clasificación, *overfitting* | `sesion_6_modelo.ipynb` |
| 07 | [Pipelines](07-Pipelines/) | `Pipeline`, `ColumnTransformer`, CV y `GridSearchCV` | `sesion_7_pipelines.ipynb` |
| 08 | [API con FastAPI](08-API-FastAPI/) | Servir el modelo, validar con Pydantic, probar con pytest | `api-example-udem-2026-01` |
| 09 | [Proyecto final](09-Proyecto-Final/) | Plantilla, rúbrica, checklist y presentación | Cronograma del curso |

## Cómo está organizado cada módulo

```
NN-Nombre-Modulo/
├── README.md              ← teoría explicada paso a paso (empieza aquí)
├── notebooks/             ← práctica guiada (primera parte de la clase), cuando aplica
├── scripts/               ← la misma lógica en .py ejecutables y documentados
├── ejercicios/
│   ├── EJERCICIOS.md      ← actividad en salas de Zoom (segunda parte de la clase)
│   └── soluciones/        ← soluciones de los ejercicios guiados
└── presentacion/          ← diapositivas del módulo (.pptx)
```

### El hilo del proyecto: los ejercicios están encadenados

La **segunda parte de cada clase** se trabaja en equipos de 3 personas en salas de Zoom. Cada ejercicio produce un entregable en el **repositorio del equipo**, y ese entregable es el punto de partida del módulo siguiente. Así, al final del curso el equipo ya tiene su proyecto armado.

| Módulo | Entregable del equipo (en su repositorio) | Lo usa el módulo |
|---|---|---|
| 00 | Proyecto `uv` del equipo con `pyproject.toml` + `uv.lock` | 01 |
| 01 | Repositorio en GitHub con estructura, ramas y primer PR | todos |
| 02 | `docs/01_problema_y_kpis.md`: tema, dataset candidato y 3 KPIs | 03 |
| 03 | `docs/02_project_charter.md` + perfil inicial del dataset | 04 |
| 04 | `src/limpieza.py` + `docs/03_decisiones_limpieza.md` | 05 |
| 05 | `notebooks/eda.ipynb` + 5 hallazgos e hipótesis | 06 |
| 06 | *Baseline* y primer modelo con métricas justificadas | 07 |
| 07 | `src/train.py` que entrena el pipeline y guarda el modelo | 08 |
| 08 | API con `/health` y `/predict` + pruebas | 09 |
| 09 | Entrega final y presentación | |

### Dataset guía: House Prices (Ames, Iowa)

Los notebooks usan **un mismo caso de punta a punta** para que se vea el ciclo completo: limpiar (04) → explorar (05) → modelar (06) → empaquetar (07) → desplegar (08). Los datos ya están en `data/raw/`, así que no hay que descargar nada.

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
├── src/intro_analitica/    ← funciones reutilizables (config, datos, limpieza, eda, métricas)
├── 00-Entornos-uv/ … 09-Proyecto-Final/
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
