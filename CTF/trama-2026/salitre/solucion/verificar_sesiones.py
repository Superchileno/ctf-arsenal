#!/usr/bin/env python3
"""SAL-16 - Control negativo: descifra las 6 sesiones del export DNS.

Cada alias del registro de accesos tiene su sesion. Solo la de `cormoran`
(A-1193 / Nordkapp, Tocopilla muelle 3, 06:06Z) contiene la flag; las demas
son actas internas. La de `azul` (A-1192 / Arauco Star, Mejillones muelle 3)
es el senuelo del mismo minuto UTC: descifra correctamente pero no es el
incidente.

Uso:  python verificar_sesiones.py
"""

import hashlib
import re
from pathlib import Path

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

BASE = Path(__file__).resolve().parents[1] / "evidencias"

# (alias, folio DNS): (folio, contenedor, hora UTC)
SESIONES = {
    ("petrel", "a1188"): ("A-1188", "TEMU4321", "2026-01-16T05:44Z"),
    ("gaviota", "a1191"): ("A-1191", "OOLU2740", "2026-01-16T06:01Z"),
    ("azul", "a1192"): ("A-1192", "CAIU2821", "2026-01-16T06:06Z"),
    ("cormoran", "a1193"): ("A-1193", "NYKU9087", "2026-01-16T06:06Z"),
    ("farero", "a1194"): ("A-1194", "HLBU3002", "2026-01-16T06:11Z"),
    ("merlin", "a1197"): ("A-1197", "NYKU9081", "2026-01-16T06:31Z"),
}

PATRON = re.compile(
    r"^_(?P<tipo>meta|p(?P<nn>\d+))\.(?P<alias>[a-z0-9]+)\.(?P<folio>a\d+)"
    r"\.control\.salitre\.invalid\.\s+\d+\s+IN\s+TXT\s+\"(?P<txt>[^\"]+)\"",
    re.I,
)


def cargar():
    sesiones = {}
    for linea in (BASE / "registros_dns.txt").read_text(encoding="utf-8").splitlines():
        m = PATRON.match(linea.strip())
        if not m:
            continue
        clave = (m["alias"].lower(), m["folio"].lower())
        datos = sesiones.setdefault(clave, {"meta": None, "partes": {}})
        campos = dict(
            par.split("=", 1) for par in m["txt"].split(";") if "=" in par
        )
        if m["tipo"].lower() == "meta":
            datos["meta"] = campos
        else:
            datos["partes"][int(m["nn"])] = campos["hex"]
    return sesiones


def main():
    for clave, sesion in sorted(cargar().items()):
        folio, contenedor, hora = SESIONES[clave]
        material = f"{folio}|{contenedor}|{clave[0]}|{hora}"
        key = hashlib.sha256(material.encode()).digest()
        ct = bytes.fromhex(
            "".join(sesion["partes"][n] for n in sorted(sesion["partes"]))
        )
        dec = Cipher(algorithms.AES(key), modes.CTR(bytes.fromhex(sesion["meta"]["iv"]))).decryptor()
        pt = dec.update(ct) + dec.finalize()
        valido = hashlib.sha256(pt).hexdigest() == sesion["meta"]["sha256"]
        print(f"{clave[0]:9} {clave[1]}  sha_ok={str(valido):5}  {pt.decode('utf-8', 'replace')}")


if __name__ == "__main__":
    main()
