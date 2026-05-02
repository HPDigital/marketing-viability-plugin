#!/usr/bin/env python3
"""
validate_handoff.py
Valida que un archivo handoff YAML contenga los campos requeridos por el siguiente skill del pipeline.

Uso:
    python validate_handoff.py --handoff <ruta-yaml> --part <1|2|3|4>
"""

import argparse
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.stderr.write("Falta el paquete 'pyyaml'. Instalar con: pip install pyyaml\n")
    sys.exit(2)


REQUIRED_FIELDS_FOR_NEXT_PART = {
    1: [
        "handoff_part1.business_definition",
        "handoff_part1.market_sizing.sam",
        "handoff_part1.market_sizing.som",
        "handoff_part1.customer_understanding.job_statement",
        "handoff_part1.customer_understanding.jobs_functional",
        "handoff_part1.customer_understanding.four_forces",
        "handoff_part1.customer_understanding.outcomes_prioritized",
        "handoff_part1.customer_understanding.willingness_to_pay_declared",
        "handoff_part1.preliminary_segments",
        "handoff_part1.competitive_landscape.price_benchmark",
    ],
    2: [
        "handoff_part2.segmentation.entry_segment_id",
        "handoff_part2.targeting.icp",
        "handoff_part2.positioning.positioning_statement",
        "handoff_part2.positioning.reason_to_believe_assets",
        "handoff_part2.blue_ocean.factors_buyer_side",
        "handoff_part2.blue_ocean.eliminate",
        "handoff_part2.blue_ocean.create",
        "handoff_part2.value_proposition.main_statement",
        "handoff_part2.value_proposition.products_services",
    ],
    3: [
        "handoff_part3.pricing_plan.tariff_by_line",
        "handoff_part3.pricing_plan.unit_economics_test",
        "handoff_part3.channels_plan.cac_blended",
        "handoff_part3.capacity_plan.max_capacity_phase_1",
        "handoff_part3.capacity_plan.unit_cost_structure",
        "handoff_part3.capacity_plan.capacity_jumps",
        "handoff_part3.communication_plan.launch_campaign.budget",
        "handoff_part3.operational_calendar.year_1_monthly_milestones",
    ],
    4: [
        "handoff_part4.viability_indicators.npv",
        "handoff_part4.viability_indicators.irr",
        "handoff_part4.unit_economics.ltv_cac_ratio",
        "handoff_part4.sensitivity_analysis.critical_variables",
        "handoff_part4.validation_program.critical_hypotheses",
        "handoff_part4.final_verdict.veredict",
    ],
}


def get_nested(data, dotted_key):
    """Resolver clave anidada con notación punto."""
    keys = dotted_key.split(".")
    cur = data
    for k in keys:
        if isinstance(cur, dict) and k in cur:
            cur = cur[k]
        else:
            return None
    return cur


def validate(handoff_path: Path, part_number: int) -> tuple[bool, list]:
    if not handoff_path.exists():
        return False, [f"El archivo {handoff_path} no existe."]

    with open(handoff_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    required = REQUIRED_FIELDS_FOR_NEXT_PART.get(part_number, [])
    if not required:
        return False, [f"No hay reglas de validación para la parte {part_number}."]

    missing = []
    for field in required:
        value = get_nested(data, field)
        if value is None or (isinstance(value, (list, dict)) and len(value) == 0):
            missing.append(field)

    return (len(missing) == 0), missing


def main():
    parser = argparse.ArgumentParser(description="Validador de handoffs entre skills.")
    parser.add_argument("--handoff", required=True, type=Path, help="Ruta al archivo YAML del handoff.")
    parser.add_argument("--part", required=True, type=int, choices=[1, 2, 3, 4], help="Número de la parte cuyo handoff se valida.")
    args = parser.parse_args()

    ok, missing = validate(args.handoff, args.part)
    if ok:
        print(f"OK. Handoff de la parte {args.part} contiene todos los campos requeridos.")
        sys.exit(0)
    else:
        print(f"FAIL. Handoff de la parte {args.part} incompleto. Faltan los siguientes campos:")
        for m in missing:
            print(f"  - {m}")
        sys.exit(1)


if __name__ == "__main__":
    main()
