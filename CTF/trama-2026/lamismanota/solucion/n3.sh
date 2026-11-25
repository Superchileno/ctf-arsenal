#!/bin/bash
cd /mnt/c/Users/shapl/AppData/Local/Temp/opencode/lamismanota || exit 1
rm -rf anot2 && mkdir anot2
for p in 6d2a91c47b3e 6D2A91C47B3E e3b74c19a2d6 "6d 2a 91 c4 7b 3e" 6912e4f3d1a7; do
  out=$(unzip -o -P "$p" -d anot2 anotaciones.zip 2>&1)
  if echo "$out" | grep -qi "inflating\|extracting"; then
    echo ">>> EXITO con [$p]"
    cat anot2/mensaje.txt; echo
    break
  else
    echo "fallo [$p]: $(echo "$out" | head -2 | tr '\n' ' ')"
  fi
done
ls -l anot2
