#!/usr/bin/env python3
"""Punto Ciego (HackRocks blind-spot) - comprobacion de disponibilidad.

Uso:
    python check.py

Lee la cookie JWT del reto (caduca 2026-10-29 15:03 UTC). Si el servicio
responde 200, guarda index.html y lista formularios/endpoints.
"""
import os
import re
import sys
import time
from pathlib import Path

import requests

URL = "https://<host>/blind-spot"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/203.0.113.10 Safari/537.36")
HERE = Path(__file__).parent

COOKIE = os.environ.get("CTF_ACCESS", (
    "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9."
    "eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzkzMjg2MTkwLCJpYXQiOjE3OTMyNzUyMTcs"
    "Imp0aSI6IjliMTlkMDUwNjZiZDRkZjRiMGYyMzk1NGMwZGQ0OGQ1IiwidXNlcl9pZCI6NzI1ODB9."
    "ujK_nJHs29hFwtRtgNd7IZzLuQNqQeSXgkwaVpUcPHY"
))
HEADERS = {"User-Agent": UA, "Cookie": f"access={COOKIE}"}


def probe(path, method="GET", timeout=20, **kw):
    t = time.time()
    try:
        r = requests.request(method, URL.rstrip("/") + path, timeout=timeout,
                             headers=HEADERS, allow_redirects=False, **kw)
        return r.status_code, len(r.content), round(time.time() - t, 1), r
    except Exception as e:
        return None, 0, round(time.time() - t, 1), type(e).__name__


def main():
    status, size, secs, r = probe("/", timeout=30)
    print(f"GET / -> {status} ({size} B, {secs}s) {'' if status else r}")

    if status == 200:
        text = r.text
        (HERE / "index.html").write_text(text, encoding="utf-8")
        print(f"OK: guardado index.html ({len(text)} chars)")
        forms = re.findall(r"<form[^>]*>", text, re.I)
        actions = re.findall(r"action=[\"']([^\"']+)", text, re.I)
        scripts = re.findall(r"(?:fetch|axios\.(?:post|get))\([\"']([^\"']+)", text)
        print("forms:", forms)
        print("actions:", actions)
        print("fetch/axios:", sorted(set(scripts)))
        return 0

    for p in ("/health", "/api/", "/api/preview", "/docs", "/openapi.json"):
        st, sz, s, extra = probe(p, timeout=12)
        print(f"GET {p} -> {st} ({sz} B, {s}s) {'' if st else extra}")
    print("\nServicio no disponible (upstream caido). Reintentar mas tarde.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
