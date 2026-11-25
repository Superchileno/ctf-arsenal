# Criptografía — de clásica a casera

## Identificar antes de atacar

```bash
# ¿Qué es?
file mensaje.txt
python - <<'PY'
import sys, collections
d = open(sys.argv[1],'rb').read() if len(sys.argv)>1 else b''
print("len", len(d), "entropía", round(len(set(d)).bit_length() and __import__('math').log2(len(set(d))),2))
PY

# Codificaciones frecuentes
base64 -d mensaje.b64
xxd -r -p mensaje.hex
python ../arsenal/ctf-arsenal decode mensaje.txt
```

## César / ROT

```bash
python ../arsenal/ctf-arsenal vigenere --caesar mensaje.txt
# o a mano: comparar con el prefijo esperado, p. ej. flag{ / PREFIJO{
```

## Vigenère

```bash
python ../arsenal/ctf-arsenal vigenere mensaje.txt --key COLINA
python ../arsenal/ctf-arsenal vigenere mensaje.txt --key COLINA --advance letters --subtract
```

Variantes que aparecen en retos:
- clave que **solo avanza con letras** (signos y dígitos no consumen clave);
- operación inversa (restar en vez de sumar);
- texto invertido antes de descifrar.

## XOR

```bash
# Clave repetida conocida
python ../arsenal/ctf-arsenal xor key mensaje.bin --key "clave"

# Par conocido (texto plano + cifrado) → keystream
python ../arsenal/ctf-arsenal xor known --plain p.txt --cipher c1.hex --target c2.hex

# Two-time pad: diff de dos cifrados
python ../arsenal/ctf-arsenal xor diff c1.bin c2.bin

# Fuerza bruta de clave de 1 byte
python ../arsenal/ctf-arsenal xor brute mensaje.bin
```

## Cifradores caseros

1. Leer el script que cifra.
2. Reimplementar la inversa en Python, paso por paso.
3. Validar con **round-trip**: cifrar un texto conocido y comparar con el original.
4. Solo entonces aplicarlo al texto del reto.

Patrones vistos: XOR + rotación + swap de nibbles; máscara dependiente del índice;
Base64 antes/después del XOR.

## RSA

```bash
# Datos
openssl rsa -pubin -in pub.pem -text -noout
python -c "import sympy;print(sympy.factorint(<n>))"

# Ataques frecuentes
# - e=3 y mensaje corto → raíz cúbica entera
# - n compartido entre dos claves → gcd(n1,n2)
# - p y q muy cercanos → Fermat
# - d pequeño → Wiener
```

```python
python -c "from gmpy2 import iroot;print(iroot(123456789,3))"
```

## Hashes

```bash
hashid hash.txt
hashcat --example-hashes | grep -i -A3 'sha256'
john --format=raw-sha256 hash.txt --wordlist=rockyou.txt
```

## Bloques y streams

```bash
# AES-CTR / CBC con openssl
openssl enc -d -aes-256-ctr -K <hex> -iv <hex> -in cifrado.bin -out plano.bin
openssl enc -d -aes-256-cbc -K <hex> -iv <hex> -in cifrado.bin -out plano.bin

# Verificar un SHA-256 esperado
sha256sum plano.bin
```

## Codificaciones encadenadas

| Codificación | Señal | Herramienta |
|---|---|---|
| Base64 | `A-Za-z0-9+/=` | `base64 -d` |
| Base64url | `-_` en vez de `+/` | `python base64.urlsafe_b64decode` |
| Base45 | alfabeto QR | `base45` (pip) |
| ASCII85 | `~>` al final | `base64.a85decode` |
| Hex | solo `0-9a-f` | `xxd -r -p` |
| Ook! / Brainfuck | símbolos `!?` o `+-<>` | intérprete propio |
| gzip / deflate | `1f 8b` / `78 9c` | `gzip -d`, `zlib.decompress` |

## Validación obligatoria

Antes de declarar que se encontró la respuesta:

- [ ] El texto decodificado es legible o tiene forma de flag.
- [ ] Se puede volver a cifrar y obtener el original (round-trip).
- [ ] Se descartaron al menos dos variantes plausibles (señuelos).
