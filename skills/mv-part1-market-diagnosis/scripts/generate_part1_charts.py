#!/usr/bin/env python3
"""
generate_part1_charts.py
Genera los ocho gráficos canónicos del diagnóstico de mercado.

Uso:
    python generate_part1_charts.py --inputs chart_inputs.yaml --output-dir charts/

El archivo chart_inputs.yaml debe tener la siguiente estructura:

tam_sam_som:
  tam: {min: 25000, max: 45000, unit: "personas"}
  sam: {min: 4000, max: 7500, unit: "personas"}
  som: {min: 80, max: 150, unit: "Big Hire/año"}
  tam_value: {min: 50, max: 100, currency: "USD M"}
  sam_value: {min: 9, max: 19, currency: "USD M"}
  som_value: {min: 1.9, max: 3.6, currency: "USD M"}

cagr_by_segment:
  - {segment: "P1 traumático", cagr: 2.0}
  - {segment: "P2 diabético", cagr: 5.0}
  - {segment: "P3 clínicas", cagr: 3.0}

porter:
  rivalry: 3
  new_entrants: 2
  substitutes: 4
  suppliers: 3
  buyers: 3

price_benchmark:
  - {category: "Importadores anónimos", low: 1500, high: 3500, mid: 2500}
  - {category: "Ortopedias locales", low: 4000, high: 7000, mid: 5500}
  - {category: "Propuesta del caso", low: 6000, high: 12000, mid: 9000}
  - {category: "Viajes médicos", low: 8000, high: 15000, mid: 11500}

four_forces:
  push: {score: 4, label: "Push (dolor del statu quo)"}
  pull: {score: 3, label: "Pull (atractivo de la propuesta)"}
  anxiety: {score: 4, label: "Anxiety (miedo al cambio)"}
  habit: {score: 3, label: "Habit (rutinas establecidas)"}

outcomes:
  - {id: "O01", desc: "Encontrar técnico", importance: 5, satisfaction: 2}
  - {id: "O02", desc: "Repuestos garantizados", importance: 5, satisfaction: 1}
  - {id: "O07", desc: "Financiamiento accesible", importance: 5, satisfaction: 1}
  - {id: "O11", desc: "Minimizar caídas", importance: 5, satisfaction: 2}
  - {id: "O17", desc: "Estética bajo ropa", importance: 3, satisfaction: 3}

wtp_by_segment:
  - {segment: "P1", samples: [6000, 7500, 8000, 9000, 10000, 11000, 12000]}
  - {segment: "P2", samples: [4000, 5000, 6000, 6500, 7000, 8000]}

competitors_2d:
  dimensions:
    x: "Calidad técnica del componente"
    y: "Servicio integrado y seguimiento"
  competitors:
    - {name: "Ortopedias locales", x: 3, y: 2, share: 25}
    - {name: "Importadores anónimos", x: 2, y: 1, share: 30}
    - {name: "Representantes europeos", x: 4, y: 2, share: 10}
    - {name: "Viajes médicos", x: 4, y: 1, share: 5}
    - {name: "Propuesta del caso", x: 5, y: 5, share: 0}
"""

import argparse
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.stderr.write("Falta pyyaml. Instalar con pip install pyyaml\n")
    sys.exit(2)

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np
except ImportError:
    sys.stderr.write("Falta matplotlib/numpy. Instalar con pip install matplotlib numpy\n")
    sys.exit(2)

# Paleta de colores institucional sobria
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
    "axes.labelsize": 9,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "figure.facecolor": "white",
})


