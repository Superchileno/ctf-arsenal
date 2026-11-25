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

| Evento | Reto | Categoría | Estado | Fecha |
|---|---|---|---|---|
| — | *(sin retos todavía)* | — | — | — |

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
| — | — | — | — |
