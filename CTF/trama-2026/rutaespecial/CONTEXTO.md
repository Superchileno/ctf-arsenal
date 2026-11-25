# Desafío 17 — El Cielo Falsificado (ruta espectral)

| Campo | Valor |
|---|---|
| Categoría | reversing / ofuscación aritmética |
| Dificultad | media |
| Puntos | — |
| Estado | ✅ resuelto |
| Vector (flag) | `flag{ejemplo}` |

## Enunciado

> **El Cielo Falsificado** — Un astrónomo aseguró que alguien había cambiado las estrellas de lugar […]
> Durante una exhibición en el planetario, los visitantes observaron una constelación que no aparecía en
> ningún registro. Sus estrellas formaban una trayectoria imposible […]
> El archivo contenía un pequeño programa que representaba una extraña ruta entre puntos luminosos.
> Al ejecutarlo, solicitaba un vector. Los investigadores probaron distintas combinaciones, pero el
> resultado siempre era el mismo: «Trayectoria perdida». […]
> Analiza el programa y descubre qué vector permite sincronizar la trayectoria.

## Reconocimiento

```
ruta_espectral: ELF 64-bit LSB pie executable, x86-64, dynamic, stripped
SHA256 3fde2a9836c8e1804f097049d88c3cda25717ff951f5652876203292f2f9fd63
```

Ejecución local:

```
Vector: Trayectoria perdida.
```

Cadenas propias (`strings`): `Vector: `, `Trayectoria sincronizada.`, `Trayectoria perdida.`

`main` está en `0x1237` (PIE, base desplazada en ejecución). No hay flag en claro en el binario: el
programa solo valida un vector de 36 caracteres y muestra uno u otro mensaje.

## Análisis

### Estructura de `main`

```c
fwrite("Vector: ", 8, 1, stdout);
fgets(buf, 0x60, stdin);
buf[strcspn(buf, "\n")] = 0;
*(uint32_t*)(rsp+5) = 0x414e4143;   // "CANA"
*(uint32_t*)(rsp+8) = 0x37344c41;   // "AL47"  (se solapa en la 'A')
if (strlen(buf) != 0x24) { puts("Trayectoria perdida."); return; }   // 36 bytes
...
```

Los dos dwords construyen la clave `CANAL47` en la pila, justo antes del buffer de entrada:

```
rsp+5 .. rsp+11 : 43 41 4e 41 4c 34 37   ->  "CANAL47"
rsp+0x10        : buffer de 36 bytes (fgets)
```

### Bucle de validación (36 iteraciones)

Por cada `i` de 0 a 35:

```
in_idx  = (7*i) mod 36                  ; magia 0xE38E38E38E38E38F (división por 36)
key_idx = i mod 7                        ; magia 0x2492492492492493 (división por 7)

s  = entrada[in_idx] ^ clave[key_idx]
s  = (s + i) & 0xff
s  = rol8(s, rot1(i))                    ; rot1: 1,2,3,1,2,3,...   (secuencia 0xAAAA…)
s ^= ((0x41 + 0x13*i) ^ TA[i]) & 0xff
s ^= rol8(TB[(7+5*i) & 31] ^ TB[(3+9*i) & 31] ^ ((0x3d*i) & 0xff), rot2(i))
                                         ; rot2: 1,2,3,4,5,1,2,... (secuencia 0xCCCC…)
s ^= 0xa7
r13 |= s                                 ; al final se prueba r13b == 0
```

Tablas en `.rodata` (el offset de fichero coincide con la vaddr porque `.rodata` está en `0x2000`):

| Tabla | Dirección | Tamaño | Uso |
|---|---|---|---|
| `T3` | `0x2140` | 36 B | comparación final XOR con la entrada (inalcanzable, ver abajo) |
| `TB` | `0x2180` | 32 B | mezcla con índices `(7+5i)&31` y `(3+9i)&31` |
| `TA` | `0x21a0` | 36 B | mezcla con `(0x41+0x13i)` |

### Por qué se puede resolver byte a byte

`(7*i) mod 36` es una **permutación** de `0..35` (gcd(7,36)=1): cada byte de la entrada se usa en
exactamente una iteración. La condición de esa iteración solo depende de ese byte (los demás términos
son constantes), y es una ecuación XOR/rotación sobre 8 bits. Por tanto, para cada `i` basta probar los
256 valores posibles: hay **solución única** en todas las iteraciones.

