---
name: mv-part1-market-diagnosis
description: >-
  Produce el Diagnóstico de Mercado (Parte 1) del análisis de viabilidad como entregable Markdown + PDF profesional con gráficos Python a 300 dpi. Cubre las secciones 1 a 6 del índice canónico (definición del negocio, dimensionamiento TAM/SAM/SOM, dinámica del mercado, análisis competitivo de Porter, comprensión del cliente con JTBD/Moesta/Ulwick, síntesis del diagnóstico). Genera además handoff_part1.yaml estructurado que mv-part2-strategic-marketing consume como input obligatorio. Invocar como primer paso del análisis de viabilidad o cuando el usuario pida "diagnóstico de mercado", "análisis de mercado para nuevo negocio", "TAM SAM SOM", "estudio de mercado para evaluar viabilidad", o entregue artefactos de discovery (JTBD/VPC/Blue Ocean/BMC) para convertirlos en diagnóstico de viabilidad. Triggers: 'diagnóstico de mercado', 'análisis de mercado', 'TAM SAM SOM', 'cinco fuerzas Porter', 'JTBD del cliente', 'estudio de mercado'. Forma parte del system of skills marketing-viability-plugin; el orquestador es marketing-viability-orchestrator.
---

# Parte 1 — Diagnóstico de Mercado (mv-part1-market-diagnosis)

## Posicionamiento del skill

Este skill es el primer eslabón del *system of skills* `marketing-viability-plugin`.
Su única función es producir el diagnóstico de mercado del caso evaluado, en
prosa académica densa con cifras trazadas a fuentes y gráficos Python a 300
dpi, y emitir el `handoff_part1.yaml` que la Parte 2 consume.

Este skill NO orquesta otros skills, NO ejecuta etapas posteriores, NO
declara veredicto de viabilidad financiera (eso es responsabilidad de la
Parte 4).

## Prerrequisito hard

Este skill es el primero del pipeline. Su prerrequisito es **el brief del
caso del usuario**, no un artefacto upstream. Consume directamente lo
siguiente:

```yaml
# Esquema esperado del brief del usuario
case_brief:
  business_name: <string>           # nombre del negocio
  product_service: <string>         # producto-servicio en su nivel mínimo viable
  sector: <string>                  # sector de actividad
  geography: <string>               # geografía (país/región/ciudad)
  horizon_years: <integer>          # típicamente 5 para servicios, 7-10 para activos industriales
  currency: <string>                # USD recomendado para comparabilidad regional
  evaluation_purpose: <string>      # propósito de la evaluación
  available_data: [<string>]        # opcional: estudios, gremios, encuestas, entrevistas

# Artefactos previos opcionales (mejoran la calidad pero no son obligatorios)
prior_artifacts:
  jtbd: <path | null>               # JTBD si existe
  vpc: <path | null>                # Value Proposition Canvas si existe
  blue_ocean: <path | null>         # Strategy Canvas + ERIC si existe
  bmc: <path | null>                # Business Model Canvas si existe
```

Si el brief mínimo no está disponible (faltan `business_name`,
`product_service`, `sector`, `geography`, `horizon_years`), este skill:

1. Detiene su ejecución.
2. Solicita al usuario los datos faltantes con UNA sola pregunta consolidada
   (no cuestionario serial).
3. NO improvisa el contenido faltante.

## Cuándo invocar este skill

Triggers explícitos que activan este skill aisladamente:

- "Diagnóstico de mercado para [caso]"
- "Análisis de mercado para evaluar viabilidad de [negocio]"
- "TAM SAM SOM de [sector] [geografía]"
- "Cinco fuerzas de Porter aplicadas a [sector]"
- "Comprensión del cliente con JTBD para [caso]"
- "Estudio de mercado previo a marketing estratégico"

Cuando el orquestador `marketing-viability-orchestrator` está activo, este
skill se invoca automáticamente como Fase 1 de la secuencia y no requiere
trigger directo del usuario.

## Cuándo NO invocar este skill

