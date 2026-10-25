"""
Limpieza del dataset *House Prices* con **criterio de negocio**.

La lección más importante del módulo 03 está resumida en este archivo:

    En House Prices, la mayoría de los ``NaN`` NO son datos perdidos:
    significan "la casa no tiene eso" (no tiene piscina, no tiene garaje...).

Por eso no imputamos a ciegas con la media: primero leemos el diccionario de
datos (``data_description.txt``) y decidimos columna por columna.

Cada función hace **una sola cosa**, recibe un DataFrame y devuelve uno nuevo
(no modifica el original). Así se pueden probar y reutilizar por separado, y
:func:`limpiar_house_prices` simplemente las encadena.
"""

import pandas as pd

# --- Columnas categóricas donde NaN significa "no tiene" ---------------------
# (tomado de data_description.txt: p.ej. "PoolQC: NA = No Pool")
NAN_SIGNIFICA_NO_TIENE: dict[str, str] = {
    "Alley": "No Alley",
    "FireplaceQu": "No Fireplace",
    "PoolQC": "No Pool",
    "Fence": "No Fence",
    "MiscFeature": "None",
}

COLUMNAS_SOTANO = ["BsmtQual", "BsmtCond", "BsmtExposure", "BsmtFinType1", "BsmtFinType2"]
COLUMNAS_GARAJE = ["GarageType", "GarageFinish", "GarageQual", "GarageCond"]


def rellenar_no_tiene(df: pd.DataFrame) -> pd.DataFrame:
    """Rellena las categóricas donde ``NaN`` significa "no tiene".

    Ejemplo: ``PoolQC`` vale ``NaN`` en 1453 casas porque esas casas no tienen
    piscina. Rellenar con la moda ("Gd") sería inventar piscinas.
    """
    df = df.copy()
    for columna, valor in NAN_SIGNIFICA_NO_TIENE.items():
        if columna in df.columns:
            df[columna] = df[columna].fillna(valor)
    return df


def limpiar_numericas_estructurales(df: pd.DataFrame) -> pd.DataFrame:
    """Numéricas donde ``NaN`` significa 0 o "no aplica".

    - ``LotFrontage`` (metros de frente a la calle): no hay ningún 0 en los
      datos, así que asumimos que ``NaN`` = sin conexión directa a la calle → 0.
    - ``MasVnrArea`` (área de enchape): ``NaN`` = sin enchape → 0. Y si el
      área es 0, el tipo de enchape ``MasVnrType`` es ``"None"``. Si el área es
      mayor que 0 pero el tipo es ``NaN``, el dato es inconsistente: lo dejamos
      como ``NaN`` para que :func:`eliminar_inconsistencias` lo elimine.
    - ``GarageYrBlt`` (año del garaje): sin garaje → ``-1`` (valor centinela).
      [AVISO] Un centinela es una *señal*, no una cantidad: no lo promedies.
    """
    df = df.copy()
    df["LotFrontage"] = df["LotFrontage"].fillna(0)
    df["MasVnrArea"] = df["MasVnrArea"].fillna(0)
    sin_enchape = df["MasVnrArea"] == 0
    df.loc[sin_enchape, "MasVnrType"] = df.loc[sin_enchape, "MasVnrType"].fillna("None")
    df["GarageYrBlt"] = df["GarageYrBlt"].fillna(-1).astype(int)
    return df


def limpiar_sotano(df: pd.DataFrame) -> pd.DataFrame:
    """Sótano: si ``TotalBsmtSF == 0`` la casa no tiene sótano.

    En ese caso las 5 columnas de sótano se rellenan con ``"No Basement"``.
    Las filas que SÍ tienen sótano pero les falta algún dato del sótano son
    inconsistentes (son muy pocas) y se eliminan en :func:`eliminar_inconsistencias`.
    """
    df = df.copy()
    sin_sotano = df["TotalBsmtSF"] == 0
    for columna in COLUMNAS_SOTANO:
        df.loc[sin_sotano, columna] = df.loc[sin_sotano, columna].fillna("No Basement")
    return df


def limpiar_garaje(df: pd.DataFrame) -> pd.DataFrame:
    """Garaje: si ``GarageArea == 0`` la casa no tiene garaje → ``"No Garage"``."""
    df = df.copy()
    sin_garaje = df["GarageArea"] == 0
    for columna in COLUMNAS_GARAJE:
        df.loc[sin_garaje, columna] = df.loc[sin_garaje, columna].fillna("No Garage")
    return df


def eliminar_inconsistencias(df: pd.DataFrame) -> pd.DataFrame:
    """Elimina las pocas filas que quedan con datos realmente faltantes.

    Después de aplicar las reglas de negocio quedan ~8 filas con ``NaN``
    (p.ej. una casa con sótano pero sin ``BsmtExposure``, o sin ``Electrical``).
    Con 1460 filas, perder menos del 1% es aceptable y más honesto que inventar el valor.
    """
    return df.dropna().reset_index(drop=True)


def limpiar_house_prices(df: pd.DataFrame, verbose: bool = False) -> pd.DataFrame:
    """Pipeline completo de limpieza de House Prices.

    Parameters
    ----------
    df:
        DataFrame crudo (``train.csv``).
    verbose:
        Si es ``True`` imprime cuántos nulos quedan después de cada paso.

    Returns
    -------
    pd.DataFrame
        DataFrame sin nulos, listo para EDA y modelado.
    """
    pasos = [
        rellenar_no_tiene,
        limpiar_numericas_estructurales,
        limpiar_sotano,
        limpiar_garaje,
        eliminar_inconsistencias,
    ]
    for paso in pasos:
        df = paso(df)
        if verbose:
            print(f"{paso.__name__:<35} filas={len(df):>5}  nulos={int(df.isna().sum().sum()):>5}")
    return df


def agregar_variables(df: pd.DataFrame) -> pd.DataFrame:
    """*Feature engineering*: crea variables nuevas con sentido de negocio.

    - ``HouseAge``: años de la casa al momento de la venta.
    - ``YearsSinceRemod``: años desde la última remodelación.
    - ``Remodeled``: 1 si la casa fue remodelada (año de remodelación ≠ año de construcción).
    - ``TotalSF``: área total (sótano + piso 1 + piso 2), en pies².
    - ``TotalBath``: baños totales (los medios baños cuentan 0.5).

    Ninguna usa ``SalePrice``, así que no hay riesgo de *data leakage*.
    """
    df = df.copy()
    df["HouseAge"] = df["YrSold"] - df["YearBuilt"]
    df["YearsSinceRemod"] = df["YrSold"] - df["YearRemodAdd"]
    df["Remodeled"] = (df["YearRemodAdd"] != df["YearBuilt"]).astype(int)
    df["TotalSF"] = df["TotalBsmtSF"] + df["1stFlrSF"] + df["2ndFlrSF"]
    df["TotalBath"] = (
        df["FullBath"] + 0.5 * df["HalfBath"] + df["BsmtFullBath"] + 0.5 * df["BsmtHalfBath"]
    )
    return df
