# Guía práctica de Git y GitHub

Guía paso a paso para la práctica del módulo 01 y referencia de los comandos que todo desarrollador usa en su día a día. Funciona en macOS, Linux y Windows: en Windows se recomienda usar **Git Bash**, que se instala junto con Git.

## Contenido

1. [Conceptos básicos](#1-conceptos-básicos)
2. [Instalación y configuración inicial](#2-instalación-y-configuración-inicial)
3. [Práctica guiada paso a paso](#3-práctica-guiada-paso-a-paso)
4. [Comandos esenciales](#4-comandos-esenciales)
5. [Mensajes de commit: Conventional Commits](#5-mensajes-de-commit-conventional-commits)
6. [Qué no se sube: `.gitignore`](#6-qué-no-se-sube-gitignore)
7. [Deshacer cambios sin miedo](#7-deshacer-cambios-sin-miedo)
8. [Errores frecuentes y cómo resolverlos](#8-errores-frecuentes-y-cómo-resolverlos)
9. [Para ir más allá: ramas](#9-para-ir-más-allá-ramas)
10. [Resumen de comandos](#10-resumen-de-comandos)

---

## 1. Conceptos básicos

| Concepto | Qué es | Analogía |
|---|---|---|
| **Git** | Programa que guarda el historial de cambios de un proyecto | Los puntos de guardado de un videojuego |
| **GitHub** | Sitio web donde se guarda una copia del proyecto en la nube | La nube donde se respalda la partida |
| **Repositorio (repo)** | Carpeta del proyecto con su historial | El álbum con todas las fotos del proyecto |
| **Commit** | Una "foto" del proyecto en un momento dado, con un mensaje | Una foto con su descripción |
| **Remoto (`origin`)** | La copia del repositorio que está en GitHub | El respaldo en la nube |
| **Push** | Subir tus commits a GitHub | Subir las fotos a la nube |
| **Pull** | Traer a tu computador los commits nuevos de GitHub | Descargar las fotos que subieron otros |
| **Clone** | Descargar un repositorio completo por primera vez | Copiar el álbum completo |

### Las tres zonas de Git

```
 Carpeta de trabajo   --git add-->   Staging   --git commit-->   Repositorio local   --git push-->   GitHub
 (tus archivos)                     (preparados)                 (historial)                        (remoto)
                                                                         <---------- git pull ----------
```

1. **Carpeta de trabajo:** los archivos como los ves y editas.
2. **Staging (área de preparación):** los cambios que elegiste para el próximo commit.
3. **Repositorio local:** el historial de commits en tu computador.

Y fuera de tu computador está **GitHub**, que se sincroniza con `push` y `pull`.

---

## 2. Instalación y configuración inicial

### Instalar Git

| Sistema | Cómo instalar |
|---|---|
| macOS | Ejecutar `git --version` en la Terminal; si no está, macOS ofrece instalarlo. También `brew install git` |
| Windows | Instalador de [git-scm.com/download/win](https://git-scm.com/download/win) (incluye Git Bash) o `winget install --id Git.Git -e --source winget` |
| Linux (Ubuntu/Debian) | `sudo apt install git` |

### Instalar GitHub CLI (`gh`)

| Sistema | Comando |
|---|---|
| macOS | `brew install gh` |
| Windows | `winget install --id GitHub.cli` |
| Linux (Ubuntu/Debian) | `sudo apt install gh` |

Después de instalar, cierra y vuelve a abrir la terminal.

### Configurar tu identidad (una sola vez por computador)

```bash
git config --global user.name "Nombre Apellido"
git config --global user.email "correo@ejemplo.com"     # el mismo correo de tu cuenta de GitHub
git config --global init.defaultBranch main
git config --global pull.rebase false                    # al hacer pull, unir cambios con merge (lo más sencillo)

# Opcional: usar VS Code como editor para los mensajes de Git
git config --global core.editor "code --wait"

# Revisar la configuración
git config --global --list
```

### Iniciar sesión en GitHub

```bash
gh auth login
```

Opciones a elegir: **GitHub.com → HTTPS → Yes (autenticar Git) → Login with a web browser**. Copia el código que aparece, pégalo en el navegador y autoriza.

```bash
gh auth status     # verificar que la sesión quedó activa
```

---

## 3. Práctica guiada paso a paso

### Paso 1. Crear un repositorio en GitHub

**Desde la web:**

1. En [github.com](https://github.com), clic en **New repository**.
2. Nombre: `practica-git`. Marca **Add a README file**.
3. Clic en **Create repository**.

**O desde la terminal, con GitHub CLI:**

```bash
gh repo create practica-git --public --add-readme --clone
cd practica-git
```

### Paso 2. Clonar el repositorio

Si lo creaste desde la web, cópialo a tu computador (botón **Code → HTTPS**):

```bash
git clone https://github.com/<tu-usuario>/practica-git.git
cd practica-git
```

Revisa el estado:

```bash
git status
# On branch main
# nothing to commit, working tree clean
```

### Paso 3. Hacer un cambio y guardarlo (commit)

1. Crea el archivo `presentacion.md` (desde VS Code) con este contenido:

   ```markdown
   # Hola, soy <nombre>
   - Carrera: ...
   - Lenguaje favorito: ...
   ```

2. Mira qué detecta Git:

   ```bash
   git status            # presentacion.md aparece como "Untracked"
   ```

3. Prepara el archivo y guarda la foto:

   ```bash
   git add presentacion.md
   git status            # ahora aparece como "Changes to be committed"
   git commit -m "docs: agrega mi presentación"
   ```

4. Revisa el historial:

   ```bash
   git log --oneline
   ```

### Paso 4. Subir el cambio a GitHub (push)

```bash
git push
```

Recarga la página del repositorio en GitHub: el archivo y el commit ya aparecen.

### Paso 5. Modificar un archivo existente y ver la diferencia

1. Agrega una línea a `presentacion.md`, por ejemplo `- Ciudad: Medellín`.
2. Mira exactamente qué cambió:

   ```bash
   git diff              # líneas con + fueron agregadas; con - fueron eliminadas
   ```

3. Guarda y sube:

   ```bash
   git add presentacion.md
   git commit -m "docs: agrega ciudad a la presentación"
   git push
   ```

### Paso 6. Traer cambios hechos por otra persona (pull)

1. En GitHub (navegador), abre `README.md`, clic en el lápiz (**Edit**), agrega una línea y clic en **Commit changes** con el mensaje `docs: actualiza README desde GitHub`.
2. En tu terminal:

   ```bash
   git pull
   git log --oneline     # aparece el commit hecho desde la web
   ```

### Paso 7. Subir un proyecto que ya existe en tu computador

Este es el caso del proyecto del equipo creado en el módulo 00:

```bash
cd proyecto-<equipo>
git init                                   # si la carpeta aún no es un repositorio
git add .
git commit -m "feat: estructura inicial del proyecto con uv"
gh repo create proyecto-<equipo> --private --source=. --push
```

Sin GitHub CLI (creando primero el repositorio vacío en la web, **sin** README):

```bash
git branch -M main
git remote add origin https://github.com/<usuario>/proyecto-<equipo>.git
git push -u origin main
```

> `-u` (o `--set-upstream`) vincula tu rama local con la de GitHub. Solo se usa en el primer push; después basta con `git push`.

### Paso 8. Trabajar en equipo sobre el mismo repositorio

1. El dueño del repositorio invita a los compañeros: **Settings → Collaborators → Add people**. Cada invitado acepta desde su correo o desde [github.com/notifications](https://github.com/notifications).
2. Los compañeros clonan:

   ```bash
   git clone https://github.com/<usuario>/proyecto-<equipo>.git
   ```

3. El ciclo de trabajo de cada persona:

   ```bash
   git pull                                  # 1. traer lo último
   # ... editar archivos ...
   git status                                # 2. revisar qué cambió
   git add <archivo>                         # 3. preparar
   git commit -m "tipo: descripción"         # 4. guardar
   git pull                                  # 5. traer cambios que otros subieron mientras tanto
   git push                                  # 6. subir
   ```

---

## 4. Comandos esenciales

### Empezar

| Comando | Qué hace |
|---|---|
| `git init` | Convierte la carpeta actual en un repositorio |
| `git clone <url>` | Descarga un repositorio completo de GitHub |
| `gh repo create <nombre>` | Crea un repositorio en GitHub desde la terminal |

### Ver el estado

| Comando | Qué hace |
|---|---|
| `git status` | Qué archivos cambiaron y cuáles están preparados. **Úsalo todo el tiempo** |
| `git diff` | Cambios que aún no están en staging |
| `git diff --staged` | Cambios que ya están en staging (lo que irá en el próximo commit) |
| `git log --oneline` | Historial resumido, un commit por línea |
| `git log --oneline --graph --all` | Historial en forma de árbol, con todas las ramas |
| `git show <hash>` | Detalle de un commit específico |

### Guardar cambios

| Comando | Qué hace |
|---|---|
| `git add <archivo>` | Prepara un archivo para el próximo commit |
| `git add .` | Prepara todos los cambios de la carpeta actual (revisar antes con `git status`) |
| `git commit -m "mensaje"` | Guarda los cambios preparados con un mensaje |
| `git commit -am "mensaje"` | Prepara y guarda los archivos **ya conocidos** por Git (no incluye archivos nuevos) |

### Sincronizar con GitHub

| Comando | Qué hace |
|---|---|
| `git push` | Sube tus commits a GitHub |
| `git push -u origin main` | Primer push: sube y vincula la rama local con la remota |
| `git pull` | Trae los commits nuevos de GitHub y los une con los tuyos |
| `git fetch` | Descarga la información de GitHub **sin** modificar tus archivos (para revisar antes de unir) |
| `git remote -v` | Muestra a qué repositorio de GitHub está conectado |

### Guardar temporalmente (stash)

Útil cuando necesitas hacer `pull` pero tienes cambios a medias que no quieres guardar todavía en un commit:

| Comando | Qué hace |
|---|---|
| `git stash` | Guarda tus cambios a un lado y deja la carpeta limpia |
| `git stash list` | Lista lo guardado |
| `git stash pop` | Recupera los cambios guardados |

---

## 5. Mensajes de commit: Conventional Commits

Formato: **`tipo: descripción`**, en minúscula, en presente y sin punto final.

| Tipo | Cuándo se usa | Ejemplo |
|---|---|---|
| `feat` | Algo nuevo (código, notebook, funcionalidad) | `feat: agrega notebook de EDA` |
| `fix` | Corrección de un error | `fix: corrige ruta del archivo de datos` |
| `docs` | Documentación | `docs: agrega integrantes al README` |
| `refactor` | Reorganizar código sin cambiar lo que hace | `refactor: mueve la limpieza a src/limpieza.py` |
| `style` | Formato sin cambiar la lógica | `style: aplica formato con ruff` |
| `test` | Pruebas | `test: agrega prueba del endpoint /health` |
| `chore` | Mantenimiento (dependencias, configuración) | `chore: agrega pandas con uv add` |
| `data` | Datos (convención del curso) | `data: agrega dataset crudo de ventas 2024` |

También se puede indicar el área del cambio (*scope*): `feat(eda): agrega histogramas de precios`.

**Buenas prácticas:**

- Un commit = un cambio lógico. Si el mensaje necesita "y", probablemente son dos commits.
- El mensaje explica **qué** cambió, para que se entienda sin abrir el archivo.
- Evitar: `cambios`, `asdf`, `ya quedó`, `final`, `arreglos varios`.

---

## 6. Qué no se sube: `.gitignore`

El archivo `.gitignore` le dice a Git qué archivos ignorar. Se crea en la raíz del repositorio.

```gitignore
# Entorno virtual (se regenera con uv sync)
.venv/

# Archivos temporales de Python y Jupyter
__pycache__/
.ipynb_checkpoints/

# Secretos
.env

# Datos y modelos generados (se regeneran ejecutando el código)
data/processed/
models/

# Sistema operativo
.DS_Store
Thumbs.db
```

| Sí se sube | No se sube |
|---|---|
| Código (`.py`, `.ipynb`), `README.md`, `docs/` | `.venv/` |
| `pyproject.toml` y `uv.lock` | Contraseñas, llaves, `.env` |
| Datos crudos pequeños | Datos de más de 50 MB |

**Si ya subiste algo que no debía subirse** (por ejemplo `.venv/`):

```bash
git rm -r --cached .venv        # lo quita de Git, pero no lo borra de tu computador
# agrega .venv/ al .gitignore
git commit -m "chore: deja de versionar .venv"
git push
```

> Si subiste una contraseña o una llave, **cámbiala de inmediato**: aunque la borres en otro commit, sigue en el historial.

---

## 7. Deshacer cambios sin miedo

| Situación | Comando |
|---|---|
| Quiero descartar los cambios de un archivo (sin commit) | `git restore <archivo>` |
| Hice `git add` de algo que no quería | `git restore --staged <archivo>` |
| Me equivoqué en el mensaje del último commit (sin push) | `git commit --amend -m "nuevo mensaje"` |
| Olvidé agregar un archivo al último commit (sin push) | `git add <archivo>` y luego `git commit --amend --no-edit` |
| Quiero deshacer un commit que **ya subí** | `git revert <hash>` (crea un commit nuevo que lo revierte) y `git push` |
| Quiero ver cómo estaba un archivo en un commit anterior | `git show <hash>:<ruta/archivo>` |

> **Regla:** lo que ya subiste a GitHub no se borra del historial; se corrige con un commit nuevo (`git revert`). Los comandos como `git reset --hard` o `git push --force` pueden borrar el trabajo de otros: no los uses en el repositorio del equipo.

---

## 8. Errores frecuentes y cómo resolverlos

| Mensaje | Qué significa | Solución |
|---|---|---|
| `git: command not found` | Git no está instalado o la terminal no lo encuentra | Instalarlo (sección 2) y abrir una terminal nueva |
| `gh: command not found` | GitHub CLI no está instalado | `brew install gh` (macOS) o `winget install --id GitHub.cli` (Windows) |
| `fatal: not a git repository` | No estás dentro de la carpeta del repositorio | `cd` a la carpeta correcta o `git init` |
| `Please tell me who you are` | Falta configurar nombre y correo | `git config --global user.name ...` y `user.email ...` |
| `! [rejected] ... (fetch first)` | Alguien subió cambios antes que tú | `git pull` y luego `git push` |
| Se abre un editor raro al hacer `pull` | Git pide un mensaje para unir cambios | En Vim: escribir `:wq` y Enter. Para evitarlo: `git config --global core.editor "code --wait"` |
| `Your local changes would be overwritten by merge` | Tienes cambios sin guardar que chocan con los que vas a traer | `git stash`, `git pull`, `git stash pop` (o haz commit antes del pull) |
| `CONFLICT (content): Merge conflict in <archivo>` | Dos personas cambiaron la misma línea | Ver la sección siguiente |
| `Permission denied` o `403` al hacer push | No tienes acceso al repositorio o no has iniciado sesión | Aceptar la invitación del dueño y ejecutar `gh auth login` |
| `remote origin already exists` | El repositorio ya tiene un remoto | `git remote -v` para verlo; `git remote set-url origin <url>` para cambiarlo |
| `src refspec main does not match any` | Intentas subir sin haber hecho ningún commit | Hacer el primer commit y luego `git push -u origin main` |

### Resolver un conflicto

Un conflicto aparece cuando dos personas modificaron **la misma línea** del mismo archivo. Git marca el archivo así:

```text
<<<<<<< HEAD
Objetivo: predecir el precio de venta de una casa
=======
Objetivo: estimar el valor comercial de un inmueble
>>>>>>> origin/main
```

1. Abre el archivo en VS Code. Aparecen botones: *Accept Current*, *Accept Incoming*, *Accept Both*.
2. Deja el texto como debe quedar y **borra las marcas** `<<<<<<<`, `=======` y `>>>>>>>`.
3. Guarda y termina:

```bash
git add <archivo>
git commit -m "fix: resuelve conflicto en <archivo>"
git push
```

> **Para evitar conflictos:** hacer `git pull` antes de empezar, hacer commits pequeños y frecuentes, y repartir el trabajo para que cada persona edite archivos distintos.

---

## 9. Para ir más allá: ramas

Una **rama** es una línea de trabajo paralela. La rama `main` es la versión oficial del proyecto. En equipos grandes, cada tarea se hace en su propia rama y luego se une a `main` mediante un *pull request* en GitHub.

| Comando | Qué hace |
|---|---|
| `git branch` | Lista las ramas (la actual tiene `*`) |
| `git switch -c <rama>` | Crea una rama nueva y se mueve a ella |
| `git switch main` | Vuelve a la rama `main` |
| `git push -u origin <rama>` | Sube la rama a GitHub |
| `gh pr create --fill` | Abre un *pull request* desde la terminal |
| `git branch -d <rama>` | Borra una rama local que ya se unió |

Flujo típico con ramas:

```bash
git switch main && git pull
git switch -c feat/eda
# ... trabajar, add, commit ...
git push -u origin feat/eda
gh pr create --fill          # un compañero revisa y aprueba en GitHub
git switch main && git pull  # después de unir el pull request
```

---

## 10. Resumen de comandos

| Tarea | Comando |
|---|---|
| Configurar nombre y correo | `git config --global user.name "..."` / `user.email "..."` |
| Iniciar sesión en GitHub | `gh auth login` |
| Crear un repositorio local | `git init` |
| Crear un repositorio en GitHub | `gh repo create <nombre>` |
| Clonar | `git clone <url>` |
| Ver el estado | `git status` |
| Ver diferencias | `git diff` |
| Preparar archivos | `git add <archivo>` / `git add .` |
| Guardar un commit | `git commit -m "tipo: descripción"` |
| Ver el historial | `git log --oneline` |
| Subir a GitHub | `git push` |
| Primer push | `git push -u origin main` |
| Traer de GitHub | `git pull` |
| Ver el remoto | `git remote -v` |
| Guardar temporalmente | `git stash` / `git stash pop` |
| Descartar cambios de un archivo | `git restore <archivo>` |
| Sacar un archivo del staging | `git restore --staged <archivo>` |
| Corregir el último mensaje | `git commit --amend -m "..."` |
| Revertir un commit subido | `git revert <hash>` |
| Dejar de versionar un archivo | `git rm --cached <archivo>` |

**Ciclo diario:**

```bash
git pull
# trabajar
git status
git add <archivos>
git commit -m "tipo: descripción"
git push
```

---

**Documentación oficial:** [git-scm.com/doc](https://git-scm.com/doc) · [docs.github.com/es](https://docs.github.com/es) · [conventionalcommits.org](https://www.conventionalcommits.org/es/v1.0.0/)
