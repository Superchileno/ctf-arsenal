#!/usr/bin/env python3
"""
Pirata 1 — transcripción ASR (faster-whisper) del audio normal y al revés.
Se pasa la señal como np.float32 ya que la versión de PyAV instalada no es
compatible con el decodificador de faster-whisper.
"""
import re
import wave
from pathlib import Path

import numpy as np
from faster_whisper import WhisperModel

W = Path("/mnt/c/Users/shapl/OneDrive - dipreca.cl/Agentes IA/AUDITORIA_IA_V2/ctf/pirata1/work")


def leer(ruta: Path) -> np.ndarray:
    with wave.open(str(ruta)) as w:
        fr = w.getframerate()
        x = np.frombuffer(w.readframes(w.getnframes()), dtype="<i2")
    if fr != 16000:
        # remuestreo sencillo por interpolación
        n = int(len(x) * 16000 / fr)
        idx = np.linspace(0, len(x) - 1, n)
        x = np.interp(idx, np.arange(len(x)), x)
    return (x.astype(np.float32) / 32768.0)


modelo = WhisperModel("base", device="cpu", compute_type="int8")
print("modelo cargado")

for nombre, ruta in (("NORMAL", W / "senal_malapata.wav"), ("REVERSO", W / "reverso.wav")):
    print(f"\n===== {nombre} =====")
    audio = leer(ruta)
    segs, info = modelo.transcribe(audio, language="es", beam_size=1,
                                   vad_filter=False, condition_on_previous_text=False)
    for s in segs:
        texto = s.text.strip()
        if not texto:
            continue
        marca = ""
        if re.search(r"(?i)trama|flag|grados|latitud|longitud|coordenad|sur|norte|plus|mapa|c[oó]digo", texto):
            marca = "  <---"
        print(f"[{s.start:6.1f}-{s.end:6.1f}] {texto}{marca}")