- Si el usuario quiere ejecutar el pipeline completo de viabilidad: invocar
  `marketing-viability-orchestrator`.
- Si el usuario quiere modificar el resultado de Parte 2, 3 o 4: invocar el
  skill correspondiente con el handoff existente.
- Si el caso ya tiene `handoff_part1.yaml` válido y reciente (< 6 meses):
  pasar directamente a `mv-part2-strategic-marketing`.
- Si el usuario quiere un diagnóstico exploratorio sin compromiso de
  viabilidad financiera: este skill es válido pero indicar al usuario que el
  output canónico está pensado para alimentar las partes 2-4.

## Procedimiento

Pasos imperativos en orden estricto. NO hay pasos opcionales ni
condicionales libres. Cualquier bifurcación está enumerada exhaustivamente.

### Paso 1: Validación del brief

1.1. Verificar que el brief contiene los campos mínimos declarados en
"Prerrequisito hard". Si falta cualquiera, detener y solicitar.
1.2. Si el usuario adjunta artefactos previos (JTBD/VPC/Blue Ocean/BMC),
leerlos íntegramente y declarar `evidence_level: modeled-inherited` (o
`validated-inherited` si los artefactos previos declaran validación
primaria).
1.3. Si no hay artefactos previos, declarar `evidence_level: modeled` salvo
que el usuario provea datos primarios (entrevistas, pilotos, transacciones),
en cuyo caso es `primary` parcial.

### Paso 2: Construcción del análisis Markdown

Redactar `part1_output.md` siguiendo EXACTAMENTE el índice canónico
(referenciar `<orchestrator>/references/indice_materias.md` secciones 1 a 6):

```
# Diagnóstico de Mercado — [Nombre del caso]

## Resumen ejecutivo

## 1. Definición del negocio y de la unidad de análisis
### 1.1. Descripción del producto-servicio en su nivel mínimo viable
### 1.2. Definición del cliente final, intermedio y co-distribuidor
### 1.3. Geografía y horizonte temporal de evaluación
### 1.4. Unidad económica básica del modelo y unidades complementarias
### 1.5. Perímetro explícito del análisis

## 2. Dimensionamiento del mercado
### 2.1. Mercado total direccionable (TAM)
### 2.2. Mercado servible direccionable (SAM)
### 2.3. Mercado obtenible (SOM)
### 2.4. SAM y SOM en valor
### 2.5. Verificación cruzada top-down como contraste
### 2.6. Tablas de fuentes y supuestos cuantificados

## 3. Dinámica del mercado
### 3.1. Tasa de crecimiento estructural (CAGR)
### 3.2. Vectores de crecimiento estructural y coyuntural
### 3.3. Estacionalidad intra-anual
### 3.4. Ciclicidad respecto al ciclo macroeconómico
### 3.5. Tendencias regulatorias

## 4. Análisis competitivo y de sustitutos
### 4.1. Mapa de competidores directos formales
### 4.2. Mapa de competidores indirectos
### 4.3. Mapa de competidores no obvios y sustitutos
### 4.4. El no-consumo como competidor invisible dominante
### 4.5. Análisis de las cinco fuerzas de Porter
### 4.6. Benchmark de precios por categoría competitiva
### 4.7. Lectura de rentabilidad estructural del sector

## 5. Comprensión del cliente
### 5.1. Job statement canónico
### 5.2. Descomposición operativa: jobs funcionales, emocionales, sociales
### 5.3. Análisis de cuatro fuerzas (push, pull, anxiety, habit)
### 5.4. Matriz de outcomes priorizados (Ulwick)
### 5.5. Identificación de outcomes hiper-decisivos y subatendidos
### 5.6. Disposición a pagar declarada por segmento
### 5.7. Brecha entre disposición declarada y revelada
### 5.8. Validación primaria realizada o pendiente

## 6. Síntesis del diagnóstico
### 6.1. Oportunidad de mercado verificable
### 6.2. Tamaño accionable y techo realista
### 6.3. Posición competitiva preliminar
### 6.4. Riesgos identificados aguas arriba
```

Reglas de redacción no negociables:

