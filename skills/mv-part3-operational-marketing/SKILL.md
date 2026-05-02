---
name: mv-part3-operational-marketing
description: >-
  Produce el Marketing Operativo Aterrizado en Acciones (Parte 3) del análisis de viabilidad como entregable Markdown + PDF profesional con gráficos Python a 300 dpi. Cubre las secciones 11 a 16 del índice canónico (plan de producto con MVP y backlog 24 meses, plan de precios con tarifario por segmento y test de unidad económica, plan de canales con CAC blended cuantificado, plan de comunicación con embudo de conversión y campaña de lanzamiento presupuestada, capacidades operativas con cuellos de botella secuenciales y saltos de capacidad no lineales, calendario operativo consolidado con hitos mensuales año 1, trimestrales años 2-3 y semestrales años 4-5). Genera handoff_part3.yaml con los inputs cuantificados que mv-part4-financial-viability consume para construir el modelo financiero. Invocar como TERCER PASO del análisis de viabilidad, después de mv-part2-strategic-marketing y antes de mv-part4-financial-viability. Triggers: 'marketing operativo', 'plan de marketing 4P', 'marketing mix aterrizado', 'plan de canales y comunicación', 'CAC LTV', 'capacidades operativas', 'calendario operativo de lanzamiento'. Forma parte del system of skills marketing-viability-plugin; el orquestador es marketing-viability-orchestrator.
---

# Parte 3 — Marketing Operativo (mv-part3-operational-marketing)

## Posicionamiento del skill

Este skill es el tercer eslabón del *system of skills* `marketing-viability-plugin`.
Su única función es convertir las decisiones estratégicas de la Parte 2 en
planes operativos cuantificados (producto, precios, canales, comunicación,
capacidades, calendario) que la Parte 4 usará como inputs directos al modelo
financiero.

Este skill NO orquesta otros skills, NO ejecuta Parte 4, NO regenera el
posicionamiento ni la segmentación.

Principio rector: **cada decisión operativa debe (i) rastrearse a una
decisión estratégica de la Parte 2, (ii) producir un dato cuantificado que
la Parte 4 pueda usar como input directo, y (iii) ser realizable con las
capacidades efectivamente construibles.**

## Prerrequisito hard

Este skill requiere como input los artefactos canónicos siguientes:

```yaml
# Artefactos upstream obligatorios
upstream:
  - artefacto: handoff_part2.yaml
    obligatorio: true
    producido_por: mv-part2-strategic-marketing
  - artefacto: handoff_part1.yaml
    obligatorio: true            # consultado por trazabilidad
    producido_por: mv-part1-market-diagnosis
```

Si `handoff_part2.yaml` no existe o no cumple los criterios de aceptación
declarados en `mv-part2-strategic-marketing/SKILL.md`, este skill:

1. Detiene su ejecución.
2. Reporta al usuario el motivo del rechazo.
3. Sugiere invocar `mv-part2-strategic-marketing` antes.
4. NO improvisa el contenido faltante.

La validación se hace mecánicamente con:

```bash
python <orchestrator>/scripts/validate_handoff.py --handoff handoff_part2.yaml --part 2
```

## Cuándo invocar este skill

Triggers explícitos que activan este skill aisladamente:

- "Plan de marketing operativo (4P) para [caso] con estrategia ya definida"
- "Plan de canales y CAC blended sobre [caso]"
- "Definir tarifario por segmento y test de unidad económica"
- "Embudo de conversión y campaña de lanzamiento (90 días)"
- "Capacidades operativas y saltos de capacidad para [caso]"
- "Calendario operativo consolidado año 1-5"

Cuando el orquestador `marketing-viability-orchestrator` está activo, este
skill se invoca automáticamente como Fase 3 de la secuencia tras la
validación del handoff de Parte 2.

## Cuándo NO invocar este skill

- Si `handoff_part2.yaml` no existe: invocar primero
  `mv-part2-strategic-marketing`.
- Si el usuario quiere ejecutar el pipeline completo: invocar
  `marketing-viability-orchestrator`.
