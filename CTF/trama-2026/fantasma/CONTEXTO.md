# Registro Fantasma — Campeonato Nocturno del Completo al Vapor

| Campo | Valor |
|---|---|
| Categoría | Forense — correlación de logs + base64 + deflate |
| Evidencia | `Registro_Fantasma.zip` (5 173 B): `access.log`, `proxy_trace.csv`, `parte_turno.txt`, `LEEME.txt` |
| Estado | ✅ Resuelto |
| Flag | `flag{ejemplo}` |

## Enunciado (resumen)

Campeonato nocturno del completo al vapor en Talca. A las 01:46 la **CAJA-07**
informa un envío fuera de horario vinculado a la mesa de recuento; a las 01:49 el
marcador queda congelado. Se recuperaron dos capas de log desincronizadas y hay que
reconstruir qué se transmitió.

## Pistas del `parte_turno.txt`

- El `access.log` es del **backend, detrás de un proxy**: la IP no identifica la caja.
- El **proxy** guarda el resultado real del reenvío: hay `REJECT`, `REPLAY` y `OK`.
- Los logs se volcaron **por lotes**: el orden de aparición y la hora de escritura no
  reflejan la secuencia original.
- El protocolo de telemetría **comprime el bloque y lo convierte a texto** para la URL.

## Las dos capas

```
access.log        GET /telemetry/sync?rid=RQ-XXXX&p=<bloque>  "vapor-sync/3.2"
proxy_trace.csv   request_id, terminal, flow, seq, proxy_result, backend_status, content_encoding
```

Unión por `request_id` (`rid`), orden por **(flow, seq)**, y solo las peticiones que el
proxy marcó `OK` (las demás son reintentos rechazados, 403/409/429).

## El detalle clave del `p`

Cada bloque **no** se descomprime por separado: son **pedazos del texto** de un único
flujo deflate codificado en base64url. Por eso hay piezas de 5 caracteres (no múltiplos
de 4 y por tanto base64 inválido por sí solas). Hay que:

```
p_total = concatenar(p en orden flow+seq)  ->  base64url decode  ->  zlib/deflate
```

## Reconstrucción por flujo

| Flujo | Caja | Filas | Mensaje |
|---|---|---|---|
| **FV-9D6** | **CAJA-07** | 19 (11 OK, 3 REJECT, 5 REPLAY) | ✅ **`flag{ejemplo}`** |
| FA-8E3 | CAJA-09 | 10 OK | `flag{ejemplo}` (señuelo) |
| FW-7B1 | CAJA-02 | 10 OK | `flag{ejemplo}` (señuelo) |
| FE-2C8 | CAJA-07 | 12 REJECT (403) | `PREPRODUCCION: ensayo de telemetria descartado` (descartado) |

**Por qué FV-9D6 es el bueno:** el parte de turno sitúa el incidente en la **CAJA-07**.
Esa caja tiene dos flujos: `FE-2C8` (todo rechazado por el proxy → ensayo de
preproducción) y `FV-9D6`, que es el único **aceptado** y además el único que exige
descartar los `REPLAY`/`REJECT` duplicados (si se meten todas las filas, el deflate
revienta). Los otros dos flujos son de cajas distintas: CAJA-09 («informe de caja
equivocado», coherente con la nota de que la IP no identifica la caja) y CAJA-02
(«premio de prueba no válido»).

## Solución

```bash
python3 solucion/reconstruir.py     # reconstruye los 4 flujos y marca la flag
python3 solucion/analizar.py        # resumen por flujo + rutas del access.log
python3 solucion/correlacion.py     # rid -> caja/hora/IP, ordenado por seq
```

Núcleo del solver:

```python
for f in proxy_trace:                       # solo OK
    if f.proxy_result != "OK": continue
    piezas[(f.flow, int(f.seq))] = eventos[f.request_id]
for flow in flows:
    b64 = "".join(piezas[k] for k in sorted(k for k in piezas if k[0]==flow))
    texto = zlib.decompress(base64.urlsafe_b64decode(b64 + "=" * (-len(b64)%4)), -15)
```

## Flag

```
flag{ejemplo}
```

## Lecciones

- Correlacionar **dos capas** (proxy + backend) es imprescindible: el `access.log`
  solo tiene la petición que llegó, no la que el proxy rechazó.
- El orden de las líneas en el archivo es ruido; manda el campo `seq` del proxy.
- Los `REPLAY`/`REJECT` no se descartan por “ruido”: si se incluyen, el flujo
  comprimido se corrompe — son la prueba de que hubo reintentos.
- Un bloque base64 de longitud no múltiplo de 4 es la señal de que el base64 está
  **partido en trozos** y hay que unirlo antes de decodificar.

## Archivos de la carpeta

| Ruta | Contenido |
|---|---|
| `Registro_Fantasma.zip` | evidencia original |
| `flag.txt` | flag final |
| `CONTEXTO.md` | este writeup |
| `solucion/reconstruir.py` | solver (une rid + proxy + base64url + deflate) |
| `solucion/analizar.py` | resumen por flujo, resultados del proxy y rutas |
| `solucion/correlacion.py` | cruce rid → caja / hora / IP por `seq` |
| `work/` | los cuatro archivos extraídos |
