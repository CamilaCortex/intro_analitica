# data/

| Carpeta / archivo | Qué contiene | ¿Se versiona? |
|---|---|---|
| `raw/house_prices/train.csv` | House Prices (Ames, Iowa): 1460 casas × 81 columnas, con `SalePrice` | sí |
| `raw/house_prices/test.csv` | Mismas columnas, sin `SalePrice` (para simular predicciones "nuevas") | sí |
| `raw/house_prices/data_description.txt` | Diccionario de datos: qué significa cada columna y cada código | sí |
| `raw/housing.csv` | 546 casas, 12 variables (ejemplo de API del profesor) | sí |
| `processed/` | Lo que generan los notebooks y scripts (p.ej. `house_prices_limpio.csv`) | no |

## Reglas de oro

1. **Nunca modifiques `raw/`.** Si necesitas cambiar algo, hazlo con código y guarda el resultado en `processed/`.
2. **Todo lo de `processed/` se puede regenerar** ejecutando los scripts. Por eso no se sube a git.
3. **Datasets grandes (>50 MB) no van a GitHub.** Documenta en el README de dónde se descargan.

Fuente original de House Prices: [Kaggle: House Prices, Advanced Regression Techniques](https://www.kaggle.com/c/house-prices-advanced-regression-techniques) (De Cock, 2011).
