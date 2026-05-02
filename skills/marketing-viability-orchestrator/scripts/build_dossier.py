#!/usr/bin/env python3
"""
build_dossier.py
Consolida los outputs de las cuatro partes en un dossier unificado (Markdown + PDF).

Uso:
    python build_dossier.py --workspace <path> --output-md <path> --output-pdf <path>

Estructura esperada del workspace:
    workspace/
      part1/part1_output.md
      part1/handoff_part1.yaml
      part1/charts/
      part2/part2_output.md
      part2/handoff_part2.yaml
      part2/charts/
      part3/part3_output.md
      part3/handoff_part3.yaml
      part3/charts/
      part4/part4_output.md
      part4/handoff_part4.yaml
      part4/charts/
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime

try:
    import yaml
except ImportError:
    sys.stderr.write("Falta el paquete 'pyyaml'. Instalar con: pip install pyyaml\n")
    sys.exit(2)


def read_text(path: Path) -> str:
    if not path.exists():
        return f"\n_[Archivo no encontrado: {path}]_\n"
    return path.read_text(encoding="utf-8")


def read_yaml(path: Path) -> dict:
    if not path.exists():
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def build_executive_summary(handoffs: dict) -> str:
    """Sintetiza un resumen ejecutivo cross-partes a partir de los handoffs."""
    h1 = handoffs.get("part1", {}).get("handoff_part1", {})
    h2 = handoffs.get("part2", {}).get("handoff_part2", {})
    h3 = handoffs.get("part3", {}).get("handoff_part3", {})
    h4 = handoffs.get("part4", {}).get("handoff_part4", {})

    case_name = h1.get("case_name", "Caso sin nombre")
    geography = h1.get("business_definition", {}).get("geography", "—")
    horizon = h1.get("business_definition", {}).get("horizon_years", "—")

    sam = h1.get("market_sizing", {}).get("sam", {})
    som = h1.get("market_sizing", {}).get("som", {})
    sam_value = sam.get("value_currency", {})
    som_value = som.get("value_currency", {})

    entry_segment = h2.get("segmentation", {}).get("entry_segment_id", "—")
    positioning = h2.get("positioning", {}).get("positioning_statement", "—")
    tagline = h2.get("positioning", {}).get("tagline", "—")

    cac = h3.get("channels_plan", {}).get("cac_blended", {})
    breakeven = h4.get("viability_indicators", {}).get("breakeven_volume", "—")
    npv = h4.get("viability_indicators", {}).get("npv", {})
    irr = h4.get("viability_indicators", {}).get("irr", {})
    payback = h4.get("viability_indicators", {}).get("payback_simple_months", {})
    verdict = h4.get("final_verdict", {}).get("veredict", "—")
    capital_needed = h4.get("final_verdict", {}).get("capital_needed_total", "—")

    summary = f"""# Resumen Ejecutivo

**Caso:** {case_name}
**Geografía:** {geography}
**Horizonte:** {horizon} años
**Fecha de cierre del análisis:** {datetime.now().strftime('%Y-%m-%d')}

## Oportunidad de mercado
SAM estimado entre {sam_value.get('min', '—')} y {sam_value.get('max', '—')} {sam_value.get('currency', '')} anuales. SOM realizable entre {som_value.get('min', '—')} y {som_value.get('max', '—')} {som_value.get('currency', '')} anuales en estado estable.

## Decisión estratégica
Segmento de entrada: **{entry_segment}**.

Posicionamiento declarado:
> {positioning}

Tagline operativo: *{tagline}*.

## Inputs operativos al modelo financiero
CAC blended año 1: {cac.get('year_1', '—')} {cac.get('currency', '')}.
Punto de equilibrio: {breakeven} unidades.

## Veredicto financiero
VAN base: {npv.get('base', '—')} {npv.get('currency', '')}.
TIR base: {irr.get('base', '—')}%.
Payback simple: {payback.get('base', '—')} meses.
**Veredicto:** {verdict}.
Capital total necesario estimado: {capital_needed} {npv.get('currency', '')}.

