# Ejercicios: Módulo 09, Proyecto final

---

## Parte 1: Autoevaluación (20 min, primera parte de la clase)

Cada equipo, con su repositorio:

1. Ejecuta el verificador y corrige lo que pueda en el momento:
   ```bash
   uv run python <ruta>/intro_analitica/09-Proyecto-Final/scripts/verificar_entrega.py .
   ```
2. **Prueba del clon limpio:** un integrante clona el repositorio en una carpeta nueva y sigue **solo** el README. ¿Llega hasta el modelo o el dashboard sin pedir ayuda? Anoten cada paso donde se trabó.
3. Califíquense con `rubrica.md`. ¿Dónde están más débiles?

---

## Parte 2: Salas de Zoom, revisión entre equipos y ensayo (70 min)

> **Objetivo:** recibir retroalimentación **antes** de la entrega y ensayar la presentación con público.
> **Viene de:** todo el hilo del proyecto (módulos 00 a 08).
> **Va a:** la entrega final

La profesora junta **dos equipos por sala** (A y B).

### Ronda 1: El equipo A presenta (25 min)

1. **A presenta** su ensayo de 10-12 minutos (con la demo). B cronometra.
2. **B evalúa** con la rúbrica y llena la tabla de retroalimentación (10 min):

| Criterio | Puntaje (1-5) | Lo mejor | Lo que mejoraría |
|---|---|---|---|
| Problema y KPIs | | | |
| Datos y limpieza | | | |
| EDA | | | |
| Modelo y evaluación | | | |
| Reproducibilidad | | | |
| Comunicación | | | |

3. **B hace 3 preguntas difíciles** (usen las de `guia_presentacion.md` como inspiración).

### Ronda 2: Intercambio (25 min)

El equipo B presenta y A evalúa.

### Ronda 3: Revisión cruzada del repositorio (20 min)

Cada equipo **clona el repositorio del otro** y trata de reproducirlo:

```bash
gh repo clone <usuario>/<repo-del-otro-equipo>
cd <repo>
uv sync
# seguir el README…
```

Abran un **issue** en el repositorio del otro equipo con:
- Qué funcionó
- Dónde se trabaron (comando exacto y error)
- Una sugerencia concreta

### Entregable

- [ ] Tabla de retroalimentación recibida, guardada en `docs/retroalimentacion.md`
- [ ] Issue abierto en el repositorio del otro equipo
- [ ] Lista de 3 mejoras priorizadas para la entrega final

---

## Plenaria de cierre del curso

1. ¿Qué fase de CRISP-DM les tomó más tiempo del que esperaban?
2. ¿Qué harían distinto si empezaran el proyecto hoy?
3. ¿Qué herramienta del curso (uv, Git, pipelines, FastAPI…) van a seguir usando en su trabajo?

**¡Felicitaciones por llegar hasta aquí!**
