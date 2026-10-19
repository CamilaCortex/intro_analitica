"""
kpis.py: tabla de KPIs agrupada, para cualquier CSV.

Ejemplos::

    # House Prices: KPIs del precio de venta por barrio
    uv run python 02-BI-Analitica/scripts/kpis.py --por Neighborhood

    # Por año de venta, guardando el resultado
    uv run python 02-BI-Analitica/scripts/kpis.py --por YrSold --salida reports/kpis_anio.csv

    # Con el dataset del equipo
    uv run python 02-BI-Analitica/scripts/kpis.py --csv data/raw/ventas.csv --valor monto --por region

Para cada grupo calcula:
    - n           → cuántos registros (volumen)
    - total       → suma del valor (ingreso)
    - mediana     → valor típico (robusto a extremos)
    - promedio    → valor promedio
    - participacion_% → qué porcentaje del total aporta el grupo
"""

import argparse
from pathlib import Path

import pandas as pd

from intro_analitica import config


def calcular_kpis(df: pd.DataFrame, valor: str, por: str) -> pd.DataFrame:
    """Calcula los KPIs de ``valor`` agrupados por ``por``.

    Parameters
    ----------
    df:
        Datos.
    valor:
        Columna numérica a resumir (p.ej. ``SalePrice``).
    por:
        Columna para agrupar (p.ej. ``Neighborhood``).

    Returns
    -------
    pd.DataFrame
        Una fila por grupo, ordenada por ``total`` de mayor a menor.
    """
    if valor not in df.columns or por not in df.columns:
        faltan = {valor, por} - set(df.columns)
        raise KeyError(f"Columnas no encontradas: {faltan}. Disponibles: {list(df.columns)[:15]}...")

    kpis = df.groupby(por)[valor].agg(n="count", total="sum", mediana="median", promedio="mean")
    kpis["participacion_%"] = (kpis["total"] / kpis["total"].sum() * 100).round(1)
    return kpis.sort_values("total", ascending=False).round(0)


def main() -> None:
    parser = argparse.ArgumentParser(description="Tabla de KPIs agrupada")
    parser.add_argument("--csv", type=Path, default=config.HOUSE_PRICES_TRAIN, help="Ruta al CSV")
    parser.add_argument("--valor", default="SalePrice", help="Columna numérica a resumir")
    parser.add_argument("--por", default="Neighborhood", help="Columna para agrupar")
    parser.add_argument("--top", type=int, default=10, help="Cuántos grupos mostrar")
    parser.add_argument("--salida", type=Path, help="(opcional) guardar la tabla en CSV")
    args = parser.parse_args()

    df = pd.read_csv(args.csv)
    kpis = calcular_kpis(df, args.valor, args.por)

    print(f"\nKPIs de '{args.valor}' por '{args.por}': {args.csv.name}\n")
    print(kpis.head(args.top).to_string())
    print(f"\nTotal general: {df[args.valor].sum():,.0f} · Mediana general: {df[args.valor].median():,.0f}")

    if args.salida:
        args.salida.parent.mkdir(parents=True, exist_ok=True)
        kpis.to_csv(args.salida)
        print(f"Guardado en {args.salida}")


if __name__ == "__main__":
    main()
