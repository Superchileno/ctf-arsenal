# Frecuencia Muerta / Pulso ORION — CONTEXTO

**Reto:** `pulso_mantenimiento` (reversing / criptografía embebida)
**Fecha de análisis:** 2026-10-24
**Archivo:** `pulso_mantenimiento` (14.496 B, ELF 64-bit PIE, dinámico, stripped)
**SHA-256:** `fa8acae4298f469648d11e4b88ae400d3ac16a65761a445051e93cd33eb45d94`

| Dato | Valor |
|---|---|
| Flag | ✅ `flag{ejemplo}` |
| Entrada que activa el mecanismo | exactamente la flag (se compara con `strcmp`) |
| Respuesta correcta | `Mantenimiento habilitado.` |
| Respuesta incorrecta | `Pulso no reconocido.` |

---

## 1. Reconocimiento

```
$ file pulso_mantenimiento
ELF 64-bit LSB pie executable, x86-64, dynamically linked, stripped

$ checksec
Partial RELRO | No canary | NX enabled | PIE enabled
```

Strings (`strings -n 4`):

| Dirección | Cadena |
|---|---|
| `0x2004` | `\x1b[1;31m` (rojo) |
| `0x2025` | `\x1b[0m` (reset) |
| `0x202b` | `Mantenimiento habilitado.` |
| `0x2045` | `Pulso no reconocido.` |
| `0x205a` | `ORION-03` |
| `0x2063` | `Comando: ` |
| `0x206d` | `\n` (para `strcspn`) |
| `0x2070`-`0x2109` | arte ASCII del "PULSO ORION" |
| `0x2120`-`0x2147` | **blob cifrado de 40 bytes** |

Importa: `fgets`, `strcspn`, `strcmp`, `puts`, `fwrite`. Nada de `system`.

## 2. `main` (`0x11f8`) — estructura

1. **Deriva una clave de 4 palabras** a partir de la cadena `ORION-03` (bucle de 4 iteraciones,
   `0x1216`-`0x1267`):

   ```
   ptr_i   = 0x205a + 4*(i & 1)        -> alterna "ORIO" / "N-03"
   word_i  = *(uint32*)ptr_i           -> carga little-endian
   key[i]  = word_i ^ (0x11111111 * i) ^ 0x65F2A4C0
   ```

   Resultado:

   | i | origen | key |
   |---|---|---|
   | 0 | `ORIO` (`0x4F49524F`) | `0x2ABBF68F` |
   | 1 | `N-03` (`0x33302D4E`) | `0x47D3989F` |
   | 2 | `ORIO` | `0x0899D4AD` |
   | 3 | `N-03` | `0x65F1BABD` |

2. **Descifra** el blob de `.rodata` (`0x2120`, 40 bytes = 5 bloques de 8) con una variante de
   **TEA de 32 rondas**, `delta = 0x9E3779B9`, `sum` inicial `0xC6EF3720`, y **clave indexada por
   `(sum >> 11) & 3`** (estilo XXTEA) en lugar de los índices fijos de TEA clásico:

   ```c
   sum = 0xC6EF3720;
   do {
       v1 -= ((((v0 << 4) ^ (v0 >> 5)) + v0) ^ (sum + key[(sum >> 11) & 3]));
       sum += 0x61C88647;                     // sum -= delta
       v0 -= ((((v1 << 4) ^ (v1 >> 5)) + v1) ^ (sum + key[sum & 3]));
   } while (sum != 0);
   ```

3. Escribe los 40 bytes descifrados en `rsp+0x20`, `movb $0x0,0x48(%rsp)` (terminador) y
   **`fgets` + `strcspn` + `strcmp`** contra lo tecleado.

4. `puts` de la cadena que corresponda y `return (*(int*)&var_0c == 0x3e7)` — la variable vale
   `0x54` y nunca se modifica, así que siempre devuelve 0 (detalle irrelevante).

## 3. Descifrado

El resultado del descifrado **es la propia flag**:

```
flag{ejemplo}
flag{ejemplo}\0\0\0\0\0\0\0\0\0
```

Script: `solucion/decrypt.py` (implementa la derivación de clave y el descifrado tal cual el
desensamblado, leyendo el blob desde `.rodata` en el offset `0x2120`).

## 4. Verificación

```bash
printf 'flag{ejemplo}\n' | ./pulso_mantenimiento
# Comando: Mantenimiento habilitado.        [rc=0]

printf 'flag{ejemplo}\n' | ./pulso_mantenimiento
# Comando: Pulso no reconocido.             [rc=0]
```

Pruebas adicionales: `ORION-03` como entrada **no** funciona (`Pulso no reconocido.`) — esa
cadena solo es la semilla de la clave.

## 5. Archivos

| Ruta | Contenido |
|---|---|
| `pulso_mantenimiento` | binario original |
| `flag.txt` | la flag |
| `solucion/decrypt.py` | derivación de clave + descifrado TEA-like |
| `solucion/orden.txt` | orden descifrada |
| `backups/pulso_mantenimiento.20261024-181000` | copia previa a cualquier manipulación |

## 6. Historial

- **2026-10-24** — `file`/`checksec`/`strings`. Localizado `main` en `0x11f8` vía
  `__libc_start_main` desde `_start`. Interpretados los dos bucles: derivación de clave desde
  `ORION-03` (XOR con `0x11111111*i` y `0x65F2A4C0`) y descifrado TEA-like de 40 bytes con clave
  indexada por `sum`. Obtenida la flag `flag{ejemplo}` y validada contra el
  binario («Mantenimiento habilitado.»).
