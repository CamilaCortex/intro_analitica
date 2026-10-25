# Guía para la presentación final

**Duración:** 10-12 minutos + 5 de preguntas · **Público:** imaginen que es el **comité directivo** de la empresa, no un jurado técnico.

## Estructura sugerida (unas 10 diapositivas)

Casi todo el contenido ya está en el notebook del equipo: la columna **Sale de** indica la sección.

| # | Diapositiva | Tiempo | Pregunta que responde | Sale de |
|---|---|---|---|---|
| 1 | Título y equipo | 0:15 | ¿Quiénes son? | |
| 2 | **El problema** | 1:00 | ¿Qué duele y a quién? ¿Cuánto cuesta? | Sección 1 |
| 3 | Objetivo y criterio de éxito | 0:45 | ¿Qué significa "lo logramos"? | Sección 1 |
| 4 | Los datos | 1:00 | ¿De dónde salen, qué tan buenos son, qué tuvimos que limpiar? | Secciones 2 y 3 |
| 5-6 | **3 hallazgos del EDA** | 2:00 | ¿Qué descubrimos? (una gráfica por hallazgo) | Sección 4 |
| 7 | El modelo frente al *baseline* | 1:30 | ¿Cuánto mejor que no tener modelo? | Sección 5 |
| 8 | Demostración (opcional: API o dashboard) | 2:00 | ¿Cómo se usaría en el día a día? | Módulo 05 |
| 9 | Límites y riesgos | 1:00 | ¿Cuándo **no** confiar en el resultado? | Sección 6 |
| 10 | Recomendación y siguientes pasos | 1:00 | ¿Qué decisión debería tomar el comité? | Sección 6 |

Si no hay demostración, usen esos 2 minutos para explicar mejor los hallazgos o los errores del modelo.

## Consejos

- **Una idea por diapositiva.** El título de cada diapositiva debe ser la conclusión ("El barrio suma hasta un 46 % al precio"), no el tema ("Análisis por barrio").
- **Gráficos simples**, con ejes en unidades de negocio (pesos, %, días) y la parte importante resaltada.
- **Hablen el idioma del negocio.** Digan "nos equivocamos en promedio un 10 %" en lugar de "MAPE de 0.0968".
- **Si hay demostración, ensáyenla** y tengan capturas o un video de respaldo.
- **Los límites dan credibilidad.** Decir dónde falla el modelo muestra que lo entienden.
- **Ensayen con cronómetro.** Pasarse del tiempo es la falla más común.

## Preguntas que probablemente les harán

- ¿Por qué esa métrica y no otra?
- ¿Cómo saben que el modelo no está sobreajustado?
- ¿Qué pasaría si los datos cambian (otro año, otra ciudad)?
- ¿Qué variable sorprendió más?
- Si tuvieran un mes más, ¿qué harían?