def chart_tam_sam_som(data, output_dir):
    """Chart 1: TAM, SAM, SOM en escala logarítmica con barras de error."""
    if "tam_sam_som" not in data:
        return
    d = data["tam_sam_som"]

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))

    # En unidades
    cats = ["TAM", "SAM", "SOM"]
    mins = [d["tam"]["min"], d["sam"]["min"], d["som"]["min"]]
    maxs = [d["tam"]["max"], d["sam"]["max"], d["som"]["max"]]
    mids = [(a + b) / 2 for a, b in zip(mins, maxs)]
    errs_low = [m - mn for m, mn in zip(mids, mins)]
    errs_high = [mx - m for m, mx in zip(mids, maxs)]

    axes[0].bar(cats, mids, yerr=[errs_low, errs_high], capsize=8,
                color=[COLORS["neutral"], COLORS["secondary"], COLORS["primary"]],
                edgecolor="white", linewidth=1.2)
    axes[0].set_yscale("log")
    axes[0].set_title(f"Mercado en unidades ({d['tam'].get('unit', '')})", pad=10)
    axes[0].grid(True, alpha=0.25, axis="y", linestyle="--")
    for i, (mn, mx) in enumerate(zip(mins, maxs)):
        axes[0].text(i, mx * 1.15, f"{mn:,}–{mx:,}", ha="center", fontsize=8.5)

    # En valor
    if all(k in d for k in ["tam_value", "sam_value", "som_value"]):
        cats_v = ["TAM", "SAM", "SOM"]
        mins_v = [d["tam_value"]["min"], d["sam_value"]["min"], d["som_value"]["min"]]
        maxs_v = [d["tam_value"]["max"], d["sam_value"]["max"], d["som_value"]["max"]]
        mids_v = [(a + b) / 2 for a, b in zip(mins_v, maxs_v)]
        errs_low_v = [m - mn for m, mn in zip(mids_v, mins_v)]
        errs_high_v = [mx - m for m, mx in zip(mids_v, maxs_v)]
        currency = d["tam_value"].get("currency", "USD")

        axes[1].bar(cats_v, mids_v, yerr=[errs_low_v, errs_high_v], capsize=8,
                    color=[COLORS["neutral"], COLORS["secondary"], COLORS["primary"]],
                    edgecolor="white", linewidth=1.2)
        axes[1].set_yscale("log")
        axes[1].set_title(f"Mercado en valor ({currency})", pad=10)
        axes[1].grid(True, alpha=0.25, axis="y", linestyle="--")
        for i, (mn, mx) in enumerate(zip(mins_v, maxs_v)):
            axes[1].text(i, mx * 1.15, f"{mn}–{mx}", ha="center", fontsize=8.5)

    fig.suptitle("Dimensionamiento del mercado: TAM, SAM, SOM", fontsize=12, y=1.02)
    fig.tight_layout()
    fig.savefig(output_dir / "chart_01_tam_sam_som.png", dpi=DPI, bbox_inches="tight")
    plt.close(fig)


def chart_cagr_by_segment(data, output_dir):
    """Chart 2: CAGR estructural por segmento."""
    if "cagr_by_segment" not in data:
        return
    items = data["cagr_by_segment"]
    segs = [it["segment"] for it in items]
    cagrs = [it["cagr"] for it in items]

    fig, ax = plt.subplots(figsize=(8, 0.7 * len(segs) + 1.5))
    bars = ax.barh(segs, cagrs, color=COLORS["primary"], edgecolor="white", linewidth=1.2)
    ax.set_xlabel("CAGR estructural esperado (%)")
    ax.set_title("Crecimiento estructural anual proyectado por segmento")
    ax.grid(True, alpha=0.25, axis="x", linestyle="--")
    for bar, cagr in zip(bars, cagrs):
        ax.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height() / 2,
                f"{cagr:.1f}%", va="center", fontsize=9)
    fig.tight_layout()
    fig.savefig(output_dir / "chart_02_cagr.png", dpi=DPI, bbox_inches="tight")
    plt.close(fig)


def chart_porter_radar(data, output_dir):
    """Chart 3: Cinco fuerzas de Porter en radar."""
    if "porter" not in data:
        return
    p = data["porter"]
    labels = ["Rivalidad", "Nuevos entrantes", "Sustitutos", "Proveedores", "Compradores"]
    values = [p["rivalry"], p["new_entrants"], p["substitutes"], p["suppliers"], p["buyers"]]
    values_closed = values + [values[0]]
    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    angles_closed = angles + [angles[0]]

    fig, ax = plt.subplots(figsize=(7, 7), subplot_kw=dict(polar=True))
    ax.plot(angles_closed, values_closed, color=COLORS["primary"], linewidth=2)
    ax.fill(angles_closed, values_closed, color=COLORS["primary"], alpha=0.20)
    ax.set_xticks(angles)
    ax.set_xticklabels(labels, fontsize=10)
    ax.set_yticks([1, 2, 3, 4, 5])
    ax.set_yticklabels(["1 Bajo", "2", "3 Medio", "4", "5 Alto"], fontsize=8)
    ax.set_ylim(0, 5)
    ax.set_title("Cinco fuerzas de Porter", pad=20, fontsize=12)
    fig.tight_layout()
    fig.savefig(output_dir / "chart_03_porter.png", dpi=DPI, bbox_inches="tight")
    plt.close(fig)


