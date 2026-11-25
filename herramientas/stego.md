# Esteganografía y análisis de archivos

## Regla cero

Ningún archivo «está limpio» hasta haber mirado **después de su fin lógico** y sus
**metadatos**.

## Carving de datos anexados

```bash
binwalk archivo
binwalk -e --run-as=root archivo
foremost -t all -i archivo -o work/carve
python ../arsenal/ctf-arsenal carve archivo --out work/
```

Puntos de corte: `FFD9` (JPEG), `49454E44AE426082` (IEND PNG), `%%EOF` (PDF),
`PK\x03\x04` (ZIP anexado).

## Metadatos

```bash
exiftool -a -u -g1 archivo
identify -verbose imagen.png      # ImageMagick
pdfinfo documento.pdf
strings -n 6 archivo | head -60
```

## Imágenes

```bash
# LSB
zsteg imagen.png                  # prueba bit 0..7, canales y orden
python ../arsenal/ctf-arsenal lsb imagen.png --bit 0 --order interleaved

# Patrón periódico (mosaico)
python ../arsenal/ctf-arsenal pattern imagen.png --period 164

# Verificar integridad PNG
pngcheck -v imagen.png
```

## ZIP / RAR / 7z

```bash
unzip -l archivo.zip
zip2john archivo.zip > hash.txt
john hash.txt --wordlist=/usr/share/wordlists/rockyou.txt
bkcrack -C archivo.zip -c flag.txt -p plano.txt   # known plaintext
```

## Cadena de capas

```bash
python ../arsenal/ctf-arsenal decode archivo
python ../arsenal/ctf-arsenal zip archivo
```

## Documentos OOXML (docx/xlsx/pptx)

```bash
python ../arsenal/ctf-arsenal ooxml documento.docx
# manual: texto blanco (w:color FFFFFF), w:vanish, customXml/item1.xml, header/footer
unzip -o documento.docx -d work/docx
grep -rl 'FFFFFF' work/docx/word
```

## Audio

```bash
sox audio.wav -n spectrogram -o work/spec.png
python ../arsenal/ctf-arsenal spectrogram audio.wav --out work/
python ../arsenal/ctf-arsenal pcm-lsb audio.wav --bit 0
python ../arsenal/ctf-arsenal tones audio.wav
```

## QR y códigos de barra

```bash
zbarimg imagen.png
```

## Guardrails

- `binwalk -e` puede escribir muchos archivos: trabajar siempre en `work\`.
- Verificar hashes antes y después del carving.
- No publicar artefactos con datos de terceros.
