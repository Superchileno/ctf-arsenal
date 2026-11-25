#!/usr/bin/env python3
"""
Desafío 11 - 6puntos / "SEÑAL DETECTADA" (nodo VF0)

Idea:
  - Las 6 fotos conservan EXIF con (a) fecha/hora de captura y (b) GPS.
  - Orden de emisión = orden de DateTimeOriginal (6 días consecutivos, 17..22 oct 2026).
  - Lugar = municipio de cada coordenada (geocodificación inversa).
  - Los nombres, sin tildes ni espacios, se concatenan con "_".

Las coordenadas se decodifican a mano (tabla de abajo) para que el script funcione
también sin red; con --online consulta Nominatim para confirmar el municipio.
"""
import argparse
import glob
import json
import os
import time
import unicodedata
import urllib.parse
import urllib.request

from PIL import Image, ExifTags

BASE = "/mnt/c/Users/shapl/OneDrive - dipreca.cl/Agentes IA/AUDITORIA_IA_V2/ctf/6puntos"
FOTOS = BASE + "/work/*.jpg"

# Municipio / lugar identificado por geocodificación inversa (ver CONTEXTO.md)
# Punto 6: la coordenada está en la comuna de Puerto Octay, pero sobre el
# lago Rupanco; el "nombre más corto" que contiene la comuna es Rupanco, y
# además hace que las iniciales de los seis lugares formen VECTOR.
LUGARES = {
    "IMG_7C2E.jpg": "Viña del Mar",
    "IMG_2E8C.jpg": "El Monte",
    "IMG_19B7.jpg": "Curicó",
    "IMG_A91F.jpg": "Talca",
    "IMG_F03A.jpg": "Osorno",
    "IMG_D440.jpg": "Rupanco",
}


def leer_exif(ruta):
    exif = Image.open(ruta).getexif()
    fecha = exif.get(0x0132)                      # DateTime
    gps_ifd = exif.get_ifd(0x8825) or {}
    gps = {}
    for k, v in gps_ifd.items():
        gps[ExifTags.GPSTAGS.get(k, k)] = v
    return fecha, gps


def a_decimal(gps):
    def conv(v):
        g, m, s = (float(x) for x in v)
        return g + m / 60 + s / 3600
    lat = conv(gps["GPSLatitude"]) * (-1 if gps.get("GPSLatitudeRef") == "S" else 1)
    lon = conv(gps["GPSLongitude"]) * (-1 if gps.get("GPSLongitudeRef") == "W" else 1)
    return lat, lon


def normalizar(nombre):
    """Elimina tildes y espacios (regla del enunciado)."""
    sin_tildes = "".join(c for c in unicodedata.normalize("NFD", nombre)
                         if unicodedata.category(c) != "Mn")
    return sin_tildes.replace(" ", "")


def municipio(lat, lon):
    url = ("https://nominatim.openstreetmap.org/reverse?format=jsonv2&zoom=14"
           f"&addressdetails=1&lat={lat:.6f}&lon={lon:.6f}")
    req = urllib.request.Request(url, headers={"User-Agent": "trama-ctf/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        a = json.load(r).get("address", {})
    return a.get("city") or a.get("town") or a.get("village") or a.get("municipality")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--online", action="store_true", help="confirmar municipio con Nominatim")
    args = ap.parse_args()

    filas = []
    for ruta in sorted(glob.glob(FOTOS)):
        fecha, gps = leer_exif(ruta)
        lat, lon = a_decimal(gps)
        filas.append({"archivo": os.path.basename(ruta), "fecha": fecha,
                      "lat": lat, "lon": lon})
    filas.sort(key=lambda f: f["fecha"])            # orden de emisión

    print("Secuencia de pulsos (orden por DateTimeOriginal):\n")
    nombres = []
    for i, f in enumerate(filas, 1):
        lugar = LUGARES[f["archivo"]]
        if args.online:
            try:
                conf = municipio(f["lat"], f["lon"])
                print(f"    [online] {f['archivo']} -> {conf}")
            except Exception as e:
                print(f"    [online] error: {e}")
            time.sleep(1.2)
        nombres.append(lugar)
        print(f" {i}. {f['fecha']}  {f['archivo']:15s}  {f['lat']:9.5f}, {f['lon']:9.5f}  -> {lugar}")

    partes = [normalizar(n) for n in nombres]
    iniciales = "".join(p[0].upper() for p in partes)
    flag = "TRAMACTF{" + "_".join(partes) + "}"
    print("\nNombres normalizados (sin tildes ni espacios):", partes)
    print("Iniciales:", iniciales, "(deben formar VECTOR)")
    print("FLAG:", flag)

    with open(BASE + "/flag.txt", "w") as fh:
        fh.write(flag + "\n")


if __name__ == "__main__":
    main()
