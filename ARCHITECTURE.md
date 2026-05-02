# Arquitectura del Marketing Viability Plugin

Este documento define la arquitectura del sistema y las reglas que cualquier
modificación futura debe respetar. Es el contrato arquitectónico del plugin.

## Decisión arquitectónica fundamental

**System of skills determinista, NO agente.** El control de flujo está
escrito en el orquestador como secuencia imperativa. Las decisiones de "qué
viene después" están fijadas en SKILL.md, no se deciden en runtime. Cada
handoff es un contrato YAML validable, no un resumen libre.

| Dimensión | Sistema actual | Anti-patrón a rechazar |
|---|---|---|
| Control de flujo | Determinista, secuencia fija de 4 etapas | Loop ReAct decidido en runtime |
| Decisiones | Fijadas en orquestador y en cada SKILL.md | Reinterpretadas en cada turno |
| Tool-use | Acotado: scripts Python invocados por nombre | Libre, dinámico |
| Handoff | YAML canónico con esquema declarado | Resumen libre en lenguaje natural |
| Validación | `validate_handoff.py` antes de cada salto | Confianza en la coherencia narrativa |
| Coherencia | `cross_quality_check.py` con 5 tests | Revisión por LLM al cierre |

## Composición del sistema

### Skills atómicos (4)

Cada skill atómico es responsable de una parte del análisis y produce
exactamente tres entregables: documento Markdown, documento PDF, handoff YAML.

| Skill | Cobertura del índice de materias | Handoff producido |
|---|---|---|
| `mv-part1-market-diagnosis` | Secciones 1–6 (definición del negocio, TAM/SAM/SOM, dinámica, competencia, cliente, síntesis) | `handoff_part1.yaml` |
| `mv-part2-strategic-marketing` | Secciones 7–10 (segmentación, targeting, posicionamiento, ERIC, estrategia competitiva) | `handoff_part2.yaml` |
| `mv-part3-operational-marketing` | Secciones 11–16 (producto, precios, canales, comunicación, capacidades, calendario) | `handoff_part3.yaml` |
| `mv-part4-financial-viability` | Secciones 17–27 (modelo financiero, sensibilidad, riesgos, validación, veredicto) | `handoff_part4.yaml` |

### Orquestador (1)

`marketing-viability-orchestrator`. Su única función es:

1. Recibir el brief del caso.
2. Invocar los 4 skills atómicos en secuencia estricta.
3. Validar cada handoff antes de pasar al siguiente.
4. Ejecutar el `cross_quality_check.py` sobre los cuatro handoffs.
5. Producir el dossier consolidado.

El orquestador NO construye los artefactos por sí mismo. Si lo hiciera, sería
un agente.

## Secuencia obligatoria

```
[brief de caso + artefactos previos opcionales]
            ↓
   mv-part1 (Diagnóstico de Mercado)
            ↓
   handoff_part1.yaml + part1_output.md/pdf + charts/
            ↓
   [validate_handoff --part 1] — bloqueo si falla
            ↓
   mv-part2 (Marketing Estratégico)
            ↓
   handoff_part2.yaml + part2_output.md/pdf + charts/
            ↓
   [validate_handoff --part 2] — bloqueo si falla
            ↓
   mv-part3 (Marketing Operativo)
            ↓
   handoff_part3.yaml + part3_output.md/pdf + charts/
            ↓
   [validate_handoff --part 3] — bloqueo si falla
            ↓
   mv-part4 (Análisis Financiero)
            ↓
   handoff_part4.yaml + part4_output.md/pdf + charts/
            ↓
   [validate_handoff --part 4] — bloqueo si falla
            ↓
   [cross_quality_check] — 5 tests inter-bloque
            ↓
   dossier_viabilidad.md + dossier_viabilidad.pdf
   cross_quality_report.md
```

## Contratos de handoff

Cada handoff es un YAML con esquema declarado en
`skills/marketing-viability-orchestrator/references/handoff_schemas.md`. La
estructura mínima de cada handoff es:

```yaml
handoff_partN:
  version: "1.0"
  case_name: <string>
  date: <ISO-8601>
  source_handoffs: [<lista de handoffs upstream>]
  evidence_level: "primary" | "secondary" | "modeled" | "modeled-inherited"
  # ... campos específicos del dominio del skill ...
  required_fields_for_partN+1: [<lista de campos que el siguiente skill consume>]
```

**Reglas inviolables:**

1. **Inmutabilidad**: una vez producido un handoff, no se modifica. Si una
   parte posterior detecta inconsistencia, se documenta como observación.
2. **Completitud verificable**: el skill receptor valida la presencia de los
   campos críticos antes de empezar a trabajar. Si falta alguno, detiene el
   pipeline.
3. **Trazabilidad ascendente**: cada decisión generada en una parte posterior
   debe rastrearse al elemento que la origina en una parte anterior.
4. **No-redundancia**: un campo se define una sola vez en el handoff donde se
   origina; las partes posteriores lo consumen, no lo redefinen.

## Quality gates

El plugin tiene tres niveles de control de calidad, todos automatizados:

### 1. Validación estructural por handoff

Script: `skills/marketing-viability-orchestrator/scripts/validate_handoff.py`.
Verifica que el handoff de la parte N contiene los campos requeridos por la
parte N+1, declarados explícitamente en `REQUIRED_FIELDS_FOR_NEXT_PART`.

Ejecución (cada skill la corre antes de entregar su handoff):

```bash
python scripts/validate_handoff.py --handoff <ruta-yaml> --part <1|2|3|4>
```

