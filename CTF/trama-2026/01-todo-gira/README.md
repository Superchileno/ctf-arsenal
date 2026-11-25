# Desafío 01 — Todo Gira («La rueda que cobraba otra vuelta»)

| Campo | Valor |
|---|---|
| Evento | TRAMA CTF 2026 · Expediente MISC-015: *La última vuelta* |
| Categoría | MISC / forense de archivos (archivos anidados) |
| Dificultad | Fácil-media (mecánica simple, volumen alto) |
| Estado | ✅ Resuelto |
| Evidencia | `Todo_Gira.zip` (11.894 bytes, SHA256 `5CF23F48629026438807A38AAD56DF21C6E387504EEBE9C6770B89BD2AC534AA`) |

## Flag

```
flag{ejemplo}
```

## Enunciado (resumen)

Un único archivo de respaldo del controlador de la rueda. Cada vuelta parece llevar a
otra («si no pierdes el hilo, al final sabrás qué pasó con la cabina 13»); los nombres de
los archivos «podrían ser menos arbitrarios de lo que parecen». Hay que atravesar la
estructura y recuperar el mensaje final.

## Reconocimiento

```
$ file Todo_Gira.zip
Zip archive data ... uncompressed size 11751, method=deflate

$ unzip -l Todo_Gira.zip
  Length      Date    Time    Name
    11751  2026-10-20 12:00   file_218922995834555169026.zip
```

Un zip que contiene **un solo zip**. La pista «cada vuelta te lleva a otra» = archivos
anidados recursivamente; la pista «los nombres no son arbitrarios» = los números de
nombre codifican la posición en la cadena.

## Análisis

Extrayendo niveles a mano se ve la serie de nombres:

```
file_218922995834555169026.zip   <-  F(99)
file_135301852344706746049.zip   <-  F(98)
file_83621143489848422977.zip    <-  F(97)
...
file_13.zip   file_8.zip   file_5.zip   file_3.zip
file_2.zip    file_1_b.zip file_1.zip    file_0.zip
LaFlag.txt
```

Son los **números de Fibonacci en orden descendente**, desde `F(99) = 218922995834555169026`
hasta `F(0) = 0`. El detalle `file_1_b.zip` existe porque `F(1) = F(2) = 1` colisionarían
como nombre de archivo: el autor desambiguó la segunda aparición con el sufijo `_b`.

Por tanto la «última vuelta» es la **capa 100** (F(0) → `file_0.zip`), y dentro está
`LaFlag.txt` con 72 bytes. Total: 100 capas de zip + 1 archivo de texto (101 entradas en
la cadena).

## Solución (pasos reproducibles)

### Opción A — script Python (recomendada, conserva la traza)

```python
import io, os, zipfile

data = open("Todo_Gira.zip", "rb").read()
level = 0
while True:
    zf = zipfile.ZipFile(io.BytesIO(data))          # abrir zip en memoria
    entries = zf.namelist()
    if len(entries) != 1:                            # se rompió la cadena -> final
        print("final:", entries)
        for e in entries:
            print(zf.read(e).decode("utf-8", "replace"))
        break
    name = entries[0]
    print(f"[{level:03d}] {name}")
    data = zf.read(name)                             # contenido = zip siguiente
    level += 1
```

Script completo guardado en `work/desanidar.py` (además vuelca cada capa en `work/chain/`).

Ejecución en el entorno (Kali/WSL2):

```bash
wsl -d kali-linux -- bash -lc "python3 /mnt/c/Users/shapl/AppData/Local/Temp/opencode/ctf01_unzip.py"
```

### Opción B — shell puro (unzip en bucle)

```bash
mkdir -p out && cd out
cp ../Todo_Gira.zip .
i=0
while file *.zip >/dev/null 2>&1; do
    unzip -o -q *.zip && rm -f *.zip
    i=$((i+1))
done
cat LaFlag.txt
echo "capas: $i"        # 100
```

### Opción C — carvers automáticos

`binwalk -e Todo_Gira.zip` o `7z x` repetido también funcionan, pero con 100 niveles
conviene el bucle (`binwalk` suele truncar la recursión) — el script de la opción A es el
más fiable y deja traza ordenada.

## Resultado

```
[nivel 000] file_218922995834555169026.zip (11751 bytes)
...
[nivel 099] file_0.zip (191 bytes)
[nivel 100] LaFlag.txt (72 bytes)
---- vista previa ----
La flag es: flag{ejemplo}
```

## Lecciones / notas

- **Reconocimiento antes de automatizar**: `unzip -l` en el primer nivel reveló la
  mecánica en 5 segundos.
- **Los nombres son metadatos**: la serie de Fibonacci no era decorativa, permitía saber
  de antemano que la cadena tenía 100 capas (F(99)→F(0)) y detectar si faltaba alguna.
- **Recursión en memoria** (`io.BytesIO`) evita crear 100 archivos y 100 carpetas, y
  esquiva límites de longitud de ruta en Windows.
- Detalle de diseño del reto: la colisión `F(1)=F(2)=1` resuelta como `file_1_b.zip`.
- La flag juega con el nombre del evento: *«C13n vueltas después y el reclamo sigue
  pendiente»* (cabina 13).

## Archivos de la carpeta

| Ruta | Contenido |
|---|---|
| `work/Todo_Gira.zip` | evidencia original (copia) |
| `work/desanidar.py` | script de extracción recursiva |
| `work/chain/` | las 100 capas intermedias + `final.bin` |
| `flag.txt` | mensaje final extraído |
