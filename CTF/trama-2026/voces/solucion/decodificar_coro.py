#!/usr/bin/env python3
"""El Coro de Treinta Voces — decodificador de tomas.

Cada toma dura 0,35 s (0,30 s de nota + 0,05 s de silencio) y contiene dos tonos:
  - banco GRAVE: 520 + 40*k  (k = dígito hexadecimal ALTO, 0..15)
  - banco AGUDO: 1400 + 40*k (k = dígito hexadecimal BAJO, 0..15)
byte = (alto << 4) | bajo.

Solo las tomas MAESTRAS entran al montaje, en el orden indicado por la planilla.
Las CALIBRACION son señuelos.

Uso:
  python3 decodificar_coro.py [work/coro_30_tomas.wav] [work/planilla_de_mezcla.csv]
"""
import csv
import pathlib
import sys
import wave

import numpy as np

WAV = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "work/coro_30_tomas.wav")
CSV = pathlib.Path(sys.argv[2] if len(sys.argv) > 2 else "work/planilla_de_mezcla.csv")

TAKE_SECONDS = 0.35
NOTE_SECONDS = 0.30
LOW0, HIGH0, STEP = 520, 1400, 40
NFFT = 32768


def read_mono(path):
    with wave.open(str(path), "rb") as w:
        assert w.getnchannels() == 1 and w.getsampwidth() == 2
        sr = w.getframerate()
        frames = w.readframes(w.getnframes())
    return sr, np.frombuffer(frames, dtype="<i2").astype(np.float64)


def peak_freq(seg, sr, fmin, fmax):
    win = np.hanning(len(seg))
    spec = np.abs(np.fft.rfft(seg * win, n=NFFT))
    freqs = np.fft.rfftfreq(NFFT, 1.0 / sr)
    band = (freqs >= fmin) & (freqs <= fmax)
    idx = np.argmax(spec[band])
    return freqs[band][idx]


def decode_take(sr, data, n):
    start = int(round((n - 1) * TAKE_SECONDS * sr))
    # ventana central de la nota (evita ataque/liberación del tono)
    a = start + int(0.05 * sr)
    b = start + int(0.28 * sr)
    seg = data[a:b]
    f_low = peak_freq(seg, sr, 480, 1220)
    f_high = peak_freq(seg, sr, 1320, 2080)
    k_low = int(round((f_low - LOW0) / STEP))
    k_high = int(round((f_high - HIGH0) / STEP))
    return (
        max(0, min(15, k_low)),
        max(0, min(15, k_high)),
        f_low,
        f_high,
    )


def main():
    sr, data = read_mono(WAV)
    n_takes = int(round(len(data) / sr / TAKE_SECONDS))
    print(f"# {WAV}  sr={sr} Hz  tomas={n_takes}")

    rows = list(csv.DictReader(CSV.open(encoding="utf-8")))
    decoded = {}
    for row in rows:
        n = int(row["toma"])
        k_low, k_high, f_low, f_high = decode_take(sr, data, n)
        byte = (k_low << 4) | k_high
        ch = chr(byte) if 32 <= byte < 127 else "."
        decoded[n] = (row["clase"], row["orden"], byte)
        print(
            f"toma {n:02d} {row['clase']:<11} orden={row['orden']:>2}  "
            f"grave={f_low:7.1f}Hz({k_low:X}) agudo={f_high:7.1f}Hz({k_high:X}) "
            f"-> 0x{byte:02X} {ch}"
        )

    maestras = sorted(
        ((int(o), n, decoded[n][2]) for n, (c, o, b) in decoded.items() if c == "MAESTRA"),
        key=lambda t: t[0],
    )
    msg = bytes(b for _, _, b in maestras)
    print("\n# MAESTRAS en orden editorial")
    print("orden:", " ".join(f"{o:02d}" for o, _, _ in maestras))
    print("tomas:", " ".join(f"{n:02d}" for _, n, _ in maestras))
    print("bytes:", msg.hex())
    print("texto:", repr(msg.decode(errors="replace")))


if __name__ == "__main__":
    main()
