# Módulo 00: Entornos virtuales con `uv`

> **Objetivo:** que cada estudiante tenga un entorno de Python **reproducible** y que el equipo pueda decir "en mi máquina funciona… **y en la tuya también**".

**Duración sugerida:** 2 horas (1 h de explicación y práctica guiada, 1 h de trabajo en salas)

## Contenido

| Archivo | Para qué sirve |
|---|---|
| `README.md` | Teoría y paso a paso (estás aquí) |
| `guia-comandos-uv.md` | Guía de referencia de comandos de uv: Python, entornos, dependencias, grupos, lock y sync |
| `notebooks/01_mi_primer_entorno.ipynb` | Explorar "por dentro" en qué entorno corre tu código |
| `ejercicios/EJERCICIOS.md` | Actividad para salas de Zoom |
| `presentacion/00-Entornos-uv.pptx` | Diapositivas de la clase |

---

## 1. ¿Qué problema resuelve un entorno virtual?

Imagina que el equipo hace un trabajo en grupo y cada uno tiene una **versión distinta de Excel**: a uno le abren las fórmulas y a otro no. Con Python pasa lo mismo:

- Laura tiene `pandas 2.1` y su código usa una función que en `pandas 3.0` cambió.
- Andrés instaló todo "a nivel global" y ahora dos proyectos necesitan versiones distintas de `scikit-learn`.
- El profesor corre el notebook de entrega y… `ModuleNotFoundError`.

Un **entorno virtual** es una carpeta (`.venv/`) con **su propio Python y sus propias librerías**, aislada del resto del computador. Cada proyecto tiene el suyo.

```
Tu computador
├── Python del sistema   ← ¡no lo toques!
├── proyecto_A/.venv     ← pandas 2.2, scikit-learn 1.5
└── intro_analitica/.venv← pandas 3.0, scikit-learn 1.8, Python 3.14
```

## 2. ¿Por qué `uv`?

| Herramienta | Qué hace | Lo que la hace incómoda |
|---|---|---|
| `pip` + `venv` | Instala paquetes / crea entornos | Son dos herramientas, no hay *lockfile* y no instala Python |
| `conda` | Entornos + paquetes | Pesada y lenta, con canales que pueden chocar |
| `pyenv` | Instala versiones de Python | Solo hace eso |
| **`uv`** | **Todo lo anterior en un solo binario** | Muy rápido (está escrito en Rust) y genera `uv.lock` automáticamente |

```
┌─────────────────────────────────────────────────────┐
│  uv reemplaza:   pip + venv + pip-tools + pyenv     │
└─────────────────────────────────────────────────────┘
```

## 3. Instalar `uv` (una sola vez por computador)

No necesitas instalar Python antes: `uv` descarga la versión que pida cada proyecto. Elige las instrucciones de tu sistema operativo.

### macOS

Abre la aplicación **Terminal** (Cmd + Espacio, escribe "Terminal") y ejecuta **una** de estas opciones:

```bash
# Opción A (recomendada): instalador oficial
curl -LsSf https://astral.sh/uv/install.sh | sh

# Opción B: Homebrew (si ya lo tienes instalado)
brew install uv
```

### Linux (Ubuntu, Debian, Fedora, etc.)

Abre una terminal y ejecuta:

```bash
# Con curl
curl -LsSf https://astral.sh/uv/install.sh | sh

# Si tu sistema no tiene curl, con wget
wget -qO- https://astral.sh/uv/install.sh | sh
```

### Windows

Abre **PowerShell** (menú Inicio, escribe "PowerShell") y ejecuta **una** de estas opciones:

```powershell
# Opción A (recomendada): instalador oficial
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Opción B: winget (gestor de paquetes de Windows)
winget install --id=astral-sh.uv -e
```

### Verificar la instalación (todos los sistemas)

**Cierra la terminal y abre una nueva** (para que reconozca el comando) y ejecuta:

```bash
uv --version
```

Debe mostrar algo como `uv 0.12.x`.

### Si aparece "uv: command not found" o "uv no se reconoce"

El instalador deja `uv` en una carpeta que la terminal todavía no conoce:

| Sistema | Carpeta de instalación | Solución |
|---|---|---|
| macOS / Linux | `~/.local/bin` | Cierra y abre la terminal, o ejecuta `source $HOME/.local/bin/env` |
| Windows | `%USERPROFILE%\.local\bin` | Cierra **todas** las ventanas de PowerShell y abre una nueva. Si persiste, reinicia la sesión de Windows |

### Actualizar `uv` más adelante

| Instalado con | Comando |
|---|---|
| Instalador oficial (cualquier sistema) | `uv self update` |
| Homebrew | `brew upgrade uv` |
| winget | `winget upgrade --id=astral-sh.uv -e` |

