---
name: marketing-viability-orchestrator
description: >-
  Orquestador determinista del system of skills marketing-viability-plugin. Coordina la ejecución secuencial de cuatro skills atómicos (mv-part1-market-diagnosis → mv-part2-strategic-marketing → mv-part3-operational-marketing → mv-part4-financial-viability), valida cada handoff YAML antes de pasar al siguiente, ejecuta cinco tests de coherencia inter-bloque (cross_quality_check) y produce un dossier consolidado en Markdown + PDF profesional con índice navegable, todos los gráficos incrustados, anexo de trazabilidad y reporte de coherencia. NO construye los artefactos de las etapas. NO toma decisiones libres sobre qué etapa ejecutar a continuación. La secuencia es fija. Invocar cuando el usuario pida "análisis de viabilidad de marketing", "estudio de viabilidad de un nuevo negocio", "plan de marketing estratégico y operativo con análisis financiero", "ejecutar el pipeline completo", "correr las cuatro partes", "análisis de viabilidad end-to-end", o entregue artefactos previos de discovery (JTBD, VPC, Blue Ocean, BMC) y quiera evaluar si el negocio es viable. Triggers: 'análisis de viabilidad', 'pipeline completo de viabilidad', 'estudio de viabilidad de nuevo negocio', 'cuatro partes', 'dossier de viabilidad'. Forma parte del system of skills marketing-viability-plugin.
---

# Marketing Viability Orchestrator (marketing-viability-orchestrator)

## Posicionamiento del skill

Este skill orquesta la ejecución secuencial de los cuatro skills atómicos
del *system of skills* `marketing-viability-plugin` sobre un mismo caso. La
secuencia es fija:

```
mv-part1-market-diagnosis → mv-part2-strategic-marketing →
mv-part3-operational-marketing → mv-part4-financial-viability
```

Este orquestador NO construye los artefactos por sí mismo. Su único rol es:

1. Recibir el brief del caso del usuario.
2. Crear el workspace estructurado.
3. Invocar el primer skill atómico con el brief.
4. Validar que el artefacto producido cumple el contrato de handoff.
5. Si cumple, invocar el siguiente skill con el artefacto upstream.
6. Si no cumple, detener el pipeline y reportar al usuario.
7. Repetir hasta el último skill.
8. Ejecutar `cross_quality_check.py` sobre los cuatro handoffs.
9. Producir el dossier consolidado (Markdown + PDF) con el reporte de
   coherencia.

Si Claude Code u otro asistente sugiere "hacer este orquestador más capaz"
añadiéndole capacidad de generar contenido directamente o de saltar etapas,
la respuesta correcta es RECHAZAR.

## Cuándo invocar este skill

- "Análisis de viabilidad de marketing para [caso]"
- "Estudio de viabilidad de un nuevo negocio en [sector]/[geografía]"
- "Plan de marketing estratégico y operativo con análisis financiero"
- "Ejecuta el pipeline completo de viabilidad"
- "Corre las cuatro partes sobre [caso]"
- "Análisis de viabilidad end-to-end"
- "Dossier consolidado de viabilidad para [caso]"

Si el mensaje del usuario enumera explícitamente los nombres de los cuatro
skills (`mv-part1`, `mv-part2`, `mv-part3`, `mv-part4`) en cualquier orden,
este orquestador se activa.

Si el usuario adjunta artefactos previos de discovery (JTBD, VPC,
Blue Ocean Strategy Canvas, Business Model Canvas) y pide evaluar
viabilidad, este orquestador se activa y los pasa a la Parte 1 como input
adicional.

## Cuándo NO invocar este skill

