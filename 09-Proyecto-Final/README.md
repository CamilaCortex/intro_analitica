# Módulo 09: Proyecto final

> **Objetivo:** entregar un proyecto de ciencia de datos **completo, reproducible y bien comunicado**, que resuelva un problema real siguiendo CRISP-DM.

**Basado en:** "Generalidades del curso" (`sesion_1_intro_bi.pdf`) del profesor

## Contenido

| Archivo | Para qué sirve |
|---|---|
| `README.md` | Enunciado, cronograma y entregables |
| `rubrica.md` | Cómo se califica (100 puntos) |
| `checklist_entrega.md` | Lista para revisar antes de entregar |
| `guia_presentacion.md` | Estructura y consejos para la presentación final |
| `plantilla_repo/` | Esqueleto del repositorio del equipo, por si alguien empieza de cero |
| `scripts/verificar_entrega.py` | Revisa automáticamente el repositorio del equipo |
| `ejercicios/EJERCICIOS.md` | Ensayo de la presentación y revisión entre pares |

---

## Objetivos (del profesor)

- Desarrollar un proyecto de ciencia de datos con los conocimientos adquiridos hasta ahora en la especialización.
- Enfocarse en **solucionar un problema real**.
- Comprender **todas las fases** de un proyecto de este tipo.
- Ver las **dificultades prácticas** de este tipo de proyectos.

## Reglas

- Equipos de **3 personas**.
- Un **repositorio de GitHub** por equipo, con commits de los 3 integrantes.
- Dataset público (o anonimizado) y de menos de 50 MB, o con instrucciones claras de descarga.

## Cronograma

| Semana | Hito | Entregable | Módulos |
|---|---|---|---|
| 1 | Equipo, temática y dataset con exploración inicial | `docs/01_problema_y_kpis.md`, `docs/02_project_charter.md`, perfil inicial | 00–03 |
| 2 | Análisis exploratorio (EDA) | Limpieza + `notebooks/05_eda.ipynb` con hallazgos | 04–05 |
| 3 | Primeros avances de la solución (prototipo de dashboard, *baseline* del modelo, etc.) | `docs/05_modelado.md`, `src/train.py` | 06–07 |
| 4 | **Entrega final** | Repositorio completo + API o dashboard + presentación | 08–09 |

> En el semestre 2026-01, el profesor usó estas fechas: 27-29 de abril (equipo y dataset), 4-6 de mayo (EDA), 11-12 de mayo (avances) y 19 de mayo (entrega final). Ajústalas al calendario de tu cohorte.

## Entregables finales

1. **Repositorio en GitHub** con código, documentación y resultados (ver `checklist_entrega.md`).
2. **Solución funcionando**, según el tipo de proyecto:
   - Predictivo → **API** (módulo 08) o script de predicción por lotes.
   - Descriptivo o diagnóstico → **dashboard** (Power BI, Looker Studio, Streamlit…) con los KPIs del módulo 02.
3. **Presentación** de 10-12 minutos + 5 de preguntas (ver `guia_presentacion.md`).

## Estructura esperada del repositorio

```
proyecto-<equipo>/
├── README.md                 ← resumen ejecutivo, cómo ejecutar, resultados
├── pyproject.toml / uv.lock
├── data/raw/                 ← datos originales (o instrucciones de descarga)
├── docs/
│   ├── 00_acuerdos_equipo.md
│   ├── 01_problema_y_kpis.md
│   ├── 02_project_charter.md
│   ├── 02_perfil_inicial.md
│   ├── 03_decisiones_limpieza.md
│   ├── 04_eda.md (o hallazgos en el README)
│   ├── 05_modelado.md
│   └── 06_pipeline.md
├── notebooks/                ← 05_eda.ipynb, 06_modelado.ipynb, 07_pipeline.ipynb
├── src/                      ← limpieza.py, pipeline.py, train.py
├── api/ + tests/             ← (proyectos predictivos)
└── models/                   ← generado por train.py (no se sube)
```

`plantilla_repo/` tiene este esqueleto listo para copiar.

## Verificar antes de entregar

```bash
uv run python 09-Proyecto-Final/scripts/verificar_entrega.py ruta/al/proyecto-del-equipo
```

## Consejos de quien ya pasó por aquí

- **Empiecen por el problema, no por el algoritmo.** Un modelo simple que responde la pregunta correcta le gana a un XGBoost que responde otra.
- **Iteren.** CRISP-DM es un ciclo: volver a la fase de datos después de modelar es normal.
- **Documenten mientras avanzan**, no la noche antes.
- **Comuniquen los límites.** "El modelo no funciona bien para casas de más de USD 500.000" es una conclusión valiosa, no un fracaso.
