# Desafío 04 — El Cuaderno de Claves

| Campo | Valor |
|---|---|
| Evento | TRAMA CTF 2026 · *La última transmisión del Cerro Alegre* |
| Categoría | Crypto / reversing de cifrador casero (XOR + rotación + swap de nibbles) |
| Estado | ✅ Resuelto |
| Evidencia | `cuaderno-de-claves_publico.zip` (38.640 B, SHA256 `48DB0900...91E4C5F8`) |

## Flag

```
flag{ejemplo}
```

## Enunciado (resumen)

Un radioaficionado de Valparaíso («El Viejo») cifró su bitácora con un sistema propio
«imposible de romper». Se recuperan de una caja de lata: la tarjeta de radioaficionado
(QSL), el script del cifrador y la última anotación cifrada. Hay que reconstruir el
funcionamiento y descifrar la última anotación.

## Evidencia

| Archivo | Tamaño | Descripción |
|---|---|---|
| `cifrador.py` | 447 B | implementación del cifrador (17 líneas) |
| `bitacora.cifrada` | 411 B | hex, 410 caracteres → **205 bytes** de texto cifrado |
| `qsl_cerro_alegre.png` | 41.045 B | tarjeta QSL 960×600 (fuente de la clave) |

Hashes SHA256:

```
zip            48DB0900947961164354AD1648FBACAF909FE06E0FCA3178CE6A9D1291E4C5F8
bitacora        BAD0189E5D5F481E358690270262766CEF040BCC4D622915C0AE3BC9ED433963
cifrador.py     978539B68F5B9C71E8236C5F2AF40BC138E346BD2FD82A423F95C7C424727064
qsl_cerro.png   E0093C68A6467A15F92CB113B568C1757363F37BE57CCE8134AC88D5D80C7AB5
```

## Análisis del cifrador

`cifrador.py` completo:

```python
import sys
def _r(b,n): return ((b<<n)|(b>>(8-n)))&255          # rotación izquierda de n bits
def _s(b):   return ((b&15)<<4)|((b>>4)&15)          # swap de nibbles
def _e(p,k):
    o=bytearray()
    for i in range(len(p)):
        x=p[i]^k[i%len(k)]                            # 1) XOR con clave repetida
        x=_r(x,(i%7)+1)                               # 2) rotación variable 1..7
        x=_s(x)                                       # 3) nibble swap
        o.append(x)
    return bytes(o)
# ... argv: CLAVE entrada.txt salida.cifrada ; escribe _e(...).hex()
```

Tres capas, todas reversibles:

1. **XOR** con la clave repetida (`i % len(k)`).
2. **Rotación izquierda** de `(i % 7) + 1` bits → 1,2,3,4,5,6,7,1,2,…
3. **Swap de nibbles** (intercambia los 4 bits altos y bajos).

El cifrador usa solo operaciones biyectivas, así que el descifrado es exactamente el
proceso inverso y en orden inverso:

```
swap_nibbles  ->  rotación derecha (i%7)+1  ->  XOR con la clave
```

`_s` es su propia inversa (aplicarla dos veces devuelve el byte). Rotar a la derecha `n`
equivale a rotar a la izquierda `8-n`.

## Obtención de la clave

El enunciado destaca que se recuperó **la tarjeta de radioaficionado**: la clave está en la
QSL, no en el script (el script la recibe por argumento).

Contenido de la tarjeta:

```
RADIO CLUB CERRO ALEGRE — Valparaíso · Chile
CE2RCA                              73!
QSL — Confirmación de contacto
Date: 14-JUL-1987   UTC: 0312   Freq: 7.045 MHz   Mode: CW   RST: 599
Op: "El Viejo"
```

- **`CE2RCA`** → indicativo chileno (CE2 = zona 2, Región de Valparaíso). Es la clave.
- Coincidencias con el texto cifrado: la fecha `14-07-1987` y `03:12 UTC` y `7.045 MHz`
  aparecen en la bitácora descifrada → confirma la calibración del análisis.
