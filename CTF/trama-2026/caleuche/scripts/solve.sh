#!/bin/bash
cd /mnt/c/Users/<usuario>/AppData/Local/Temp/opencode/caleuche || exit 1

echo "== Huellas de claves publicas =="
for i in 1 2 3; do
  printf "turno_%s  " "$i"
  openssl pkey -in "respaldo_turno_$i.pem" -pubout 2>/dev/null | openssl dgst -sha256 | awk '{print $NF}'
done
printf "cert      "
openssl pkey -pubin -in certificado_receptor.pem -pubout 2>/dev/null | openssl dgst -sha256 | awk '{print $NF}'

echo
echo "== Modulos RSA (primeros 40 hex) =="
for i in 1 2 3; do
  printf "turno_%s  " "$i"
  openssl rsa -in "respaldo_turno_$i.pem" -noout -modulus 2>/dev/null | cut -c9-48
done
printf "cert      "
openssl rsa -pubin -in certificado_receptor.pem -noout -modulus 2>/dev/null | cut -c9-48
