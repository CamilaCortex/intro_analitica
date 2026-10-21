# Módulo 01: Git y GitHub para trabajar en equipo

> **Objetivo:** que el equipo tenga **un solo repositorio** donde los tres trabajan al tiempo sin pisarse, y que sepa resolver un conflicto sin entrar en pánico.

**Duración sugerida:** 2 horas (1 h de explicación y práctica guiada, 1 h de trabajo en salas)

## Contenido

| Archivo | Para qué sirve |
|---|---|
| `README.md` | Teoría y paso a paso (estás aquí) |
| `guia-practica-git.md` | Guía de la práctica paso a paso y comandos esenciales de Git y GitHub |
| `guia-comandos.md` | Resumen de comandos para tener a mano |
| `scripts/practica_conflicto.sh` | Crea un repositorio de juguete con un conflicto para practicar sin miedo |
| `scripts/revisar_repo.py` | Revisa que el repositorio del equipo cumpla las buenas prácticas del curso |
| `plantillas/` | `.gitignore`, README del equipo y plantilla de *pull request* |
| `ejercicios/EJERCICIOS.md` | Actividad para salas de Zoom |
| `presentacion/01-Git-GitHub.pptx` | Diapositivas de la clase |

---

## 1. ¿Por qué Git?

Seguro has visto esto:

```
informe_final.docx
informe_final_v2.docx
informe_final_v2_CORREGIDO.docx
informe_final_v2_CORREGIDO_ahora_si.docx
```

**Git** es un sistema de control de versiones: guarda una **foto** (un *commit*) de tu proyecto cada vez que tú se lo pides. Puedes volver a cualquier foto, ver qué cambió y quién lo cambió.

**GitHub** es un sitio web donde se guarda una copia del repositorio en la nube, para que el equipo la comparta y colabore.

| | Git | GitHub |
|---|---|---|
| ¿Qué es? | Un programa en tu computador | Una plataforma web |
| ¿Funciona sin internet? | Sí | No |
| Analogía | Los puntos de guardado del videojuego | La nube donde se guarda la partida |

## 2. Las tres zonas de Git

```
  Directorio de trabajo  ──git add──>  Staging (área de preparación)  ──git commit──>  Repositorio (historial)
   (tus archivos)                       ("esto va en la próxima foto")                  (las fotos guardadas)
                                                                                              │
                                                                               git push ▼  ▲ git pull
                                                                                     GitHub (remoto)
```

## 3. Configuración inicial (una sola vez por computador)

```bash
git config --global user.name "Tu Nombre"
git config --global user.email "tu-correo@ejemplo.com"
git config --global init.defaultBranch main
git config --global pull.rebase false     # al hacer pull, "merge" (lo más sencillo)
```

### Autenticarse con GitHub

La forma más fácil es usar **GitHub CLI**:

```bash
# macOS
brew install gh
# Windows
winget install --id GitHub.cli

gh auth login     # elige GitHub.com → HTTPS → Login with a web browser
```

