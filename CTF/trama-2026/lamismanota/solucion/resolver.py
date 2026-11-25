#!/usr/bin/env python3
"""Detecta las 12 reescrituras enarmonicas de practica_17.mscx y calcula el password del ZIP.

Regla de revision_17.txt: compas con 16 notas (8 arriba + 8 abajo); el contador
empieza en 0, cuenta primero las 8 del pentagrama superior y luego las 8 del inferior,
de izquierda a derecha. Cada indice (0-15) es un nibble hexadecimal.
"""
import sys, os, zipfile, subprocess
import xml.etree.ElementTree as ET

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MSCX = os.path.join(BASE, "mscz", "mi heart is broken.mscx")
ZIP = os.path.join(BASE, "anotaciones.zip")

SHARP = {21: "C#", 22: "G#", 23: "D#", 24: "A#", 25: "E#", 26: "B#", 16: "D", 17: "A", 18: "E"}
FLAT_OK = {7: "Cb", 8: "Gb", 9: "Db", 10: "Ab", 11: "Eb", 12: "Bb", 13: "F", 14: "C", 15: "G"}

def find_anomalies(mscx):
    root = ET.parse(mscx).getroot()
    score = root.find("Score")
    hits = []
    for st in score.findall("Staff"):
        sid = int(st.get("id"))
        for mi, m in enumerate(st.findall("Measure"), 1):
            notes = []
            for ch in m.iter("Chord"):
                for n in ch.findall("Note"):
                    acc = n.find("Accidental")
                    notes.append((
                        int(n.findtext("pitch") or 0),
                        int(n.findtext("tpc") or 0),
                        acc.findtext("subtype") if acc is not None else None,
                    ))
            n1, n2 = len(notes), None
            for i, (pitch, tpc, acc) in enumerate(notes):
                # reescritura enarmonica: tpc de sostenido SIN accidental impreso
                if tpc in (21, 22, 23, 24, 25) and acc is None:
                    hits.append({
                        "compas": mi, "staff": sid, "idx": i,
                        "tpc": tpc, "escrita": SHARP[tpc], "pitch": pitch,
                    })
    return hits

def password(hits):
    nibbles = []
    for h in sorted(hits, key=lambda x: (x["compas"], x["staff"], x["idx"])):
        nibbles.append(h["idx"] if h["staff"] == 1 else 8 + h["idx"])
    return "".join(f"{v:X}" for v in nibbles)

if __name__ == "__main__":
    if not os.path.exists(MSCX):
        subprocess.run(["unzip", "-o", "-q", os.path.join(BASE, "practica_17.mscz"), "-d",
                        os.path.join(BASE, "mscz")], check=True)
    hits = find_anomalies(MSCX)
    print(f"{len(hits)} inconsistencias:\n")
    print(f"{'#':>2} {'compas':>6} {'staff':>5} {'idx':>3} {'tpc':>3} {'escrita':>7} {'suena':>6} {'pitch':>5}")
    for i, h in enumerate(sorted(hits, key=lambda x: x["compas"]), 1):
        print(f"{i:2d} {h['compas']:6d} {h['staff']:5d} {h['idx']:3d} {h['tpc']:3d} "
              f"{h['escrita']:>7} {'':>6} {h['pitch']:5d}")
    pw = password(hits)
    print(f"\npassword = {pw}")
    with zipfile.ZipFile(ZIP) as z:
        try:
            data = z.read("mensaje.txt", pwd=pw.encode())
            print("\n--- mensaje.txt ---")
            print(data.decode())
        except RuntimeError as e:
            print("No se pudo abrir el zip:", e)
