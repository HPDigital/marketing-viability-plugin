---
name: mv-part4-financial-viability
description: >-
  Produce el Análisis Financiero de Viabilidad (Parte 4 y final) del análisis de viabilidad como entregable Markdown + PDF profesional con gráficos Python a 300 dpi y modelo financiero opcional XLSX. Cubre las secciones 17 a 27 del índice canónico (estructura del modelo financiero, proyección de ingresos en escenarios base/pesimista/optimista, estructura de costos variables y fijos, plan de inversiones CAPEX, flujo de caja proyectado con punto de inflexión, indicadores de viabilidad VAN/TIR/payback/punto de equilibrio, métricas de unidad económica CAC/LTV/payback CAC/margen contributivo, análisis de sensibilidad con tornado chart sobre variables críticas, análisis de riesgos por categoría con matriz probabilidad × impacto, programa de validación con hipótesis críticas y umbrales paso/no-paso, veredicto financiero condicional con cronograma de desembolsos). Genera handoff_part4.yaml con el veredicto final que el orquestador integra en el dossier consolidado. Invocar como CUARTO Y ÚLTIMO PASO del análisis de viabilidad, después de mv-part3-operational-marketing. Triggers: 'análisis financiero de viabilidad', 'modelo financiero proyectado', 'VAN TIR payback', 'análisis de sensibilidad', 'veredicto de viabilidad', 'programa de validación previo a inversión'. Forma parte del system of skills marketing-viability-plugin; el orquestador es marketing-viability-orchestrator.
---

# Parte 4 — Análisis Financiero de Viabilidad (mv-part4-financial-viability)

## Posicionamiento del skill

Este skill es el cuarto y último eslabón del *system of skills*
`marketing-viability-plugin`. Su única función es construir el modelo
financiero proyectado a partir de los inputs operativos de la Parte 3,
calcular indicadores de viabilidad, ejecutar análisis de sensibilidad y
escenarios, identificar hipótesis críticas y emitir un veredicto financiero
**condicional**.

Este skill NO orquesta otros skills, NO regenera el plan operativo, y su
veredicto **no es una decisión de inversión** sino una evaluación
condicional sobre la base de las hipótesis cuantificadas a lo largo del
pipeline.

## Prerrequisito hard

Este skill requiere como input los artefactos canónicos siguientes:

```yaml
upstream:
  - artefacto: handoff_part3.yaml
    obligatorio: true
    producido_por: mv-part3-operational-marketing
  - artefacto: handoff_part2.yaml
    obligatorio: true            # consultado por trazabilidad de estrategia
    producido_por: mv-part2-strategic-marketing
  - artefacto: handoff_part1.yaml
    obligatorio: true            # consultado por SOM, fuerzas, riesgos aguas arriba
    producido_por: mv-part1-market-diagnosis
```

Si `handoff_part3.yaml` no existe o no cumple los criterios de aceptación
declarados en `mv-part3-operational-marketing/SKILL.md`, este skill:

1. Detiene su ejecución.
2. Reporta al usuario el motivo del rechazo.
3. Sugiere invocar `mv-part3-operational-marketing` antes.
4. NO improvisa el contenido faltante.

La validación se hace mecánicamente con:

```bash
python <orchestrator>/scripts/validate_handoff.py --handoff handoff_part3.yaml --part 3
```

## Cuándo invocar este skill

Triggers explícitos que activan este skill aisladamente:

- "Análisis financiero de viabilidad de [caso] con plan operativo cerrado"
- "Modelo financiero proyectado a 5 años para [caso]"
- "Calcular VAN, TIR, payback simple y descontado para [caso]"
- "Análisis de sensibilidad con tornado chart sobre [variable]"
- "Programa de validación previo a inversión con hipótesis críticas"
- "Veredicto de viabilidad condicional"

Cuando el orquestador `marketing-viability-orchestrator` está activo, este
skill se invoca automáticamente como Fase 4 (final) de la secuencia tras la
validación del handoff de Parte 3.

## Cuándo NO invocar este skill

- Si `handoff_part3.yaml` no existe: invocar primero
  `mv-part3-operational-marketing`.
- Si el usuario quiere ejecutar el pipeline completo o el dossier
  consolidado: invocar `marketing-viability-orchestrator`.
- Si el usuario quiere modificar tarifario, CAC, capacidades o calendario:
  invocar `mv-part3-operational-marketing`.

## Procedimiento

Pasos imperativos en orden estricto. NO hay pasos opcionales ni
condicionales libres. Cualquier bifurcación está enumerada exhaustivamente.

### Paso 1: Validación de inputs y construcción del esqueleto del modelo