## 4. Paso a paso: tu primer proyecto con `uv`

### Paso 1: Crear el proyecto

```bash
uv init mi-proyecto --python 3.14
cd mi-proyecto
```

Se crea esta estructura:

```
mi-proyecto/
├── .python-version   ← "3.14": la versión de Python del proyecto
├── pyproject.toml    ← la "lista de mercado": qué librerías necesitas
├── README.md
└── main.py
```

### Paso 2: Agregar librerías

```bash
uv add pandas matplotlib      # dependencias del proyecto
uv add --dev pytest ruff      # dependencias solo para desarrollo
```

Al ejecutar `uv add` pasan tres cosas:

1. Se crea `.venv/` si no existía.
2. Se escribe la librería en `pyproject.toml`.
3. Se crea o actualiza **`uv.lock`** con la versión **exacta** que se instaló.

### Paso 3: Ejecutar código dentro del entorno

```bash
uv run python main.py
uv run jupyter lab
uv run pytest
```

`uv run` se asegura de que el entorno esté sincronizado **y** ejecuta el comando dentro de `.venv`. No tienes que activar nada.

Si prefieres activar el entorno para no escribir `uv run` cada vez, consulta la **sección 5**, con los comandos para macOS, Linux y Windows.

### Paso 4: Reproducir el entorno en otro computador

Tu compañero clona el repositorio y ejecuta **un solo comando**:

```bash
uv sync
```

`uv` lee `uv.lock` e instala **exactamente** las mismas versiones que tienes tú.

## 5. Activar y desactivar el entorno virtual

### ¿Es obligatorio activarlo?

No. Con `uv run <comando>` el comando se ejecuta dentro de `.venv` sin activar nada, y es la forma recomendada en el curso. Activar el entorno es útil cuando vas a escribir muchos comandos seguidos y prefieres usar `python`, `jupyter lab` o `pytest` directamente, sin anteponer `uv run`.

| Sin activar | Con el entorno activado |
|---|---|
| `uv run python script.py` | `python script.py` |
| `uv run jupyter lab` | `jupyter lab` |
| `uv run pytest` | `pytest` |

### Paso 1: Crear el entorno (si aún no existe)

Desde la carpeta del proyecto:

```bash
uv sync      # crea .venv e instala las dependencias del proyecto
# o, en una carpeta sin pyproject.toml:
uv venv      # crea un .venv vacío
```

### Paso 2: Activarlo según tu sistema y tu terminal

| Sistema | Terminal | Comando para activar |
|---|---|---|
| macOS | Terminal (zsh) | `source .venv/bin/activate` |
| Linux | bash / zsh | `source .venv/bin/activate` |
| macOS / Linux | fish | `source .venv/bin/activate.fish` |
| Windows | PowerShell | `.venv\Scripts\Activate.ps1` |
| Windows | Símbolo del sistema (CMD) | `.venv\Scripts\activate.bat` |
| Windows | Git Bash | `source .venv/Scripts/activate` |

