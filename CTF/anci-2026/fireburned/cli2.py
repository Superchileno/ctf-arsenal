#!/usr/bin/env python3
"""Fireburned - cliente con reintentos para GET/POST JSON."""
import json
import sys
import time

import requests
import urllib3

urllib3.disable_warnings()

BASE = "https://<host>/fireburned"
HEADERS = {"User-Agent": "Mozilla/5.0"}


def req(method, path, tries=25, timeout=20, **kw):
    last = None
    hdrs = {**HEADERS, **kw.pop("headers", {})}
    for _ in range(tries):
        try:
            r = requests.request(method, BASE + path, headers=hdrs,
                                 timeout=timeout, verify=False, **kw)
            if r.status_code not in (502, 503, 504):
                return r
            last = r.status_code
        except Exception as e:
            last = type(e).__name__
        time.sleep(0.3)
    return last


def show(r):
    if isinstance(r, str):
        print("FALLO:", r)
        return
    print(f"STATUS {r.status_code} ({len(r.content)} b) {r.headers.get('content-type','')}")
    print(r.text[:4000])


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "post":
        path = sys.argv[2]
        data = json.loads(sys.argv[3])
        show(req("POST", path, json=data))
    else:
        show(req("GET", sys.argv[1] if len(sys.argv) > 1 else "/"))
