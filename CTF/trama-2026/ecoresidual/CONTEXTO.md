# Eco Residual — CANAL 03

| Campo | Valor |
|---|---|
| Categoría | Reversing de binario (ELF x86-64) |
| Artefacto | `eco_residual` (14 496 bytes, ELF 64-bit PIE, stripped) |
| SHA-256 | `62c26646cbdaefdf34de1196bb0d9842e0e5bb445cc151bbdf351c9bcf589850` |
| Estado | ✅ Resuelto |
| Flag | `flag{ejemplo}` |

## Enunciado (resumen)

Tras la operación «Vector Fantasma» el Canal 03 dejó de emitir. En los sistemas
abandonados apareció un ejecutable sin inventario ni código fuente. Al probarlo,
**sigue respondiendo pero espera algo**: cada intento fallido devuelve el mismo
mensaje. Hay que averiguar **qué necesita para restaurar el acceso al canal**.

Al ejecutarlo:

```
   .-''''-.   .-''''-.   .-''''-.
 .'  ECO  '. .'  ECO  '. .'  ECO  '.
:  .----.  ::  .----.  ::  .----.  :
 '._.__._.'  '._.__._.'  '._.__._.'

+-----------------------------------+
|  .::  // CANAL 03 ::. |
|       ))      ))      ))          |
+-----------------------------------+
Token recuperado: Eco inválido.
```

Cualquier entrada produce `Eco inválido.`; solo el token correcto imprime
`Acceso restaurado.`

## Reconocimiento

```bash
file eco_residual
# ELF 64-bit LSB pie executable, x86-64, dynamically linked, stripped

checksec --file=eco_residual
# Partial RELRO | No canary | NX | PIE | No symbols
```

`strings` ya delata el esquema: junto a los textos del banner aparecen
`TRAMA` y una secuencia de bytes «basura» `/(#6(7$>`, `< 0((`, `,=3"/`,
`;*3$"` → típico de una **clave XOR** almacenada en `.rodata`.

Al ser *stripped*, `main` se localiza en `_start` (`lea rdi,[rip+0x164]` con
`rsi=argc`, `rdx=argv`): **main @ `0x123f`**.

## Ingeniería inversa

### Estructura de `main` (0x123f)

```asm
123f: push rbx
1240: sub  rsp, 0x90
1247: mov  DWORD PTR [rsp+0xc], 0x54      ; contador muerto (luego se compara con 999)
124f: lea  rsi, [rsp+0x10]                ; buffer destino del token (32 bytes)
1259: lea  r10, [rip+0xf20]               ; 0x2180 -> tabla_A ("TRAMA")
1260: lea  r9,  [rip+0xf1f]               ; 0x2186 -> tabla_B (índices)
1267: movabs r8, 0xcccccccccccccccd       ; magic para calcular i % 5
1271: lea  rdi, [rip+0xf28]               ; 0x21a0 -> clave XOR (32 bytes)

1280: loop:
      mov  rax, rcx
      mul  r8                             ; rdx:rax = i * magic
      mov  rax, rdx
      shr  rax, 2
      and  rdx, -4
      add  rdx, rax
      mov  rax, rcx
      sub  rax, rdx                       ; rax = i % 5
      movzx eax, BYTE PTR [r9+rax]        ; tabla_B[i % 5]
      movzx eax, BYTE PTR [r10+rax]       ; tabla_A[ tabla_B[i % 5] ]
      xor  al, BYTE PTR [rdi+rcx]         ; XOR clave[i]
      mov  BYTE PTR [rsi], al
      inc  rcx
      inc  rsi
      cmp  rcx, 0x20
      jne  loop
12b7: mov  BYTE PTR [rsp+0x30], 0         ; NUL
      ...                                 ; banner
1308: lea  rdi, [rsp+0x50]                ; buffer de entrada (0x40)
1319: call fgets
1332: call strcspn(..., "\n")             ; quita el salto de línea
1344: call strcmp(entrada, token)
1359: cmove rdi, "Acceso restaurado."     ; si coincide
1370: ...                                 ; return (var == 999 ? 1 : 0) -> siempre 0
```

### Datos en `.rodata`

```
0x2180  54 52 41 4d 41 00        "TRAMA\0"          <- tabla_A
0x2186  03 01 04 00 02           permutación         <- tabla_B
0x21a0  19 00 00 19 00 0e 06 07 2f 28 23 36 28 37 24 3e   <- clave XOR (32 B)
0x21b0  0d 30 21 24 12 3c 20 30 28 28 0d 2c 3d 33 22 2f
```

El token se genera así:

```
token[i] = "TRAMA"[ tabla_B[i % 5] ] XOR clave[i]
```

Con `tabla_B = {3,1,4,0,2}` el texto índice queda **`MRATA`** repetido en vez de
`TRAMA`: el binario no espera la palabra «TRAMA», espera la misma palabra
**leída por los índices** de la tabla de permutación. Esa es justamente la pista
de la flag.

## Solución

```bash
python3 solucion/recuperar_token.py
```

```
[*] tabla_A = b'TRAMA\x00'
[*] tabla_B = [3, 1, 4, 0, 2]
[*] clave   = 19000019000e06072f2823362837243e0d302124123c203028280d2c3d33222f

[+] token recalculado: 'flag{ejemplo}'
[+] largo: 32 (el buffer del binario es de 32 bytes + NUL)
[✓] el binario responde: Acceso restaurado.
```

Verificación directa:

```bash
$ echo 'flag{ejemplo}' | ./eco_residual
...
Token recuperado: Acceso restaurado.
```

## Detalles / trampas

- **No hay canary ni símbolos**: no es un reto de pwn (no hay buffer overflow
  explotable de forma útil); el buffer de entrada es de 64 bytes y el token de 32.
- La comparación final `cmp DWORD PTR [rsp+0xc], 0x3e7` (999) es **código
  muerto**: la variable se inicializa a `0x54` y nunca se modifica, así que el
  programa siempre devuelve 0 aunque el token sea correcto. El éxito se detecta
  por el texto `Acceso restaurado.`, no por el código de salida.
- La cadena correcta mide **exactamente 32 caracteres**; escribir una variante
  de 33 (p. ej. añadiendo una letra) ya falla el `strcmp`.
- El «índice» de la tabla es el concepto central: `i % 5` calculado con
  multiplicación modular (`0xcccccccccccccccd`) en vez de una instrucción `div`.

## Flag

```
flag{ejemplo}
```

*«Los índices que nadie miró»* — el token solo aparece si se leen las letras de
`TRAMA` en el orden 3,1,4,0,2 en lugar del orden natural.

## Archivos de la carpeta

| Ruta | Contenido |
|---|---|
| `eco_residual` | artefacto original (ELF) |
| `CONTEXTO.md` | este writeup |
| `flag.txt` | flag final |
| `solucion/recuperar_token.py` | recalcula el token y lo valida contra el binario |
| `work/desensamblado.txt` | `objdump -d -M intel` completo |
| `work/rodata.txt` | volcado de `.rodata` con las tablas y la clave |
