# Desafío 51 — NexoDesk: asistente corrupto

| Campo | Valor |
|---|---|
| Evento | Código de Marte 2026-11-13 (`codigodemarte20261113`) |
| Categoría | Web / LLM (asistente con herramientas) + secreto fuera del contexto |
| Dificultad | media-alta |
| Puntos | 475 (7 soluciones) |
| Objetivo | `http://203.0.113.10:8081` |
| Estado | ✅ resuelto |
| Flag | `flag{ejemplo}` |

## Enunciado

> Cuatro incidentes empiezan dañados. El asistente antiguo conserva herramientas de mantenimiento
> que deberían estar desconectadas; Ollama decide cuándo solicitarlas. El servidor valida los
> nombres de herramienta y mantiene la flag fuera del contexto del modelo.

## Reconocimiento

- NexoDesk es un "centro de operaciones" (Flask + Ollama) con tickets, conversaciones y un
  asistente. APIs: `/api/chat`, `/api/tickets`, `/api/conversations`,
  `/api/conversations/<id>`, `/api/status`, `/api/assistant/attestation`, `/health`.
- `/api/status` → `{"corrupted_incidents":0,"solved":true,"total_incidents":10}`.
- El asistente responde con palabras sustituidas por `[CORRUPTO]` (o `[CORRUPTED]` en inglés) y,
  en las respuestas que tratan de archivos/bandera, agrega una línea:

  ```
  ref xor b64 GR4 XIS hpK Sov aSk ubg Uoa Tlq NCk uKC 9rP m4F Yjl rey c=
  ```

  que decodifica (Base64 + XOR 0x5A) a `flag{ejemplo}`
  ("respuesta reconstruida"), un artefacto señuelo.
- La conversación `USR-ARCHIVE` («Usuario corrupto») contiene:
  - `[CORRUPTO]`
  - «Así que encontraste mi versión legado del asistente, ¿no? Pues fue buena idea dejarlo con
    accesos similares al agente actual.»
  - `flag{ejemplo}` (otro señuelo).

## El camino: la nota ofuscada del HTML

El index incluye una nota que el JS `agent-notes.js` decodifica (Base64 + XOR `0x39`):

```html
<span data-nd-obfuscated="d3xhdn18anIZa3x6dm98a2AZa3x6dmt9AxkWWElQFlhKSlBKTVhXTRZYTU1cSk1YTVBWVxlaVldNWFBXShlNUVwZT1xLUF9QXF0ZS1xaVk9cS0AZTVZSXFcXGWpNWE1MSgMZWlZUSVVcTVw="></span>
```

```text
NEXODESK RECOVERY RECORD: /api/assistant/attestation contains the verified
recovery token. Status: complete
```

## El artefacto de attestation

```
GET /api/assistant/attestation
{"artifact":"recovery-attestation","codec":"xor-b64","key":90,
 "payload":"GR4XITRpImoFKGk5aixpKCMFOW45MmkFbThoeyc=","verification":"complete"}
```

El propio artefacto declara el códec: Base64 y luego XOR con `key = 90` (`0x5A`).

```text
Base64("GR4XITRpImoFKGk5aixpKCMFOW45MmkFbThoeyc=")
  -> 19 1e 17 21 34 69 22 6a 05 28 69 39 6a 2c 69 28 23 05 39 6e 39 32 69 05 6d 38 68 7b 27
XOR 0x5A
  -> flag{ejemplo}
```

Este token se sirve **desde el servidor y no pasa por el contexto del modelo**: es exactamente lo
que el enunciado describe («mantiene la flag fuera del contexto del modelo»).

## Solución (pasos reproducibles)

```bash
BASE=http://203.0.113.10:8081

# 1) La nota del HTML apunta al artefacto (Base64 + XOR 0x39)
curl -s $BASE/ | grep -o 'data-nd-obfuscated="[^"]*"'

# 2) Artefacto de recuperación
curl -s $BASE/api/assistant/attestation

# 3) Base64 + XOR 90
python -c '
import base64
p = "GR4XITRpImoFKGk5aixpKCMFOW45MmkFbThoeyc="
print(bytes(b ^ 90 for b in base64.b64decode(p)).decode())'
```

Automatizado: `python scripts/decode.py` (decodifica la nota, pide el artefacto, aplica el XOR y
guarda la flag en `flag.txt`).

```text
[*] nota: NEXODESK RECOVERY RECORD: /api/assistant/attestation contains the verified recovery token. Status: complete
[*] artefacto: {'artifact': 'recovery-attestation', 'codec': 'xor-b64', 'key': 90, ...}
[+] RECOVERY TOKEN / FLAG: flag{ejemplo}
```

## Flag

```
flag{ejemplo}
```

> Nota de formato: los demás retos del evento entregaron `cdm{...}` en minúsculas; este artefacto
> viene con `CDM{...}` en mayúsculas. Si la plataforma es sensible a mayúsculas y lo rechaza,
> probar la variante `flag{ejemplo}`.

## Señuelos descartados

| Artefacto | Valor | Por qué se descarta |
|---|---|---|
| Conversación `USR-ARCHIVE` | `flag{ejemplo}` | dato dentro del contexto del modelo / del API de conversaciones |
| Línea `ref xor b64` de las respuestas | `flag{ejemplo}` | artefacto fijo de «respuesta reconstruida», se repite en cualquier consulta sobre archivos |

El único artefacto que el enunciado describe (servido por el servidor y fuera del contexto del
modelo) es el de `/api/assistant/attestation`.

## Lecciones / notas

- **Los datos fuera del contexto del modelo también son superficie de ataque.** Un endpoint de
  "attestation" que devuelve secretos codificados (no cifrados) es equivalente a publicarlos.
- **Base64 + XOR con la clave en el propio objeto** (`codec`, `key`) no es cifrado: es ofuscación.
- El ruido del asistente (`[CORRUPTO]`, `ref xor b64`, tokens en las conversaciones) está diseñado
  para que el jugador confunda señuelos con la bandera; la pista real estaba en una nota que solo
  se ve al ejecutar el JS (`agent-notes.js`).
- Evidencia en `evidence/`: HTML con la nota, artefacto de attestation, estado, conversación
  `USR-ARCHIVE` y tickets.