def chart_price_benchmark(data, output_dir):
    """Chart 4: Benchmark de precios por categoría competitiva."""
    if "price_benchmark" not in data:
        return
    items = data["price_benchmark"]
    cats = [it["category"] for it in items]
    lows = [it["low"] for it in items]
    highs = [it["high"] for it in items]
    mids = [it.get("mid", (it["low"] + it["high"]) / 2) for it in items]

    fig, ax = plt.subplots(figsize=(10, 0.7 * len(cats) + 1.5))
    y = np.arange(len(cats))
    for i, (lo, hi, mi) in enumerate(zip(lows, highs, mids)):
        color = COLORS["accent"] if "propuesta" in cats[i].lower() or "caso" in cats[i].lower() else COLORS["secondary"]
        ax.plot([lo, hi], [i, i], linewidth=8, color=color, alpha=0.65, solid_capstyle="round")
        ax.plot(mi, i, "o", color="white", markersize=6, markeredgecolor=color, markeredgewidth=2)
        ax.text(hi * 1.02, i, f"{lo:,}–{hi:,}", va="center", fontsize=9)
    ax.set_yticks(y)
    ax.set_yticklabels(cats)
    ax.set_xlabel("Precio (USD)")
    ax.set_title("Benchmark de precios por categoría competitiva")
    ax.grid(True, alpha=0.25, axis="x", linestyle="--")
    ax.set_xlim(0, max(highs) * 1.25)
    fig.tight_layout()
    fig.savefig(output_dir / "chart_04_price_benchmark.png", dpi=DPI, bbox_inches="tight")
    plt.close(fig)


def chart_four_forces(data, output_dir):
    """Chart 5: Cuatro fuerzas push-pull vs anxiety-habit."""
    if "four_forces" not in data:
        return
    ff = data["four_forces"]

    fig, ax = plt.subplots(figsize=(8.5, 5))
    forces = ["Push", "Pull", "Anxiety", "Habit"]
    scores = [ff["push"]["score"], ff["pull"]["score"], -ff["anxiety"]["score"], -ff["habit"]["score"]]
    colors = [COLORS["ok"], COLORS["ok"], COLORS["accent"], COLORS["accent"]]
    bars = ax.bar(forces, scores, color=colors, edgecolor="white", linewidth=1.4)
    ax.axhline(y=0, color="black", linewidth=0.8)
    ax.set_ylim(-5.5, 5.5)
    ax.set_ylabel("Score (a favor del switch ↑ / contra el switch ↓)")
    ax.set_yticks([-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5])
    ax.set_yticklabels(["5", "4", "3", "2", "1", "0", "1", "2", "3", "4", "5"])
    ax.set_title("Análisis de cuatro fuerzas (Moesta)")
    for bar, sc in zip(bars, scores):
        ax.text(bar.get_x() + bar.get_width() / 2, sc + (0.15 if sc >= 0 else -0.45),
                f"{abs(sc)}", ha="center", fontsize=10, fontweight="bold")

    sum_pro = ff["push"]["score"] + ff["pull"]["score"]
    sum_against = ff["anxiety"]["score"] + ff["habit"]["score"]
    ax.text(0.98, 0.02,
            f"A favor del switch: {sum_pro}   /   Contra el switch: {sum_against}\n"
            f"Delta: {sum_pro - sum_against}",
            transform=ax.transAxes, ha="right", va="bottom",
            fontsize=9, bbox=dict(boxstyle="round,pad=0.4", facecolor="#f4f4f4", edgecolor="#ccc"))

    fig.tight_layout()
    fig.savefig(output_dir / "chart_05_four_forces.png", dpi=DPI, bbox_inches="tight")
    plt.close(fig)


def chart_outcomes_matrix(data, output_dir):
    """Chart 6: Matriz importancia × satisfacción con líneas iso-opportunity."""
    if "outcomes" not in data:
        return
    items = data["outcomes"]
    imp = [it["importance"] for it in items]
    sat = [it["satisfaction"] for it in items]
    ids = [it["id"] for it in items]

    fig, ax = plt.subplots(figsize=(8.5, 6.5))

    # Líneas iso-opportunity (OS = imp + max(imp - sat, 0)). Para visual: dibujamos curvas referenciales.
    x = np.linspace(0, 5, 100)
    for os_val, label in [(8, "OS=8 (decisivo)"), (10, "OS=10 (subatendido)"), (12, "OS=12 (hiper)")]:
        y_vals = []
        for s_val in x:
            # Resolver imp: imp + max(imp - s, 0) = os_val
            # caso imp >= s: 2*imp - s = os_val => imp = (os_val + s) / 2
            imp_calc = (os_val + s_val) / 2
            if imp_calc < 0 or imp_calc > 5:
                y_vals.append(np.nan)
            else:
                y_vals.append(imp_calc)
        ax.plot(x, y_vals, linestyle="--", color=COLORS["neutral"], alpha=0.5, linewidth=1)
        ax.text(0.05, (os_val + 0.05) / 2, label, fontsize=8, color=COLORS["neutral"])

    ax.scatter(sat, imp, s=120, c=COLORS["primary"], edgecolor="white", linewidth=1.5, zorder=3)
    for s_val, i_val, oid in zip(sat, imp, ids):
        ax.annotate(oid, (s_val, i_val), xytext=(7, 5), textcoords="offset points", fontsize=8.5)

    ax.set_xlim(0, 5.5)
    ax.set_ylim(0, 5.5)
    ax.set_xlabel("Satisfacción con la solución actual (1=baja, 5=alta)")
    ax.set_ylabel("Importancia para el cliente (1=baja, 5=alta)")
    ax.set_title("Matriz de outcomes priorizados (Ulwick)")
    ax.grid(True, alpha=0.25, linestyle="--")
    fig.tight_layout()
    fig.savefig(output_dir / "chart_06_outcomes_matrix.png", dpi=DPI, bbox_inches="tight")
    plt.close(fig)


