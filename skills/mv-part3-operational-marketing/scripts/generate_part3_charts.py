#!/usr/bin/env python3
"""
generate_part3_charts.py
Genera los gráficos canónicos del Marketing Operativo (Parte 3).

Estructura del chart_inputs.yaml:

funnel_by_channel:
  - {channel: "Prescriptor médico", stages: [
      {name: "Referencia recibida", low: 100, high: 100},
      {name: "Cita inicial", low: 60, high: 80},
      {name: "Evaluación clínica", low: 45, high: 65},
      {name: "Cotización aceptada", low: 25, high: 40},
      {name: "Contrato firmado", low: 15, high: 28}]}
  - {channel: "B2B clínicas", stages: [...]}

cac_by_channel:
  - {channel: "Prescriptor médico", cac: 450, currency: "USD"}
  - {channel: "B2B clínicas", cac: 1200, currency: "USD"}
  - {channel: "Digital orgánico", cac: 250, currency: "USD"}
  - {channel: "Alianzas financieras", cac: 350, currency: "USD"}
cac_blended:
  year_1: 750
  year_2: 600
  year_3_5: 500

capacity_vs_som:
  capacity_phase_1:
    big_hire: {min: 80, max: 150}
    little_hire: {min: 200, max: 400}
    b2b_active: {min: 8, max: 15}
  som_target_year_1:
    big_hire: 60
    little_hire: 150
    b2b_active: 6

capacity_jumps:
  - {year: 1, capacity_big_hire: 100, capex: 0, milestone: "Inicio operación"}
  - {year: 2, capacity_big_hire: 100, capex: 0, milestone: "Año estable"}
  - {year: 3, capacity_big_hire: 200, capex: 80000, milestone: "+ Segundo técnico"}
  - {year: 4, capacity_big_hire: 350, capex: 120000, milestone: "+ Segundo taller"}
  - {year: 5, capacity_big_hire: 500, capex: 90000, milestone: "+ Tercer técnico"}

tariff_by_line:
  - {line: "Big Hire P1", segment: "P1", low: 6000, mid: 9000, high: 12000, currency: "USD"}
  - {line: "Big Hire P2", segment: "P2", low: 4000, mid: 6000, high: 8000, currency: "USD"}
  - {line: "Little Hire mensual", segment: "P1+P2", low: 80, mid: 120, high: 180, currency: "USD"}
  - {line: "Contrato B2B anual", segment: "P3", low: 15000, mid: 22000, high: 35000, currency: "USD"}

operational_calendar_year_1:
  - {month: 1, milestones: ["Constitución legal", "AGEMED inicio expediente"]}
  - {month: 2, milestones: ["Taller listo", "Contratación técnico ortoprotesista"]}
  - {month: 3, milestones: ["Lanzamiento web", "Acuerdo con 2 prescriptores"]}
  - {month: 4, milestones: ["Primer Big Hire entregado"]}
  - {month: 5, milestones: ["Campaña 90 días lanzamiento"]}
  - {month: 6, milestones: ["Primer contrato B2B firmado"]}
  - {month: 7, milestones: ["AGEMED 1er dispositivo registrado"]}
  - {month: 8, milestones: ["Revisión de pricing y descuentos"]}
  - {month: 9, milestones: ["Ampliación red prescriptora"]}
  - {month: 10, milestones: ["Cohorte 1 a 6 meses post-entrega"]}
  - {month: 11, milestones: ["Validación H-1 cierre"]}
  - {month: 12, milestones: ["Cierre año 1, planificación año 2"]}

unit_cost_structure:
  - {line: "Big Hire P1", components: {component: 3500, labor: 800, materials: 200, financial: 150, service: 350}}
  - {line: "Big Hire P2", components: {component: 2200, labor: 600, materials: 150, financial: 100, service: 250}}
  - {line: "Little Hire mensual", components: {component: 0, labor: 35, materials: 8, financial: 0, service: 25}}

journey_channel_map:
  phases: ["Awareness", "Evaluation", "Purchase", "Delivery", "After-sales"]
  channels:
    - {channel: "Prescriptor médico", priority_by_phase: ["primary", "primary", "secondary", "support", "support"]}
    - {channel: "B2B clínicas", priority_by_phase: ["secondary", "primary", "primary", "primary", "secondary"]}
    - {channel: "Digital", priority_by_phase: ["primary", "secondary", "support", "no", "secondary"]}
    - {channel: "Alianzas financieras", priority_by_phase: ["no", "secondary", "primary", "no", "no"]}
"""

