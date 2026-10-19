# Módulo 03: CRISP-DM, la metodología para proyectos de datos

> **Objetivo:** tener un **mapa** para el proyecto: saber en qué fase está el equipo, qué entregables tiene cada fase y por qué se vuelve hacia atrás (¡y está bien!).

**Duración sugerida:** 2 horas · **Basado en:** `sesion_2_crisp_dm.pdf` del profesor

## Contenido

| Archivo | Para qué sirve |
|---|---|
| `README.md` | Las 6 fases explicadas paso a paso |
| `notebooks/01_comprension_negocio_y_datos.ipynb` | Fases 1 y 2 aplicadas a House Prices |
| `scripts/perfil_inicial.py` | Genera un reporte de calidad en Markdown para **cualquier** CSV |
| `plantillas/project_charter.md` | Plantilla del *project charter* del equipo |
| `ejercicios/EJERCICIOS.md` | Actividad en salas: *charter* y perfil del dataset del equipo |
| `presentacion/03-CRISP-DM.pptx` | Diapositivas |

---

## 1. ¿Por qué una metodología?

La mayoría de proyectos de datos no fallan por el algoritmo, sino porque:

- se resolvió **el problema equivocado**,
- los datos no servían y nadie lo notó a tiempo,
- el modelo nunca se usó.

**CRISP-DM** (*Cross-Industry Standard Process for Data Mining*) nació a finales de los 90 (Daimler-Chrysler, SPSS, NCR y OHRA) y sigue siendo la metodología más usada porque es **sistemática, versátil, repetible y orientada al negocio**.

| | KDD | SEMMA | **CRISP-DM** |
|---|---|---|---|
| Enfoque | Académico | Orientado a una herramienta (SAS) | **Orientado al negocio** |

## 2. El ciclo

```
                ┌──────────────────────┐
         ┌─────>│ 1. Comprensión del   │<─────┐
         │      │    negocio           │      │
         │      └─────────┬────────────┘      │
         │                ▼                   │
         │      ┌──────────────────────┐      │
         │      │ 2. Comprensión de    │      │
         │      │    los datos         │      │
         │      └─────────┬────────────┘      │
   ┌─────┴────┐           ▼                   │
   │6.Desplie-│ ┌──────────────────────┐      │
   │   gue    │ │ 3. Preparación de    │<──┐  │
   └─────▲────┘ │    los datos         │   │  │
         │      └─────────┬────────────┘   │  │
         │                ▼                │  │
         │      ┌──────────────────────┐   │  │
         │      │ 4. Modelado          │───┘  │
         │      └─────────┬────────────┘      │
         │                ▼                   │
         │      ┌──────────────────────┐      │
         └──────│ 5. Evaluación        │──────┘
                └──────────────────────┘
          La iteración es el eje central
```

## 3. Las 6 fases, paso a paso

### Fase 1: Comprensión del negocio

- Entender **qué problema** se quiere resolver y **quién decide**.
- Traducirlo a un **objetivo de ciencia de datos** y a un **criterio de éxito**.
- Tener a la gente de negocio del lado es crucial.

| Nivel | Ejemplo (churn) | Ejemplo (inmobiliaria) |
|---|---|---|
| Negocio | Reducir la pérdida de clientes | Dar avalúos rápidos y confiables |
| Ciencia de datos | Modelo que prediga la probabilidad de churn | Modelo que estime `SalePrice` |
| Éxito | Reducir el churn real un 10 % en 3 meses | Error típico (MAPE) < 15 % |

**Entregables:** declaración del problema y métricas de éxito · recursos, limitaciones y riesgos · plan preliminar → **[project charter](plantillas/project_charter.md)**

### Fase 2: Comprensión de los datos

- Recolectar los datos y entender **qué representa cada fila y cada columna**.
- Detectar problemas de **calidad, volumen, variedad y sesgos**.
- Generar **hipótesis** iniciales.

Revisión inicial mínima: histogramas · boxplots · correlaciones · conteo de nulos · cardinalidad de las categóricas · *outliers*.

**Entregables:** informe descriptivo · problemas detectados y posibles causas · hipótesis → `scripts/perfil_inicial.py`

> Usa fuentes confiables: los datos de calidad tienen pocos faltantes y duplicados, y representan bien todas las subcategorías.

