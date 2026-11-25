#!/bin/bash
D="/mnt/c/Users/shapl/OneDrive - dipreca.cl/Agentes IA/AUDITORIA_IA_V2/ctf/6puntos/work/mapa"
mkdir -p "$D"
UA="User-Agent: ctf-research/1.0"
# punto 6: -40.86764,-72.58711  -> z12 x1222 y2558 ; vecinos para contexto
for t in "12/1222/2558" "12/1221/2558" "12/1222/2557" "12/1221/2557" "13/2444/5117"; do
  f="$D/tile_$(echo $t | tr '/' '_').png"
  curl -s -H "$UA" "https://tile.openstreetmap.org/$t.png" -o "$f"
  echo "$f $(stat -c%s "$f") bytes"
done
