"""
Herramientas de perfilamiento y calidad de datos (módulos 03 y 05).

Estas funciones responden rápido las preguntas que SIEMPRE hay que hacerle a un
dataset nuevo:

1. ¿Qué tipo tiene cada columna?
2. ¿Cuántos nulos hay y dónde?
3. ¿Cuántos valores distintos (cardinalidad)?
4. ¿Hay valores atípicos (outliers)?
"""

import pandas as pd


def perfil_rapido(df: pd.DataFrame) -> pd.DataFrame:
    """Tabla resumen con una fila por columna.

    Columnas del resultado: ``tipo``, ``nulos``, ``pct_nulos``, ``unicos`` y
    ``ejemplo``. Ordenada de más a menos nulos.

    Examples
    --------
    >>> perfil_rapido(df).head(10)   # las 10 columnas con más nulos
    """
    perfil = pd.DataFrame(
        {
            "tipo": df.dtypes.astype(str),
            "nulos": df.isna().sum(),
            "pct_nulos": (df.isna().mean() * 100).round(1),
            "unicos": df.nunique(),
            "ejemplo": df.apply(lambda s: s.dropna().iloc[0] if s.notna().any() else None),
        }
    )
    return perfil.sort_values(["nulos", "unicos"], ascending=[False, False])


def outliers_iqr(serie: pd.Series, k: float = 1.5) -> pd.Series:
    """Marca como outlier lo que está fuera de ``[Q1 - k·IQR, Q3 + k·IQR]``.

    Parameters
    ----------
    serie:
        Serie numérica.
    k:
        Multiplicador del rango intercuartílico. 1.5 es la regla clásica del
        boxplot; 3 detecta solo los atípicos "extremos".

    Returns
    -------
    pd.Series
        Serie booleana: ``True`` donde el valor es atípico.
    """
    q1, q3 = serie.quantile([0.25, 0.75])
    iqr = q3 - q1
    return (serie < q1 - k * iqr) | (serie > q3 + k * iqr)


def resumen_outliers(df: pd.DataFrame, k: float = 1.5) -> pd.DataFrame:
    """Cuenta outliers (regla IQR) para todas las columnas numéricas."""
    numericas = df.select_dtypes("number")
    conteo = {col: int(outliers_iqr(numericas[col].dropna(), k).sum()) for col in numericas}
    resumen = pd.DataFrame({"outliers": conteo})
    resumen["pct"] = (resumen["outliers"] / len(df) * 100).round(1)
    return resumen.sort_values("outliers", ascending=False)


def correlaciones_con_target(df: pd.DataFrame, target: str) -> pd.Series:
    """Correlación de Pearson de cada variable numérica con el target, ordenada."""
    numericas = df.select_dtypes("number")
    return numericas.corr()[target].drop(target).sort_values(ascending=False)


def reporte_calidad_markdown(df: pd.DataFrame, nombre: str = "dataset", top: int = 15) -> str:
    """Genera un reporte de calidad en Markdown (para pegar en el README del equipo)."""
    perfil = perfil_rapido(df)
    con_nulos = perfil[perfil["nulos"] > 0].head(top)
    lineas = [
        f"# Reporte de calidad — {nombre}",
        "",
        f"- **Filas:** {len(df):,}",
        f"- **Columnas:** {df.shape[1]}",
        f"- **Numéricas:** {df.select_dtypes('number').shape[1]}",
        f"- **Categóricas/texto:** {df.select_dtypes(exclude='number').shape[1]}",
        f"- **Filas duplicadas:** {int(df.duplicated().sum())}",
        f"- **Celdas nulas:** {int(df.isna().sum().sum()):,} "
        f"({df.isna().mean().mean() * 100:.1f}% del total)",
        "",
        f"## Columnas con nulos (top {top})",
        "",
    ]
    if con_nulos.empty:
        lineas.append("[OK] No hay columnas con nulos.")
    else:
        lineas.append(con_nulos[["tipo", "nulos", "pct_nulos", "unicos"]].to_markdown())
    lineas += ["", "## Outliers por regla IQR (top 10)", "", resumen_outliers(df).head(10).to_markdown()]
    return "\n".join(lineas)