1.1. Verificar que `handoff_part3.yaml` existe y es legible.
1.2. Ejecutar `python <orchestrator>/scripts/validate_handoff.py --handoff
handoff_part3.yaml --part 3`. Si falla, detener.
1.3. Leer `handoff_part1.yaml` (SOM efectivo, riesgos) y `handoff_part2.yaml`
(estrategia genérica, posicionamiento).
1.4. Definir horizonte y granularidad: año 1 mensual, años 2-3 trimestral,
años 4-5 semestral.
1.5. Establecer supuestos macro: inflación, tipo de cambio, tasa de
descuento.

   **Bifurcación enumerada de tasa de descuento por defecto:**
   - Mercado emergente con riesgo medio-alto: 15%.
   - Mercado desarrollado: 12%.
   - Sector muy volátil: 18-20%.
   - Documentar la elección.

### Paso 2: Proyección de ingresos

2.1. Por línea (de `pricing_plan.tariff_by_line` de Parte 3), por escenario,
con la granularidad requerida.
2.2. Volumen acotado por `capacity_plan.max_capacity_phase_1` hasta el
primer salto de capacidad.
2.3. Precio mid del tarifario.
2.4. Tres escenarios con factores convencionales:
   - **Base**: 1.0 × volumen, 1.0 × precio, 1.0 × costo.
   - **Pesimista**: 0.6 × volumen, 0.92 × precio, 1.08 × costo.
   - **Optimista**: 1.3 × volumen, 1.05 × precio, 0.97 × costo.

   Estos factores son convención del sistema; ajustables si el caso lo
   justifica con documentación explícita.

### Paso 3: Estructura de costos y gastos

3.1. Costos variables: replicar `unit_cost_structure` de Parte 3 (NO
inventar costos no declarados).
3.2. Costos fijos operativos: derivados del `capacity_plan`.
3.3. Costos comerciales y marketing: `cac_blended × volumen +
launch_campaign.budget` y presupuesto fijo de comunicación.
3.4. Costos corporativos: estructura mínima viable.
3.5. Costos financieros: si aplica financiación parcial.
3.6. Ahorros heredados de Blue Ocean: incorporar `cost_savings_estimated`
de Parte 2.

### Paso 4: Plan de inversiones CAPEX

4.1. CAPEX inicial: taller, stock, regulatorio, comercial (de Parte 3).
4.2. CAPEX expansión: replicar `capacity_jumps` de Parte 3.
4.3. Capital de trabajo permanente.

### Paso 5: Flujo de caja proyectado

5.1. Operativo, inversión, financiación, FCF.
5.2. Identificar mes de cash flow positivo sostenido (`cash_inflection_month`).
5.3. Tensiones estacionales de tesorería.

### Paso 6: Indicadores de viabilidad

6.1. VAN en los tres escenarios.
6.2. TIR en los tres escenarios.
6.3. Payback simple y payback descontado.
6.4. Punto de equilibrio en volumen y en valor, mes en que se alcanza.
6.5. Ratio cobertura de servicio de deuda si aplica.

### Paso 7: Métricas de unidad económica

7.1. CAC blended (de Parte 3).
7.2. LTV blended.
7.3. Ratio LTV/CAC con interpretación de salud (>3 sano, >5 holgado, <3
alerta).
7.4. Payback CAC en meses.
7.5. Margen contributivo por unidad.

### Paso 8: Análisis de sensibilidad

8.1. Identificar variables críticas: aquellas cuya variación de ±20% altera
materialmente el VAN (cambio de signo o caída > 30% del VAN base).
8.2. Tornado chart sobre VAN.
8.3. Umbrales de invalidación por variable.

### Paso 9: Análisis de riesgos

Por categoría: mercado, operativo, regulatorio, financiero, partnership.
Matriz probabilidad × impacto. Mitigaciones. Triggers de pivote.

### Paso 10: Programa de validación

10.1. Hipótesis críticas (4-8): cada una corresponde a una variable crítica
del análisis de sensibilidad.
10.2. Métodos de validación.
10.3. Presupuestos por trimestre.
10.4. Umbrales paso/no-paso.

### Paso 11: Veredicto financiero (bifurcación enumerada)

Aplicar criterios canónicos:

| Veredicto | Criterios |
|---|---|
| `viable` | VAN base > 0, TIR base > tasa descuento + 5pp, payback < 36 meses, LTV/CAC > 3, sensibilidad ±20% mantiene VAN positivo |
| `viable_with_observations` | VAN base > 0 pero alguna condición secundaria falla; requiere programa de validación previo |
| `marginal` | VAN base ligeramente positivo (< 10% del CAPEX inicial), alta sensibilidad a una sola variable; requiere pivote o renegociación |
| `not_viable` | VAN base ≤ 0 o sensibilidad muestra invalidación con variación moderada |

