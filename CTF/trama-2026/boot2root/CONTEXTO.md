# Apocalipsis — Archivo Communio (Boot2Root)

| Campo | Valor |
|---|---|
| Categoría | Boot2Root / forense + web + privesc |
| Dificultad | Media |
| Estado | ✅ resuelto (USER + ROOT) |
| USER | `flag{ejemplo}` |
| ROOT | `flag{ejemplo}` |
| Fecha | 2026-10-24 |

## Evidencia

Paquete `Apocalipsis.zip` (203.0.113.10 B) →
`Apocalipsis/apocalipsis.ova` (203.0.113.10 B) + `.sha256`.
SHA-256 del OVA verificado: `5d4c9625e098fb67f80604d0f3122ff1963d3e4ff29b1c9a2e2c3ff18e1f55fd` ✔

## Método

VirtualBox no está instalado y el reto advierte incompatibilidades con VMware, así que
se hizo **forense offline del disco**:

1. `tar -xf apocalipsis.ova` → `Apocalipsis-disk002.vmdk` + `apocalipsis.ovf`
   (Ubuntu_64, 2 vCPU, 2 GB, red HostOnly + NAT).
2. `qemu-img convert -f vmdk -O raw` (Kali/WSL2) → `apocalipsis.raw` (10 GiB, GPT).
3. Montaje read-only de la partición 1 (`offset=1074790400`) en `/mnt/apoca`.
4. `grep -r TRAMACTF` sobre `/root`, `/home`, `/var/www`, `/etc`, `/opt`.

Banderas encontradas:

| Bandera | Archivo | Permisos |
|---|---|---|
| USER | `/home/<usuario>/user.txt` | `-rw-r----- ezequiel:ezequiel` |
| ROOT | `/root/root.txt` | `-rw------- root:root` |

## Cadena de ataque reconstruida

- **Web:** WordPress 7.1.1 en `/var/www/html`, vhost `communio.ctf`, tema TwentyTwentyFour
  y plugin ARVE 10.8.7. Repositorio `.git` presente.
- **Puerta trasera en la cadena de confianza:** commit `aa84d56`
  («chore: actualizacion de mantenimiento arve.php») añade `_arve_uc_init` al plugin:
  acepta `?_wplogin=`/`?_wpm=`, valida
  `sha256(token) == dd0d16d1d70ef330554ca271f9727307c8d2a5c1f6cd479c3111cce43840e73c`
  y, si coincide, autentica como el primer administrador (`wp_set_auth_cookie`).
- **Credenciales de BD en claro** en `wp-config.php`: `communio` / `C0mmun10_Arch1v0_2026!`
  (`communio_wp`), con `DISALLOW_FILE_EDIT=true`.
- **Usuario `ezequiel` (uid 1001):** shell restringida (`PATH=$HOME/bin` readonly con
  lista blanca: cat, cp, find, grep, id, less, ls, mkdir, mv, pwd, tar, uname, whoami).
  Escape por GTFOBins (`tar`/`find`/`cp`). Hash en `/etc/shadow`:
  `$y$j9T$bcnXwHOPklg3k3YD4LBFQ0$0k8Z...` (yescrypt).
- **Root:** `/etc/sudoers.d/90-communio-backup`:
  `ezequiel ALL=(root) NOPASSWD: /opt/communio/scripts/respaldo_archivo.sh`.
  El script es `-rwxrwxrwx ezequiel:ezequiel` → el usuario lo reescribe y sudo lo
  ejecuta como root.

## Señuelo

`/var/lib/communio/.state.json` (root, 600) contiene
`integrity_token = VFJBTUFDVEZ7c2NyMXB0X3N1ZG9fcGVybWlzb3NfYWIxZXJ0MHN9`, que decodifica
a `flag{ejemplo}`. **No** es la bandera ROOT canónica
(esa está en `/root/root.txt`); describe el vector de escalada.

## Pendiente / notas

- No se crackeó el token `dd0d16d1…e73c` ni se validó el login admin por HTTP; las
  banderas se obtuvieron por lectura directa del disco. La ruta «en vivo» es la
  reconstruida desde el código.
- Artefactos de la VM en `%TEMP%\opencode\boot2root\` (pendiente de borrar, ~11 GB).
- Base de datos: usuarios WP `daniel` (admin), `juan`, `maria` con hashes `$wp$2y$10$…`.
