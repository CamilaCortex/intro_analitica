"""
verificar_entrega.py: revisa automáticamente el repositorio del proyecto final.

Uso::

    uv run python 09-Proyecto-Final/scripts/verificar_entrega.py <ruta-al-repo-del-equipo>

Reutiliza las revisiones del módulo 01 (estructura, .gitignore, archivos pesados,
secretos, autores) y agrega las propias de la entrega final:
    - Documentos de cada módulo en docs/
    - Código reutilizable en src/ (limpieza, pipeline, train)
    - Notebooks sin errores guardados en sus salidas
    - API y pruebas (o un dashboard documentado)
    - Al menos 3 autores en el historial y PR unidos

No reemplaza la revisión humana: verifica lo mínimo para que el proyecto sea evaluable.
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

DOCS_ESPERADOS = [
    "01_problema_y_kpis.md",
    "02_project_charter.md",
    "03_decisiones_limpieza.md",
    "05_modelado.md",
]
SRC_ESPERADOS = ["limpieza.py", "train.py"]


def check(ok: bool, mensaje: str, consejo: str = "") -> bool:
    print(f"  {'[OK]' if ok else '[FALTA]'} {mensaje}")
    if not ok and consejo:
        print(f"     → {consejo}")
    return ok


def git(repo: Path, *args: str) -> list[str]:
    salida = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True, check=False).stdout
    return [linea for linea in salida.splitlines() if linea.strip()]


def notebooks_con_errores(repo: Path) -> list[str]:
    """Notebooks que tienen guardada una salida de error (se ejecutaron y fallaron)."""
    malos = []
    for nb in repo.glob("notebooks/**/*.ipynb"):
        try:
            celdas = json.loads(nb.read_text(encoding="utf-8")).get("cells", [])
        except (json.JSONDecodeError, UnicodeDecodeError):
            malos.append(f"{nb.name} (no es un JSON válido)")
            continue
        if any(o.get("output_type") == "error" for c in celdas for o in c.get("outputs", [])):
            malos.append(nb.name)
    return malos


def main() -> int:
    parser = argparse.ArgumentParser(description="Verifica la entrega final")
    parser.add_argument("repo", type=Path)
    repo = parser.parse_args().repo.resolve()
    if not (repo / ".git").exists():
        print(f"[ERROR] {repo} no es un repositorio git")
        return 1

    print(f"\nVerificando entrega: {repo.name}\n" + "═" * 55)
    resultados: list[bool] = []

    # 1. Revisiones básicas del módulo 01
    print("\n> Buenas prácticas de repositorio (módulo 01)")
    revisor = Path(__file__).resolve().parents[2] / "01-Git-GitHub/scripts/revisar_repo.py"
    basicas = subprocess.run([sys.executable, str(revisor), str(repo)], capture_output=True, text=True)
    resultados.append(check(basicas.returncode == 0, "revisar_repo.py sin errores",
                            f"corre: uv run python {revisor.relative_to(revisor.parents[2])} {repo}"))

    # 2. Documentación
    print("\n> Documentación (docs/)")
    for doc in DOCS_ESPERADOS:
        archivo = repo / "docs" / doc
        resultados.append(check(archivo.exists() and archivo.stat().st_size > 200, doc,
                                "falta o está casi vacío (< 200 bytes)"))
    readme = (repo / "README.md").read_text(encoding="utf-8", errors="ignore") if (repo / "README.md").exists() else ""
    resultados.append(check(len(readme) > 1500, f"README con contenido ({len(readme)} caracteres)",
                            "debe incluir problema, datos, cómo ejecutar, resultados y límites"))

    # 3. Código
    print("\n> Código reutilizable (src/)")
    for archivo in SRC_ESPERADOS:
        resultados.append(check((repo / "src" / archivo).exists(), f"src/{archivo}"))

    # 4. Notebooks
    print("\n> Notebooks")
    notebooks = list(repo.glob("notebooks/**/*.ipynb"))
    resultados.append(check(len(notebooks) >= 2, f"{len(notebooks)} notebooks"))
    malos = notebooks_con_errores(repo)
    resultados.append(check(not malos, "Sin errores guardados en las salidas", f"revisar: {malos}"))

    # 5. Solución
    print("\n> Solución (API o dashboard)")
    tiene_api = (repo / "api" / "main.py").exists()
    tiene_tests = any(repo.glob("tests/test_*.py"))
    menciona_dashboard = "dashboard" in readme.lower()
    resultados.append(check(tiene_api or menciona_dashboard, "API (api/main.py) o dashboard documentado en el README"))
    if tiene_api:
        resultados.append(check(tiene_tests, "Pruebas en tests/", "agrega tests/test_api.py"))

    # 6. Trabajo en equipo
    print("\n> Trabajo en equipo")
    autores = set(git(repo, "log", "--format=%ae"))
    merges = git(repo, "log", "--merges", "--oneline")
    resultados.append(check(len(autores) >= 3, f"{len(autores)} autores distintos", "los 3 integrantes deben hacer commits"))
    resultados.append(check(len(merges) >= 3, f"{len(merges)} merges (PR unidos)", "trabajen con ramas y PR"))

    ok, total = sum(resultados), len(resultados)
    print("\n" + "═" * 55 + f"\n{ok}/{total} verificaciones OK")
    print("¡Listo para entregar!\n" if ok == total else "[AVISO] Revisen los [FALTA] antes de entregar.\n")
    return 0 if ok == total else 1


if __name__ == "__main__":
    sys.exit(main())
