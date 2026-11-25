#!/usr/bin/env python3
"""
Desafío «Eco Residual» — recuperación del token / flag
======================================================

El ejecutable `eco_residual` (ELF x86-64 PIE, stripped) reconstruye en la pila
una cadena de 32 bytes y la compara con la línea que introduce el usuario:

    token[i] = tabla_A[ tabla_B[i % 5] ] XOR clave[i]        i = 0..31

Ubicaciones en .rodata (vaddr == offset de fichero en este binario):

    0x2180  tabla_A  = "TRAMA\\0"            (6 bytes)
    0x2186  tabla_B  = 03 01 04 00 02        (5 bytes: permutación 3,1,4,0,2)
    0x21a0  clave    = 32 bytes XOR          ("/(#6(7$>..." en strings)

Detalle del desensamblado (main @ 0x123f):

    mov DWORD PTR [rsp+0xc], 0x54     ; variable muerta (luego compara con 999)
    loop 32 veces:
        calcula  i % 5  con la "magic number" 0xcccccccccccccccd
        al = tabla_A[ tabla_B[i % 5] ]
        al ^= clave[i]
        guarda al

El texto índice es siempre "MRATA" repetido (TRAMA permutado por 3,1,4,0,2),
es decir el token no es "TRAMA..." sino que cada letra se toma del índice que
nadie mira (de ahí la flag).

Uso:
    python3 recuperar_token.py [ruta_al_binario]
"""

import subprocess
import sys
from pathlib import Path

TABLA_A_OFF = 0x2180
TABLA_B_OFF = 0x2186
CLAVE_OFF = 0x21A0
LARGO = 0x20


def main() -> None:
    binario = Path(sys.argv[1] if len(sys.argv) > 1 else "eco_residual")
    if not binario.exists():
        sys.exit(f"[-] no existe {binario}")

    datos = binario.read_bytes()

    tabla_a = datos[TABLA_A_OFF:TABLA_A_OFF + 6]          # b"TRAMA\0"
    tabla_b = datos[TABLA_B_OFF:TABLA_B_OFF + 5]          # 03 01 04 00 02
    clave = datos[CLAVE_OFF:CLAVE_OFF + LARGO]

    print(f"[*] tabla_A = {tabla_a!r}")
    print(f"[*] tabla_B = {list(tabla_b)}")
    print(f"[*] clave   = {clave.hex()}")

    token = bytearray()
    for i in range(LARGO):
        letra = tabla_a[tabla_b[i % 5]]
        token.append(letra ^ clave[i])

    flag = token.decode()
    print(f"\n[+] token recalculado: {flag!r}")
    print(f"[+] largo: {len(flag)} (el buffer del binario es de 32 bytes + NUL)")

    # Verificación real contra el binario
    try:
        salida = subprocess.run(
            ["./" + binario.name],
            input=flag + "\n",
            capture_output=True,
            text=True,
            cwd=str(binario.parent),
        ).stdout
        ok = "Acceso restaurado" in salida
        print(f"[{'✓' if ok else '✗'}] el binario responde: "
              f"{'Acceso restaurado.' if ok else 'Eco inválido.'}")
    except OSError as e:
        print(f"[!] no se pudo ejecutar el binario: {e}")


if __name__ == "__main__":
    main()
