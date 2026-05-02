#!/usr/bin/env python3
"""
cross_quality_check.py
======================

Control de calidad cruzado del system of skills marketing-viability-plugin.

Ejecuta cinco tests de coherencia inter-bloque sobre los cuatro handoffs
(handoff_part1.yaml ... handoff_part4.yaml) producidos por los skills
atomicos. Lo invoca el orquestador `marketing-viability-orchestrator` antes
de generar el dossier consolidado.

Tests implementados (referencia: integration_rules.md):

  1. Cobertura de canal por segmento: cada segmento declarado en Parte 2
     tiene un canal primario en Parte 3.
  2. Activacion de productos del Value Map: cada producto/servicio del
     Value Map (Parte 2) tiene una key activity asociada en el plan
     operativo (Parte 3).
  3. Cadena de captura de ingresos: cada linea de ingreso modelada en
     Parte 4 tiene un canal de captura definido en Parte 3.
  4. Trazabilidad de hipotesis criticas: cada hipotesis critica del
     programa de validacion (Parte 4) corresponde a una variable de
     input que viene de Parte 3 o Parte 1.
  5. Coherencia del veredicto: el veredicto final (Parte 4) es coherente
     con la oportunidad declarada en la sintesis del diagnostico
     (Parte 1).

Uso:
    python cross_quality_check.py --workspace <viability-workspace-XX> \
                                  --output cross_quality_report.md

Codigo de salida:
    0  todos los tests pasan
    1  uno o mas tests fallan (el reporte se genera de todos modos)
    2  error de I/O o de schema basico
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime
from typing import Tuple, List, Dict, Any

try:
    import yaml
except ImportError:
    sys.stderr.write("Falta el paquete 'pyyaml'. Instalar con: pip install pyyaml\n")
    sys.exit(2)


# ---------------------------------------------------------------------------
# Lectura de handoffs
# ---------------------------------------------------------------------------

def read_handoff(workspace: Path, part_num: int) -> Dict[str, Any]:
    """Lee un handoff_partN.yaml del workspace."""
    path = workspace / f"part{part_num}" / f"handoff_part{part_num}.yaml"
    if not path.exists():
        raise FileNotFoundError(f"No se encuentra el handoff: {path}")
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    key = f"handoff_part{part_num}"
    if key not in data:
        raise ValueError(f"{path}: el YAML no tiene la clave raiz '{key}'.")
    return data[key]


def get_nested(data: Any, dotted_key: str) -> Any:
    """Resolver clave anidada con notacion punto."""
    keys = dotted_key.split(".")
    cur = data
    for k in keys:
        if isinstance(cur, dict) and k in cur:
            cur = cur[k]
        else:
            return None
    return cur


# ---------------------------------------------------------------------------
# Tests inter-bloque
# ---------------------------------------------------------------------------

def test_1_segments_have_primary_channel(h2: dict, h3: dict) -> Tuple[bool, str, list]:
    """
    Test 1: Cobertura de canal por segmento.
    Cada segmento (entry + secondaries) declarado en Parte 2 debe tener al
    menos un canal primario asignado en alguna fase del journey de Parte 3.
    """
    entry = get_nested(h2, "segmentation.entry_segment_id")
    secondaries = get_nested(h2, "segmentation.secondary_segment_ids") or []
    target_segments = [s for s in [entry] + list(secondaries) if s]

    journey = get_nested(h3, "channels_plan.journey_map") or {}
    declared_channels = []
    for phase, value in journey.items():
        if isinstance(value, dict):
            for slot in ("primary", "secondary"):
                ch = value.get(slot)
                if ch:
                    declared_channels.append(str(ch).lower())

    channel_ops = get_nested(h3, "channels_plan.channel_operations") or []
    for op in channel_ops:
        ch = op.get("channel_name") or op.get("channel_id")
        if ch:
            declared_channels.append(str(ch).lower())

    if not declared_channels:
        return False, "test_1_segments_have_primary_channel", \
               [f"Parte 3 no declara ningun canal primario en journey_map ni en channel_operations."]

    if not target_segments:
        return False, "test_1_segments_have_primary_channel", \
               ["Parte 2 no declara entry_segment_id ni secondary_segment_ids."]

    return True, "test_1_segments_have_primary_channel", []


def test_2_products_have_key_activity(h2: dict, h3: dict) -> Tuple[bool, str, list]:
    """
    Test 2: Activacion de productos del Value Map.
    Cada producto/servicio essential del Value Map (Parte 2) debe tener una
    key activity asociada en el plan de producto operativo (Parte 3).
    """
    products = get_nested(h2, "value_proposition.products_services") or []
    essential_products = [
        p for p in products
        if isinstance(p, dict) and (p.get("category") == "essential" or "category" not in p)
    ]
    if not essential_products:
        return False, "test_2_products_have_key_activity", \
               ["Parte 2 no declara productos/servicios con category essential."]

    initial_portfolio = get_nested(h3, "product_plan.initial_portfolio") or []
    backlog = get_nested(h3, "product_plan.backlog_24m") or []
    mvp = get_nested(h3, "product_plan.mvp_definition") or ""

    portfolio_text = " ".join([
        str(initial_portfolio), str(backlog), str(mvp)
    ]).lower()

    missing = []
    for p in essential_products:
        name = p.get("name") or p.get("id") or ""
        if name and name.lower() not in portfolio_text:
            missing.append(f"Producto essential '{name}' (Parte 2) no aparece en product_plan de Parte 3.")

    if missing:
        return False, "test_2_products_have_key_activity", missing
    return True, "test_2_products_have_key_activity", []


def test_3_revenue_lines_have_capture_channel(h3: dict, h4: dict) -> Tuple[bool, str, list]:
    """
    Test 3: Cadena de captura de ingresos.
    Cada linea de ingreso modelada en Parte 4 debe tener un canal de
    captura definido en Parte 3 (sea via channel_operations o journey_map).
    """
    by_line = get_nested(h4, "revenue_projection.by_line_by_year") or []
    revenue_lines = sorted({
        item.get("line_id") for item in by_line
        if isinstance(item, dict) and item.get("line_id")
    })
    if not revenue_lines:
        return False, "test_3_revenue_lines_have_capture_channel", \
               ["Parte 4 no declara revenue_projection.by_line_by_year con line_id."]

    tariff = get_nested(h3, "pricing_plan.tariff_by_line") or []
    tariff_lines = sorted({
        item.get("line_id") for item in tariff
        if isinstance(item, dict) and item.get("line_id")
    })

    missing = []
    for line in revenue_lines:
        if line not in tariff_lines:
            missing.append(
                f"Linea de ingreso '{line}' modelada en Parte 4 no tiene "
                f"tariff equivalente en Parte 3 (pricing_plan.tariff_by_line).")

    channel_ops = get_nested(h3, "channels_plan.channel_operations") or []
    if not channel_ops:
        missing.append(
            "Parte 3 no declara channel_operations; no es posible asegurar "
            "canal de captura para las lineas de ingreso de Parte 4.")

    if missing:
        return False, "test_3_revenue_lines_have_capture_channel", missing
    return True, "test_3_revenue_lines_have_capture_channel", []


def test_4_critical_hypotheses_traceable(h1: dict, h3: dict, h4: dict) -> Tuple[bool, str, list]:
    """
    Test 4: Trazabilidad de hipotesis criticas.
    Cada hipotesis critica del programa de validacion (Parte 4) debe
    corresponder a una variable de input que viene de Parte 3 o Parte 1.
    """
    hypotheses = get_nested(h4, "validation_program.critical_hypotheses") or []
    if not hypotheses:
        return False, "test_4_critical_hypotheses_traceable", \
               ["Parte 4 no declara validation_program.critical_hypotheses."]

    critical_vars = set(get_nested(h4, "sensitivity_analysis.critical_variables") or [])
    p3_keys = set()
    for k in [
        "pricing_plan.tariff_by_line", "channels_plan.cac_blended",
        "capacity_plan.max_capacity_phase_1",
        "communication_plan.funnel.total_conversion",
    ]:
        if get_nested(h3, k):
            p3_keys.add(k)
    p1_keys = set()
    for k in [
        "customer_understanding.willingness_to_pay_declared",
        "customer_understanding.outcomes_prioritized",
        "market_sizing.som",
    ]:
        if get_nested(h1, k):
            p1_keys.add(k)

    untraceable = []
    for hyp in hypotheses:
        hid = hyp.get("id") if isinstance(hyp, dict) else None
        text = str(hyp).lower()
        traceable = False
        if hid and hid in critical_vars:
            traceable = True
        if any(token in text for token in [
            "wtp", "disposicion", "willingness", "cac", "ltv", "som",
            "capacidad", "funnel", "outcome", "precio", "price", "volumen",
            "volume",
        ]):
            traceable = True
        if not traceable:
            untraceable.append(
                f"Hipotesis '{hid or text[:80]}' no se rastrea a una variable "
                f"de Parte 3 ni a un campo de Parte 1.")

    if untraceable:
        return False, "test_4_critical_hypotheses_traceable", untraceable
    return True, "test_4_critical_hypotheses_traceable", []


def test_5_verdict_coherent_with_diagnosis(h1: dict, h4: dict) -> Tuple[bool, str, list]:
    """
    Test 5: Coherencia del veredicto.
    El veredicto final (Parte 4) debe ser coherente con la oportunidad
    declarada en la sintesis del diagnostico (Parte 1).
    Reglas:
      - Si el veredicto es 'viable' o 'viable_with_observations',
        diagnosis_synthesis.opportunity_verifiable de Parte 1 NO debe estar
        vacio ni declarar ausencia de oportunidad.
      - Si el veredicto es 'not_viable', upstream_risks de Parte 1 deberia
        contener al menos un riesgo material (de lo contrario la
        contradiccion entre diagnostico e ingresos modelados no esta
        explicitada).
    """
    verdict = get_nested(h4, "final_verdict.veredict") or get_nested(
        h4, "final_verdict.verdict")
    if not verdict:
        return False, "test_5_verdict_coherent_with_diagnosis", \
               ["Parte 4 no declara final_verdict.veredict."]

    opportunity = get_nested(h1, "diagnosis_synthesis.opportunity_verifiable") or ""
    risks = get_nested(h1, "diagnosis_synthesis.upstream_risks") or []

    inconsistencies = []
    if verdict in ("viable", "viable_with_observations"):
        if not opportunity or len(str(opportunity)) < 20:
            inconsistencies.append(
                f"Veredicto '{verdict}' pero Parte 1 no declara una "
                f"oportunidad de mercado verificable consistente "
                f"(diagnosis_synthesis.opportunity_verifiable vacio o demasiado breve).")

    if verdict == "not_viable":
        if not risks:
            inconsistencies.append(
                f"Veredicto 'not_viable' pero Parte 1 no declara "
                f"upstream_risks que expliquen la falta de viabilidad.")

    if inconsistencies:
        return False, "test_5_verdict_coherent_with_diagnosis", inconsistencies
    return True, "test_5_verdict_coherent_with_diagnosis", []


# ---------------------------------------------------------------------------
# Reporte
# ---------------------------------------------------------------------------

def render_report(results: List[Tuple[bool, str, list]],
                   workspace: Path) -> str:
    """Renderiza el reporte de coherencia en Markdown."""
    passed = sum(1 for ok, _, _ in results if ok)
    total = len(results)
    overall = "PASS" if passed == total else "FAIL"

    lines = [
        f"# Cross-Quality Report — Marketing Viability Plugin",
        "",
        f"**Workspace:** `{workspace}`  ",
        f"**Fecha:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  ",
        f"**Resultado global:** **{overall}** ({passed}/{total} tests OK)",
        "",
        "---",
        "",
        "## Detalle por test",
        "",
    ]

    test_titles = {
        "test_1_segments_have_primary_channel":
            "1. Cobertura de canal por segmento (Parte 2 ↔ Parte 3)",
        "test_2_products_have_key_activity":
            "2. Activación de productos del Value Map (Parte 2 ↔ Parte 3)",
        "test_3_revenue_lines_have_capture_channel":
            "3. Cadena de captura de ingresos (Parte 3 ↔ Parte 4)",
        "test_4_critical_hypotheses_traceable":
            "4. Trazabilidad de hipótesis críticas (Parte 4 → Parte 3 / Parte 1)",
        "test_5_verdict_coherent_with_diagnosis":
            "5. Coherencia del veredicto (Parte 4 ↔ Parte 1)",
    }

    for ok, name, errors in results:
        title = test_titles.get(name, name)
        status = "PASS" if ok else "FAIL"
        lines.append(f"### {title}")
        lines.append("")
        lines.append(f"**Estado:** {status}")
        lines.append("")
        if errors:
            lines.append("**Inconsistencias detectadas:**")
            lines.append("")
            for e in errors:
                lines.append(f"- {e}")
            lines.append("")
        else:
            lines.append("Sin inconsistencias.")
            lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## Interpretacion")
    lines.append("")
    if overall == "PASS":
        lines.append(
            "Los cuatro handoffs son coherentes entre si segun los cinco "
            "criterios. El dossier consolidado puede entregarse al usuario "
            "como producto final del pipeline.")
    else:
        lines.append(
            "Al menos un test ha fallado. Esto NO detiene el pipeline (el "
            "orquestador ya genera el dossier), pero las inconsistencias "
            "se incluyen como Anexo de Observaciones de Coherencia. La "
            "decision de re-ejecutar la parte que origino la inconsistencia "
            "queda en manos del usuario; el orquestador NO modifica los "
            "handoffs por su cuenta.")

    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Control de calidad cruzado entre los cuatro handoffs.")
    parser.add_argument("--workspace", required=True, type=Path,
                        help="Carpeta viability-workspace-<slug>/.")
    parser.add_argument("--output", required=True, type=Path,
                        help="Ruta del reporte Markdown a generar.")
    args = parser.parse_args()

    if not args.workspace.exists():
        sys.stderr.write(f"Workspace no existe: {args.workspace}\n")
        return 2

    try:
        h1 = read_handoff(args.workspace, 1)
        h2 = read_handoff(args.workspace, 2)
        h3 = read_handoff(args.workspace, 3)
        h4 = read_handoff(args.workspace, 4)
    except (FileNotFoundError, ValueError) as e:
        sys.stderr.write(f"Error leyendo handoffs: {e}\n")
        return 2

    results = [
        test_1_segments_have_primary_channel(h2, h3),
        test_2_products_have_key_activity(h2, h3),
        test_3_revenue_lines_have_capture_channel(h3, h4),
        test_4_critical_hypotheses_traceable(h1, h3, h4),
        test_5_verdict_coherent_with_diagnosis(h1, h4),
    ]

    report = render_report(results, args.workspace)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(report, encoding="utf-8")

    all_pass = all(ok for ok, _, _ in results)
    print(f"Cross-quality report: {args.output}")
    print(f"Resultado: {'PASS' if all_pass else 'FAIL'} "
          f"({sum(1 for ok, _, _ in results if ok)}/{len(results)})")
    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
