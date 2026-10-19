"""
Soluciones: ejercicios guiados del módulo 05 (EDA).

    uv run python 05-EDA/ejercicios/soluciones/solucion_05.py

Guarda las figuras en reports/m05_*.png
"""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

from intro_analitica import config
from intro_analitica.datos import cargar_house_prices_limpio
from intro_analitica.eda import outliers_iqr

df = cargar_house_prices_limpio()
config.asegurar_carpetas()

# --- 1. Precio por m² por barrio ---------------------------------------------------------
df["precio_m2"] = df["SalePrice"] / (df["GrLivArea"] * 0.092903)
por_barrio = df.groupby("Neighborhood").agg(
    precio_mediano=("SalePrice", "median"), precio_m2_mediano=("precio_m2", "median"), ventas=("SalePrice", "size")
)
top_total = por_barrio["precio_mediano"].idxmax()
top_m2 = por_barrio["precio_m2_mediano"].idxmax()
print("1) Precio por m²")
print(por_barrio.sort_values("precio_m2_mediano", ascending=False).head(5).round(0).to_string())
print(f"   → Más caro en total: {top_total} · más caro por m²: {top_m2}")
print("     Aquí coinciden, pero el ranking cambia más abajo: un barrio puede tener casas más grandes")
print("     (más caras en total) sin que el m² sea más caro. Para comparar ubicación, el m² es más justo.\n")

# --- 2. Precio mediano por mes ------------------------------------------------------------
mensual = df.groupby("MoSold")["SalePrice"].agg(["size", "median"])
fig, ax1 = plt.subplots(figsize=(8, 3.5))
ax1.bar(mensual.index, mensual["size"], color="lightgray", label="Ventas")
ax2 = ax1.twinx()
ax2.plot(mensual.index, mensual["median"], color="crimson", marker="o", label="Precio mediano")
ax1.set(title="Volumen vs. precio mediano por mes", xlabel="Mes", ylabel="Ventas")
ax2.set_ylabel("USD")
fig.savefig(config.REPORTS_DIR / "m05_estacionalidad.png", dpi=110, bbox_inches="tight")
plt.close(fig)
print("2) Precio mediano por mes")
print(mensual["median"].astype(int).to_string())
print(f"   Rango: {mensual['median'].min():,.0f} - {mensual['median'].max():,.0f}")
print("   → El VOLUMEN tiene una estacionalidad fuerte, pero el PRECIO se mueve poco y sin un patrón claro.")
print("     Lección: que se vendan más casas en verano no significa que se vendan más caras.\n")

# --- 3. Outliers extremos de LotArea (k=3) ----------------------------------------------
extremos = outliers_iqr(df["LotArea"], k=3)
print(f"3) LotArea: {outliers_iqr(df['LotArea']).sum()} outliers con k=1.5 · {extremos.sum()} con k=3")
fig, ax = plt.subplots(figsize=(7, 4))
sns.scatterplot(data=df, x="LotArea", y="SalePrice", hue=extremos, palette={False: "steelblue", True: "red"}, alpha=0.5, ax=ax)
ax.set(title="LotArea: outliers extremos (k=3) en rojo", xscale="log")
fig.savefig(config.REPORTS_DIR / "m05_lotarea_outliers.png", dpi=110, bbox_inches="tight")
plt.close(fig)
print("   → Lotes enormes NO implican precios enormes: LotArea es una variable 'ruidosa'.\n")

# --- 4. Hipótesis: chimenea --------------------------------------------------------------
df["tiene_chimenea"] = (df["Fireplaces"] > 0).map({True: "Sí", False: "No"})
print("4) H: las casas con chimenea valen más")
print(df.groupby("tiene_chimenea")["SalePrice"].agg(["size", "median"]).astype(int).to_string())
control = df.groupby(["OverallQual", "tiene_chimenea"])["SalePrice"].median().unstack().dropna()
print("\n   Controlando por calidad (mediana por OverallQual):")
print(control.astype(int).to_string())
print("   → Parece confirmada: con chimenea la mediana es mayor en casi todos los niveles de calidad,")
print("     aunque en general la brecha es menor que sin controlar (~41 %): parte del efecto 'chimenea'")
print("     era en realidad efecto 'calidad' (otra vez, variables de confusión).")
