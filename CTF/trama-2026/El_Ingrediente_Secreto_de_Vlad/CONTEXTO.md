# Desafío 10 — El Ingrediente Secreto de Vlad

| Campo | Valor |
|---|---|
| Categoría | OSINT / GitHub (reconocimiento de perfil, repos públicos e historial de commits) |
| Estado | ✅ Resuelto |
| Objetivo | Perfil `VladElVeg666` → repo `Mis_Recetas_Favoritas` → flag |
| URL | https://github.com/VladElVeg666/Mis_Recetas_Favoritas |

## Flag

```
flag{ejemplo}
```

## Enunciado (resumen)

El Conde Ciber-Drácula quiere censurar el perfil secreto de su hijo vegano, **VladElVeg666**,
que publicó sus «recetas secretas» en GitHub. Hay que encontrar el repositorio y recuperar
la flag escondida en el código (el «ingrediente secreto»).

## Reconocimiento

### 1. El perfil existe (y se delata solo)

```bash
$ curl -s https://api.github.com/users/VladElVeg666
login        : VladElVeg666
name         : Vlad The Vegeterian
bio          : I love tomatos!!!
location     : TransilVilla
public_repos : 1
created      : 2026-10-17T17:52:10Z
```

### 2. Un único repositorio público

```
VladElVeg666/Mis_Recetas_Favoritas — "Tomates, tomates y mas tomates!"
```

Árbol completo del repo: **un solo archivo**, `README.md` (264 B).

### 3. Tres commits, y el último es sospechoso

```
0bc36fc0  Update secret ingredient in README      2026-10-17T18:02:48Z
4afebb92  Add secret recipe section to README     2026-10-17T18:01:42Z
2ca8c7bb  Initial commit                          2026-10-17T17:59:55Z
```

El mensaje «Update **secret ingredient**» es la pista: si algo se actualizó, la versión
anterior quedó en el historial.

## Análisis

Contenido del `README.md` en `main` (HEAD):

```markdown
# Mis_Recetas_Favoritas
Tomates, tomates y mas tomates!

# Recetas Secretas de Vlad 🍅
Para hacer sangre de tomate falsa:
- 1 taza de tomate triturado
- 1 cucharada de remolacha
- Sal al gusto

**Ingrediente secreto:** flag{ejemplo}
```

Y el diff del último commit confirma que ese es el valor vigente:

```diff
-**Ingrediente secreto:** flag{ejemplo}
+**Ingrediente secreto:** flag{ejemplo}
```

Barrido del historial completo (los 3 commits):

| Commit | README contiene |
|---|---|
| `0bc36fc0` (HEAD) | `flag{ejemplo}` |
| `4afebb92` | `flag{ejemplo}` (versión anterior) |
| `2ca8c7bb` | solo el título (sin receta) |

No hay más ramas, ni tags, ni otros blobs (`git/trees/main?recursive=1` devuelve solo
`README.md`). Por lo tanto **no hay flag escondida fuera del README**: la flag buena es la
del HEAD.

## Solución (pasos reproducibles)

### Opción A — API de GitHub (sin clonar)

```bash
# 1) perfil y repos
curl -s https://api.github.com/users/VladElVeg666 | jq '.name, .bio, .public_repos'
curl -s https://api.github.com/users/VladElVeg666/repos | jq -r '.[].full_name'

# 2) contenido del repo (un solo archivo) y commits
curl -s https://api.github.com/repos/VladElVeg666/Mis_Recetas_Favoritas/contents/ | jq -r '.[].name'
curl -s "https://api.github.com/repos/VladElVeg666/Mis_Recetas_Favoritas/commits?per_page=100" | jq -r '.[] | "\(.sha[0:8])  \(.commit.message | split("\n")[0])"'

# 3) README actual
curl -s https://raw.githubusercontent.com/VladElVeg666/Mis_Recetas_Favoritas/main/README.md
```

### Opción B — clonando (mejor para revisar historial)

```bash
git clone https://github.com/VladElVeg666/Mis_Recetas_Favoritas.git
cd Mis_Recetas_Favoritas
git log --oneline --all
git log -p --all -- README.md | grep -o "TRAMACTF{[^}]*}"
git show 4afebb92:README.md      # versión anterior
```

### Opción C — script usado aquí

```bash
$ bash solucion/recolectar.sh
[i] perfil
  login: VladElVeg666 | name: Vlad The Vegeterian | bio: I love tomatos!!! | repos: 1
[i] repositorios
   VladElVeg666/Mis_Recetas_Favoritas - Tomates, tomates y mas tomates!
[i] commits
   0bc36fc0 Update secret ingredient in README 2026-10-17T18:02:48Z
   4afebb92 Add secret recipe section to README 2026-10-17T18:01:42Z
   2ca8c7bb Initial commit 2026-10-17T17:59:55Z
[i] README por commit
  guardado README_0bc36fc0.md / README_4afebb92.md / README_2ca8c7bb.md

[+] flags encontradas en el historial:
      2 flag{ejemplo}
      1 flag{ejemplo}
```

## Resultado

```
flag{ejemplo}
```

*«Tu vampiro vegetariano favorito»* — con `4` por `a`, `1` por `i`, `0` por `o` y `3` por `e`.

## Lecciones / notas

- **El mensaje del commit es inteligencia**: «Update secret ingredient» avisa que hubo un
  valor anterior. En GitHub, borrar/editar no elimina: el historial es público por diseño.
- Revisar siempre: ramas (`/branches`), tags (`/tags`), árbol recursivo
  (`/git/trees/main?recursive=1`), gists (`/gists`) y el historial de cada archivo.
- En este caso el repo tenía **un solo archivo** y **una sola rama**, así que la duda se
  cierra rápido: no hay flag escondida en otra parte.
- La flag vigente es la del HEAD. La del commit anterior (`flag{ejemplo}`)
  es un resto obsoleto: sirve como dato histórico, pero el reto pide la que está publicada.
- Técnica de OSINT: el alias ya venía dado (`VladElVeg666`); con el perfil se llega a los
  repos, y del repo al historial. Cuando el alias no se conoce, el camino es la búsqueda
  por código (`in:file`, `user:`, forks) — aquí no hizo falta.

## Archivos de la carpeta

| Ruta | Contenido |
|---|---|
| `CONTEXTO.md` | este writeup |
| `flag.txt` | flag final |
| `solucion/recolectar.sh` | script: perfil → repos → commits → README por commit |
| `solucion/salida.txt` | salida de la ejecución |
| `work/usuario.json` | respuesta de la API del perfil |
| `work/repos.json` | lista de repositorios |
| `work/commits.json` | historial de commits |
| `work/README_main.md` | README del HEAD (contiene la flag) |
| `work/README_0bc36fc0.md` | README en el commit más reciente |
| `work/README_4afebb92.md` | README en el commit intermedio (flag antigua) |
| `work/README_2ca8c7bb.md` | README inicial (sin receta) |
