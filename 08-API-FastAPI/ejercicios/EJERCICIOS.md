# Ejercicios: Módulo 08, API con FastAPI

> **Roten los roles.**

---

## Parte 1: Ejercicios guiados (25 min, primera parte de la clase)

Al final de `notebooks/01_consumir_api.ipynb` (soluciones en `soluciones/solucion_08.md`):

1. Predicción desde `/docs` con "Try it out"
2. Predicción con `curl`
3. "Tu casa soñada": ¿qué cambio sube más el precio?
4. ¿Qué pasa con 101 casas en `/predict/batch`?

**Mini-reto en vivo (10 min):** agreguen a `api/main.py` un endpoint `GET /ejemplo` que devuelva `EJEMPLO_CASA`. Recarguen `/docs` y verifiquen que aparece.

---

## Parte 2: Salas de Zoom, la API del proyecto del equipo (70 min)

> **Objetivo:** servir el modelo del equipo con una API que valide los datos y tenga pruebas automáticas.
> **Viene de:** `models/modelo.joblib` generado por `src/train.py` (módulo 07).
> **Va a:** módulo 09 (la demo de la API forma parte de la presentación final).

### Paso 1: Copiar la estructura (5 min)

```bash
mkdir -p api tests
cp <ruta>/intro_analitica/08-API-FastAPI/api/*.py api/
cp <ruta>/intro_analitica/08-API-FastAPI/tests/test_api.py tests/
uv add fastapi "uvicorn[standard]" httpx
```

### Paso 2: Adaptar (40 min, repartido)

| Integrante | Archivo | Tarea |
|---|---|---|
| A | `api/schemas.py` | Reemplazar `CasaEntrada` por las variables de **su** modelo, con reglas de negocio (`Field(ge=…, le=…)`, `Literal[...]`). Actualizar el ejemplo |
| B | `api/config.py` + `api/modelo.py` | Ruta a `models/modelo.joblib`, título y descripción. En `modelo.py`, ajustar cómo se arma el DataFrame. Si es **clasificación**, devolver la clase **y** la probabilidad (`predict_proba`) |
| C | `tests/test_api.py` | Al menos: `/health` responde 200, una predicción válida da 200, un dato inválido da 422 y una prueba de "sentido común" de su dominio |

> Si su modelo es de **clasificación**, la salida podría ser:
> ```python
> class PrediccionSalida(BaseModel):
>     clase: str
>     probabilidad: float
>     umbral: float
> ```

### Paso 3: Probar (15 min)

```bash
uv run pytest -v
uv run uvicorn api.main:app --reload
```

Cada integrante hace **una** predicción desde `/docs` con datos que tengan sentido para el negocio. ¿El resultado es razonable?

### Paso 4: Documentar (10 min)

Agreguen al README la sección **"API"** con: cómo levantarla, un ejemplo de solicitud y respuesta, y la tabla de códigos de error.

### Entregable

- [ ] `api/` con `/health` y `/predict` (y `/model-info` si tienen metadatos)
- [ ] Validación de negocio en `schemas.py` (al menos 3 reglas)
- [ ] `tests/test_api.py` con al menos 4 pruebas, todas en verde
- [ ] README con la sección "API"
- [ ] PR unido a `main`

### Reto opcional

1. Agreguen `/predict/batch`.
2. Creen un `Dockerfile` (ver sección 6 del README del módulo) y prueben `docker build` y `docker run`.
3. Configuren GitHub Actions para que `uv run pytest` corra en cada PR.

---

## Preguntas para la plenaria

1. Muestren una solicitud inválida y el mensaje de error de su API: ¿lo entendería alguien que no conoce el modelo?
2. ¿Qué regla de negocio pusieron en el esquema que **el modelo por sí solo** no sabría?
3. ¿Batch o tiempo real? ¿Qué necesita **su** negocio?

## Para la próxima sesión

Revisen la **rúbrica** del módulo 09 y el checklist de entrega. ¡Es la recta final!
