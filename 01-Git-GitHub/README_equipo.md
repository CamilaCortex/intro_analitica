# <Nombre del proyecto>

> Una frase que explique qué problema resuelven y para quién.

## Equipo

| Integrante | Rol principal | GitHub |
|---|---|---|
| Nombre 1 | Datos y limpieza | @usuario1 |
| Nombre 2 | EDA y visualización | @usuario2 |
| Nombre 3 | Modelado y API | @usuario3 |

## Problema de negocio

_(se completa en el módulo 02)_

## Dataset

- **Fuente:** <enlace>
- **Tamaño:** N filas × M columnas
- **Variable objetivo:** <columna>

## Cómo ejecutar

```bash
uv sync
uv run jupyter lab
```

## Estructura

```
├── data/raw/          ← datos originales
├── data/processed/    ← datos limpios (generados)
├── docs/              ← problema, charter, decisiones
├── notebooks/         ← exploración
├── src/               ← código reutilizable (limpieza, train, api)
└── models/            ← modelos entrenados (generados)
```

## Avance

- [ ] 00 Entorno con uv
- [ ] 01 Repositorio en GitHub
- [ ] 02 Problema y KPIs
- [ ] 03 Project charter
- [ ] 04 Limpieza
- [ ] 05 EDA
- [ ] 06 Baseline
- [ ] 07 Pipeline de entrenamiento
- [ ] 08 API
- [ ] 09 Entrega final
