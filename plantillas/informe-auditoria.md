# Plantilla — Informe de auditoría / pentesting

> Copiar a `<objetivo>/CONTEXTO.md` y completar. Evidencia siempre redactada.

## 1. Resumen ejecutivo

- **Cliente:**
- **Sistema evaluado:**
- **Periodo:**
- **Modalidad:**
- **Resultado global:** (n hallazgos: n críticos, n altos, n medios, n bajos)
- **Riesgo principal en una frase:**

## 2. Alcance y autorización

- Referencia a `authorization.md` y `scope.txt` (fecha, autorizante).
- Sistemas excluidos y por qué.
- Limitaciones: ventana horaria, credenciales entregadas, sistemas caídos.

## 3. Metodología

| Fase | Actividades | Herramientas |
|---|---|---|
| Reconocimiento |  |  |
| Enumeración |  |  |
| Explotación |  |  |
| Post-explotación |  |  |
| Revisión de configuración |  |  |

Marcos de referencia: OWASP WSTG / API Top 10, PTES, MITRE ATT&CK, NIST SP 800-115.

## 4. Hallazgos

### H-01 — <título>

| Campo | Valor |
|---|---|
| Severidad | Crítica / Alta / Media / Baja |
| Nivel de evidencia | L1 / L2 / L3 / L4 |
| CVSS 3.1 | x.x (`vector`) |
| CWE | CWE-xxx |
| Activo afectado |  |
| Autenticación requerida | No / Sí (rol) |

**Descripción**
...

**Prueba de concepto (reproducible)**

```bash
# comando o request exacto (datos redactados)
```

**Evidencia**

```
request / response relevante, credenciales enmascaradas
```

**Impacto**
...

**Remediación**

1. ...
2. ...

**Referencias:** OWASP, CWE, documentación del fabricante.

---

*(repetir el bloque por cada hallazgo)*

## 5. No explotado / pendiente

| Elemento | Motivo | Recomendación |
|---|---|---|
|  |  |  |

## 6. Fuera de alcance observado

Riesgos vistos en sistemas no autorizados: se reportan sin prueba activa.

## 7. Conclusiones

- Lo que quedó demostrado.
- Lo que **no** se puede afirmar (evitar «el sistema es seguro»).
- Prioridad de remediación sugerida (30/60/90 días).

## 8. Anexos

- `evidence/` — evidencia redactada.
- `solucion/` — scripts usados.
- Registro de actividad (fecha, comando, resultado).

## 9. Registro de cambios

| Fecha | Cambio | Backup |
|---|---|---|
|  |  |  |
