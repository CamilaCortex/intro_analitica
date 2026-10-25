"""
Soluciones: ejercicios del notebook 01_pipeline_house_prices (módulo 05).

    uv run python 05-Pipelines-y-API/ejercicios/soluciones/solucion_01_pipeline.py
"""

import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.inspection import permutation_importance
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import KFold, cross_val_score, train_test_split

from intro_analitica import config
from intro_analitica.datos import cargar_house_prices_limpio
from intro_analitica.pipeline import construir_pipeline, construir_preprocesamiento

df = cargar_house_prices_limpio()
kfold = KFold(5, shuffle=True, random_state=config.SEMILLA)


def mape_cv(pipeline, X, y) -> float:
    return -cross_val_score(pipeline, X, y, cv=kfold, scoring="neg_mean_absolute_percentage_error").mean() * 100


# --- 1. Agregar TotalSF ---------------------------------------------------------------------------
print("1) ¿TotalSF mejora la lineal + log?")
for numericas in [config.FEATURES_NUMERICAS, config.FEATURES_NUMERICAS + ["TotalSF"]]:
    X = df[numericas + config.FEATURES_CATEGORICAS]
    pipe = construir_pipeline(LinearRegression())
    pipe.set_params(preprocesamiento=construir_preprocesamiento(numericas=numericas))
    print(f"   {len(numericas)} numéricas{' + TotalSF' if 'TotalSF' in numericas else '':<10} → MAPE CV = {mape_cv(pipe, X, df[config.TARGET]):.2f} %")
print("   → Prácticamente igual: TotalSF ≈ TotalBsmtSF + GrLivArea, y ambas ya están en el modelo.")
print("     Para un modelo lineal, una suma de variables que ya tiene es información redundante.")
print("     (En el módulo 04 sí ayudó porque se agregó junto con TotalBath y HouseAge.)")

# --- 2. Random Forest con y sin log ----------------------------------------------------------------
print("\n2) Random Forest: ¿le ayuda el log?")
X, y = df[config.FEATURES_MODELO], df[config.TARGET]
rf = RandomForestRegressor(n_estimators=200, random_state=config.SEMILLA, n_jobs=-1)
print(f"   Sin log → {mape_cv(construir_pipeline(rf, log_target=False), X, y):.2f} %")
print(f"   Con log → {mape_cv(construir_pipeline(rf, log_target=True), X, y):.2f} %")
print("   → A los árboles les afecta mucho menos: dividen por umbrales, no les importa la forma de la distribución.")
print("     El log ayuda sobre todo a los modelos lineales.\n")

# --- 3. Robustez ante nulos ---------------------------------------------------------------------------
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=config.SEMILLA)
modelo = construir_pipeline().fit(X_train, y_train)
casa = pd.DataFrame([{
    "LotArea": 9000, "OverallQual": 7, "OverallCond": 5, "YearBuilt": 2005, "YearRemodAdd": 2006,
    "GrLivArea": None, "TotalBsmtSF": 1000, "FullBath": 2, "BedroomAbvGr": 3, "GarageCars": 2,
    "Neighborhood": "CollgCr", "BldgType": "1Fam", "HouseStyle": "2Story", "KitchenQual": "Gd",
}])
print(f"3) Casa con GrLivArea = None → USD {modelo.predict(casa)[0]:,.0f}")
print("   → No falla: el SimpleImputer(median) del pipeline rellena el hueco con la mediana del TRAIN.")
print("     Ojo: la predicción es menos confiable; en la API conviene exigir los campos críticos.\n")

# --- 4. Importancia por permutación -------------------------------------------------------------------
resultado = permutation_importance(modelo, X_test, y_test, n_repeats=5, random_state=config.SEMILLA,
                                   scoring="neg_mean_absolute_percentage_error")
importancia = pd.Series(resultado.importances_mean * 100, index=X_test.columns).sort_values(ascending=False)
print("4) Importancia por permutación (cuántos puntos de MAPE se pierden al 'desordenar' cada variable)")
print(importancia.round(2).to_string())
print("   → A diferencia de feature_importances_, funciona con CUALQUIER modelo y habla de las variables ORIGINALES.")
