#!/usr/bin/env python3
"""Fireburned - prueba de creacion/listado en el store (POST)."""
import json
import sys
import time

import requests
import urllib3

urllib3.disable_warnings()

MIRROR = sys.argv[1] if len(sys.argv) > 1 else "fireburned-3"
BASE = f"https://<host>/{MIRROR}"
H = {"User-Agent": "Mozilla/5.0", "Content-Type": "application/json"}
DB = "http://fireburned--db:8080"

PATHS = ["/", "/cards", "/drafts", "/hooks", "/hook", "/documents",
         "/webhook", "/notify", "/api/cards", "/v1/cards"]
BODY = json.dumps({"template": "hello",
                   "fields": {"template": {"stringValue": "hello"}}})


def call(url, method="POST", body=BODY, tries=8):
    p = {"url": url, "method": method}
    if body is not None:
        p["body"] = body
    for _ in range(tries):
        try:
            r = requests.post(BASE + "/api/fetch", data=json.dumps(p),
                              headers=H, timeout=12, verify=False)
            if r.status_code in (502, 503, 504):
                time.sleep(0.4)
                continue
            return r
        except Exception:
            time.sleep(0.4)
    return None


if __name__ == "__main__":
    for path in PATHS:
        r = call(DB + path, "POST")
        print(f"POST {path:14} -> {None if r is None else r.text[:250]}", flush=True)
    for path in PATHS:
        r = call(DB + path, "GET", None)
        print(f"GET  {path:14} -> {None if r is None else r.text[:250]}", flush=True)
