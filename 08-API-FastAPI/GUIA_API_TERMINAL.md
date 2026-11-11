# Guía práctica: levantar y consumir la API desde la terminal

> Complemento del [README del módulo 08](README.md). Aquí está **la introducción para explicar la API en clase** y **todos los comandos `curl`** listos para copiar y pegar.

---

## Parte 1. La introducción: ¿qué es una API y qué es uvicorn?

### 1.1 El problema

Al terminar el módulo 07 tenemos un archivo `models/house_price_model.joblib` que predice el precio de una casa. Pero **solo funciona dentro de Python, en mi computador**.

Una inmobiliaria quiere mostrar avalúos en su página web. ¿Le mandamos el notebook? No:

- La página web no habla Python, no tiene pandas ni scikit-learn.
- No queremos que nadie toque el modelo directamente.
- Queremos validar los datos **antes** de que lleguen al modelo.

Necesitamos un **intermediario**. Ese intermediario es la **API**.

### 1.2 La analogía del restaurante

| Restaurante | Nuestro sistema |
|---|---|
| Cliente | Página web, app móvil, un script, `curl` |
| Menú | La documentación en `/docs` |
| Pedido escrito | El **JSON** con los datos de la casa |
| **Mesero** | **La API (FastAPI)** |
| Cocina | El pipeline (`.joblib`) |
| Plato | La predicción |
| **El local abierto al público** | **El servidor (uvicorn)** |

El cliente **nunca entra a la cocina**: solo habla con el mesero, en un formato acordado.

```
 Cliente ──── POST /predict + JSON ────►  uvicorn  ──►  FastAPI  ──►  pipeline.predict()
         ◄─── 200 + JSON (precio) ──────          ◄──           ◄──
```

### 1.3 Las tres piezas: FastAPI, Pydantic y uvicorn

| Pieza | Rol en el restaurante | Qué hace |
|---|---|---|
| **Pydantic** | El formato del pedido | Define qué datos son válidos (`OverallQual` entre 1 y 10, área > 0…). Si el pedido está mal, se devuelve **sin molestar a la cocina** |
| **FastAPI** | El mesero | Define los endpoints (`/predict`, `/health`…): qué hacer con cada pedido. Genera `/docs` automáticamente |
| **uvicorn** | El local con la puerta abierta | Es el **servidor web**: escucha en un puerto (8000), recibe los pedidos HTTP, se los pasa a FastAPI y devuelve la respuesta |

> **¿Por qué hace falta uvicorn si ya tenemos FastAPI?**
> FastAPI solo **describe** qué responder; por sí sola no abre ningún puerto ni escucha a nadie. Es como tener un mesero entrenado pero el restaurante cerrado. **uvicorn abre la puerta**: mantiene un proceso corriendo que atiende las conexiones de red. Técnicamente, uvicorn es un servidor **ASGI** (la interfaz estándar entre servidores web y aplicaciones Python asíncronas) y FastAPI es una aplicación ASGI.

### 1.4 HTTP en 5 minutos

**La dirección:** `http://127.0.0.1:8000/predict`

| Parte | Significado |
|---|---|
| `http://` | El protocolo (el "idioma" de la web) |
| `127.0.0.1` | "Este mismo computador" (también se escribe `localhost`) |
| `8000` | El puerto: la "puerta" donde escucha uvicorn |
| `/predict` | El **endpoint**: el "plato del menú" |

**Los verbos:**

| Verbo | Para qué | Ejemplo |
|---|---|---|
| `GET` | **Consultar** (no envía datos) | `/health`, `/model-info` |
| `POST` | **Enviar** datos para procesar | `/predict`, `/predict/batch` |

**Los códigos de respuesta** (la "cara del mesero"):

| Código | Significado | En nuestra API |
|---|---|---|
| **200** | Todo bien | La predicción salió |
| **404** | Ese plato no existe | Pediste una dirección sin endpoint (p. ej. `/`) |
| **413** | Pediste demasiado | Más de 100 casas en un batch |
| **422** | Tu pedido está mal escrito | Campo faltante, `OverallQual: 15`, área negativa… |
| **503** | La cocina está cerrada | No hay modelo cargado |

### 1.5 Los endpoints de nuestra API

| Endpoint | Verbo | Qué responde |
|---|---|---|
| `/health` | GET | ¿Está viva la API? ¿Cargó el modelo? |
| `/model-info` | GET | Versión, fecha de entrenamiento, variables y métricas |
| `/predict` | POST | Precio de **una** casa |
| `/predict/batch` | POST | Precios de **varias** casas |
| `/docs` | GET (navegador) | Documentación interactiva generada por FastAPI |

---

## Parte 2. Levantar la API

### 2.0 Requisito: tener el modelo entrenado

