#!/bin/bash
cd /mnt/c/Users/shapl/AppData/Local/Temp/opencode/caleuche || exit 1

echo "== Tamano del sobre =="
ls -l llave_sobre.rsa manifiesto.enc

echo
echo "== Descifrando llave simetrica con turno_2 (RSA-OAEP SHA-256) =="
openssl pkeyutl -decrypt -inkey respaldo_turno_2.pem \
  -in llave_sobre.rsa -out llave_aes.bin \
  -pkeyopt rsa_padding_mode:oaep -pkeyopt rsa_oaep_md:sha256 -pkeyopt rsa_mgf1_md:sha256 \
  && echo "OK" || echo "FALLO"

ls -l llave_aes.bin 2>/dev/null
echo "llave (hex):"
xxd -p llave_aes.bin | tr -d '\n'; echo
