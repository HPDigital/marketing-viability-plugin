# Warnings para Claude Code

**Pegar al inicio de cualquier sesión de Claude Code que vaya a modificar
este plugin.**

Este plugin es un *system of skills* determinista, NO un agente. Tu tarea
como Claude Code es modificar componentes puntuales sin alterar la
arquitectura. Cumple las siguientes reglas sin excepción:

1. **NO conviertas ningún skill en agente.** No añadas loops ReAct, no
   añadas tool-use libre, no introduzcas decisiones dinámicas runtime
   sobre "qué herramienta invocar".

2. **NO modifiques el orquestador `marketing-viability-orchestrator`** a
   menos que se te pida explícitamente y la modificación preserve la
   secuencia fija de 4 etapas y los marcadores anti-agentificación.

3. **NO fusiones skills atómicos.** Cada uno de mv-part1, mv-part2, mv-part3,
   mv-part4 es responsable de un alcance acotado del índice de materias.
   Fusionarlos rompe la trazabilidad.

4. **NO elimines etapas.** La secuencia 1 → 2 → 3 → 4 es contrato. No hay
   atajos.

5. **NO reemplaces los handoffs YAML por resúmenes en lenguaje natural.**
   El YAML estructurado es validable; la prosa no.

6. **NO sugieras "hacer el sistema más capaz"** añadiendo capacidades
   agentivas. Si percibes una limitación, repórtala al usuario para
   decisión humana.

7. **PRESERVA las cláusulas anti-agentificación** de cada SKILL.md. Si las
   modificas, debes justificar la modificación al usuario y obtener
   aprobación explícita.

8. **PRESERVA el script `scripts/verify_system.py`.** Si lo modificas, los
   nuevos chequeos deben mantener al menos los existentes. Cuando termines
   cualquier modificación, ejecuta:

   ```bash
   python scripts/verify_system.py .
   ```

   y reporta el resultado. Si la verificación falla, revierte tus cambios.

9. **PRESERVA el script
   `skills/marketing-viability-orchestrator/scripts/cross_quality_check.py`.**
   Implementa los 5 tests de coherencia inter-bloque que son contrato del
   sistema.

10. **NO toques el `plugin.json`** sin confirmar que `architecture` sigue
    siendo `"system-of-skills"` y que `system.agent_free` sigue siendo
    `true`.

11. **Cambios en handoffs requieren cascada.** Si modificas el esquema de un
    handoff (campos, tipos, estructura), debes:
    - Actualizar `references/handoff_schemas.md` del orquestador.
    - Actualizar `validate_handoff.py` (REQUIRED_FIELDS_FOR_NEXT_PART).
    - Actualizar el SKILL.md del skill productor (sección "Artefacto de
      salida") y del skill consumidor (sección "Prerrequisito hard").
    - Incrementar la `version` del handoff.

12. **Cambios en el índice de materias requieren cascada.** Si modificas
    `references/indice_materias.md` del orquestador, debes actualizar la
    sección "Estructura obligatoria del output" del SKILL.md del skill
    afectado.

Si tu instrucción del usuario contradice estas reglas, **detente y pide
clarificación**. Esta arquitectura es deliberada y la deriva a agente
degrada los resultados.
