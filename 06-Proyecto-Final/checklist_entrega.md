# Checklist de entrega

Revisen cada punto **entre los tres** antes del avance del 4 de noviembre y antes de la sustentación.

## Repositorio

- [ ] Compartido con la profesora como colaboradora
- [ ] `README.md` con: problema, equipo, dataset (fuente y enlace), cómo ejecutar, resultados principales y límites
- [ ] `pyproject.toml` y `uv.lock` con Python 3.14
- [ ] `.gitignore` excluye `.venv/`, `.env`, `data/processed/` y `models/`
- [ ] Sin archivos de más de 50 MB y sin contraseñas
- [ ] Commits de los 3 integrantes, con mensajes en formato *tipo: descripción*

## Reproducibilidad

- [ ] Prueba del clon limpio: en una carpeta nueva, `git clone`, `uv sync` y *Run All* funcionan sin pedir ayuda
- [ ] El notebook corre de principio a fin con *Restart Kernel and Run All*
- [ ] La semilla está fija (`SEMILLA = 42` en la sección 0)

## Notebook del proyecto

- [ ] **Sección 1:** tabla del problema completa, con criterio de éxito y 2 KPIs SMART
- [ ] **Sección 2:** qué representa una fila, 3 problemas de calidad y 3 hipótesis
- [ ] **Sección 3:** al menos 3 decisiones de limpieza con su justificación en el registro
- [ ] **Sección 4:** 3 hallazgos con evidencia, implicación e hipótesis relacionada
- [ ] **Sección 5:** métrica principal justificada, comparación con el *baseline* e interpretación completa
- [ ] **Sección 6:** conclusiones para negocio, con límites y siguientes pasos
- [ ] No quedan celdas con `COMPLETAR` sin llenar

## Presentación

- [ ] `docs/presentacion.md` con el esquema y quién presenta cada parte
- [ ] 10 a 12 minutos, ensayada con cronómetro
- [ ] Títulos-conclusión en cada diapositiva
- [ ] Cada integrante presenta una parte
- [ ] Si hay demostración (API o dashboard), un plan B con capturas por si falla
