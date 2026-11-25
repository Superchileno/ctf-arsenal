#!/bin/bash
cd /mnt/c/Users/shapl/AppData/Local/Temp/opencode/lamismanota || exit 1
echo "=== tipos ==="
file practica_17.mscz anotaciones.zip
echo
echo "=== contenido mscz ==="
unzip -l practica_17.mscz
echo
echo "=== contenido anotaciones.zip ==="
unzip -l anotaciones.zip
echo
echo "=== intento de extraer anotaciones ==="
rm -rf anot && mkdir anot && cd anot
unzip -o ../anotaciones.zip 2>&1 | head -20
cd ..
ls -lR anot 2>/dev/null
