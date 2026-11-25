# Desafío 09 — La Cuenta que No Existía

| Campo | Valor |
|---|---|
| Evento | TRAMA CTF 2026 · *Archivo de los rastros perdidos* |
| Categoría | OSINT / forense de metadatos (EXIF) + perfiles archivados |
| Estado | ✅ Resuelto |
| Evidencia | `La_Cuenta_que_No_Existia.zip` (SHA256 `F9D192F1...E66B36B3`) |
| Hallazgo | `ultima_foto.jpg` conserva EXIF con `Artist = valen_nomade_priv` |

## Flag

```
flag{ejemplo}
```

## Enunciado (resumen)

Valentina (@valen.nomade) borra su cuenta tras un escándalo. Una seguidora guardó **cinco
fotografías y varias copias de perfiles**; algunas pistas se contradicen. Hay que
determinar si desapareció todo rastro, **identificar el rastro que conecta ambas
evidencias** y encontrar el mensaje que no pudo borrar. El PR insiste: «si apretó
eliminar, se eliminó».

## Evidencia

```
work/
├── archivo_web/            6 perfiles archivados + index
│   ├── valen_nomade.html            43Dvy2AUMU66g4LA
│   ├── valen_oficial.html           xa6DEc/hZtIhPO3M
│   ├── valen.viajes.html            dR52+15NnRv5qVN2
│   ├── vnomade2020.html             gw24aHD7lcwZqO0N
│   ├── valenr_backup.html           ZI2RNKdOClgIOYaA
│   └── valen_nomade_priv.html       <-- el bueno (base64)
└── fotos/
    ├── atardecer_lisboa.jpg  · cafe_manana.jpg · mercado.jpg · muelle.jpg
    └── ultima_foto.jpg                <-- el único con EXIF
```

## Análisis

### 1. Las cinco fotos: cuatro están limpias

`exiftool -a -G1` sobre las cinco imágenes: **solo una** tiene metadatos.

```
atardecer_lisboa.jpg   sin EXIF
cafe_manana.jpg        sin EXIF
mercado.jpg            sin EXIF
muelle.jpg             sin EXIF
ultima_foto.jpg        CON EXIF
```

### 2. La "última foto" delata el rastro

```
[IFD0]     Make        : Pixel
[IFD0]     Software    : cam-app 4.2
[IFD0]     Artist      : valen_nomade_priv          <-- huella
[ExifIFD]  UserComment : il espejo: valen_nomade_priv
[GPS]      GPSPosition : 33° 2' 0.00" S, 71° 37' 0.00" W
```

- **`Artist = valen_nomade_priv`** es el nombre que conecta la foto con un perfil.
- El `UserComment` («perfil espejo») confirma la intención: es la cuenta espejo/privada.
- El **GPS** `33.0333 S, 71.6167 W` cae en **Viña del Mar / Valparaíso**, coherente con
  el resto del material y con el resto del evento (no es la pista principal, pero cuadra).

### 3. El perfil correcto entre seis copias

Los cinco perfiles "normales" traen un `codigo:` de 16 caracteres que **parece**
base64 pero decodifica a bytes binarios sin sentido (señuelos):

```
43Dvy2AUMU66g4LA -> e3 70 ef cb 60 14 31 4e ba 83 82 c0 ...
```

El perfil **espejo** es distinto: dice explícitamente «Código de recuperación (base64)» y
su valor sí es Base64 legible:

```
VFJBTUFDVEZ7Ym9ycm9fbGFfY3VlbnRhX25vX2VsX21ldGFkYXRvfQ==
        |
        v
flag{ejemplo}
```

## Solución (pasos reproducibles)

### Script (guardado en `solucion/rastrear_cuenta.py`)

```python
# 1) buscar la huella en el EXIF de las fotos
for f in glob("work/fotos/*.jpg"):
    exif = Image.open(f).getexif()
    artista = exif.get(0x013B)       # Artist
    if artista:
        print(f, artista)

# 2) el perfil archivado con ese nombre
html = open(f"work/archivo_web/{artista}.html").read()

# 3) decodificar su código base64
print(base64.b64decode(re.search(r"base64\)?:\s*(\S+)", html).group(1)).decode())
```

```bash
$ python3 solucion/rastrear_cuenta.py
== 1) EXIF de las 5 fotografías ==
  ultima_foto.jpg      CON EXIF -> {'Make': 'Pixel', 'Artist': 'valen_nomade_priv', ...}
      -> GPS: -33.0333, -71.6167
== 2) Perfil archivado que corresponde a esa huella ==
  abriendo valen_nomade_priv.html
  código: VFJBTUFDVEZ7Ym9ycm9fbGFfY3VlbnRhX25vX2VsX21ldGFkYXRvfQ==
== 3) Decodificación ==
  flag{ejemplo}
```

### A mano, en tres comandos

```bash
exiftool work/fotos/ultima_foto.jpg | grep -Ei "artist|comment|gps"
grep -i base64 work/archivo_web/valen_nomade_priv.html
echo 'VFJBTUFDVEZ7Ym9ycm9fbGFfY3VlbnRhX25vX2VsX21ldGFkYXRvfQ==' | base64 -d
```

## Resultado

```
flag{ejemplo}
```

La ironía del reto: borró la cuenta, pero la foto que subió como "última" conservó el
nombre del perfil espejo en los metadatos. La respuesta al PR es la flag: **borrar la
cuenta no borra el metadato**.

## Lecciones / notas

- **El metadato sobrevive al borrado**: la identidad no estaba en la red social, estaba en
  el `Artist` de un JPEG.
- Ante varias copias de perfil, el discriminante no es el nombre: los cinco decoys tenían
  códigos que *parecían* Base64 pero eran binario aleatorio. Solo el espejo declaraba
  «base64» y decodificaba a texto.
- `exiftool -a -G1` (mostrar todo, agrupado) es el estándar para no perder tags raros como
  `UserComment`.
- PIL no expone `UserComment` en el bloque principal de `getexif()`; conviene usar
  `exiftool` o `exif.get_ifd(0x8769)` si se automatiza.
- Señal de calidad del reto: 4 de 5 fotos limpias → el análisis diferencial (¿cuál tiene
  metadatos?) apunta directo sin fuerza bruta.

## Archivos de la carpeta

| Ruta | Contenido |
|---|---|
| `La_Cuenta_que_No_Existia.zip` | evidencia original |
| `CONTEXTO.md` | este writeup |
| `flag.txt` | flag final |
| `solucion/rastrear_cuenta.py` | EXIF → huella → perfil → base64 |
| `solucion/salida.txt` | salida de la ejecución |
| `work/fotos/` | las 5 fotografías (solo `ultima_foto.jpg` con EXIF) |
| `work/archivo_web/` | los 6 perfiles archivados + index |
