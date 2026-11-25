#!/bin/bash
cd /mnt/c/Users/<usuario>/AppData/Local/Temp/opencode/susurro || exit 1
mkdir -p out
# recorte temporal 0.5-4.8s y banda 2500-4500 Hz, alta resolucion
sox ChismeAudio.wav -n trim 0.5 4.3 highpass 2400 lowpass 4600 rate 12000 \
  spectrogram -x 2600 -y 700 -z 120 -o out/spec_text.png
# version con mayor contraste
sox ChismeAudio.wav -n trim 0.5 4.3 highpass 2400 lowpass 4600 rate 12000 \
  spectrogram -x 3000 -y 800 -o out/spec_text2.png
ls -l out/spec_text*.png