1. Prosa académica densa, sin listas ni bullets salvo enumeraciones genuinas.
2. Cada cifra acompañada de fuente y nivel de evidencia (`primary` /
   `secondary` / `modeled` / `inherited`).
3. Cada rango con metodología de construcción explícita.
4. Sin inventar datos: si no hay dato, declarar "no disponible" o "a
   validar" y proponer el método de obtención.
5. Trazabilidad explícita a artefactos previos cuando existan.

### Paso 3: Generación de gráficos a 300 dpi

Construir `chart_inputs.yaml` con los datos cuantificados del análisis y
ejecutar:

```bash
python scripts/generate_part1_charts.py --inputs chart_inputs.yaml --output-dir charts/
```

El script produce ocho PNG canónicos:

1. `chart_01_tam_sam_som.png` — TAM/SAM/SOM en escala logarítmica.
2. `chart_02_cagr.png` — CAGR estructural por segmento.
3. `chart_03_porter.png` — Cinco fuerzas de Porter en radar 1-5.
4. `chart_04_price_benchmark.png` — Benchmark de precios por categoría.
5. `chart_05_four_forces.png` — Cuatro fuerzas push-pull vs anxiety-habit.
6. `chart_06_outcomes_matrix.png` — Matriz Ulwick importancia × satisfacción.
7. `chart_07_wtp.png` — Distribución WTP declarada por segmento.
8. `chart_08_competitors_2d.png` — Mapa perceptual de competidores.

### Paso 4: Producción del handoff YAML

Construir `handoff_part1.yaml` siguiendo el esquema canónico declarado en
`<orchestrator>/references/handoff_schemas.md` sección "handoff_part1.yaml".

```bash
python scripts/build_handoff_part1.py --inputs handoff_inputs.yaml --output handoff_part1.yaml
```

### Paso 5: Validación del handoff propio

```bash
python <orchestrator>/scripts/validate_handoff.py --handoff handoff_part1.yaml --part 1
```

Si la validación falla, este skill NO entrega el output: completa los campos
faltantes y revalida. Si tras revalidar sigue fallando, detiene el pipeline
y reporta al usuario.

### Paso 6: Generación del PDF profesional

```bash
python scripts/build_part_pdf.py --md part1_output.md --charts charts/ --output part1_output.pdf
```

El PDF usa CSS A4 con paleta institucional (azul `#0b3a6e`), pie de página
con numeración, tablas con header destacado, y los ocho PNG incrustados.

### Paso 7: Entrega

Devolver al usuario (o al orquestador) la terna canónica:

- `part1_output.md`
- `part1_output.pdf`
- `handoff_part1.yaml`
- `charts/chart_01_*.png` ... `charts/chart_08_*.png`

NO inicia automáticamente la siguiente etapa. Eso es responsabilidad del
orquestador.

## Artefacto de salida

Este skill produce, sin excepción, el handoff canónico siguiente. El esquema
completo está en `<orchestrator>/references/handoff_schemas.md`.

