"""
Funciones de carga de datos.

Todas devuelven un ``pandas.DataFrame`` y reciben la ruta como parámetro
opcional: si no la pasas, usan la ruta definida en :mod:`intro_analitica.config`.
"""

from pathlib import Path

import pandas as pd

from intro_analitica import config


def cargar_house_prices(ruta: str | Path | None = None) -> pd.DataFrame:
    """Carga el set de entrenamiento de *House Prices* (Ames, Iowa).

    Parameters
    ----------
    ruta:
        Ruta al ``train.csv``. Por defecto ``data/raw/house_prices/train.csv``.

    Returns
    -------
    pd.DataFrame
        1460 filas x 81 columnas. La columna objetivo es ``SalePrice``.
    """
    ruta = Path(ruta) if ruta else config.HOUSE_PRICES_TRAIN
    return pd.read_csv(ruta)


def cargar_house_prices_limpio(ruta: str | Path | None = None) -> pd.DataFrame:
    """Carga la versión limpia generada en el módulo 03.

    Si el archivo aún no existe, lo genera al vuelo (limpieza + variables nuevas,
    igual que en ``03-Preparacion-y-EDA/notebooks/01_preparacion_house_prices.ipynb``) para que
    ningún notebook "se quede sin datos".
    """
    ruta = Path(ruta) if ruta else config.HOUSE_PRICES_LIMPIO
    if not ruta.exists():
        from intro_analitica.limpieza import agregar_variables, limpiar_house_prices

        config.asegurar_carpetas()
        agregar_variables(limpiar_house_prices(cargar_house_prices())).to_csv(ruta, index=False)
    return pd.read_csv(ruta)


def cargar_housing_simple(ruta: str | Path | None = None) -> pd.DataFrame:
    """Carga el dataset pequeño ``housing.csv`` (546 casas, 12 variables).

    Es el dataset del ejemplo de API del profesor; lo usamos para ejemplos
    rápidos de regresión con 2 variables (``lotsize``, ``bedrooms``).
    """
    ruta = Path(ruta) if ruta else config.HOUSING_SIMPLE
    df = pd.read_csv(ruta)
    return df.drop(columns=["rownames"], errors="ignore")


def leer_diccionario_house_prices(ruta: str | Path | None = None) -> dict[str, str]:
    """Convierte ``data_description.txt`` en un diccionario ``{columna: descripción}``.

    El archivo original tiene líneas del tipo ``MSSubClass: Identifies the type...``
    seguidas de los posibles valores (indentados). Aquí nos quedamos solo con la
    descripción principal de cada columna.
    """
    ruta = Path(ruta) if ruta else config.HOUSE_PRICES_DESCRIPCION
    diccionario: dict[str, str] = {}
    for linea in ruta.read_text(encoding="utf-8", errors="ignore").splitlines():
        if linea and not linea[0].isspace() and ":" in linea:
            columna, descripcion = linea.split(":", 1)
            diccionario[columna.strip()] = descripcion.strip()
    return diccionario
