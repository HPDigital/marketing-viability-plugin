# Hipótesis críticas y programa de validación

## Identificación de hipótesis críticas

Una hipótesis es crítica si su validación o invalidación cambia la decisión de inversión. La regla operativa es: si esta hipótesis es falsa, el VAN base se hace negativo o el payback se extiende más allá del horizonte aceptable.

Las hipótesis críticas típicas en un modelo de viabilidad caen en cuatro grupos:

1. **Deseabilidad**: ¿el cliente quiere realmente lo que ofrecemos al precio que cobramos?
2. **Factibilidad**: ¿podemos construir y entregar lo que prometimos al costo modelado?
3. **Viabilidad operativa**: ¿podemos sostener la operación a la escala proyectada?
4. **Viabilidad financiera estructural**: ¿el modelo financiero es robusto bajo variación razonable?

## Plantilla de hipótesis

```yaml
- id: "H-1"
  hypothesis: "El segmento P1 ratifica disposición a pagar de USD 6.000-12.000 por Big Hire"
  category: "deseabilidad"
  origin_in_handoff: "handoff_part1.willingness_to_pay_declared[P1]"
  validation_method: "Entrevistas in-depth con N=15-20 pacientes elegibles + simulación de cotización con cierre"
  budget: 18000
  duration_weeks: 8
  pass_threshold: ">=70% de los pacientes ratifican estar dispuestos a pagar precio mid"
  fail_action: "Pivote a precio en cuartil bajo del benchmark + aumento de financiamiento, o salida"
```

## Estructura del programa de validación por trimestre

**Trimestre 1 — Deseabilidad**
- H-1, H-2, H-3 sobre disposición a pagar, deseo del servicio integrado, densidad prescriptora.
- Métodos: entrevistas, encuestas pasivas, simulación de cotización.
- Presupuesto típico: 30-50% del presupuesto total de validación.
- Decisión al cierre del trimestre: continuar / pivote / abandonar.

**Trimestre 2 — Factibilidad**
- H-4, H-5 sobre partnership con proveedor, factibilidad técnica del SLA, capacidad real del técnico ortoprotesista o equivalente.
- Métodos: cartas de intención, prototipos operativos, mediciones piloto.
- Presupuesto típico: 30-40% del presupuesto total.

**Trimestre 3 — Viabilidad operativa**
- H-6, H-7, H-8 sobre conversión real del embudo, márgenes operativos en operación piloto, retención del cliente recurrente.
- Métodos: piloto operativo controlado en una geografía, métricas reales de embudo.
- Presupuesto típico: 20-30% del presupuesto total.

## Umbrales de paso/no-paso

Cada hipótesis debe tener un umbral cuantitativo de paso:

| Hipótesis | Umbral de paso | Umbral de salida |
|---|---|---|
| H-1 Disposición a pagar | ≥70% ratifica precio mid | <40% ratifica precio mid |
| H-2 SLA factible | <72h respuesta en 90% casos | >120h o <70% cumplimiento |
| H-3 Densidad prescriptora | ≥3 prescriptores activos/ciudad | <1 prescriptor activo |
| H-4 Partnership europeo | LOI firmado en Q2 | Sin contraparte identificada al cierre Q2 |
| H-5 Conversión B2B | ≥2 contratos pilotos firmados | 0 contratos en Q3 |

Entre umbral de paso y umbral de salida hay una zona gris que requiere juicio. Documentarla.

## Pivote vs salida

**Pivote**: cuando la hipótesis falla pero el aprendizaje sugiere una variante viable. Ejemplos:
- H-1 fallida (precio premium rechazado) → pivote a precio reducido + foco en P2 diabético.
- H-3 fallida (red prescriptora insuficiente) → pivote a canal B2B clínicas como primario.

**Salida**: cuando múltiples hipótesis críticas fallan simultáneamente o cuando el pivote requeriría reformular el modelo de negocio.

## Reglas anti-error

1. **No diseñar el programa de validación después del veredicto**: el programa nace al identificar las hipótesis críticas.
2. **No omitir el presupuesto de validación**: típicamente USD 50.000-100.000 según complejidad. Sin presupuesto explícito, la validación no se ejecuta.
3. **No declarar veredicto "viable" basado en hipótesis modeladas no validadas sin programa de validación adjunto**.
4. **Cada hipótesis debe poder rastrearse a una variable crítica del análisis de sensibilidad**.
