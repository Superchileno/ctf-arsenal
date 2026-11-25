#!/usr/bin/env python3
"""SAL-16 - Operacion Salitre.

Reconstruye la cadena completa a partir de las evidencias:

  camara (03:17, CAM-07) -> correccion por bitacora de sincronizacion
  -> hora oficial local -> zarpe UTC (rastreo + manifiesto)
  -> alias habilitado en registro de accesos -> sesion DNS cifrada
  -> AES-256-CTR -> flag + verificacion SHA-256

Uso:  python descifrar_sesion.py
"""

import csv
import hashlib
import re
from datetime import datetime, timedelta
from pathlib import Path

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

BASE = Path(__file__).resolve().parents[1]
EV = BASE / "evidencias"

# Lectura literal del fotograma CAM-07 (Tocopilla, muelle 3).
CAMARA = "CAM-07"
LECTURA_CAMARA = "03:17"
FECHA = "2026-01-16"
HUSO_LOCAL = timedelta(hours=-3)  # UTC-03:00 segun informe_marea_norte.pdf


def leer_csv(nombre):
    with open(EV / nombre, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def leer_dns():
    """Devuelve {(alias, folio): {'meta': {...}, 'partes': {nn: hex}}}."""
    sesiones = {}
    patron = re.compile(
        r"^_(?P<tipo>meta|p(?P<nn>\d+))\.(?P<alias>[a-z0-9]+)\.(?P<folio>a\d+)"
        r"\.control\.salitre\.invalid\.\s+\d+\s+IN\s+TXT\s+\"(?P<txt>[^\"]+)\"",
        re.I,
    )
    for linea in (EV / "registros_dns.txt").read_text(encoding="utf-8").splitlines():
        m = patron.match(linea.strip())
        if not m:
            continue
        clave = (m["alias"].lower(), m["folio"].lower())
        datos = sesiones.setdefault(clave, {"meta": None, "partes": {}})
        campos = dict(
            (k, v) for k, v in (par.split("=", 1) for par in m["txt"].split(";") if "=" in par)
        )
        if m["tipo"].lower() == "meta":
            datos["meta"] = campos
        else:
            datos["partes"][int(m["nn"])] = campos["hex"]

    # Integridad del sobre: segmentos 01..TT sin huecos ni duplicados.
    for clave, datos in sesiones.items():
        nn = sorted(datos["partes"])
        if nn != list(range(1, len(nn) + 1)):
            raise ValueError(f"Segmentos incompletos en {clave}: {nn}")
    return sesiones


def main():
    # 1) Hora real: el reloj de CAM-07 esta adelantado 11 min.
    fila_cam = next(r for r in leer_csv("bitacora_sincronizacion.csv")
                    if r["camara"] == CAMARA and r["fecha"] == FECHA)
    mostrada = datetime.strptime(f"{FECHA} {fila_cam['hora_mostrada']}", "%Y-%m-%d %H:%M")
    oficial_sync = datetime.strptime(f"{FECHA} {fila_cam['hora_oficial_local']}", "%Y-%m-%d %H:%M")
    desfase = mostrada - oficial_sync
    hora_local = datetime.strptime(f"{FECHA} {LECTURA_CAMARA}", "%Y-%m-%d %H:%M") - desfase
    hora_utc = hora_local - HUSO_LOCAL
    print(f"[1] CAM-07 muestra {LECTURA_CAMARA}; desfase {desfase} "
          f"-> local {hora_local:%H:%M} -> UTC {hora_utc:%Y-%m-%dT%H:%M}Z")

    # 2) Acceso: solo CAM-07 (Tocopilla, muelle 3) a esa hora oficial.
    acceso = next(r for r in leer_csv("registro_accesos.csv")
                  if r["fecha"] == FECHA and r["camara"] == CAMARA
                  and r["hora_oficial_local"] == f"{hora_local:%H:%M}")
    alias = acceso["alias"]
    print(f"[2] Acceso {acceso['evento']}: alias '{alias}' ({acceso['credencial']})")

    # 3) Zarpe: mismo puerto y muelle, hora UTC exacta. Descarta el zarpe
    #    simultaneo de otro puerto (p. ej. Mejillones muelle 3).
    utc_txt = f"{hora_utc:%Y-%m-%dT%H:%M}:00Z"
    zarpe = next(r for r in leer_csv("rastreo_maritimo.csv")
                 if r["hora_utc"] == utc_txt
                 and r["puerto_reportado"] == acceso["puerto"]
                 and r["muelle_reportado"] == acceso["muelle"])
    print(f"[3] Zarpe {utc_txt}: {zarpe['buque']} "
          f"({zarpe['puerto_reportado']}, muelle {zarpe['muelle_reportado']})")

    # 4) Manifiesto: folio y contenedor reales del buque.
    manifiesto = next(r for r in leer_csv("manifiesto_carga.csv")
                      if r["buque"] == zarpe["buque"]
                      and r["puerto"] == zarpe["puerto_reportado"])
    folio, contenedor = manifiesto["folio"], manifiesto["contenedor"]
    print(f"[4] Manifiesto: folio {folio}, contenedor {contenedor}")

    # 5) Sobre DNS de la sesion y llave derivada.
    sesiones = leer_dns()
    clave_sesion = (alias.lower(), folio.lower().replace("-", ""))
    sesion = sesiones[clave_sesion]
    hora = f"{hora_utc:%Y-%m-%dT%H:%M}Z"
    material = f"{folio}|{contenedor}|{alias.lower()}|{hora}"
    llave = hashlib.sha256(material.encode("utf-8")).digest()
    print(f"[5] Clave = SHA256({material!r}) = {llave.hex()}")

    # 6) AES-256-CTR: concatenar segmentos por NN y validar SHA-256.
    ct = bytes.fromhex("".join(sesion["partes"][n] for n in sorted(sesion["partes"])))
    iv = bytes.fromhex(sesion["meta"]["iv"])
    dec = Cipher(algorithms.AES(llave), modes.CTR(iv)).decryptor()
    pt = dec.update(ct) + dec.finalize()
    sha = hashlib.sha256(pt).hexdigest()
    if sha != sesion["meta"]["sha256"]:
        raise SystemExit(f"[!] SHA-256 no coincide: {sha} != {sesion['meta']['sha256']}")

    print(f"[6] SHA-256 verificado: {sha}")
    print("\nFLAG:", pt.decode("utf-8"))


if __name__ == "__main__":
    main()
