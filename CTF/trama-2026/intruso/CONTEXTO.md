# Desafío 33 — Puerta Abierta (intruso.pcap)

| Campo | Valor |
|---|---|
| Categoría | forense de red / análisis de PCAP (FTP) |
| Dificultad | fácil |
| Puntos | — |
| Estado | ✅ resuelto |
| Flag | `flag{ejemplo}` |

## Enunciado

> **Puerta Abierta** — Alguien dejó una puerta abierta. Un servicio que no debía estar expuesto quedó
> asomado a la red […] desde una dirección externa, un intruso tanteó la casa, probó llaves hasta que
> una entró y se marchó con información que no le pertenecía.
>
> Analiza la captura y reconstruye el incidente: IP de origen, servicio comprometido, intentos fallidos,
> credenciales utilizadas y archivo exfiltrado. Examina también el contenido del archivo sustraído.
>
> ¿Cuál de las siguientes reconstrucciones coincide por completo con la evidencia?
>
> - 203.0.113.37 | FTP/21 | 5 intentos fallidos | soporte / **Soporte2024** | credenciales.txt
> - 203.0.113.37 | FTP/21 | 6 intentos fallidos | soporte / Verano2024 | catalogo.txt
> - **198.51.100.10** | FTP/21 | 5 intentos fallidos | soporte / Verano2024 | credenciales.txt
> - **203.0.113.37 | FTP/21 | 5 intentos fallidos | soporte / Verano2024 | credenciales.txt**
> - 203.0.113.37 | SSH/22 | 5 intentos fallidos | admin / 123456 | catalogo.txt

## Reconocimiento

`intruso.pcap` — 147 paquetes, 11.511 B, **3,99 s**, capturado el **2026-10-19 15:33:11**
(SHA-256 `38e09b5c...6807c1c8`, verificado contra `SHA256SUMS (2).txt`).

Protocolos: TCP/FTP (59 tramas), FTP-DATA (2 tramas) e ICMPv6 (2 tramas).

Conversaciones relevantes:

| Cliente | Servidor | Bytes |
|---|---|---|
| 203.0.113.37:58620 | 198.51.100.10:21 | 2.878 |
| 203.0.113.37:58204 | 198.51.100.10:50021 (datos) | 836 |
| 203.0.113.37:58196 | 198.51.100.10:50021 (datos) | 739 |

Antes del FTP hay un **barrido de puertos** desde `203.0.113.37` hacia `198.51.100.10` en
**22, 23, 80, 443, 445 y 3389** (una conexión SYN por puerto). El servidor FTP se anuncia como
`CentinelaFTP listo.`

Direcciones: el **atacante es `203.0.113.37`** (inicia las conexiones y envía `USER`/`PASS`);
el servidor comprometido es `198.51.100.10` (responde `220`, `331`, `530`, `230`).

## Análisis

### Tentativas de autenticación

| # | Usuario | Clave | Respuesta |
|---|---|---|---|
| 1 | admin | admin | `530 Login incorrecto` |
| 2 | admin | 123456 | `530 Login incorrecto` |
| 3 | root | toor | `530 Login incorrecto` |
| 4 | soporte | soporte | `530 Login incorrecto` |
| 5 | soporte | Soporte2024 | `530 Login incorrecto` |
| 6 | **soporte** | **Verano2024** | **`230 Acceso concedido`** |

→ **5 intentos fallidos** y una sesión válida con `soporte / Verano2024`.

### Sesión y exfiltración

```
230 Acceso concedido. Bienvenido, soporte.
SYST / TYPE I / PWD
PASV  -> 227 Entering Passive Mode (198,51,100,10,195,101)   # puerto 50021
LIST  -> listado del directorio
PASV  -> 227 ...
RETR credenciales.txt
226 Transferencia completa.
QUIT
```

Listado del servidor (stream 13, 195 B):

