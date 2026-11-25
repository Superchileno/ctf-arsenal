# El Susurro del Conde — TRAMA CTF 2026

| Campo | Valor |
|---|---|
| Categoría | Forense de audio / esteganografía (espectrograma + LSB) |
| Dificultad | Media |
| Estado | ✅ resuelto |
| Flag | `flag{ejemplo}` |
| Fecha | 2026-10-24 |

## Enunciado

Tras el incidente de la foto chismosa, el Conde Ciber-Drácula ordena a la Hermandad de
las Sombras grabar un audio con el siguiente movimiento del clan. El informante
intercepta el `.wav` y deja una nota: «El Conde esconde dos secretos en el mismo sonido.
Uno para los ojos, otro para los oídos. Y para abrir el segundo, necesitarás la llave
del primero».

## Evidencia

| Archivo | Rol |
|---|---|
| `ChismeAudio.wav` | PCM 16-bit mono, 44.100 Hz, 320.000 muestras, 7,256 s |
| Tamaño | 640.044 B (RIFF + `fmt ` 16 B + `data` 640.000 B, sin chunks extra) |
| SHA-256 | `7CCD2A904E21D3AF1C09F3C31CF526CFD6700D99246559B0BE91551A77896011` |

## Secreto 1 — «para los ojos»: la llave

El audio es un peine armónico con F0 = **110,25 Hz** (= 44100/400). En la banda
**2,4–4,1 kHz** hay un texto dibujado mediante modulación de amplitud. Render 1:1 en
`evidencias/band_1to1.png`:

```
KEY: SweetBlood
```

La palabra base es **SweetBlood**. El render no distingue con claridad `o` de `0`;
la capa 2 confirma que la llave real es la variante leet **`SweetBl00d`** (dos ceros).

## Secreto 2 — «para los oídos»: el blob LSB

El bit 0 de cada muestra PCM (empaquetado MSB-first) no es ruido: al inicio del flujo
hay una cadena Base64 de 44 caracteres, seguida de un `0x00` y del resto del audio:

```
ByUkKDUBOHZLNyNECRAaKQVeVzsWGVYJKw8JREJULg==
```

Decodificada son **31 bytes**:

```
07252428350138764b37234409101a29055e573b161956092b0f094442542e
```

Al hacer **XOR con la llave `SweetBl00d` repetida** aparece la flag:

```
flag{ejemplo}
```

Comprobación del prefijo: con `SweetBl00d` los primeros bytes son `TRAMACTF{`;
con `SweetBlood` el XOR se rompe justo en la `F` (posición 7), porque el octavo
carácter de la llave debe ser `0` (0x30), no `o` (0x6f). Con `SweetBL00D`,
`Sweetbl00d` o `sweetbl00d` también se rompe la mayúscula/minúscula.

## Solución reproducible

```bash
cd ctf/susurro
python3 solucion/descifrar_susurro.py
```

Salida:

```
[1] LSB empaquetado: 40000 bytes; inicio: b'ByUkKDUBOHZLNyNECRAaKQVeVzsWGVYJKw8JREJULg==\x00...'
[2] Blob Base64 (44 chars): ByUkKDUBOHZLNyNECRAaKQVeVzsWGVYJKw8JREJULg==
[3] Ciphertext (31 B): 07252428350138764b37234409101a29055e573b161956092b0f094442542e
[4] XOR con 'SweetBl00d': flag{ejemplo}

FLAG: flag{ejemplo}
```

## Zonas descartadas

- Contenedor: no hay chunks RIFF extra, datos anexados, `DSCF` (DeepSound),
  `Salted__`, `PK`, `7z`, etc.
- `steghide` (28 passphrases) y LSB de bits 1–3: sin payload.
- Cola 4,61–7,26 s: tono constante de 100,03 Hz; sin FSK ni texto.
- Intro 0–0,57 s: fade-in del mismo tono.
- DTMF: las detecciones son clics de banda ancha en los ataques de las ráfagas, no tonos.
- Las 14 ráfagas corresponden a los 14 glifos de `KEY: SweetBlood` (duración,
  F0 constante 110,25 Hz), no a Morse.

## Artefactos

| Ruta | Contenido |
|---|---|
| `solucion/descifrar_susurro.py` | Extrae el LSB, localiza el Base64, decodifica y hace XOR con `SweetBl00d` |
| `work/bit0_msb.bin` | Flujo LSB empaquetado (40.000 B) |
| `work/blob.b64` | Cadena Base64 extraída |
| `work/salida.txt` | Salida del descifrado |
| `flag.txt` | Flag |
| `evidencias/band_1to1.png` | Render del texto del espectrograma |
| `scripts/` | Análisis previo (espectrogramas, glifos, LSB, DTMF, etc.) |
| `RESOLUCION_SUSURRO.md` | Investigación parcial previa (se conserva como histórico) |

## Lecciones

- Un texto en el espectrograma puede ser solo la *llave*; el segundo mensaje puede
  estar en el plano LSB y pasar desapercibido si solo se buscan cadenas imprimibles
  (el blob Base64 está al inicio, pero el resto parece ruido).
- La variante leet de la llave (`SweetBl00d`) se valida por el prefijo conocido
  `TRAMACTF{`: un XOR correcto convierte el ciphertext en texto coherente desde el
  primer byte.
- El LSB de un WAV sintético puede estar sesgado en intro/cola (tono puro) y aleatorio
  en el cuerpo (modulación); hay que mirar el flujo completo, no solo la estadística
  global.
