"""
Solución comentada: ejercicio guiado de viajes (módulo 04, notebook 1).

    uv run python 04-Preparacion-Datos/ejercicios/soluciones/solucion_04_viajes.py

Basada en la solución del profesor (sesion_3_preparacion_de_datos_desarrollo.ipynb),
con algunos ajustes: se imputa DESPUÉS de convertir la moneda y se normaliza el
destino con una función que tolera nuevas variantes de escritura.
"""

import pandas as pd
from sklearn.preprocessing import MinMaxScaler

TASA_USD_POR_EUR = 1.16

viajeros = pd.DataFrame(
    {
        "user_id": [136, 284, 101, 529, 800, 823],
        "age": [None, 38, 30, 43, 49, 28],
        "name": ["Ana", "Jose", "Tomas", "Viviana", "Carolina", "Katerine"],
    }
)
viajes = pd.DataFrame(
    {
        "user_id": [101, 284, 136, 800, 101, 800, 823, 529, 284],
        "date_of_journey": [
            "2018-01-16", "2017-07-13", "2019-10-10", "2018/03/20", "2019-12-24",
            "2017-10-17", "2016/11/02", "2019/09/14", "2019-08-07",
        ],
        "duration": [3, 3, 2, 4, 2, 3.5, 4.5, 2.5, 4.3],
        "destination": [
            "Costa Rica", "colombia", "Colombia", "Costa_Rica", "Colombia/",
            "Colombia", "Costa Rica", "Colombia", "Costa_Rica",
        ],
        "cost": [None, 775, 587, 913, 1333, 825, 1046, 613, 970],
        "currency": [None, "EUR", "USD", "USD", "USD", "EUR", "USD", "USD", "USD"],
    }
)

# 1) Integrar ---------------------------------------------------------------------
# LEFT desde viajes: queremos conservar TODOS los viajes aunque faltara el viajero.
# (Aquí todos existen, así que inner y left dan lo mismo; validate lo comprueba.)
data = pd.merge(viajes, viajeros, on="user_id", how="left", validate="many_to_one")
print("1) Filas después del join:", len(data))

# 2) Fechas -------------------------------------------------------------------------
# Unificamos el separador y convertimos con un formato explícito (más seguro que adivinar).
data["date_of_journey"] = pd.to_datetime(data["date_of_journey"].str.replace("/", "-"), format="%Y-%m-%d")
print("2) Tipo de la fecha:", data["date_of_journey"].dtype)

# 3) Moneda ---------------------------------------------------------------------------
es_eur = data["currency"] == "EUR"
data.loc[es_eur, "cost"] = data.loc[es_eur, "cost"] * TASA_USD_POR_EUR
data["currency"] = "USD"
print(f"3) {es_eur.sum()} costos convertidos de EUR a USD")


# 4) Destino --------------------------------------------------------------------------
def normalizar_destino(texto: str) -> str:
    """'colombia', 'Colombia/', 'Costa_Rica'… → 'Colombia' o 'Costa Rica'."""
    limpio = texto.lower().replace("_", " ").replace("/", "").strip()
    if "costa" in limpio:
        return "Costa Rica"
    if "colombia" in limpio:
        return "Colombia"
    return texto  # si aparece un destino nuevo, lo dejamos para revisarlo


data["destination"] = data["destination"].map(normalizar_destino)
print("4) Destinos:", data["destination"].unique().tolist())

# 5) Nulos ------------------------------------------------------------------------------
# Imputamos el costo con la media DEL MISMO DESTINO: Costa Rica y Colombia tienen costos
# distintos, así que la media global mezclaría peras con manzanas.
data["cost"] = data["cost"].fillna(data.groupby("destination")["cost"].transform("mean"))
data["age"] = data["age"].fillna(data["age"].median())
print("5) Nulos restantes:", int(data.isna().sum().sum()))

# 6) Nueva variable ---------------------------------------------------------------------
data["costo_por_dia"] = data["cost"] / data["duration"]

# 7) Respuesta -------------------------------------------------------------------------
resumen = data.groupby("destination")[["cost", "duration", "costo_por_dia"]].mean().round(1)
print("\n7) Promedios por destino\n", resumen, sep="")
mas_caro = resumen["costo_por_dia"].idxmax()
print(f"   → {mas_caro} es el más caro por día (USD {resumen.loc[mas_caro, 'costo_por_dia']:.0f}/día)")

# 8) Transformar ------------------------------------------------------------------------
data["cost_minmax"] = MinMaxScaler().fit_transform(data[["cost"]]).ravel()
# Destino tiene solo 2 valores y no hay orden: one-hot (o una sola columna 0/1, que es equivalente).
data = pd.get_dummies(data, columns=["destination"], prefix="dest", dtype=int)
print("\n8) Resultado final\n", data.drop(columns=["name", "currency"]).round({"cost": 2, "costo_por_dia": 2, "cost_minmax": 2}).to_string(index=False), sep="")
