#!/usr/bin/env python3
"""
Desafío 09 - La Cuenta que No Existía

Rastro que conecta fotos <-> perfiles:
  - 4 de las 5 fotos están "limpias" (sin EXIF).
  - ultima_foto.jpg conserva EXIF: Artist = valen_nomade_priv,
    UserComment = "perfil espejo: valen_nomade_priv" y GPS 33°2'S 71°37'W.
  - Ese nombre apunta al perfil archivado valen_nomade_priv.html, cuyo
    "código de recuperación (base64)" es la flag.

Uso: python3 rastrear_cuenta.py
"""
import base64
import glob
import os
import re

from PIL import ExifTags, Image
from PIL.ExifTags import GPSTAGS

BASE = "/mnt/c/Users/shapl/OneDrive - dipreca.cl/Agentes IA/AUDITORIA_IA_V2/ctf/La_Cuenta_que_No_Existia/work"

INTERES = {"Artist", "UserComment", "Copyright", "ImageDescription", "Software", "Make", "Model"}


def leer_exif(ruta):
    img = Image.open(ruta)
    exif = img.getexif()
    datos = {}
    for tag_id, valor in exif.items():
        nombre = ExifTags.TAGS.get(tag_id, str(tag_id))
        if nombre in INTERES and isinstance(valor, (str, bytes)):
            datos[nombre] = valor.decode("utf-8", "replace") if isinstance(valor, bytes) else valor
    # GPS
    ifd = exif.get_ifd(0x8825) or {}
    gps = {GPSTAGS.get(k, k): v for k, v in ifd.items()}
    if gps:
        datos["_gps"] = gps
    return datos


def gps_decimal(gps):
    def conv(v):
        if not isinstance(v, tuple) or len(v) != 3:
            return None
        g, m, s = (float(x) for x in v)
        return g + m / 60 + s / 3600

    lat, lon = conv(gps.get("GPSLatitude")), conv(gps.get("GPSLongitude"))
    if lat is None or lon is None:
        return None
    if gps.get("GPSLatitudeRef") == "S":
        lat = -lat
    if gps.get("GPSLongitudeRef") == "W":
        lon = -lon
    return lat, lon


def main():
    print("== 1) EXIF de las 5 fotografías ==")
    usuario = None
    for f in sorted(glob.glob(BASE + "/fotos/*.jpg")):
        datos = leer_exif(f)
        nombre = os.path.basename(f)
        if not datos:
            print(f"  {nombre:20s} sin EXIF (limpia)")
            continue
        print(f"  {nombre:20s} CON EXIF -> {datos}")
        for clave in ("Artist", "UserComment"):
            if clave in datos:
                usuario = datos[clave].split(":")[-1].strip()
                print(f"      -> huella de usuario: {usuario!r}")
        if "_gps" in datos:
            coords = gps_decimal(datos["_gps"])
            if coords:
                print(f"      -> GPS: {coords[0]:.4f}, {coords[1]:.4f}")

    print("\n== 2) Perfil archivado que corresponde a esa huella ==")
    ruta = BASE + f"/archivo_web/{usuario}.html" if usuario else None
    if not ruta or not os.path.exists(ruta):
        raise SystemExit(f"[-] no hay perfil archivado para {usuario!r}")
    print(f"  abriendo {os.path.basename(ruta)}")
    html = open(ruta, encoding="utf-8", errors="replace").read()
    m = re.search(r"base64\)?:\s*([A-Za-z0-9+/=]+)", html)
    print(f"  código: {m.group(1)}")

    print("\n== 3) Decodificación ==")
    flag = base64.b64decode(m.group(1)).decode()
    print(f"  {flag}")
    if re.match(r"TRAMACTF\{.+\}", flag):
        open(BASE + "/../flag.txt", "w").write(flag + "\n")
        print("  [+] guardada en flag.txt")


if __name__ == "__main__":
    main()
