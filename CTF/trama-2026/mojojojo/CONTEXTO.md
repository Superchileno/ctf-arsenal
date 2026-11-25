# Desafío 08 — Mojojojo (Las Calilas, la Mojojojo y el mensaje del micrófono)

| Campo | Valor |
|---|---|
| Categoría | MISC / audio simulado → cadena de codificaciones (hex → Base45 → Base64 → Ook! → Brainfuck) |
| Estado | ✅ Resuelto |
| Evidencia | `Mojojojos_v2.zip` (1.210 B, SHA256 `B9AD365E...77923BBD`) |
| Registro correcto | `transmision.txt` (23:10, emisión autorizada) |

## Flag

```
flag{ejemplo}
```

## Enunciado (resumen)

Radio comunitaria de San Felipe, programa sobre frases virales chilenas. Hay **dos
grabaciones**: una prueba de micrófono y la emisión definitiva de las 23:10. El sonidista
la llamó «puro ruido»; la animadora dijo que «con el volumen adecuado, sonaba como si un
mono estuviera escribiendo»; el técnico sentenció: «no es el micrófono, es que
**codificaron hasta el botón de apagar**». Hay que identificar el registro correcto y
recuperar el mensaje.

## Evidencia

| Archivo | Tamaño | Rol |
|---|---|---|
| `control_de_cabina.txt` | 202 B | hoja de horarios: decide qué archivo vale |
| `senal_2140_ensayo.txt` | 45 B | prueba de micrófono (señuelo) |
| `transmision.txt` | 111.780 B | **emisión autorizada** (la buena) |

Hashes (prefijo SHA256):

```
zip                  B9AD365E26878B92...
control_de_cabina    FE1D6B282D5AEDFB...
senal_2140_ensayo    F50263EEF4D948C6...
transmision          3829674E4BD34C82...
```

### 1. La hoja de control resuelve la ambigüedad

```
RADIO / SAN-FELIPE-2310
21:40 -> prueba de micrófono (archivo senal_2140_ensayo.txt)
23:10 -> emisión autorizada (archivo transmision.txt)
La prueba quedó guardada por error junto al registro final.
```

### 2. El señuelo, en claro

```
50 52 55 45 42 41 20 44 45 20 41 55 44 49 4f  ->  "PRUEBA DE AUDIO"
```

## Análisis

`transmision.txt` es **una sola línea de 37.260 bytes hex**. Al decodificar el hex se
obtiene ASCII con un patrón que engaña: 1.242 bloques de 30 caracteres, casi idénticos
entre sí:

```
:SA B7VT9BH8SIC$QE$B9+B7NEC5S6
:SA B76C9BH8SICOQE$B9+B7NEC$Y8
```

Toda la diferencia entre bloques está en 3 posiciones (pos 6-7 `VT`↔`76`, pos 15 `$`↔`O`,
pos 27-29 `5S6`↔`$Y8`), lo que simula una señal modulada: **1 bit por bloque**. Es una
trampa: extraer esos bits (aun con voto de mayoría entre los 3 grupos) da una onda
cuadrada sin información (39 transiciones, sin texto en ninguna codificación de 5/6/7/8
bits, ni ITA2, ni base64/base85 por bits).

La pista real es el **alfabeto**: los 25 símbolos que aparecen pertenecen exactamente al
alfabeto de **Base45** (RFC 9285):

```
0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ $%*+-./:
```

Ese alfabeto tiene 45 símbolos y el texto no contiene ninguno fuera de él (`set(txt) ⊆
Base45`). Y 37.260 es múltiplo de 3 → grupos de 3 caracteres = 2 bytes.

```
hex  ->  ASCII  ->  Base45  ->  Base64  ->  Ook!  ->  Brainfuck  ->  flag
```

- Base45 decodifica a **Base64**: `T29rLiBPb2su...` = `Ook. Ook. Ook. ...`
- El «mono escribiendo» es literal: **Ook!** es el lenguaje esotérico de orangutanes
  (variante de Brainfuck con tres tokens: `Ook.` `Ook!` `Ook?`).
- Cada par de tokens Ook = una instrucción de Brainfuck → 1.863 instrucciones que, al
  ejecutarse, imprimen la flag.

## Solución (pasos reproducibles)

### Script completo (guardado en `solucion/resolver.py`)

