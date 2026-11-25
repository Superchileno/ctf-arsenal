#!/usr/bin/env python3
"""Fireburned - fuzzing de rutas de la app principal."""
import json
import sys
import time

import requests
import urllib3

urllib3.disable_warnings()

BASE = "https://<host>/fireburned"
H = {"User-Agent": "Mozilla/5.0", "Content-Type": "application/json"}

PATHS = [
    "/api/cards", "/api/card", "/api/webhooks", "/api/hooks", "/api/config",
    "/api/settings", "/api/admin", "/api/debug", "/api/env", "/api/flag",
    "/api/internal", "/api/token", "/api/tokens", "/api/secrets",
    "/api/users", "/api/me", "/api/info", "/api/status", "/api/metrics",
    "/api/templates", "/api/drafts", "/api/store", "/api/db", "/api/send",
    "/api/distribute", "/api/notifications", "/api/docs", "/api/openapi.json",
    "/admin", "/internal", "/debug", "/metrics", "/env", "/flag",
    "/robots.txt", "/sitemap.xml", "/.git/config", "/server.js", "/app.js",
    "/package.json", "/api.js", "/config.js",
]


def get(path, tries=30):
    for _ in range(tries):
        try:
            r = requests.get(BASE + path, headers=H, timeout=12, verify=False)
            if r.status_code in (502, 503, 504):
                time.sleep(0.25)
                continue
            return r
        except Exception:
            time.sleep(0.25)
    return None


if __name__ == "__main__":
    for p in sys.argv[1:] or PATHS:
        r = get(p)
        if r is None:
            print(f"{p:24} -> SIN RESPUESTA", flush=True)
        elif r.status_code != 404:
            print(f"{p:24} -> {r.status_code} {len(r.content)}b {r.text[:180]!r}", flush=True)
    print("fin")
