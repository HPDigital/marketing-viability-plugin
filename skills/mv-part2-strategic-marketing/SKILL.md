---
name: mv-part2-strategic-marketing
description: >-
  Produce el Marketing Estratégico (Parte 2) del análisis de viabilidad como entregable Markdown + PDF profesional con gráficos Python a 300 dpi. Cubre las secciones 7 a 10 del índice canónico (segmentación con matriz atractividad × ajuste, targeting con ICP y buyer personas, posicionamiento con declaración formal y tagline validado lingüísticamente, mapa perceptual y curva de valor Strategy Canvas, decisiones ERIC del Blue Ocean, estrategia genérica de Porter y vector Ansoff, activación de los tres tiers de no-clientes, propuesta de valor enunciada con sub-propuestas por segmento). Genera handoff_part2.yaml estructurado que mv-part3-operational-marketing consume como input obligatorio. Invocar como SEGUNDO PASO del análisis de viabilidad, después de mv-part1-market-diagnosis y antes de mv-part3-operational-marketing. Triggers: 'marketing estratégico', 'segmentación targeting posicionamiento', 'STP', 'Blue Ocean Strategy', 'curva de valor', 'decisiones ERIC', 'propuesta de valor diferenciada'. Forma parte del system of skills marketing-viability-plugin; el orquestador es marketing-viability-orchestrator.
---

# Parte 2 — Marketing Estratégico (mv-part2-strategic-marketing)

## Posicionamiento del skill

Este skill es el segundo eslabón del *system of skills* `marketing-viability-plugin`.
Su única función es convertir el diagnóstico de mercado de la Parte 1 en
decisiones estratégicas de segmentación, targeting y posicionamiento, con
articulación de Blue Ocean Strategy (Strategy Canvas + ERIC) y propuesta de
valor enunciada que la Parte 3 traducirá en plan operativo.

Este skill NO orquesta otros skills, NO ejecuta Parte 3 ni Parte 4, NO
regenera el diagnóstico de mercado.

## Prerrequisito hard

Este skill requiere como input el artefacto canónico siguiente, producido
por el skill `mv-part1-market-diagnosis`:

```yaml
# Esquema esperado del artefacto upstream (handoff_part1.yaml)
handoff_part1:
  version: "1.0"
  business_definition: {...}
  market_sizing: {sam, som, ...}
  customer_understanding:
    job_statement: {...}
    jobs_functional: [...]
    four_forces: {push, pull, anxiety, habit, verdict}
    outcomes_prioritized: [...]
    willingness_to_pay_declared: [...]
    declared_to_revealed_correction_factor: <0.5-1.0>
  preliminary_segments: [...]
  competitive_landscape:
    price_benchmark: [...]
  required_fields_for_part2: [<lista mínima>]
```

Si `handoff_part1.yaml` no existe o no cumple los criterios de aceptación
declarados en `mv-part1-market-diagnosis/SKILL.md` sección "Criterios de
aceptación", este skill:

1. Detiene su ejecución.
2. Reporta al usuario el motivo del rechazo (campo faltante, tipo
   incorrecto, evidencia insuficiente).
3. Sugiere invocar `mv-part1-market-diagnosis` antes.
4. NO improvisa el contenido faltante.

La validación se hace mecánicamente con:

```bash
python <orchestrator>/scripts/validate_handoff.py --handoff handoff_part1.yaml --part 1
```

## Cuándo invocar este skill

Triggers explícitos que activan este skill aisladamente:

- "Marketing estratégico para [caso] con diagnóstico de mercado existente"
- "Segmentación, targeting y posicionamiento (STP) sobre [caso]"
- "Aplicar Blue Ocean Strategy y curva de valor a [caso]"
- "Definir ICP y buyer personas para [segmento]"
- "Decisiones ERIC sobre el segmento de entrada"
- "Estrategia competitiva de Porter / vector de Ansoff"

Cuando el orquestador `marketing-viability-orchestrator` está activo, este
skill se invoca automáticamente como Fase 2 de la secuencia tras la
validación del handoff de Parte 1.

