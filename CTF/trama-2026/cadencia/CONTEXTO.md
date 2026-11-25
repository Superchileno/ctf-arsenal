# Cadencia Fantasma (MESA-17) — CONTEXTO (parcial)

**Reto:** `cadencia` (forense MIDI + criptografía)
**Fecha:** 2026-10-24
**Evidencias:** `cadencia_fantasma.mid` (12.952 B), `buffer_0317.bin` (80 B)
**Estado:** ❌ **flag NO obtenida** — MIDI caracterizado por completo, password del buffer sin descubrir.

---

## 1. `buffer_0317.bin`

```
000000  53 61 6c 74 65 64 5f 5f  "Salted__"
000008  56 46 30 33 31 37 21 21  "VF0317!!"   <- salt de 8 B (¡ASCII elegido a mano!)
000010  8c d9 1e 55 60 d6 5b 56 40 61 ec ba 06 ab 58 d2
000020  e9 a4 81 60 d5 e6 e8 e2 35 97 9d 6a 55 ea df 12
000030  0d 7a c7 9d 76 d5 90 e3 d7 ad f1 37 0d 39 87 9d
000040  1e 9d 56 2d f6 a7 71 ab ab bd ed de 47 1d 67 b8
```

- Formato `openssl enc` (header `Salted__` + salt de 8 B + ciphertext de **64 B** = 4 bloques).
- Plaintext esperado: 48-63 B con PKCS#7 → cabe una flag de 48-63 caracteres.

## 2. `cadencia_fantasma.mid` — caracterización completa

- **Formato 1, 9 pistas, 480 ticks/negra**, 12.952 B, íntegro (9 `MTrk` que suman el tamaño exacto;
  **0 bytes tras cada `FF 2F 00`**).
- **74 BPM**, compás **6/8**, **56 compases** (`t=80640`), armadura **1 bemol (Re menor)**.
- Sin `program change`, sin `control change`, sin textos salvo nombres de pista → **generado por script**.

| # | Pista | Notas ON | Canal | Compases | Velocidades |
|---|---|---|---|---|---|
| 1 | Piano RH | 330 | 0 | 1-56 | 48,50,52,58,62,64,65,66,67,68,70,72,74 |
| 2 | Piano LH | 112 | 1 | 1-56 | 43,45,50,55,58,64,65,70 |
| 3 | Cello | 82 | 2 | 1-21,31-43,48-56 | 47,49,52,55,56,58 |
| 4 | Strings | 215 | 3 | 3-56 | 38,46,50,52 |
| 5 | Violin | **32** | **6** | **41-56** | 62,66,70,75 |
| 6 | Electric Guitar | 150 | **4** | **21-56** | 52,68,72,78,86 |
| 7 | Bass | 152 | 5 | 5-56 | 52,56,60,64,74 |
| 8 | Drums | 469 | 9 | 5-56 | 32,36,38,40,42,44,45,48,54,55,58,60,62,66,68,70,72,82,84,86,88 |

- "Retornos" exactos detectados en la melodía: m2≡m6, m4≡m48≡m52, m8≡m42≡m55, m10≡m14≡m34≡m39,
  m11≡m35, m12≡m36, m13≡m38.
- Secciones con notas repetidas (m21-28 y m41-47) — el material "vuelve" con eco/stutter.
- Micro-timing: **todas** las notas ON caen en múltiplos de 240 ticks (sin jitter).
- Duraciones: RH 240/480; LH y Cello 720; Strings 720/1410/1415; Violin 690/695/720;
  Guitar 680/695/720/1415; Bass 240/720; Drums 35/40/60/70/80/100.

## 3. Hipótesis probadas y descartadas

| Hipótesis | Resultado |
|---|---|
| Datos tras el end-of-track | ❌ no hay |
| Pistas retrógradas / canon entre pistas (con y sin transposición) | ❌ sin coincidencias |
| Micro-timing (`tick % 240`) como canal | ❌ todo alineado |
| Velocidad de note-off (release velocity) | ❌ todas 0 |
| Velocidades como ASCII directo (todas las pistas, directo e inverso) | ❌ son dinámicas por sección |
| Orden de notas dentro de acordes | ❌ siempre ascendente (salvo batería) |
| Bits "la nota repite la anterior / vuelve a una altura ya vista" | ❌ sin ASCII |
| Password = melodía en nombres de nota, grados, intervalos, etc. (438 variantes) | ❌ |
| Password = combinaciones de tokens (MESA, 17, 0317, VF, cadencia, fantasma, violin…) (66.930) | ❌ |
| Password en rockyou (primeros 5,4 M) | ❌ |
| Clave derivada del propio MIDI (bytes, sha256, md5, hex) | ❌ |
| XOR del buffer con salt / notas / velocidades / nombres de pista | ❌ |
| Otros cifrados openssl (des3, bf, cast5, camellia, aria, sm4, seed, rc2) con VF0317 y variantes | ❌ |
| Password vacía / salt como IV / salt como password | ❌ |

## 4. Pistas del enunciado (sin explotar del todo)

- «**No busques lo que cambia. Busca cómo regresa**» → apunta a **retorno/retrogradación/repetición**.
  El candidato más fuerte pendiente: comparar los bloques que **vuelven** (m21-28 vs m49-56) y
  codificar las diferencias (patrón simétrico ±2, ±4 ya observado en m24/m52 y m25/m53).
- El salt **`VF0317!!`** parece una **contraseña puesta en el campo salt** (8 bytes ASCII elegidos a
  mano). Probar a generar el buffer con `-S`/salt fijo distinto del que quedó, o a fuerza bruta
  sobre `VF0317` **como salt incorrecto** (el salt real podría ser otro y éste la password).
- `Violin` (canal 6, fuera de orden respecto a Guitar=4/Bass=5) y `Electric Guitar` son los
  "fantasmas": entran tarde (m41 y m21) y con las dinámicas más altas.

## 5. Artefactos

En `%TEMP%\opencode\cadencia\`: `dump.py`, `explore1-3.py`, `sweep.py`, `bymeasure.py`, `returns.py`,
`permeasure.py`, `veltable.py`, `eot.py`, `micro.py`, `patterns.py`, `counts.py`, `release.py`,
`canon.py`, `bitrepeat.py`, `crack.py` (rockyou), `melody_pw.py`, `combo.py`, `midikey.py`, `xor.py`,
`variants.py`, `c1-c5.sh`.

## 6. Siguiente paso recomendado

1. Diff nota a nota de los bloques que **regresan** (m21-28 → m49-56; m41-47 → m49-55) y codificar
   los intervalos de diferencia como letras/números.
2. Probar la generación inversa: crear buffers `openssl` con salt conocido y password candidata y
   comparar los primeros bytes con `8c d9 1e 55` (permite *verificar* la password sin depender del
   padding).
3. Si el autor usó un salt **aleatorio** y sólo puso `VF0317` como password, la decodificación debe
   salir con `-S` correcto: probar el salt implícito en el header pero con `-md md5`/`-pbkdf2`/
   `-iter N` (OpenSSL 1.1+ usa `-pbkdf2` por defecto en algunas builds).
