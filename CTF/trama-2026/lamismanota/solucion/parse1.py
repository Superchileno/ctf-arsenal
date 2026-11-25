import xml.etree.ElementTree as ET
import sys, re

P = "/mnt/c/Users/shapl/AppData/Local/Temp/opencode/lamismanota/mscz/mi heart is broken.mscx"
tree = ET.parse(P)
root = tree.getroot()

score = root.find("Score")
print("hijos de Score:", [c.tag for c in score][:20])

# localizar staves
staffs = score.findall("Part/Staff")
print("staves en Part:", len(staffs))
# MuseScore 4: <Score><Staff id="1"> con <Measure>
all_staff = score.findall("Staff")
print("Score/Staff:", [(s.get("id"), len(s.findall("Measure"))) for s in all_staff])

# contar notas por compas y staff
def notes_of_measure(meas):
    out = []
    for ch in meas.iter("Chord"):
        for n in ch.findall("Note"):
            out.append(n)
    return out

for s in all_staff:
    sid = s.get("id")
    ms = s.findall("Measure")
    print(f"Staff {sid}: {len(ms)} compases")