```
-rw-r--r-- 1 soporte soporte   32 Oct 19 10:00 catalogo.txt
-rw-r--r-- 1 soporte soporte  292 Oct 19 10:00 credenciales.txt
-rw-r--r-- 1 soporte soporte    5 Oct 19 10:00 logo.png
```

Archivo exfiltrado: **`credenciales.txt`** (292 B, stream 14).

### Contenido del archivo sustraído

```
# Respaldo de accesos - Centinela (CONFIDENCIAL - no distribuir)
vpn_user=admin_vpn
vpn_pass=C3ntinela#VPN2024
panel_admin=https://panel.centinela.local/manage
db_root=r00t_db_2024
backup_note=si lees esto, alguien se llevo las llaves de la casa
flag=flag{ejemplo}
```

## Respuesta correcta

```
203.0.113.37 | FTP/21 | 5 intentos fallidos | soporte / Verano2024 | credenciales.txt
```

Descartes:

- **198.51.100.10** es el servidor, no el origen (las conexiones las inicia `203.0.113.37`).
- **Soporte2024** fue el quinto intento **fallido**; la clave válida es **Verano2024**.
- **6 intentos fallidos** no cuadra: son cinco `530` y el sexto es el `230`.
- **SSH/22** solo aparece en el barrido de puertos (una conexión, sin autenticación).
- **catalogo.txt** existe, pero el `RETR` fue de `credenciales.txt`.

## Flag

```
flag{ejemplo}
```

## Solución (pasos reproducibles)

```bash
# 1) Verificar integridad
sha256sum intruso.pcap          # 38e09b5c...6807c1c8

# 2) Cronología FTP (comandos/respuestas)
tshark -r intruso.pcap -Y ftp -T fields \
  -e frame.number -e ip.src -e ip.dst \
  -e ftp.request.command -e ftp.request.arg \
  -e ftp.response.code -e ftp.response.arg

# 3) Transferencias de datos
tshark -r intruso.pcap -Y ftp-data -T fields -e tcp.stream -e tcp.len

# 4) Extraer el archivo exfiltrado (stream 14)
tshark -r intruso.pcap -Y 'tcp.stream==14 && ip.src==198.51.100.10' \
  -T fields -e tcp.payload | tr -d '\n' | xxd -r -p > credenciales.txt

# Alternativa interactiva:
tshark -r intruso.pcap -q -z follow,tcp,ascii,14
```

Automatizado en `solucion/analizar_intruso.py` (requiere `tshark`).

## Evidencia y artefactos

| Ruta | Contenido |
|---|---|
| `intruso.pcap` | Captura original (147 paquetes) |
| `SHA256SUMS (2).txt` | Hash de referencia (coincide) |
| `work/credenciales.txt` | Archivo exfiltrado (292 B) |
| `work/listado.txt` | Listado FTP del servidor (195 B) |
| `solucion/analizar_intruso.py` | Reconstrucción automatizada del incidente |
| `flag.txt` | Flag del reto |

## Lecciones / notas

- La **dirección del flujo** importa: el atacante es quien inicia la conexión y envía `USER/PASS`
  (203.0.113.37), no el servidor (198.51.100.10).
- Distinguir **intento fallido** (`530`) de **acceso concedido** (`230`) es la clave para contar 5 y no 6.
- El canal de datos FTP pasivo va por un puerto efímero anunciado en `227`; hay que seguirlo para
  recuperar el archivo (`tcp.payload` o `follow tcp`).
- Un `LIST` muestra lo que hay, pero la exfiltración real es el `RETR`; no confundir `catalogo.txt` con
  `credenciales.txt`.
- El contenido robado (VPN, panel, root de BD) muestra el impacto real y contenía la flag.

## Backups

| Archivo | Backup |
|---|---|
| `ctf/CONTEXTO_CTF.md` (índice) | `ctf/backups/CONTEXTO_CTF.md.20261023-204028` |
