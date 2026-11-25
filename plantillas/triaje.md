# Plantilla — Triaje de un reto (5 minutos)

> Ejecutar antes de tocar el artefacto a fondo. Marca cada casilla y anota.

## 1. Inventario

- [ ] Listar todos los artefactos entregados con tamaño y `sha256sum`
- [ ] Leer el enunciado dos veces y subrayar la pregunta exacta
- [ ] Identificar el formato de cada archivo (`file`, `xxd | head`)

```bash
sha256sum * > SHA256SUMS
file *
```

## 2. Señal dominante

| Señal | Categoría probable | Skill |
|---|---|---|
| URL / API / SPA | web | `ctf-web` |
| ELF + host:puerto | pwn | `exploiting-binary-vulnerabilities-in-ctf` |
| ELF sin símbolos, pide token | reversing | `reversing-obfuscated-binaries-and-vms` |
| Imagen, ZIP, DOCX, PDF | stego / forense de archivo | `analyzing-file-artifacts-for-steganography` |
| Texto cifrado, tokens iguales | crypto | `solving-classical-and-custom-cryptography` |
| WAV, MP3, log, pcap, MFT | forense | `performing-ctf-forensics-on-audio-and-logs` |
| Pyjail, bash jail, SDR, VM | misc | `ctf-misc` |
| Modelo, pesos, endpoint LLM | ia/ml | `ctf-ai-ml` |
| Muestra, pcap malicioso, C2 | malware | `ctf-malware` |
| Foto, perfil, coordenadas | OSINT | `ctf-osint` |

## 3. Primeras comprobaciones universales

```bash
# ¿Hay algo después del fin lógico del archivo?
binwalk -e archivo
python arsenal/ctf-arsenal carve archivo

# ¿Metadatos?
exiftool archivo

# ¿Cadenas útiles?
strings -n 6 archivo | head -50

# ¿Texto oculto en lo visible?
# (abrir imágenes y documentos y mirar con zoom, activar marcas de formato)
```

## 4. Hipótesis inicial

- **Hipótesis 1:**
  - Cómo la falsaría:
- **Hipótesis 2:**
  - Cómo la falsaría:

## 5. Criterio de pivote

- Si dos intentos fallan → cambiar de **categoría**, no de payload.
- Si el artefacto no responde a la categoría esperada → releer el enunciado.
- Si aparece un resultado plausible pero raro → anotarlo como señuelo antes de
  descartarlo.
