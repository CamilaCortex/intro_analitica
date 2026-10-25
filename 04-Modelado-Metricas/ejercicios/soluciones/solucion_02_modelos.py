"""
Soluciones: ejercicios del notebook 02_baseline_house_prices (módulo 04).

    uv run python 04-Modelado-Metricas/ejercicios/soluciones/solucion_02_modelos.py
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder

from intro_analitica import config
from intro_analitica.datos import cargar_house_prices_limpio
from intro_analitica.metricas import brecha_overfitting, metricas_regresion

df = cargar_house_prices_limpio()
CATEGORICAS = config.FEATURES_CATEGORICAS


def dividir(numericas):
    """Mismo split que el notebook: 60/20/20 con la semilla del curso."""
    X, y = df[numericas + CATEGORICAS], df[config.TARGET]
    X_temp, _, y_temp, _ = train_test_split(X, y, test_size=0.2, random_state=config.SEMILLA)
    return train_test_split(X_temp, y_temp, test_size=0.25, random_state=config.SEMILLA)


def preparar(X_tr, X_va, numericas):
    encoder = OneHotEncoder(handle_unknown="ignore", sparse_output=False).fit(X_tr[CATEGORICAS])

    def _p(X):
        dummies = pd.DataFrame(encoder.transform(X[CATEGORICAS]), index=X.index,
                               columns=encoder.get_feature_names_out(CATEGORICAS))
        return pd.concat([X[numericas], dummies], axis=1)

    return _p(X_tr), _p(X_va)


def lineal_log(X_tr, X_va, y_tr, y_va):
    modelo = LinearRegression().fit(X_tr, np.log1p(y_tr))
    return metricas_regresion(y_va, np.expm1(modelo.predict(X_va)))


# --- 1. Más variables ------------------------------------------------------------------------
print("1) ¿Agregar TotalSF, TotalBath y HouseAge mejora la lineal + log?")
for nombre, numericas in [
    ("Variables originales", config.FEATURES_NUMERICAS),
    ("+ TotalSF, TotalBath, HouseAge", config.FEATURES_NUMERICAS + ["TotalSF", "TotalBath", "HouseAge"]),
]:
    X_tr, X_va, y_tr, y_va = dividir(numericas)
    Xtr, Xva = preparar(X_tr, X_va, numericas)
    print(f"   {nombre:<32} {lineal_log(Xtr, Xva, y_tr, y_va)}")

# --- 2. Sin outliers en el train ---------------------------------------------------------------
print("\n2) Quitando del TRAIN las casas con GrLivArea > 4000")
numericas = config.FEATURES_NUMERICAS
X_tr, X_va, y_tr, y_va = dividir(numericas)
mascara = X_tr["GrLivArea"] <= 4000
print(f"   Se quitan {(~mascara).sum()} casas del train")
Xtr, Xva = preparar(X_tr, X_va, numericas)
print(f"   Con outliers: {lineal_log(Xtr, Xva, y_tr, y_va)}")
print(f"   Sin outliers: {lineal_log(Xtr[mascara], Xva, y_tr[mascara], y_va)}")
print("   → Solo se quitan del TRAIN: la validación debe parecerse a la realidad, con sus casos raros incluidos.")

# --- 3. Random Forest regularizado -------------------------------------------------------------
print("\n3) Random Forest: max_depth × min_samples_leaf")
filas = []
for depth in [8, 12, 16, None]:
    for leaf in [1, 3, 5]:
        rf = RandomForestRegressor(n_estimators=200, max_depth=depth, min_samples_leaf=leaf,
                                   random_state=config.SEMILLA, n_jobs=-1).fit(Xtr, y_tr)
        mae_tr = metricas_regresion(y_tr, rf.predict(Xtr))["MAE"]
        m_va = metricas_regresion(y_va, rf.predict(Xva))
        filas.append({"max_depth": str(depth), "min_samples_leaf": leaf, "MAE_valid": m_va["MAE"],
                      "MAPE_valid": m_va["MAPE_%"], "brecha_%": brecha_overfitting(mae_tr, m_va["MAE"])})
tabla = pd.DataFrame(filas).sort_values("MAE_valid")
print(tabla.to_string(index=False))
print("   → Subir min_samples_leaf y bajar max_depth reduce mucho la brecha con poca pérdida en validación.")

# --- 4. Reflexión -------------------------------------------------------------------------------
print(
    "\n4) Si ajustamos el modelo después de ver el test, el test se convierte en otro conjunto de validación\n"
    "   y su métrica deja de ser una estimación honesta del desempeño con datos nuevos. El test se usa UNA vez."
)
