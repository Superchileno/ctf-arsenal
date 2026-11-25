# Formato de un objetivo documentado

Todo objetivo (reto, auditoría o pentest) debe poder reproducirse siguiendo su
`CONTEXTO.md` sin ayuda de quien lo resolvió.

## Nombre de carpeta

```
<MODO>\<evento-o-cliente>\<objetivo>\
```

- `MODO` ∈ `CTF`, `AUDITORIA`, `PENTESTING`.
- `evento-o-cliente` y `objetivo`: minúsculas, sin espacios ni tildes.
  Válido: `[a-z0-9._-]`. Ejemplo: `CTF\ctf-ejemplo-2026\reto-stego-01\`.
- Si la carpeta ya existe con otro nombre, se respeta.

## Contenido mínimo

| Elemento | Obligatorio | Se publica |
|---|---|---|
| `CONTEXTO.md` | sí | sí, saneado |
| `solucion\` | sí si hay código | sí |
| `work\` | no | no |
| `flags\` | solo CTF | no |
| `evidence\` | solo auditoría/pentest | no (versión redactada sí) |

## `CONTEXTO.md` — secciones

1. Enunciado (qué se pide)
2. Artefactos y hashes
3. Reconocimiento (comandos + salida)
4. Hipótesis descartadas
5. Solución paso a paso (reproducible)
6. Señuelos
7. Resultado (flag o hallazgo L1–L4)
8. Lecciones / técnica reutilizable
9. Registro de cambios

Plantillas: `plantillas\writeup.md`, `plantillas\informe-auditoria.md`.

## Criterio de calidad del writeup

- Otra persona, con el mismo artefacto y sin contexto previo, llega al mismo
  resultado siguiendo los pasos.
- Cada paso tiene **comando exacto** y **resultado esperado**.
- Los intentos fallidos quedan registrados con el motivo del fallo.
- No hay pasos del tipo «aquí se ve claramente que…» sin comando que lo demuestre.

## Publicación

1. Pasar el saneador: `python arsenal\sanitize.py --path <objetivo> --check`.
2. Corregir hallazgos (`--fix`) y revisar el diff a mano.
3. Copiar la versión publicable a `docs\writeups\<categoria>\<slug>.md`.
4. Agregar la fila al índice en `CONTEXTO.md`.