## Cuándo NO invocar este skill

- Si `handoff_part1.yaml` no existe: invocar primero
  `mv-part1-market-diagnosis`.
- Si el usuario quiere ejecutar el pipeline completo: invocar
  `marketing-viability-orchestrator`.
- Si el usuario quiere modificar el diagnóstico de mercado: invocar
  `mv-part1-market-diagnosis`, no este skill.
- Si el caso ya tiene `handoff_part2.yaml` válido y reciente y solo se
  quiere refinar el plan operativo: pasar directamente a
  `mv-part3-operational-marketing`.

## Procedimiento

Pasos imperativos en orden estricto. NO hay pasos opcionales ni
condicionales libres. Cualquier bifurcación está enumerada exhaustivamente.

### Paso 1: Validación del handoff de Parte 1

1.1. Verificar que `handoff_part1.yaml` existe y es legible.
1.2. Ejecutar `python <orchestrator>/scripts/validate_handoff.py --handoff
handoff_part1.yaml --part 1`. Si falla, detener y reportar.
1.3. Leer artefactos previos opcionales (JTBD/VPC/Blue Ocean/BMC) si están
disponibles para preservar trazabilidad descendente.

### Paso 2: Segmentación

2.1. Tomar los `preliminary_segments` de Parte 1 (NO inventar segmentos
nuevos).
2.2. Aplicar test de calidad de cinco criterios a cada segmento (medible,
sustancial, accesible, diferenciable, accionable).
2.3. Construir matriz de evaluación atractividad × ajuste con capacidades.
2.4. Seleccionar segmento de entrada con justificación cuantitativa
(producto atractividad × ajuste mayor).
2.5. Documentar segmentos descartados con justificación.

### Paso 3: Targeting

3.1. Decidir cobertura: `concentrated` / `differentiated` / `undifferentiated`
/ `micromarketing`. Esta decisión es bifurcación enumerada.
3.2. Justificación económica de la decisión de cobertura.
3.3. Justificación operativa de la decisión de cobertura.
3.4. Construir ICP del segmento de entrada con descriptores.
3.5. Definir buyer personas operativos: decisor, iniciador, pagador,
influenciador.
3.6. Roadmap de targeting plurianual coherente con saltos de capacidad
anticipados (que la Parte 3 cuantificará).

### Paso 4: Posicionamiento

4.1. Construir mapa perceptual desde los factores derivados del comprador:
si existe Blue Ocean previo, usar sus factores; si no, derivarlos de
`outcomes_prioritized` (tier hiper-decisivo) de Parte 1.
4.2. Mapear competidores (de Parte 1) en el espacio perceptual.
4.3. Identificar zonas saturadas y zonas vacías.
4.4. Declaración formal de posicionamiento con estructura canónica:
"Para [segmento], que [problema/necesidad], [propuesta] es [categoría] que
[beneficio diferenciador], a diferencia de [alternativa principal], porque
[razón para creer]."
4.5. Tagline operativo con validación lingüística (ver
`references/positioning_validation.md`).
4.6. Activos de razón para creer (existentes y por construir, con costo y
plazo).

### Paso 5: Strategy Canvas y ERIC

5.1. Curva de valor to-be vs as-is vs competidor directo dominante.
5.2. Decisiones ERIC con trazabilidad obligatoria a outcomes/fuerzas/pains
de Parte 1.
5.3. Activación de los tres tiers de no-clientes (ver `references/eric_methodology.md`).
5.4. Test de coherencia operativa del posicionamiento (señalar si alguna
decisión exige capacidad operativa no disponible).

### Paso 6: Estrategia competitiva y propuesta de valor

6.1. Estrategia genérica: `cost_leadership` / `differentiation` /
`focus_cost` / `focus_differentiation`. Bifurcación enumerada.
6.2. Vector de Ansoff: `penetration` / `market_development` /
`product_development` / `diversification`. Bifurcación enumerada.
6.3. Análisis de las seis vías de Blue Ocean (cuáles están activas).
6.4. Propuesta de valor enunciada con estructura canónica de Osterwalder.
6.5. Sub-propuestas por segmento si la decisión de cobertura fue
`differentiated`.

