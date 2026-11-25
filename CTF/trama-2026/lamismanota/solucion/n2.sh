#!/bin/bash
cd /mnt/c/Users/shapl/AppData/Local/Temp/opencode/lamismanota || exit 1
rm -rf mscz && mkdir mscz
cd mscz
unzip -o -q ../practica_17.mscz
ls -l
f="mi heart is broken.mscx"
echo "=== cabecera ==="
head -30 "$f"
echo "=== conteo de etiquetas relevantes ==="
for t in Measure Staff Voice Chord Rest Note Accidental Tie Slur Articulation StaffText Expression Fermata Arpeggio Glissando Lyric; do
  printf "%-14s %s\n" "$t" "$(grep -c "<$t" "$f")"
done
