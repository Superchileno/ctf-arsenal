# Desafío 18 — La Partitura Muda

| Campo | Valor |
|---|---|
| Categoría | forense de audio / esteganografía en espectrograma |
| Dificultad | fácil-media |
| Puntos | — |
| Estado | ✅ resuelto |
| Flag | `flag{ejemplo}` |

## Enunciado

> **La Partitura Muda — El concierto que nadie escuchó** — TRAMA CTF 2026 · Archivo musical 014 […]
> Cuando se levantó el telón no hubo violines, ni piano […] De los parlantes salió un zumbido […]
> Al día siguiente la organización encontró una grabación del ensayo y un paquete digital cerrado con
> contraseña. […] «Que nadie haya escuchado la obra no significa que no la haya interpretado».
>
> Evidencia adjunta: `La_Partitura_Muda.zip`. Se resuelve con los archivos adjuntos; no requiere servicios.

## Reconocimiento

`La_Partitura_Muda.zip` (427.691 B, SHA256 `41ff1835...e3195b6c`) contiene:

| Archivo | Tamaño | Notas |
|---|---|---|
| `LEEME.txt` | 389 B | Acta de recepción: grabación + paquete cerrado |
| `partitura.wav` | 1.152.044 B | Grabación del ensayo |
| `premio.zip` | 243 B | Paquete protegido con contraseña |

`premio.zip` tiene una sola entrada: `flag.txt` (49 B), **cifrada** (ZipCrypto, método 0 = almacenada).

Metadatos del audio:

```
RIFF WAVE, PCM 16 bit, mono, 16000 Hz, 36,00 s
```

Se trata de un zumbido: la "música" no está pensada para escucharse, sino para **verse**.

## Análisis

El enunciado insiste en que «nadie escuchó la obra» pero «sí la interpretó»: la información está en el
dominio de la frecuencia, no en el mensaje audible. Un espectrograma de la grabación completa muestra
texto dibujado con energía entre ~1,2 y ~2,8 kHz:

```
RESONANCIA2026
```

Esa es la contraseña del paquete `premio.zip`. Al abrirlo:

```python
zipfile.ZipFile('premio.zip').read('flag.txt', pwd=b'RESONANCIA2026')
# b'flag{ejemplo}\n'
```

### Verificación / pistas descartadas

- El audio no contiene voz ni tonos DTMF/Morse evidentes: es un barrido con la imagen inyectada en
  frecuencia (técnica clásica de "spectrogram art").
- El ZIP es pequeño y de método *stored*: también sería atacable con texto plano conocido
  (`bkcrack` + prefijo `TRAMACTF{`), pero la vía prevista —y directa— es el espectrograma.
- No hay metadatos EXIF/RF64 ocultos ni datos tras el final del WAV; todo el secreto está en el espectro.

## Solución (pasos reproducibles)

```bash
# 1) Extraer la evidencia
unzip La_Partitura_Muda.zip -d work/

# 2) Generar el espectrograma y leer la contraseña
sox work/partitura.wav -n spectrogram -o work/spec.png -x 1800 -y 900 -z 100
#   (imagen: RESONANCIA2026, entre 1,2 y 2,8 kHz)

# 3) Abrir el paquete protegido
python - <<'EOF'
import zipfile
z = zipfile.ZipFile('work/premio.zip')
print(z.read('flag.txt', pwd=b'RESONANCIA2026').decode())
EOF
```

## Flag

```
flag{ejemplo}
```

## Evidencia y artefactos

| Ruta | Contenido |
|---|---|
| `La_Partitura_Muda.zip` | Evidencia entregada (427.691 B) |
| `work/LEEME.txt` | Acta de recepción |
| `work/partitura.wav` | Grabación (36 s, 16 kHz mono) |
| `work/premio.zip` | Paquete cifrado (ZipCrypto) |
| `work/spec.png` / `work/spec_wide.png` | Espectrogramas generados (texto `RESONANCIA2026`) |
| `flag.txt` | Flag extraída de `premio.zip` |

## Lecciones / notas

- **Esteganografía en espectrograma**: lo que no se oye se ve; `sox ... spectrogram` es suficiente y no
  hace falta software especializado.
- La contraseña puede ser una cadena "temática" del reto (`RESONANCIA2026`, coherente con el título).
- Un ZIP con datos *stored* y cifrado clásico es vulnerable a *known-plaintext* si se conoce el prefijo
  de la flag; aquí no fue necesario, pero es una alternativa válida.
- Moraleja del enunciado: la obra "muda" sí se interpretó; el mensaje estaba en el sonido, no en la
  melodía.

## Backups

| Archivo | Backup |
|---|---|
| `ctf/CONTEXTO_CTF.md` (índice) | `ctf/backups/CONTEXTO_CTF.md.20261023-185821` |