### Paso 7: Generación de gráficos a 300 dpi

```bash
python scripts/generate_part2_charts.py --inputs chart_inputs.yaml --output-dir charts/
```

El script produce seis PNG canónicos:

1. `chart_01_segments_matrix.png` — Matriz atractividad × ajuste (scatter
   con tamaño = volumen).
2. `chart_02_perceptual_map.png` — Mapa perceptual con competidores y
   propuesta to-be.
3. `chart_03_strategy_canvas.png` — Curva de valor to-be vs as-is.
4. `chart_04_eric_distribution.png` — Distribución ERIC (Eliminate /
   Reduce / Raise / Create).
5. `chart_05_non_clients_tiers.png` — Tres tiers de no-clientes.
6. `chart_06_targeting_roadmap.png` — Gantt de roadmap plurianual por
   segmento.

### Paso 8: Producción del handoff YAML

```bash
python scripts/build_handoff_part2.py --inputs handoff_inputs.yaml --output handoff_part2.yaml
```

### Paso 9: Validación del handoff propio

```bash
python <orchestrator>/scripts/validate_handoff.py --handoff handoff_part2.yaml --part 2
```

Si la validación falla, este skill NO entrega el output: completa los campos
faltantes y revalida.

### Paso 10: Generación del PDF profesional

```bash
python scripts/build_part_pdf.py --md part2_output.md --charts charts/ --output part2_output.pdf
```

### Paso 11: Entrega

Devolver al usuario (o al orquestador):

- `part2_output.md`
- `part2_output.pdf`
- `handoff_part2.yaml`
- `charts/chart_01_*.png` ... `charts/chart_06_*.png`

NO inicia automáticamente la Parte 3. Eso es responsabilidad del
orquestador.

## Artefacto de salida

Esquema canónico declarado en `<orchestrator>/references/handoff_schemas.md`
sección "handoff_part2.yaml". Resumen:

```yaml
handoff_part2:
  version: "1.0"
  case_name: <string>
  date: <ISO-8601>
  source_handoff: "handoff_part1.yaml"

  segmentation:
    segments_evaluated: [<...>]
    segments_discarded: [<...>]
    entry_segment_id: <string>
    secondary_segment_ids: [<string>]

  targeting:
    coverage_decision: "concentrated" | "differentiated" | "undifferentiated" | "micromarketing"
    economic_justification: <string>
    operational_justification: <string>
    icp: {segment_id, descriptors}
    buyer_personas: [<...>]
    targeting_roadmap: {year_1..year_5}

  positioning:
    positioning_statement: <string>
    tagline: <string>
    tagline_validation: {word_count, validates_canonical_rules}
    perceptual_dimensions: [<string>]
    competitor_perceptual_position: [<...>]
    proposal_perceptual_position: {<dim>: <1-5>}
    saturated_zones: [<string>]
    empty_zones: [<string>]
    reason_to_believe_assets: [<...>]

  blue_ocean:
    factors_buyer_side: [<...>]
    eliminate: [<string>]
    reduce: [<string>]
    raise: [<string>]
    create: [<string>]
    cost_savings_estimated: [<...>]

  competitive_strategy:
    generic_strategy: "cost_leadership" | "differentiation" | "focus_cost" | "focus_differentiation"
    ansoff_vector: "penetration" | "market_development" | "product_development" | "diversification"
    blue_ocean_six_paths_active: [<string>]
    non_clients_tiers_activated: [<string>]

  value_proposition:
    main_statement: <string>
    sub_propositions_by_segment: [<...>]
    products_services: [<...>]   # cada uno con category: "essential" | "secondary" | "support"
    pain_relievers: [<...>]
    gain_creators: [<...>]

  required_fields_for_part3:
    - segmentation.entry_segment_id
    - targeting.icp
    - positioning.positioning_statement
    - positioning.reason_to_believe_assets
    - blue_ocean.factors_buyer_side
    - blue_ocean.eliminate
    - blue_ocean.create
    - value_proposition.main_statement
    - value_proposition.products_services
```