import argparse
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.stderr.write("Falta pyyaml.\n")
    sys.exit(2)

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np
except ImportError:
    sys.stderr.write("Falta matplotlib/numpy.\n")
    sys.exit(2)

COLORS = {
    "primary": "#0b3a6e",
    "secondary": "#5b9bd5",
    "accent": "#c0504d",
    "neutral": "#7f7f7f",
    "highlight": "#e09f3e",
    "ok": "#6a994e",
}

DPI = 300
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.size": 9,
    "axes.titlesize": 11,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "figure.facecolor": "white",
})


def chart_funnel_by_channel(data, output_dir):
    if "funnel_by_channel" not in data:
        return
    items = data["funnel_by_channel"]
    n_channels = len(items)
    fig, axes = plt.subplots(1, n_channels, figsize=(5 * n_channels, 5.5), squeeze=False)
    axes = axes[0]
    for ax, ch in zip(axes, items):
        stages = ch["stages"]
        names = [s["name"] for s in stages]
        lows = [s["low"] for s in stages]
        highs = [s["high"] for s in stages]
        y = np.arange(len(stages))[::-1]
        for i, (lo, hi, n) in enumerate(zip(lows, highs, names)):
            mid = (lo + hi) / 2
            ax.barh(y[i], hi, color=COLORS["secondary"], alpha=0.45, edgecolor="white")
            ax.barh(y[i], lo, color=COLORS["primary"], alpha=0.85, edgecolor="white")
            ax.text(hi + 2, y[i], f"{lo}-{hi}", va="center", fontsize=8.5)
        ax.set_yticks(y)
        ax.set_yticklabels(names, fontsize=8.5)
        ax.set_xlabel("Volumen relativo")
        ax.set_title(ch["channel"], fontsize=10)
        ax.grid(True, alpha=0.25, axis="x", linestyle="--")
    fig.suptitle("Embudo de conversión por canal (rango low-high)", fontsize=12, y=1.02)
    fig.tight_layout()
    fig.savefig(output_dir / "chart_p3_01_funnel.png", dpi=DPI, bbox_inches="tight")
    plt.close(fig)


def chart_cac_by_channel(data, output_dir):
    if "cac_by_channel" not in data:
        return
    items = data["cac_by_channel"]
    blended = data.get("cac_blended", {})
    channels = [it["channel"] for it in items]
    cacs = [it["cac"] for it in items]
    currency = items[0].get("currency", "USD")

    fig, ax = plt.subplots(figsize=(9, 0.7 * len(channels) + 2))
    bars = ax.barh(channels, cacs, color=COLORS["secondary"], edgecolor="white", linewidth=1.2)
    if "year_1" in blended:
        ax.axvline(x=blended["year_1"], color=COLORS["accent"], linestyle="--", linewidth=2,
                   label=f"CAC blended año 1: {blended['year_1']} {currency}")
    if "year_3_5" in blended:
        ax.axvline(x=blended["year_3_5"], color=COLORS["ok"], linestyle="--", linewidth=2,
                   label=f"CAC blended años 3-5: {blended['year_3_5']} {currency}")
    for bar, cac in zip(bars, cacs):
        ax.text(bar.get_width() + 20, bar.get_y() + bar.get_height() / 2,
                f"{cac} {currency}", va="center", fontsize=9)
    ax.set_xlabel(f"CAC ({currency})")
    ax.set_title("Coste de adquisición por canal y CAC blended")
    ax.grid(True, alpha=0.25, axis="x", linestyle="--")
    ax.legend(loc="lower right", framealpha=0.95)
    fig.tight_layout()
    fig.savefig(output_dir / "chart_p3_02_cac.png", dpi=DPI, bbox_inches="tight")
    plt.close(fig)


