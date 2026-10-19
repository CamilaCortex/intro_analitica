"""
Soluciones: ejercicios guiados del notebook 2 (House Prices), módulo 04.

    uv run python 04-Preparacion-Datos/ejercicios/soluciones/solucion_04_house_prices.py

Genera una figura en reports/m04_lotfrontage.png
"""

import matplotlib

matplotlib.use("Agg")  # permite generar la figura sin abrir ventanas
import matplotlib.pyplot as plt
import numpy as np

from intro_analitica import config
from intro_analitica.datos import cargar_house_prices
from intro_analitica.limpieza import limpiar_house_prices

crudo = cargar_house_prices()

# --- 1. LotFrontage: 0 vs. mediana del barrio -------------------------------------
con_cero = crudo["LotFrontage"].fillna(0)
con_mediana_barrio = crudo["LotFrontage"].fillna(
    crudo.groupby("Neighborhood")["LotFrontage"].transform("median")
)
print("1) LotFrontage")
print(f"   Media con 0:                {con_cero.mean():6.1f}")
print(f"   Media con mediana de barrio: {con_mediana_barrio.mean():6.1f}")
print("   → Imputar con 0 crea un 'pico' artificial en 0 (259 casas = 18 %) y baja la media.")
print("     La mediana por barrio conserva la forma de la distribución. Ninguna es 'la correcta':")
print("     depende de si creemos que el NaN significa 'no tiene frente' o 'no se midió'.")

config.asegurar_carpetas()
fig, ax = plt.subplots(figsize=(8, 3.5))
ax.hist(con_cero, bins=40, alpha=0.6, label="NaN → 0")
ax.hist(con_mediana_barrio, bins=40, alpha=0.6, label="NaN → mediana del barrio")
ax.set(title="LotFrontage según la estrategia de imputación", xlabel="pies")
ax.legend()
fig.savefig(config.REPORTS_DIR / "m04_lotfrontage.png", dpi=120, bbox_inches="tight")
print(f"   Figura en {(config.REPORTS_DIR / 'm04_lotfrontage.png').relative_to(config.RAIZ)}")

# --- 2. HasPool y GarageAge cuidando el centinela -------------------------------------
df = limpiar_house_prices(crudo)
df["HasPool"] = (df["PoolArea"] > 0).astype(int)
df["GarageAge"] = np.where(df["GarageYrBlt"] == -1, np.nan, df["YrSold"] - df["GarageYrBlt"])
print("\n2) Nuevas variables")
print(f"   Casas con piscina: {df['HasPool'].sum()}")
print(f"   GarageAge: mediana {np.nanmedian(df['GarageAge']):.0f} años; "
      f"{df['GarageAge'].isna().sum()} casas sin garaje quedan como NaN (no como 2009 años)")
print("   → En el modelo, esos NaN se imputan dentro del Pipeline o se acompañan de una variable HasGarage.")

# --- 3. Ordinales -----------------------------------------------------------------------
escala = {"Po": 1, "Fa": 2, "TA": 3, "Gd": 4, "Ex": 5, "No Basement": 0}
for col in ["ExterQual", "KitchenQual", "BsmtQual"]:
    df[f"{col}_num"] = df[col].map(escala)
print("\n3) Ordinales (correlación con SalePrice)")
print(df[["ExterQual_num", "KitchenQual_num", "BsmtQual_num", "SalePrice"]].corr()["SalePrice"].round(2).to_string())
print("   → 'No Basement' = 0: no tener sótano es 'menos' que tener uno malo. Es una decisión razonable,")
print("     pero también se podría usar one-hot para no imponer ese orden.")

# --- 4. Reflexión ---------------------------------------------------------------------------
print(
    "\n4) Si imputas ANTES de quitar duplicados, los registros repetidos cuentan dos veces en la\n"
    "   media/mediana y sesgan el valor imputado. Primero se limpia la estructura (duplicados) y\n"
    "   después el contenido (nulos)."
)
