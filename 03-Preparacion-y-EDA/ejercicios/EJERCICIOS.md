# Ejercicios: Módulo 03, Preparación de datos y EDA

> **Roten los roles:** quien fue copiloto ayer ahora es piloto. Recuerden: **solo el piloto edita el notebook**.

| Clase | Secciones del notebook del equipo |
|---|---|
| 26 de octubre | 0. Configuración · 1. El problema · 2. Los datos |
| **27 de octubre (hoy)** | **3. Limpieza · 4. EDA** |
| 28 de octubre | 5. Modelo |
| 11 de noviembre | 6. Conclusiones |



---

## Parte 1: Salas de Zoom, limpieza y EDA del equipo (45 min)

> **Objetivo:** resolver los problemas de calidad que encontraron ayer y salir con 3 hallazgos con evidencia.
> **Viene de:** la sección 2 del notebook (problemas de calidad e hipótesis).
> **Va a:** la clase del 28 de octubre, donde los hallazgos deciden qué variables entran al modelo.

### Paso 0: Actualizar (2 min)

Todos, en el repositorio del equipo:

```bash
git pull
```

El piloto abre `notebooks/proyecto_equipo.ipynb` y ejecuta todo hasta el final de la sección 2 (*Run All Above* o celda por celda).

### Paso 1: Limpieza (sección 3, 18 min)

1. Retomen la tabla de **3 problemas de calidad** de la sección 2.4.
2. Para cada problema, decidan **entre los tres** qué hacer, usando la tabla "¿qué hago con un nulo?" de la sección 3 del notebook. Escriban el código en las celdas `COMPLETAR: decisión 1, 2 y 3`.
3. Ejecuten la celda de comprobación: ¿quedan nulos? Los que queden en las variables del modelo se rellenan automáticamente en la sección 5; no tienen que llegar a cero.
4. Llenen el **registro de decisiones**: problema, decisión y **por qué**.
5. Ejecuten la celda que guarda `data/processed/datos_limpios.csv`.

> **Si su dataset no tiene nulos**, busquen otros problemas: duplicados, valores imposibles (edades negativas, precios en cero), textos escritos de varias formas o números leídos como texto.

### Paso 2: EDA (sección 4, 18 min)

1. **4.1:** ejecuten la celda de relaciones con el objetivo. ¿Qué variables aparecen más arriba? ¿Coinciden con sus hipótesis?
2. **4.2:** elijan la variable numérica más prometedora, escriban su nombre en `VARIABLE_NUMERICA` y ejecuten.
3. **4.3:** elijan una variable categórica, escriban su nombre en `VARIABLE_CATEGORICA` y ejecuten.
4. **4.4:** ajusten la celda del KPI para calcular uno de los KPIs de la sección 1.
5. **4.5:** llenen la tabla de **3 hallazgos**. Para cada uno, indiquen si confirma o rechaza una hipótesis de la sección 2.4.

> **Una hipótesis rechazada también es un hallazgo.** "Creíamos que el barrio no influía, pero a igual calidad suma hasta un 46 % al precio" es exactamente lo que se busca.

### Paso 3: Subir los cambios (7 min)

Antes de subir, ejecuten *Restart Kernel and Run All*.

**Piloto:**

```bash
git pull
git add notebooks/proyecto_equipo.ipynb
git commit -m "feat: agrega limpieza y EDA con tres hallazgos"
git push
```

**Relator** (en su computador, después de que el piloto suba): agrega al README del equipo una sección **Hallazgos principales** con los 3 hallazgos en una línea cada uno y marca el avance del módulo 03.

```bash
git pull
git add README.md
git commit -m "docs: agrega hallazgos del EDA al README"
git push
```

**Copiloto:** hace `git pull` y ejecuta el notebook completo en su computador para comprobar que funciona.

### Entregable

- [ ] Sección 3 con al menos 3 decisiones de limpieza y su registro justificado
- [ ] Sección 4 con las gráficas y la tabla de 3 hallazgos
- [ ] README del equipo con los hallazgos principales
- [ ] El notebook corre completo (*Restart Kernel and Run All*) en el computador del copiloto

---

## Plenaria (10 min)

Cada relator comparte **un hallazgo** en 1 minuto, con su evidencia. El grupo responde: ¿es un hallazgo o solo una descripción de la gráfica?

## Para la próxima clase

Piensen qué error sería aceptable para su negocio: ¿equivocarse en un 10 %, en un 20 %? ¿Qué es peor, una falsa alarma o un caso que se escapa? Mañana eligen la métrica del modelo.
