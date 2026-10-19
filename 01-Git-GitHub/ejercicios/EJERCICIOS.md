# Ejercicios: Módulo 01, Git y GitHub

> **Roten los roles:** quien fue piloto en el módulo 00 ahora es copiloto.

En este módulo practicamos el ciclo básico que usarán todo el semestre:

```
crear o clonar el repo  ->  hacer cambios  ->  git add  ->  git commit  ->  git push
                                    ^                                          |
                                    +------------- git pull <------------------+
```

> **Usuarios de Windows:** todos los comandos de esta guía funcionan en **Git Bash** (se instala junto con Git para Windows) y en PowerShell. Para crear archivos y carpetas, usen el explorador de VS Code (clic derecho → *New File* / *New Folder*); así evitamos comandos que cambian según el sistema operativo.

---

## Parte 1: Práctica individual (30 min, primera parte de la clase)

### Ejercicio 1. Configurar Git (5 min)

Solo se hace una vez por computador:

```bash
git config --global user.name "Nombre Apellido"
git config --global user.email "correo@ejemplo.com"
git config --global init.defaultBranch main

# Verificar
git config --global --list
```

Inicien sesión en GitHub desde la terminal (elegir *GitHub.com → HTTPS → Login with a web browser*):

```bash
gh auth login
```