def chart_capacity_vs_som(data, output_dir):
    if "capacity_vs_som" not in data:
        return
    d = data["capacity_vs_som"]
    cap = d["capacity_phase_1"]
    som = d["som_target_year_1"]
    units = list(cap.keys())
    cap_min = [cap[u]["min"] for u in units]
    cap_max = [cap[u]["max"] for u in units]
    cap_mid = [(a + b) / 2 for a, b in zip(cap_min, cap_max)]
    som_vals = [som[u] for u in units]

    fig, ax = plt.subplots(figsize=(9, 5))
    x = np.arange(len(units))
    width = 0.35
    ax.bar(x - width / 2, cap_mid, width, yerr=[[m - mn for m, mn in zip(cap_mid, cap_min)],
                                                  [mx - m for m, mx in zip(cap_mid, cap_max)]],
           capsize=6, color=COLORS["primary"], label="Capacidad fase 1", edgecolor="white", linewidth=1.2)
    ax.bar(x + width / 2, som_vals, width, color=COLORS["accent"], label="SOM objetivo año 1",
           edgecolor="white", linewidth=1.2)
    ax.set_xticks(x)
    ax.set_xticklabels([u.replace("_", " ").title() for u in units])
    ax.set_ylabel("Volumen anual")
    ax.set_title("Capacidad operativa fase 1 vs SOM objetivo año 1")
    ax.grid(True, alpha=0.25, axis="y", linestyle="--")
    ax.legend(loc="upper right", framealpha=0.95)
    fig.tight_layout()
    fig.savefig(output_dir / "chart_p3_03_capacity_vs_som.png", dpi=DPI, bbox_inches="tight")
    plt.close(fig)


def chart_capacity_jumps(data, output_dir):
    if "capacity_jumps" not in data:
        return
    items = data["capacity_jumps"]
    years = [it["year"] for it in items]
    cap = [it["capacity_big_hire"] for it in items]
    capex = [it["capex"] for it in items]

    fig, ax1 = plt.subplots(figsize=(10, 5.5))
    ax1.step(years, cap, where="post", color=COLORS["primary"], linewidth=3, marker="o", markersize=10)
    ax1.set_xlabel("Año")
    ax1.set_ylabel("Capacidad anual Big Hire", color=COLORS["primary"])
    ax1.tick_params(axis="y", labelcolor=COLORS["primary"])
    ax1.grid(True, alpha=0.25, linestyle="--")

    for it in items:
        if it["capex"] > 0:
            ax1.annotate(f'{it["milestone"]}\n+CAPEX {it["capex"]:,}',
                         xy=(it["year"], it["capacity_big_hire"]),
                         xytext=(0, 25), textcoords="offset points",
                         ha="center", fontsize=8.5,
                         bbox=dict(boxstyle="round,pad=0.3", facecolor="#fff5e6",
                                   edgecolor=COLORS["highlight"]))

    ax2 = ax1.twinx()
    ax2.bar(years, capex, color=COLORS["accent"], alpha=0.35, edgecolor="white", width=0.5)
    ax2.set_ylabel("CAPEX incremental (USD)", color=COLORS["accent"])
    ax2.tick_params(axis="y", labelcolor=COLORS["accent"])
    ax2.spines["top"].set_visible(False)

    ax1.set_title("Saltos de capacidad no lineales y CAPEX asociado")
    ax1.set_xticks(years)
    fig.tight_layout()
    fig.savefig(output_dir / "chart_p3_04_capacity_jumps.png", dpi=DPI, bbox_inches="tight")
    plt.close(fig)


def chart_tariff_by_line(data, output_dir):
    if "tariff_by_line" not in data:
        return
    items = data["tariff_by_line"]
    fig, ax = plt.subplots(figsize=(10, 0.7 * len(items) + 2))
    y = np.arange(len(items))
    for i, it in enumerate(items):
        ax.plot([it["low"], it["high"]], [i, i], linewidth=10, color=COLORS["secondary"],
                alpha=0.6, solid_capstyle="round")
        ax.plot(it["mid"], i, "o", color="white", markersize=10,
                markeredgecolor=COLORS["primary"], markeredgewidth=2.5)
        ax.text(it["high"] * 1.02, i, f"{it['low']:,}-{it['high']:,} {it['currency']}",
                va="center", fontsize=9)
    labels = [f"{it['line']} ({it['segment']})" for it in items]
    ax.set_yticks(y)
    ax.set_yticklabels(labels)
    ax.set_xlabel("Precio")
    ax.set_title("Tarifario por línea y por segmento (rango low-high, mid resaltado)")
    ax.grid(True, alpha=0.25, axis="x", linestyle="--")
    fig.tight_layout()
    fig.savefig(output_dir / "chart_p3_05_tariff.png", dpi=DPI, bbox_inches="tight")
    plt.close(fig)


