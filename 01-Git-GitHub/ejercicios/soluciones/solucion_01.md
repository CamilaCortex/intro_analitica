# Soluciones: Módulo 01, Ejercicio 5 (Conventional Commits)

| Mensaje original | Mensaje corregido | Por qué |
|---|---|---|
| `cambios` (se agregó un notebook de limpieza) | `feat: agrega notebook de limpieza de datos` | Es algo nuevo, y el mensaje dice **qué** cambió |
| `arreglé el error` (la ruta al CSV estaba mal) | `fix: corrige la ruta del archivo CSV` | Es una corrección; se escribe en presente y dice cuál error |
| `README` (se agregó cómo instalar el proyecto) | `docs: agrega instrucciones de instalación al README` | Es documentación |
| `ya quedó la gráfica!!!` (nueva gráfica de ventas por mes) | `feat: agrega gráfica de ventas por mes` | Es algo nuevo; sin signos de exclamación ni lenguaje informal |
| `instalé seaborn` | `chore: agrega seaborn como dependencia` | Es mantenimiento del proyecto (dependencias) |
| `Organicé el código` (se pasó una función del notebook a `src/`) | `refactor: mueve la función de limpieza a src/limpieza.py` | Cambia la organización, no el comportamiento |

## Reglas para recordar

1. **Formato:** `tipo: descripción`, o `tipo(scope): descripción`.
2. **Presente e impersonal:** "agrega", "corrige", "mueve" (no "agregué" ni "agregando").
3. **Minúscula al inicio y sin punto final.**
4. **Específico:** quien lea el historial debe entender el cambio sin abrir el archivo.
5. **Un commit, un cambio:** si el mensaje necesita la palabra "y", probablemente son dos commits.
