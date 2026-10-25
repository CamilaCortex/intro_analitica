# <Nombre del proyecto>

> Una frase que explique qué problema resuelven y para quién.

## Equipo

| Integrante | Rol principal | GitHub |
|---|---|---|
| Nombre 1 | Datos y limpieza | @usuario1 |
| Nombre 2 | EDA y visualización | @usuario2 |
| Nombre 3 | Modelado y API | @usuario3 |

## Problema de negocio

_(se completa en el módulo 02: qué decisión apoya el proyecto y cómo se mide el éxito)_

## Dataset

- **Fuente:** <enlace>
- **Tamaño:** N filas × M columnas
- **Variable objetivo:** <columna>

## Cómo ejecutar

```bash
uv sync
uv run jupyter lab
```

Luego abrir `notebooks/proyecto_equipo.ipynb` y ejecutar todas las celdas (*Run All*).

## Estructura

```
├── data/raw/          ← datos originales
├── data/processed/    ← datos limpios (los genera el notebook; no se suben)
├── notebooks/         ← proyecto_equipo.ipynb: el proyecto completo
├── docs/              ← acuerdos del equipo y material de apoyo
├── src/               ← código reutilizable (opcional)
└── models/            ← modelo entrenado (lo genera el notebook; no se sube)
```

## Resultados principales

_(se completa en el módulo 05: resultado del modelo frente al baseline, hallazgos y límites)_

## Avance

- [ ] 00 Entorno con uv
- [ ] 01 Repositorio en GitHub
- [ ] 02 Problema y datos (secciones 1 y 2 del notebook)
- [ ] 03 Limpieza y EDA (secciones 3 y 4)
- [ ] 04 Modelo (sección 5)
- [ ] 05 Conclusiones (sección 6)
- [ ] 06 Sustentación