### Validación con GDB (imprescindible)

Las secuencias de división mágica no son las habituales (`hi & ~1 + hi>>1`, `hi & ~3 + hi>>2`), así que
emularlas "a ojo" lleva a errores. La traza real con `gdb` (ASLR desactivado, base `0x555555554000`)
permitió fijar los valores exactos. Breakpoints usados: `0x1380` (índice de entrada), `0x13af`
(rotación 1), `0x13c6` (índices de `TB`), `0x13f8` (rotación 2) y `0x13fe` (estado previo al XOR final).

Ejemplo para `i = 1` con entrada `'A'`:

```
IDX  i=1 rcx=7  inbyte=0x41        ; entrada[7]
ROT1 i=1 cl=2  sil=0x01            ; (0x41 ^ 'A' + 1) = 0x01
TB   i=1 rdx=12 rax=12 r11=0x3d    ; TB[12]^TB[12]^0x3d
ROT2 i=1 cl=2 r15b=0x3d
PRE  i=1 esi=0x83                  ; 0x04 ^ 0x73 ^ 0xf4
```

`0x83 ^ 0xa7 = 0x24`, que coincide con el valor observado en `0x1401` (`esi=0x24`). Este contraste
detectó que faltaba el `add esi, edi` (suma de `i`) antes de la primera rotación en la primera versión
del emulador.

### Señuelo: la segunda etapa es código muerto

Tras el bucle hay un checksum sobre `TB`:

```
r9b = 0x52 XOR (rol8(TB[j], (j%7)+1), j=0..31)
si r9b != 0x24  -> salta la comparación final
```

Calculado: `0x52 ^ Σ = 0xf5 ≠ 0x24` → **nunca** se ejecuta la comparación `entrada[i] ^ T3[i]`.
`T3` es un señuelo de 36 bytes no imprimibles (incluye `0x0a`, imposible de teclear con `fgets`).
Perseguir `T3` lleva a un callejón sin salida; la validación real es solo el bucle principal.

## Solución (pasos reproducibles)

```bash
# 1) El script lee las tablas del propio binario y resuelve el vector
python solucion/resolver_vector.py ruta_espectral
# vector hex : 5452414d414354467b6c615f727574615f676972615f62616a6f5f656c5f727569646f7d
# vector     : flag{ejemplo}

# 2) Verificación contra el binario
printf 'flag{ejemplo}\n' | ./ruta_espectral
# Vector: Trayectoria sincronizada.
```

## Flag

```
flag{ejemplo}
```

## Evidencia y artefactos

| Ruta | Contenido |
|---|---|
| `ruta_espectral` | Binario entregado (14.496 B) |
| `solucion/resolver_vector.py` | Resuelve el vector leyendo `TA`/`TB` del propio ELF |
| `work/trace.gdb` | Traza de `esi`/`r13` por iteración |
| `work/trace2.gdb` | Traza detallada de índices, rotaciones y tablas |
| `work/inp_aa.bin` | Entrada de 36 `'A'` usada para instrumentar |
| `work/payload_emul.bin` | Primer intento de vector (emulador incompleto; falla) |
| `flag.txt` | Vector/flag del reto |

## Lecciones / notas

- Las **divisiones por constantes** del compilador (`mulhi` + desplazamientos) se deben emular
  literalmente; reconocerlas "por intuición" introduce errores sutiles.
- Un **detalle de una instrucción** (`add esi, edi`) cambia por completo la solución; la traza con
  breakpoints y la comparación de valores intermedios es la forma fiable de validar el emulador.
- **Código muerto como señuelo**: un checksum que nunca cuadra desvía hacia una tabla cifrada que nunca
  se usa. Antes de atacar una comparación, comprobar si es alcanzable.
- Cuando el índice es una permutación y la condición es byte a byte, el espacio de búsqueda es 36 × 256,
  no 256³⁶.
- El vector resultante es la flag: una frase alusiva al enunciado («la ruta gira bajo el ruido»),
  coherente con la historia del mapa que muestra dónde deberían estar las cosas.

## Backups

| Archivo | Backup |
|---|---|
| `ctf/CONTEXTO_CTF.md` (índice) | `ctf/backups/CONTEXTO_CTF.md.20261023-184511` |
