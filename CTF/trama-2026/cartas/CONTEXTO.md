# Desafío 05 — Cartas (Mitos y Leyendas: la lámina sin número)

| Campo | Valor |
|---|---|
| Categoría | Crypto / sustitución de glifos (catálogo de imprenta, hexadecimal) |
| Estado | ✅ Resuelto |
| Evidencia | `Cartas.zip` (1.699 B, SHA256 `8C4A4363...D022EDFF`) |
| Tema | Coleccionismo de Mitos y Leyendas; carta apócrifa de La Quintrala |

## Flag

```
flag{ejemplo}
```

## Enunciado (resumen)

En una feria de las pulgas aparecen dos catálogos de símbolos (uno de imprenta y otro de
una reimpresión dudosa) y dos láminas: una «sin número» (supuesta carta perdida de La
Quintrala) y otra marcada **PROMO / NO JUGABLE**. Hay que decidir **cuál catálogo es el
auténtico**, interpretar la lámina correcta y recuperar el mensaje.

> El acta de subasta es la clave del reto: *«La lámina sin número se coteja con
> `catalogo_glifos.txt` (impresión original). La reimpresión carece del sello del lote. La
> lámina promocional no participa en el inventario.»*

## Evidencia

| Archivo | Tamaño | Rol |
|---|---|---|
| `acta_de_subasta.txt` | 210 B | reglas del cotejo (indica qué catálogo vale) |
| `catalogo_glifos.txt` | 277 B | catálogo de imprenta **auténtico** |
| `catalogo_reimpresion.txt` | 327 B | reimpresión sin sello (señuelo) |
| `lamina_promocional.txt` | 354 B | PROMO / NO JUGABLE (control de calidad) |
| `lamina_quintrala.txt` | 537 B | lámina sin número (objetivo) |

Hashes SHA256:

```
zip                  8C4A436354B34DEBD2A1EE02B155F12D3F3F3F540B632683D4E6524FD022EDFF
acta_de_subasta      C24BCEF851BB0424227C8E5AC05E491CFA08BA665300CFC6F331F0A1F8C644B4
catalogo_glifos      171F229C23168070227F3C8A9EC75F192C6412E6786A1CB1FB8D4F9CE69F3A68
catalogo_reimpresion 97BD65998E46A8578BAFA1974FC73A326F30932180A26DF0847DC7ACC2120942
lamina_promocional   49466B719351F3444079DD680A044DB850DDF0C966AD2D812C3C1D3D6629E925
lamina_quintrala     BBA385911C6A825C43FC5BF4AF2A53FF59B79210590AACC0EF6712ACF71FDD64
```

## Análisis

Cada catálogo es una tabla de **16 glifos → cifra hexadecimal** (0–F). Las láminas son
secuencias de glifos: **dos glifos por byte**, leídas de izquierda a derecha.

Catálogo auténtico (`catalogo_glifos.txt`):

| Glifo | Valor | Glifo | Valor |
|---|---|---|---|
| ▽ `U+25BD` | 9 | ○ `U+25CB` | 4 |
| ▲ `U+25B2` | 2 | ☀ `U+2600` | D |
| ♣ `U+2667` | E | □ `U+25A1` | 6 |
| ◇ `U+25C7` | 5 | ◆ `U+25C6` | 1 |
| ◉ `U+25C9` | 0 | ☆ `U+2606` | A |
| ☾ `U+263D` | C | ★ `U+2605` | B |
| ■ `U+25A0` | 7 | ▼ `U+25BC` | 3 |
| ♠ `U+2660` | F | △ `U+25B3` | 8 |

La reimpresión es **idéntica salvo dos filas intercambiadas**: `▽ = 2` y `▲ = 9`
(en la auténtica son `▽ = 9`, `▲ = 2`). Un solo bit de diferencia por glifo, suficiente
para corromper el resultado.

### Cómo se decide cuál es el auténtico (no adivinando)

Decodificando la lámina **PROMO / NO JUGABLE** con ambos catálogos:

| Catálogo | Resultado |
|---|---|
| `catalogo_glifos` (auténtico) | `ENSAYO DE IMPRENTA SIN VALOR DE TORNEO` |
| `catalogo_reimpresion` | `ENSARO\x03DE\x0bBMPYENTA\x0bSBN\x0bVALOY\x0bDE\x0bTOYNEO` |

Solo el catálogo de imprenta produce texto legible en la lámina de control. Es el mismo
criterio que fija el acta, así que la decisión no depende de la narrativa: **se valida
criptográficamente**.

## Solución (pasos reproducibles)

```python
import re

# 1) cargar glifo -> dígito hex de cada catálogo
def cargar(path):
    return {m.group(1): m.group(2)
            for m in re.finditer(r"^(.) \| ([0-9A-F])$", open(path, encoding="utf-8").read(), re.M)}

# 2) dos glifos por byte
def decodificar(texto, mapa):
    h = "".join(mapa[c] for c in texto if c in mapa)
    return bytes.fromhex(h).decode("utf-8")

autentico = cargar("work/catalogo_glifos.txt")
print(decodificar(open("work/lamina_quintrala.txt", encoding="utf-8").read(), autentico))
```

```bash
$ python3 solucion/decodificar_lamina.py
>>> flag{ejemplo}
```

### Contraste con el catálogo equivocado

```
AUTÉNTICO     : flag{ejemplo}
REIMPRESIÓN   : flag{ejemplo}
```

La versión falsa **sigue pareciendo una flag válida** (mismo largo, leetspeak coherente):
es el cebo del reto, pensado para que se envíe sin verificar. Los caracteres que cambian
son exactamente los que usan los glifos permutados (`▽`/`▲`): M↔Y en `TRAMA`, R↔Y en
`R4r4`, L↔Y en `Qu1ntr4l4`, b↔i en `Est4b4`.

## Resultado

```
flag{ejemplo}
```

*«La carta rara de La Quintrala no estaba maldita»* — con `4` por `a`, `1` por `i` y `0`
por `o`, y `N0_Est4b4_M4ld1t4` en referencia a la leyenda de la Quintrala.

## Lecciones / notas

- **Valida el alfabeto antes de descifrar**: la lámina PROMO es un vector de prueba
  perfecto; quien la ignore acepta una flag corrupta.
- Dos filas intercambiadas en un catálogo de 16 símbolos bastan para producir un texto
  plausible y falso. En criptografía real es el mismo problema que un *codebook* alterado.
- Los glifos son Unicode reales (`U+25xx`, `U+26xx`), no imágenes: hay que leer el archivo
  como UTF-8; abrirlo en una consola con codificación incorrecta (como la de PowerShell)
  muestra `?` y destruye la tabla. Se detectó leyendo con Python y volcando los
  codepoints.
- Regla práctica: si un reto ofrece «catálogo original» y «copia», el discriminante suele
  ser un **vector de control conocido** (aquí, la lámina PROMO), no la narración.
- El acta de subasta es documentación operativa, no relleno: fija qué catálogo aplica a
  qué pieza.

## Archivos de la carpeta

| Ruta | Contenido |
|---|---|
| `Cartas.zip` | evidencia original |
| `CONTEXTO.md` | este writeup |
| `flag.txt` | flag extraída |
| `solucion/decodificar_lamina.py` | decodificador con ambos catálogos y comparación |
| `solucion/salida.txt` | salida completa |
| `work/` | los 5 archivos del zip |
