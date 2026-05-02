# Reglas de Integración Cross-Partes

Este documento define las reglas que el orquestador y los skills aplican para garantizar coherencia entre las cuatro partes del análisis.

## Principio rector

Cada decisión tomada en una parte posterior debe poder rastrearse a un elemento de una parte anterior. La trazabilidad es el mecanismo que evita que el análisis se convierta en una sucesión de documentos paralelos sin relación causal.

## Flujo de trazabilidad por elemento

### Segmentación (Parte 2 ← Parte 1)
Los segmentos seleccionados en la Parte 2 deben corresponder a los `preliminary_segments` declarados en `handoff_part1.yaml`. La caracterización de cada segmento (circumstance, push dominante, anxiety dominante, capacidad de pago) hereda directamente del JTBD y del análisis de cuatro fuerzas de la Parte 1.

### Targeting (Parte 2)
El segmento de entrada elegido debe ser el de mayor producto atractividad × ajuste según la matriz de evaluación. El roadmap plurianual debe respetar las restricciones de capacidad operativa que se cuantifican en la Parte 3 (saltos de capacidad), por lo que existe un loop de ajuste posible: si la Parte 3 detecta que el roadmap declarado en la Parte 2 es operativamente inviable, se documenta como observación y se decide si se vuelve atrás.

### Posicionamiento (Parte 2 ← Parte 1)
La declaración de posicionamiento debe incorporar al menos: el segmento target, el problema o necesidad, el beneficio diferenciador y la razón para creer. Cada elemento se mapea a su origen en la Parte 1: el segmento al `preliminary_segments`, el problema al `job_statement`, el beneficio al `outcomes_prioritized` (tier hiper-decisivo), la razón para creer al benchmark competitivo de la Parte 1.

### Decisiones ERIC (Parte 2 ← Parte 1)
Cada acción Eliminate, Reduce, Raise o Create debe estar fundamentada en al menos uno de los siguientes elementos del `handoff_part1.yaml`: un `outcome` del análisis de Ulwick, un componente de las cuatro fuerzas, un pain o gain identificado, o un descriptor del benchmark competitivo. No se permiten acciones ERIC sin trazabilidad.

### Plan de producto (Parte 3 ← Parte 2)
El MVP de lanzamiento debe contener exclusivamente productos y servicios listados en el `value_proposition.products_services` del `handoff_part2.yaml` con categoría `essential`. Los productos `secondary` y `support` se postergan al backlog 24m según justificación operativa o financiera.

### Plan de precios (Parte 3 ← Parte 1, Parte 2)
El tarifario por línea debe estar dentro del rango de `willingness_to_pay_declared` de la Parte 1, ajustado por el factor de corrección declarado-revelado. El precio mid debe estar coherente con el `price_benchmark` de la Parte 1. Si el posicionamiento de la Parte 2 es premium-diferenciación, el precio mid puede situarse en el cuartil alto del benchmark; si es de bajo costo, en el cuartil bajo.

### Plan de canales (Parte 3 ← Parte 2)
El canal primario en cada fase del journey debe ser coherente con la decisión de cobertura del targeting. Marketing concentrado implica canales focalizados (red prescriptora, B2B), no canales masivos. La estrategia genérica condiciona el mix de inversión por canal.

### Plan de comunicación (Parte 3 ← Parte 2)
La promesa central debe coincidir con el tagline operativo del `handoff_part2.yaml`. Los mensajes secundarios deben mapear a los `pain_relievers` y `gain_creators` críticos de la Parte 2. El embudo de conversión y sus tasas deben ser coherentes con la decisión de canales primarios y secundarios.

### Capacidades operativas (Parte 3)
Los cuellos de botella secuenciales deben identificarse explícitamente. La capacidad máxima en fase 1 acota el SOM realizable del año 1, lo que produce un loop de validación con la Parte 1: si la capacidad operativa en fase 1 es inferior al SOM proyectado en la Parte 1, prevalece la capacidad y se ajusta el SOM efectivo del modelo financiero.

