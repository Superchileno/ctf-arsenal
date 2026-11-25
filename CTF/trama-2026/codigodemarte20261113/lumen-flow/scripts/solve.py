#!/usr/bin/env python3
"""CDM CTF 2026-11-13 - Lumen Flow (203.0.113.10:8083)

Idea del reto:
- El "modelo predictivo" es un Q-learning tabular con estados
  <zona>|<ocupacion>|<calidad> y acciones liberar/dosificar/retener.
- El envio ENV-900 vive en el estado `recepcion|alta|baja`.
- Si la accion elegida es `liberar`, el paquete se desvia por el canal C y
  `/api/simulation/<run>/resolve` devuelve la bandera (outcome
  `desvio_de_carga`).
- El modelo aprende con el feedback de cada episodio
  (`POST /api/replays/<id>/feedback`), donde el `observed_time` que envia el
  operador define la recompensa. Cerrando episodios con observed_time=5 y
  scan_errors=0 se inyecta recompensa maxima y `liberar` pasa a ser la accion
  preferida en ese estado.

Uso: python solve.py [host:puerto]
"""
from __future__ import annotations

import json
import sys
import time
import urllib.error
import urllib.request

HOST = sys.argv[1] if len(sys.argv) > 1 else "203.0.113.10:8083"
BASE = "http://" + HOST
STATE = "recepcion|alta|baja"


def api(path: str, payload=None, method: str = "GET"):
    datos = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(BASE + path, data=datos, method=method,
                                 headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.status, json.loads(r.read().decode("utf-8", "replace"))
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read().decode("utf-8", "replace")


def overview():
    return api("/api/overview")[1]


def entrenar(limite: int = 20) -> None:
    """Cierra episodios con recompensa alta hasta que `liberar` domine el estado."""
    for intento in range(1, limite + 1):
        estado = overview()
        objetivo = estado["target"]
        valores = objetivo["values"]
        if objetivo["decision"] == "liberar" and valores["liberar"] == max(valores.values()):
            print(f"[*] `liberar` ya domina {STATE}: {valores}")
            return

        print(f"[*] intento {intento}: valores={valores} decision={objetivo['decision']}")
        st, creado = api("/api/replays", {
            "name": f"Lote prioritario de auditoria {intento}",
            "zone": "recepcion",
            "queue_score": 90,
            "confidence": 10,
            "nominal_time": 90,
        }, "POST")
        if st != 200:
            print("[!] no se pudo crear el caso:", st, creado)
            return

        st, feedback = api(f"/api/replays/{creado['id']}/feedback", {
            "action": "liberar",
            "observed_time": 5,
            "scan_errors": 0,
        }, "POST")
        if st != 200:
            print("[!] feedback rechazado:", st, feedback)
            return
        print(f"    {creado['id']} -> reward={feedback.get('reward')} "
              f"liberar={feedback.get('new_value')}")

    print("[!] el modelo no llego a preferir `liberar`; revisar el estado")


def resolver(espera_extra: float = 1.5) -> str:
    st, inicio = api("/api/simulation/start", {}, "POST")
    if st not in (200, 201):
        raise SystemExit(f"no se pudo iniciar la simulacion: {st} {inicio}")
    run_id = inicio["run_id"]
    print(f"[*] simulacion {run_id} decision={inicio['decision']} "
          f"duracion={inicio['duration_ms']} ms")
    time.sleep(inicio.get("duration_ms", 5000) / 1000 + espera_extra)

    for _ in range(10):
        st, resultado = api(f"/api/simulation/{run_id}/resolve", {}, "POST")
        if st == 200 and isinstance(resultado, dict):
            print("[*] resultado:", json.dumps(resultado, ensure_ascii=False))
            if "flag" in resultado:
                return resultado["flag"]
            raise SystemExit("la simulacion no termino en desvio; modelo no entrenado")
        time.sleep(0.5)
    raise SystemExit(f"resolve no devolvio resultado: {st} {resultado}")


def main() -> int:
    estado = overview()
    print(f"[*] episodios={estado['model']['episodes']} "
          f"objetivo={estado['target']['code']} estado={estado['target']['state']}")
    entrenar()
    flag = resolver()
    print(f"[+] FLAG: {flag}")
    with open("flag.txt", "w", encoding="utf-8") as fh:
        fh.write(flag + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