> Observa la diferencia de carpeta: en macOS y Linux los ejecutables están en `.venv/bin/`; en Windows, en `.venv\Scripts\`.

### Paso 3: Comprobar que está activo

Al activarlo, el inicio de la línea de la terminal muestra el nombre del entorno entre paréntesis:

```
(intro-analitica) usuario@equipo intro_analitica %
```

Para confirmarlo, revisa qué Python se está usando:

| Sistema | Comando | Resultado esperado |
|---|---|---|
| macOS / Linux | `which python` | `.../intro_analitica/.venv/bin/python` |
| Windows (PowerShell) | `Get-Command python` | `...\intro_analitica\.venv\Scripts\python.exe` |
| Windows (CMD) | `where python` | La primera línea debe apuntar a `.venv\Scripts\python.exe` |
| Cualquiera | `python -c "import sys; print(sys.prefix)"` | La ruta de la carpeta `.venv` |

### Paso 4: Desactivarlo

En todos los sistemas:

```bash
deactivate
```

El nombre entre paréntesis desaparece y la terminal vuelve a usar el Python del sistema.

### Problemas frecuentes al activar

| Síntoma | Causa | Solución |
|---|---|---|
| Windows: "la ejecución de scripts está deshabilitada en este sistema" | Política de seguridad de PowerShell | Ejecuta una vez `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` y vuelve a intentarlo |
| "No such file or directory: .venv/bin/activate" | No estás en la carpeta del proyecto o el entorno no existe | Verifica con `ls` (o `dir` en Windows) que exista `.venv`; si no, ejecuta `uv sync` |
| Usaste la ruta de otro sistema | `bin` es para macOS/Linux y `Scripts` para Windows | Usa el comando de la tabla del paso 2 |
| Activaste el entorno y `python` sigue siendo el del sistema | La terminal tiene un alias de `python` | Cierra y abre la terminal; en macOS prueba también `python3` |

### En VS Code

VS Code activa el entorno automáticamente en las terminales nuevas cuando seleccionas el intérprete `.venv` (`Cmd/Ctrl + Shift + P` → **Python: Select Interpreter**). Ver la sección 8.

## 6. `pyproject.toml` vs `uv.lock`

| | `pyproject.toml` | `uv.lock` |
|---|---|---|
| Analogía | Lista de mercado: "leche, pan" | Factura: "Leche Colanta 1 L, lote 4532" |
| Lo escribes tú | (o con `uv add`) | lo genera `uv` |
| Versiones | Rangos (`pandas>=3.0`) | Exactas (`pandas==3.0.3` + hash) |
| ¿Va a git? | Sí | **Sí, siempre** |

Y **`.venv/` NUNCA va a git**: pesa cientos de MB, depende del sistema operativo y se regenera con `uv sync`.

## 7. Comandos que vas a usar todo el semestre

La referencia completa, con grupos de dependencias, extras, actualización y flujos de trabajo, está en [`guia-comandos-uv.md`](guia-comandos-uv.md).

| Comando | Qué hace |
|---|---|
| `uv init` | Crea un proyecto nuevo |
| `uv python install 3.14` | Instala una versión de Python |
| `uv python pin 3.14` | Fija la versión del proyecto (`.python-version`) |
| `uv add <paquete>` | Agrega una dependencia |
| `uv add --dev <paquete>` | Agrega una dependencia de desarrollo |
| `uv remove <paquete>` | Quita una dependencia |
| `uv sync` | Instala o actualiza el entorno según `uv.lock` |
| `uv lock --upgrade` | Actualiza las versiones del lock dentro de los rangos permitidos |
| `uv run <comando>` | Ejecuta dentro del entorno |
| `uv tree` | Muestra el árbol de dependencias |
| `uv pip list` | Lista lo instalado en `.venv` |

## 8. Jupyter y VS Code con el entorno correcto

**Opción A: Jupyter Lab desde uv (recomendada)**

```bash
uv run jupyter lab
```

**Opción B: VS Code**

1. Abre la carpeta del repositorio en VS Code.
2. `Cmd/Ctrl + Shift + P` → **Python: Select Interpreter** → elige `./.venv/bin/python` (en Windows: `.venv\Scripts\python.exe`).
3. En el notebook, arriba a la derecha: **Select Kernel** → **Python Environments** → `.venv`.

> El error más común del curso es tener el kernel equivocado. Si `import pandas` falla en el notebook pero `uv run python -c "import pandas"` funciona, **el problema es el kernel**.

## 9. Problemas comunes y cómo resolverlos

| Síntoma | Causa probable | Solución |
|---|---|---|
| `uv: command not found` | La terminal no recargó el PATH | Cierra y abre la terminal; en macOS prueba `exec $SHELL` |
| `ModuleNotFoundError` en el notebook | Kernel equivocado | Selecciona el kernel `.venv` (sección 8) |
| En Windows: "la ejecución de scripts está deshabilitada" | Política de PowerShell | `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` |
| `No interpreter found for Python 3.14` | Falta esa versión de Python | `uv python install 3.14` |
| El compañero tiene otras versiones | No se subió `uv.lock` | Haz commit de `uv.lock` y pide al compañero que corra `uv sync` |
| Todo raro, nada funciona | Entorno corrupto | Borra `.venv/` y corre `uv sync` (¡es seguro!) |

## 10. Verifica tu instalación

Desde la raíz del repositorio:

```bash
uv sync
uv run python -V
uv run python -c "import pandas, sklearn; print(pandas.__version__, sklearn.__version__)"
```

El primer comando debe mostrar `Python 3.14.x` y el segundo, las versiones de pandas y scikit-learn sin errores. Después abre `notebooks/01_mi_primer_entorno.ipynb` con el kernel `.venv`: en la Pregunta 2 debe responder "Sí" (estás dentro del entorno virtual).

---

## Checklist del módulo

- [ ] `uv --version` funciona
- [ ] `uv sync` corre sin errores en el repositorio del curso
- [ ] `uv run python -V` muestra Python 3.14 y las librerías del curso se importan sin errores
- [ ] El notebook `01_mi_primer_entorno.ipynb` corre con el kernel `.venv`
- [ ] Sé explicar la diferencia entre `pyproject.toml` y `uv.lock`

**Siguiente:** [Módulo 01: Git y GitHub](../01-Git-GitHub/)
