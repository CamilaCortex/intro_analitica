"""
Métricas de evaluación reutilizables (módulos 06 y 07).

Regla de oro: **un número solo no dice nada**. Siempre compara contra un
*baseline* (p.ej. predecir siempre la mediana) y reporta varias métricas.
"""

import numpy as np
import pandas as pd
from sklearn.metrics import (
    mean_absolute_error,
    mean_absolute_percentage_error,
    r2_score,
    root_mean_squared_error,
)


def metricas_regresion(y_real, y_pred) -> dict[str, float]:
    """Calcula MAE, RMSE, MAPE (%) y R² en un solo diccionario.

    Examples
    --------
    >>> metricas_regresion([100, 200], [110, 190])
    {'MAE': 10.0, 'RMSE': 10.0, 'MAPE_%': 7.5, 'R2': 0.96}
    """
    return {
        "MAE": round(float(mean_absolute_error(y_real, y_pred)), 2),
        "RMSE": round(float(root_mean_squared_error(y_real, y_pred)), 2),
        "MAPE_%": round(float(mean_absolute_percentage_error(y_real, y_pred) * 100), 2),
        "R2": round(float(r2_score(y_real, y_pred)), 4),
    }


def tabla_comparativa(resultados: dict[str, dict[str, float]]) -> pd.DataFrame:
    """Convierte ``{modelo: metricas}`` en una tabla ordenada por RMSE."""
    return pd.DataFrame(resultados).T.sort_values("RMSE")


def brecha_overfitting(metrica_train: float, metrica_test: float) -> float:
    """Diferencia relativa (%) entre test y train para un error (MAE/RMSE).

    Una brecha grande (p.ej. > 30%) es señal de *overfitting*: el modelo
    memorizó el entrenamiento y no generaliza.
    """
    if metrica_train == 0:
        return float(np.inf)
    return round((metrica_test - metrica_train) / metrica_train * 100, 1)