```bash
cd ~/Downloads/intro_analitica
uv run python 07-Pipelines/scripts/train.py --buscar
```

### 2.1 Levantar el servidor (elige una opción)

**Opción A: desde la raíz del proyecto** (la recomendada en el curso)

```bash
cd ~/Downloads/intro_analitica
uv run uvicorn api.main:app --reload --app-dir 08-API-FastAPI
```

**Opción B: desde la carpeta del módulo**

```bash
cd ~/Downloads/intro_analitica/08-API-FastAPI
uv run uvicorn api.main:app --reload
```

**Opción C: ejecutando `main.py` directamente** (sin recarga automática)

```bash
cd ~/Downloads/intro_analitica
uv run python 08-API-FastAPI/api/main.py
```

### 2.2 ¿Qué significa cada parte del comando?

```
uv run   uvicorn   api.main:app   --reload   --app-dir 08-API-FastAPI
  │         │          │             │                │
  │         │          │             │                └─ dónde está la carpeta que contiene "api/"
  │         │          │             └─ reinicia solo al guardar cambios (solo para desarrollo)
  │         │          └─ paquete "api" → archivo main.py → variable app = FastAPI(...)
  │         └─ el servidor web
  └─ usa el entorno del proyecto (donde están FastAPI y uvicorn)
```

**¿Por qué `--app-dir`?** Python busca el paquete `api` en la carpeta donde estás parado. Desde la raíz no hay ninguna carpeta `api` (está dentro de `08-API-FastAPI/`), así que hay que indicárselo. Tampoco se puede escribir `08-API-FastAPI.api.main`, porque un módulo de Python no puede tener guiones ni empezar con números.

> **Regla:** `--app-dir` debe apuntar a la carpeta que **contiene** `api/`. Si ya estás dentro de esa carpeta, no lo pongas.

### 2.3 ¿Cómo sé que funcionó?

```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Application startup complete.
```

Abre en el navegador: **http://127.0.0.1:8000/docs**

> **Para apagar el servidor:** `Ctrl + C` en esa terminal.

### 2.4 Errores comunes

| Lo que ves | Por qué pasa | Solución |
|---|---|---|
| `ModuleNotFoundError: No module named 'api'` | Estás en una carpeta que no corresponde a `--app-dir` (por ejemplo, en `07-Pipelines`, o dentro de `08-API-FastAPI` **con** `--app-dir 08-API-FastAPI`) | Usa la opción A desde la raíz o la B desde la carpeta del módulo |
| `"GET / HTTP/1.1" 404 Not Found` | **No es un error de la API**: entraste a `http://127.0.0.1:8000/`, que no tiene endpoint | Entra a `/docs` |
| `GET /favicon.ico 404` | El navegador pide un ícono que no existe | Ignóralo |
| `/health` dice `"modelo_cargado": false` y `/predict` da 503 | No existe `models/house_price_model.joblib` | Entrena primero (paso 2.0) |
| `[Errno 48] Address already in use` | Ya hay otro servidor en el puerto 8000 | Ciérralo con `Ctrl + C` o usa `--port 8001` |

---

## Parte 3. Consumir la API desde la terminal con `curl`

> **Importante:** abre una **terminal nueva**; la otra está ocupada con el servidor. Los comandos son de **una sola línea** y se corren **desde la raíz del proyecto**:
>
> ```bash
> cd ~/Downloads/intro_analitica
> ```

### 3.0 Anatomía de un `curl`

| Parte | Significado |
|---|---|
| `curl` | Programa para hacer pedidos HTTP desde la terminal |
| `-X POST` | El verbo (si no se pone, es `GET`) |
| `-H "Content-Type: application/json"` | Avisa al servidor: "te mando JSON" |
| `-d '{...}'` | El cuerpo del pedido escrito a mano |
| `-d @archivo.json` | El cuerpo del pedido leído desde un archivo (la `@` significa "lee este archivo") |
| `-i` | Muestra también el código de respuesta y los encabezados |
| `-s` | Modo silencioso (sin barra de progreso) |

> **Tip:** agrega `| python3 -m json.tool` al final para ver la respuesta con formato legible.

### 3.1 Monitoreo

**¿Está viva la API?**

```bash
curl http://127.0.0.1:8000/health
```

Respuesta esperada:

```json
{"status": "healthy", "api_version": "1.0.0", "modelo_cargado": true, "version_modelo": "1.0.0"}
```

**¿Qué modelo está respondiendo?**

```bash
curl -s http://127.0.0.1:8000/model-info | python3 -m json.tool
```

Muestra la versión, la fecha de entrenamiento, los hiperparámetros y las métricas (MAPE ≈ 9.7 %).

### 3.2 Predecir una casa (`/predict`)

**Desde el archivo de ejemplo:**