def chart_operational_calendar(data, output_dir):
    if "operational_calendar_year_1" not in data:
        return
    items = data["operational_calendar_year_1"]
    fig, ax = plt.subplots(figsize=(13, 0.6 * len(items) + 2))
    months = [it["month"] for it in items]
    for i, it in enumerate(reversed(items)):
        for milestone in it["milestones"]:
            ax.barh(i, 0.8, left=it["month"] - 0.4, color=COLORS["primary"], alpha=0.7,
                    edgecolor="white")
            ax.text(it["month"], i, milestone, ha="center", va="center", fontsize=7.5,
                    color="white", wrap=True)
    ax.set_yticks(range(len(items)))
    ax.set_yticklabels([f"M{m}" for m in reversed(months)])
    ax.set_xticks(range(1, 13))
    ax.set_xticklabels([f"Mes {m}" for m in range(1, 13)])
    ax.set_xlim(0.5, 12.5)
    ax.set_title("Calendario operativo año 1 (hitos mensuales)")
    fig.tight_layout()
    fig.savefig(output_dir / "chart_p3_06_calendar.png", dpi=DPI, bbox_inches="tight")
    plt.close(fig)


def chart_unit_cost_structure(data, output_dir):
    if "unit_cost_structure" not in data:
        return
    items = data["unit_cost_structure"]
    components_keys = ["component", "labor", "materials", "financial", "service"]
    components_labels = ["Componente importado", "Mano de obra", "Materiales", "Financiero", "Servicio incluido"]
    components_colors = [COLORS["primary"], COLORS["secondary"], COLORS["highlight"], COLORS["accent"], COLORS["ok"]]

    lines = [it["line"] for it in items]
    matrix = np.array([[it["components"].get(k, 0) for k in components_keys] for it in items])

    fig, ax = plt.subplots(figsize=(10, 0.7 * len(lines) + 2))
    bottom = np.zeros(len(lines))
    y = np.arange(len(lines))
    for j, (label, color) in enumerate(zip(components_labels, components_colors)):
        vals = matrix[:, j]
        ax.barh(y, vals, left=bottom, color=color, edgecolor="white", linewidth=1.2, label=label)
        bottom += vals
    ax.set_yticks(y)
    ax.set_yticklabels(lines)
    ax.set_xlabel("Costo unitario (USD)")
    ax.set_title("Estructura de costo unitario por línea de ingreso")
    ax.grid(True, alpha=0.25, axis="x", linestyle="--")
    ax.legend(loc="lower right", framealpha=0.95, fontsize=8.5)
    for i, total in enumerate(bottom):
        ax.text(total * 1.02, i, f"{int(total):,}", va="center", fontsize=9, fontweight="bold")
    fig.tight_layout()
    fig.savefig(output_dir / "chart_p3_07_unit_cost.png", dpi=DPI, bbox_inches="tight")
    plt.close(fig)


def chart_journey_channel_map(data, output_dir):
    if "journey_channel_map" not in data:
        return
    d = data["journey_channel_map"]
    phases = d["phases"]
    channels = d["channels"]
    priority_color = {
        "primary": COLORS["primary"],
        "secondary": COLORS["secondary"],
        "support": "#cfd9e3",
        "no": "#ffffff",
    }
    priority_label = {"primary": "Primario", "secondary": "Secundario", "support": "Soporte", "no": "—"}

    fig, ax = plt.subplots(figsize=(11, 0.7 * len(channels) + 2.5))
    for i, ch in enumerate(reversed(channels)):
        for j, prio in enumerate(ch["priority_by_phase"]):
            color = priority_color.get(prio, "#ffffff")
            ax.barh(i, 1, left=j - 0.4, color=color, edgecolor=COLORS["neutral"], linewidth=0.6)
            text_color = "white" if prio == "primary" else COLORS["primary"]
            ax.text(j, i, priority_label[prio], ha="center", va="center", fontsize=8, color=text_color)
    ax.set_yticks(range(len(channels)))
    ax.set_yticklabels([ch["channel"] for ch in reversed(channels)])
    ax.set_xticks(range(len(phases)))
    ax.set_xticklabels(phases)
    ax.set_xlim(-0.5, len(phases) - 0.5)
    ax.set_title("Mapa de canales por fase del journey del cliente")
    fig.tight_layout()
    fig.savefig(output_dir / "chart_p3_08_journey_channels.png", dpi=DPI, bbox_inches="tight")
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--inputs", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    with open(args.inputs, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}

    chart_funnel_by_channel(data, args.output_dir)
    chart_cac_by_channel(data, args.output_dir)
    chart_capacity_vs_som(data, args.output_dir)
    chart_capacity_jumps(data, args.output_dir)
    chart_tariff_by_line(data, args.output_dir)
    chart_operational_calendar(data, args.output_dir)
    chart_unit_cost_structure(data, args.output_dir)
    chart_journey_channel_map(data, args.output_dir)

    print(f"Gráficos de Parte 3 generados en {args.output_dir}")


if __name__ == "__main__":
    main()
