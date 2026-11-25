#!/bin/bash
echo -n "openssl: "; openssl passwd -1 -salt aa pwned
python3 - <<'PY'
try:
    import crypt
    print("crypt:", crypt.crypt('pwned', '$1$aa'))
except Exception as e:
    print("crypt module:", e)
PY
