#!/usr/bin/env python3
"""
generate_part4_charts.py
Genera los gráficos canónicos del Análisis Financiero (Parte 4).

Estructura del chart_inputs.yaml:

revenue_by_scenario:
  years: [1, 2, 3, 4, 5]
  base: [350000, 850000, 1500000, 2400000, 3200000]
  pessimistic: [180000, 460000, 880000, 1450000, 1950000]
  optimistic: [490000, 1180000, 2050000, 3250000, 4350000]
  currency: "USD"

ebitda_by_scenario:
  base: [-220000, -80000, 180000, 480000, 780000]
  pessimistic: [-310000, -250000, -100000, 80000, 250000]
  optimistic: [-150000, 50000, 380000, 820000, 1280000]

free_cash_flow:
  years_periods: [1, 2, 3, 4, 5]
  fcf: [-450000, -140000, 80000, 350000, 620000]
  cumulative: [-450000, -590000, -510000, -160000, 460000]
  inflection_period: 4

tornado_sensitivity:
  base_npv: 480000
  variables:
    - {name: "Tasa de conversión", impact_minus_20: -380000, impact_plus_20: 380000}
    - {name: "Precio Big Hire P1", impact_minus_20: -290000, impact_plus_20: 290000}
    - {name: "CAC blended", impact_minus_20: 220000, impact_plus_20: -220000}
    - {name: "Costo unitario componente", impact_minus_20: 210000, impact_plus_20: -210000}
    - {name: "Capacidad técnico", impact_minus_20: -180000, impact_plus_20: 180000}
    - {name: "Tasa de retención Little Hire", impact_minus_20: -120000, impact_plus_20: 120000}

breakeven:
  monthly_units: 9
  monthly_revenue: 65000
  monthly_fixed_costs: 28000
  monthly_contribution_per_unit: 4100
  breakeven_month: 14
  currency: "USD"

scenarios_summary:
  scenarios: ["Pesimista", "Base", "Optimista"]
  npv: [-180000, 480000, 1450000]
  irr: [4, 22, 41]
  payback_months: [60, 30, 22]

unit_economics:
  cac: 750
  ltv: 4800
  ratio: 6.4
  payback_cac_months: 8

risk_matrix:
  - {risk: "AGEMED retraso 6m+", category: "regulatorio", probability: 3, impact: 4}
  - {risk: "Demanda menor a SOM modelado", category: "mercado", probability: 3, impact: 5}
  - {risk: "Partnership europeo no se concreta", category: "partnership", probability: 2, impact: 5}
  - {risk: "Salida del técnico ortoprotesista", category: "operativo", probability: 2, impact: 4}
  - {risk: "Tipo de cambio +20%", category: "financiero", probability: 3, impact: 3}
  - {risk: "Mora pacientes financiados", category: "financiero", probability: 3, impact: 3}
  - {risk: "Competidor copia servicio integrado", category: "mercado", probability: 2, impact: 3}

validation_program:
  hypotheses:
    - {id: "H-1", name: "Disposición a pagar P1", quarter: 1, budget: 18000, threshold: ">=70% pacientes ratifican rango"}
    - {id: "H-2", name: "Factibilidad SLA técnico", quarter: 2, budget: 12000, threshold: "Tiempo respuesta <72h en 90% casos"}
    - {id: "H-3", name: "Densidad prescriptora", quarter: 1, budget: 8000, threshold: ">=3 prescriptores activos por ciudad"}
    - {id: "H-4", name: "Partnership europeo", quarter: 2, budget: 25000, threshold: "Carta de intención firmada"}
    - {id: "H-5", name: "Conversión B2B clínicas", quarter: 3, budget: 15000, threshold: ">=2 contratos firmados de pilotos"}
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
    "pessimistic": "#8b2c2c",
    "base": "#0b3a6e",
    "optimistic": "#6a994e",
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


def chart_revenue_by_scenario(data, output_dir):
    if "revenue_by_scenario" not in data:
        return
    d = data["revenue_by_scenario"]
    years = d["years"]
    fig, ax = plt.subplots(figsize=(10, 5.5))
    ax.fill_between(years, d["pessimistic"], d["optimistic"], color=COLORS["secondary"], alpha=0.18, label="Rango pes.-opt.")
    ax.plot(years, d["pessimistic"], marker="v", color=COLORS["pessimistic"], linewidth=2, label="Pesimista")
    ax.plot(years, d["base"], marker="o", color=COLORS["base"], linewidth=2.8, label="Base")
    ax.plot(years, d["optimistic"], marker="^", color=COLORS["optimistic"], linewidth=2, label="Optimista")
    ax.set_xlabel("Año")
    ax.set_ylabel(f"Ingresos ({d.get('currency', 'USD')})")
    ax.set_title("Proyección de ingresos por escenario")
    ax.set_xticks(years)
    ax.grid(True, alpha=0.25, linestyle="--")
    ax.legend(loc="upper left", framealpha=0.95)
    fig.tight_layout()
    fig.savefig(output_dir / "chart_p4_01_revenue.png", dpi=DPI, bbox_inches="tight")
    plt.close(fig)


def chart_ebitda_by_scenario(data, output_dir):
    if "ebitda_by_scenario" not in data:
        return
    d = data["ebitda_by_scenario"]
    rev = data.get("revenue_by_scenario", {})
    years = rev.get("years", list(range(1, len(d["base"]) + 1)))
    fig, ax = plt.subplots(figsize=(10, 5.5))
    ax.axhline(y=0, color="black", linewidth=0.8)
    ax.plot(years, d["pessimistic"], marker="v", color=COLORS["pessimistic"], linewidth=2, label="Pesimista")
    ax.plot(years, d["base"], marker="o", color=COLORS["base"], linewidth=2.8, label="Base")
    ax.plot(years, d["optimistic"], marker="^", color=COLORS["optimistic"], linewidth=2, label="Optimista")
    ax.set_xlabel("Año")
    ax.set_ylabel(f"EBITDA ({rev.get('currency', 'USD')})")
    ax.set_title("Proyección de EBITDA por escenario")
    ax.set_xticks(years)
    ax.grid(True, alpha=0.25, linestyle="--")
    ax.legend(loc="lower right", framealpha=0.95)
    fig.tight_layout()
    fig.savefig(output_dir / "chart_p4_02_ebitda.png", dpi=DPI, bbox_inches="tight")
    plt.close(fig)


def chart_free_cash_flow(data, output_dir):
    if "free_cash_flow" not in data:
        return
    d = data["free_cash_flow"]
    periods = d["years_periods"]
    fig, ax1 = plt.subplots(figsize=(11, 5.5))
    colors = [COLORS["pessimistic"] if v < 0 else COLORS["ok"] for v in d["fcf"]]
    ax1.bar(periods, d["fcf"], color=colors, alpha=0.7, edgecolor="white", label="FCF anual")
    ax1.axhline(y=0, color="black", linewidth=0.8)
    ax1.set_xlabel("Año")
    ax1.set_ylabel("FCF anual (USD)", color=COLORS["primary"])
    ax1.tick_params(axis="y", labelcolor=COLORS["primary"])
    ax1.set_xticks(periods)
    ax1.grid(True, alpha=0.25, linestyle="--", axis="y")

    ax2 = ax1.twinx()
    cum_colors = [COLORS["accent"] if v < 0 else COLORS["primary"] for v in d["cumulative"]]
    ax2.plot(periods, d["cumulative"], marker="o", color=COLORS["primary"], linewidth=2.5, label="FCF acumulado")
    for p, v in zip(periods, d["cumulative"]):
        ax2.annotate(f"{v:,}", (p, v), xytext=(0, 8), textcoords="offset points",
                     ha="center", fontsize=8.5)
    ax2.set_ylabel("FCF acumulado (USD)", color=COLORS["accent"])
    ax2.tick_params(axis="y", labelcolor=COLORS["accent"])
    ax2.spines["top"].set_visible(False)

    if "inflection_period" in d:
        ax1.axvline(x=d["inflection_period"], color=COLORS["highlight"], linestyle="--", linewidth=2)
        ax1.text(d["inflection_period"], max(d["fcf"]) * 0.9,
                 f" Punto de inflexión\n año {d['inflection_period']}",
                 fontsize=9, color=COLORS["highlight"])

    ax1.set_title("Flujo de caja libre y FCF acumulado")
    fig.tight_layout()
    fig.savefig(output_dir / "chart_p4_03_fcf.png", dpi=DPI, bbox_inches="tight")
    plt.close(fig)


def chart_tornado(data, output_dir):
    if "tornado_sensitivity" not in data:
        return
    d = data["tornado_sensitivity"]
    base_npv = d["base_npv"]
    variables = d["variables"]
    variables = sorted(variables, key=lambda v: max(abs(v["impact_minus_20"]), abs(v["impact_plus_20"])), reverse=True)

    names = [v["name"] for v in variables]
    minus = [v["impact_minus_20"] for v in variables]
    plus = [v["impact_plus_20"] for v in variables]

    y = np.arange(len(names))[::-1]
    fig, ax = plt.subplots(figsize=(11, 0.6 * len(names) + 2))
    for i, (m, p) in enumerate(zip(minus, plus)):
        yi = y[i]
        ax.barh(yi, m, color=COLORS["pessimistic"], alpha=0.8, edgecolor="white", height=0.6)
        ax.barh(yi, p, color=COLORS["ok"], alpha=0.8, edgecolor="white", height=0.6)
        ax.text(m - 5000 if m < 0 else m + 5000, yi, f"{m:+,}", va="center",
                fontsize=8.5, ha="right" if m < 0 else "left", color=COLORS["pessimistic"])
        ax.text(p + 5000 if p > 0 else p - 5000, yi, f"{p:+,}", va="center",
                fontsize=8.5, ha="left" if p > 0 else "right", color=COLORS["ok"])
    ax.axvline(x=0, color="black", linewidth=1.2)
    ax.set_yticks(y)
    ax.set_yticklabels(names)
    ax.set_xlabel(f"Impacto en VAN (USD). VAN base = {base_npv:,}")
    ax.set_title("Tornado de sensibilidad sobre VAN (variación ±20%)")
    ax.grid(True, alpha=0.25, axis="x", linestyle="--")
    fig.tight_layout()
    fig.savefig(output_dir / "chart_p4_04_tornado.png", dpi=DPI, bbox_inches="tight")
    plt.close(fig)


def chart_breakeven(data, output_dir):
    if "breakeven" not in data:
        return
    d = data["breakeven"]
    units_range = list(range(0, max(d["monthly_units"] * 2 + 1, 20)))
    rev = [u * (d["monthly_revenue"] / max(d["monthly_units"], 1)) for u in units_range]
    cost = [d["monthly_fixed_costs"] + (d["monthly_revenue"] / max(d["monthly_units"], 1) - d["monthly_contribution_per_unit"]) * u for u in units_range]

    fig, ax = plt.subplots(figsize=(10, 5.5))
    ax.plot(units_range, rev, color=COLORS["primary"], linewidth=2.5, label="Ingresos")
    ax.plot(units_range, cost, color=COLORS["accent"], linewidth=2.5, label="Costos totales")
    ax.fill_between(units_range, rev, cost, where=[r >= c for r, c in zip(rev, cost)],
                    color=COLORS["ok"], alpha=0.15, label="Beneficio")
    ax.axvline(x=d["monthly_units"], color=COLORS["highlight"], linestyle="--", linewidth=2)
    ax.text(d["monthly_units"] + 0.3, max(rev) * 0.5,
            f"Punto de equilibrio:\n {d['monthly_units']} unidades\n mes {d.get('breakeven_month', '?')}",
            fontsize=9, color=COLORS["highlight"], fontweight="bold")
    ax.set_xlabel("Unidades vendidas por mes")
    ax.set_ylabel(f"Valor ({d.get('currency', 'USD')} mensual)")
    ax.set_title("Análisis del punto de equilibrio")
    ax.grid(True, alpha=0.25, linestyle="--")
    ax.legend(loc="upper left", framealpha=0.95)
    fig.tight_layout()
    fig.savefig(output_dir / "chart_p4_05_breakeven.png", dpi=DPI, bbox_inches="tight")
    plt.close(fig)


def chart_scenarios_summary(data, output_dir):
    if "scenarios_summary" not in data:
        return
    d = data["scenarios_summary"]
    scenarios = d["scenarios"]
    x = np.arange(len(scenarios))

    fig, axes = plt.subplots(1, 3, figsize=(13, 4.5))
    colors = [COLORS["pessimistic"], COLORS["base"], COLORS["optimistic"]]

    axes[0].bar(scenarios, d["npv"], color=colors, edgecolor="white", linewidth=1.4)
    axes[0].axhline(y=0, color="black", linewidth=0.8)
    axes[0].set_title("VAN")
    axes[0].set_ylabel("USD")
    axes[0].grid(True, alpha=0.25, axis="y", linestyle="--")
    for i, v in enumerate(d["npv"]):
        axes[0].text(i, v + (50000 if v >= 0 else -50000), f"{v:,}",
                     ha="center", fontsize=9, fontweight="bold")

    axes[1].bar(scenarios, d["irr"], color=colors, edgecolor="white", linewidth=1.4)
    axes[1].set_title("TIR")
    axes[1].set_ylabel("%")
    axes[1].grid(True, alpha=0.25, axis="y", linestyle="--")
    for i, v in enumerate(d["irr"]):
        axes[1].text(i, v + 1, f"{v}%", ha="center", fontsize=9, fontweight="bold")

    axes[2].bar(scenarios, d["payback_months"], color=colors, edgecolor="white", linewidth=1.4)
    axes[2].set_title("Payback (meses)")
    axes[2].set_ylabel("meses")
    axes[2].grid(True, alpha=0.25, axis="y", linestyle="--")
    for i, v in enumerate(d["payback_months"]):
        axes[2].text(i, v + 1, f"{v}m", ha="center", fontsize=9, fontweight="bold")

    fig.suptitle("Comparativa de los tres escenarios", fontsize=12, y=1.02)
    fig.tight_layout()
    fig.savefig(output_dir / "chart_p4_06_scenarios.png", dpi=DPI, bbox_inches="tight")
    plt.close(fig)


def chart_unit_economics(data, output_dir):
    if "unit_economics" not in data:
        return
    d = data["unit_economics"]
    fig, ax = plt.subplots(figsize=(8, 5))
    metrics = ["CAC", "LTV"]
    values = [d["cac"], d["ltv"]]
    bars = ax.bar(metrics, values, color=[COLORS["accent"], COLORS["ok"]],
                  edgecolor="white", linewidth=1.5, width=0.5)
    for bar, v in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, v + max(values) * 0.02,
                f"{v:,} USD", ha="center", fontsize=11, fontweight="bold")
    ax.set_ylabel("USD")
    ax.set_title(f"Métricas de unidad económica\nLTV/CAC = {d['ratio']:.1f}   |   Payback CAC: {d.get('payback_cac_months', '?')} meses")
    ax.grid(True, alpha=0.25, axis="y", linestyle="--")
    fig.tight_layout()
    fig.savefig(output_dir / "chart_p4_07_unit_economics.png", dpi=DPI, bbox_inches="tight")
    plt.close(fig)


def chart_risk_matrix(data, output_dir):
    if "risk_matrix" not in data:
        return
    items = data["risk_matrix"]
    category_color = {
        "mercado": COLORS["accent"],
        "operativo": COLORS["primary"],
        "regulatorio": COLORS["highlight"],
        "financiero": COLORS["secondary"],
        "partnership": COLORS["ok"],
    }
    fig, ax = plt.subplots(figsize=(9, 7))
    for it in items:
        cat = it.get("category", "operativo")
        color = category_color.get(cat, COLORS["neutral"])
        ax.scatter(it["probability"], it["impact"], s=350, c=color, alpha=0.75,
                   edgecolor="white", linewidth=1.5)
        ax.annotate(it["risk"], (it["probability"], it["impact"]),
                    xytext=(7, 5), textcoords="offset points", fontsize=8.5)

    # Zonas de criticidad
    ax.fill_between([3.5, 5.5], 3.5, 5.5, color=COLORS["pessimistic"], alpha=0.08)
    ax.text(5, 5, "CRÍTICO", color=COLORS["pessimistic"], fontsize=11, fontweight="bold",
            ha="right", va="top", alpha=0.4)
    ax.fill_between([0, 1.5], 0, 1.5, color=COLORS["ok"], alpha=0.08)

    ax.set_xlim(0, 5.5)
    ax.set_ylim(0, 5.5)
    ax.set_xlabel("Probabilidad (1=baja, 5=alta)")
    ax.set_ylabel("Impacto (1=bajo, 5=alto)")
    ax.set_title("Matriz de riesgos: probabilidad × impacto")
    ax.grid(True, alpha=0.25, linestyle="--")

    # Leyenda manual
    handles = [plt.Line2D([0], [0], marker="o", color="w", markerfacecolor=c, markersize=11, label=k.capitalize())
               for k, c in category_color.items()]
    ax.legend(handles=handles, loc="lower right", framealpha=0.95, fontsize=9)
    fig.tight_layout()
    fig.savefig(output_dir / "chart_p4_08_risk_matrix.png", dpi=DPI, bbox_inches="tight")
    plt.close(fig)


def chart_validation_program(data, output_dir):
    if "validation_program" not in data:
        return
    items = data["validation_program"].get("hypotheses", [])
    if not items:
        return
    fig, ax = plt.subplots(figsize=(11, 0.7 * len(items) + 2))
    quarter_color = {1: COLORS["primary"], 2: COLORS["secondary"], 3: COLORS["highlight"], 4: COLORS["ok"]}
    y = np.arange(len(items))[::-1]
    for i, it in enumerate(items):
        q = it.get("quarter", 1)
        color = quarter_color.get(q, COLORS["neutral"])
        ax.barh(y[i], it["budget"], color=color, edgecolor="white", linewidth=1.2)
        ax.text(it["budget"] + 200, y[i],
                f" {it['id']}: {it['name']} (T{q}) — {it['budget']:,}",
                va="center", fontsize=9)
    ax.set_yticks(y)
    ax.set_yticklabels([it["id"] for it in items])
    ax.set_xlabel("Presupuesto (USD)")
    ax.set_title("Programa de validación: hipótesis críticas y presupuestos por trimestre")
    ax.grid(True, alpha=0.25, axis="x", linestyle="--")

    # Leyenda
    handles = [plt.Line2D([0], [0], marker="s", color="w", markerfacecolor=c, markersize=11,
                          label=f"Trimestre {q}")
               for q, c in quarter_color.items()]
    ax.legend(handles=handles, loc="lower right", framealpha=0.95, fontsize=9)

    total = sum(it["budget"] for it in items)
    ax.text(0.99, 0.02, f"Presupuesto total: {total:,} USD",
            transform=ax.transAxes, ha="right", va="bottom",
            fontsize=10, fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.4", facecolor="#f4f4f4", edgecolor="#ccc"))

    fig.tight_layout()
    fig.savefig(output_dir / "chart_p4_09_validation.png", dpi=DPI, bbox_inches="tight")
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--inputs", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    with open(args.inputs, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}

    chart_revenue_by_scenario(data, args.output_dir)
    chart_ebitda_by_scenario(data, args.output_dir)
    chart_free_cash_flow(data, args.output_dir)
    chart_tornado(data, args.output_dir)
    chart_breakeven(data, args.output_dir)
    chart_scenarios_summary(data, args.output_dir)
    chart_unit_economics(data, args.output_dir)
    chart_risk_matrix(data, args.output_dir)
    chart_validation_program(data, args.output_dir)

    print(f"Gráficos de Parte 4 generados en {args.output_dir}")


if __name__ == "__main__":
    main()
