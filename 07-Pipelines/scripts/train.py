"""
train.py: entrena el pipeline de House Prices y lo guarda listo para producción.

Uso (desde la raíz del repo)::

    uv run python 07-Pipelines/scripts/train.py                 # hiperparámetros por defecto
    uv run python 07-Pipelines/scripts/train.py --buscar        # con GridSearchCV (más lento, mejor)
    uv run python 07-Pipelines/scripts/train.py --version 1.1.0

Qué hace, paso a paso:
    1. Carga data/processed/house_prices_limpio.csv (lo genera si no existe).
    2. Divide train/test (80/20) con la semilla del curso.
    3. Construye el pipeline con ``intro_analitica.pipeline.construir_pipeline``.
    4. (Opcional) Busca hiperparámetros con validación cruzada.
    5. Evalúa en test y verifica el criterio de negocio (MAPE < 15 %).
    6. Reentrena con TODOS los datos y guarda:
         models/house_price_model.joblib  → el pipeline
         models/house_price_model.json    → metadatos (versión, fecha, features, métricas)

¿Por qué reentrenar con todo al final?
    El test ya cumplió su función (estimar el desempeño). Para producción queremos
    que el modelo aprenda de la mayor cantidad de datos posible.
"""

import argparse
import json
from datetime import datetime

import joblib
from sklearn.model_selection import GridSearchCV, KFold, train_test_split

from intro_analitica import config
from intro_analitica.datos import cargar_house_prices_limpio
from intro_analitica.metricas import metricas_regresion
from intro_analitica.pipeline import construir_pipeline

CRITERIO_MAPE = 15.0
NOMBRE_MODELO = "house_price_model"

GRILLA = {
    "modelo__regressor__learning_rate": [0.03, 0.1],
    "modelo__regressor__max_leaf_nodes": [15, 31],
    "modelo__regressor__min_samples_leaf": [10, 20],
    "modelo__regressor__l2_regularization": [0.0, 1.0],
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Entrena y guarda el pipeline de House Prices")
    parser.add_argument("--buscar", action="store_true", help="Buscar hiperparámetros con GridSearchCV")
    parser.add_argument("--version", default="1.0.0", help="Versión del modelo (semver)")
    args = parser.parse_args()

    # 1-2. Datos
    df = cargar_house_prices_limpio()
    X, y = df[config.FEATURES_MODELO], df[config.TARGET]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=config.SEMILLA)
    print(f"Datos: {len(df)} casas · train={len(X_train)} · test={len(X_test)}")

    # 3-4. Pipeline (+ búsqueda opcional)
    pipeline = construir_pipeline()
    hiperparametros = {}
    if args.buscar:
        print("Buscando hiperparámetros (GridSearchCV, 5 folds)...")
        busqueda = GridSearchCV(
            pipeline, GRILLA, cv=KFold(5, shuffle=True, random_state=config.SEMILLA),
            scoring="neg_mean_absolute_percentage_error", n_jobs=-1,
        )
        busqueda.fit(X_train, y_train)
        pipeline = busqueda.best_estimator_
        hiperparametros = {k.split("__")[-1]: v for k, v in busqueda.best_params_.items()}
        print(f"   Mejores: {hiperparametros} · MAPE CV = {-busqueda.best_score_ * 100:.2f} %")
    else:
        pipeline.fit(X_train, y_train)

    # 5. Evaluación
    metricas = metricas_regresion(y_test, pipeline.predict(X_test))
    cumple = metricas["MAPE_%"] < CRITERIO_MAPE
    print(f"Test: {metricas}")
    print(f"   Criterio de negocio MAPE < {CRITERIO_MAPE} %: {'CUMPLE' if cumple else 'NO CUMPLE'}")

    # 6. Reentrenar con todo y guardar
    pipeline.fit(X, y)
    config.asegurar_carpetas()
    ruta_modelo = config.MODELS_DIR / f"{NOMBRE_MODELO}.joblib"
    ruta_meta = config.MODELS_DIR / f"{NOMBRE_MODELO}.json"
    joblib.dump(pipeline, ruta_modelo)
    ruta_meta.write_text(
        json.dumps(
            {
                "modelo": "HistGradientBoostingRegressor + log(target)",
                "version": args.version,
                "entrenado_en": datetime.now().isoformat(timespec="seconds"),
                "features_numericas": config.FEATURES_NUMERICAS,
                "features_categoricas": config.FEATURES_CATEGORICAS,
                "hiperparametros": hiperparametros or "por defecto",
                "metricas_test": metricas,
                "cumple_criterio_negocio": cumple,
                "n_entrenamiento_final": len(X),
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    print(f"Modelo:     {ruta_modelo.relative_to(config.RAIZ)}")
    print(f"Metadatos:  {ruta_meta.relative_to(config.RAIZ)}")


if __name__ == "__main__":
    main()
