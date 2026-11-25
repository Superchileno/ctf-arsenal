#!/bin/bash
cd /mnt/c/Users/shapl/AppData/Local/Temp/opencode/susurro || exit 1
set -x
soxi ChismeAudio.wav
exiftool ChismeAudio.wav
echo "== strings =="
strings -n 6 ChismeAudio.wav | head -40
echo "== tail hexdump (posible dato anexado) =="
tail -c 64 ChismeAudio.wav | od -Ax -tx1z