- Si el usuario quiere modificar el posicionamiento o la segmentación:
  invocar `mv-part2-strategic-marketing`.
- Si el caso ya tiene `handoff_part3.yaml` válido y solo se quiere correr el
  modelo financiero: pasar directamente a `mv-part4-financial-viability`.

## Procedimiento

Pasos imperativos en orden estricto. NO hay pasos opcionales ni
condicionales libres. Cualquier bifurcación está enumerada exhaustivamente.

### Paso 1: Validación del handoff de Parte 2

1.1. Verificar que `handoff_part2.yaml` existe y es legible.
1.2. Ejecutar `python <orchestrator>/scripts/validate_handoff.py --handoff
handoff_part2.yaml --part 2`. Si falla, detener y reportar.
1.3. Leer `handoff_part1.yaml` para acceder a `price_benchmark`,
`willingness_to_pay_declared` y `declared_to_revealed_correction_factor`.

### Paso 2: Plan de producto

2.1. MVP de lanzamiento: filtrar `value_proposition.products_services` de
Parte 2 con `category: "essential"`. NO incluir `secondary` ni `support`.
2.2. Portafolio inicial: líneas, referencias, alcance.
2.3. Backlog de incrementos a 24 meses con costo estimado por incremento.
2.4. Pricing por release.
2.5. Plan de testing técnico/clínico previo al lanzamiento.
2.6. KPIs de producto y umbrales objetivo.

### Paso 3: Plan de precios

3.1. Decisión de estructura: `linear` / `tiered` / `value_based` / `hybrid`.
Bifurcación enumerada.
3.2. Modalidad de cobro: `one_time` / `recurring_monthly` /
`recurring_annual` / `mixed`. Bifurcación enumerada.
3.3. Tarifario por segmento y por línea, con `price_low`, `price_mid`,
`price_high` y `currency`.

   **Regla de coherencia (no negociable):** cada `price_mid` debe estar
   dentro del rango de `willingness_to_pay_declared` de Parte 1 corregido
   por `declared_to_revealed_correction_factor`, y dentro del cuartil del
   `price_benchmark` de Parte 1 coherente con la estrategia genérica de
   Parte 2:
   - Si Parte 2 declaró `differentiation` o `focus_differentiation`: precio
     mid en cuartil alto (Q3-Q4) del benchmark.
   - Si Parte 2 declaró `cost_leadership` o `focus_cost`: precio mid en
     cuartil bajo (Q1-Q2) del benchmark.

3.4. Política de descuentos y aprobación.
3.5. Política de revisión anual de precios.
3.6. Promociones de lanzamiento.
3.7. Test de unidad económica del precio modelado: `avg_price -
avg_variable_cost = avg_contribution_margin`. Si margen contributivo
negativo, detener y reportar.

### Paso 4: Plan de canales

4.1. Mapa de canales por fase del journey (awareness, evaluation, purchase,
delivery, after-sales). Canal primario y secundario en cada fase.
4.2. Plan operativo por canal con presupuesto mensual, volumen objetivo y
CAC por canal.
4.3. Cuantificación de CAC por canal: presupuesto del canal / leads
cualificados generados / tasa de conversión.
4.4. CAC blended ponderado por mix proyectado.

   **Regla de coherencia (no negociable):** los canales primarios deben ser
   coherentes con `targeting.coverage_decision` de Parte 2:
   - `concentrated`: 2-3 canales primarios focalizados, no diversificar.
   - `differentiated`: canales por segmento, evaluar trade-off de eficiencia.
   - `undifferentiated`: canales masivos.
   - `micromarketing`: canales hiperfocalizados por nicho.

### Paso 5: Plan de comunicación

5.1. Mensaje central derivado del `tagline` de Parte 2.
5.2. Mensajes secundarios mapeados a `pain_relievers` y `gain_creators` de
Parte 2.
5.3. Tono, estilo, identidad visual mínima.
5.4. Calendario editorial 12 meses.
5.5. Campaña de lanzamiento 90 días con presupuesto.
5.6. Embudo de conversión con tasas por etapa (low-high) cuantificadas.
5.7. Herramientas operativas (CRM, email, analítica).
5.8. Acciones de retención y desarrollo de cliente.

