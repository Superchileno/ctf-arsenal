#!/usr/bin/env python3
"""Insiste en paralelo hasta obtener 200 de <host>/fireburned/."""
import sys
import threading
import time

import requests
import urllib3

urllib3.disable_warnings()

BASE = "https://<host>/fireburned"
HEADERS = {"User-Agent": "Mozilla/5.0"}
stop = threading.Event()
stats = {"ok": 0, "err": 0, "bad": 0}


def worker(path, outfile):
    while not stop.is_set():
        try:
            r = requests.get(BASE + path, headers=HEADERS, timeout=15, verify=False)
            if r.status_code == 200:
                with open(outfile, "wb") as f:
                    f.write(r.content)
                stats["ok"] += 1
                print(f"[+] 200 ({len(r.content)} b) -> {outfile}", flush=True)
                stop.set()
                return
            stats["bad"] += 1
            print(f"[-] {r.status_code}", flush=True)
        except Exception as e:
            stats["err"] += 1
            print(f"[!] {type(e).__name__}", flush=True)
        time.sleep(0.2)


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "/"
    out = sys.argv[2] if len(sys.argv) > 2 else "index.html"
    dur = int(sys.argv[3]) if len(sys.argv) > 3 else 900
    threads = [threading.Thread(target=worker, args=(path, out), daemon=True)
               for _ in range(4)]
    for t in threads:
        t.start()
    start = time.time()
    while not stop.is_set() and time.time() - start < dur:
        time.sleep(1)
    stop.set()
    print("stats:", stats)
    sys.exit(0 if stats["ok"] else 1)
