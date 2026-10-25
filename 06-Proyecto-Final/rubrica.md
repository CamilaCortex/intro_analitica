# Rúbrica: Proyecto final (100 puntos)

Cada criterio corresponde a una o más secciones del notebook del equipo (`notebooks/proyecto_equipo.ipynb`).

| Criterio | Peso | Excelente (100 %) | Aceptable (60 %) | Insuficiente (20 %) |
|---|---|---|---|---|
| **1. Comprensión del negocio** (sección 1) | 15 | Problema claro, decisión que apoya, KPIs SMART y criterio de éxito definido **antes** de modelar | Problema claro pero KPIs vagos o sin criterio de éxito | No se entiende qué problema se resuelve |
| **2. Datos y limpieza** (secciones 2 y 3) | 15 | Perfil de calidad, decisiones de limpieza justificadas con criterio de negocio y registradas en la tabla | Limpieza correcta pero poco justificada | Datos usados sin revisar, o nulos rellenados "a ciegas" |
| **3. EDA** (sección 4) | 15 | 3 o más hallazgos con evidencia e implicación, conectados con las hipótesis y con el modelo | Gráficos correctos pero sin conclusiones claras | Gráficos sin interpretación |
| **4. Modelo y evaluación** (sección 5) | 20 | Comparación con el *baseline*, métrica alineada con el negocio, variables justificadas, revisión de *overfitting* y de los errores | Modelos correctos pero con métrica poco justificada o sin interpretar | Sin *baseline*, o evaluado solo con los datos de entrenamiento |
| **5. Reproducibilidad** | 10 | En un clon limpio, `uv sync` y *Run All* reproducen todo; el README explica cómo ejecutar | Se reproduce con instrucciones adicionales | No se puede ejecutar |
| **6. Trabajo en equipo (Git)** | 5 | Commits de los 3 integrantes con mensajes en formato *tipo: descripción* | Commits de todos pero con mensajes poco claros | Un solo integrante hace todos los commits |
| **7. Comunicación** (sección 6 y presentación) | 20 | Historia clara para negocio, títulos-conclusión, límites explícitos, tiempo respetado, respuestas sólidas | Presentación correcta pero demasiado técnica o larga | Lectura de diapositivas, sin conclusión |

**Proyectos descriptivos o diagnósticos:** el criterio 4 se evalúa con los KPIs y su análisis (¿responden la pregunta del negocio? ¿están bien calculados y comparados?) en lugar del modelo.

## Bonificaciones (máximo +5)

- +3 API con el modelo del equipo funcionando (módulo 05) **o** dashboard publicado con los KPIs
- +2 Un modelo adicional bien justificado (por ejemplo, Random Forest) o validación cruzada
- +1 Análisis de sesgos: ¿el modelo se equivoca más en algún grupo?

## Penalizaciones

- −10 El repositorio incluye `.venv/`, contraseñas o datos de más de 50 MB
- −5 El notebook no corre de principio a fin
- −5 por cada día de retraso
