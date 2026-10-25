# Módulo 06: Proyecto final

> **Objetivo:** entregar un proyecto de ciencia de datos **completo, reproducible y bien comunicado**, que resuelva un problema real siguiendo CRISP-DM.

**Sustentación:** miércoles 25 de noviembre

## Contenido

| Archivo | Para qué sirve |
|---|---|
| `README.md` | Enunciado, cronograma y entregables (estás aquí) |
| `plantilla/proyecto_equipo.ipynb` | El notebook del proyecto: se copia al repositorio del equipo en el módulo 02 |
| `rubrica.md` | Cómo se califica (100 puntos) |
| `checklist_entrega.md` | Lista para revisar antes de entregar |
| `guia_presentacion.md` | Estructura y consejos para la sustentación |
| `presentacion/06-Proyecto-Final.pptx` | Diapositivas: cronograma, entregables, rúbrica y checklist |

---

## Objetivos

- Desarrollar un proyecto de ciencia de datos con los conocimientos adquiridos en la especialización.
- Enfocarse en **solucionar un problema real**.
- Recorrer **todas las fases** de un proyecto de este tipo.
- Enfrentar las **dificultades prácticas**: datos incompletos, decisiones de limpieza, elección de métricas y comunicación de resultados.

## Reglas

- Equipos de **3 personas**.
- Un **repositorio de GitHub** por equipo, con commits de los 3 integrantes y la profesora como colaboradora.
- Dataset público (o anonimizado). Si pesa más de 50 MB, no se sube: el README explica cómo descargarlo.

## Cronograma

| Fecha | Clase | Avance del proyecto (secciones del notebook) |
|---|---|---|
| 19 de octubre | Introducción al curso | Equipos conformados |
| 20 y 21 de octubre | 00 Entornos con uv · 01 Git y GitHub | Repositorio del equipo con el proyecto `uv` |
| 26 de octubre | 02 Del problema a los datos | 0. Configuración · 1. El problema · 2. Los datos |
| 27 de octubre | 03 Preparación de datos y EDA | 3. Limpieza · 4. EDA |
| 28 de octubre | 04 Modelado y métricas | 5. Modelo |
| 29 de octubre al 10 de noviembre | Trabajo autónomo | Mejorar las secciones 1 a 5 |
| **4 de noviembre** | **Avance intermedio** | El notebook corre completo; README con problema, datos, hallazgos y resultado |
| 11 de noviembre | 05 Del modelo al producto | 6. Conclusiones · esquema de la presentación |
| **25 de noviembre** | **Sustentación** | Entrega final y presentación |

## Entregables finales

1. **Repositorio en GitHub** con:
   - `README.md`: problema, equipo, dataset, cómo ejecutar, resultados principales y límites.
   - `notebooks/proyecto_equipo.ipynb`: las 6 secciones completas y ejecutadas de principio a fin.
   - `pyproject.toml` y `uv.lock`: cualquiera puede reproducir el proyecto con `uv sync`.
   - `docs/presentacion.md`: el esquema de la presentación.
2. **Presentación** de 10 a 12 minutos y 5 de preguntas (ver `guia_presentacion.md`).

**Según el tipo de proyecto:**

- **Predictivo** (regresión o clasificación): el modelo de la sección 5, comparado contra el *baseline*.
- **Descriptivo o diagnóstico:** en lugar de la sección 5, KPIs y hallazgos que respondan la pregunta del negocio. Puede acompañarse de un dashboard (Power BI, Looker Studio, Streamlit).

**Bonificación:** una API con el modelo del equipo (módulo 05) o un dashboard publicado. Ver `rubrica.md`.

## Estructura esperada del repositorio

```
proyecto-<equipo>/
├── README.md                     ← resumen, cómo ejecutar, resultados y límites
├── pyproject.toml / uv.lock      ← entorno reproducible (módulo 00)
├── .gitignore                    ← sin .venv/, data/processed/ ni models/
├── data/
│   ├── raw/                      ← datos originales (o enlace de descarga en el README)
│   └── processed/                ← datos limpios (los genera el notebook; no se suben)
├── notebooks/
│   └── proyecto_equipo.ipynb     ← el proyecto completo
├── docs/
│   ├── 00_acuerdos_equipo.md     ← módulo 01
│   └── presentacion.md           ← módulo 05
└── models/                       ← modelo guardado (lo genera el notebook; no se sube)
```

## Consejos

- **Empiecen por el problema, no por el algoritmo.** Un modelo simple que responde la pregunta correcta le gana a uno complejo que responde otra.
- **Iteren.** CRISP-DM es un ciclo: volver a la limpieza después de modelar es normal.
- **Documenten mientras avanzan**, no la noche antes. Las tablas de cada sección del notebook son la documentación.
- **Comuniquen los límites.** "El modelo no funciona bien para casas de más de USD 500.000" es una conclusión valiosa, no un fracaso.
- **No cumplir el criterio de éxito no es reprobar.** Se califica el proceso y que expliquen por qué pasó y qué harían distinto.
