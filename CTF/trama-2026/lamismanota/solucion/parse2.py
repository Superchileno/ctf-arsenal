import xml.etree.ElementTree as ET
from collections import Counter

P = "/mnt/c/Users/<usuario>/AppData/Local/Temp/opencode/lamismanota/mscz/mi heart is broken.mscx"
root = ET.parse(P).getroot()
score = root.find("Score")

NAMES = {0:'C',1:'G',2:'D',3:'A',4:'E',5:'B',6:'F#',7:'C#',8:'G#',9:'D#',10:'A#',11:'E#',12:'B#'}
def tpc_name(tpc):
    # tpc = 14 + k  (k posicion en quintas)
    k = tpc - 14
    oct_shift, idx = divmod(k, 7)
    base = NAMES[idx % 12] if idx >= 0 else None
    name = NAMES.get(idx % 12 if idx % 12 >= 0 else idx+12, '?')
    # corregir nombres para k negativos
    flat_names = {0:'F',1:'Bb',2:'Eb',3:'Ab',4:'Db',5:'Gb',6:'Cb'}
    if k < 0:
        q, r = divmod(-k, 7)
        nm = flat_names[r]
        return nm + ("b" * 0)
    return name

print("=== distribucion global de tpc ===")
tpcs = Counter()
for st in score.findall("Staff"):
    for n in st.iter("Note"):
        t = n.findtext("tpc")
        if t: tpcs[int(t)] += 1
for t,c in sorted(tpcs.items()):
    print(f"  tpc {t:3d} ({tpc_name(t):4s}) -> {c}")

print("\n=== armaduras (KeySig) ===")
for st in score.findall("Staff"):
    sid = st.get("id")
    keys = []
    for i, m in enumerate(st.findall("Measure"), 1):
        for ks in m.iter("KeySig"):
            acc = ks.findtext("accidental")
            keys.append((i, acc))
    # solo cambios
    prev = None; cambios = []
    for i, a in keys:
        if a != prev:
            cambios.append((i, a)); prev = a
    print(f"  Staff {sid}: {cambios}")
