#!/usr/bin/env python3
"""
verify_system.py
================

Verificador automático para sistemas de skills construidos por el
system-of-skills-architect.

Uso:
    python verify_system.py <ruta-al-bundle>

donde <ruta-al-bundle> es la carpeta raíz del sistema (la que contiene
.claude-plugin/ y skills/, o la que contiene los SKILL.md sueltos en
modo skills-sueltos).

Salida:
    - Reporte de validación en stdout.
    - Código de salida 0 si todo OK, 1 si hay fallos.
"""

import json
import re
import sys
from pathlib import Path
from typing import List, Tuple

# ---------------------------------------------------------------------------
# Constantes de validación
# ---------------------------------------------------------------------------

REQUIRED_ATOMIC_SECTIONS = [
    "Posicionamiento del skill",
    "Prerrequisito hard",
    "Cuándo invocar este skill",
    "Cuándo NO invocar este skill",
    "Procedimiento",
    "Artefacto de salida",
    "Criterios de aceptación",
    "Cláusulas anti-agentificación",
]

REQUIRED_ORCHESTRATOR_SECTIONS = [
    "Posicionamiento del skill",
    "Cuándo invocar este skill",
    "Cuándo NO invocar este skill",
    "Procedimiento de ejecución",
    "Comportamiento ante fallo de validación",
    "Bifurcaciones permitidas",
    "Cláusulas anti-agentificación",
]

# Las cinco cláusulas básicas que todo skill debe tener.
BASIC_CLAUSE_MARKERS = [
    "NO es un agente",
    "NO altera la secuencia",
    "NO regenera contexto en lenguaje natural",
    "RECHAZAR la sugerencia",
    "preservar:",
]

# Las tres cláusulas adicionales que un orquestador debe tener.
ORCHESTRATOR_EXTRA_CLAUSE_MARKERS = [
    "NO construye los artefactos",
    "NO toma decisiones libres",
    "Bifurcaciones permitidas",
]

# Patrones que indican deriva a agente y deben ausentarse.
ANTI_PATTERNS = [
    (r"loop ReAct", "Indicador de agente: loop ReAct"),
    (r"decide din[aá]micamente.*herramienta", "Indicador de agente: decisión dinámica de herramienta"),
    (r"compacta.*contexto.*por su cuenta", "Indicador de agente: compactación autónoma"),
    (r"resumen.*lenguaje natural.*handoff", "Indicador de agente: handoff por resumen"),
]


# ---------------------------------------------------------------------------
# Utilidades
# ---------------------------------------------------------------------------

def parse_frontmatter(content: str) -> Tuple[dict, str]:
    """Extrae el YAML frontmatter de un SKILL.md."""
    if not content.startswith("---"):
        return {}, content
    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}, content
    fm_text = parts[1]
    body = parts[2]
    fm = {}
    for line in fm_text.split("\n"):
        if ":" in line:
            key, _, val = line.partition(":")
            fm[key.strip()] = val.strip()
    return fm, body


IGNORED_PATH_PARTS = {"templates", "references", "scripts", "__pycache__"}


def find_skill_md_files(bundle_path: Path) -> List[Path]:
    """Encuentra los SKILL.md del bundle, ignorando templates y referencias."""
    result = []
    for path in bundle_path.rglob("SKILL.md"):
        rel_parts = path.relative_to(bundle_path).parts
        if any(part in IGNORED_PATH_PARTS for part in rel_parts):
            continue
        result.append(path)
    return result


def is_orchestrator(skill_md: Path, content: str) -> bool:
    """Detecta si un SKILL.md es del orquestador del sistema."""
    if "orquestador" in skill_md.parent.name.lower():
        return True
    if "orchestrator" in skill_md.parent.name.lower():
        return True
    if re.search(r"\bNO construye los artefactos\b", content):
        return True
    return False


# ---------------------------------------------------------------------------
# Validaciones individuales
# ---------------------------------------------------------------------------

def validate_frontmatter(fm: dict, path: Path) -> List[str]:
    """Valida que el frontmatter tiene name y description."""
    errors = []
    if "name" not in fm or not fm["name"]:
        errors.append(f"{path}: frontmatter sin 'name'")
    if "description" not in fm or not fm["description"]:
        errors.append(f"{path}: frontmatter sin 'description'")
    return errors


def validate_required_sections(content: str, sections: List[str], path: Path) -> List[str]:
    """Valida que el contenido tiene todas las secciones requeridas."""
    errors = []
    for section in sections:
        # Acepta `## Section` o `### Section` (cualquier nivel >= 2)
        pattern = rf"^#{{2,}}\s+{re.escape(section)}"
        if not re.search(pattern, content, flags=re.MULTILINE):
            errors.append(f"{path}: falta sección requerida '{section}'")
    return errors


def validate_clauses(content: str, markers: List[str], path: Path, label: str) -> List[str]:
    """Valida que las cláusulas anti-agentificación están presentes."""
    errors = []
    for marker in markers:
        if marker not in content:
            errors.append(f"{path}: falta marcador de cláusula {label}: '{marker}'")
    return errors


