# Soluciones: ejercicios guiados del notebook 2 (consumir la API), módulo 05

## 1. `/docs` → "Try it out"

1. `uv run uvicorn api.main:app --reload --app-dir 05-Pipelines-y-API`
2. Abrir http://127.0.0.1:8000/docs → `POST /predict` → **Try it out**. El cuerpo ya viene lleno con el ejemplo definido en `schemas.py` (`json_schema_extra`) → **Execute**.
3. Abajo aparecen la respuesta, el código 200 y el comando `curl` equivalente.

## 2. Con `curl`

```bash
curl -X POST http://127.0.0.1:8000/predict \
     -H "Content-Type: application/json" \
     -d @05-Pipelines-y-API/ejemplos/casa.json
# {"precio_estimado":204839.0,"rango_aproximado":[185011.0,224667.0],"version_modelo":"1.0.0"}
```

> Los valores exactos pueden variar un poco según las versiones de las librerías y si entrenaste con `--buscar`.

En Windows (PowerShell), `curl` es un alias de otro comando. Usa:

```powershell
Invoke-RestMethod -Uri http://127.0.0.1:8000/predict -Method Post -ContentType "application/json" -InFile 05-Pipelines-y-API\ejemplos\casa.json
```

## 3. "Tu casa soñada"

Con la casa base (≈ USD 205.000), el modelo de referencia dio:

| Cambio | Precio | Variación |
|---|---|---|
| Cocina `Ex` | ≈ 207.000 | +1 % |
| Garaje para 3 carros | ≈ 214.000 | +4 % |
| Calidad general 8 | ≈ 214.000 | +5 % |
| Barrio `NridgHt` | ≈ 210.000 | +2 % |

**Lectura:** subir la **calidad general** es de lo que más mueve el precio, igual que en el EDA. Pero ojo: el modelo responde "¿cuánto valen casas **parecidas** que tienen esa característica?", no "¿cuánto ganaré si remodelo?". Eso es **correlación, no causalidad**: para la segunda pregunta habría que hacer un experimento o un análisis causal.

## 4. 101 casas en `/predict/batch`

```python
r = cliente.post("/predict/batch", json={"casas": [casa] * 101})
r.status_code   # 413 (Payload Too Large)
r.json()        # {'detail': 'Máximo 100 casas por solicitud'}
```

El límite está en `api/config.py` (`MAX_BATCH`) y se puede cambiar con una variable de entorno sin tocar el código:

```bash
MAX_BATCH=500 uv run uvicorn api.main:app --app-dir 05-Pipelines-y-API
```

**¿Por qué limitar?** Para que una sola solicitud gigante no deje la API sin memoria y bloquee a los demás usuarios.
