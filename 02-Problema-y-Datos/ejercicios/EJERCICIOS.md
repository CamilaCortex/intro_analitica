# Ejercicios: Módulo 02, Del problema a los datos

> **Roten los roles:** quien fue relator en el módulo 01 ahora es piloto.

## Cómo trabajamos desde hoy

Desde esta clase el proyecto vive en **un solo notebook**, `notebooks/proyecto_equipo.ipynb`, dentro del repositorio del equipo. En cada clase se llena una parte:

| Clase | Secciones del notebook |
|---|---|
| **26 de octubre (hoy)** | **0. Configuración · 1. El problema · 2. Los datos** |
| 27 de octubre | 3. Limpieza · 4. EDA |
| 28 de octubre | 5. Modelo |
| 11 de noviembre | 6. Conclusiones |

**Regla para no tener conflictos en Git:** durante la sala, **solo el piloto edita el notebook** y comparte pantalla. El copiloto y el relator ayudan a pensar, buscan en la documentación y revisan. Al final, el piloto sube los cambios y los demás hacen `git pull`.

---

## Parte 2: Salas de Zoom, el problema y los datos del equipo (45 min)

> **Objetivo:** con el dataset que el equipo ya eligió, escribir el problema con su criterio de éxito y conocer la calidad de los datos.
> **Viene de:** el repositorio del equipo (módulo 01) y el dataset elegido.
> **Va a:** la clase del 27 de octubre, donde se limpian los problemas que encuentren hoy.

### Paso 1: Preparar el repositorio (10 min)

El **piloto**, en su computador (el copiloto revisa en paralelo que el dataset tenga una **variable objetivo** clara y pese **menos de 50 MB**):

1. En el repositorio del equipo, trae los últimos cambios y copia la plantilla en la carpeta `notebooks/`:

   ```bash
   cd <ruta>/proyecto-<equipo>
   git pull
   ```

   | Sistema | Comando para copiar la plantilla |
   |---|---|
   | macOS, Linux y Git Bash | `cp <ruta>/intro_analitica/06-Proyecto-Final/plantilla/proyecto_equipo.ipynb notebooks/` |
   | Windows (PowerShell) | `Copy-Item <ruta>\intro_analitica\06-Proyecto-Final\plantilla\proyecto_equipo.ipynb notebooks\` |

   También se puede arrastrar el archivo con el explorador de VS Code.

2. Guarda el dataset del equipo en `data/raw/` (si ya está ahí, sigue al punto 4). Usen un nombre corto, sin espacios ni tildes (por ejemplo, `data/raw/ventas.csv`).
3. Abre el notebook en VS Code o con `uv run jupyter lab`, y selecciona el kernel `.venv` del proyecto.

### Paso 2: Configuración y problema (secciones 0 y 1, 15 min)

1. **Sección 0:** completen `ARCHIVO`, `SEPARADOR`, `OBJETIVO` y `TIPO_PROBLEMA`. Ejecuten las dos celdas: debe aparecer "Configuración lista".
2. **Sección 1:** llenen la tabla del problema **entre los tres**. Las respuestas más importantes son la **decisión**, la **variable objetivo** y el **criterio de éxito**.

> **Si su proyecto es descriptivo** (un dashboard, sin modelo), escriban como objetivo el KPI principal y como criterio de éxito la pregunta que el dashboard debe responder.

### Paso 3: Conocer los datos (sección 2, 15 min)

1. **2.1:** ejecuten la celda que carga el dataset. Si `pd.read_csv` falla o todo queda en una sola columna, prueben `SEPARADOR = ";"`. Respondan **qué representa una fila**.
2. **2.2, exploración libre:** respondan las preguntas de la tabla de esa sección con su propio código, en las celdas "Su código aquí". La sección trae herramientas de pandas sugeridas, pero pueden usar las que quieran. Mientras el piloto escribe, el copiloto y el relator buscan cómo resolver la siguiente pregunta.
3. **2.3:** con lo que encontraron, llenen la tabla de **3 problemas de calidad** y **3 hipótesis**.

### Paso 4: Subir los cambios (5 min)

Antes de subir, ejecuten *Restart Kernel and Run All* para comprobar que el notebook corre completo.

**Piloto** (sube el notebook y los datos):

```bash
git pull
git add notebooks/proyecto_equipo.ipynb data/raw/
git commit -m "feat: agrega problema, configuración y perfil de los datos"
git push
```

**Relator** (actualiza el README del equipo en su computador, en las secciones *Problema de negocio* y *Dataset*):

```bash
git pull
git add README.md
git commit -m "docs: agrega problema y dataset al README"
git push
```

**Copiloto:** hace `git pull` y comprueba que el notebook se abre y corre en su computador.

> Si el dataset pesa más de 50 MB, no lo suban: agreguen `data/raw/` al `.gitignore` y escriban en el README el enlace de descarga.

### Entregable

- [ ] Dataset en `data/raw/` (o enlace de descarga en el README)
- [ ] `notebooks/proyecto_equipo.ipynb` con las secciones 0, 1 y 2 completas y ejecutadas
- [ ] README del equipo con el problema y el dataset
- [ ] Commits del piloto y del relator en GitHub

---

## Plenaria (10 min)

Cada relator presenta en **1 minuto**: el problema, la variable objetivo y el criterio de éxito. El resto del grupo responde: ¿se entiende **cómo** van a medir si lo lograron?

## Para la próxima clase

Lean el diccionario de datos de su dataset y traigan claro **por qué** faltan los datos en las columnas con nulos. Mañana se limpian.