```bash
curl -X POST http://127.0.0.1:8000/predict -H "Content-Type: application/json" -d @08-API-FastAPI/ejemplos/casa.json
```

**Escribiendo los datos a mano:**

```bash
curl -X POST http://127.0.0.1:8000/predict -H "Content-Type: application/json" -d '{"LotArea": 9000, "OverallQual": 7, "OverallCond": 5, "YearBuilt": 2005, "YearRemodAdd": 2006, "GrLivArea": 1800, "TotalBsmtSF": 1000, "FullBath": 2, "BedroomAbvGr": 3, "GarageCars": 2, "Neighborhood": "CollgCr", "BldgType": "1Fam", "HouseStyle": "2Story", "KitchenQual": "Gd"}'
```

Respuesta esperada (con el modelo entrenado con `--buscar`):

```json
{"precio_estimado": 204839.0, "rango_aproximado": [185011.0, 224667.0], "version_modelo": "1.0.0"}
```

| Campo | Significado |
|---|---|
| `precio_estimado` | Precio predicho en USD |
| `rango_aproximado` | Precio ± el MAPE del modelo (orientativo, no es un intervalo de confianza estadístico) |
| `version_modelo` | La versión que se puso con `train.py --version` |

### 3.3 Predecir varias casas (`/predict/batch`)

```bash
curl -s -X POST http://127.0.0.1:8000/predict/batch -H "Content-Type: application/json" -d @08-API-FastAPI/ejemplos/casas.json | python3 -m json.tool
```

El cuerpo debe tener la forma `{"casas": [ {...}, {...} ]}`. Responde con la lista de `predicciones`, la `cantidad` y la `version_modelo`.

### 3.4 Escenarios "¿qué pasa si…?"

Mismo ejemplo, cambiando **una sola variable**. Compara los precios con el de la casa base:

**Calidad general 9 (en vez de 7):**

```bash
curl -X POST http://127.0.0.1:8000/predict -H "Content-Type: application/json" -d '{"LotArea": 9000, "OverallQual": 9, "OverallCond": 5, "YearBuilt": 2005, "YearRemodAdd": 2006, "GrLivArea": 1800, "TotalBsmtSF": 1000, "FullBath": 2, "BedroomAbvGr": 3, "GarageCars": 2, "Neighborhood": "CollgCr", "BldgType": "1Fam", "HouseStyle": "2Story", "KitchenQual": "Gd"}'
```

**Cocina excelente (`Ex`):**

```bash
curl -X POST http://127.0.0.1:8000/predict -H "Content-Type: application/json" -d '{"LotArea": 9000, "OverallQual": 7, "OverallCond": 5, "YearBuilt": 2005, "YearRemodAdd": 2006, "GrLivArea": 1800, "TotalBsmtSF": 1000, "FullBath": 2, "BedroomAbvGr": 3, "GarageCars": 2, "Neighborhood": "CollgCr", "BldgType": "1Fam", "HouseStyle": "2Story", "KitchenQual": "Ex"}'
```

**Barrio caro (`NridgHt`):**

```bash
curl -X POST http://127.0.0.1:8000/predict -H "Content-Type: application/json" -d '{"LotArea": 9000, "OverallQual": 7, "OverallCond": 5, "YearBuilt": 2005, "YearRemodAdd": 2006, "GrLivArea": 1800, "TotalBsmtSF": 1000, "FullBath": 2, "BedroomAbvGr": 3, "GarageCars": 2, "Neighborhood": "NridgHt", "BldgType": "1Fam", "HouseStyle": "2Story", "KitchenQual": "Gd"}'
```

### 3.5 Romperla a propósito (validación)

> Pregunta a la clase **antes de enviar**: ¿qué código creen que va a responder?

**Calidad fuera de rango (`OverallQual: 15`) → 422**

```bash
curl -i -X POST http://127.0.0.1:8000/predict -H "Content-Type: application/json" -d '{"LotArea": 9000, "OverallQual": 15, "OverallCond": 5, "YearBuilt": 2005, "YearRemodAdd": 2006, "GrLivArea": 1800, "TotalBsmtSF": 1000, "FullBath": 2, "BedroomAbvGr": 3, "GarageCars": 2, "Neighborhood": "CollgCr", "BldgType": "1Fam", "HouseStyle": "2Story", "KitchenQual": "Gd"}'
```

**Área negativa (`GrLivArea: -100`) → 422**

```bash
curl -i -X POST http://127.0.0.1:8000/predict -H "Content-Type: application/json" -d '{"LotArea": 9000, "OverallQual": 7, "OverallCond": 5, "YearBuilt": 2005, "YearRemodAdd": 2006, "GrLivArea": -100, "TotalBsmtSF": 1000, "FullBath": 2, "BedroomAbvGr": 3, "GarageCars": 2, "Neighborhood": "CollgCr", "BldgType": "1Fam", "HouseStyle": "2Story", "KitchenQual": "Gd"}'
```

