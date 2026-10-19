"""
baseline.py: compara un baseline contra 3 modelos con validación cruzada, para cualquier CSV.

Uso::

    # House Prices (regresión)
    uv run python 06-Modelado-Metricas/scripts/baseline.py data/processed/house_prices_limpio.csv --target SalePrice

    # Dataset del equipo: clasificación
    uv run python 06-Modelado-Metricas/scripts/baseline.py data/processed/mis_datos.csv --target churn --tipo clasificacion

    # Elegir columnas (por defecto usa todas menos el target y las que parecen IDs)
    uv run python 06-Modelado-Metricas/scripts/baseline.py datos.csv --target y --columnas edad ingreso ciudad

Qué hace:
    1. Detecta columnas numéricas y categóricas.
    2. Arma un preprocesamiento seguro (imputar + escalar + one-hot) DENTRO de cada fold.
    3. Compara con validación cruzada (5 folds):
         regresión     → Dummy(mediana), Lineal, Random Forest, Gradient Boosting   [MAE, RMSE, MAPE, R²]
         clasificación → Dummy(mayoritaria), Logística, Random Forest, Gradient Boosting [Accuracy, F1, AUC]

Es un punto de partida rápido para el proyecto: el detalle de cada paso se explica en
los notebooks del módulo 06 y los pipelines en el módulo 07.
"""

import argparse
import warnings
from pathlib import Path

import pandas as pd
from sklearn.compose import make_column_selector, make_column_transformer
from sklearn.dummy import DummyClassifier, DummyRegressor
from sklearn.ensemble import (
    HistGradientBoostingClassifier,
    HistGradientBoostingRegressor,
    RandomForestClassifier,
    RandomForestRegressor,
)
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.model_selection import KFold, StratifiedKFold, cross_validate
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

SEMILLA = 42


def construir_preprocesamiento():
    """Imputa y escala las numéricas; imputa y aplica one-hot a las categóricas."""
    return make_column_transformer(
        (make_pipeline(SimpleImputer(strategy="median"), StandardScaler()), make_column_selector(dtype_include="number")),
        (
            make_pipeline(SimpleImputer(strategy="most_frequent"), OneHotEncoder(handle_unknown="infrequent_if_exist", min_frequency=5, sparse_output=False)),
            make_column_selector(dtype_exclude="number"),
        ),
    )


def modelos(tipo: str) -> dict:
    if tipo == "regresion":
        return {
            "Baseline (mediana)": DummyRegressor(strategy="median"),
            "Regresión lineal": LinearRegression(),
            "Random Forest": RandomForestRegressor(n_estimators=200, random_state=SEMILLA, n_jobs=-1),
            "Gradient Boosting": HistGradientBoostingRegressor(random_state=SEMILLA),
        }
    return {
        "Baseline (mayoritaria)": DummyClassifier(strategy="most_frequent"),
        "Regresión logística": LogisticRegression(max_iter=2000),
        "Random Forest": RandomForestClassifier(n_estimators=200, random_state=SEMILLA, n_jobs=-1),
        "Gradient Boosting": HistGradientBoostingClassifier(random_state=SEMILLA),
    }


def metricas(tipo: str, n_clases: int) -> dict:
    if tipo == "regresion":
        return {
            "MAE": "neg_mean_absolute_error",
            "RMSE": "neg_root_mean_squared_error",
            "MAPE": "neg_mean_absolute_percentage_error",
            "R2": "r2",
        }
    if n_clases == 2:
        return {"Accuracy": "accuracy", "F1": "f1", "AUC": "roc_auc"}
    return {"Accuracy": "accuracy", "F1_macro": "f1_macro"}


def parecen_ids(df: pd.DataFrame) -> list[str]:
    """Columnas con un valor distinto por fila (no float) o con 'id' en el nombre."""
    return [
        c for c in df.columns
        if c.lower() in {"id", "rownames"} or c.lower().endswith("_id")
        or (df[c].nunique() == len(df) and not pd.api.types.is_float_dtype(df[c]))
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description="Baseline vs. modelos con validación cruzada")
    parser.add_argument("csv", type=Path)
    parser.add_argument("--target", required=True)
    parser.add_argument("--tipo", choices=["regresion", "clasificacion"], default="regresion")
    parser.add_argument("--columnas", nargs="*", help="Variables a usar (por defecto, todas menos el target y los IDs)")
    parser.add_argument("--sep", default=",")
    args = parser.parse_args()

    df = pd.read_csv(args.csv, sep=args.sep).dropna(subset=[args.target])
    columnas = args.columnas or [c for c in df.columns if c != args.target and c not in parecen_ids(df)]
    X, y = df[columnas], df[args.target]

    n_clases = y.nunique()
    cv = (
        KFold(5, shuffle=True, random_state=SEMILLA)
        if args.tipo == "regresion"
        else StratifiedKFold(5, shuffle=True, random_state=SEMILLA)
    )
    scoring = metricas(args.tipo, n_clases)

    print(f"\n{args.csv.name} · target='{args.target}' · {args.tipo} · {len(df):,} filas · {len(columnas)} variables")
    if args.tipo == "clasificacion":
        print("   Distribución de clases:", y.value_counts(normalize=True).round(3).to_dict())

    filas = {}
    for nombre, modelo in modelos(args.tipo).items():
        pipeline = make_pipeline(construir_preprocesamiento(), modelo)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            res = cross_validate(pipeline, X, y, cv=cv, scoring=scoring, n_jobs=1)
        fila = {}
        for metrica in scoring:
            valores = res[f"test_{metrica}"]
            if scoring[metrica].startswith("neg_"):
                valores = -valores
            if metrica == "MAPE":
                valores = valores * 100
            fila[metrica] = f"{valores.mean():,.3f} ± {valores.std():,.3f}"
        filas[nombre] = fila
        print(f"   - {nombre}")

    print("\nResultados (validación cruzada, 5 folds: media ± desviación)\n")
    print(pd.DataFrame(filas).T.to_string())
    print("\nSi un modelo no le gana claramente al baseline, revisen las variables antes de probar modelos más complejos.")


if __name__ == "__main__":
    main()
