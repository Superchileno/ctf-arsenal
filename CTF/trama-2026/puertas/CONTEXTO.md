# Desafío 38 — Las Veinte Puertas

| Campo | Valor |
|---|---|
| Categoría | Misc / grafos dirigidos + lectura por columnas |
| Dificultad | fácil-media |
| Puntos | — |
| Estado | ✅ resuelto |
| Flag | `flag{ejemplo}` |

## Enunciado

> **Las Veinte Puertas — La inauguración que terminó en el pasillo**
> Un hotel boutique de Valparaíso prometía una experiencia «inmersiva» con veinte puertas […]
> el edificio tenía un mecanismo de verificación de sellos bastante ingenioso; por desgracia, el dueño
> lo confundía con un sistema de fidelización.
> «Si sigues el cartel más bonito, terminas en la lavandería. Si sigues los sellos correctos, terminas
> donde corresponde. Las bandas del registro no se leen como un cuento.»
> Los veinte accesos contienen datos, pero no todos pertenecen al recorrido de aquella noche. Y el
> recorrido importa tanto como el orden en que se lee lo recuperado.
> **Reconstruye la ronda nocturna y recupera el mensaje que dejó el sistema al encontrar la única salida válida.**

## Reconocimiento

`Veinte_Puertas.zip` (1.519 B) contiene cuatro archivos de texto sin cifrar:

| Archivo | Contenido |
|---|---|
| `LEEME.txt` | sin servicios externos |
| `nota_de_recepcion.txt` | **señuelo**: el dueño cree que las puertas 02 y 19 son «las buenas» por tener marcos nuevos |
| `protocolo_de_ronda.txt` | **las reglas reales** |
| `registro_de_puertas.csv` | 20 filas: `sello`, `paso_izq`, `paso_der`, `banda`, `estado` |

## Análisis

### Reglas extraídas del protocolo

1. Entrada por la **puerta 01**.
2. La ronda válida recorre **7 puertas** contando la inicial.
3. Cada puerta ofrece dos salidas: **IZQ** (`paso_izq`) y **DER** (`paso_der`).
4. Controlador de sellos: `sello_siguiente = (3 · sello_actual + 7) mod 17`.
5. **Solo una** de las dos salidas conduce a una puerta cuyo sello coincida con el esperado.
6. La ronda termina en la puerta cuyo `estado` es `SALIDA`.
7. Cada puerta visitada aporta **una banda de 5 símbolos**.
8. Las bandas se colocan como **columnas** en orden de visita y se leen por **filas**.

### La trampa de las puertas 02 y 19

La nota del recepcionista empuja a empezar por las puertas «con marco nuevo». Es un señuelo: ni la 02
ni la 19 aparecen en el recorrido válido, y seguir su banda produce basura. La frase
*«las bandas del registro no se leen como un cuento»* avisa de que la lectura **no es secuencial por
puertas** (como un cuento), sino **por columnas y luego por filas**.

### Traza del recorrido

| Paso | Puerta | Sello | Esperado `(3s+7) mod 17` | Salida | Destino | Sello destino |
|---|---|---|---|---|---|---|
| 1 | 01 | 2 | 13 | IZQ | 06 | 13 ✔ |
| 2 | 06 | 13 | 12 | DER | 12 | 12 ✔ |
| 3 | 12 | 12 | 9 | IZQ | 03 | 9 ✔ |
| 4 | 03 | 9 | 0 | DER | 17 | 0 ✔ |
| 5 | 17 | 0 | 7 | IZQ | 10 | 7 ✔ |
| 6 | 10 | 7 | 11 | DER | 05 | 11 ✔ |
| 7 | 05 | 11 | — | — | **SALIDA** | — |

Recorrido: **`01 → 06 → 12 → 03 → 17 → 10 → 05`** (7 puertas, termina en `SALIDA`).

En cada paso exactamente **una** de las dos salidas cumple la congruencia: el grafo está construido
para que el camino sea único, sin necesidad de backtracking.

### Lectura en columnas

```
col 1  02  03  04  05  06  07   (puertas visitadas)
 01   T   F   i   r   _
 06   R   {   c   t   a
 12   A   l   a   a   b
 03   M   a   _   _   r
 17   A   _   p   q   i
 10   C   u   u   u   a
 05   T   n   e   e   }
```

FILA 1 (izq→der): `TRAMACT`
FILA 2: `F{la_un`
FILA 3: `ica_pue`
FILA 4: `rta_que`
FILA 5: `_abria}`

## Solución (pasos reproducibles)

```bash
python3 solucion/resolver_puertas.py Veinte_Puertas.zip
# [*] 20 puertas cargadas
#     puerta 01 (sello  2) -> esperado 13 -> IZQ -> puerta 06
#     ...
# [*] recorrido: 01 -> 06 -> 12 -> 03 -> 17 -> 10 -> 05 (7 puertas)
# [*] estado final: SALIDA
# FLAG: flag{ejemplo}
```

A mano: partir de la puerta 1, calcular `(3·sello+7) mod 17`, elegir la salida cuyo destino tenga ese
sello, repetir 6 veces y verificar que se llega a `SALIDA`. Luego transcribir las 7 bandas como
columnas y leer las 5 filas.

## Flag

```
flag{ejemplo}
```

## Evidencia y artefactos

| Ruta | Contenido |
|---|---|
| `Veinte_Puertas.zip` | Evidencia entregada (1.519 B) |
| `work/LEEME.txt` | Léeme original |
| `work/nota_de_recepcion.txt` | Señuelo de las puertas 02/19 |
| `work/protocolo_de_ronda.txt` | Reglas del controlador |
| `work/registro_de_puertas.csv` | 20 puertas con sellos, saltos y bandas |
| `work/salida.txt` | Ejecución del solver |
| `solucion/resolver_puertas.py` | Solver (recorrido + lectura por columnas) |
| `flag.txt` | Flag del reto |

## Lecciones / notas

- La nota del recepcionista es **información corrupta a propósito**: dos puertas «bonitas» que no
  pertenecen a la ronda. En CTF, toda pista debe validarse contra la regla formal.
- El grafo es un **recorrido único autovalidado**: no hace falta fuerza bruta, basta comprobar la
  congruencia en cada bifurcación (y detectar si hay 0 o 2 opciones válidas).
- El orden de lectura es parte del reto: bandas = columnas, mensaje = filas. Leerlas como «cuento»
  (secuencialmente por puerta) devuelve texto sin sentido.
- Las 13 puertas no visitadas son ruido deliberado; el estado `SALIDA` de la puerta 05 confirma el
  final antes de intentar leer nada.

## Backups

| Archivo | Backup |
|---|---|
| `ctf/CONTEXTO_CTF.md` (índice) | `ctf/backups/CONTEXTO_CTF.md.20261024-134251` |
