"""
perfil_inicial.py: reporte de calidad de datos (Fase 2 de CRISP-DM) para cualquier CSV.

Uso::

    uv run python 03-CRISP-DM/scripts/perfil_inicial.py <archivo.csv> [--salida docs/perfil.md] [--sep ";"]

El reporte incluye:
    - Dimensiones, tipos de columnas y duplicados
    - Columnas con nulos (cantidad y %)
    - Outliers por regla IQR
    - Cardinalidad de las columnas categóricas (para decidir el encoding)
    - Advertencias automáticas (columnas constantes, posibles IDs, mucha cardinalidad)

Usa las funciones de ``intro_analitica.eda``, así que el mismo código sirve en
notebooks y en la terminal.
"""

import argparse
from pathlib import Path

import pandas as pd

from intro_analitica.eda import reporte_calidad_markdown


def advertencias(df: pd.DataFrame) -> list[str]:
    """Reglas sencillas que detectan problemas típicos de un dataset nuevo."""
    alertas = []
    for columna in df.columns:
        serie = df[columna]
        unicos = serie.nunique(dropna=True)
        if unicos <= 1:
            alertas.append(f"[AVISO] `{columna}` es constante: no aporta información")
        elif unicos == len(df) and not pd.api.types.is_float_dtype(serie):
            alertas.append(f"`{columna}` tiene un valor distinto por fila: ¿es un ID? No la uses como variable")
        elif not pd.api.types.is_numeric_dtype(serie) and unicos > 50:
            alertas.append(f"`{columna}` es categórica con {unicos} categorías: el one-hot generaría muchas columnas")
        if serie.isna().mean() > 0.5:
            alertas.append(f"`{columna}` tiene más del 50 % de nulos: ¿significa 'no tiene' o es un dato perdido?")
    return alertas


def cardinalidad_categoricas(df: pd.DataFrame, top: int = 20) -> str:
    """Tabla Markdown con la cardinalidad y la categoría más frecuente de cada categórica."""
    categoricas = df.select_dtypes(exclude="number")
    if categoricas.empty:
        return "No hay columnas categóricas."
    tabla = pd.DataFrame(
        {
            "categorias": categoricas.nunique(),
            "mas_frecuente": categoricas.mode().iloc[0],
            "pct_mas_frecuente": (categoricas.apply(lambda s: s.value_counts(normalize=True).iloc[0] if s.notna().any() else 0) * 100).round(1),
        }
    ).sort_values("categorias", ascending=False)
    return tabla.head(top).to_markdown()


def generar_reporte(df: pd.DataFrame, nombre: str) -> str:
    """Arma el reporte completo en Markdown."""
    partes = [
        reporte_calidad_markdown(df, nombre=nombre),
        "",
        "## Cardinalidad de las categóricas",
        "",
        cardinalidad_categoricas(df),
        "",
        "## Advertencias automáticas",
        "",
    ]
    alertas = advertencias(df)
    partes += [f"- {a}" for a in alertas] if alertas else ["[OK] Sin advertencias"]
    partes += ["", "## Hipótesis iniciales (complétalas tú)", "", "1. ", "2. ", "3. "]
    return "\n".join(partes)


def main() -> None:
    parser = argparse.ArgumentParser(description="Reporte de calidad de un CSV (CRISP-DM, fase 2)")
    parser.add_argument("csv", type=Path, help="Ruta al archivo CSV")
    parser.add_argument("--salida", type=Path, help="(opcional) archivo .md donde guardar el reporte")
    parser.add_argument("--sep", default=",", help="Separador del CSV (los de datos.gov.co a veces usan ';')")
    args = parser.parse_args()

    df = pd.read_csv(args.csv, sep=args.sep)
    reporte = generar_reporte(df, nombre=args.csv.name)

    if args.salida:
        args.salida.parent.mkdir(parents=True, exist_ok=True)
        args.salida.write_text(reporte, encoding="utf-8")
        print(f"Reporte guardado en {args.salida}")
    else:
        print(reporte)


if __name__ == "__main__":
    main()