---
"""
    return summary


def build_traceability_appendix(handoffs: dict) -> str:
    """Construye el anexo de trazabilidad cross-partes."""
    out = ["# Anexo A — Trazabilidad cross-partes\n"]
    out.append("Cada decisión de las partes posteriores se rastrea a su origen en partes anteriores. Esta tabla resume los enlaces principales.\n")
    out.append("| Decisión | Parte origen | Elemento origen |")
    out.append("|---|---|---|")

    h1 = handoffs.get("part1", {}).get("handoff_part1", {})
    h2 = handoffs.get("part2", {}).get("handoff_part2", {})

    entry_seg = h2.get("segmentation", {}).get("entry_segment_id", "—")
    out.append(f"| Segmento de entrada ({entry_seg}) | Parte 1 | preliminary_segments |")

    positioning = h2.get("positioning", {}).get("positioning_statement", "—")[:80] + "..."
    out.append(f"| Posicionamiento | Parte 1 | job_statement + outcomes_prioritized |")

    out.append(f"| Curva de ingresos | Parte 3 | tariff_by_line × volumen capacity_plan |")
    out.append(f"| Estructura de costos variables | Parte 3 | unit_cost_structure |")
    out.append(f"| CAPEX inicial | Parte 3 | capacity_plan + launch_campaign budget |")
    out.append(f"| Hipótesis críticas | Partes 1, 2, 3 | willingness_to_pay, reason_to_believe, capacity |")

    out.append("\n")
    return "\n".join(out)


def build_handoffs_appendix(handoffs: dict) -> str:
    """Anexo con los cuatro YAMLs de handoff serializados."""
    out = ["# Anexo B — Handoffs YAML del pipeline\n"]
    for part_id in ("part1", "part2", "part3", "part4"):
        out.append(f"## {part_id}\n")
        out.append("```yaml")
        out.append(yaml.dump(handoffs.get(part_id, {}), allow_unicode=True, sort_keys=False))
        out.append("```\n")
    return "\n".join(out)


def build_dossier_md(workspace: Path) -> str:
    handoffs = {
        "part1": read_yaml(workspace / "part1" / "handoff_part1.yaml"),
        "part2": read_yaml(workspace / "part2" / "handoff_part2.yaml"),
        "part3": read_yaml(workspace / "part3" / "handoff_part3.yaml"),
        "part4": read_yaml(workspace / "part4" / "handoff_part4.yaml"),
    }

    parts_md = {
        "part1": read_text(workspace / "part1" / "part1_output.md"),
        "part2": read_text(workspace / "part2" / "part2_output.md"),
        "part3": read_text(workspace / "part3" / "part3_output.md"),
        "part4": read_text(workspace / "part4" / "part4_output.md"),
    }

    summary = build_executive_summary(handoffs)
    traceability = build_traceability_appendix(handoffs)
    handoffs_appendix = build_handoffs_appendix(handoffs)

    toc = """# Índice

1. Resumen ejecutivo
2. Parte 1 — Diagnóstico de mercado
3. Parte 2 — Marketing estratégico
4. Parte 3 — Marketing operativo aterrizado en acciones
5. Parte 4 — Análisis financiero de viabilidad
6. Anexo A — Trazabilidad cross-partes
7. Anexo B — Handoffs YAML del pipeline

---
"""

    body = "\n\n---\n\n".join([
        summary,
        toc,
        "# Parte 1 — Diagnóstico de mercado\n\n" + parts_md["part1"],
        "# Parte 2 — Marketing estratégico\n\n" + parts_md["part2"],
        "# Parte 3 — Marketing operativo aterrizado en acciones\n\n" + parts_md["part3"],
        "# Parte 4 — Análisis financiero de viabilidad\n\n" + parts_md["part4"],
        traceability,
        handoffs_appendix,
    ])

    return body


def md_to_pdf(md_path: Path, pdf_path: Path) -> None:
    """Convertir markdown a PDF usando markdown + weasyprint, o pandoc como fallback."""
    try:
        import markdown
        from weasyprint import HTML, CSS
        md_text = md_path.read_text(encoding="utf-8")
        html_body = markdown.markdown(md_text, extensions=["tables", "fenced_code", "toc"])
        css = CSS(string="""
            @page { size: A4; margin: 2cm; }
            body { font-family: 'Helvetica', 'Arial', sans-serif; font-size: 10pt; line-height: 1.45; color: #1a1a1a; }
            h1 { font-size: 18pt; color: #0b3a6e; border-bottom: 2px solid #0b3a6e; padding-bottom: 4pt; margin-top: 18pt; }
            h2 { font-size: 14pt; color: #0b3a6e; margin-top: 14pt; }
            h3 { font-size: 12pt; margin-top: 10pt; }
            table { border-collapse: collapse; width: 100%; font-size: 9pt; margin: 8pt 0; }
            th, td { border: 1px solid #cfcfcf; padding: 4pt 6pt; text-align: left; vertical-align: top; }
            th { background-color: #eef2f7; }
            code { background-color: #f4f4f4; padding: 1pt 3pt; font-size: 9pt; }
            pre { background-color: #f4f4f4; padding: 8pt; font-size: 8.5pt; white-space: pre-wrap; }
            blockquote { border-left: 3px solid #0b3a6e; padding-left: 10pt; color: #444; }
        """)
        full_html = f"<html><head><meta charset='utf-8'></head><body>{html_body}</body></html>"
        HTML(string=full_html, base_url=str(md_path.parent)).write_pdf(str(pdf_path), stylesheets=[css])
        print(f"PDF generado: {pdf_path}")
    except ImportError:
        # Fallback a pandoc
        import subprocess
        try:
            subprocess.run(
                ["pandoc", str(md_path), "-o", str(pdf_path), "--pdf-engine=xelatex"],
                check=True
            )
            print(f"PDF generado con pandoc: {pdf_path}")
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            print(f"No se pudo generar PDF (instalar weasyprint o pandoc). Detalle: {e}", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(description="Construir el dossier consolidado de viabilidad.")
    parser.add_argument("--workspace", required=True, type=Path)
    parser.add_argument("--output-md", required=True, type=Path)
    parser.add_argument("--output-pdf", required=True, type=Path)
    args = parser.parse_args()

    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_pdf.parent.mkdir(parents=True, exist_ok=True)

    md = build_dossier_md(args.workspace)
    args.output_md.write_text(md, encoding="utf-8")
    print(f"Markdown generado: {args.output_md}")

    md_to_pdf(args.output_md, args.output_pdf)


if __name__ == "__main__":
    main()
