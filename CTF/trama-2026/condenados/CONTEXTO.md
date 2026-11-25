# Desafío 19 — La Lotería de los Condenados

| Campo | Valor |
|---|---|
| Categoría | crypto / Base64 + XOR con clave repetida |
| Dificultad | fácil |
| Puntos | — |
| Estado | ✅ resuelto |
| Flag | `flag{ejemplo}` |

## Enunciado

> **La Lotería de los Condenados — El premio que nadie quería ganar** — En una sede vecinal de
> Valparaíso decidieron organizar una rifa para arreglar el techo. […] Encontraron una urna que llevaba
> décadas guardada […]. A medianoche, los boletos comenzaron a mostrar inscripciones extrañas. Un
> exsecretario había anotado que **solo un resultado correspondía al sorteo verdadero**; los demás
> provenían de pruebas, trampas y reclamos […].
>
> Tu misión: investiga el registro `la_urna.txt`, distingue el mensaje auténtico de los señuelos y
> recupera el único premio que realmente importa.
>
> Archivo adjunto: `Loteria_Condenados.zip`. No necesitas servicios externos.

## Reconocimiento

`Loteria_Condenados.zip` (1.821 B, SHA256 `bb47a5ad...dc3915c3`) contiene:

| Archivo | Tamaño | Notas |
|---|---|---|
| `LEEME.txt` | 322 B | Contexto: 10 boletos, solo uno auténtico |
| `la_urna.txt` | 2.543 B | Transcripción de los 10 boletos y sus mensajes |

`la_urna.txt` incluye una pista clave en el párrafo 8:

> Todos llevaban mensajes imposibles de leer y la misma marca de archivo, **`nodo_trama_2026`**, que el
> exsecretario utilizaba para cerrar las copias digitales de los tickets. […] esa marca se repetía en
> cada registro y era **necesaria para revisarlos**.

Cada boleto trae un mensaje con pinta de Base64 (alfabeto `A-Za-z0-9+/`, con y sin relleno `=`):

```
Boleto 01: KxwQDn8aHUEMAy1X
Boleto 02: Iw4XTywBFxMZBH9eURJGHAAcBjIV
Boleto 03: Oj0lIh43JicWBDNtXkdbCx0LMC4BFz4eCABBUV5fARI=
...
```

## Análisis

La "marca de archivo" es literalmente la **clave de un XOR repetido**. El proceso por boleto es:

1. Decodificar Base64.
2. Aplicar XOR byte a byte con `nodo_trama_2026` repetida (15 bytes de periodo).
3. Leer el texto resultante.

Resultado de los diez boletos:

| Boleto | Texto en claro | ¿Auténtico? |
|---|---|---|
| 01 | `Esta no abre` | señuelo |
| 02 | `Mas suerte la proxima` | señuelo |
| **03** | **`flag{ejemplo}`** | ✅ **flag** |
| 04 | `Te falta, mortal` | señuelo |
| 05 | `Error: no era esta` | señuelo |
| 06 | `Nop, no soy yo` | señuelo |
| 07 | `Frio. Muy frio.` | señuelo |
| 08 | `No era este numero` | señuelo |
| 09 | `Numero equivocado` | señuelo |
| 10 | `Tibio, tibio... frio otra vez` | señuelo |

Todos los mensajes decodifican a texto legible con la misma clave: la diferencia es el contenido. Solo
el boleto **03** contiene la estructura de flag. No hay que "adivinar" más: el enunciado y la nota de
inventario ya advierten que nueve son bromas y uno es el verdadero.

Notas:

- La longitud de cada mensaje varía (9–28 bytes), por lo que el XOR cíclico no siempre agota la clave;
  no importa, el descifrado es directo.
- No hay trampa de doble codificación ni cifrado adicional: los señuelos son mensajes plausibles para
  desanimar al que prueba un solo boleto y se detiene.

## Solución (pasos reproducibles)

```bash
unzip Loteria_Condenados.zip -d work/
python solucion/decodificar_boletos.py work/la_urna.txt
# Boleto 03: flag{ejemplo}  <-- FLAG
```

Implementación mínima:

```python
import base64
msg = "Oj0lIh43JicWBDNtXkdbCx0LMC4BFz4eCABBUV5fARI="
key = b"nodo_trama_2026"
claro = bytes(c ^ key[i % len(key)] for i, c in enumerate(base64.b64decode(msg)))
print(claro)   # b'flag{ejemplo}'
```

## Flag

```
flag{ejemplo}
```

## Evidencia y artefactos

| Ruta | Contenido |
|---|---|
| `Loteria_Condenados.zip` | Evidencia entregada (1.821 B) |
| `work/LEEME.txt` | Contexto del reto |
| `work/la_urna.txt` | Transcripción de los 10 boletos |
| `solucion/decodificar_boletos.py` | Decodifica los 10 boletos y marca la flag |
| `flag.txt` | Flag del reto |

## Lecciones / notas

- Las pistas narrativas ("marca de archivo", "necesaria para revisarlos") describen el esquema
  criptográfico: Base64 + XOR con clave repetida.
- En retos con "un auténtico entre señuelos", conviene automatizar la decodificación de **todos** los
  candidatos y buscar la estructura de flag (`TRAMACTF{`), en lugar de probar de a uno.
- XOR con clave repetida es trivialmente reversible; la "seguridad" aquí era solo la apariencia del
  texto codificado.

## Backups

| Archivo | Backup |
|---|---|
| `ctf/CONTEXTO_CTF.md` (índice) | `ctf/backups/CONTEXTO_CTF.md.20261023-185959` |
