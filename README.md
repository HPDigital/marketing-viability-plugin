# Marketing Viability Plugin

Plugin Claude Code que provee un *system of skills* determinista para producir
un análisis profesional de viabilidad de marketing y financiera de un nuevo
negocio. Compuesto por un skill orquestador y cuatro skills atómicos
encadenados por handoffs YAML canónicos, con cláusulas anti-agentificación
embebidas en cada artefacto.

## Qué produce

A partir de un brief de caso (con o sin artefactos previos de discovery
JTBD/VPC/Blue Ocean/BMC), el plugin genera por cada parte:

- `partN_output.md`: documento en prosa académica con índice canónico.
- `partN_output.pdf`: versión PDF profesional A4 con gráficos incrustados.
- `handoff_partN.yaml`: artefacto canónico para la siguiente parte.
- `charts/*.png`: 6–9 gráficos por parte a 300 dpi (matplotlib).

Y al final de la secuencia, un dossier consolidado:

- `dossier_viabilidad.md` y `dossier_viabilidad.pdf`.
- `cross_quality_report.md`: reporte de los cinco tests de coherencia
  inter-bloque (segmentación, posicionamiento, cadena costos, hipótesis
  críticas, veredicto).

## Arquitectura

```
[brief de caso + artefactos previos opcionales]
            ↓
   mv-part1-market-diagnosis              → handoff_part1.yaml
            ↓ (validate_handoff --part 1)
   mv-part2-strategic-marketing           → handoff_part2.yaml
            ↓ (validate_handoff --part 2)
   mv-part3-operational-marketing         → handoff_part3.yaml
            ↓ (validate_handoff --part 3)
   mv-part4-financial-viability           → handoff_part4.yaml
            ↓ (validate_handoff --part 4)
   cross_quality_check (5 inter-block tests)
            ↓
   marketing-viability-orchestrator → dossier_viabilidad.md/pdf
```

La secuencia es estricta. Cada paso valida el handoff upstream antes de
trabajar; si la validación falla, el pipeline se detiene y reporta. Esta
rigidez es deliberada: es el mecanismo que distingue un *system of skills*
de un agente.

## Instalación

### Opción A — Marketplace (recomendado)

```
/plugin marketplace add https://github.com/HPDigital/marketing-viability-plugin
/plugin install marketing-viability-plugin@hpdigital-marketplace
```

### Opción B — Carga directa

Copiar la carpeta `marketing-viability-plugin/` a `~/.claude/plugins/` y
reiniciar Claude Code.

### Dependencias Python

Para que los scripts de gráficos y PDF funcionen, instalar:

```bash
pip install pyyaml matplotlib numpy markdown weasyprint openpyxl
```

En Windows, `weasyprint` requiere GTK. Alternativa: instalar `pandoc` y
`xelatex` (los scripts caen a pandoc si weasyprint falla). Ver
[INSTALL.md](INSTALL.md) para detalles.

## Uso

Una vez instalado, el orquestador se activa con triggers como:

- "Análisis de viabilidad de marketing para [caso]"
- "Estudio de viabilidad de un nuevo negocio en [sector] [geografía]"
- "Plan de marketing estratégico y operativo con análisis financiero"
- "Ejecuta el pipeline completo de viabilidad"

Los skills atómicos también pueden invocarse aisladamente (cada uno tiene
sus propios triggers), siempre que el handoff upstream exista.

## Qué NO hace

- No es un agente. No improvisa pasos ni decide dinámicamente qué herramienta
  invocar.
- No salta etapas. Sin handoff upstream válido, el skill downstream se detiene.
- No regenera contexto en lenguaje natural. Los handoffs son YAML estructurado
  validable.
- No emite veredicto financiero sin sensibilidad documentada.
- No inventa datos. Si no hay dato, declara "no disponible" y propone método
  de obtención.

## Documentación

- [ARCHITECTURE.md](ARCHITECTURE.md) — arquitectura del system of skills, contratos de handoff, reglas anti-agentificación.
- [WARNINGS-CLAUDE-CODE.md](WARNINGS-CLAUDE-CODE.md) — pegar al inicio de cualquier sesión de Claude Code que vaya a modificar el plugin.
- [INSTALL.md](INSTALL.md) — instalación detallada con dependencias Python.
- [examples/](examples/) — ejemplo mínimo de inputs (`case_brief.md` + `chart_inputs.yaml`).

## Verificación

Antes de empaquetar o tras cualquier modificación, ejecutar:

```bash
python scripts/verify_system.py .
```

Verifica que cada SKILL.md cumple el contrato estructural, que las cláusulas
anti-agentificación están presentes, que el orquestador menciona por nombre
todos los skills atómicos, y que el `plugin.json` tiene los campos canónicos
con `agent_free: true`.

## Licencia

MIT. Ver [LICENSE](LICENSE).

## Autor

Herwig Poleyn Paz · hpoleynpaz@gmail.com
