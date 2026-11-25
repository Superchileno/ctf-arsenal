# Reversing — entender un binario

## Primeras cinco preguntas

```bash
file ./bin                  # arquitectura, estático/dinámico, stripped
readelf -h ./bin            # entry point
checksec --file=./bin       # PIE, NX, canary, RELRO
strings -n 5 ./bin | less   # mensajes, rutas, claves
ltrace ./bin; strace -f ./bin
```

## Localizar `main` sin símbolos

```bash
python ../skills/reversing-obfuscated-binaries-and-vms/scripts/find_main.py ./bin
objdump -d -Mintel ./bin | sed -n '/<_start>/,/^$/p'
```

`_start` llama a `__libc_start_main(main, …)`; el primer argumento es `main`.

## Tablas en `.rodata`

```bash
readelf -SW ./bin | grep -E '\.rodata|\.data'
python ../skills/reversing-obfuscated-binaries-and-vms/scripts/extract_tables.py ./bin
xxd -s 0x2000 -l 256 ./bin
```

Patrón típico: `token[i] = TABLA[otra_tabla[i]] ^ clave[i]`.

## Radare2

```bash
r2 -A ./bin
> afl                  # listar funciones
> s main; pdf          # desensamblar main
> axt @ str.flag       # referencias cruzadas
> /R pop rdi           # buscar gadgets
> iz                   # strings en data
```

## Ghidra (interfaz)

1. New Project → importar binario → auto-analizar.
2. Buscar `main` en el Symbol Tree; renombrar variables.
3. Usar Decompiler para leer la lógica y exportar el pseudocódigo al writeup.

## GDB con pwndbg

```bash
gdb -q ./bin
> set disassembly-flavor intel
> break *main
> run
> ni / si            # paso a paso
> info registers
> x/20gx $rsp
> vmmap              # mapas de memoria (pwndbg)
> telescope $rsp 20
```

## Ofuscación aritmética

- `div`/`mul` con constantes mágicas → división por constante; validar en GDB con
  los valores reales de los registros.
- Permutaciones del tipo `(a*i + b) mod n` → comprobar si son biyección.
- Condición byte a byte → fuerza bruta de 256 valores por índice con oráculo.

```bash
python ../skills/reversing-obfuscated-binaries-and-vms/scripts/oracle_bruteforce.py ./bin
```

## VMs de bytecode

1. Localizar el dispatcher (`switch` o tabla de saltos).
2. Extraer el bytecode (sección, `.rodata` o entrada).
3. Reimplementar el intérprete en Python.
4. Ejecutar y comparar con el binario original.

## Herramientas auxiliares

| Necesidad | Herramienta |
|---|---|
| Diff de binarios | `radiff2 -C a b` |
| Firmas y tipos | `rizin`, `cutter` |
| .NET | `dnSpy`, `ilspycmd` |
| Python empaquetado | `pyinstxtractor`, `decompyle3` |
| Go/Rust | `redress`, `goresym`, `rustfilt` |
| Android | `jadx`, `apktool`, `frida` |
