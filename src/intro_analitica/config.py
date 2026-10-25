"""
Configuración central del proyecto: rutas y constantes.

¿Por qué un archivo de configuración?
-------------------------------------
Si cada notebook escribe su propia ruta (``"../../data/raw/train.csv"``), basta
con mover un archivo para que todo se rompa. Centralizando las rutas aquí,
cualquier script o notebook —sin importar en qué carpeta esté— encuentra los
datos de la misma forma.
"""

from pathlib import Path


def _encontrar_raiz() -> Path:
    """Sube por las carpetas hasta encontrar el ``pyproject.toml`` del repo."""
    actual = Path(__file__).resolve()
    for carpeta in [actual, *actual.parents]:
        if (carpeta / "pyproject.toml").exists():
            return carpeta
    # Fallback: src/intro_analitica/config.py -> raíz = 2 niveles arriba de src
    return actual.parents[2]


# --- Rutas principales -------------------------------------------------------
RAIZ = _encontrar_raiz()
DATA_DIR = RAIZ / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
MODELS_DIR = RAIZ / "models"
REPORTS_DIR = RAIZ / "reports"

# --- Datasets ----------------------------------------------------------------
HOUSE_PRICES_DIR = RAW_DIR / "house_prices"
HOUSE_PRICES_TRAIN = HOUSE_PRICES_DIR / "train.csv"
HOUSE_PRICES_TEST = HOUSE_PRICES_DIR / "test.csv"
HOUSE_PRICES_DESCRIPCION = HOUSE_PRICES_DIR / "data_description.txt"
HOUSE_PRICES_LIMPIO = PROCESSED_DIR / "house_prices_limpio.csv"

HOUSING_SIMPLE = RAW_DIR / "housing.csv"  # dataset pequeño del ejemplo de API del profesor

# --- Constantes de modelado --------------------------------------------------
SEMILLA = 42          # misma semilla en todo el curso = resultados reproducibles
TARGET = "SalePrice"  # variable objetivo de House Prices

# Subconjunto de variables que usamos para el modelo "de producción" (módulo 05).
# Es un subconjunto pequeño a propósito: la API debe pedir pocas entradas.
FEATURES_NUMERICAS = [
    "LotArea",
    "OverallQual",
    "OverallCond",
    "YearBuilt",
    "YearRemodAdd",
    "GrLivArea",
    "TotalBsmtSF",
    "FullBath",
    "BedroomAbvGr",
    "GarageCars",
]
FEATURES_CATEGORICAS = [
    "Neighborhood",
    "BldgType",
    "HouseStyle",
    "KitchenQual",
]
FEATURES_MODELO = FEATURES_NUMERICAS + FEATURES_CATEGORICAS


def asegurar_carpetas() -> None:
    """Crea las carpetas de salida si no existen (processed, models, reports)."""
    for carpeta in (PROCESSED_DIR, MODELS_DIR, REPORTS_DIR):
        carpeta.mkdir(parents=True, exist_ok=True)
