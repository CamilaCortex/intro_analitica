"""
reporte_eda.py: genera un EDA automático (figuras + resumen en Markdown) para cualquier CSV.

Uso::

    # House Prices limpio (salida del módulo 04)
    uv run python 05-EDA/scripts/reporte_eda.py data/processed/house_prices_limpio.csv --target SalePrice

    # Dataset del equipo
    uv run python 05-EDA/scripts/reporte_eda.py data/processed/mis_datos_limpio.csv --target ventas --salida reports/eda

Genera en la carpeta de salida (por defecto reports/eda_<archivo>/):
    01_target.png             distribución del target
    02_numericas.png          histogramas de las numéricas
    03_correlaciones.png      heatmap de correlación
    04_top_vs_target.png      las 6 numéricas más correlacionadas vs. el target
    05_categoricas.png        boxplots del target por las categóricas de baja cardinalidad
    resumen.md                tabla de correlaciones, outliers y plantilla de hallazgos

[AVISO] Un EDA automático es un PUNTO DE PARTIDA. Los hallazgos los escribe el equipo.
"""

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from intro_analitica import config
from intro_analitica.eda import correlaciones_con_target, resumen_outliers

MAX_CATEGORIAS = 15  # para no graficar columnas con cientos de categorías


def figura_target(df: pd.DataFrame, target: str, carpeta: Path) -> None:
    """Histograma (numérico) o barras (categórico) del target."""
    fig, ax = plt.subplots(figsize=(7, 4))
    if pd.api.types.is_numeric_dtype(df[target]):
        sns.histplot(df[target], bins=50, kde=True, ax=ax)
        ax.set(title=f"{target} (asimetría = {df[target].skew():.2f})")
    else:
        df[target].value_counts().plot(kind="bar", ax=ax)
        ax.set(title=f"Distribución de {target} (clasificación)")
    fig.savefig(carpeta / "01_target.png", dpi=110, bbox_inches="tight")
    plt.close(fig)


def figura_numericas(df: pd.DataFrame, carpeta: Path) -> None:
    numericas = df.select_dtypes("number")
    axes = numericas.hist(bins=30, figsize=(16, 3 * ((numericas.shape[1] + 3) // 4)), layout=(-1, 4))
    fig = axes.ravel()[0].figure
    fig.suptitle("Variables numéricas", y=1.0)
    fig.tight_layout()
    fig.savefig(carpeta / "02_numericas.png", dpi=90, bbox_inches="tight")
    plt.close(fig)


def figura_correlaciones(df: pd.DataFrame, carpeta: Path, max_vars: int = 20) -> None:
    numericas = df.select_dtypes("number")
    if numericas.shape[1] > max_vars:  # nos quedamos con las de mayor varianza relativa para que sea legible
        numericas = numericas[numericas.std().div(numericas.mean().abs() + 1e-9).nlargest(max_vars).index]
    fig, ax = plt.subplots(figsize=(12, 9))
    sns.heatmap(numericas.corr(), cmap="RdBu_r", center=0, annot=numericas.shape[1] <= 15, fmt=".2f", ax=ax)
    ax.set(title="Matriz de correlación")
    fig.savefig(carpeta / "03_correlaciones.png", dpi=100, bbox_inches="tight")
    plt.close(fig)


def figura_top_vs_target(df: pd.DataFrame, target: str, carpeta: Path) -> pd.Series:
    correlaciones = correlaciones_con_target(df, target)
    top = correlaciones.abs().sort_values(ascending=False).head(6).index
    fig, axes = plt.subplots(2, 3, figsize=(15, 8))
    for ax, col in zip(axes.ravel(), top):
        sns.regplot(data=df, x=col, y=target, ax=ax, scatter_kws={"alpha": 0.25, "s": 10}, line_kws={"color": "red"})
        ax.set(title=f"{col} (r = {correlaciones[col]:.2f})")
    fig.tight_layout()
    fig.savefig(carpeta / "04_top_vs_target.png", dpi=100, bbox_inches="tight")
    plt.close(fig)
    return correlaciones


def figura_categoricas(df: pd.DataFrame, target: str, carpeta: Path, max_cols: int = 6) -> None:
    categoricas = [c for c in df.select_dtypes(exclude="number") if 2 <= df[c].nunique() <= MAX_CATEGORIAS][:max_cols]
    if not categoricas:
        return
    fig, axes = plt.subplots(len(categoricas), 1, figsize=(10, 3.2 * len(categoricas)), squeeze=False)
    for ax, col in zip(axes.ravel(), categoricas):
        orden = df.groupby(col)[target].median().sort_values().index
        sns.boxplot(data=df, x=col, y=target, order=orden, ax=ax, color="lightsteelblue")
        ax.set(title=f"{target} por {col}", xlabel="")
        ax.tick_params(axis="x", rotation=30)
    fig.tight_layout()
    fig.savefig(carpeta / "05_categoricas.png", dpi=100, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description="EDA automático de un CSV")
    parser.add_argument("csv", type=Path)
    parser.add_argument("--target", required=True, help="Columna objetivo")
    parser.add_argument("--salida", type=Path, help="Carpeta de salida (por defecto reports/eda_<archivo>)")
    parser.add_argument("--sep", default=",")
    args = parser.parse_args()

    df = pd.read_csv(args.csv, sep=args.sep)
    if args.target not in df.columns:
        raise SystemExit(f"[ERROR] La columna '{args.target}' no existe. Columnas: {list(df.columns)[:20]}…")

    carpeta = args.salida or config.REPORTS_DIR / f"eda_{args.csv.stem}"
    carpeta.mkdir(parents=True, exist_ok=True)
    sns.set_theme(style="whitegrid")

    figura_target(df, args.target, carpeta)
    figura_numericas(df, carpeta)
    figura_correlaciones(df, carpeta)
    lineas = [f"# EDA: {args.csv.name}", "", f"- Filas: {len(df):,} · Columnas: {df.shape[1]} · Target: `{args.target}`", ""]

    if pd.api.types.is_numeric_dtype(df[args.target]):
        correlaciones = figura_top_vs_target(df, args.target, carpeta)
        figura_categoricas(df, args.target, carpeta)
        lineas += ["## Correlación con el target", "", correlaciones.round(3).to_frame("r").to_markdown(), ""]

    lineas += [
        "## Outliers (regla IQR, top 10)", "", resumen_outliers(df).head(10).to_markdown(), "",
        "## Figuras", "",
        *[f"![{p.stem}]({p.name})" for p in sorted(carpeta.glob("*.png"))],
        "", "## Hallazgos (escríbanlos ustedes)", "",
        "| # | Hallazgo | Evidencia (figura/tabla) | Implicación para el modelo |",
        "|---|---|---|---|", "| 1 | | | |", "| 2 | | | |", "| 3 | | | |", "| 4 | | | |", "| 5 | | | |",
    ]
    (carpeta / "resumen.md").write_text("\n".join(lineas), encoding="utf-8")
    print(f"[OK] EDA generado en {carpeta}")
    for archivo in sorted(carpeta.iterdir()):
        print("   ·", archivo.name)


if __name__ == "__main__":
    main()
