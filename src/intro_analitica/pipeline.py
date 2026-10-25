"""
Construcción del pipeline de House Prices (módulo 05).

Un ``Pipeline`` de scikit-learn encadena preprocesamiento + modelo en UN SOLO objeto:

    datos crudos ──> [imputar → escalar → one-hot] ──> [modelo] ──> predicción

Ventajas:
    1. ``fit`` aprende el preprocesamiento SOLO con los datos de entrenamiento
       (adiós *data leakage*, incluso dentro de la validación cruzada).
    2. Se guarda con ``joblib`` como un solo archivo: la API (módulo 05) recibe
       datos "como vienen" y el pipeline hace todo lo demás.
    3. Se puede cambiar el modelo o los hiperparámetros con ``set_params`` o ``GridSearchCV``.

Este archivo lo usan el notebook del módulo 05 y ``05-Pipelines-y-API/scripts/train.py``,
así que ambos construyen exactamente el mismo pipeline.
"""

import numpy as np
from sklearn.compose import ColumnTransformer, TransformedTargetRegressor
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, StandardScaler

from intro_analitica import config

# Variables ordinales: el orden importa (Po < Fa < TA < Gd < Ex)
ESCALA_CALIDAD = ["Po", "Fa", "TA", "Gd", "Ex"]
ORDINALES = {"KitchenQual": ESCALA_CALIDAD}


def construir_preprocesamiento(
    numericas: list[str] | None = None,
    categoricas: list[str] | None = None,
    ordinales: dict[str, list[str]] | None = None,
) -> ColumnTransformer:
    """Arma el ``ColumnTransformer`` con un tratamiento distinto por tipo de columna.

    ======================  =============================================
    Tipo                    Pasos
    ======================  =============================================
    Numéricas               imputar con la mediana → estandarizar
    Categóricas (sin orden) imputar con la moda → one-hot (ignora categorías nuevas)
    Ordinales               imputar con la moda → ordinal con el orden dado
    ======================  =============================================

    Por defecto usa las variables de :mod:`intro_analitica.config`.
    """
    ordinales = ORDINALES if ordinales is None else ordinales
    numericas = config.FEATURES_NUMERICAS if numericas is None else numericas
    categoricas = config.FEATURES_CATEGORICAS if categoricas is None else categoricas
    categoricas = [c for c in categoricas if c not in ordinales]

    transformadores = [
        (
            "num",
            Pipeline([("imputar", SimpleImputer(strategy="median")), ("escalar", StandardScaler())]),
            numericas,
        ),
        (
            "cat",
            Pipeline(
                [
                    ("imputar", SimpleImputer(strategy="most_frequent")),
                    ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
                ]
            ),
            categoricas,
        ),
    ]
    if ordinales:
        transformadores.append(
            (
                "ord",
                Pipeline(
                    [
                        ("imputar", SimpleImputer(strategy="most_frequent")),
                        (
                            "ordinal",
                            OrdinalEncoder(
                                categories=list(ordinales.values()),
                                handle_unknown="use_encoded_value",
                                unknown_value=-1,
                            ),
                        ),
                    ]
                ),
                list(ordinales.keys()),
            )
        )
    return ColumnTransformer(transformadores, verbose_feature_names_out=False)


def construir_pipeline(modelo=None, log_target: bool = True) -> Pipeline:
    """Pipeline completo: preprocesamiento + modelo.

    Parameters
    ----------
    modelo:
        Cualquier regresor de scikit-learn. Por defecto, ``HistGradientBoostingRegressor``
        (el elegido en el módulo 04).
    log_target:
        Si es ``True``, el modelo aprende ``log(1 + precio)`` y la predicción se
        devuelve en dólares automáticamente (``TransformedTargetRegressor``).
    """
    modelo = modelo if modelo is not None else HistGradientBoostingRegressor(random_state=config.SEMILLA)
    if log_target:
        modelo = TransformedTargetRegressor(regressor=modelo, func=np.log1p, inverse_func=np.expm1)
    return Pipeline([("preprocesamiento", construir_preprocesamiento()), ("modelo", modelo)])
