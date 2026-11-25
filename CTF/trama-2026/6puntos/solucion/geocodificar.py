import json
import time
import urllib.parse
import urllib.request

PUNTOS = {
    "IMG_7C2E.jpg": (33, 1, 28.20, "S", 71, 33, 6.48, "W"),
    "IMG_2E8C.jpg": (33, 40, 46.88, "S", 70, 59, 5.35, "W"),
    "IMG_19B7.jpg": (34, 58, 58.04, "S", 71, 14, 21.95, "W"),
    "IMG_A91F.jpg": (35, 25, 36.98, "S", 71, 39, 56.02, "W"),
    "IMG_F03A.jpg": (40, 34, 26.00, "S", 73, 8, 1.00, "W"),
    "IMG_D440.jpg": (40, 52, 3.50, "S", 72, 35, 13.60, "W"),
}

def dec(g, m, s, ref):
    v = g + m / 60 + s / 3600
    return -v if ref in ("S", "W") else v

def nominatim(lat, lon):
    url = ("https://nominatim.openstreetmap.org/reverse?format=jsonv2&zoom=18&addressdetails=1"
           f"&lat={lat:.6f}&lon={lon:.6f}")
    req = urllib.request.Request(url, headers={"User-Agent": "ctf-research/1.0 (trama-ctf)"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)

for img, (g1, m1, s1, r1, g2, m2, s2, r2) in PUNTOS.items():
    lat, lon = dec(g1, m1, s1, r1), dec(g2, m2, s2, r2)
    print("=" * 70)
    print(f"{img}: {lat:.5f}, {lon:.5f}")
    try:
        j = nominatim(lat, lon)
        print("  display_name:", j.get("display_name"))
        a = j.get("address", {})
        claves = ["tourism", "leisure", "amenity", "road", "neighbourhood", "suburb",
                  "village", "town", "city", "municipality", "county", "state", "country"]
        for k in claves:
            if k in a:
                print(f"  {k:14s}: {a[k]}")
        print("  tipo:", j.get("type"), "| categoria:", j.get("category"))
    except Exception as e:
        print("  error:", e)
    time.sleep(1.2)