> Si no tienen GitHub CLI: macOS `brew install gh` · Windows `winget install --id GitHub.cli` · Linux: ver [cli.github.com](https://cli.github.com/).

### Ejercicio 2. Crear un repositorio en GitHub y clonarlo (10 min)

1. En [github.com](https://github.com), clic en **New repository**.
2. Nombre: `practica-git`. Marquen **Add a README file**. Clic en **Create repository**.
3. En la página del repositorio, clic en **Code** y copien la URL (HTTPS).
4. En la terminal:

```bash
git clone https://github.com/<su-usuario>/practica-git.git
cd practica-git
git status
```

`git status` debe decir *"nothing to commit, working tree clean"*: el repositorio local es igual al de GitHub.

### Ejercicio 3. Subir un cambio: add, commit y push (10 min)

1. Abran la carpeta `practica-git` en VS Code y creen el archivo `presentacion.md` con este contenido:

   ```markdown
   # Hola, soy <nombre>
   - Carrera: ...
   - Lenguaje favorito: ...
   ```

2. Guarden el cambio en Git y súbanlo:

```bash
git status                                    # el archivo aparece como "untracked"
git add presentacion.md                       # preparar el archivo
git commit -m "docs: agrega mi presentación"  # guardar la foto con un mensaje claro
git push                                      # subir a GitHub
```

3. Recarguen la página del repositorio en GitHub: el archivo debe aparecer.
4. Ejecuten `git log --oneline` y observen el historial.

### Ejercicio 4. Traer cambios: pull (5 min)

1. En **GitHub** (navegador), abran `README.md`, clic en el lápiz (*Edit*), agreguen una línea y clic en **Commit changes**. Usen el mensaje `docs: actualiza README desde GitHub`.
2. En la terminal:

```bash
git pull
git log --oneline
```

El commit que hicieron en la web ahora está también en su computador.

> **Regla de oro:** antes de empezar a trabajar, `git pull`. Después de terminar, `git add`, `git commit` y `git push`.

### Ejercicio 5. Mensajes de commit con Conventional Commits (5 min)

Usamos el formato **tipo: descripción** (en minúscula, en presente y sin punto final):

| Tipo | Cuándo se usa | Ejemplo |
|---|---|---|
| `feat` | Algo nuevo (código, notebook, funcionalidad) | `feat: agrega notebook de EDA` |
| `fix` | Corrección de un error | `fix: corrige ruta del archivo de datos` |
| `docs` | Documentación (README, guías, comentarios) | `docs: agrega integrantes al README` |
| `refactor` | Reorganizar código sin cambiar lo que hace | `refactor: mueve la limpieza a src/limpieza.py` |
| `style` | Formato (espacios, nombres) sin cambiar la lógica | `style: aplica formato con ruff` |
| `test` | Pruebas | `test: agrega prueba del endpoint /health` |
| `chore` | Tareas de mantenimiento (dependencias, configuración) | `chore: agrega pandas con uv add` |
| `data` | Datos (convención del curso) | `data: agrega dataset crudo de ventas 2024` |

También se puede indicar el área del cambio entre paréntesis (*scope*): `feat(eda): agrega histogramas de precios`.

**Ejercicio:** reescriban estos mensajes con el formato correcto.

| Mensaje original | ¿Cómo debería quedar? |
|---|---|
| `cambios` (se agregó un notebook de limpieza) | |
| `arreglé el error` (la ruta al CSV estaba mal) | |
| `README` (se agregó cómo instalar el proyecto) | |
| `ya quedó la gráfica!!!` (nueva gráfica de ventas por mes) | |
| `instalé seaborn` | |
| `Organicé el código` (se pasó una función del notebook a `src/`) | |

Respuestas en `soluciones/solucion_01.md`.

---

## Parte 2: Salas de Zoom, el repositorio del equipo (45 min)

> **Objetivo:** subir a GitHub el proyecto que crearon en el módulo 00 y que los tres integrantes suban cambios al mismo repositorio.
> **Viene de:** la carpeta `proyecto-<equipo>` del módulo 00.
> **Va a:** todos los módulos siguientes: aquí vivirá el proyecto del equipo.

Para no pisarse, en esta práctica **cada integrante trabaja en un archivo distinto**.

### Paso 1: El piloto crea el repositorio del equipo (10 min)

1. En [github.com](https://github.com), clic en **New repository**. Nombre: `proyecto-<equipo>`, **sin** marcar *Add a README* (el proyecto ya tiene uno). Clic en **Create repository**.
2. En la terminal, desde la carpeta del proyecto del módulo 00:

```bash
cd proyecto-<equipo>
git init
cp <ruta>/intro_analitica/01-Git-GitHub/plantillas/gitignore_proyecto .gitignore
git add .
git commit -m "feat: estructura inicial del proyecto con uv"
git branch -M main
git remote add origin https://github.com/<usuario-piloto>/proyecto-<equipo>.git
git push -u origin main
```

> Si el proyecto se creó con `uv init`, es posible que ya exista un repositorio Git; en ese caso `git init` simplemente lo informa y se puede continuar.

3. En GitHub: **Settings → Collaborators → Add people**. Inviten a los otros dos integrantes y a la profesora. Cada invitado debe **aceptar la invitación** desde su correo o desde [github.com/notifications](https://github.com/notifications).

### Paso 2: Copiloto y relator clonan el repositorio (5 min)

```bash
git clone https://github.com/<usuario-piloto>/proyecto-<equipo>.git
cd proyecto-<equipo>
uv sync
```

### Paso 3: Cada integrante sube un cambio (15 min)

Cada persona hace **su** tarea, en **su** archivo:

| Integrante | Archivo | Tarea | Mensaje de commit sugerido |
|---|---|---|---|
| Piloto | `README.md` | Copiar el contenido de `plantillas/README_equipo.md` y llenar la tabla del equipo | `docs: completa README con datos del equipo` |
| Copiloto | `docs/00_acuerdos_equipo.md` | Horarios de reunión, canal de comunicación y cómo se reparten las tareas | `docs: agrega acuerdos del equipo` |
| Relator | `src/hola.py` | Un script que imprima "Hola desde el equipo <nombre>" y la versión de pandas | `feat: agrega script de bienvenida` |

Cada uno, cuando termine:

```bash
git pull                                   # traer lo que subieron los demás
git add <archivo>
git commit -m "<tipo>: <descripción>"
git push
```

> **Si `git push` responde "rejected" o "fetch first":** significa que un compañero subió algo antes que tú. Ejecuta `git pull` (Git une los cambios automáticamente porque son archivos distintos) y vuelve a ejecutar `git push`. Si se abre un editor pidiendo un mensaje, guarda y ciérralo sin cambiar nada.

### Paso 4: Todos se actualizan (5 min)

```bash
git pull
git log --oneline
```

Los tres deben ver los mismos commits y los tres archivos nuevos. El relator prueba el script del equipo:

```bash
uv run python src/hola.py
```

### Paso 5: Segunda ronda (10 min)

Repitan el ciclo **pull → cambio → add → commit → push** con un cambio pequeño cada uno, eligiendo el tipo de commit adecuado:

- Piloto: corrige un error de escritura en el README (`fix: ...`).
- Copiloto: agrega una sección "Herramientas" a los acuerdos (`docs: ...`).
- Relator: agrega una librería con `uv add` y sube `pyproject.toml` y `uv.lock` (`chore: ...`).

### Entregable (es la base de todos los módulos siguientes)

- [ ] Repositorio `proyecto-<equipo>` en GitHub, con los 3 integrantes y la profesora como colaboradores
- [ ] `.gitignore`, `pyproject.toml`, `uv.lock` y `README.md` con la tabla del equipo
- [ ] `docs/00_acuerdos_equipo.md` y `src/hola.py`
- [ ] Al menos **2 commits de cada integrante**, todos con formato Conventional Commits
- [ ] **Enlace del repositorio** compartido en el chat o en el formulario del curso

### Reto opcional

1. Revisen el historial en GitHub (**Commits**): ¿se distingue quién hizo cada cambio?
2. Ejecuten el revisor del curso sobre su repositorio:
   ```bash
   uv run python <ruta>/intro_analitica/01-Git-GitHub/scripts/revisar_repo.py .
   ```
3. Escriban un commit con *scope*, por ejemplo `docs(readme): agrega sección de instalación`.

---

## Preguntas para la plenaria

1. ¿Qué diferencia hay entre `git commit` y `git push`?
2. ¿Alguien recibió el mensaje "rejected" al hacer push? ¿Cómo lo resolvió?
3. ¿Qué archivos dejó por fuera el `.gitignore`? ¿Por qué no deben subirse?

## Para la próxima sesión

Cada integrante debe traer **1 tema y 1 dataset candidato** para el proyecto (de datos.gov.co, UCI, Kaggle…). En el **módulo 02** el equipo elige uno y define sus KPIs.
