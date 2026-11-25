# El Chino se pierde en el Cajón del Maipo: Misión Fotito

| Campo | Valor |
|---|---|
| Categoría | Criptografía — inversión + Vigenère con clave repetida |
| Artefacto | `interceptacion.txt` (674 B) |
| Estado | ✅ Resuelto |
| Flag | `flag{ejemplo}` |

## Enunciado (resumen)

Parodia del caso del «Chino Orellana» (julio 2026): salió de un carrete rumbo a las
Termas de Colina, lo sorprendió una nevazón y quedó aislado en el Cajón del Maipo.
Meses después circula un supuesto **registro de radio** con la transmisión
desordenada por la nieve y las palabras bajo **una clave repetida**. Hay que
recuperar el mensaje de `interceptacion.txt`.

## El archivo

```
TRAMA CTF / REGISTRO DE RADIO SIMULADO
ARCHIVO: REFUGIO-06 / MISION FOTITO
ESTADO: INTERFERENCIA EN LA SENAL
DESTINO REGISTRADO: TERMAS DE COLINA

MENSAJE_INTERCEPTADO:
}0e0t_4pu_e0x_01mi5_0p1hp_t3{QHEAZICH .QITCQST NH VP GQMNLPIS SBV J SXEVV LWDAU .WECH AAC CCR SBUTIH

NOTAS DE CALIBRACION
[1] "La ventisca dio vuelta el mensaje entero, de la ultima marca a la primera".
[2] "Para abrirlo, usa solo la ultima palabra del destino como llave".
[3] "La llave se repite de principio a fin; solo avanzas al leer letras A-Z".
[4] "Numeros, espacios, puntos, llaves y guiones bajos no cambian".
```

## Las cuatro pistas, una por una

| Pista | Interpretación |
|---|---|
| [1] «dio vuelta el mensaje entero» | invertir la cadena completa (`[::-1]`) |
| [2] «última palabra del destino» | destino `TERMAS DE COLINA` → clave **`COLINA`** |
| [3] «clave repetida; avanzas solo con A-Z» | Vigenère con clave cíclica; el índice **solo** avanza al consumir una letra |
| [4] «números, espacios, puntos, llaves y guiones bajos no cambian» | los no alfabéticos se copian tal cual y **no** consumen clave |

## Solución

```python
cifrado = "}0e0t_4pu_e0x_01mi5_0p1hp_t3{QHEAZICH .QITCQST NH VP GQMNLPIS ..."
volteado = cifrado[::-1]

# Vigenère: descifrar restando la clave, avanzando solo en letras A-Z
salida, k = [], 0
for c in volteado:
    if c.isascii() and c.isalpha():
        base = ord('A') if c.isupper() else ord('a')
        d = (ord(c) - base - (ord('COLINA'[k % 6]) - ord('A'))) % 26
        salida.append(chr(base + d)); k += 1
    else:
        salida.append(c)
```

Resultado tras invertir:

```
HITUBS RCC CAA HCEW. UADWL VVEXS J VBS SIPLNMQG PV HN TSQCTIQ.
flag{ejemplo}
```

Resultado descifrado:

```
FUIMOS POR UNA FOTO. HABIA NIEVE Y NOS QUEDAMOS EN UN REFUGIO.
flag{ejemplo}
```

## Verificación de hipótesis

El script prueba las tres interpretaciones razonables y solo una produce texto
legible — descartando la ambigüedad de «clave repetida»:

| Variante | Resultado |
|---|---|
| XOR con `COLINA` | binario ilegible |
| Vigenère sumando | `JWECOS TQN KNA JQPE...` (basura) |
| **Vigenère restando** | ✅ `FUIMOS POR UNA FOTO...` + flag |

## Explotación

```bash
python3 solucion/resolver.py
```

## Flag

```
flag{ejemplo}
```

*«El Chino subió por una foto»* — coherente con la excusa original del caso.

## Archivos de la carpeta

| Ruta | Contenido |
|---|---|
| `interceptacion.txt` | artefacto original |
| `flag.txt` | flag final |
| `CONTEXTO.md` | este writeup |
| `solucion/resolver.py` | invierte, prueba XOR/Vigenère y extrae la flag |
