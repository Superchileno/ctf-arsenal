---
name: ctf-ai-ml
description: 'Retos de IA y machine learning en CTF: ejemplos adversariales (FGSM, PGD, C&W),
  evasión de clasificadores, ataques a LLM (prompt injection, jailbreak, fuga de system prompt),
  extracción e inversión de modelos, análisis de pesos (safetensors, LoRA, HuggingFace) y
  envenenamiento de datos. Usar cuando el reto entregue un modelo, un notebook, pesos o un
  endpoint de LLM.
  Keywords: CTF AI, ML, adversarial examples, FGSM, PGD, model extraction, prompt injection,
  jailbreak, poisoning, safetensors, LoRA.'
domain: cybersecurity
subdomain: ctf
tags:
- ctf
- ai
- ml
- adversarial
- llm
- prompt-injection
version: '1.0'
author: auditoria-ia-v2
license: Apache-2.0
---

# CTF AI/ML — modelos adversariales y LLM

## Cuándo usarla

El reto entrega un modelo entrenado, pesos, un notebook, un clasificador remoto o
un endpoint de LLM con un objetivo que hay que cumplir.

## Procedimiento

1. Identificar el artefacto: `.pt`/`.pth`, `.safetensors`, `.onnx`, LoRA, `pickle` o API.
2. Inspeccionar formato y arquitectura antes de cargar: un `pickle` puede ejecutar código.
3. Definir el objetivo real: cambiar la clase, extraer pesos, leer un secreto del prompt
   o provocar una salida concreta.
4. Elegir familia: evasión (adversarial), extracción (queries), inversión (reconstruir
   entradas) o ataque lingüístico (LLM).
5. Medir con la métrica del reto; ajustar épsilon, pasos y restricciones.
6. Comparar pesos entre modelos cuando se busca un fine-tune malicioso.

## Material de profundidad

Repo upstream: <https://github.com/ljagiello/ctf-skills> (MIT, commit `a6106aaf`).
Clonar aparte y leer `skills/_src/ljagiello-ctf-skills/ctf-ai-ml/`; no se vendoriza en este repositorio.
(MIT).

| Tema | Archivo |
|---|---|
| Adversarial y gradientes | `adversarial-ml.md` |
| LLM y prompt injection | `llm-attacks.md` |
| Extracción y pesos | `model-attacks.md` |

Complementa `defending-against-prompt-injection-in-ctf-agents` (defensa) con la
cara ofensiva.

## Herramientas

`torch`, `numpy`, `scikit-learn`, `onnx`, `safetensors`, `transformers`,
`adversarial-robustness-toolbox`, `fickling`.

## Guardrails

- Cargar modelos ajenos en entorno aislado y sin red.
- No usar `torch.load` sobre archivos no confiables sin `weights_only`.
- Documentar la perturbación mínima que cambia la decisión.
