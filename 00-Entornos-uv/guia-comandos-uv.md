# Guía de comandos de `uv`

Referencia rápida de los comandos de `uv` que se usan en el curso, organizada por tarea. Cada sección explica qué hace el comando, cuándo usarlo y qué archivos modifica.

> Versión de referencia: `uv 0.12`. Para ver todas las opciones de un comando, ejecuta `uv <comando> --help` (por ejemplo, `uv add --help`).

## Contenido

1. [Instalar y actualizar uv](#1-instalar-y-actualizar-uv)
2. [Gestionar versiones de Python](#2-gestionar-versiones-de-python)
3. [Crear un proyecto](#3-crear-un-proyecto)
4. [Crear y usar un entorno virtual](#4-crear-y-usar-un-entorno-virtual)
5. [Agregar dependencias](#5-agregar-dependencias)
6. [Quitar dependencias](#6-quitar-dependencias)
7. [Grupos de dependencias](#7-grupos-de-dependencias)
8. [Dependencias opcionales (extras)](#8-dependencias-opcionales-extras)
9. [Bloquear y sincronizar: `uv lock` y `uv sync`](#9-bloquear-y-sincronizar-uv-lock-y-uv-sync)
10. [Actualizar dependencias](#10-actualizar-dependencias)
11. [Ejecutar código](#11-ejecutar-código)
12. [Inspeccionar el entorno](#12-inspeccionar-el-entorno)
13. [Herramientas globales: `uvx` y `uv tool`](#13-herramientas-globales-uvx-y-uv-tool)
14. [Compatibilidad con pip y `requirements.txt`](#14-compatibilidad-con-pip-y-requirementstxt)
15. [Caché](#15-caché)
16. [Flujos de trabajo frecuentes](#16-flujos-de-trabajo-frecuentes)
17. [Resumen de comandos](#17-resumen-de-comandos)

---

## 1. Instalar y actualizar uv

| Sistema | Opción | Comando |
|---|---|---|
| macOS | Instalador oficial (recomendado) | `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| macOS | Homebrew | `brew install uv` |
| Linux | Instalador oficial (curl) | `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| Linux | Instalador oficial (wget) | `wget -qO- https://astral.sh/uv/install.sh \| sh` |
| Windows (PowerShell) | Instalador oficial (recomendado) | `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 \| iex"` |
| Windows | winget | `winget install --id=astral-sh.uv -e` |

```bash
uv --version        # verificar la instalación
uv self update      # actualizar uv (si se instaló con el instalador oficial)
brew upgrade uv     # actualizar uv (si se instaló con Homebrew)
winget upgrade --id=astral-sh.uv -e   # actualizar uv (si se instaló con winget)
```

Después de instalar, cierra y vuelve a abrir la terminal para que el comando `uv` quede disponible. Si aún no se reconoce, la carpeta de instalación es `~/.local/bin` en macOS y Linux (ejecuta `source $HOME/.local/bin/env`) y `%USERPROFILE%\.local\bin` en Windows (cierra todas las ventanas de PowerShell y abre una nueva).

---

## 2. Gestionar versiones de Python

`uv` descarga e instala versiones de Python por sí mismo. No es necesario instalar Python desde python.org ni usar `pyenv`.

```bash
# Ver las versiones disponibles y las instaladas
uv python list
uv python list --only-installed

# Instalar una o varias versiones
uv python install 3.14
uv python install 3.12 3.13

# Fijar la versión del proyecto actual (crea o modifica .python-version)
uv python pin 3.14

# Ver qué intérprete usaría uv en esta carpeta
uv python find

# Actualizar a la última versión de parche (3.14.x)
uv python upgrade 3.14

# Desinstalar una versión
uv python uninstall 3.12
```

**¿Dónde queda definida la versión del proyecto?** En dos lugares que trabajan juntos:

| Archivo | Contenido | Para qué sirve |
|---|---|---|
| `.python-version` | `3.14` | La versión que `uv` usa para crear `.venv` |
| `pyproject.toml` | `requires-python = ">=3.14"` | Las versiones con las que el proyecto es compatible |

**Cambiar la versión de Python de un proyecto existente:**

```bash
uv python pin 3.13        # 1. cambia .python-version
# 2. si hace falta, ajusta requires-python en pyproject.toml
uv sync                   # 3. uv recrea .venv con la nueva versión
```

**Usar una versión puntual sin cambiar el proyecto:**

```bash
uv run --python 3.13 python -V
```

---

## 3. Crear un proyecto

```bash
# Proyecto nuevo en una carpeta nueva
uv init mi-proyecto
cd mi-proyecto

# Proyecto nuevo indicando la versión de Python
uv init mi-proyecto --python 3.14

# Convertir la carpeta actual en un proyecto
uv init

# Proyecto mínimo: solo crea pyproject.toml
uv init mi-proyecto --bare
```

Estructura que se crea:

```
mi-proyecto/
├── .python-version   ← versión de Python del proyecto
├── pyproject.toml    ← metadatos y dependencias
├── README.md
└── main.py           ← archivo de ejemplo (puede borrarse)
```

`uv init` también inicializa un repositorio Git si la carpeta no está dentro de uno. Para evitarlo, usa `--vcs none`.

Los archivos `.venv/` y `uv.lock` se crean la primera vez que ejecutas `uv add`, `uv sync` o `uv run`.

**Tipos de proyecto:**

| Opción | Cuándo usarla |
|---|---|
| `--app` (por defecto) | Scripts, notebooks, análisis. Es el caso del proyecto del curso |
| `--package` | Cuando el código de `src/` se debe instalar como paquete importable (como `src/intro_analitica` en este repositorio) |
| `--lib` | Librerías pensadas para publicarse y reutilizarse en otros proyectos |

---

## 4. Crear y usar un entorno virtual

En un proyecto con `pyproject.toml` normalmente **no hace falta crear el entorno a mano**: `uv sync`, `uv add` y `uv run` lo crean automáticamente en `.venv/`. El comando `uv venv` es útil cuando se trabaja sin `pyproject.toml` o se quiere controlar la creación.

```bash
# Crear .venv con la versión de .python-version (o la disponible por defecto)
uv venv

# Crear .venv con una versión específica
uv venv --python 3.14

# Crear el entorno con otro nombre
uv venv entorno-pruebas

# Recrear el entorno desde cero (borra el contenido anterior)
uv venv --clear
```

**Activar y desactivar** (opcional, porque `uv run` ya ejecuta dentro del entorno):

| Sistema | Terminal | Activar | Desactivar |
|---|---|---|---|
| macOS / Linux | zsh / bash | `source .venv/bin/activate` | `deactivate` |
| macOS / Linux | fish | `source .venv/bin/activate.fish` | `deactivate` |
| Windows | PowerShell | `.venv\Scripts\Activate.ps1` | `deactivate` |
| Windows | CMD | `.venv\Scripts\activate.bat` | `deactivate` |
| Windows | Git Bash | `source .venv/Scripts/activate` | `deactivate` |

**Comprobar que el entorno está activo:** la línea de la terminal empieza con `(nombre-del-entorno)`, y `which python` (macOS/Linux) o `Get-Command python` (Windows PowerShell) apunta a la carpeta `.venv`.

**Windows:** si PowerShell responde que "la ejecución de scripts está deshabilitada", ejecuta una vez `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`.

**Si el entorno se daña:** se puede borrar la carpeta `.venv/` y ejecutar `uv sync`. No se pierde nada, porque todo lo necesario está en `pyproject.toml` y `uv.lock`.

---

## 5. Agregar dependencias

`uv add` hace tres cosas: escribe la dependencia en `pyproject.toml`, actualiza `uv.lock` e instala el paquete en `.venv/`.

```bash
# Una o varias librerías
uv add pandas
uv add pandas numpy matplotlib

# Con restricción de versión (usar comillas por los símbolos < >)
uv add "pandas>=3.0"
uv add "scikit-learn>=1.8,<2"
uv add "numpy==2.3.2"

# Con extras del paquete (funcionalidades opcionales que trae la librería)
uv add "uvicorn[standard]"

# Desde un repositorio de GitHub
uv add git+https://github.com/usuario/repositorio
uv add git+https://github.com/usuario/repositorio --tag v1.0.0

# Desde una carpeta local, en modo editable (los cambios se ven sin reinstalar)
uv add --editable ../mi-libreria

# Desde un requirements.txt existente
uv add -r requirements.txt
```

Resultado en `pyproject.toml`:

```toml
[project]
dependencies = [
    "pandas>=3.0",
    "scikit-learn>=1.8,<2",
    "uvicorn[standard]>=0.46",
]
```

> Si no indicas versión, `uv` agrega un límite inferior con la versión instalada (por ejemplo `pandas>=3.0.3`). Así el proyecto no acepta versiones más antiguas que la que se probó.

---

## 6. Quitar dependencias

```bash
uv remove matplotlib                  # de las dependencias principales
uv remove --dev pytest                # del grupo dev
uv remove --group docs mkdocs         # de un grupo específico
uv remove --optional api fastapi      # de un extra
```

`uv remove` quita la librería de `pyproject.toml`, actualiza `uv.lock` y la desinstala de `.venv/`, junto con las dependencias que solo ella necesitaba.

> No edites `pyproject.toml` a mano para quitar librerías sin ejecutar después `uv sync`: el entorno quedaría desincronizado.

---

## 7. Grupos de dependencias

Los **grupos** separan las librerías que no hacen falta para ejecutar el proyecto, sino para **desarrollarlo**: pruebas, *linters*, documentación, notebooks. No se publican con el paquete.

```bash
# Grupo "dev" (atajo especial)
uv add --dev pytest ruff

# Grupos con nombre propio
uv add --group notebooks jupyter ipykernel
uv add --group docs mkdocs
```

Resultado en `pyproject.toml`:

```toml
[dependency-groups]
dev = ["pytest>=8.4", "ruff>=0.13"]
notebooks = ["jupyter>=1.1", "ipykernel>=6.30"]
docs = ["mkdocs>=1.6"]
```

**Instalar según los grupos:**

| Comando | Qué instala |
|---|---|
| `uv sync` | Dependencias principales + grupo `dev` (incluido por defecto) |
| `uv sync --no-dev` | Solo las principales (por ejemplo, para producción) |
| `uv sync --group docs` | Principales + `dev` + `docs` |
| `uv sync --all-groups` | Principales + todos los grupos |
| `uv sync --only-group docs` | Solo el grupo `docs` |
| `uv sync --no-group notebooks` | Todo lo que se instala por defecto, excepto `notebooks` |

Las mismas opciones funcionan con `uv run` (por ejemplo, `uv run --group docs mkdocs serve`).

**Instalar otros grupos por defecto** (opcional), en `pyproject.toml`:

```toml
[tool.uv]
default-groups = ["dev", "notebooks"]
```

---

## 8. Dependencias opcionales (extras)

Los **extras** son funcionalidades opcionales **del propio proyecto** que el usuario decide si instala. Por ejemplo, la API del módulo 08 podría ser un extra para quien solo quiere entrenar modelos.

```bash
uv add --optional api fastapi "uvicorn[standard]"
```

```toml
[project.optional-dependencies]
api = ["fastapi>=0.136", "uvicorn[standard]>=0.46"]
```

```bash
uv sync --extra api          # instala las principales + el extra api
uv sync --all-extras         # instala todos los extras
```

**¿Grupo o extra?**

| | Grupo (`--group`, `--dev`) | Extra (`--optional`) |
|---|---|---|
| Para quién | El equipo que desarrolla | Quien usa el proyecto |
| Ejemplos | pytest, ruff, jupyter | API, conexión a una base de datos, visualizaciones extra |
| Se publica con el paquete | No | Sí |

En los proyectos del curso, casi siempre basta con dependencias principales y el grupo `dev`.

---

## 9. Bloquear y sincronizar: `uv lock` y `uv sync`

| Comando | Qué hace | Modifica |
|---|---|---|
| `uv lock` | Resuelve las versiones exactas a partir de `pyproject.toml` | `uv.lock` |
| `uv sync` | Instala en `.venv/` exactamente lo que dice `uv.lock` (y lo actualiza si `pyproject.toml` cambió) | `.venv/` y, si hace falta, `uv.lock` |

```bash
uv lock                 # regenerar el lock (por ejemplo, después de editar pyproject.toml a mano)
uv lock --check         # verificar que uv.lock está al día con pyproject.toml (útil en CI)
uv sync                 # instalar / sincronizar el entorno
uv sync --locked        # sincronizar, pero fallar si uv.lock no está al día
uv sync --frozen        # usar uv.lock tal cual, sin revisar pyproject.toml
```

**Regla del curso:** `pyproject.toml` y `uv.lock` siempre se suben a Git. `.venv/` nunca.

---

## 10. Actualizar dependencias

```bash
# Ver qué librerías tienen versiones más nuevas disponibles
uv tree --outdated --depth 1

# Actualizar UNA librería dentro del rango permitido por pyproject.toml
uv lock --upgrade-package pandas
uv sync

# Actualizar TODAS las librerías dentro de sus rangos
uv lock --upgrade
uv sync

# Cambiar el rango permitido (por ejemplo, pasar a una versión mayor nueva)
uv add "pandas>=3.1"
```

> Actualiza en una rama, ejecuta los notebooks y las pruebas, y solo después une los cambios a `main`. Las actualizaciones grandes pueden cambiar resultados.

---

## 11. Ejecutar código

`uv run` verifica que el entorno esté sincronizado con `uv.lock` y ejecuta el comando dentro de `.venv/`, sin necesidad de activarlo.

```bash
uv run python script.py
uv run python -m src.train           # ejecutar un módulo
uv run jupyter lab
uv run pytest -v
uv run uvicorn api.main:app --reload

# Agregar una librería solo para esta ejecución (no modifica pyproject.toml)
uv run --with rich python script.py

# Ejecutar con otra versión de Python
uv run --python 3.13 python -V

# Ejecutar sin sincronizar antes (más rápido, si sabes que el entorno está al día)
uv run --no-sync python script.py
```

---

## 12. Inspeccionar el entorno

```bash
uv tree                      # árbol de dependencias del proyecto
uv tree --depth 1            # solo las dependencias directas
uv tree --invert --package numpy   # ¿quién necesita numpy?
uv pip list                  # paquetes instalados en .venv
uv pip show pandas           # detalles de un paquete (versión, ubicación, dependencias)
uv python find               # ruta del intérprete que usa el proyecto
```

---

## 13. Herramientas globales: `uvx` y `uv tool`

Algunas herramientas de línea de comandos no pertenecen a un proyecto, sino a tu computador (por ejemplo, `ruff` o `cookiecutter`).

```bash
# Ejecutar una herramienta sin instalarla (entorno temporal)
uvx ruff check .
uv tool run ruff check .       # forma larga de uvx

# Instalar una herramienta de forma permanente
uv tool install ruff
uv tool list
uv tool upgrade ruff
uv tool uninstall ruff
```

---

## 14. Compatibilidad con pip y `requirements.txt`

`uv` incluye una interfaz compatible con `pip`. Es útil para proyectos que todavía no usan `pyproject.toml`.

```bash
uv pip install pandas                 # como pip install, pero en .venv
uv pip install -r requirements.txt
uv pip uninstall pandas
uv pip freeze > requirements.txt
```

**Migrar un proyecto con `requirements.txt` a `uv`:**

```bash
uv init --bare
uv add -r requirements.txt
```

**Generar un `requirements.txt` desde `uv.lock`** (por ejemplo, para una plataforma que solo acepta ese formato):

```bash
uv export --format requirements-txt --no-hashes -o requirements.txt
uv export --format requirements-txt --no-dev -o requirements.txt   # sin el grupo dev
```

> Dentro de un proyecto con `pyproject.toml`, prefiere `uv add` y `uv remove` en lugar de `uv pip install`: `uv pip` no actualiza `pyproject.toml` ni `uv.lock`.

---

## 15. Caché

`uv` guarda los paquetes descargados en una caché global para no descargarlos dos veces.

```bash
uv cache dir      # ubicación de la caché
uv cache size     # espacio que ocupa
uv cache prune    # eliminar entradas que ya no se usan
uv cache clean    # vaciar toda la caché
```

---

## 16. Flujos de trabajo frecuentes

### Empezar un proyecto desde cero

```bash
uv init proyecto-equipo --python 3.14
cd proyecto-equipo
uv add pandas numpy matplotlib seaborn scikit-learn
uv add --dev pytest ruff
uv add --group notebooks jupyter ipykernel
git init && git add . && git commit -m "feat: estructura inicial"
```

### Clonar el proyecto de un compañero

```bash
git clone <url>
cd <repositorio>
uv sync                 # instala Python (si falta) y todas las dependencias
uv run jupyter lab
```

### Agregar una librería durante el proyecto

```bash
git switch -c feat/agregar-xgboost
uv add xgboost
git add pyproject.toml uv.lock
git commit -m "feat: agrega xgboost"
# Los demás integrantes, después del merge: git pull && uv sync
```

### Resolver un conflicto de Git en `uv.lock`

No se edita a mano. Se acepta cualquiera de las dos versiones y se regenera:

```bash
git checkout --theirs uv.lock    # o --ours
uv lock
git add uv.lock
```

### Preparar el entorno para producción

```bash
uv sync --locked --no-dev
```

---

## 17. Resumen de comandos

| Tarea | Comando |
|---|---|
| Ver la versión de uv | `uv --version` |
| Actualizar uv | `uv self update` |
| Instalar Python | `uv python install 3.14` |
| Fijar la versión de Python | `uv python pin 3.14` |
| Ver versiones de Python | `uv python list` |
| Crear un proyecto | `uv init nombre --python 3.14` |
| Crear un entorno virtual | `uv venv` |
| Recrear el entorno | `uv venv --clear` o borrar `.venv/` y `uv sync` |
| Agregar una dependencia | `uv add paquete` |
| Agregar con versión | `uv add "paquete>=1.0,<2"` |
| Agregar al grupo dev | `uv add --dev paquete` |
| Agregar a un grupo | `uv add --group nombre paquete` |
| Agregar un extra | `uv add --optional nombre paquete` |
| Quitar una dependencia | `uv remove paquete` |
| Quitar de un grupo | `uv remove --group nombre paquete` |
| Regenerar el lock | `uv lock` |
| Sincronizar el entorno | `uv sync` |
| Sincronizar sin dev | `uv sync --no-dev` |
| Sincronizar todos los grupos | `uv sync --all-groups` |
| Actualizar un paquete | `uv lock --upgrade-package paquete && uv sync` |
| Actualizar todo | `uv lock --upgrade && uv sync` |
| Ejecutar un script | `uv run python script.py` |
| Abrir Jupyter | `uv run jupyter lab` |
| Ver el árbol de dependencias | `uv tree` |
| Ver paquetes desactualizados | `uv tree --outdated --depth 1` |
| Listar paquetes instalados | `uv pip list` |
| Exportar requirements.txt | `uv export --format requirements-txt -o requirements.txt` |
| Ejecutar una herramienta suelta | `uvx herramienta` |
| Limpiar la caché | `uv cache clean` |

---

**Documentación oficial:** [docs.astral.sh/uv](https://docs.astral.sh/uv/)

**Regresar a:** [README del módulo 00](README.md)