- «con nuestra señal» en el texto plano = el indicativo del club.

## Solución (pasos reproducibles)

### 1. Descifrado directo con la clave de la QSL

```bash
python3 solucion/descifrar.py CE2RCA work/bitacora.cifrada
```

```python
def decrypt(c, k):
    o = bytearray()
    for i, byte in enumerate(c):
        x = _s(byte)                     # invierte el swap de nibbles
        x = _r(x, 8 - ((i % 7) + 1))     # rotación derecha = izquierda 8-n
        x = x ^ k[i % len(k)]            # invierte el XOR
        o.append(x)
    return bytes(o)
```

Salida:

```
[+] clave: CE2RCA | 205 bytes
------------------------------------------------------------
Bitacora 14-07-1987, 03:12 UTC. Capte de nuevo la emision fantasma en 7.045 MHz.
Nadie del club me cree. Dejo la prueba cifrada como siempre, con nuestra senal:
flag{ejemplo}
```

Comprobación de ida y vuelta: `encrypt(decrypt(c)) == c` → **True**.

### 2. Sin la tarjeta: ataque con crib (`solucion/ataque_crib.py`)

Deshaciendo rotación + swap **sin clave** queda un XOR de clave repetida puro:

```
u[i] = p[i] ^ k[i % L]
```

Con el crib `"Bitacora"` (la palabra que abre cualquier bitácora) se prueban longitudes
`L = 1..16`: se derivan los `L` primeros bytes de clave y se valida que el texto completo
sea imprimible.

```
[+] longitud de clave probable: 6
[+] clave derivada: 'CE2RCA'  (434532524341)
[+] texto plano (100% imprimible): ...
```

Ambas vías convergen en la misma clave.

### 3. Fuerza bruta (por si acaso)

Si no hubiera crib, el espacio de indicativos chilenos (`CE`/`CA` + dígito + 3 letras) es
diminuto (**~350k** combinaciones): bastaría validar cada candidato buscando `TRAMACTF{`
en el resultado. No fue necesario.

## Resultado

```
Bitacora 14-07-1987, 03:12 UTC. Capte de nuevo la emision fantasma en 7.045 MHz.
Nadie del club me cree. Dejo la prueba cifrada como siempre, con nuestra senal:
flag{ejemplo}
```

## Lecciones / notas

- **El cifrador es efímero, la clave es el secreto**: el script no oculta nada; toda la
  seguridad dependía de que nadie leyera la QSL. Seguridad por oscuridad, clásico.
- XOR + rotación + swap de nibbles **no aporta confidencialidad real**: las tres son
  biyecciones conocidas, y al deshacer las dos últimas el esquema degenera en un XOR de
  clave repetida, rompible con IC/crib en segundos.
- Los metadatos narrativos también son datos: fechas, hora UTC y frecuencia de la tarjeta
  se repiten en el texto descifrado → validación cruzada de que la clave es correcta.
- Errores típicos a evitar: invertir el orden de las capas (hay que deshacer de la última
  a la primera) y olvidar que `_r` con `8-n` es la rotación inversa.
- Detalle del reto: la flag está *dentro* del texto, no en un archivo aparte.

## Archivos de la carpeta

| Ruta | Contenido |
|---|---|
| `cuaderno-de-claves.zip` | evidencia original |
| `CONTEXTO.md` | este writeup |
| `flag.txt` | flag extraída |
| `solucion/descifrar.py` | implementación inversa + CLI por clave |
| `solucion/ataque_crib.py` | ataque de clave repetida sin conocer la clave |
| `solucion/salida.txt` | salida del descifrado |
| `work/cifrador.py` | cifrador original |
| `work/bitacora.cifrada` | texto cifrado (410 hex) |
| `work/qsl_cerro_alegre.png` | tarjeta QSL con el indicativo `CE2RCA` |
