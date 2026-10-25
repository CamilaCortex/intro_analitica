# Ejercicios: Módulo 04, Modelado y métricas

> **Roten los roles:** quien no ha sido piloto todavía lo es hoy. Recuerden: **solo el piloto edita el notebook**.

| Clase | Secciones del notebook del equipo |
|---|---|
| 26 de octubre | 0. Configuración · 1. El problema · 2. Los datos |
| 27 de octubre | 3. Limpieza · 4. EDA |
| **28 de octubre (hoy)** | **5. Modelo** |
| 11 de noviembre | 6. Conclusiones |

---

## Parte 1: Práctica guiada (15 min, primera parte de la clase)

1. **Métricas a mano (8 min).** Un modelo de avalúos predijo estos precios:

   | Casa | Precio real | Precio predicho |
   |---|---|---|
   | 1 | 250.000 | 240.000 |
   | 2 | 300.000 | 310.000 |
   | 3 | 200.000 | 210.000 |
   | 4 | 400.000 | 380.000 |
   | 5 | 350.000 | 340.000 |

   Calculen el **MAE** (promedio del error absoluto, en dólares) y el **MAPE** (promedio del error en porcentaje). Pueden hacerlo a mano o con este código:

   ```python
   import numpy as np
   reales = np.array([250_000, 300_000, 200_000, 400_000, 350_000])
   predichos = np.array([240_000, 310_000, 210_000, 380_000, 340_000])
   errores = reales - predichos
   print("MAE :", np.mean(np.abs(errores)))
   print("MAPE:", np.mean(np.abs(errores / reales)) * 100, "%")
   ```

   ¿Cómo le explicarían el resultado a un gerente, en una frase y sin usar la palabra "MAPE"?

2. **¿Qué error es peor? (7 min, en parejas).** Para cada caso, ¿qué métrica priorizarían: *precision* (evitar falsas alarmas) o *recall* (que no se escape ningún caso)?

   | Caso | Métrica |
   |---|---|
   | Detectar tumores malignos en mamografías | |
   | Filtro de correo no deseado (spam) | |
   | Detectar transacciones fraudulentas | |
   | Recomendar a quién ofrecerle un crédito | |

Soluciones en `soluciones/solucion_01_metricas.py` (ejercicios 1 y 2).

---

## Parte 2: Salas de Zoom, el modelo del equipo (45 min)

> **Objetivo:** entrenar un *baseline* y dos modelos, y responder si el modelo le gana al *baseline* y si cumple el criterio de éxito.
> **Viene de:** los hallazgos del EDA (sección 4) y el criterio de éxito (sección 1).
> **Va a:** las conclusiones y la sustentación.

### Paso 0: Actualizar (2 min)

Todos ejecutan `git pull`. El piloto abre el notebook y ejecuta todo hasta el final de la sección 4.

### Paso 1: Elegir la métrica principal (5 min)

Entre los tres, decidan cuál métrica de la tabla de la sección 5.4 es la **principal** para su negocio y por qué. Si en la sección 1 escribieron un criterio de éxito con otra métrica, revisen si sigue teniendo sentido.

| Si el problema es... | Métrica principal sugerida |
|---|---|
| Regresión y el negocio piensa en porcentajes | MAPE |
| Regresión con valores en cero o muy cercanos a cero | MAE |
| Clasificación con clases balanceadas | *Accuracy* o F1 |
| Clasificación donde se escapa un caso importante | *Recall* |
| Clasificación donde las falsas alarmas cuestan | *Precision* |

### Paso 2: Variables y entrenamiento (secciones 5.1 a 5.4, 18 min)

1. **5.1:** escriban en `VARIABLES` la lista de variables que el EDA mostró como importantes (entre 5 y 15 suele ser suficiente). Revisen que **no** incluyan columnas que se conocen después del resultado (*data leakage*).
2. Ejecuten 5.2, 5.3 y 5.4. La tabla compara el *baseline*, el modelo lineal y el árbol de decisión, en train y en test.
3. **Experimento rápido:** cambien la lista de variables (agreguen o quiten 2 o 3) y vuelvan a ejecutar 5.1 a 5.4. ¿Mejora o empeora la métrica principal en test? Dejen la versión que funcione mejor.

> **Si aparece un error:** lean la última línea del mensaje. Los más comunes son un nombre de columna mal escrito en `VARIABLES` o una columna de texto con miles de valores distintos (sáquenla de la lista).

### Paso 3: Revisar errores e interpretar (sección 5.5, 12 min)

1. Escriban en `MEJOR_MODELO` el nombre del modelo con mejor resultado en **test** y ejecuten la gráfica.
2. Llenen la tabla de interpretación. Las dos preguntas clave:
   - ¿Cuánto mejora frente al *baseline*?
   - ¿Cumple el criterio de éxito de la sección 1? **Si no lo cumple, también es un resultado válido:** expliquen qué creen que falta (más datos, otras variables, otro modelo).

### Paso 4: Subir los cambios (8 min)

Antes de subir, ejecuten *Restart Kernel and Run All*.

**Piloto:**

```bash
git pull
git add notebooks/proyecto_equipo.ipynb
git commit -m "feat: agrega baseline, modelos y evaluación"
git push
```

**Relator:** agrega al README del equipo la tabla de resultados del modelo frente al *baseline* (solo la métrica principal, en test) y marca el avance del módulo 04.

```bash
git pull
git add README.md
git commit -m "docs: agrega resultados del modelo al README"
git push
```

**Copiloto:** hace `git pull` y ejecuta el notebook completo en su computador.

### Entregable

- [ ] Sección 5 ejecutada, con la tabla de modelos y la gráfica de errores
- [ ] Tabla de interpretación completa: modelo elegido, mejora frente al *baseline* y criterio de éxito
- [ ] README del equipo con el resultado principal
- [ ] El notebook corre completo en el computador del copiloto

---

## Plenaria (10 min)

Cada relator muestra en 1 minuto su resultado: *"el baseline se equivoca en X, nuestro modelo en Y"*. El grupo responde: ¿hay señales de *overfitting* (mucho mejor en train que en test)?

## Trabajo autónomo (29 de octubre al 10 de noviembre)

Estas dos semanas no hay clase. Cada equipo:

1. Revisa y mejora las secciones 1 a 5 del notebook con lo aprendido (mejor limpieza, más hallazgos, otras variables).
2. **Avance intermedio, 4 de noviembre:** el notebook debe correr completo de principio a fin y el README debe tener problema, dataset, hallazgos y resultado del modelo. La profesora revisará el repositorio ese día.
3. Opcional: prueben un modelo más en la sección 5.4, por ejemplo `RandomForestRegressor` o `RandomForestClassifier` de `sklearn.ensemble`.