```python
ALF = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ $%*+-./:"          # Base45

def base45_decode(s):
    out = bytearray()
    for i in range(0, len(s) - 2, 3):
        v = ALF.index(s[i]) + ALF.index(s[i+1]) * 45 + ALF.index(s[i+2]) * 45 * 45
        out += bytes((v // 256, v % 256))
    return bytes(out)

capa1 = bytes(int(t, 16) for t in hex_tokens).decode()   # hex -> ASCII
capa2 = base45_decode(capa1).decode()                     # -> Base64
capa3 = base64.b64decode(capa2).decode()                  # -> Ook!
bf    = traducir_ook(capa3)                               # -> Brainfuck
flag  = ejecutar_bf(bf)                                   # -> flag
```

### Ejecución

```bash
$ python3 solucion/resolver.py
[1] hex -> ASCII          : 37260 caracteres
    muestra: ':SA B7VT9BH8SIC$QE$B9+B7NEC5S6:SA B7VT9BH8SIC$QE...'
[2] Base45 -> texto       : 24840 caracteres
    muestra: 'T29rLiBPb2suIE9vay4g...'   (parece Base64)
[3] Base64 -> código      : 18629 caracteres
    muestra: 'Ook. Ook. Ook. Ook. ...'   (Ook!: el 'mono escribiendo')
[4] Ook! -> Brainfuck     : 1863 instrucciones
[5] Brainfuck -> FLAG     : flag{ejemplo}
```

### Tabla de traducción Ook! → Brainfuck

| Ook | BF | Ook | BF |
|---|---|---|---|
| `Ook. Ook?` | `>` | `Ook! Ook.` | `.` |
| `Ook? Ook.` | `<` | `Ook. Ook!` | `,` |
| `Ook. Ook.` | `+` | `Ook! Ook?` | `[` |
| `Ook! Ook!` | `-` | `Ook? Ook!` | `]` |

### Atajo con herramientas

```bash
# 1) hex -> ascii
xxd -r -p work/transmision.txt work/capa1.txt     # (sin espacios: tr -d ' \n')
# 2) Base45 -> bytes            (pip install base45)
python3 -c "import base45;open('work/capa2.txt','wb').write(base45.b64decode(open('work/capa1.txt').read()))"
# 3) base64 -> Ook!
base64 -d work/capa2.txt > work/capa3.ook
# 4) Ook! -> BF y ejecutar con cualquier intérprete Ook
```

## Resultado

```
flag{ejemplo}
```

*«Las Mojojojos quieren dominar la feria»* — con `0` por `o`, `4` por `a`, `1` por `i` y
`3` por `e`.

## Lecciones / notas

- **Decodificar ≠ interpretar**: el hex es solo el contenedor. Lo que hay dentro es texto,
  y el texto está en **Base45**, no en Base64 (aunque lo parezca).
- La pista decisiva fue puramente **conjuntista**: `set(texto) ⊆ alfabeto Base45` y longitud
  múltiplo de 3. Cuando un archivo "raro" usa solo símbolos de un alfabeto conocido, es
  ese alfabeto.
- El «ruido» del enunciado era **texto válido**; el patrón de 1.242 bloques casi idénticos
  era el cebo: parecía una señal modulada (1 bit por bloque) y no lo era. Perdí tiempo
  intentando Morse/ITA2/FSK sobre esa estructura antes de mirar el alfabeto.
- «Un mono escribiendo» era literal: **Ook!** (orangután) → Brainfuck.
- «Codificaron hasta el botón de apagar»: la codificación está en **todas** las capas, no
  solo en la primera.
- Verificar la elección de archivo con `control_de_cabina.txt` evita analizar el señuelo
  (que solo decía `PRUEBA DE AUDIO`).

## Archivos de la carpeta

| Ruta | Contenido |
|---|---|
| `Mojojojos_v2.zip` | evidencia original |
| `CONTEXTO.md` | este writeup |
| `flag.txt` | flag final |
| `solucion/resolver.py` | pipeline completo hex→Base45→Base64→Ook!→Brainfuck |
| `solucion/salida.txt` | salida de la ejecución |
| `work/control_de_cabina.txt` | hoja de horarios |
| `work/senal_2140_ensayo.txt` | prueba de micrófono (señuelo) |
| `work/transmision.txt` | emisión autorizada (hex) |
| `work/capa3_ook.txt` | código Ook! extraído |
| `work/programa.bf` | programa Brainfuck traducido (1.863 instrucciones) |
