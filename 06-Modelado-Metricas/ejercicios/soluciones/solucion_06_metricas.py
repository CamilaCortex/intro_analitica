"""
Soluciones: ejercicios del notebook 01_metricas (módulo 06).

    uv run python 06-Modelado-Metricas/ejercicios/soluciones/solucion_06_metricas.py
"""

import numpy as np
from sklearn.datasets import load_breast_cancer
from sklearn.linear_model import LinearRegression, LogisticRegression, Ridge
from sklearn.metrics import root_mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures, StandardScaler

SEMILLA = 42

# --- 1. Métricas a mano ---------------------------------------------------------------------
reales = np.array([250_000, 300_000, 200_000, 400_000, 350_000])
predichos = np.array([240_000, 310_000, 210_000, 380_000, 340_000])
errores = reales - predichos

mae = np.mean(np.abs(errores))
rmse = np.sqrt(np.mean(errores**2))
r2 = 1 - np.sum(errores**2) / np.sum((reales - reales.mean()) ** 2)
print("1) A mano:")
print(f"   MAE  = {mae:,.0f}")
print(f"   RMSE = {rmse:,.0f}")
print(f"   R²   = {r2:.3f}   (igual a scikit-learn [OK])\n")

# --- 2. Umbral que deja escapar como máximo 1 maligno ----------------------------------------
datos = load_breast_cancer(as_frame=True)
X, y = datos.data, 1 - datos.target
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3, random_state=SEMILLA, stratify=y)
prob = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000)).fit(X_tr, y_tr).predict_proba(X_te)[:, 1]

print("2) Umbral vs. malignos que se escapan (FN) y falsas alarmas (FP)")
elegido = None
for umbral in np.arange(0.95, 0.0, -0.05):
    pred = prob >= umbral
    fn = int(((~pred) & (y_te == 1)).sum())
    fp = int((pred & (y_te == 0)).sum())
    if fn <= 1 and elegido is None:
        elegido = (round(umbral, 2), fn, fp)
    print(f"   umbral={umbral:.2f}  FN={fn:2d}  FP={fp:2d}")
print(f"   → El umbral más alto con FN ≤ 1 es {elegido[0]}: se escapan {elegido[1]} y hay {elegido[2]} falsas alarmas.")
print("     Bajar el umbral 'compra' seguridad (menos FN) a cambio de más exámenes innecesarios (FP).\n")

# --- 3. Ridge vs. lineal en un polinomio de grado 15 -----------------------------------------
rng = np.random.default_rng(SEMILLA)
x = np.sort(rng.uniform(0, 1, 30))
y_ruido = np.sin(2 * np.pi * x) + rng.normal(0, 0.25, size=x.size)
x_tr, x_te, yy_tr, yy_te = train_test_split(x.reshape(-1, 1), y_ruido, test_size=0.3, random_state=SEMILLA)

print("3) Polinomio de grado 15")
for nombre, regresor in [("LinearRegression", LinearRegression()), ("Ridge(alpha=0.001)", Ridge(alpha=0.001))]:
    modelo = make_pipeline(PolynomialFeatures(15), regresor).fit(x_tr, yy_tr)
    print(f"   {nombre:<20} RMSE train={root_mean_squared_error(yy_tr, modelo.predict(x_tr)):.3f}  "
          f"test={root_mean_squared_error(yy_te, modelo.predict(x_te)):.3f}")
print("   → Ridge 'castiga' los coeficientes grandes, la curva se suaviza y el error de test baja:")
print("     la regularización controla el overfitting sin tener que bajar el grado.")