> Otra opción es usar **llaves SSH**. Si te interesa, consulta la [guía oficial de GitHub](https://docs.github.com/es/authentication/connecting-to-github-with-ssh).

## 4. Paso a paso: del proyecto local a GitHub

Partimos de la carpeta del proyecto que crearon en el módulo 00.

```bash
cd proyecto-<nombre-equipo>

# 1. Convertir la carpeta en repositorio
git init

# 2. Decir qué NO se versiona (ver sección 5)
cp ../intro_analitica/01-Git-GitHub/plantillas/gitignore_proyecto .gitignore

# 3. Ver el estado: ¿qué archivos ve Git?
git status

# 4. Preparar y guardar la primera foto
git add .
git commit -m "feat: estructura inicial del proyecto con uv"

# 5. Crear el repositorio en GitHub y subirlo (con gh)
gh repo create proyecto-<nombre-equipo> --private --source=. --push
```

Si prefieres crear el repositorio desde la web de GitHub:

```bash
git remote add origin https://github.com/<usuario>/proyecto-<nombre-equipo>.git
git push -u origin main
```

## 5. `.gitignore`: lo que NUNCA se sube

| No se sube | ¿Por qué? |
|---|---|
| `.venv/` | Pesa cientos de MB y se regenera con `uv sync` |
| `__pycache__/`, `.ipynb_checkpoints/` | Son archivos temporales |
| `.env`, llaves, contraseñas | **Seguridad**: GitHub es público o compartido |
| `data/processed/`, `models/` | Se regeneran ejecutando el código |
| Datasets de más de 50 MB | GitHub los rechaza. Documenta de dónde se descargan |

| Sí se sube |
|---|
| Código (`.py`, `.ipynb`), `pyproject.toml`, **`uv.lock`**, `README.md`, `docs/`, datos crudos pequeños |

> Si subiste por error una contraseña, **cámbiala de inmediato**. Borrarla en un commit nuevo no la quita del historial.

## 6. Ramas: trabajar al tiempo sin pisarse

Una **rama** (*branch*) es una línea de trabajo paralela. `main` es la rama "oficial", la que siempre debe funcionar.

```
main     ●────────●─────────────●──────────●   (siempre funciona)
          \                    /          /
eda        ●───●───●──────────●          /     (Laura hace el EDA)
            \                           /
limpieza     ●───●───●─────────────────●       (Andrés hace la limpieza)
```

```bash
git switch -c feature/eda          # crear la rama y moverse a ella
# ... trabajar, git add, git commit ...
git push -u origin feature/eda     # subir la rama a GitHub
```

## 7. *Pull requests* (PR): revisar antes de unir

Un **pull request** es una solicitud del tipo "revisen mis cambios y, si están bien, únanlos a `main`".

1. Subes tu rama: `git push -u origin feature/eda`.
2. En GitHub aparece el botón **"Compare & pull request"**, o desde la terminal ejecutas `gh pr create --fill`.
3. Un compañero **revisa**, comenta y aprueba.
4. Se hace **Merge** y la rama se borra.
5. Todos actualizan su copia: `git switch main && git pull`.

> **Regla del equipo:** nadie hace `push` directo a `main`. Todo entra por PR. Pueden activarlo en GitHub en *Settings → Branches → Add rule → Require a pull request before merging*.

## 8. Conflictos: no son errores, son preguntas

Un conflicto ocurre cuando **dos personas cambian la misma línea** del mismo archivo. Git no sabe cuál versión dejar y te pregunta:

```text
<<<<<<< HEAD
Objetivo: predecir el precio de venta de una casa
=======
Objetivo: estimar el valor comercial de un inmueble
>>>>>>> feature/objetivo
```

**Cómo resolverlo:**

1. Abre el archivo (VS Code muestra los botones *Accept Current / Incoming / Both*).
2. Deja el texto como debe quedar y **borra las marcas** `<<<<<<<`, `=======` y `>>>>>>>`.
3. `git add archivo` y luego `git commit`.

**Practica sin miedo** con el script que crea un conflicto de juguete:

```bash
bash 01-Git-GitHub/scripts/practica_conflicto.sh
```

## 9. Buenos mensajes de commit

Usamos un formato sencillo, **tipo: descripción en presente**:

| Tipo | Cuándo | Ejemplo |
|---|---|---|
| `feat` | Algo nuevo | `feat: agrega notebook de EDA` |
| `fix` | Corrección | `fix: corrige imputación de LotFrontage` |
| `docs` | Documentación | `docs: actualiza README con KPIs` |
| `refactor` | Reorganizar sin cambiar lo que hace el código | `refactor: mueve limpieza a src/limpieza.py` |
| `data` | Datos | `data: agrega dataset crudo de ventas 2024` |

Incorrecto: `cambios`, `asdf`, `ya quedó`, `final final`
Correcto: `feat: calcula KPI de precio mediano por barrio`

## 10. Notebooks y Git: tips

- Antes de hacer commit, **reinicia el kernel y ejecuta todo**: así el notebook queda reproducible.
- Los notebooks con salidas enormes (gráficas, tablas de 1000 filas) hacen difícil revisar los PR. Limpia las salidas muy grandes.
- **Dos personas no deben editar el mismo notebook al tiempo**: los conflictos en `.ipynb` son difíciles de resolver. Repártanse notebooks o pasen la lógica a `src/`.

## 11. GitHub para organizar al equipo

- **Issues:** una tarea por *issue* ("Hacer EDA de variables numéricas"), con un responsable asignado.
- **Projects:** un tablero Kanban (*To do → In progress → Done*).
- Escribir `Closes #3` en la descripción del PR cierra el *issue* automáticamente cuando se une.

## 12. Revisa tu repositorio

```bash
uv run python 01-Git-GitHub/scripts/revisar_repo.py ruta/al/proyecto-del-equipo
```

Revisa la estructura, `.gitignore`, `uv.lock`, archivos pesados, secretos y que `.venv` no esté versionado.

---

## Checklist del módulo

- [ ] `git config` con mi nombre y correo
- [ ] `gh auth login` (o SSH) funcionando
- [ ] Repositorio del equipo en GitHub, con los 3 integrantes como colaboradores
- [ ] Cada integrante hizo al menos un PR
- [ ] Resolví un conflicto (con el script de práctica o en el proyecto)

**Anterior:** [Módulo 00: Entornos](../00-Entornos-uv/) · **Siguiente:** [Módulo 02: BI y Analítica](../02-BI-Analitica/)
