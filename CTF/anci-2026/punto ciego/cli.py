#!/usr/bin/env python3
"""Cliente con reintentos para el reto Punto Ciego (upstream inestable)."""
import sys
import time

import requests
import urllib3

urllib3.disable_warnings()

BASE = "https://<host>/blind-spot"
COOKIE = ("eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9."
          "eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzkzMjg2MTkwLCJpYXQiOjE3OTMyNzUyMTcs"
          "Imp0aSI6IjliMTlkMDUwNjZiZDRkZjRiMGYyMzk1NGMwZGQ0OGQ1IiwidXNlcl9pZCI6NzI1ODB9."
          "ujK_nJHs29hFwtRtgNd7IZzLuQNqQeSXgkwaVpUcPHY")
HEADERS = {"User-Agent": "Mozilla/5.0", "Cookie": f"access={COOKIE}"}


def req(method, path, tries=25, timeout=15, **kw):
    last = None
    hdrs = {**HEADERS, **kw.pop("headers", {})}
    for i in range(tries):
        try:
            r = requests.request(method, BASE + path, headers=hdrs,
                                 timeout=timeout, verify=False, **kw)
            if r.status_code not in (502, 503, 504):
                return r
            last = f"{r.status_code}"
        except Exception as e:
            last = type(e).__name__
        time.sleep(0.25)
    return last


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "yaml":
        doc = sys.stdin.read()
        r = req("POST", "/api/preview", data=doc.encode(),
                headers={**HEADERS, "Content-Type": "text/yaml"})
    elif len(sys.argv) > 1:
        r = req("GET", sys.argv[1])
    else:
        r = req("GET", "/api/health")
    if isinstance(r, str):
        print(f"FALLO tras reintentos: {r}")
        sys.exit(1)
    print(f"STATUS {r.status_code}  ({len(r.content)} b)")
    print(r.text[:4000])
