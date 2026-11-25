import xml.etree.ElementTree as ET
from collections import Counter

P = "/mnt/c/Users/<usuario>/AppData/Local/Temp/opencode/lamismanota/mscz/mi heart is broken.mscx"
root = ET.parse(P).getroot()
score = root.find("Score")

SHARP = {16:'D', 17:'A', 18:'E', 19:'B', 20:'F#', 21:'C#', 22:'G#', 23:'D#', 24:'A#', 25:'E#', 26:'B#'}
FLAT  = {14:'C',13:'F',12:'Bb',11:'Eb',10:'Ab',9:'Db',8:'Gb',7:'Cb',6:'Fb'}
def name(tpc):
    return SHARP.get(tpc) or FLAT.get(tpc) or f"tpc{tpc}"

staves = score.findall("Staff")   # id 1, 2
data = {}   # (measure_idx, staff_id) -> list of notes
for st in staves:
    sid = int(st.get("id"))
    for mi, m in enumerate(st.findall("Measure")):
        chords = []
        # recorrer en orden documental
        for ch in m.iter("Chord"):
            chords.append(ch)
        notes = []
        for ch in chords:
            for n in ch.findall("Note"):
                notes.append({
                    "pitch": int(n.findtext("pitch")) if n.findtext("pitch") else None,
                    "tpc": int(n.findtext("tpc")) if n.findtext("tpc") else None,
                    "acc": (n.find("Accidental").findtext("subtype") if n.find("Accidental") is not None else None),
                })
        data[(mi, sid)] = notes

print("=== medidas con 16 notas (8+8) ===")
ok = 0
for mi in range(105):
    n1 = len(data.get((mi,1), [])); n2 = len(data.get((mi,2), []))
    if n1 == 8 and n2 == 8:
        ok += 1
print("medidas con 8+8 notas:", ok, "de 105")

print("\n=== notas con tpc 'raro' (sostenidos en contexto de bemoles) ===")
anom = []
for mi in range(105):
    for sid in (1,2):
        notes = data.get((mi,sid), [])
        for i, n in enumerate(notes):
            t = n["tpc"]
            if t in (16,17,18,19,20,21,22,23,24,25,26):
                anom.append((mi+1, sid, i, t, name(t), n["pitch"], n["acc"]))
for a in anom:
    print(f"compas {a[0]:3d}  staff {a[1]}  idx {a[2]:2d}  tpc {a[3]:2d} => {a[4]:3s}  pitch {a[5]:3d}  acc={a[6]}")
print("\ntotal:", len(anom))