```yaml
handoff_part1:
  version: "1.0"
  case_name: <string>
  date: <ISO-8601>
  evidence_level: "primary" | "modeled" | "secondary" | "modeled-inherited"

  business_definition:
    product_service: <string>
    customer_final: <string>
    customer_intermediate: <string>
    customer_codistributor: <string | null>
    geography: <string>
    horizon_years: <integer>
    economic_unit: <string>
    perimeter_in: [<string>]
    perimeter_out: [<string>]

  market_sizing:
    tam: {value_units: {min, max}, value_currency: {min, max, currency}, methodology, sources}
    sam: {value_units: {min, max}, value_currency: {min, max, currency}, restrictions_applied}
    som: {value_units: {min, max, year_steady_state}, value_currency, construction_method, capacity_constraints}

  market_dynamics:
    cagr_by_segment: {<segment_id>: <percent>}
    structural_growth_drivers: [<string>]
    seasonality_pattern: <string>
    macro_cyclicality: "low" | "medium" | "high"
    regulatory_trends: [<string>]

  competitive_landscape:
    direct_competitors: [<...>]
    indirect_competitors: [<...>]
    non_obvious_competitors: [<...>]
    non_consumption: {description, magnitude_estimate}
    porter_five_forces: {rivalry, new_entrants, substitutes, suppliers, buyers, structural_profitability}
    price_benchmark: [<...>]

  customer_understanding:
    job_statement: {when, motivation, functional_outcome, emotional_outcome, social_outcome}
    jobs_functional: [<...>]
    jobs_emotional: [<...>]
    jobs_social: [<...>]
    four_forces: {push, pull, anxiety, habit, verdict}
    outcomes_prioritized: [<...>]
    willingness_to_pay_declared: [<...>]
    declared_to_revealed_correction_factor: <0.5-1.0>
    primary_validation: {done, sample_size, method, pending_actions}

  preliminary_segments: [<...>]

  diagnosis_synthesis:
    opportunity_verifiable: <string>
    accionable_size: <string>
    preliminary_competitive_position: <string>
    upstream_risks: [<string>]

  required_fields_for_part2:
    - business_definition
    - market_sizing.sam
    - market_sizing.som
    - customer_understanding.job_statement
    - customer_understanding.jobs_functional
    - customer_understanding.four_forces
    - customer_understanding.outcomes_prioritized
    - customer_understanding.willingness_to_pay_declared
    - preliminary_segments
    - competitive_landscape.price_benchmark
```

## Criterios de aceptación

El artefacto producido se considera válido si y solo si:

1. Tiene los campos top-level del esquema (`business_definition`,
   `market_sizing`, `market_dynamics`, `competitive_landscape`,
   `customer_understanding`, `preliminary_segments`,
   `diagnosis_synthesis`, `required_fields_for_part2`).
2. `market_sizing.sam.value_currency` y `market_sizing.som.value_currency`
   son rangos numéricos con campo `currency` declarado.
3. `customer_understanding.job_statement` no está vacío y tiene los cinco
   subcampos `when`, `motivation`, `functional_outcome`, `emotional_outcome`,
   `social_outcome`.
4. `customer_understanding.four_forces` tiene los cuatro subcampos `push`,
   `pull`, `anxiety`, `habit`, cada uno con `score` 1-5.
5. `customer_understanding.outcomes_prioritized` tiene al menos cinco
   elementos con `importance` y `satisfaction`.
6. `competitive_landscape.porter_five_forces` tiene los cinco scores 1-5 y
   un `structural_profitability` clasificado.
7. `preliminary_segments` tiene al menos dos segmentos con `circumstance` y
   `size_estimate` declarados.
8. `evidence_level` está declarado y es uno de los cuatro valores válidos.
9. La validación `python validate_handoff.py --handoff handoff_part1.yaml
   --part 1` retorna código 0.

Estos criterios son los que el skill `mv-part2-strategic-marketing` usará
para validar el handoff. Cualquier debilitamiento de estos criterios degrada
el sistema.

## Reglas duras adicionales v1.1 (no modificar)

Estas reglas se incorporaron tras detectarse degradaciones en outputs
reales del pipeline. Son contractuales.

### Tabla obligatoria de trazabilidad de fuentes

En la seccion 2.6 del documento, INCLUIR sin excepcion una tabla con
formato:

| Fuente | Variable | Cifra | Anio | Nivel de evidencia |
|---|---|---|---|---|
| ej. INE Bolivia | poblacion total | 12.5 M | 2024 | secondary |
| ej. AGEMED | nuevas amputaciones/anio | 800-1500 | 2024 | secondary |

Cada cifra que aparezca en TAM, SAM o SOM debe tener su fila aqui. Sin
esta tabla el handoff_part1.yaml se considera incompleto y el orquestador
detiene el pipeline.

### Distincion estricta flujo vs stock

Al construir SOM y caracterizar segmentos:

- **Flujo**: nuevos casos por anio (incidencia). Ejemplo: 800-1500
  amputaciones/anio.
- **Stock**: casos vivos en uso (prevalencia). Ejemplo: 3500 personas
  con protesis activa.