### Fase 3: Preparación de los datos → [Módulo 04](../04-Preparacion-Datos/)

Construir el dataset final: imputar nulos, codificar (*one-hot*, *label encoding*), escalar, seleccionar variables y crear nuevas (*feature engineering*).

**Entregables:** dataset preparado (train/test) · documentación de las transformaciones · justificación de las variables elegidas

### Fase 4: Modelado → [Módulos 06 y 07](../06-Modelado-Metricas/)

Elegir algoritmos según el tipo de problema, definir **qué métrica optimizar** y comparar candidatos con validación cruzada.

> Ejemplo (churn): regresión logística F1 = 0.72, árbol F1 = 0.76, Random Forest F1 = 0.81 → se elige RF por el balance entre desempeño e interpretabilidad.

**Entregables:** modelos entrenados y comparados · parámetros y resultados de validación · importancia de variables

**Discusión:** ¿qué pesa más, el desempeño o la interpretabilidad?

### Fase 5: Evaluación

Verificar si el modelo cumple los **objetivos de negocio**, no solo las métricas técnicas. Analizar errores y sesgos y **comunicar** los resultados.

> Para negocio: cómo ayuda el modelo al objetivo. Para un público técnico: algoritmos e hiperparámetros. **El *storytelling* sencillo y visual gana.**

### Fase 6: Despliegue → [Módulo 08](../08-API-FastAPI/)

| En tiempo real (API) | Por lotes (*batch*) |
|---|---|
| Respuesta inmediata a cada solicitud | Procesa muchos datos de una vez (diario, semanal…) |
| Baja latencia | Mayor latencia |
| Consume recursos todo el tiempo | Consume recursos solo cuando corre |

**Mantenimiento:** monitorear el desempeño (*data drift*), etiquetar datos nuevos, protocolo de errores y planes de reentrenamiento.

## 4. KPIs: lo que el proyecto optimiza

Preguntas que debes hacerte sobre tu KPI:

- ¿Es muy general? ¿Mide **realmente** lo que quiero?
- ¿Qué otros factores lo afectan? ¿Los controlo?
- ¿Es difícil de medir? ¿Hay fuentes para construirlo?
- ¿Con qué periodicidad se mide?
- ¿Se relaciona con la métrica que optimiza el modelo?
- ¿Los *stakeholders* están de acuerdo?

## 5. Caso de ejemplo: e-commerce de moda

| Fase | Qué se hizo |
|---|---|
| Negocio | Los clientes no recompran → identificar a los que tienen riesgo de abandono. Meta: +15 % de recompra |
| Datos | 10.000 clientes, 25 variables (historial, género, edad, visitas) |
| Preparación | Imputación + nueva variable "días desde la última compra" |
| Modelado | Random Forest → AUC = 0.84 |
| Evaluación | Cumple el objetivo |
| Despliegue | Dashboard + campaña automática de retención |

**¿Qué riesgos ven? ¿Dónde podría fallar?** (pista: ¿AUC 0.84 garantiza +15 % de recompra?)

## 6. Paso a paso en el notebook

1. **Fase 1:** escribir el problema de la inmobiliaria en el formato del *charter*.
2. **Fase 2:** dimensiones, diccionario de datos, tipos, nulos, cardinalidad y target.
3. Detectar **problemas de calidad** y escribir **hipótesis**.
4. **Actividad puente** hacia el módulo 04: ¿qué harías con una tabla "sucia"?

## 7. Script reutilizable

```bash
# Reporte de House Prices en pantalla
uv run python 03-CRISP-DM/scripts/perfil_inicial.py data/raw/house_prices/train.csv

# Reporte del dataset del equipo, guardado en docs/
uv run python 03-CRISP-DM/scripts/perfil_inicial.py data/raw/mis_datos.csv --salida docs/perfil_inicial.md
```

---

## Checklist del módulo

- [ ] Sé nombrar las 6 fases y el entregable principal de cada una
- [ ] Sé traducir un problema de negocio a un objetivo de ciencia de datos con criterio de éxito
- [ ] El equipo tiene su *project charter* y el perfil inicial de su dataset

**Anterior:** [Módulo 02: BI](../02-BI-Analitica/) · **Siguiente:** [Módulo 04: Preparación de datos](../04-Preparacion-Datos/)
