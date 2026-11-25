# El Caleuche — Resolución del reto (TRAMA CTF)

**Fecha:** 2026-10-24
**Paquete:** `Caleuche.zip` (paquete 022 / «embarcación no identificada»)
**Resultado:** ✅ manifiesto recuperado

## Flag

```
flag{ejemplo}
```

## Material entregado

| Archivo | Rol |
|---|---|
| `manifiesto.enc` | 48 bytes = 3 bloques AES-256-CBC (contenido real) |
| `llave_sobre.rsa` | 256 bytes = llave AES-256 envuelta con RSA-2048 OAEP/SHA-256 |
| `iv.hex` | IV real del manifiesto → **el que sirve** |
| `iv_boya.hex` | IV de la boya QL-19 → **señuelo** (no pertenece al paquete) |
| `certificado_receptor.pem` | Llave pública del receptor legítimo (identifica la llave privada correcta) |
| `respaldo_turno_1..3.pem` | Tres llaves privadas RSA-2048; solo una es la del receptor |
| `nota_servilleta.txt` | `LLAVE-MAREA-1810` → **señuelo** (contraseña, no llave del sobre) |
| `bitacora.txt` | Declara el esquema: RSA-OAEP SHA-256 → AES-256-CBC + PKCS#7 |

## Cadena de resolución

1. **Identificar la llave privada correcta.** Se calculó la huella SHA-256 de la clave pública
   derivada de cada `respaldo_turno_N.pem` y se comparó con la de `certificado_receptor.pem`:

   | Llave | SHA-256 de la pública | ¿Coincide? |
   |---|---|---|
   | turno_1 | `426b3ced…a21f023` | ✗ |
   | **turno_2** | `566bf91666129776904d650e5f820f2b14d50639201936261ad7063866f30169` | **✓** |
   | turno_3 | `9a3088f2…43cfa1` | ✗ |
   | certificado | `566bf916…f30169` | — |

   Se confirmó además con el módulo RSA (`AF8876BEAA95AF4C…` idéntico).

2. **Desenvolver la llave simétrica** con `turno_2`:

   ```bash
   openssl pkeyutl -decrypt -inkey respaldo_turno_2.pem \
     -in llave_sobre.rsa -out llave_aes.bin \
     -pkeyopt rsa_padding_mode:oaep -pkeyopt rsa_oaep_md:sha256 -pkeyopt rsa_mgf1_md:sha256
   ```

   → 32 bytes: `d64b4d90302b2644a54d2edf4f0ba313d7051f2e56c284dec43faab4a0b31c08`

3. **Descifrar el manifiesto** con AES-256-CBC e `iv.hex`:

   ```bash
   openssl enc -d -aes-256-cbc \
     -K d64b4d90302b2644a54d2edf4f0ba313d7051f2e56c284dec43faab4a0b31c08 \
     -iv b1c7b41babee791c511e876020fad0f3 \
     -in manifiesto.enc -out manifiesto.txt
   ```

   Padding PKCS#7 válido y texto plano coherente → flag.

## Controles anti-señuelo (ejecutados)

- `turno_1` y `turno_3` contra `llave_sobre.rsa` → **fallan** (padding OAEP inválido).
- `LLAVE-MAREA-1810` como passphrase (`-pass pass:`) → **falla** (padding PKCS#7 inválido).
- `iv_boya.hex` con la llave correcta → descifra sin error de padding **pero corrompe el primer
  bloque** (001 `A 257 206 376 O 225 …`), confirmando que un IV erróneo solo destruye el bloque
  inicial en CBC; el texto queda ilegible. El IV correcto produce `TRAMACTF{El_C4l3uch3_…`.
- La nota de la servilleta **no** es una llave AES-256 (32 bytes) ni una llave RSA: el enunciado lo
  advierte («no consta en el manifiesto»).

## Artefactos generados (carpeta de trabajo)

`C:\Users\<usuario>\AppData\Local\Temp\opencode\caleuche\`
- `solve.sh` — comparación de huellas de claves públicas
- `step2.sh` — desenvolver `llave_sobre.rsa` → `llave_aes.bin`
- `step3.sh` — descifrar manifiesto → `manifiesto.txt`
- `controles.sh` — pruebas negativas (señuelos)
- `llave_aes.bin`, `manifiesto.txt` — resultados

Copia de los scripts y del manifiesto recuperado en esta misma carpeta (`scripts/`).

## Notas

- Todo el ejercicio es criptografía offline: no hubo objetivos de red ni servidores.
- El «patrón de la boya» (`iv_boya.hex`, registro de la sonda QL-19) es ruido deliberado.
