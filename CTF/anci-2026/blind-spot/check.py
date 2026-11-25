#!/usr/bin/env python3
"""Comprueba si el reto Blind Spot (HackRocks) volvio a estar arriba.

Uso:  python check.py
Si responde, guarda el HTML en index.html y muestra los endpoints encontrados.
"""
import re
import sys
import time
from pathlib import Path

import requests

URL = "https://<host>/blind-spot/"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/203.0.113.10 Safari/537.36"
HERE = Path(__file__).parent


def probe(path, method="GET", timeout=20, **kw):
    t = time.time()
    try:
        r = requests.request(method, URL.rstrip("/") + path, timeout=timeout,
                             headers={"User-Agent": UA}, allow_redirects=False, **kw)
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
        forms = re.findall(r'<form[^>]*>', text, re.I)
        actions = re.findall(r'action=["\']([^"\']+)', text, re.I)
        scripts = re.findall(r'(?:fetch|axios\.(?:post|get))\(["\']([^"\']+)', text)
        print("forms:", forms)
        print("actions:", actions)
        print("fetch/axios:", sorted(set(scripts)))
        return 0

    for p in ("/health", "/api/preview", "/docs", "/openapi.json"):
        st, sz, s, extra = probe(p, timeout=10)
        print(f"GET {p} -> {st} ({sz} B, {s}s) {'' if st else extra}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
