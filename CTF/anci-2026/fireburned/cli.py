#!/usr/bin/env python3
"""Cliente con reintentos para retos de <host>."""
import sys
import time

import requests
import urllib3

urllib3.disable_warnings()

BASE = "https://<host>/fireburned"
HEADERS = {"User-Agent": "Mozilla/5.0"}


def req(method, path, tries=30, timeout=25, **kw):
    last = None
    for i in range(tries):
        try:
            r = requests.request(method, BASE + path, headers=HEADERS,
                                 timeout=timeout, verify=False, **kw)
            if r.status_code not in (502, 503, 504):
                return r
            last = r.status_code
        except Exception as e:
            last = type(e).__name__
        time.sleep(0.4)
    return last


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "/"
    r = req("GET", path)
    if isinstance(r, str):
        print("FALLO:", r)
        sys.exit(1)
    print(f"STATUS {r.status_code} ({len(r.content)} b) {r.headers.get('content-type')}")
    print(r.text[:5000])
