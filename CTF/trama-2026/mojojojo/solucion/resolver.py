#!/usr/bin/env python3
"""
Desafío 08 - Mojojojo: "Las Calilas, la Mojojojo y el mensaje del micrófono"

Cadena de capas (todas dentro de la "grabación" transmision.txt):

    transmision.txt            hex ASCII  ("3a 53 41 20 ...")
      -> ASCII                 Base45 (RFC 9285, alfabeto 45 simbolos)
      -> Base45                Base64
      -> Base64                codigo Ook!  (el "mono escribiendo")
      -> Ook!                  Brainfuck
      -> Brainfuck             FLAG

Uso: python3 resolver.py [ruta_transmision]
"""
import base64
import re
import sys

BASE = "/mnt/c/Users/<usuario>/OneDrive - dipreca.cl/Agentes IA/AUDITORIA_IA_V2/ctf/mojojojo"
RUTA = sys.argv[1] if len(sys.argv) > 1 else BASE + "/work/transmision.txt"

# Base45 (RFC 9285)
ALFABETO45 = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ $%*+-./:"

# Ook! -> Brainfuck (pares de tokens)
OOK = {
    ("Ook.", "Ook?"): ">",
    ("Ook?", "Ook."): "<",
    ("Ook.", "Ook."): "+",
    ("Ook!", "Ook!"): "-",
    ("Ook!", "Ook."): ".",
    ("Ook.", "Ook!"): ",",
    ("Ook!", "Ook?"): "[",
    ("Ook?", "Ook!"): "]",
}


def base45_decode(s: str) -> bytes:
    out = bytearray()
    for i in range(0, len(s) - 2, 3):
        v = (ALFABETO45.index(s[i])
             + ALFABETO45.index(s[i + 1]) * 45
             + ALFABETO45.index(s[i + 2]) * 45 * 45)
        if v > 0xFFFF:
            raise ValueError(f"grupo Base45 fuera de rango en {i}: {v}")
        out += bytes((v // 256, v % 256))
    return bytes(out)


def ook_a_brainfuck(ook: str) -> str:
    tok = ook.split()
    if len(tok) % 2:
        raise ValueError("número impar de tokens Ook")
    return "".join(OOK[(tok[i], tok[i + 1])] for i in range(0, len(tok), 2))


def ejecutar_bf(bf: str, max_pasos: int = 50_000_000) -> str:
    cinta = [0] * 30000
    ptr = pc = pasos = 0
    salida = []
    saltos, pila = {}, []
    for i, c in enumerate(bf):
        if c == "[":
            pila.append(i)
        elif c == "]":
            j = pila.pop()
            saltos[i], saltos[j] = j, i
    while pc < len(bf) and pasos < max_pasos:
        c = bf[pc]
        if c == ">":
            ptr += 1
        elif c == "<":
            ptr -= 1
        elif c == "+":
            cinta[ptr] = (cinta[ptr] + 1) & 255
        elif c == "-":
            cinta[ptr] = (cinta[ptr] - 1) & 255
        elif c == ".":
            salida.append(chr(cinta[ptr]))
        elif c == ",":
            cinta[ptr] = 0
        elif c == "[" and cinta[ptr] == 0:
            pc = saltos[pc]
        elif c == "]" and cinta[ptr] != 0:
            pc = saltos[pc]
        pc += 1
        pasos += 1
    return "".join(salida)


def main() -> None:
    # capa 1: hex -> ASCII
    hexs = re.findall(rb"[0-9A-Fa-f]{2}", open(RUTA, "rb").read())
    capa1 = bytes(int(t, 16) for t in hexs).decode("latin-1")
    print(f"[1] hex -> ASCII          : {len(capa1)} caracteres")
    print(f"    muestra: {capa1[:60]!r}")

    # capa 2: Base45
    capa2 = base45_decode(capa1).decode()
    print(f"[2] Base45 -> texto       : {len(capa2)} caracteres")
    print(f"    muestra: {capa2[:60]!r}   (parece Base64)")

    # capa 3: Base64
    capa3 = base64.b64decode(capa2).decode()
    print(f"[3] Base64 -> código      : {len(capa3)} caracteres")
    print(f"    muestra: {capa3[:60]!r}   (Ook!: el 'mono escribiendo')")

    # capa 4: Ook! -> Brainfuck
    bf = ook_a_brainfuck(capa3)
    print(f"[4] Ook! -> Brainfuck     : {len(bf)} instrucciones")

    # capa 5: ejecutar Brainfuck
    flag = ejecutar_bf(bf).strip()
    print(f"[5] Brainfuck -> FLAG     : {flag}")

    open(BASE + "/work/programa.bf", "w").write(bf)
    open(BASE + "/work/capa3_ook.txt", "w").write(capa3)
    m = re.search(r"TRAMACTF\{[^}]*\}", flag)
    if m:
        open(BASE + "/flag.txt", "w").write(m.group(0) + "\n")


if __name__ == "__main__":
    main()
