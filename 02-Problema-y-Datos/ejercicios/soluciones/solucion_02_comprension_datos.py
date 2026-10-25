"""
Soluciones: ejercicios guiados del notebook 2 (comprensión de los datos), módulo 02.

    uv run python 02-Problema-y-Datos/ejercicios/soluciones/solucion_02_comprension_datos.py
"""

from intro_analitica.datos import (
    cargar_house_prices,
    cargar_housing_simple,
    leer_diccionario_house_prices,
)
from intro_analitica.eda import perfil_rapido

df = cargar_house_prices()
diccionario = leer_diccionario_house_prices()

# --- 1. Descripción de las 5 variables más correlacionadas -----------------------
print("1) Top 5 correlaciones con SalePrice")
top5 = df.select_dtypes("number").corr()["SalePrice"].drop(["SalePrice", "Id"]).nlargest(5)
for columna, r in top5.items():
    print(f"   {columna:<12} r={r:.2f}  → {diccionario.get(columna, '?')}")

# --- 2. Hipótesis del sótano -----------------------------------------------------------
print("\n2) ¿Sin datos de sótano ⇒ TotalBsmtSF == 0?")
cols_sotano = ["BsmtQual", "BsmtCond", "BsmtExposure", "BsmtFinType1", "BsmtFinType2"]
todos_nulos = df[cols_sotano].isna().all(axis=1)
print(f"   Casas con TODOS los Bsmt* nulos: {todos_nulos.sum()}")
print(f"   De ellas, con TotalBsmtSF == 0: {(df.loc[todos_nulos, 'TotalBsmtSF'] == 0).sum()}  [OK] hipótesis confirmada")
algunos = df[cols_sotano].isna().any(axis=1) & ~todos_nulos
print(f"   Casas con ALGUNOS nulos (inconsistentes): {algunos.sum()} → se revisan en el módulo 03")

# --- 3. Duplicados ignorando el Id ---------------------------------------------------
print(f"\n3) Duplicados sin contar Id: {df.drop(columns='Id').duplicated().sum()}")
print("   → 0: cada fila es una venta distinta. (Si hubiera, revisaríamos si son la misma casa vendida dos veces)")

# --- 4. Perfil de housing.csv --------------------------------------------------------
print("\n4) Perfil de housing.csv (primeras líneas)")
casas = cargar_housing_simple()
print(perfil_rapido(casas).to_string())
print(
    "   Hipótesis de ejemplo:\n"
    "   - H1: las casas con aire acondicionado (airco='yes') son más caras.\n"
    "   - H2: el precio crece con lotsize, pero con rendimientos decrecientes."
)