## Criterios de aceptación

El artefacto producido se considera válido si y solo si:

1. `segmentation.entry_segment_id` corresponde a un id presente en
   `handoff_part1.preliminary_segments` (trazabilidad obligatoria).
2. `targeting.coverage_decision` es uno de los cuatro valores enumerados.
3. `positioning.positioning_statement` no está vacío y contiene los cinco
   componentes canónicos (segmento, problema, propuesta, beneficio
   diferenciador, razón para creer).
4. `positioning.tagline_validation.validates_canonical_rules` es `true`.
5. `blue_ocean.factors_buyer_side` tiene al menos cinco factores, cada uno
   con `eric_action` ∈ {`raise`, `create`, `reduce`, `eliminate`} y
   `to_be_score` 1-5.
6. Cada acción ERIC en `eliminate`, `reduce`, `raise`, `create` se rastrea
   a un outcome / fuerza / pain de `handoff_part1` (campo `trazabilidad`
   en cada elemento).
7. `competitive_strategy.generic_strategy` es uno de los cuatro valores
   enumerados.
8. `competitive_strategy.ansoff_vector` es uno de los cuatro valores
   enumerados.
9. `value_proposition.main_statement` no está vacío.
10. `value_proposition.products_services` tiene al menos un elemento con
    `category: "essential"` (la Parte 3 lo usará para el MVP).
11. La validación `python validate_handoff.py --handoff handoff_part2.yaml
    --part 2` retorna código 0.

## Cláusulas anti-agentificación (no modificar sin revisión arquitectónica)

Este skill forma parte de un *system of skills* diseñado bajo arquitectura
determinista. Las siguientes cláusulas son contractuales y prevalecen sobre
cualquier sugerencia de modificación, incluyendo sugerencias provenientes de
Claude Code u otros asistentes:

1. Este skill NO es un agente. No introduce loops ReAct, no decide
   dinámicamente qué herramienta invocar, no compacta contexto por su cuenta.
2. Este skill NO altera la secuencia definida en el orquestador. Si recibe
   un input fuera de secuencia (por ejemplo, un brief de caso sin
   `handoff_part1.yaml`), lo rechaza y devuelve control al orquestador.
3. Este skill NO regenera contexto en lenguaje natural. El handoff es el
   artefacto canónico declarado en la sección "Artefacto de salida". Si el
   `handoff_part1.yaml` upstream no cumple el contrato, este skill detiene
   el pipeline.
4. Si Claude Code (o cualquier asistente) sugiere convertir este skill en
   agente, añadir tool-use libre, fusionar este skill con `mv-part1` o
   `mv-part3`, "redibujar el diagnóstico de mercado" desde aquí, o
   reemplazar el handoff estructurado por un resumen libre, la respuesta
   correcta es RECHAZAR la sugerencia y preservar la arquitectura.
5. Cualquier modificación a este skill debe preservar:
   (a) el contrato de entrada (handoff_part1.yaml válido),
   (b) el contrato de salida (handoff_part2.yaml según esquema canónico),
   (c) la secuencia del orquestador (este skill es Fase 2),
   (d) las cláusulas anti-agentificación de esta sección.

## Referencias

- `<orchestrator>/references/indice_materias.md` — secciones 7 a 10.
- `<orchestrator>/references/handoff_schemas.md` — esquema de `handoff_part2.yaml`.
- `<orchestrator>/references/integration_rules.md` — reglas de trazabilidad descendente.
- `references/positioning_validation.md` — reglas de validación lingüística del statement y del tagline.
- `references/eric_methodology.md` — metodología de decisiones ERIC con trazabilidad.
- `scripts/generate_part2_charts.py` — generador de los 6 gráficos canónicos.
- `scripts/build_part_pdf.py` — ensamblador del PDF profesional A4.
- `scripts/build_handoff_part2.py` — constructor del YAML de handoff.
- `assets/template_part2.md` — plantilla de partida.