Si falla, el pipeline se detiene y se reporta el campo faltante. NO se
improvisa.

### 2. Control de calidad cruzado (5 tests)

Script: `skills/marketing-viability-orchestrator/scripts/cross_quality_check.py`.
Implementa los cinco tests de coherencia inter-bloque definidos en
`integration_rules.md`:

1. **Cobertura de canal por segmento**: cada segmento declarado en Parte 2
   tiene un canal primario en Parte 3.
2. **Activación de productos**: cada producto/servicio del Value Map (Parte 2)
   tiene una key activity asociada en el plan operativo (Parte 3).
3. **Cadena de captura**: cada línea de ingreso modelada en Parte 4 tiene un
   canal de captura definido en Parte 3.
4. **Trazabilidad de hipótesis**: cada hipótesis crítica del programa de
   validación (Parte 4) corresponde a una variable de input que viene de
   Parte 3 o Parte 1.
5. **Coherencia del veredicto**: el veredicto final (Parte 4) es coherente
   con la oportunidad declarada en la síntesis del diagnóstico (Parte 1).

Si algún test falla, el orquestador genera la sección "Observaciones de
coherencia" en el dossier consolidado, identifica explícitamente la
inconsistencia y deja la resolución al usuario. NO modifica los handoffs
automáticamente.

### 3. Verificación estructural del plugin

Script: `scripts/verify_system.py`. Verifica:

- Cada SKILL.md tiene YAML frontmatter válido con `name` y `description`.
- Cada SKILL.md atómico contiene las 8 secciones requeridas.
- El SKILL.md del orquestador contiene las 7 secciones del orquestador y los
  marcadores adicionales.
- Las cláusulas anti-agentificación están presentes con sus 5 marcadores
  básicos (y 3 adicionales en el orquestador).
- El `plugin.json` tiene los campos canónicos con `agent_free: true`.
- El orquestador menciona por nombre todos los skills atómicos.

Ejecución:

```bash
python scripts/verify_system.py .
```

Salida 0 si OK, 1 si hay errores. Antes de cualquier release o merge, este
script debe pasar.

## Reglas anti-agentificación (resumen ejecutivo)

Cada SKILL.md del plugin contiene una sección titulada
"Cláusulas anti-agentificación" con cinco cláusulas básicas (más tres
adicionales en el orquestador). Aquí el resumen ejecutivo:

1. **No-agente**: ningún skill introduce loops ReAct, decide dinámicamente
   qué herramienta invocar, ni compacta contexto por su cuenta.
2. **Respeto a la secuencia**: ningún skill atómico altera el orden definido
   en el orquestador. Inputs fuera de secuencia se rechazan.
3. **Handoff estructurado**: el output canónico es YAML, no prosa libre. Si
   el upstream no cumple el contrato, el skill detiene el pipeline.
4. **Rechazo a sugerencias de agentificación**: si Claude Code (u otro
   asistente) sugiere convertir un skill en agente, fusionar skills, o
   reemplazar handoffs por resúmenes, la respuesta correcta es RECHAZAR.
5. **Preservación contractual**: cualquier modificación debe preservar el
   contrato de entrada, el contrato de salida, la secuencia y las cláusulas
   anti-agentificación.
6. **No-construcción del orquestador**: el orquestador no construye los
   artefactos. Solo invoca skills atómicos y valida sus handoffs.
7. **Secuencia fija**: el orquestador no toma decisiones libres sobre qué
   etapa ejecutar a continuación.
8. **Bifurcaciones explícitas**: solo las declaradas exhaustivamente en
   "Bifurcaciones permitidas". Cualquier rama no declarada es un error de
   arquitectura.

Ver `skills/<cualquiera>/SKILL.md` sección "Cláusulas anti-agentificación"
para la versión literal.

## Cómo modificar el plugin sin degradarlo

Pasos obligatorios para cualquier modificación:

1. Leer `WARNINGS-CLAUDE-CODE.md` y pegarlo al inicio de la sesión de Claude
   Code.
2. Identificar qué SKILL.md o script se va a tocar.
3. Verificar que la modificación NO altera: (a) el contrato de entrada,
   (b) el contrato de salida, (c) la secuencia del orquestador, (d) las
   cláusulas anti-agentificación.
4. Realizar la modificación con cambios mínimos al alcance.
5. Ejecutar `python scripts/verify_system.py .` y confirmar que pasa.
6. Ejecutar el pipeline sobre un caso ejemplo de `examples/` y confirmar que
   los cinco tests cross-quality pasan.
7. Si la modificación cambia el contrato de un handoff, actualizar también
   los skills downstream que lo consumen y la `version` del handoff.

## Decisión sobre empaquetado

Este plugin se distribuye en modo **plugin** (no skills sueltos) porque:

1. Los scripts Python (`generate_partN_charts.py`, `build_part_pdf.py`,
   `validate_handoff.py`, `cross_quality_check.py`, `build_dossier.py`)
   requieren ejecución vía subprocess, soportada de manera nativa en
   Claude Code.
2. La estructura de carpetas con `references/`, `assets/` y `scripts/` por
   skill funciona limpia bajo la convención de plugin.
3. La verificación cruzada y el dossier consolidado requieren acceso al
   filesystem, natural en Claude Code y no garantizado en Claude.ai web.

Si en el futuro se quiere distribuir además como skills sueltos (Claude.ai),
los scripts deberían embeberse en el SKILL.md o reemplazarse por equivalentes
ejecutables in-line; el sistema dejaría de tener la garantía de
reproducibilidad estricta.