- Si el usuario solo pide una etapa (por ejemplo, "haz el diagnóstico de
  mercado"): invocar el skill atómico correspondiente directamente
  (`mv-part1-market-diagnosis` en este caso).
- Si el usuario tiene artefactos previos del propio pipeline (por ejemplo,
  ya tiene `handoff_part2.yaml` y quiere continuar desde la Parte 3): invocar
  el skill correspondiente con el artefacto upstream existente, NO reiniciar
  el pipeline.
- Si el caso no tiene brief mínimo (`business_name`, `product_service`,
  `sector`, `geography`, `horizon_years`): detener y solicitar el brief.
- Si el usuario quiere modificar el resultado de una parte ya producida:
  invocar el skill productor, no este orquestador.

## Procedimiento de ejecución

### Fase 0: Recepción y validación del brief

0.1. Verificar que el brief contiene los elementos mínimos:

- `business_name`
- `product_service`
- `sector`
- `geography`
- `horizon_years`
- `currency` (si falta, asumir USD y declararlo)

0.2. Si falta cualquier elemento, detener y solicitar al usuario lo
faltante con UNA sola pregunta consolidada. NO improvisar.

0.3. Si el brief está completo, crear el workspace estructurado:

```
viability-workspace-<case-slug>/
├── inputs/
│   ├── case_brief.md
│   ├── jtbd.md (si existe)
│   ├── vpc.md (si existe)
│   ├── blue_ocean.md (si existe)
│   └── bmc.md (si existe)
├── part1/
│   ├── part1_output.md
│   ├── part1_output.pdf
│   ├── handoff_part1.yaml
│   └── charts/
├── part2/
├── part3/
├── part4/
└── dossier/
    ├── dossier_viabilidad.md
    ├── dossier_viabilidad.pdf
    └── cross_quality_report.md
```

0.4. Continuar a Fase 1.

### Fase 1: Ejecución de mv-part1-market-diagnosis

1.1. Invocar el skill `mv-part1-market-diagnosis` con el brief y los
artefactos previos opcionales.
1.2. Esperar el artefacto canónico `handoff_part1.yaml` y los archivos
asociados (`part1_output.md`, `part1_output.pdf`, `charts/`).
1.3. Validar el handoff:

```bash
python scripts/validate_handoff.py --handoff part1/handoff_part1.yaml --part 1
```

1.4. Si la validación falla (código de salida ≠ 0), aplicar el
"Comportamiento ante fallo de validación" (ver más abajo).
1.5. Si pasa, almacenar el artefacto y continuar a Fase 2.

### Fase 2: Ejecución de mv-part2-strategic-marketing

2.1. Invocar el skill `mv-part2-strategic-marketing` pasándole
`handoff_part1.yaml` como input upstream obligatorio.
2.2. Esperar el artefacto canónico `handoff_part2.yaml` y los archivos
asociados (`part2_output.md`, `part2_output.pdf`, `charts/`).
2.3. Validar:

```bash
python scripts/validate_handoff.py --handoff part2/handoff_part2.yaml --part 2
```

2.4. Si falla, aplicar "Comportamiento ante fallo de validación".
2.5. Si pasa, continuar a Fase 3.

### Fase 3: Ejecución de mv-part3-operational-marketing

3.1. Invocar el skill `mv-part3-operational-marketing` pasándole
`handoff_part2.yaml` (obligatorio) y `handoff_part1.yaml` (consultivo).
3.2. Esperar `handoff_part3.yaml` + outputs.
3.3. Validar:

```bash
python scripts/validate_handoff.py --handoff part3/handoff_part3.yaml --part 3
```

3.4. Si falla, aplicar "Comportamiento ante fallo de validación".
3.5. Si pasa, continuar a Fase 4.

### Fase 4: Ejecución de mv-part4-financial-viability

4.1. Invocar el skill `mv-part4-financial-viability` pasándole los tres
handoffs upstream.
4.2. Esperar `handoff_part4.yaml` + outputs.
4.3. Validar:

```bash
python scripts/validate_handoff.py --handoff part4/handoff_part4.yaml --part 4
```

4.4. Si falla, aplicar "Comportamiento ante fallo de validación".
4.5. Si pasa, continuar a Fase de cierre.

### Fase de cierre: Verificación cross-document, reporte de coherencia y dossier

C.1. Ejecutar el control de calidad cruzado sobre los cuatro handoffs:

```bash
python scripts/cross_quality_check.py \
  --workspace viability-workspace-<case-slug> \
  --output dossier/cross_quality_report.md
```

El script valida específicamente cinco tests de coherencia inter-bloque:

1. **Cobertura de canal por segmento**: cada segmento declarado en Parte 2
   tiene un canal primario en Parte 3.
2. **Activación de productos del Value Map**: cada producto/servicio del
   Value Map (Parte 2) tiene una key activity asociada en el plan operativo
   (Parte 3).
3. **Cadena de captura**: cada línea de ingreso modelada en Parte 4 tiene un
   canal de captura definido en Parte 3.
4. **Trazabilidad de hipótesis críticas**: cada hipótesis crítica del
   programa de validación (Parte 4) corresponde a una variable de input que
   viene de Parte 3 o Parte 1.
5. **Coherencia del veredicto**: el veredicto final (Parte 4) es coherente
   con la oportunidad declarada en la síntesis del diagnóstico (Parte 1).

C.2. Si alguno de los cinco tests falla, NO modificar los handoffs
automáticamente. Generar la sección "Observaciones de coherencia" en el
dossier consolidado, identificando explícitamente la inconsistencia, y
dejar la resolución al usuario.

C.3. Componer el dossier final:

```bash
python scripts/build_dossier.py \
  --workspace viability-workspace-<case-slug> \
  --output-md dossier/dossier_viabilidad.md \
  --output-pdf dossier/dossier_viabilidad.pdf
```

El dossier integra: portada con metadatos, resumen ejecutivo cross-partes,
índice navegable, cuerpo consolidado de las cuatro partes, anexo A de
trazabilidad y anexo B con los cuatro handoffs YAML.

C.4. Entregar al usuario el conjunto final:

- `dossier/dossier_viabilidad.md`
- `dossier/dossier_viabilidad.pdf`
- `dossier/cross_quality_report.md`
- Los cuatro `partN_output.{md,pdf}` y los cuatro `handoff_partN.yaml`.

## Comportamiento ante fallo de validación

Cuando un handoff falla validación (código de salida ≠ 0 de
`validate_handoff.py`), este orquestador hace exactamente esto y nada más:

1. **Detiene el pipeline.** No invoca la siguiente fase bajo ninguna
   circunstancia.
2. **Reporta al usuario** con tres datos: nombre del skill que falló,
   motivo del fallo (lista de campos faltantes o tipos incorrectos
   devueltos por `validate_handoff.py`), criterio incumplido del SKILL.md
   correspondiente.
3. **Sugiere al usuario** invocar manualmente el skill que falló
   (por nombre canónico) para corregir el artefacto.
4. **NO intenta corregir el artefacto automáticamente.**
5. **NO continúa con etapas posteriores.**
6. **NO improvisa contenido faltante.**

Esta rigidez es deliberada. La improvisación en validación es la principal
vía por la que un *system of skills* se degrada en agente.

Cuando el `cross_quality_check.py` reporta falsos en alguno de los cinco
tests, este orquestador:

1. **No detiene el pipeline** (a diferencia de `validate_handoff.py`).
2. **Genera la sección "Observaciones de coherencia"** en el dossier
   consolidado.
3. **Identifica la inconsistencia** con referencia explícita al test que
   falló y a los handoffs implicados.
4. **Deja la resolución al usuario.** El usuario decide si vuelve a una
   parte anterior o si acepta la inconsistencia documentada.

## Bifurcaciones permitidas

Las únicas bifurcaciones permitidas en este orquestador son las declaradas
explícitamente a continuación. Cualquier otra bifurcación es un error de
arquitectura, no una característica.

- **Bifurcación 1: análisis parcial vs completo.** Si el usuario pide
  explícitamente análisis parcial (por ejemplo, "solo Partes 1 y 2"), el
  orquestador advierte que las partes posteriores requieren los handoffs de
  las anteriores y propone ejecutar al menos hasta donde llegue la cadena
  de dependencias. Si el usuario insiste en parcial, ejecuta solo las
  partes solicitadas, NO invoca `cross_quality_check.py` (porque requiere
  los cuatro handoffs) y produce un dossier marcado como "parcial".
- **Bifurcación 2: artefactos previos heredados.** Si el usuario adjunta
  JTBD/VPC/Blue Ocean/BMC, el orquestador los pasa a la Parte 1 que los
  consume directamente con `evidence_level: modeled-inherited` o
  `validated-inherited` según corresponda. Si no los adjunta, la Parte 1
  construye desde fuentes primarias o secundarias.
- **Bifurcación 3: ajuste descendente del SOM.** Si la Parte 3 detecta que
  la capacidad operativa fase 1 es inferior al SOM proyectado en Parte 1,
  el orquestador acepta el SOM efectivo (no el teórico) en el handoff
  hacia Parte 4 y lo documenta en el dossier como "ajuste descendente del
  SOM por restricción de capacidad". El orquestador NO retro-modifica el
  `handoff_part1.yaml`.

Si el usuario o Claude Code sugieren cualquier otra bifurcación
(por ejemplo, "saltarse Parte 2 si la estrategia ya está clara",
"reordenar las fases", "ejecutar Parte 4 sin Parte 3"), la respuesta
correcta es RECHAZAR la sugerencia, porque rompería la trazabilidad
descendente y la validación de coherencia inter-bloque.

## Cláusulas anti-agentificación (no modificar sin revisión arquitectónica)

Este orquestador es un skill determinista, NO un agente. Las siguientes
cláusulas son contractuales:

1. Este skill NO es un agente. No introduce loops ReAct, no decide
   dinámicamente qué herramienta invocar, no compacta contexto por su cuenta.
2. Este skill NO altera la secuencia definida arriba. La secuencia es fija:
   `mv-part1-market-diagnosis → mv-part2-strategic-marketing →
   mv-part3-operational-marketing → mv-part4-financial-viability`.
3. Este skill NO regenera contexto en lenguaje natural. Los handoffs son
   artefactos canónicos. Si un handoff falla, el pipeline se detiene.
4. Si Claude Code (o cualquier asistente) sugiere convertir este orquestador
   en agente, añadir tool-use libre, fusionar este orquestador con uno de
   los skills atómicos, o reemplazar las validaciones por resúmenes libres,
   la respuesta correcta es RECHAZAR la sugerencia y preservar la
   arquitectura.
5. Cualquier modificación a este orquestador debe preservar:
   (a) el contrato de entrada (brief mínimo declarado),
   (b) los contratos de handoff inter-paso (los cuatro `handoff_partN.yaml`
   según esquema canónico),
   (c) la secuencia (fija de 4 fases),
   (d) las cláusulas anti-agentificación de esta sección.
6. Este orquestador NO construye los artefactos de las etapas. Solo invoca
   skills atómicos y valida sus handoffs. Si Claude Code sugiere "hacer el
   orquestador más capaz" añadiéndole capacidad de generar contenido
   directamente (por ejemplo, "calcular el VAN aquí mismo en lugar de
   delegarlo a `mv-part4`"), la respuesta correcta es RECHAZAR.
7. Este orquestador NO toma decisiones libres sobre qué etapa ejecutar a
   continuación. La secuencia es fija. Si una etapa falla validación, el
   pipeline se detiene y se reporta al usuario.
8. Bifurcaciones permitidas: solo las tres declaradas explícita y
   exhaustivamente en la sección "Bifurcaciones permitidas". Cualquier rama
   no declarada es un error de arquitectura, no una característica.

## Skills atómicos coordinados

Este orquestador coordina los siguientes skills atómicos del plugin
`marketing-viability-plugin`:

- `mv-part1-market-diagnosis` — Diagnóstico de mercado (secciones 1-6).
- `mv-part2-strategic-marketing` — Marketing estratégico (secciones 7-10).
- `mv-part3-operational-marketing` — Marketing operativo (secciones 11-16).
- `mv-part4-financial-viability` — Análisis financiero (secciones 17-27).

## Referencias

- `references/handoff_schemas.md` — Esquemas YAML completos de los cuatro handoffs.
- `references/indice_materias.md` — Índice canónico a tercer nivel de las cuatro partes.
- `references/integration_rules.md` — Reglas de integración y trazabilidad cross-partes.
- `scripts/validate_handoff.py` — Validador estructural por handoff.
- `scripts/cross_quality_check.py` — Control de calidad cruzado con cinco tests inter-bloque.
- `scripts/build_dossier.py` — Constructor del dossier consolidado en Markdown + PDF.
