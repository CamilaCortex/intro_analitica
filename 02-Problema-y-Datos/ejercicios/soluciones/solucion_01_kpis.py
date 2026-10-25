"""
Soluciones: ejercicios guiados del notebook 1 (KPIs), módulo 02.

Ejecutar desde la raíz del repo::

    uv run python 02-Problema-y-Datos/ejercicios/soluciones/solucion_01_kpis.py
"""

from intro_analitica.datos import cargar_house_prices

df = cargar_house_prices()
df["precio_m2"] = df["SalePrice"] / (df["GrLivArea"] * 0.092903)

# --- Ejercicio 1: precio mediano por m² por año -------------------------------
print("1) Precio mediano por m² (USD) por año")
print(df.groupby("YrSold")["precio_m2"].median().round(0).to_string())
print(
    "   → Se mantiene casi estable (~1.270-1.300 USD/m²); baja un poco en 2008-2009\n"
    "     (crisis hipotecaria) y se recupera en 2010. El precio por m² es más\n"
    "     estable que el precio total porque corrige por el tamaño de la casa.\n"
)

# --- Ejercicio 2: SaleCondition ------------------------------------------------
print("2) Precio mediano por tipo de venta")
print(df.groupby("SaleCondition")["SalePrice"].agg(["size", "median"]).sort_values("median").to_string())
print(
    "   → 'Abnorml' (remates, embargos, ventas forzadas) tiene una mediana de ~130.000,\n"
    "     frente a ~160.000 de 'Normal': quien vende con urgencia acepta menos.\n"
    "     'Partial' (casas nuevas, vendidas antes de terminarse) es la más cara.\n"
    "     [AVISO] Ojo: 'Abnorml' tiene solo 101 casas; hay que confirmarlo con más datos.\n"
)

# --- Ejercicio 3: clasificación ----------------------------------------------------
print("3) Clasificación de preguntas")
respuestas = {
    "a) ¿Cuántas casas con piscina se vendieron?": "Descriptivo (conteo de lo que pasó)",
    "b) ¿Qué precio debería pedir por mi casa?": "Predictivo (estimar un valor), con un toque prescriptivo",
    "c) ¿Por qué las casas de NoRidge son más caras?": "Diagnóstico (buscar causas)",
    "d) ¿A quién le conviene remodelar la cocina?": "Prescriptivo (recomendar una acción)",
}
for pregunta, tipo in respuestas.items():
    print(f"   {pregunta:<50} → {tipo}")