**Categoría no permitida (`KitchenQual: "Excelente"`) → 422**

```bash
curl -i -X POST http://127.0.0.1:8000/predict -H "Content-Type: application/json" -d '{"LotArea": 9000, "OverallQual": 7, "OverallCond": 5, "YearBuilt": 2005, "YearRemodAdd": 2006, "GrLivArea": 1800, "TotalBsmtSF": 1000, "FullBath": 2, "BedroomAbvGr": 3, "GarageCars": 2, "Neighborhood": "CollgCr", "BldgType": "1Fam", "HouseStyle": "2Story", "KitchenQual": "Excelente"}'
```

**Campo faltante (sin `GrLivArea`) → 422**

```bash
curl -i -X POST http://127.0.0.1:8000/predict -H "Content-Type: application/json" -d '{"LotArea": 9000, "OverallQual": 7, "OverallCond": 5, "YearBuilt": 2005, "YearRemodAdd": 2006, "TotalBsmtSF": 1000, "FullBath": 2, "BedroomAbvGr": 3, "GarageCars": 2, "Neighborhood": "CollgCr", "BldgType": "1Fam", "HouseStyle": "2Story", "KitchenQual": "Gd"}'
```

**Remodelada antes de construida (`YearRemodAdd: 1990`, `YearBuilt: 2005`) → 422**

```bash
curl -i -X POST http://127.0.0.1:8000/predict -H "Content-Type: application/json" -d '{"LotArea": 9000, "OverallQual": 7, "OverallCond": 5, "YearBuilt": 2005, "YearRemodAdd": 1990, "GrLivArea": 1800, "TotalBsmtSF": 1000, "FullBath": 2, "BedroomAbvGr": 3, "GarageCars": 2, "Neighborhood": "CollgCr", "BldgType": "1Fam", "HouseStyle": "2Story", "KitchenQual": "Gd"}'
```

> Esta regla compara **dos campos**, por eso vive en `main.py` y no en `schemas.py`.

**Batch vacío → 422**

```bash
curl -i -X POST http://127.0.0.1:8000/predict/batch -H "Content-Type: application/json" -d '{"casas": []}'
```

**Barrio desconocido (`Neighborhood: "Laureles"`) → ¡200!**

```bash
curl -i -X POST http://127.0.0.1:8000/predict -H "Content-Type: application/json" -d '{"LotArea": 9000, "OverallQual": 7, "OverallCond": 5, "YearBuilt": 2005, "YearRemodAdd": 2006, "GrLivArea": 1800, "TotalBsmtSF": 1000, "FullBath": 2, "BedroomAbvGr": 3, "GarageCars": 2, "Neighborhood": "Laureles", "BldgType": "1Fam", "HouseStyle": "2Story", "KitchenQual": "Gd"}'
```

> **No falla** gracias al `OneHotEncoder(handle_unknown="ignore")` del módulo 07: las 25 columnas de barrio quedan en 0 y el modelo predice con las demás variables. La predicción es **menos confiable**, porque el modelo no sabe nada del barrio.

### 3.6 ¿Cómo leer un error 422?

Ejemplo de respuesta con `OverallQual: 15`:

```json
{
  "detail": [
    {
      "type": "less_than_equal",
      "loc": ["body", "OverallQual"],
      "msg": "Input should be less than or equal to 10",
      "input": 15
    }
  ]
}
```

| Campo | Qué dice |
|---|---|
| `loc` | **Dónde** está el problema: en el cuerpo (`body`), campo `OverallQual` |
| `msg` | **Qué** está mal: debe ser menor o igual a 10 |
| `input` | **Qué** se recibió: 15 |

El modelo **nunca vio** ese pedido: Pydantic lo rechazó antes.

---

## Parte 4. Otras formas de consumir la API

| Forma | Comando o dirección |
|---|---|
| Navegador | http://127.0.0.1:8000/docs → endpoint → **Try it out** → **Execute** |
| Script de Python | `uv run python 08-API-FastAPI/scripts/cliente.py` |
| Notebook | `08-API-FastAPI/notebooks/01_consumir_api.ipynb` |
| Pruebas automáticas | `uv run pytest -v` (no necesita el servidor encendido) |

---

## Resumen

```
1. Entrenar:   uv run python 07-Pipelines/scripts/train.py --buscar
2. Levantar:   uv run uvicorn api.main:app --reload --app-dir 08-API-FastAPI
3. Navegador:  http://127.0.0.1:8000/docs
4. Terminal:   curl -X POST http://127.0.0.1:8000/predict -H "Content-Type: application/json" -d @08-API-FastAPI/ejemplos/casa.json
5. Apagar:     Ctrl + C
```
