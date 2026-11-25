# Herramientas — índice de cheatsheets

Cada archivo resume los comandos que realmente se usan, no el manual completo.

| Archivo | Cubre |
|---|---|
| [`nmap.md`](nmap.md) | Descubrimiento, puertos, scripts NSE, evasión |
| [`web.md`](web.md) | Recon, fuzzing, SQLi, XSS, JWT, SSRF, XXE, SSTI, source maps |
| [`pwn.md`](pwn.md) | checksec, offsets, pwntools, format string, gadgets, SROP |
| [`reversing.md`](reversing.md) | file/strings, main sin símbolos, tablas, r2, Ghidra, GDB, VMs |
| [`stego.md`](stego.md) | Carving, metadatos, LSB, mosaicos, OOXML, audio, QR |
| [`forense.md`](forense.md) | Volatility, disco, tshark, Zeek, EVTX, YARA, timeline |
| [`crypto.md`](crypto.md) | César, Vigenère, XOR, RSA, hashes, AES, codificaciones |
| [`cracking.md`](cracking.md) | hashid, john, hashcat, hydra, zip2john y familia |
| [`ad.md`](ad.md) | AD: enumeración, Kerberos, BloodHound, ADCS, lateral |
| [`kali-wsl.md`](kali-wsl.md) | Cómo ejecutar todo esto en Kali WSL2 |

## Convención de cada cheatsheet

1. Qué señal indica usar esa herramienta.
2. Comando mínimo que funciona.
3. Variantes frecuentes en retos.
4. Siguiente paso según el resultado.
5. Guardrails aplicables.

## Aporte

Si descubres un comando que ahorra tiempo, agrégalo a la sección correspondiente
y anota la fecha en el `CONTEXTO.md` del objetivo donde lo usaste.
