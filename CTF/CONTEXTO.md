# CONTEXTO — CTF (70 %)

Aquí vive cada reto resuelto. Un directorio por evento y, dentro, uno por reto.

## Estructura

```
CTF\
├─ CONTEXTO.md          ← este archivo
└─ <evento>\
   ├─ CONTEXTO.md       ← resumen del evento, reglas, plataforma
   └─ <reto>\
      ├─ CONTEXTO.md    ← writeup reproducible (obligatorio)
      ├─ solucion\      ← scripts de resolución
      ├─ work\          ← artefactos intermedios
      └─ flags\         ← solo local, nunca se publica
```

## Convención

- Evento y reto en minúsculas: `[a-z0-9._-]`.
- Si ya existe una carpeta con otro nombre, se respeta.
- Nada de archivos sueltos en la raíz de `CTF\`.

## Índice de retos

| Evento | Retos importados | Carpeta | Estado | Fecha |
|---|---|---|---|---|
| trama-2026 | 50 | [`trama-2026\`](trama-2026/) | Importado y saneado | 2026-11-24 |
| anci-2026 | 14 | [`anci-2026\`](anci-2026/) | Importado y saneado | 2026-11-24 |

Sub-evento dentro de `trama-2026`: `codigodemarte20261113\` (retos web del evento
Código de Marte, 10 carpetas).

Cada carpeta conserva su `CONTEXTO.md`/`README.md` y sus scripts en `solucion\`.
Los artefactos pesados y los directorios `work\`, `flags\` y `evidence\` **no** se
importaron: viven en el repositorio de origen.

## Plantilla y criterios

- Writeup: `plantillas\writeup.md` (`AGENTS.md` §2 define las 9 secciones).
- Triaje previo: `plantillas\triaje.md`.
- Categoría → skill: `docs\INDICE-SKILLS.md`.
- Técnica → comando: `docs\TECNICAS.md`.

## Reglas del modo CTF

1. Registrar **todos** los intentos, incluidos los fallidos y el motivo.
2. Dos intentos fallidos = cambiar de categoría, no de payload.
3. Marcar los señuelos: un resultado plausible que no era la respuesta también se
   documenta.
4. No publicar flags de competiciones en curso; al cerrar el evento, publicar el
   writeup saneado en `docs\writeups\`.
5. Cerrar el reto con `CONTEXTO.md` completo y entrada nueva en el historial.

## Historial

| Fecha | Evento | Reto | Resultado |
|---|---|---|---|
| 2026-11-24 | trama-2026 | 50 carpetas importadas | Saneadas (431 flags y 63 hosts retirados) |
| 2026-11-24 | anci-2026 | 14 carpetas importadas | Saneadas (25 flags y 98 hosts retirados) |
