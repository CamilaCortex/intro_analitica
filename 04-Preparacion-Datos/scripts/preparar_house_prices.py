"""
preparar_house_prices.py: limpia House Prices y guarda la versión lista para EDA y modelado.

Uso (desde la raíz del repo)::

    uv run python 04-Preparacion-Datos/scripts/preparar_house_prices.py
    uv run python 04-Preparacion-Datos/scripts/preparar_house_prices.py --sin-variables-nuevas

Entrada:  data/raw/house_prices/train.csv
Salida:   data/processed/house_prices_limpio.csv

¿Por qué un script y no solo el notebook?
    El notebook sirve para EXPLORAR y explicar. El script sirve para REPETIR:
    cualquier persona del equipo (o un servidor) lo ejecuta y obtiene exactamente el
    mismo archivo. Toda la lógica vive en ``src/intro_analitica/limpieza.py``, de modo
    que el notebook y el script nunca se desincronizan.

[AVISO] Este script NO escala ni codifica variables. Eso se hace dentro del Pipeline
(módulo 07), aprendiendo solo del conjunto de entrenamiento, para evitar data leakage.
"""

import argparse

from intro_analitica import config
from intro_analitica.datos import cargar_house_prices
from intro_analitica.limpieza import agregar_variables, limpiar_house_prices


def main() -> None:
    parser = argparse.ArgumentParser(description="Limpieza de House Prices")
    parser.add_argument("--sin-variables-nuevas", action="store_true", help="No crear HouseAge, TotalSF, etc.")
    args = parser.parse_args()

    crudo = cargar_house_prices()
    print(f"Crudo:  {crudo.shape[0]} filas × {crudo.shape[1]} columnas · {int(crudo.isna().sum().sum())} celdas nulas\n")

    limpio = limpiar_house_prices(crudo, verbose=True)
    if not args.sin_variables_nuevas:
        limpio = agregar_variables(limpio)

    config.asegurar_carpetas()
    limpio.to_csv(config.HOUSE_PRICES_LIMPIO, index=False)

    perdidas = len(crudo) - len(limpio)
    print(f"\nLimpio: {limpio.shape[0]} filas × {limpio.shape[1]} columnas · 0 nulos")
    print(f"   Filas eliminadas por inconsistentes: {perdidas} ({perdidas / len(crudo):.1%})")
    print(f"Guardado en {config.HOUSE_PRICES_LIMPIO.relative_to(config.RAIZ)}")


if __name__ == "__main__":
    main()
