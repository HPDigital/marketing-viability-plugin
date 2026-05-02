# Metodología de decisiones ERIC

Las cuatro acciones del Blue Ocean Strategy se aplican sobre los factores de competencia del sector. Cada acción debe rastrearse a evidencia del `handoff_part1.yaml`.

## Definiciones

**Eliminate**: factor que el sector compite intensamente y que el cliente no valora o valora negativamente. Eliminarlo libera recursos sin perjuicio de la propuesta.

**Reduce**: factor que el sector sobre-ofrece más allá de lo que el cliente valora. Reducirlo a un nivel suficiente libera recursos.

**Raise**: factor que el cliente valora pero el sector sub-ofrece. Elevarlo por encima del estándar diferencia.

**Create**: factor nuevo que el sector no ofrece y que resuelve un outcome subatendido o una anxiety dominante.

## Trazabilidad obligatoria

Cada decisión ERIC debe documentar al menos una de las siguientes evidencias:

| Tipo de evidencia | Origen en handoff_part1 |
|---|---|
| Outcome subatendido (OS ≥ 10) | `customer_understanding.outcomes_prioritized` |
| Outcome hiper-decisivo (OS ≥ 12) | `customer_understanding.outcomes_prioritized` |
| Componente de fuerza (push, pull, anxiety, habit) | `customer_understanding.four_forces` |
| Pain o gain identificado | VPC heredado o JTBD pains |
| Brecha del benchmark competitivo | `competitive_landscape.price_benchmark` |

Sin trazabilidad, la decisión no se incorpora.

## Plantilla de documentación de cada decisión

```yaml
- action: "create"
  factor_id: "F4"
  factor_statement: "SLA escrito de respuesta técnica"
  to_be_score: 5
  trazabilidad:
    outcome_origin: "O01 - Encontrar técnico que entienda el equipo (OS=13)"
    force_origin: "anxiety - Quedarse sin soporte técnico"
    benchmark_gap: "Ningún competidor ofrece SLA escrito"
  cost_impact: "OPEX +5%/mes por técnico dedicado y stock crítico"
  revenue_impact: "Reduce anxiety dominante, mejora conversión 15-25%"
```

## Reglas anti-error

1. **No declarar una acción ERIC sin trazabilidad**.
2. **No proponer "Create" sobre factores que ya existen en algún competidor**: si existen, son "Raise" o "estado del arte", no "Create".
3. **Cuantificar el impacto en OPEX y revenue de cada decisión**: el Eliminate/Reduce sin estimación de ahorro no aporta al modelo financiero.
4. **Validar el conjunto contra el Strategy Canvas**: la curva to-be debe ser coherente con la suma de las decisiones ERIC.
5. **Verificar que cada Raise/Create sea defendible operativamente**: si la operación de la Parte 3 no puede sostener el factor elevado, debe degradarse o eliminarse de la curva to-be.
