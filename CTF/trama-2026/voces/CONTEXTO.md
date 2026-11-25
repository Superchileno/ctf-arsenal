# Desafío 21 — El Coro de Treinta Voces

| Campo | Valor |
|---|---|
| Categoría | forense de audio / decodificación de tonos duales (nibbles) |
| Dificultad | media |
| Puntos | — |
| Estado | ✅ resuelto |
| Flag | `flag{ejemplo}` |

## Enunciado

> **El Coro de Treinta Voces — La audición que salió en otra frecuencia** — […] Durante el ensayo general,
> el sistema de grabación se desconfiguró. Las voces humanas desaparecieron de la mezcla y quedaron unas
> notas de calibración que sonaban a teléfono antiguo pidiendo auxilio. […] ocho pistas correspondían a
> pruebas y el resto estaba mezclado en un orden que solo entendía la planilla del estudio. […]
>
> «No escuches todas las voces como si fueran una sola. Cada toma tiene dos tonos, y cada tono cuenta una
> mitad de la historia».
>
> Tu misión: examina la grabación, usa la documentación técnica para interpretar las tomas válidas y
> reconstruye la confesión que el coro nunca llegó a cantar.

## Reconocimiento

`Coro_Treinta_Voces.zip` (143.030 B, SHA256 `fc403ff3...b9e6223`) contiene:

| Archivo | Tamaño | Notas |
|---|---|---|
| `LEEME.txt` | 113 B | Apunta al enunciado de CTFd |
| `coro_30_tomas.wav` | 168.044 B | 30 tomas concatenadas, 10,5 s |
| `hoja_del_afinador.txt` | 819 B | Manual técnico de los tonos |
| `planilla_de_mezcla.csv` | 1.234 B | Clase y orden editorial de cada toma |

Audio: `PCM 16 bit, mono, 8000 Hz, 10,50 s` → 30 tomas de `0,35 s`.

### Manual del afinador (extracto)

- Cada toma: **0,30 s de nota + 0,05 s de silencio**.
- Cada nota lleva **dos tonos portadores** (grave y agudo).
- Banco **GRAVE**: `520 + 40·k` Hz (520…1120) → **dígito hexadecimal ALTO**.
- Banco **AGUDO**: `1400 + 40·k` Hz (1400…2000) → **dígito hexadecimal BAJO**.
- `byte = (alto << 4) | bajo` → un carácter ASCII por toma.
- Solo entran las tomas **MAESTRAS**, en el orden de la planilla.
- Las tomas de **CALIBRACIÓN** son señuelos ("pueden sonar tan convincentes como las maestras").

### Planilla

- **22 MAESTRAS** (con `orden` 01…22).
- **8 CALIBRACIÓN**: 03, 06, 12, 13, 15, 23, 25, 29 → se descartan.

## Análisis

Para cada toma `n` (1..30):

1. Recortar la nota: muestras de `0,05 s` a `0,28 s` dentro de la toma (evita el ataque y la liberación
   del tono y el silencio posterior).
2. Ventana de Hann y FFT de 32.768 puntos (resolución ~0,24 Hz, muy por debajo de los 40 Hz entre tonos).
3. Buscar el pico en `480–1220 Hz` (grave) y en `1320–2080 Hz` (agudo).
4. Índice `k = round((f − base) / 40)`, acotado a 0..15.
5. `byte = (k_grave << 4) | k_agudo`; carácter ASCII.

Ejemplo (toma 01): grave 760 Hz → `k=6`; agudo 1440 Hz → `k=1`; `0x61` = `a`.

### Resultado de las MAESTRAS en orden editorial

| orden | toma | byte | char | | orden | toma | byte | char |
|---|---|---|---|---|---|---|---|---|
| 01 | 27 | 0x6C | l | | 12 | 20 | 0x6E | n |
| 02 | 01 | 0x61 | a | | 13 | 22 | 0x5F | _ |
| 03 | 10 | 0x5F | _ | | 14 | 30 | 0x76 | v |
| 04 | 26 | 0x63 | c | | 15 | 21 | 0x65 | e |
| 05 | 18 | 0x6F | o | | 16 | 19 | 0x72 | r |
| 06 | 11 | 0x6E | n | | 17 | 08 | 0x64 | d |
| 07 | 14 | 0x66 | f | | 18 | 05 | 0x61 | a |
| 08 | 04 | 0x65 | e | | 19 | 28 | 0x64 | d |
| 09 | 09 | 0x73 | s | | 20 | 02 | 0x65 | e |
| 10 | 17 | 0x69 | i | | 21 | 24 | 0x72 | r |
| 11 | 16 | 0x6F | o | | 22 | 07 | 0x61 | a |

Bytes: `6c615f636f6e666573696f6e5f766572646164657261` → **`la_confesion_verdadera`** (22 caracteres).

El manual indica que el encabezado y las llaves los aporta el formato oficial de TRAMA CTF, por lo que la
flag es `flag{ejemplo}`.

### Señuelos

Las 8 tomas de CALIBRACIÓN decodifican a caracteres plausibles (`_`, `1`, `m`, `_`, `p`, `u`, `a`, `u`),
de modo que si se incluyen en la mezcla el texto se corrompe pero sigue pareciendo "casi" una frase.

## Solución (pasos reproducibles)

```bash
unzip Coro_Treinta_Voces.zip -d work/

python3 solucion/decodificar_coro.py work/coro_30_tomas.wav work/planilla_de_mezcla.csv
# ...
# orden: 01 02 ... 22
# bytes: 6c615f636f6e666573696f6e5f766572646164657261
# texto: 'la_confesion_verdadera'
```

Salida completa por toma en `work/salida_decodificada.txt`.

## Flag

```
flag{ejemplo}
```

## Evidencia y artefactos

| Ruta | Contenido |
|---|---|
| `Coro_Treinta_Voces.zip` | Evidencia entregada (143.030 B) |
| `work/coro_30_tomas.wav` | Grabación de las 30 tomas |
| `work/hoja_del_afinador.txt` | Manual de decodificación |
| `work/planilla_de_mezcla.csv` | Clase (MAESTRA/CALIBRACIÓN) y orden editorial |
| `work/salida_decodificada.txt` | Volcado completo: frecuencias, nibbles, bytes y texto |
| `solucion/decodificar_coro.py` | Decodificador (FFT por toma + reordenamiento por planilla) |
| `flag.txt` | Flag del reto |

## Lecciones / notas

- **Dos tonos = dos nibbles**: el byte se forma con el banco grave como nibble alto y el agudo como bajo;
  es una variante "DTMF extendida" con 16+16 frecuencias separadas 40 Hz.
- La resolución espectral no es un problema: con una ventana de ~0,23 s y FFT grande se distingue
  perfectamente cada tono del banco.
- **La planilla es parte del reto**: sin el orden editorial los bytes correctos forman un anagrama; sin
  descartar las 8 calibraciones el texto se corrompe con señuelos verosímiles.
- El enunciado ("cada tono cuenta una mitad de la historia") es literal: alto y bajo aportan medio byte.

## Backups

| Archivo | Backup |
|---|---|
| `ctf/CONTEXTO_CTF.md` (índice) | `ctf/backups/CONTEXTO_CTF.md.20261023-190245` |