### Paso 6: Capacidades operativas

6.1. Cuellos de botella secuenciales (técnico, regulatorio, comercial).
6.2. Capacidad máxima por unidad de tiempo: la del cuello de botella más
restrictivo.
6.3. Estructura de costo unitario incremental por línea.
6.4. Saltos de capacidad no lineales (años 2-5) con CAPEX y OPEX
incrementales.

   **Loop de retroalimentación con Parte 1:** si la capacidad operativa
   fase 1 es inferior al SOM proyectado en Parte 1, prevalece la capacidad.
   Documentar como "ajuste descendente del SOM" y transmitir el SOM efectivo
   (no el teórico) en el handoff hacia Parte 4.

### Paso 7: Calendario operativo consolidado

7.1. Hitos mensuales del año 1.
7.2. Hitos trimestrales de los años 2-3.
7.3. Hitos semestrales de los años 4-5.
7.4. Dependencias entre hitos y ruta crítica.
7.5. Responsables y rituales de revisión.

### Paso 8: Generación de gráficos a 300 dpi

```bash
python scripts/generate_part3_charts.py --inputs chart_inputs.yaml --output-dir charts/
```

Produce ocho PNG canónicos:

1. `chart_01_funnel.png` — Embudo de conversión por canal.
2. `chart_02_cac.png` — CAC por canal y CAC blended.
3. `chart_03_capacity_vs_som.png` — Capacidad fase 1 vs SOM proyectado.
4. `chart_04_capacity_jumps.png` — Saltos de capacidad escalonados con CAPEX
   anotado.
5. `chart_05_pricing.png` — Tarifario por línea (boxplot horizontal con mid).
6. `chart_06_gantt_year1.png` — Gantt operativo año 1.
7. `chart_07_unit_cost.png` — Estructura de costo unitario por línea.
8. `chart_08_channels_journey.png` — Mapa de canales por fase del journey.

### Paso 9: Producción del handoff YAML

```bash
python scripts/build_handoff_part3.py --inputs handoff_inputs.yaml --output handoff_part3.yaml
```

### Paso 10: Validación del handoff propio

```bash
python <orchestrator>/scripts/validate_handoff.py --handoff handoff_part3.yaml --part 3
```

### Paso 11: Generación del PDF profesional

```bash
python scripts/build_part_pdf.py --md part3_output.md --charts charts/ --output part3_output.pdf
```

### Paso 12: Entrega

Devolver al usuario (o al orquestador):

- `part3_output.md`
- `part3_output.pdf`
- `handoff_part3.yaml`
- `charts/chart_01_*.png` ... `charts/chart_08_*.png`

NO inicia automáticamente la Parte 4. Eso es responsabilidad del
orquestador.

## Artefacto de salida

Esquema canónico declarado en `<orchestrator>/references/handoff_schemas.md`
sección "handoff_part3.yaml". Resumen:

