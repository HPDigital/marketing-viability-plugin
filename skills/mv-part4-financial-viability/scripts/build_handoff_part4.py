#!/usr/bin/env python3
"""
build_handoff_part4.py
Construye el handoff_part4.yaml — output final del pipeline.
"""

import argparse
import sys
from datetime import datetime
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.stderr.write("Falta pyyaml.\n")
    sys.exit(2)


def build(inputs: dict) -> dict:
    handoff = {
        "handoff_part4": {
            "version": "1.0",
            "case_name": inputs.get("case_name", "Caso sin nombre"),
            "date": inputs.get("date", datetime.now().strftime("%Y-%m-%d")),
            "source_handoffs": ["handoff_part1.yaml", "handoff_part2.yaml", "handoff_part3.yaml"],
            "financial_model": inputs.get("financial_model", {}),
            "revenue_projection": inputs.get("revenue_projection", {}),
            "cost_structure": inputs.get("cost_structure", {}),
            "capex_plan": inputs.get("capex_plan", {}),
            "cash_flow": inputs.get("cash_flow", {}),
            "viability_indicators": inputs.get("viability_indicators", {}),
            "unit_economics": inputs.get("unit_economics", {}),
            "sensitivity_analysis": inputs.get("sensitivity_analysis", {}),
            "risk_analysis": inputs.get("risk_analysis", {}),
            "validation_program": inputs.get("validation_program", {}),
            "final_verdict": inputs.get("final_verdict", {}),
        }
    }
    return handoff


def main():
    parser = argparse.ArgumentParser(description="Construir handoff_part4.yaml")
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
    print(f"handoff_part4.yaml generado en {args.output}")


if __name__ == "__main__":
    main()
