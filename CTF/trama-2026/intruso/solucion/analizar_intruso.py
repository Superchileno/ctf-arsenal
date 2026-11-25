#!/usr/bin/env python3
"""Análisis de intruso.pcap — «Puerta Abierta».

Reconstruye el incidente FTP a partir de la captura:
  - escaneo previo de puertos,
  - intentos de login (USER/PASS) y respuestas,
  - sesión válida y transferencias (LIST / RETR),
  - contenido del archivo exfiltrado.

Requiere tshark en el PATH.
Uso: python3 analizar_intruso.py [intruso.pcap]
"""
import pathlib
import subprocess
import sys

PCAP = sys.argv[1] if len(sys.argv) > 1 else "../intruso.pcap"
OUT = pathlib.Path("work")
OUT.mkdir(parents=True, exist_ok=True)


def tshark(*args):
    return subprocess.run(["tshark", "-r", PCAP, *args], capture_output=True, text=True, check=True).stdout


def main():
    print("== FTP: comandos y respuestas ==")
    campos = tshark(
        "-Y", "ftp",
        "-T", "fields",
        "-e", "frame.number", "-e", "ip.src", "-e", "ip.dst",
        "-e", "ftp.request.command", "-e", "ftp.request.arg",
        "-e", "ftp.response.code", "-e", "ftp.response.arg",
    )
    fallos = 0
    usuario = clave = None
    archivo = None
    for linea in campos.splitlines():
        p = linea.split("\t")
        p += [""] * (7 - len(p))
        num, src, dst, cmd, arg, code, rarg = p[:7]
        if cmd == "USER":
            usuario = arg
        elif cmd == "PASS":
            clave = arg
        elif cmd in ("LIST", "RETR"):
            archivo = arg or cmd
        if code == "530" and clave is not None:
            fallos += 1
            print(f"  [{num}] {usuario}:{clave} -> 530 Login incorrecto")
            clave = None
        elif code == "230":
            print(f"  [{num}] {usuario}:{clave} -> 230 Acceso concedido")
        elif cmd in ("LIST", "RETR"):
            print(f"  [{num}] {cmd} {arg}")

    print(f"\nintentos fallidos: {fallos}")
    print(f"credenciales válidas: {usuario}/{clave}")
    print(f"archivo solicitado: {archivo}")

    print("\n== transferencias FTP (streams de datos) ==")
    data = tshark("-Y", "ftp-data", "-T", "fields", "-e", "tcp.stream", "-e", "tcp.len")
    streams = sorted({l.split("\t")[0] for l in data.splitlines() if l.strip()})
    for st in streams:
        total = sum(int(l.split("\t")[1]) for l in data.splitlines()
                    if l.strip() and l.split("\t")[0] == st and l.split("\t")[1].isdigit())
        print(f"  stream {st}: {total} bytes de datos")

    # El último stream de datos es el RETR del archivo exfiltrado
    st_archivo = streams[-1]
    hexdata = tshark(
        "-Y", f"tcp.stream=={st_archivo} && ip.src==198.51.100.10 && tcp.len>0",
        "-T", "fields", "-e", "tcp.payload",
    ).replace("\n", "")
    contenido = bytes.fromhex(hexdata).decode("utf-8", errors="replace")
    (OUT / "credenciales.txt").write_text(contenido, encoding="utf-8")
    print(f"\n== contenido de {archivo} (stream {st_archivo}) ==")
    print(contenido)

    # listado del servidor (primer stream de datos)
    if len(streams) > 1:
        st_list = streams[0]
        hexlist = tshark(
            "-Y", f"tcp.stream=={st_list} && ip.src==198.51.100.10 && tcp.len>0",
            "-T", "fields", "-e", "tcp.payload",
        ).replace("\n", "")
        (OUT / "listado.txt").write_text(bytes.fromhex(hexlist).decode("utf-8", errors="replace"), encoding="utf-8")
        print("== listado del servidor ==")
        print((OUT / "listado.txt").read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
