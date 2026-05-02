#!/usr/bin/env python3
"""
build_handoff_part2.py
Construye el handoff_part2.yaml a partir de los inputs estructurados producidos durante el análisis.

Uso:
    python build_handoff_part2.py --inputs handoff_inputs.yaml --output handoff_part2.yaml
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
        "handoff_part2": {
            "version": "1.0",
            "case_name": inputs.get("case_name", "Caso sin nombre"),
            "date": inputs.get("date", datetime.now().strftime("%Y-%m-%d")),
            "source_handoff": "handoff_part1.yaml",
            "segmentation": inputs.get("segmentation", {}),
            "targeting": inputs.get("targeting", {}),
            "positioning": inputs.get("positioning", {}),
            "blue_ocean": inputs.get("blue_ocean", {}),
            "competitive_strategy": inputs.get("competitive_strategy", {}),
            "value_proposition": inputs.get("value_proposition", {}),
            "required_fields_for_part3": [
                "segmentation.entry_segment_id",
                "targeting.icp",
                "positioning.positioning_statement",
                "positioning.reason_to_believe_assets",
                "blue_ocean.factors_buyer_side",
                "blue_ocean.eliminate",
                "blue_ocean.create",
                "value_proposition.main_statement",
                "value_proposition.products_services",
            ],
        }
    }
    return handoff


def main():
    parser = argparse.ArgumentParser(description="Construir handoff_part2.yaml")
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
    print(f"handoff_part2.yaml generado en {args.output}")


if __name__ == "__main__":
    main()