### Proyección de ingresos (Parte 4 ← Parte 3)
La curva de ingresos por línea en escenario base debe construirse multiplicando el volumen proyectado (limitado por la capacidad de la Parte 3) por el precio mid de la Parte 3. El escenario pesimista aplica factor 0.6 sobre volumen; el optimista aplica factor 1.3. Estos factores son convención del sistema, ajustables si el caso lo justifica.

### Estructura de costos (Parte 4 ← Parte 3)
Los costos variables unitarios deben replicar exactamente la `unit_cost_structure` del `handoff_part3.yaml`. Los costos fijos operativos provienen de la `capacity_plan`. Los costos fijos comerciales y de marketing provienen del `channels_plan.cac_blended` × volumen, más el presupuesto fijo del `communication_plan`.

### CAPEX (Parte 4 ← Parte 3)
El CAPEX inicial agrega: taller (de la Parte 3), stock comprometido (de la Parte 3), regulatorio (si aplica, de la Parte 3 o Parte 1), comercial (de la Parte 3 launch_campaign + materiales). El CAPEX de expansión replica los `capacity_jumps` de la Parte 3.

### Métricas de unidad económica (Parte 4 ← Parte 3)
El CAC blended es el del `handoff_part3.yaml`. El LTV se calcula sobre el ticket medio (Big Hire amortizado) más recurrencia (Little Hire) por la tasa de retención modelada. El ratio LTV/CAC debe estar por encima de 3 para considerarse sano; por encima de 5 es holgado; por debajo de 3 es señal de alerta y debe documentarse explícitamente.

### Análisis de sensibilidad (Parte 4)
Las variables críticas son las que cumplen el criterio: una variación de ±20% altera materialmente el VAN (umbral típico: cambio de signo o caída superior al 30% del VAN base). Las hipótesis críticas declaradas en el programa de validación deben corresponder a las variables críticas del análisis de sensibilidad.

## Validación de coherencia inter-bloque

El orquestador, antes de generar el dossier final, ejecuta un test de coherencia inter-bloque inspirado en el test que el BMC original hace internamente. Verifica los siguientes ítems:

1. ¿Cada segmento declarado en Parte 2 tiene un canal primario en Parte 3?
2. ¿Cada producto/servicio del Value Map (Parte 2) tiene una key activity asociada en el plan operativo (Parte 3)?
3. ¿Cada línea de ingreso modelada en Parte 4 tiene un canal de captura definido en Parte 3?
4. ¿Cada hipótesis crítica del programa de validación (Parte 4) corresponde a una variable de input que viene de Parte 3 o Parte 1?
5. ¿El veredicto final (Parte 4) es coherente con la oportunidad declarada en la síntesis del diagnóstico (Parte 1)?

Si alguno de estos tests falla, el orquestador genera una sección de "Observaciones de coherencia" en el dossier consolidado, identificando explícitamente la inconsistencia y dejando la resolución al usuario.

## Reglas de comunicación de evidencia

Cada cifra, rango o supuesto del análisis debe declarar su nivel de evidencia. La taxonomía es:

- **primary**: validado con datos primarios (entrevistas, pilotos, transacciones reales)
- **secondary**: respaldado por fuentes públicas o sectoriales (INE, gremios, papers, benchmarks)
- **modeled**: construido por extrapolación o analogía con casos comparables
- **inherited**: heredado de un artefacto previo (JTBD, VPC, Blue Ocean, BMC) sin re-validación

Esta declaración aparece en cada handoff (campo `evidence_level`) y en cada output Markdown (en notas al pie o en tablas explícitas). El veredicto final debe condicionar su fuerza al nivel de evidencia: un veredicto "viable" basado mayoritariamente en evidencia `modeled` debe leerse como "modelo viable bajo supuestos a validar", no como "decisión de inversión cerrada".
