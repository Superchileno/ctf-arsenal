#!/bin/bash
cd "/mnt/c/Users/shapl/OneDrive - dipreca.cl/Agentes IA/AUDITORIA_IA_V2/ctf/6puntos/work" || exit 1
for f in *.jpg; do
  echo "================ $f ================"
  exiftool -a -G1 -s "$f"
  echo "--- strings 8+ (filtrado) ---"
  strings -n 8 "$f" | grep -viE "^[A-Za-z0-9+/=]{40,}$" | grep -iE "trama|vf0|flag|http|lugar|place|name|route|coment|gps|fecha" | head -10
  echo
done
