#!/bin/bash
# Extrae frame + recorte de esquina (canal verde) para una lista de sq
cd "/mnt/c/Users/<usuario>/OneDrive - dipreca.cl/Agentes IA/AUDITORIA_IA_V2/ctf/El_Conde_Ciber_Dracula/work" || exit 1
mkdir -p dvr esq2 tmp
# refrescar playlist para tener URL base con firma válida
URL=$(head -1 hls_720.txt)
curl -s "$URL" -o pl.m3u8
SEG=$(grep -m1 '^https' pl.m3u8)
BASE_SQ=$(grep -oE '/sq/[0-9]+/' pl.m3u8 | head -1 | tr -dc '0-9')
PDT=$(grep -m1 'PROGRAM-DATE-TIME' pl.m3u8 | cut -d: -f2-)
echo "base sq=$BASE_SQ  program-date-time:$PDT"

paso=${1:-8}
ini=${2:-3400}
fin=${3:-4300}

for ((SQ=ini; SQ<=fin; SQ+=paso)); do
  PNG="dvr/sq_${SQ}.png"
  if [ ! -f "$PNG" ]; then
    U=$(echo "$SEG" | sed "s#/sq/${BASE_SQ}/#/sq/$SQ/#")
    curl -s --max-time 20 "$U" -o tmp/seg.ts
    SZ=$(stat -c%s tmp/seg.ts 2>/dev/null || echo 0)
    if [ "$SZ" -gt 5000 ]; then
      ffmpeg -hide_banner -loglevel error -i tmp/seg.ts -frames:v 1 -update 1 -y "$PNG" 2>/dev/null
    fi
  fi
  if (( SQ % 40 == 0 )); then echo "  ... sq=$SQ"; fi
done
echo "frames dvr: $(ls dvr/*.png 2>/dev/null | wc -l)"