11.1. Necesidad de capital total.
11.2. Estructura de capital sugerida (equity, debt, partnership).
11.3. Cronograma de desembolsos por hito de validación.
11.4. Triggers de continuación, pivote o abandono.

### Paso 12: Generación de gráficos a 300 dpi

```bash
python scripts/generate_part4_charts.py --inputs chart_inputs.yaml --output-dir charts/
```

Produce nueve PNG canónicos:

1. `chart_01_revenue_scenarios.png` — Curva de ingresos por escenario.
2. `chart_02_ebitda_scenarios.png` — Curva de EBITDA por escenario.
3. `chart_03_cashflow_inflection.png` — FCF + acumulado con punto de
   inflexión.
4. `chart_04_tornado.png` — Tornado de sensibilidad sobre VAN.
5. `chart_05_breakeven.png` — Punto de equilibrio (volumen vs valor).
6. `chart_06_scenarios_comparison.png` — Tres escenarios sobre VAN/TIR/payback.
7. `chart_07_unit_economics.png` — CAC, LTV, ratio.
8. `chart_08_risk_matrix.png` — Matriz probabilidad × impacto.
9. `chart_09_validation_calendar.png` — Cronograma de desembolsos.

### Paso 13: Modelo financiero XLSX (opcional)

```bash
python scripts/build_financial_model_xlsx.py --inputs handoff_inputs.yaml --output financial_model.xlsx
```

### Paso 14: Producción del handoff YAML

```bash
python scripts/build_handoff_part4.py --inputs handoff_inputs.yaml --output handoff_part4.yaml
```

### Paso 15: Validación del handoff propio

```bash
python <orchestrator>/scripts/validate_handoff.py --handoff handoff_part4.yaml --part 4
```

### Paso 16: Generación del PDF profesional

```bash
python scripts/build_part_pdf.py --md part4_output.md --charts charts/ --output part4_output.pdf
```

### Paso 17: Entrega

Devolver al usuario (o al orquestador):

- `part4_output.md`
- `part4_output.pdf`
- `handoff_part4.yaml`
- `charts/chart_01_*.png` ... `charts/chart_09_*.png`
- `financial_model.xlsx` (opcional)

NO inicia automáticamente el dossier consolidado. Eso es responsabilidad del
orquestador, que ejecutará además el `cross_quality_check.py` antes de
consolidar.

## Artefacto de salida

Esquema canónico declarado en `<orchestrator>/references/handoff_schemas.md`
sección "handoff_part4.yaml". Resumen:

```yaml
handoff_part4:
  version: "1.0"
  case_name: <string>
  date: <ISO-8601>
  source_handoffs: ["handoff_part1.yaml", "handoff_part2.yaml", "handoff_part3.yaml"]

  financial_model:
    horizon_years: <integer>
    granularity: {year_1: "monthly", years_2_3: "quarterly", years_4_5: "semestral"}
    macro_assumptions: {inflation_annual, exchange_rate, discount_rate}

  revenue_projection: {by_line_by_year, total_by_year: {base, pessimistic, optimistic}}
  cost_structure: {variable_costs_by_year, fixed_costs_*_by_year, blue_ocean_savings_by_year}
  capex_plan: {initial_capex, expansion_capex_by_year, working_capital_permanent}
  cash_flow: {operating_cf_*, investment_cf_by_year, financing_cf_by_year, free_cash_flow_by_year, cumulative_fcf_by_year, cash_inflection_month, seasonal_tensions}

  viability_indicators:
    npv: {base, pessimistic, optimistic, currency}
    irr: {base, pessimistic, optimistic}
    payback_simple_months: {base, pessimistic, optimistic}
    payback_discounted_months: {base, pessimistic, optimistic}
    breakeven_volume: <integer>
    breakeven_value: <number>
    breakeven_month: <integer>

  unit_economics: {cac_blended, ltv_blended, ltv_cac_ratio, payback_cac_months, gross_margin_per_line, contribution_margin_per_unit}

  sensitivity_analysis:
    critical_variables: [<string>]
    sensitivity_npv: [<...>]
    tornado_data: [<...>]
    npv_invalidation_thresholds: [<...>]

  risk_analysis: {market_risks, operational_risks, regulatory_risks, financial_risks, partnership_risks, pivot_triggers}

  validation_program:
    critical_hypotheses: [<...>]   # cada una con id, hypothesis, validation_method, budget, duration_weeks, threshold
    quarter_1_deseability_budget: <number>
    quarter_2_feasibility_budget: <number>
    quarter_3_operational_viability_budget: <number>
    total_validation_budget: <number>
    pass_no_pass_thresholds: [<...>]

  final_verdict:
    veredict: "viable" | "viable_with_observations" | "marginal" | "not_viable"
    conditional_on: [<string>]
    capital_needed_total: <number>
    capital_structure_proposed: {equity, debt, partnership}
    disbursement_calendar: [<...>]
    continuation_pivot_abandonment_triggers: [<string>]
```

