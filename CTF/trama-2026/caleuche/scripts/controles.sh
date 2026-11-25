#!/bin/bash
cd /mnt/c/Users/shapl/AppData/Local/Temp/opencode/caleuche || exit 1
KEY="$(od -An -tx1 -v llave_aes.bin | tr -d ' \n')"

echo "== Control: IV de la boya (iv_boya.hex) con la llave correcta =="
openssl enc -d -aes-256-cbc -K "$KEY" -iv "$(tr -d '\n\r ' < iv_boya.hex)" -in manifiesto.enc -out /tmp/decoy_iv.txt 2>/dev/null \
  && echo "descifrado sin error" || echo "ERROR de padding -> descartado"
od -c /tmp/decoy_iv.txt 2>/dev/null | head -3

echo
echo "== Control: turno_1 y turno_3 contra el sobre =="
for i in 1 3; do
  printf "turno_%s: " "$i"
  openssl pkeyutl -decrypt -inkey "respaldo_turno_$i.pem" -in llave_sobre.rsa -out /tmp/k$i.bin \
    -pkeyopt rsa_padding_mode:oaep -pkeyopt rsa_oaep_md:sha256 -pkeyopt rsa_mgf1_md:sha256 2>/dev/null \
    && echo "descifra (inesperado)" || echo "FALLO -> no es la llave del receptor"
done

echo
echo "== Control: contrasena de la servilleta como llave AES-256-CBC =="
openssl enc -d -aes-256-cbc -pass pass:LLAVE-MAREA-1810 -iv "$(tr -d '\n\r ' < iv.hex)" -in manifiesto.enc -out /tmp/decoy_pw.txt 2>/dev/null \
  && echo "descifrado sin error (revisar)" || echo "ERROR de padding -> descartado"
