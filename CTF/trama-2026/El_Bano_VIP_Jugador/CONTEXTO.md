# Desafío 06 — El baño VIP (El_Bano_VIP_Jugador)

| Campo | Valor |
|---|---|
| Evento | TRAMA CTF 2026 · Expediente CRIPTO-02: *Emergencia en la feria persa* |
| Categoría | Crypto / codificación (binario enmascarado de Morse + Base64) |
| Estado | ✅ Resuelto |
| Evidencia | `El_Bano_VIP_Jugador.zip` (318 B, SHA256 `2A4C36CD...C9928EF5`) |
| Ticket | `ticket_0347.txt` (3.456 B, 72 líneas, SHA256 `12755196...7E8EE3`) |

## Flag

```
flag{ejemplo}
```

*«El baño VIP tenía clave pero no tenía papel»* — coherente con el chiste del enunciado
(el papel higiénico era «un servicio adicional»).

## Enunciado (resumen)

La máquina de tickets del baño VIP de Don Lucho empieza a imprimir «hileras de rayas y
puntos» en vez de números de turno. Hay que examinar el último ticket e interpretar lo que
imprime: «la caja no está rota, el que sepa leer lo que imprime va a entender dónde quedó
el problema».

## Reconocimiento

```
$ unzip -l El_Bano_VIP_Jugador.zip
  3456  ticket_0347.txt
```

El ticket no tiene una sola letra: son **72 líneas** de tokens de 5 caracteres.

```
----- .---- ----- .---- ----- .---- .---- -----
----- .---- ----- ----- ----- .---- .---- -----
...
```

Análisis de frecuencia:

```
líneas: 72 | tokens: 576 | tokens únicos: 2
'-----'  318   (sin punto)
'.----'  258   (con un punto)
tokens por línea: 8 en las 72 líneas
```

## Análisis

Dos datos delatan el truco:

- **Solo existen 2 tokens distintos**, no el alfabeto Morse completo (que necesitaría `...`,
  `..---`, `.-`, etc.). Un Morse real tendría decenas de combinaciones.
- **8 tokens por línea × 72 líneas = 576 bits = 72 bytes exactos.**

Entonces cada token es un **bit**, no una letra Morse: la impresora dibuja «rayas y
puntos», pero el flujo es binario, 8 bits por línea (MSB primero).

Hay dos lecturas posibles y se comprueban ambas:

| Convención | Resultado |
|---|---|
| `'.' = 1`, `'-' = 0` | ASCII legible: `VFJBTUFDVEZ7...` |
| `'-' = 1`, `'.' = 0` | 72 × `0xFF` (basura) |

La primera gana, y el ASCII resultante **empieza con `VFJBTUFDVEZ7`**, que es Base64 de
`TRAMACTF{` (`VFJBTUFDVEZ7` → `TRAMACTF{`). Segunda capa: Base64.

## Solución (pasos reproducibles)

### Script (guardado en `solucion/decodificar_ticket.py`)

```python
bits = []
for linea in open("work/ticket_0347.txt", encoding="utf-8"):
    tokens = linea.split()
    if tokens:
        bits += ["1" if "." in t else "0" for t in tokens]      # '.' = 1

datos = bytes(int("".join(bits[i:i+8]), 2) for i in range(0, len(bits), 8))
print(datos.decode())                    # ASCII: VFJBTUFDVEZ7...
print(base64.b64decode(datos).decode())  # TRAMACTF{...}
```

```bash
$ python3 solucion/decodificar_ticket.py
[i] 576 bits = 72 bytes
[i] ASCII: VFJBTUFDVEZ7RWxfQjRuMF9WMVBfVDNuMTRfQ2w0djNfUDNyMF9OMF9UM24xNF9QNHAzbH0=
[i] Base64 decodificado: flag{ejemplo}
[+] FLAG: flag{ejemplo}
```

### Todo en una línea (bash)

```bash
# '.' -> 1, quitar espacios/saltos, agrupar en bytes, pasar a Base64 y decodificar
tr -d ' \n' < work/ticket_0347.txt | sed 's/-----/0/g; s/\.----/1/g' \
  | fold -w8 | while read b; do printf "\\x$(printf '%02x' $((2#$b)))"; done \
  | base64 -d
```

## Cadena de capas

```
rayas/puntos  ->  bits (8 por línea, MSB primero)  ->  ASCII Base64
              ->  Base64  ->  flag
```

```
VFJBTUFDVEZ7RWxfQjRuMF9WMVBfVDNuMTRfQ2w0djNfUDNyMF9OMF9UM24xNF9QNHAzbH0=
   |  base64 -d
flag{ejemplo}
```

## Lecciones / notas

- **No todo lo que parece Morse lo es**: si el repertorio de símbolos es diminuto y las
  cuentas cuadran con bytes (576 bits = 72 B), es binario.
- El indicio decisivo es aritmético: **8 tokens por línea**. Un alfabeto de 2 símbolos con
  8 posiciones = 1 byte.
- Probar ambas polaridades es gratis y evita callejones: `'.'=1` da texto, `'-'=1` da
  `0xFF` repetidos.
- Codificación en capas es lo habitual en CTFs: binario → ASCII/Base64 → flag. Siempre
  mirar si el texto intermedio parece Base64/hex/URL-encode.
- El `=` final del Base64 y el prefijo `VFJBTUFDVEZ7` (que siempre decodifica a `TRAMACTF{`)
  son la firma inconfundible.
- «Once minutos» del relato y `ticket_0347` son ruido narrativo: no participan del
  descifrado.

## Archivos de la carpeta

| Ruta | Contenido |
|---|---|
| `El_Bano_VIP_Jugador.zip` | evidencia original |
| `CONTEXTO.md` | este writeup |
| `flag.txt` | flag extraída |
| `solucion/decodificar_ticket.py` | bits → bytes → Base64 → flag, con validación |
| `solucion/salida.txt` | salida de la ejecución |
| `work/ticket_0347.txt` | ticket recuperado (576 tokens) |