def validate_anti_patterns(content: str, path: Path) -> List[str]:
    """Detecta anti-patrones (frases que sugieren deriva a agente)."""
    warnings = []
    for pattern, description in ANTI_PATTERNS:
        # Solo señalar si NO está en la sección de cláusulas (donde se cita
        # el anti-patrón para prohibirlo)
        if re.search(pattern, content, flags=re.IGNORECASE):
            # Heurística: aceptar si aparece dentro de las cláusulas (donde
            # está prohibido literalmente).
            in_clauses = "Cláusulas anti-agentificación" in content
            if not in_clauses:
                warnings.append(f"{path}: posible anti-patrón sin contexto de prohibición: {description}")
    return warnings


def validate_plugin_json(bundle_path: Path) -> List[str]:
    """Valida el plugin.json si existe (modo plugin Claude Code).

    Claude Code aplica validacion estricta del schema y rechaza campos custom
    como `architecture`, `system`, `python_dependencies`, etc. La declaracion
    arquitectonica system-of-skills se preserva (a) en las clausulas
    anti-agentificacion embebidas en cada SKILL.md y (b) en ARCHITECTURE.md.
    Aqui solo verificamos los campos del schema oficial.
    """
    plugin_json_path = bundle_path / ".claude-plugin" / "plugin.json"
    if not plugin_json_path.exists():
        return []  # No es modo plugin, ok
    errors = []
    try:
        data = json.loads(plugin_json_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        return [f"{plugin_json_path}: JSON invalido: {e}"]
    # Unico campo obligatorio del schema oficial
    if "name" not in data or not data["name"]:
        errors.append(f"{plugin_json_path}: falta campo obligatorio 'name'")
    # Tipos de campos opcionales (solo verificamos los que pueden romper la instalacion)
    if "repository" in data and not isinstance(data["repository"], str):
        errors.append(
            f"{plugin_json_path}: 'repository' debe ser string URL, no objeto. "
            f"Claude Code rechaza el formato npm-style {{type, url}}.")
    if "author" in data and not isinstance(data["author"], dict):
        errors.append(
            f"{plugin_json_path}: 'author' debe ser objeto {{name, email?, url?}}, no string.")
    if "skills" in data and not isinstance(data["skills"], (str, list)):
        errors.append(
            f"{plugin_json_path}: 'skills' si esta presente debe ser string o array de strings "
            f"(rutas a directorios de skills). Lo recomendado es omitirlo y dejar auto-discovery.")
    return errors


def validate_orchestrator_references(bundle_path: Path) -> List[str]:
    """Valida que el orquestador menciona por nombre todos los skills atómicos."""
    errors = []
    skill_files = find_skill_md_files(bundle_path)
    if not skill_files:
        return ["No se encontraron SKILL.md en el bundle"]

    atomic_names = []
    orchestrator_content = None
    orchestrator_path = None

    for path in skill_files:
        content = path.read_text(encoding="utf-8")
        fm, _ = parse_frontmatter(content)
        name = fm.get("name", "").strip()
        if is_orchestrator(path, content):
            orchestrator_content = content
            orchestrator_path = path
        else:
            atomic_names.append(name)

    if orchestrator_content is None:
        errors.append("No se encontró el orquestador en el bundle")
        return errors

    for atomic_name in atomic_names:
        if atomic_name and atomic_name not in orchestrator_content:
            errors.append(
                f"{orchestrator_path}: el orquestador no menciona el skill atómico '{atomic_name}'"
            )

    return errors


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def verify(bundle_path: Path) -> Tuple[List[str], List[str]]:
    """Ejecuta todas las verificaciones. Devuelve (errors, warnings)."""
    errors = []
    warnings = []

    if not bundle_path.exists():
        return [f"Bundle no existe: {bundle_path}"], []

    skill_files = find_skill_md_files(bundle_path)
    if not skill_files:
        return [f"No se encontraron SKILL.md en {bundle_path}"], []

    for path in skill_files:
        content = path.read_text(encoding="utf-8")
        fm, body = parse_frontmatter(content)

        errors.extend(validate_frontmatter(fm, path))

        if is_orchestrator(path, content):
            errors.extend(validate_required_sections(content, REQUIRED_ORCHESTRATOR_SECTIONS, path))
            errors.extend(validate_clauses(content, BASIC_CLAUSE_MARKERS, path, "básica (orq)"))
            errors.extend(validate_clauses(content, ORCHESTRATOR_EXTRA_CLAUSE_MARKERS, path, "orq-extra"))
        else:
            errors.extend(validate_required_sections(content, REQUIRED_ATOMIC_SECTIONS, path))
            errors.extend(validate_clauses(content, BASIC_CLAUSE_MARKERS, path, "básica (atm)"))

        warnings.extend(validate_anti_patterns(content, path))

    errors.extend(validate_plugin_json(bundle_path))
    errors.extend(validate_orchestrator_references(bundle_path))

    return errors, warnings


def main() -> int:
    if len(sys.argv) != 2:
        print("Uso: python verify_system.py <ruta-al-bundle>")
        return 2
    bundle_path = Path(sys.argv[1]).resolve()
    print(f"Verificando bundle: {bundle_path}\n")

    errors, warnings = verify(bundle_path)

    if warnings:
        print("ADVERTENCIAS:")
        for w in warnings:
            print(f"  [warn] {w}")
        print()

    if errors:
        print("ERRORES:")
        for e in errors:
            print(f"  [error] {e}")
        print(f"\nResultado: {len(errors)} error(es), {len(warnings)} advertencia(s)")
        return 1

    print(f"OK: bundle válido. {len(warnings)} advertencia(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