```yaml
handoff_part3:
  version: "1.0"
  case_name: <string>
  date: <ISO-8601>
  source_handoffs: ["handoff_part1.yaml", "handoff_part2.yaml"]

  product_plan:
    mvp_definition: <string>
    initial_portfolio: [<...>]
    backlog_24m: [<...>]
    product_kpis: [<...>]

  pricing_plan:
    pricing_structure: "linear" | "tiered" | "value_based" | "hybrid"
    payment_modality: "one_time" | "recurring_monthly" | "recurring_annual" | "mixed"
    tariff_by_line: [<...>]   # cada uno con price_low, price_mid, price_high, currency
    discount_policy: <string>
    annual_review_policy: <string>
    launch_promotion: <string | "none">
    unit_economics_test: {avg_price, avg_variable_cost, avg_gross_margin_percent, avg_contribution_margin}

  channels_plan:
    journey_map: {awareness, evaluation, purchase, delivery, after_sales}
    channel_operations: [<...>]
    cac_blended: {year_1, year_2, year_3_5, currency}

  communication_plan:
    promise_central: <string>
    secondary_messages: [<string>]
    tone_style: <string>
    visual_identity_minimum: [<string>]
    editorial_calendar_year_1: [<...>]
    launch_campaign: {window_days, milestones, budget: {amount, currency}}
    funnel: {stages: [<...>], total_conversion: {low, high}}
    operational_tools: [<...>]
    retention_actions: [<string>]

  capacity_plan:
    bottlenecks_sequential: [<string>]
    max_capacity_phase_1: {<unidad>: {min, max}}
    unit_cost_structure: [<...>]
    capacity_jumps: [<...>]   # cada uno con year, action, capex_estimate, opex_increment

  operational_calendar:
    year_1_monthly_milestones: [<...>]
    year_2_3_quarterly: [<...>]
    year_4_5_semestral: [<...>]
    critical_path: [<string>]
    review_rituals: [<string>]

  required_fields_for_part4:
    - pricing_plan.tariff_by_line
    - pricing_plan.unit_economics_test
    - channels_plan.cac_blended
    - capacity_plan.max_capacity_phase_1
    - capacity_plan.unit_cost_structure
    - capacity_plan.capacity_jumps
    - communication_plan.launch_campaign.budget
    - operational_calendar.year_1_monthly_milestones
```

## Criterios de aceptación

El artefacto producido se considera válido si y solo si:

1. `pricing_plan.pricing_structure` es uno de los cuatro valores enumerados.
2. `pricing_plan.payment_modality` es uno de los cuatro valores enumerados.
3. `pricing_plan.tariff_by_line` tiene al menos un elemento, y cada
   `price_mid` está dentro del rango `willingness_to_pay_declared` de
   Parte 1 corregido por el factor declarado-revelado.
4. `pricing_plan.unit_economics_test.avg_contribution_margin > 0`. Si es
   negativo, el skill detiene el pipeline y reporta.
5. `channels_plan.cac_blended.year_1` está cuantificado en moneda.
6. `capacity_plan.max_capacity_phase_1` tiene al menos un cuello de botella
   con cuantificación numérica.
7. `capacity_plan.unit_cost_structure` cubre todas las líneas del
   `pricing_plan.tariff_by_line`.
8. `capacity_plan.capacity_jumps` cubre todos los años entre el año 2 y el
   horizonte declarado en Parte 1, o documenta explícitamente "sin saltos".
9. `communication_plan.promise_central` deriva del `tagline` de Parte 2
   (trazabilidad).
10. `operational_calendar.year_1_monthly_milestones` tiene exactamente 12
    elementos, uno por mes, cada uno con `owner` declarado.
11. La validación `python validate_handoff.py --handoff handoff_part3.yaml
    --part 3` retorna código 0.

## Reglas duras adicionales v1.1 (no modificar)

### Coherencia CAC blended <-> costo de canal real (no negociable)

El CAC blended declarado debe equivaler aproximadamente, anio por anio,
al cociente:

```
CAC_blended_Yn ~ sum(presupuesto_canal_anual_i_Yn) / volumen_capturado_Yn
```

donde `presupuesto_canal_anual_i` incluye salarios fijos del personal
comercial dedicado al canal (ej. director clinico-comercial, asistente
comercial, key account manager), no solo gasto variable de medios.
Documentar la verificacion en la seccion 13.7 del documento como tabla:

| Anio | Volumen Big Hire | Costo total canales | CAC implicito | CAC declarado | Delta |
|---|---|---|---|---|---|
| Y1 | ... | ... | ... | ... | ... |
| Y2 | ... | ... | ... | ... | ... |
| Y3 | ... | ... | ... | ... | ... |

Si el CAC implicito es > 2x el CAC declarado, REVISAR la mezcla de canales
o reasignar costos fijos de personal a infraestructura comercial. Un CAC
declarado que no se sostiene con la cuenta real es violacion de
coherencia y la Parte 4 lo detectara como inconsistencia.

### Coherencia funnel <-> volumen Big Hire

Las tasas declaradas del embudo, multiplicadas por leads top-of-funnel,
deben dar el mismo volumen de Big Hire que la proyeccion operativa por
ano. Si el embudo describe regimen ideal (Y4-Y5), rotularlo
explicitamente con DOS embudos:

```
Embudo Y4-Y5 (regimen estabilizado): 1000 leads -> 600 -> 300 -> 105 BH
Embudo Y2 (rampa):                     400 leads -> 180 ->  70 ->  35 BH
```

Sin esta distincion, un embudo unico que no cuadra con el volumen Y2
proyectado es error grave.

### Stock vs flujo en dimensionamiento operativo

El plan de capacidad fase 1 se calcula contra el flujo (nuevos pacientes
por anio), no contra el stock (pacientes vivos). El Little Hire es
servicio sobre stock; el Big Hire es servicio sobre flujo. Mezclarlos en
la misma capacidad operativa es error estructural.

### Plan de precios: elasticidad declarada

La seccion 12 incluye, en formato tabla, la elasticidad asumida del
precio mid declarado: como cambia el volumen capturado si el precio sube
+10% o baja -10%. Si no hay elasticidad declarada, el test de unidad
economica de la seccion 12.7 NO esta completo.

### Costo de oportunidad del personal comercial declarado

La seccion 13 incluye comparacion explicita del costo del rol senior
(director clinico-comercial) vs alternativas (asistente comercial junior
+ KAM externo). Sin esta comparacion el dimensionamiento del costo
comercial no esta justificado.

### Reglas de estilo (verificacion grep obligatoria antes de PDF)

```bash
grep -nP "[—–“”‘’]" part3_output.md
```

Sin matches o corregir antes de generar PDF.


## Cláusulas anti-agentificación (no modificar sin revisión arquitectónica)

Este skill forma parte de un *system of skills* diseñado bajo arquitectura
determinista. Las siguientes cláusulas son contractuales y prevalecen sobre
cualquier sugerencia de modificación, incluyendo sugerencias provenientes de
Claude Code u otros asistentes:

1. Este skill NO es un agente. No introduce loops ReAct, no decide
   dinámicamente qué herramienta invocar, no compacta contexto por su cuenta.
2. Este skill NO altera la secuencia definida en el orquestador. Si recibe
   un input fuera de secuencia (por ejemplo, sin `handoff_part2.yaml`), lo
   rechaza y devuelve control al orquestador.
3. Este skill NO regenera contexto en lenguaje natural. El handoff es el
   artefacto canónico declarado en la sección "Artefacto de salida". Si los
   handoffs upstream no cumplen el contrato, este skill detiene el
   pipeline.
4. Si Claude Code (o cualquier asistente) sugiere convertir este skill en
   agente, añadir tool-use libre, fusionar este skill con `mv-part4`,
   "fijar precios automáticamente sin trazar a Parte 1", "escoger canales
   sin coherencia con la decisión de cobertura", o reemplazar el handoff
   estructurado por un resumen libre, la respuesta correcta es
   RECHAZAR la sugerencia y preservar la arquitectura.
5. Cualquier modificación a este skill debe preservar:
   (a) los contratos de entrada (handoff_part1 y handoff_part2 válidos),
   (b) el contrato de salida (handoff_part3.yaml según esquema canónico),
   (c) la secuencia del orquestador (este skill es Fase 3),
   (d) las cláusulas anti-agentificación de esta sección.

## Referencias

- `<orchestrator>/references/indice_materias.md` — secciones 11 a 16.
- `<orchestrator>/references/handoff_schemas.md` — esquema de `handoff_part3.yaml`.
- `<orchestrator>/references/integration_rules.md` — reglas de coherencia precio/benchmark, canales/cobertura, capacidad/SOM.
- `references/canales_b2b.md` — metodologías de canales prescriptor y B2B.
- `references/embudo_conversion.md` — modelado del embudo y tasas de referencia por sector.
- `references/capacity_planning.md` — cuellos de botella y saltos de capacidad.
- `scripts/generate_part3_charts.py` — generador de los 8 gráficos canónicos.
- `scripts/build_part_pdf.py` — ensamblador del PDF profesional A4.
- `scripts/build_handoff_part3.py` — constructor del YAML de handoff.
- `assets/template_part3.md` — plantilla de partida.