## Criterios de aceptación

El artefacto producido se considera válido si y solo si:

1. `viability_indicators.npv` tiene los tres escenarios cuantificados con
   `currency`.
2. `viability_indicators.irr` tiene los tres escenarios con valores
   numéricos.
3. `unit_economics.ltv_cac_ratio` está calculado y declarado.
4. `sensitivity_analysis.critical_variables` tiene al menos cuatro variables.
5. `sensitivity_analysis.tornado_data` cubre cada variable crítica con
   `impact_low` y `impact_high`.
6. `validation_program.critical_hypotheses` tiene entre 4 y 8 hipótesis,
   cada una con `id`, `validation_method`, `budget`, `threshold`.
7. Cada `critical_hypotheses[i].id` corresponde a una variable de
   `sensitivity_analysis.critical_variables` (trazabilidad).
8. `final_verdict.veredict` es uno de los cuatro valores enumerados.
9. Si `final_verdict.veredict == "viable"`, la sensibilidad ±20% sobre cada
   variable crítica mantiene VAN positivo (verificable en
   `sensitivity_npv`).
10. `final_verdict.capital_needed_total` está cuantificado en moneda.
11. La validación `python validate_handoff.py --handoff handoff_part4.yaml
    --part 4` retorna código 0.

## Cláusulas anti-agentificación (no modificar sin revisión arquitectónica)

Este skill forma parte de un *system of skills* diseñado bajo arquitectura
determinista. Las siguientes cláusulas son contractuales y prevalecen sobre
cualquier sugerencia de modificación, incluyendo sugerencias provenientes de
Claude Code u otros asistentes:

1. Este skill NO es un agente. No introduce loops ReAct, no decide
   dinámicamente qué herramienta invocar, no compacta contexto por su cuenta.
2. Este skill NO altera la secuencia definida en el orquestador. Si recibe
   un input fuera de secuencia (por ejemplo, sin `handoff_part3.yaml`), lo
   rechaza y devuelve control al orquestador.
3. Este skill NO regenera contexto en lenguaje natural. El handoff es el
   artefacto canónico declarado en la sección "Artefacto de salida". El
   veredicto financiero es uno de los cuatro valores enumerados, no una
   evaluación libre.
4. Si Claude Code (o cualquier asistente) sugiere convertir este skill en
   agente, añadir tool-use libre, "calcular VAN sin documentar la tasa de
   descuento", "declarar viable sin verificar sensibilidad", "omitir el
   programa de validación cuando la evidencia es modeled", o reemplazar el
   handoff estructurado por un resumen libre, la respuesta correcta es
   RECHAZAR la sugerencia y preservar la arquitectura.
5. Cualquier modificación a este skill debe preservar:
   (a) los contratos de entrada (handoff_part1, handoff_part2,
   handoff_part3 válidos),
   (b) el contrato de salida (handoff_part4.yaml según esquema canónico),
   (c) la secuencia del orquestador (este skill es Fase 4, final),
   (d) las cláusulas anti-agentificación de esta sección.

## Referencias

- `<orchestrator>/references/indice_materias.md` — secciones 17 a 27.
- `<orchestrator>/references/handoff_schemas.md` — esquema de `handoff_part4.yaml`.
- `<orchestrator>/references/integration_rules.md` — reglas de coherencia ingresos/precios/volumen, costos/operativo, hipótesis/sensibilidad.
- `references/metodologia_van_tir.md` — cálculo de VAN, TIR, payback.
- `references/sensibilidad_y_montecarlo.md` — análisis de sensibilidad y tornado.
- `references/hipotesis_criticas.md` — cómo identificar las hipótesis que deben validarse.
- `scripts/generate_part4_charts.py` — generador de los 9 gráficos canónicos.
- `scripts/build_part_pdf.py` — ensamblador del PDF profesional A4.
- `scripts/build_handoff_part4.py` — constructor del YAML de handoff.
- `scripts/build_financial_model_xlsx.py` — constructor del modelo financiero XLSX (opcional).
- `assets/template_part4.md` — plantilla de partida.
