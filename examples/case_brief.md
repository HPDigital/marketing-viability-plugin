# Case Brief — Ejemplo mínimo

Este archivo sirve como input mínimo del pipeline. El orquestador lo lee al
inicio de la Fase 0 y, si es completo, procede a invocar
`mv-part1-market-diagnosis`.

```yaml
case_brief:
  business_name: "Ortopedia Andes"
  product_service: >-
    Servicio integrado de prótesis transtibial: ajuste técnico personalizado,
    componentes europeos certificados, seguimiento clínico durante 24 meses
    y financiamiento accesible.
  sector: "salud / dispositivos médicos / rehabilitación"
  geography: "Bolivia (eje central La Paz - Cochabamba - Santa Cruz)"
  horizon_years: 5
  currency: "USD"
  evaluation_purpose: >-
    Evaluar si el modelo es financieramente viable antes de comprometer
    capital semilla. Identificar las cuatro a ocho hipótesis críticas que
    deben validarse en los primeros 9 meses (deseabilidad, factibilidad,
    viabilidad operativa) antes de ramp-up comercial.
  available_data:
    - "Datos AGEMED 2023-2025 sobre incidencia y registros de discapacidad"
    - "Encuestas a 18 prescriptores ortopedistas en La Paz (sample piloto)"
    - "Benchmark de precios de tres importadores y dos viajes médicos a Lima"
    - "Estimación de población diabética con riesgo de amputación 2026"

prior_artifacts:
  jtbd: null              # opcional
  vpc: null               # opcional
  blue_ocean: null        # opcional
  bmc: null               # opcional
```

Si el usuario tiene artefactos previos de discovery (JTBD, VPC, Blue Ocean,
BMC), se referencian en `prior_artifacts` con la ruta del archivo. La
Parte 1 los consume y declara `evidence_level: modeled-inherited`.
