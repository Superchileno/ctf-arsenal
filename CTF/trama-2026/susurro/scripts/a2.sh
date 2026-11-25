#!/bin/bash
cd /mnt/c/Users/<usuario>/AppData/Local/Temp/opencode/susurro || exit 1
mkdir -p out
# Espectrograma amplio (0-22 kHz)
sox ChismeAudio.wav -n remix - rate 44100 spectrogram -x 2000 -y 1025 -z 100 -o out/spec_full.png
# Espectrograma banda baja (0-4 kHz) con mas detalle
sox ChismeAudio.wav -n remix - rate 8000 spectrogram -x 2000 -y 1025 -z 100 -o out/spec_low.png
ls -l out