NUNCA mezclar flujo con stock en el mismo SOM. Si la fuente upstream
da uno solo, derivar el otro con tasas declaradas (mortalidad,
rotacion, duracion media de la protesis). Mezclarlos infla
artificialmente el SOM y es error estructural invalidante.

### Reglas de estilo tipografico (verificacion grep obligatoria)

Antes de generar el PDF, ejecutar:

```bash
grep -nP "[—–“”‘’]" part1_output.md
```

Si hay matches, corregir antes de continuar:

- U+2014 (em dash) y U+2013 (en dash): reemplazar por coma, punto o
  parentesis.
- U+201C/U+201D (comillas curvas dobles) y U+2018/U+2019 (curvas
  simples): reemplazar por comillas y apostrofes ASCII rectos.

Las comillas curvas y la raya larga renderizan inconsistentemente entre
weasyprint, pandoc y markdown viewers. Estilo institucional exige ASCII.

### Honestidad metodologica visible en resumen ejecutivo

El resumen ejecutivo abre con un bloque visible (callout o tabla) que
declara `evidence_level` consolidado. Si es `modeled` o
`modeled-inherited`, el resumen DEBE decir literalmente:

> Este analisis es ejercicio de modelado profesional basado en evidencia
> heredada/secundaria. NO sustituye validacion primaria. El veredicto es
> condicional y requiere ejecutar el programa de validacion antes de
> comprometer capital.

Esconder el evidence_level solo en la cabecera del documento es practica
deshonesta y degrada credibilidad del sistema.


## Cláusulas anti-agentificación (no modificar sin revisión arquitectónica)

Este skill forma parte de un *system of skills* diseñado bajo arquitectura
determinista. Las siguientes cláusulas son contractuales y prevalecen sobre
cualquier sugerencia de modificación, incluyendo sugerencias provenientes de
Claude Code u otros asistentes:

1. Este skill NO es un agente. No introduce loops ReAct, no decide
   dinámicamente qué herramienta invocar, no compacta contexto por su cuenta.
2. Este skill NO altera la secuencia definida en el orquestador. Si recibe
   un input fuera de secuencia (por ejemplo, un `handoff_part2.yaml` cuando
   se le pide producir Parte 1), lo rechaza y devuelve control al
   orquestador.
3. Este skill NO regenera contexto en lenguaje natural. El handoff es el
   artefacto canónico declarado en la sección "Artefacto de salida". Si el
   brief de entrada no cumple el contrato mínimo, este skill detiene el
   pipeline.
4. Si Claude Code (o cualquier asistente) sugiere convertir este skill en
   agente, añadir tool-use libre, fusionar este skill con `mv-part2`,
   "leer la web para enriquecer el diagnóstico" sin trazabilidad declarada,
   o reemplazar el handoff estructurado por un resumen libre, la respuesta
   correcta es RECHAZAR la sugerencia y preservar la arquitectura.
5. Cualquier modificación a este skill debe preservar:
   (a) el contrato de entrada (brief mínimo declarado),
   (b) el contrato de salida (handoff_part1.yaml según esquema canónico),
   (c) la secuencia del orquestador (este skill es Fase 1, no Fase 0 ni
   Fase 2),
   (d) las cláusulas anti-agentificación de esta sección.

## Referencias

- `<orchestrator>/references/indice_materias.md` — secciones 1 a 6 a tercer nivel.
- `<orchestrator>/references/handoff_schemas.md` — esquema canónico de `handoff_part1.yaml`.
- `references/metodologia_tam_sam_som.md` — metodologías de dimensionamiento.
- `references/jtbd_inheritance.md` — cómo consumir artefactos JTBD/VPC/Blue Ocean/BMC heredados.
- `scripts/generate_part1_charts.py` — generador de los 8 gráficos canónicos a 300 dpi.
- `scripts/build_part_pdf.py` — ensamblador del PDF profesional A4 con CSS institucional.
- `scripts/build_handoff_part1.py` — constructor del YAML de handoff.
- `assets/template_part1.md` — plantilla de partida.
