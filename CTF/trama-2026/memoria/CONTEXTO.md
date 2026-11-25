# Desafío 29 — Memoria (El Archivo de los Ausentes · Expediente 02)

| Campo | Valor |
|---|---|
| Categoría | esteganografía / polyglot JPEG+ZIP + QR + binario ASCII |
| Dificultad | fácil-media |
| Puntos | — |
| Estado | ✅ resuelto |
| Flag | `flag{ejemplo}` |

## Enunciado

> **Memoria — El Archivo de los Ausentes — Expediente 02: El respaldo del que nadie se acuerda** […]
> Lo único que apareció en el inventario fue una fotografía de unas memorias RAM. […] la foto llegó
> junto a una nota del antiguo responsable de los respaldos:
>
> «Aquí nadie se acuerda de nada. Por suerte, las evidencias no tienen tan mala memoria».
>
> Tu misión: investiga el archivo recuperado y averigua qué mensaje conserva. No hace falta haber
> resuelto el expediente anterior.

## Reconocimiento

`Memoria.zip` (30.340 B, SHA256 `10afb5be...40c4135`) contiene un único archivo:

```
registro_memoria.jpg   31.070 B   JPEG 500×333, EXIF de 2012 (ACD Systems)
```

`binwalk` del JPEG:

```
0      JPEG image data, JFIF standard 1.01
30     TIFF image data (EXIF)
27449  Zip archive data, ... name: respaldo_0317.png
31048  End of Zip archive, footer length: 22
```

El EXIF es "de época" (2012) y no contiene pistas; el secreto está **después** del marcador de fin de
imagen `FFD9`, que aparece en el offset `0x6b37`.

## Análisis (cadena)

```
registro_memoria.jpg
 └─ [tras FFD9, offset 0x6b39] ZIP anexado (3.621 B)
     └─ respaldo_0317.png  (924×924)  → código QR
         └─ QR: ASCII en binario, 38 grupos de 8 bits
             └─ "L0s_Recuerd0s_N0_Se_B0rr4n_C0n_Un_C4fe"
                 └─ TRAMACTF{...}
```

1. **JPEG + ZIP anexado**: tras el `FFD9` hay un ZIP válido desde `0x6b39`; se localiza buscando
   `PK\x03\x04`. La imagen se abre sin problemas, así que pasa desapercibida.
2. **`respaldo_0317.png`**: PNG de 924×924 sin metadatos ni datos extra. Visualmente es un **código QR**
   de alta densidad.
3. **Lectura del QR** (`zbarimg -q --raw`):

```
01001100 00110000 01110011 01011111 01010010 01100101 ...
```

Son **grupos de 8 bits** que codifican ASCII directamente (no es Base64 ni hex).
4. **Conversión** con `chr(int(grupo, 2))`:

```
L0s_Recuerd0s_N0_Se_B0rr4n_C0n_Un_C4fe
```

El formato oficial aporta el encabezado y las llaves → **flag**.

## Solución (pasos reproducibles)

```bash
unzip Memoria.zip -d work/

python3 solucion/resolver_memoria.py work/registro_memoria.jpg
# [1] ZIP anexado tras el EOI en 0x6b39 (3621 B)
# [2] imagen interna: respaldo_0317.png
# [3] QR: 01001100 00110000 ...
# [4] flag{ejemplo}
```

Equivalente manual:

```bash
# ZIP anexado al JPEG
python3 -c "d=open('registro_memoria.jpg','rb').read(); open('r.zip','wb').write(d[d.find(b'PK\x03\x04'):])"
unzip -o r.zip                    # respaldo_0317.png
zbarimg -q --raw respaldo_0317.png
# convertir los grupos binarios a ASCII
```

## Flag

```
flag{ejemplo}
```

## Evidencia y artefactos

| Ruta | Contenido |
|---|---|
| `Memoria.zip` | Evidencia entregada (30.340 B) |
| `work/registro_memoria.jpg` | JPEG con ZIP anexado tras `FFD9` |
| `work/respaldo.zip` | ZIP carved desde `0x6b39` |
| `work/respaldo_0317.png` | PNG con el código QR (924×924) |
| `work/flag.txt` | Flag extraída |
| `flag.txt` | Copia en la raíz del desafío |
| `solucion/resolver_memoria.py` | Resolución automatizada (carving + QR + binario) |

## Lecciones / notas

- **Datos tras el fin de imagen**: un JPEG termina en `FFD9`; lo que venga después no afecta a la
  visualización y es el escondite clásico de un ZIP.
- **El QR es un contenedor**: no siempre lleva una URL o texto legible; aquí contenía bits en ASCII
  binario, que hay que reconocer por los grupos de 8 caracteres `0/1`.
- El EXIF antiguo es atrezzo narrativo: conviene revisarlo, pero la pista real estaba en la estructura
  del archivo.
- Aunque el enunciado diga que no hace falta el expediente anterior, la mecánica (polyglot + capas)
  continúa la del «Archivo Imposible».

## Backups

| Archivo | Backup |
|---|---|
| `ctf/CONTEXTO_CTF.md` (índice) | `ctf/backups/CONTEXTO_CTF.md.20261023-192154` |
