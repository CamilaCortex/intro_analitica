"""
predecir.py: usa el modelo guardado para predecir (predicción por lotes o de una casa).

Uso::

    # Una casa, en JSON
    uv run python 07-Pipelines/scripts/predecir.py --json '{"LotArea": 9000, "OverallQual": 7, "OverallCond": 5,
        "YearBuilt": 2005, "YearRemodAdd": 2006, "GrLivArea": 1800, "TotalBsmtSF": 1000, "FullBath": 2,
        "BedroomAbvGr": 3, "GarageCars": 2, "Neighborhood": "CollgCr", "BldgType": "1Fam",
        "HouseStyle": "2Story", "KitchenQual": "Gd"}'

    # Muchas casas (predicción "batch"): por ejemplo, el test.csv de Kaggle, que no trae precio
    uv run python 07-Pipelines/scripts/predecir.py --csv data/raw/house_prices/test.csv --salida reports/predicciones.csv

Requiere haber corrido antes ``07-Pipelines/scripts/train.py``.
"""

import argparse
import json
import sys
from pathlib import Path

import joblib
import pandas as pd

from intro_analitica import config

RUTA_MODELO = config.MODELS_DIR / "house_price_model.joblib"


def main() -> None:
    parser = argparse.ArgumentParser(description="Predicciones con el modelo guardado")
    grupo = parser.add_mutually_exclusive_group(required=True)
    grupo.add_argument("--json", help="Una casa en formato JSON")
    grupo.add_argument("--csv", type=Path, help="CSV con varias casas")
    parser.add_argument("--salida", type=Path, help="(con --csv) dónde guardar las predicciones")
    args = parser.parse_args()

    if not RUTA_MODELO.exists():
        sys.exit("[ERROR] No hay modelo. Primero: uv run python 07-Pipelines/scripts/train.py")
    modelo = joblib.load(RUTA_MODELO)

    datos = pd.DataFrame([json.loads(args.json)]) if args.json else pd.read_csv(args.csv)
    faltan = set(config.FEATURES_MODELO) - set(datos.columns)
    if faltan:
        sys.exit(f"[ERROR] Faltan columnas: {sorted(faltan)}")

    predicciones = modelo.predict(datos[config.FEATURES_MODELO])

    if args.json:
        print(f"Precio estimado: USD {predicciones[0]:,.0f}")
        return

    resultado = pd.DataFrame({"Id": datos.get("Id", datos.index), "SalePrice_predicho": predicciones.round(0)})
    print(resultado.head(10).to_string(index=False))
    print(f"… {len(resultado)} predicciones · mediana USD {resultado['SalePrice_predicho'].median():,.0f}")
    if args.salida:
        args.salida.parent.mkdir(parents=True, exist_ok=True)
        resultado.to_csv(args.salida, index=False)
        print(f"{args.salida}")


if __name__ == "__main__":
    main()
