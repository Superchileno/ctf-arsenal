# CONTEXTO — AUDITORÍA (15 %)

Trabajo de revisión defensiva/ofensiva con entregable formal: configuraciones,
cumplimiento, revisión de código, análisis de arquitectura.

## Estructura

```
AUDITORIA\
├─ CONTEXTO.md
└─ <cliente>\
   ├─ CONTEXTO.md        ← resumen del engagement
   ├─ authorization.md   ← obligatorio antes de cualquier acción activa
   ├─ scope.txt          ← obligatorio
   └─ <objetivo>\
      ├─ CONTEXTO.md     ← informe del objetivo (plantilla informe-auditoria.md)
      ├─ solucion\       ← scripts y configuraciones usadas
      ├─ evidence\       ← evidencia redactada
      └─ work\           ← intermedios
```

## Requisito de arranque

Sin `authorization.md` completo **y** `scope.txt` con hosts en alcance, el agente
no ejecuta acciones activas. Puede leer documentación y planificar.

`authorization.md` debe incluir: cliente, objetivo, tipo, modalidad, fechas,
ventana horaria, autorizante con cargo, documento de respaldo y declaración de
condiciones.

## Índice de engagements

| Cliente | Objetivo | Tipo | Estado | Fecha |
|---|---|---|---|---|
| — | *(sin engagements todavía)* | — | — | — |

## Entregables

1. `CONTEXTO.md` con las 9 secciones de `plantillas\informe-auditoria.md`.
2. Hallazgos con L1–L4, CVSS 3.1 y CWE cuando corresponda a L3/L4.
3. Evidencia redactada (credenciales → últimos 6 caracteres).
4. Recomendaciones priorizadas 30/60/90 días.

## Reglas

- Lenguaje preciso: «no se encontraron problemas explotables en X» ≠ «X es seguro».
- Sin cambios de configuración en producción sin aprobación del cliente.
- Cerrar con backup y entrada en el historial.

## Historial

| Fecha | Cliente | Objetivo | Resultado |
|---|---|---|---|
| — | — | — | — |
