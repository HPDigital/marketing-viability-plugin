# Cómo consumir artefactos JTBD/VPC/Blue Ocean/BMC heredados

Cuando el usuario adjunta artefactos de discovery previos, este skill los consume sin re-elaborarlos. La función es traducir su contenido al lenguaje del diagnóstico de mercado y dejar trazabilidad explícita.

## Si hay JTBD

El JTBD aporta directamente a:

| Sección de Parte 1 | Contenido del JTBD |
|---|---|
| 5.1. Job statement canónico | `job_statement` (when, motivation, functional_outcome, emotional_outcome, social_outcome) |
| 5.2. Jobs funcionales/emocionales/sociales | `customer_jobs` desagregados |
| 5.3. Cuatro fuerzas (Moesta) | `four_forces` con sus scores y components |
| 5.4. Outcomes priorizados (Ulwick) | `outcomes_prioritized` con importancia, satisfacción, opportunity score |
| 5.5. Outcomes hiper-decisivos | filtro de outcomes con OS ≥ 12 (hiper) y 8-12 (subatendidos críticos) |
| 4.1-4.4. Mapa de competidores | `competitors` por categoría (direct, indirect, non_obvious, non_consumption) |
| 6.1. Oportunidad verificable | `recommendations.do` filtrada |
| 6.4. Riesgos aguas arriba | `limitations.evidence_gaps` y `recommendations.validate_first` |

**Regla de cita**: en cada sección que consume JTBD, declarar al pie: "Hereda de jtbd_artifact v[X], evidence_level: [nivel]".

## Si hay VPC

El VPC aporta directamente a:

| Sección de Parte 1 | Contenido del VPC |
|---|---|
| 5.6. Disposición a pagar declarada | implícita en el pricing del Big Hire en `value_proposition_statement` |
| 5.5. Outcomes hiper-decisivos | refuerzo del JTBD vía `pain_relievers` y `gain_creators` críticos |
| 4. Análisis competitivo | `fit_analysis.competitive_position` |

## Si hay Blue Ocean

El Blue Ocean aporta directamente a:

| Sección de Parte 1 | Contenido del Blue Ocean |
|---|---|
| 4.5. Cinco fuerzas de Porter | curva de valor as-is permite inferir patrón competitivo del sector |
| 4.6. Benchmark de precios | matriz factor × actor (proposal_to_be vs proposal_as_is vs competitor_direct) |
| 4.7. Rentabilidad estructural | tier de no-clientes y `non_consumption` magnitudes |

## Si hay BMC

El BMC aporta directamente a:

| Sección de Parte 1 | Contenido del BMC |
|---|---|
| 1.1. Producto-servicio MVP | `value_propositions` |
| 1.2. Cliente final, intermedio, co-distribuidor | `customer_segments` con roles diferenciados |
| 2.3. SOM bottom-up | volúmenes implícitos en `customer_segments.volumen_estimado` |
| 5.6. Disposición a pagar | `revenue_streams.disposicion` y `pricing` |

## Reglas de evidence_level

- Si los artefactos previos declaran `evidence_level: primary` y se aplican sin modificación: el handoff_part1 declara `evidence_level: validated-inherited`.
- Si los artefactos declaran `evidence_level: modeled` y se aplican sin re-validación: declara `evidence_level: modeled-inherited`.
- Si el skill complementa con datos primarios adicionales: declara `evidence_level: hybrid`.

## Reglas de no-redundancia

No re-elaborar lo que el artefacto ya hizo bien. Si el JTBD ya contiene el análisis de cuatro fuerzas con sus scores justificados, la Parte 1 lo cita y lo aplica, no lo reinventa. La función del diagnóstico es integrar y dimensionar, no duplicar el discovery.
