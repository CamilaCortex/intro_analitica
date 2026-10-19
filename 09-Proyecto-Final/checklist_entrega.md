# Checklist de entrega

Revisen cada punto **entre los tres** antes de entregar. Lo automatizable lo revisa `scripts/verificar_entrega.py`.

## Repositorio

- [ ] Público o compartido con la profesora
- [ ] `README.md` con: problema, equipo, dataset, cómo ejecutar, resultados principales y límites
- [ ] `pyproject.toml` + `uv.lock` (Python 3.14)
- [ ] `.gitignore` excluye `.venv/`, `.env`, `data/processed/`, `models/`
- [ ] Sin archivos de más de 50 MB y sin secretos
- [ ] Commits de los 3 integrantes y al menos 1 PR revisado por integrante

## Reproducibilidad

- [ ] En un clon limpio: `uv sync` funciona sin errores
- [ ] `uv run python -m src.train` (o equivalente) regenera el modelo
- [ ] Todos los notebooks corren con "Restart & Run All"
- [ ] Semillas fijas (`random_state=42`)

## Documentación (`docs/`)

- [ ] `01_problema_y_kpis.md`
- [ ] `02_project_charter.md` (actualizado con lo aprendido)
- [ ] `03_decisiones_limpieza.md`
- [ ] Hallazgos del EDA (en `docs/` o en el README)
- [ ] `05_modelado.md` con *baseline*, comparación y modelo elegido

## Modelo / solución

- [ ] Se compara contra un *baseline*
- [ ] La métrica principal está justificada por el negocio
- [ ] Se reporta la métrica en test (usado una vez)
- [ ] Se discuten los errores y los límites del modelo
- [ ] API con `/health` y `/predict` + pruebas en verde (proyectos predictivos), **o** dashboard funcionando (proyectos descriptivos)

## Presentación

- [ ] 10-12 minutos, ensayada con cronómetro
- [ ] Demo preparada, con un plan B (capturas o video) por si falla el internet
- [ ] Cada integrante presenta una parte
