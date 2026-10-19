# Project Charter: <nombre del proyecto>

> Documento de **una página** que alinea al equipo y a los *stakeholders*. Se actualiza en cada iteración de CRISP-DM.

**Equipo:** <nombres> · **Fecha:** <AAAA-MM-DD> · **Versión:** 0.1

## 1. Contexto y problema de negocio

<¿Qué pasa hoy? ¿A quién le duele? ¿Cuánto cuesta no resolverlo?>

## 2. Objetivo

| Nivel | Descripción |
|---|---|
| **Negocio** | <p.ej. "Reducir en 10 % la pérdida de clientes en 6 meses"> |
| **Ciencia de datos** | <p.ej. "Clasificar a los clientes según su probabilidad de churn en los próximos 30 días"> |
| **Tipo de problema** | Regresión Clasificación Segmentación Serie de tiempo Descriptivo (dashboard) |
| **Variable objetivo** | <columna> |

## 3. Criterios de éxito

| Tipo | Métrica | Umbral |
|---|---|---|
| Negocio (KPI) | <p.ej. tasa de recompra> | <+15 %> |
| Modelo | <p.ej. Recall de la clase churn> | <≥ 0.75> |
| *Baseline* a superar | <p.ej. "predecir siempre la clase mayoritaria"> | <valor> |

## 4. Datos

| Fuente | Descripción | Filas × columnas | Acceso |
|---|---|---|---|
| <enlace> | <qué es> | <N × M> | <público/descargado> |

**¿Qué representa una fila?** <...>

## 5. Alcance

- **Incluye:** <...>
- **No incluye:** <...>

## 6. Riesgos y supuestos

| Riesgo | Probabilidad | Impacto | Mitigación |
|---|---|---|---|
| <p.ej. muchos nulos en la variable clave> | Alta | Alto | <imputar con criterio / buscar otra fuente> |
| <p.ej. datos desbalanceados> | | | |
| <p.ej. fuga de información (*data leakage*)> | | | |

## 7. Plan (cronograma del curso)

| Semana | Fase CRISP-DM | Entregable | Responsable |
|---|---|---|---|
| 1 | Negocio + Datos | Charter + perfil inicial | |
| 2 | Preparación + EDA | Limpieza + EDA | |
| 3 | Modelado | Baseline + pipeline | |
| 4 | Evaluación + Despliegue | API + presentación | |

## 8. Stakeholders

| Persona/rol | Interés | Cómo se le comunica |
|---|---|---|
| <p.ej. gerente comercial> | <usar el modelo para campañas> | <dashboard mensual> |
