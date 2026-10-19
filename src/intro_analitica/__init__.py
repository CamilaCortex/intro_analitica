"""
intro_analitica
===============

Paquete de utilidades del curso **Proyecto 1 — Introducción a la Analítica**.

La idea es sencilla: lo que escribimos en un notebook y queremos *reutilizar*
(cargar datos, limpiar, perfilar, evaluar) termina viviendo aquí como funciones
documentadas. Así los notebooks quedan cortos y legibles, y los scripts de cada
módulo pueden importar exactamente la misma lógica.

Uso típico (desde cualquier notebook o script, después de `uv sync`)::

    from intro_analitica.datos import cargar_house_prices
    from intro_analitica.limpieza import limpiar_house_prices

    df = cargar_house_prices()
    df_limpio = limpiar_house_prices(df)
"""

__version__ = "0.1.0"
