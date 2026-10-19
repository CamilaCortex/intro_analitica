# Resumen de comandos de Git

## Lo del día a día

| Comando | Qué hace |
|---|---|
| `git status` | ¿Qué cambió? (úsalo **todo** el tiempo) |
| `git add <archivo>` / `git add .` | Prepara cambios para el próximo commit |
| `git commit -m "tipo: mensaje"` | Guarda una foto |
| `git push` | Sube tus commits a GitHub |
| `git pull` | Trae los cambios de GitHub |
| `git log --oneline --graph` | Historial en forma de árbol |
| `git diff` | Qué cambió y aún no está en *staging* |

## Ramas

| Comando | Qué hace |
|---|---|
| `git switch -c feature/x` | Crea una rama y te mueve a ella |
| `git switch main` | Vuelve a `main` |
| `git branch` | Lista las ramas |
| `git merge feature/x` | Une `feature/x` a la rama actual |
| `git branch -d feature/x` | Borra una rama local ya unida |

## Deshacer (sin pánico)

| Situación | Comando |
|---|---|
| Quiero descartar cambios de un archivo (sin commit) | `git restore archivo` |
| Hice `git add` de algo que no quería | `git restore --staged archivo` |
| Me equivoqué en el mensaje del último commit (sin push) | `git commit --amend -m "nuevo mensaje"` |
| Quiero deshacer un commit que ya subí | `git revert <hash>` (crea un commit "inverso") |
| Subí `.venv` por error | `git rm -r --cached .venv` → agregar a `.gitignore` → commit |

## GitHub CLI (`gh`)

| Comando | Qué hace |
|---|---|
| `gh auth login` | Autenticarse |
| `gh repo create <nombre> --private --source=. --push` | Crear el repositorio en GitHub desde la carpeta local |
| `gh repo clone <usuario>/<repo>` | Clonar |
| `gh pr create --fill` | Abrir un PR con el mensaje del commit |
| `gh pr list` / `gh pr checkout <n>` | Ver PR / probar el PR de un compañero |
| `gh issue create` | Crear un *issue* |

## Flujo del equipo (cada tarea)

```bash
git switch main && git pull                 # 1. partir de lo último
git switch -c feature/mi-tarea              # 2. rama nueva
# ... trabajar ...
git add . && git commit -m "feat: ..."      # 3. guardar
git push -u origin feature/mi-tarea         # 4. subir
gh pr create --fill                         # 5. pedir revisión
# 6. un compañero revisa y hace merge en GitHub
git switch main && git pull                 # 7. actualizarse
```
