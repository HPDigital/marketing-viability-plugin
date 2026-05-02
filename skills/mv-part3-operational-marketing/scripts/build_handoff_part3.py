#!/usr/bin/env python3
"""
build_handoff_part3.py
Construye el handoff_part3.yaml con los inputs cuantificados para la Parte 4.
"""

import argparse
import sys
from datetime import datetime
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.stderr.write("Falta pyyaml. Instalar con: pip install pyyaml\n")
    sys.exit(2)


def build(inputs: dict) -> dict:
    handoff = {
        "handoff_part3": {
            "version": "1.0",
            "case_name": inputs.get("case_name", "Caso sin nombre"),
            "date": inputs.get("date", datetime.now().strftime("%Y-%m-%d")),
            "source_handoffs": ["handoff_part1.yaml", "handoff_part2.yaml"],
            "product_plan": inputs.get("product_plan", {}),
            "pricing_plan": inputs.get("pricing_plan", {}),
            "channels_plan": inputs.get("channels_plan", {}),
            "communication_plan": inputs.get("communication_plan", {}),
            "capacity_plan": inputs.get("capacity_plan", {}),
            "operational_calendar": inputs.get("operational_calendar", {}),
            "required_fields_for_part4": [
                "pricing_plan.tariff_by_line",
                "pricing_plan.unit_economics_test",
                "channels_plan.cac_blended",
                "capacity_plan.max_capacity_phase_1",
                "capacity_plan.unit_cost_structure",
                "capacity_plan.capacity_jumps",
                "communication_plan.launch_campaign.budget",
                "operational_calendar.year_1_monthly_milestones",
            ],
        }
    }
    return handoff


def main():
    parser = argparse.ArgumentParser(description="Construir handoff_part3.yaml")
    parser.add_argument("--inputs", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    if not args.inputs.exists():
        sys.stderr.write(f"No se encuentra el archivo de inputs: {args.inputs}\n")
        sys.exit(1)

    with open(args.inputs, "r", encoding="utf-8") as f:
        inputs = yaml.safe_load(f) or {}

    handoff = build(inputs)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        yaml.dump(handoff, f, allow_unicode=True, sort_keys=False)
    print(f"handoff_part3.yaml generado en {args.output}")


if __name__ == "__main__":
    main()
