# Ejercicios: Módulo 05, Del modelo al producto

> **Roles de hoy:** el piloto es quien ha tenido menos commits en el repositorio (revísenlo en GitHub, pestaña *Insights → Contributors*). Recuerden: **solo el piloto edita el notebook**.

| Clase | Secciones del notebook del equipo |
|---|---|
| 26 de octubre | 0. Configuración · 1. El problema · 2. Los datos |
| 27 de octubre | 3. Limpieza · 4. EDA |
| 28 de octubre | 5. Modelo |
| **11 de noviembre (hoy)** | **6. Conclusiones** y preparación de la sustentación |

---

## Parte 1: Demostración (primera parte de la clase)

La profesora muestra, con House Prices:

1. El pipeline del notebook `01_pipeline_house_prices.ipynb`: cómo une la preparación y el modelo, y cómo se guarda con `joblib`.
2. La API en vivo:

   ```bash
   uv run python 05-Pipelines-y-API/scripts/train.py
   uv run uvicorn api.main:app --reload --app-dir 05-Pipelines-y-API
   ```

   y la documentación interactiva en http://127.0.0.1:8000/docs.

**Pregunta para todos (en el chat):** en la página `/docs`, la profesora envía una casa con `OverallQual = 15`. ¿Qué responde la API y por qué es bueno que lo haga?

> Quien quiera repetirlo en su computador puede seguir el README del módulo (sección 7). No es obligatorio.

---

## Parte 2: Salas de Zoom, cerrar el proyecto (50 min)

> **Objetivo:** dejar el notebook completo y reproducible, y salir con el esquema de la presentación final.
> **Viene de:** las secciones 1 a 5 del notebook y el avance del 4 de noviembre.
> **Va a:** la sustentación del 25 de noviembre.

### Paso 0: Actualizar (2 min)

Todos ejecutan `git pull`. El piloto abre el notebook y ejecuta *Restart Kernel and Run All*. Si algo falla, lo primero es arreglarlo.

### Paso 1: Guardar el modelo y escribir las conclusiones (sección 6, 15 min)

1. **6.1:** ejecuten la celda que guarda `models/modelo.joblib` y comprueben que el modelo cargado predice.
2. **6.2:** escriban las cuatro conclusiones **entre los tres**, pensando en quien toma la decisión: respuesta al problema, resultado principal en unidades de negocio, límites y siguientes pasos.

> **Así suena un resultado para negocio:** "el avalúo automático se equivoca en promedio un 11 %, frente a un 31 % si se usara siempre el precio mediano". Así **no**: "MAPE de 0.11".

### Paso 2: Revisión con el checklist (13 min)

Abran [`06-Proyecto-Final/checklist_entrega.md`](../../06-Proyecto-Final/checklist_entrega.md) y revisen cada punto. El copiloto lee y marca; el piloto corrige en el momento lo que sea rápido. Anoten lo que quede pendiente.

**Prueba del clon limpio (la más importante):** el relator clona el repositorio en una carpeta nueva y sigue **solo** el README:

```bash
git clone https://github.com/<usuario-piloto>/proyecto-<equipo>.git prueba-limpia
cd prueba-limpia
uv sync
uv run jupyter lab
```

¿El notebook corre completo sin pedir ayuda? Cada paso donde se trabe es algo que hay que arreglar en el README o en el notebook.

### Paso 3: Esquema de la presentación (12 min)

Con la [guía de la presentación](../../06-Proyecto-Final/guia_presentacion.md), escriban en `docs/presentacion.md` el **título-conclusión** de cada diapositiva y quién la presenta:

```markdown
# Esquema de la presentación

| # | Diapositiva | Título-conclusión | Presenta |
|---|---|---|---|
| 1 | Título y equipo | | |
| 2 | El problema | | |
| 3 | Objetivo y criterio de éxito | | |
| 4 | Los datos | | |
| 5 | Hallazgo 1 | | |
| 6 | Hallazgo 2 y 3 | | |
| 7 | El modelo frente al baseline | | |
| 8 | Límites | | |
| 9 | Recomendación y siguientes pasos | | |
```

Un **título-conclusión** dice el resultado, no el tema: "El barrio suma hasta un 46 % al precio" en lugar de "Análisis por barrio".

### Paso 4: Subir los cambios (8 min)

**Piloto** (notebook):

```bash
git pull
git add notebooks/proyecto_equipo.ipynb
git commit -m "feat: agrega conclusiones y guarda el modelo"
git push
```

**Copiloto** (esquema de la presentación, en su computador):

```bash
git pull
git add docs/presentacion.md
git commit -m "docs: agrega esquema de la presentación final"
git push
```

**Relator:** corrige en el README lo que falló en la prueba del clon limpio, agrega la sección **Resultados principales** y marca el avance:

```bash
git pull
git add README.md
git commit -m "docs: actualiza README con resultados y cómo ejecutar"
git push
```

### Entregable

- [ ] Sección 6 del notebook completa y el notebook corre de principio a fin
- [ ] `docs/presentacion.md` con el esquema y el reparto de la presentación
- [ ] README probado con la prueba del clon limpio
- [ ] Lista de pendientes del checklist, repartida entre los tres

### Reto opcional (bonificación en la rúbrica)

Pongan su propio modelo detrás de una API, partiendo de la carpeta `api/` de este módulo. Requiere leer el código con calma, así que es para hacerlo en las dos semanas antes de la sustentación:

1. Copien la carpeta `api/` a la raíz de su repositorio y agreguen las dependencias: `uv add fastapi "uvicorn[standard]" pydantic`.
2. En `api/config.py`, quiten la línea `from intro_analitica import config as config_curso` y cambien la ruta del modelo por `Path("models/modelo.joblib")`.
3. En `api/schemas.py`, cambien los campos de `CasaEntrada` por las variables de su modelo (las de `VARIABLES` en la sección 5.1), con su tipo y sus reglas.
4. En `api/main.py` y `api/schemas.py`, ajusten los nombres de la respuesta a su problema (por ejemplo, `clase_predicha` en lugar de `precio_estimado` si es clasificación).
5. Levántenla con `uv run uvicorn api.main:app --reload` y prueben `/predict` desde `/docs`.

---

## Plenaria (15 min)

Dudas sobre la sustentación: duración, demostración, reparto entre integrantes y rúbrica.

## Para la sustentación (25 de noviembre)

- 10 a 12 minutos de presentación y 5 de preguntas, con los tres integrantes.
- El repositorio debe estar actualizado **antes** del inicio de la sesión.
- Ensayen con cronómetro al menos una vez.
