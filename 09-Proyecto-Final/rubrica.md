# Rúbrica: Proyecto final (100 puntos)

| Criterio | Peso | Excelente (100 %) | Aceptable (60 %) | Insuficiente (20 %) |
|---|---|---|---|---|
| **1. Comprensión del negocio** | 15 | Problema claro, decisión que habilita, KPIs SMART y criterio de éxito definido **antes** de modelar | Problema claro pero KPIs vagos o sin criterio de éxito | No se entiende qué problema se resuelve |
| **2. Comprensión y preparación de los datos** | 15 | Perfil de calidad, decisiones de limpieza justificadas y documentadas, código reutilizable (`src/limpieza.py`) | Limpieza correcta pero poco justificada o solo en el notebook | Imputaciones "a ciegas", sin documentación |
| **3. EDA** | 15 | Hipótesis validadas con evidencia, hallazgos que se conectan con el modelo, gráficos adecuados | Gráficos correctos pero sin conclusiones claras | Gráficos sin interpretación |
| **4. Modelado y evaluación** | 20 | *Baseline*, varios modelos, métrica alineada con el negocio, validación sin *leakage*, test usado una sola vez, análisis de errores | Modelos correctos pero sin *baseline* o con métrica poco justificada | Un solo modelo, evaluado en train o con *leakage* |
| **5. Reproducibilidad e ingeniería** | 15 | `uv sync` + un comando reproducen el modelo; pipeline; API o dashboard funcionando; pruebas | Se puede reproducir con instrucciones adicionales | No se puede ejecutar |
| **6. Trabajo en equipo (Git)** | 5 | Ramas, PR revisados, commits de los 3 integrantes, mensajes claros | Commits de todos pero sin PR | Un solo integrante hace todo |
| **7. Comunicación** | 15 | Historia clara para negocio, visuales limpios, límites del modelo explícitos, tiempo respetado, respuestas sólidas | Presentación correcta pero demasiado técnica o larga | Lectura de diapositivas, sin conclusión |

## Bonificaciones (máximo +5)

- +2 API desplegada en la nube o contenedor Docker funcionando
- +2 GitHub Actions corriendo las pruebas en cada PR
- +1 Análisis de sesgos o de equidad del modelo

## Penalizaciones

- −10 El repositorio incluye `.venv/`, secretos o datos de más de 50 MB
- −5 Notebooks que no corren de principio a fin
- −5 por cada día de retraso
