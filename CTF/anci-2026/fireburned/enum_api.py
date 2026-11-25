#!/usr/bin/env python3
"""Fireburned - enumeracion inicial de la API (cuando el upstream responda)."""
import json
import sys

from cli import req

PATHS = [
    "/", "/api/health", "/api/version", "/api/", "/api/webhooks",
    "/api/hooks", "/api/drafts", "/api/documents", "/api/preview",
    "/api/notifications", "/api/cards", "/api/integrations", "/api/config",
    "/api/users", "/api/me", "/login", "/robots.txt", "/openapi.json",
]

if __name__ == "__main__":
    for p in PATHS:
        r = req("GET", p, tries=15, timeout=12)
        if isinstance(r, str):
            print(f"{p:24} -> {r}")
            continue
        ct = r.headers.get("content-type", "")
        body = r.text[:200].replace("\n", " ")
        print(f"{p:24} -> {r.status_code} {len(r.content):6d}b {ct:28} {body}")
