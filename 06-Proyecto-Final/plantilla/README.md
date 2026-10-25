# Plantilla del proyecto del equipo

`proyecto_equipo.ipynb` es el notebook donde cada equipo construye su proyecto, una sección por clase. Se copia al repositorio del equipo, en la carpeta `notebooks/`, durante el módulo 02.

| Sistema | Comando (desde la carpeta del repositorio del equipo) |
|---|---|
| macOS, Linux y Git Bash | `cp <ruta>/intro_analitica/06-Proyecto-Final/plantilla/proyecto_equipo.ipynb notebooks/` |
| Windows (PowerShell) | `Copy-Item <ruta>\intro_analitica\06-Proyecto-Final\plantilla\proyecto_equipo.ipynb notebooks\` |

## Qué necesita

- Las librerías del módulo 00 en el proyecto del equipo: `uv add pandas numpy matplotlib seaborn scikit-learn jupyter ipykernel`. Para guardar el modelo también usa `joblib`, que se instala junto con scikit-learn.
- El dataset en `data/raw/`.
- Completar las cinco variables de la sección 0: `ARCHIVO`, `SEPARADOR`, `OBJETIVO`, `TIPO_PROBLEMA` y `COLUMNAS_A_EXCLUIR`.

Con eso, todas las celdas funcionan para problemas de **regresión** y de **clasificación**. Las celdas y tablas marcadas con **COMPLETAR** son las que el equipo debe llenar en cada clase, y las celdas **Su código aquí** son espacios libres para explorar a su manera.

## Secciones

| Sección | Clase | Qué queda al terminar |
|---|---|---|
| 0. Configuración | 26 de octubre | Las variables del dataset |
| 1. El problema | 26 de octubre | Decisión, objetivo, criterio de éxito y 2 KPIs |
| 2. Los datos | 26 de octubre | Exploración libre del dataset, 3 problemas de calidad y 3 hipótesis |
| 3. Limpieza | 27 de octubre | 3 decisiones con su justificación y `data/processed/datos_limpios.csv` |
| 4. EDA | 27 de octubre | Gráficas, un KPI calculado y 3 hallazgos |
| 5. Modelo | 28 de octubre | *Baseline*, modelo lineal y árbol de decisión comparados en train y test |
| 6. Conclusiones | 11 de noviembre | Modelo guardado en `models/modelo.joblib` y conclusiones para negocio |
