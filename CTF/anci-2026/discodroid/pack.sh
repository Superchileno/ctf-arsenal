#!/bin/bash
D="/mnt/c/Users/luis.miranda/OneDrive - dipreca.cl/Agentes IA/AUDITORIA_IA_V2/ANCI/discodroid"
cd ~
cp dp "$D/dp"
base64 -w 400 dp > "$D/dp.b64"
wc -c "$D/dp" "$D/dp.b64"
sha256sum dp
