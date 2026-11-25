# PagoAustral — El bono fantasma

| Campo | Valor |
|---|---|
| Categoría | Criptografía — reutilización de keystream (two-time pad) |
| Evidencia | `PagoAustral.zip` (713 B) → `mi_sesion.txt`, `mi_token.txt`, `token_gerencia.txt` |
| Estado | ✅ Resuelto |
| Flag | `flag{ejemplo}` |

## Enunciado (resumen)

Una fintech sudamericana pierde un registro de sesión de prueba, **el token cifrado
de esa sesión** y **otro token que pertenecía a gerencia**. El encargado de seguridad
dice: *«están llenos de números y letras raras, imposible que alguien entienda eso»*.
Hay que examinar los tres archivos, identificar la falla en la protección de los
tokens y sacar la información de la sesión de gerencia.

## Evidencia

```
mi_sesion.txt     128 B   ASCII   usuario=demo;rol=cliente;plan=free;saldo=0;
                                 region=cl;token_ver=2;mfa=off................
mi_token.txt      257 B   hex     128 bytes cifrados
token_gerencia.txt 257 B  hex     128 bytes cifrados
```

Los tres miden **128 bytes útiles**. Eso ya sugiere que el token es el cifrado de
una cadena de sesión de la misma longitud.

## Análisis

1. `mi_sesion.txt` es texto plano y mide exactamente igual que los tokens →
   **tenemos un par (texto plano, cifrado)**.
2. Los dos tokens comparten los primeros 8 bytes y los últimos 16 (ver
   `C1 XOR C2`: empieza y termina en ceros) → **el mismo keystream cifró ambos**:
   no es un cifrado en bloque, es un cifrado de flujo con clave/nonce reutilizados.
3. Con un par conocido se recupera el keystream:

```
keystream  = C_mio XOR P_mio
P_gerencia = C_gerencia XOR keystream
```

El keystream resultante (`d71f93bf…`) es aleatorio y **no se repite**, lo que
descarta XOR con clave corta y confirma el cifrado de flujo.

## Solución

```python
p1 = open("work/mi_sesion.txt","rb").read()
c1 = bytes.fromhex(open("work/mi_token.txt").read().strip())
c2 = bytes.fromhex(open("work/token_gerencia.txt").read().strip())

keystream = bytes(a ^ b for a, b in zip(c1, p1))
p2 = bytes(a ^ b for a, b in zip(c2, keystream))
print(p2.decode())
```

Resultado:

```
usuario=gerencia;rol=interno;
nota=flag{ejemplo};
region=cl;mfa=on..............
```

```bash
python3 solucion/conocido_plano.py
```

## La falla

- **Reutilización de keystream**: el mismo cifrado de flujo (misma clave y mismo
  nonce) se usó para la sesión de prueba y para la de gerencia. Con dos textos
  cifrados bajo el mismo keystream, `C1 XOR C2 = P1 XOR P2`; y aquí, además, se
  filtró el texto plano de uno de ellos, así que la recuperación es directa.
- **Confiar en que «nadie va a mirar los archivos»**: el token no está atado a la
  sesión ni firmado; el paquete entregado incluía el par necesario para romperlo.
- El «bono fantasma» es la fila que alguien con la sesión de gerencia
  (`rol=interno`, `mfa=on`) podía aprobar sin que nadie lo notara.

## Flag

```
flag{ejemplo}
```

*«La gerencia reutilizó la llave y se fue de vacaciones.»*

## Archivos de la carpeta

| Ruta | Contenido |
|---|---|
| `PagoAustral.zip` | evidencia original |
| `flag.txt` | flag final |
| `CONTEXTO.md` | este writeup |
| `solucion/conocido_plano.py` | recupera el keystream y descifra el token de gerencia |
| `solucion/xor_sesion.py` | pruebas descartadas (XOR directo con la sesión y entre tokens) |
| `work/` | los tres archivos extraídos |
