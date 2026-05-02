#!/usr/bin/env python3
"""
build_handoff_part1.py
Construye el handoff_part1.yaml a partir de un archivo de inputs estructurados producido durante el análisis.

Uso:
    python build_handoff_part1.py --inputs handoff_inputs.yaml --output handoff_part1.yaml

El archivo handoff_inputs.yaml es producido por Claude durante el análisis de la Parte 1 con los datos clave.
Este script lo valida, completa con valores por defecto razonables, y emite el YAML final.
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
    """Construir el handoff_part1.yaml con la estructura canónica."""
    handoff = {
        "handoff_part1": {
            "version": "1.0",
            "case_name": inputs.get("case_name", "Caso sin nombre"),
            "date": inputs.get("date", datetime.now().strftime("%Y-%m-%d")),
            "evidence_level": inputs.get("evidence_level", "modeled"),
            "business_definition": inputs.get("business_definition", {}),
            "market_sizing": inputs.get("market_sizing", {}),
            "market_dynamics": inputs.get("market_dynamics", {}),
            "competitive_landscape": inputs.get("competitive_landscape", {}),
            "customer_understanding": inputs.get("customer_understanding", {}),
            "preliminary_segments": inputs.get("preliminary_segments", []),
            "diagnosis_synthesis": inputs.get("diagnosis_synthesis", {}),
            "required_fields_for_part2": [
                "business_definition",
                "market_sizing.sam",
                "market_sizing.som",
                "customer_understanding.job_statement",
                "customer_understanding.jobs_functional",
                "customer_understanding.four_forces",
                "customer_understanding.outcomes_prioritized",
                "customer_understanding.willingness_to_pay_declared",
                "preliminary_segments",
                "competitive_landscape.price_benchmark",
            ],
        }
    }
    return handoff


def main():
    parser = argparse.ArgumentParser(description="Construir handoff_part1.yaml")
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
    print(f"handoff_part1.yaml generado en {args.output}")


if __name__ == "__main__":
    main()