def chart_wtp_by_segment(data, output_dir):
    """Chart 7: Distribución de disposición a pagar declarada por segmento."""
    if "wtp_by_segment" not in data:
        return
    items = data["wtp_by_segment"]
    labels = [it["segment"] for it in items]
    samples = [it["samples"] for it in items]

    fig, ax = plt.subplots(figsize=(8.5, 4.5))
    bp = ax.boxplot(samples, labels=labels, patch_artist=True, vert=False, widths=0.5,
                    boxprops=dict(facecolor=COLORS["secondary"], color=COLORS["primary"]),
                    medianprops=dict(color=COLORS["primary"], linewidth=2),
                    whiskerprops=dict(color=COLORS["primary"]),
                    capprops=dict(color=COLORS["primary"]),
                    flierprops=dict(marker="o", markerfacecolor=COLORS["accent"], markersize=5))
    ax.set_xlabel("Disposición a pagar declarada (USD)")
    ax.set_title("Distribución de disposición a pagar por segmento")
    ax.grid(True, alpha=0.25, axis="x", linestyle="--")
    fig.tight_layout()
    fig.savefig(output_dir / "chart_07_wtp.png", dpi=DPI, bbox_inches="tight")
    plt.close(fig)


def chart_competitors_2d(data, output_dir):
    """Chart 8: Mapa de competidores en dos dimensiones críticas."""
    if "competitors_2d" not in data:
        return
    d = data["competitors_2d"]
    competitors = d["competitors"]
    x_label = d["dimensions"]["x"]
    y_label = d["dimensions"]["y"]

    fig, ax = plt.subplots(figsize=(9, 6.5))
    for comp in competitors:
        is_proposal = "propuesta" in comp["name"].lower() or "caso" in comp["name"].lower()
        color = COLORS["accent"] if is_proposal else COLORS["secondary"]
        size = max(comp.get("share", 5) * 60, 200)
        edge = "white" if not is_proposal else COLORS["primary"]
        ax.scatter(comp["x"], comp["y"], s=size, c=color, alpha=0.65,
                   edgecolor=edge, linewidth=2 if is_proposal else 1)
        ax.annotate(comp["name"], (comp["x"], comp["y"]),
                    xytext=(0, -22), textcoords="offset points",
                    ha="center", fontsize=9,
                    fontweight="bold" if is_proposal else "normal")

    ax.set_xlim(0, 5.5)
    ax.set_ylim(0, 5.5)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_title("Mapa perceptual de competidores (tamaño = cuota estimada)")
    ax.grid(True, alpha=0.25, linestyle="--")
    ax.axhline(y=2.5, color=COLORS["neutral"], linestyle=":", linewidth=0.8, alpha=0.5)
    ax.axvline(x=2.5, color=COLORS["neutral"], linestyle=":", linewidth=0.8, alpha=0.5)
    fig.tight_layout()
    fig.savefig(output_dir / "chart_08_competitors_2d.png", dpi=DPI, bbox_inches="tight")
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description="Generador de gráficos para la Parte 1.")
    parser.add_argument("--inputs", required=True, type=Path, help="Ruta al YAML con inputs de gráficos.")
    parser.add_argument("--output-dir", required=True, type=Path, help="Directorio donde guardar los PNG.")
    args = parser.parse_args()

    if not args.inputs.exists():
        sys.stderr.write(f"No se encuentra el archivo de inputs: {args.inputs}\n")
        sys.exit(1)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    with open(args.inputs, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}

    chart_tam_sam_som(data, args.output_dir)
    chart_cagr_by_segment(data, args.output_dir)
    chart_porter_radar(data, args.output_dir)
    chart_price_benchmark(data, args.output_dir)
    chart_four_forces(data, args.output_dir)
    chart_outcomes_matrix(data, args.output_dir)
    chart_wtp_by_segment(data, args.output_dir)
    chart_competitors_2d(data, args.output_dir)

    print(f"Gráficos generados en {args.output_dir}")


if __name__ == "__main__":
    main()
