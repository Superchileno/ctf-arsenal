#!/bin/bash
cd /mnt/c/Users/<usuario>/AppData/Local/Temp/opencode/caleuche || exit 1
echo "llave AES (hex): $(od -An -tx1 -v llave_aes.bin | tr -d ' \n')"
echo
echo "== Descifrando manifiesto.enc (AES-256-CBC, IV de iv.hex) =="
openssl enc -d -aes-256-cbc -K "$(od -An -tx1 -v llave_aes.bin | tr -d ' \n')" \
  -iv "$(tr -d '\n\r ' < iv.hex)" -in manifiesto.enc -out manifiesto.txt \
  && echo "OK (PKCS#7 valido)" || echo "FALLO"
echo
echo "===== CONTENIDO DEL MANIFIESTO ====="
cat manifiesto.txt; echo
echo "===================================="
