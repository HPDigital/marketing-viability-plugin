#!/usr/bin/env python3
"""
generate_part2_charts.py
Genera los gráficos canónicos del Marketing Estratégico (Parte 2).

Uso:
    python generate_part2_charts.py --inputs chart_inputs.yaml --output-dir charts/

Estructura del chart_inputs.yaml:

segment_evaluation:
  - {id: "P1", name: "Amputado traumático", attractiveness: 4, fit: 4, volume: 1200}
  - {id: "P2", name: "Amputado diabético", attractiveness: 4, fit: 3, volume: 2750}
  - {id: "P3", name: "Clínicas privadas", attractiveness: 3, fit: 4, volume: 18}

perceptual_map:
  dimensions:
    x: "Calidad técnica"
    y: "Servicio integrado"
  actors:
    - {name: "Ortopedias locales", x: 3, y: 2, type: "competitor"}
    - {name: "Importadores", x: 2, y: 1, type: "competitor"}
    - {name: "Viajes médicos", x: 4, y: 1, type: "substitute"}
    - {name: "Propuesta to-be", x: 5, y: 5, type: "proposal"}

strategy_canvas:
  factors:
    - {id: "F1", short: "Calidad técnica", to_be: 5, as_is: 3, competitor: 3}
    - {id: "F2", short: "Ajuste local", to_be: 5, as_is: 3, competitor: 3}
    - {id: "F3", short: "Repuestos 5+ años", to_be: 5, as_is: 1, competitor: 2}
    - {id: "F4", short: "SLA escrito", to_be: 5, as_is: 1, competitor: 2}
    - {id: "F5", short: "Contrato seguimiento", to_be: 5, as_is: 1, competitor: 1}
    - {id: "F6", short: "Trazabilidad regulatoria", to_be: 5, as_is: 3, competitor: 3}
    - {id: "F7", short: "Financiamiento cuotas", to_be: 4, as_is: 2, competitor: 2}
    - {id: "F8", short: "Predictibilidad financiera", to_be: 5, as_is: 1, competitor: 1}
    - {id: "F9", short: "Retorno laboral", to_be: 4, as_is: 2, competitor: 2}
    - {id: "F10", short: "Prevención educación", to_be: 4, as_is: 1, competitor: 1}
    - {id: "F11", short: "Coexistencia local", to_be: 4, as_is: 2, competitor: 1}
    - {id: "F12", short: "Reposicionamiento social", to_be: 4, as_is: 1, competitor: 1}

eric_distribution:
  eliminate: ["Marketing consumer-side masivo", "Catálogo extenso multi-marca"]
  reduce: ["Sucursales adicionales arranque", "I+D propio"]
  raise: ["F1", "F2", "F6", "F7", "F9", "F11"]
  create: ["F3", "F4", "F5", "F8", "F10", "F12"]

non_clients:
  - {tier: "Tier 1 Soon-to-be", description: "Pacientes con prótesis básica", size: 1750, activation_factor: 0.9}
  - {tier: "Tier 2 Refusing", description: "Pacientes que abandonan o viajan", size: 1000, activation_factor: 0.5}
  - {tier: "Tier 3 Unexplored", description: "Clínicas privadas sin línea ortoprotésica", size: 18, activation_factor: 0.7}

targeting_roadmap:
  segments:
    - {id: "P1", name: "P1 traumático", years: [1, 2, 3, 4, 5], intensity: [3, 3, 3, 3, 3]}
    - {id: "P3", name: "P3 clínicas", years: [1, 2, 3, 4, 5], intensity: [2, 3, 3, 3, 3]}
    - {id: "P2", name: "P2 diabético", years: [2, 3, 4, 5], intensity: [1, 2, 3, 3]}
    - {id: "expansion", name: "Expansión geográfica", years: [3, 4, 5], intensity: [1, 2, 3]}
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
    "eliminate": "#8b2c2c",
    "reduce": "#d68a3c",
    "raise": "#5b9bd5",
    "create": "#0b6e3a",
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


def chart_segment_evaluation(data, output_dir):
    if "segment_evaluation" not in data:
        return
    items = data["segment_evaluation"]
    fig, ax = plt.subplots(figsize=(8.5, 6.5))
    for it in items:
        size = max(it.get("volume", 100) * 0.5, 200)
        size = min(size, 2500)
        is_entry = it.get("is_entry", False) or items.index(it) == 0
        color = COLORS["accent"] if is_entry else COLORS["secondary"]
        ax.scatter(it["fit"], it["attractiveness"], s=size, c=color, alpha=0.65,
                   edgecolor=COLORS["primary"], linewidth=2 if is_entry else 1)
        ax.annotate(f"{it['id']}: {it['name']}", (it["fit"], it["attractiveness"]),
                    xytext=(0, -22), textcoords="offset points", ha="center", fontsize=9,
                    fontweight="bold" if is_entry else "normal")

    ax.set_xlim(0, 5.5)
    ax.set_ylim(0, 5.5)
    ax.set_xlabel("Ajuste con capacidades del negocio (1-5)")
    ax.set_ylabel("Atractividad del segmento (1-5)")
    ax.set_title("Matriz de evaluación de segmentos\n(tamaño = volumen estimado)")
    ax.grid(True, alpha=0.25, linestyle="--")
    ax.axhline(y=3, color=COLORS["neutral"], linestyle=":", linewidth=0.8, alpha=0.5)
    ax.axvline(x=3, color=COLORS["neutral"], linestyle=":", linewidth=0.8, alpha=0.5)
    fig.tight_layout()
    fig.savefig(output_dir / "chart_p2_01_segment_evaluation.png", dpi=DPI, bbox_inches="tight")
    plt.close(fig)


def chart_perceptual_map(data, output_dir):
    if "perceptual_map" not in data:
        return
    pm = data["perceptual_map"]
    fig, ax = plt.subplots(figsize=(9, 6.5))
    color_map = {
        "competitor": COLORS["secondary"],
        "substitute": COLORS["neutral"],
        "proposal": COLORS["accent"],
    }
    for actor in pm["actors"]:
        atype = actor.get("type", "competitor")
        is_proposal = atype == "proposal"
        color = color_map.get(atype, COLORS["secondary"])
        ax.scatter(actor["x"], actor["y"], s=350 if is_proposal else 200, c=color,
                   alpha=0.75, edgecolor=COLORS["primary"] if is_proposal else "white",
                   linewidth=2 if is_proposal else 1)
        ax.annotate(actor["name"], (actor["x"], actor["y"]),
                    xytext=(0, -22), textcoords="offset points", ha="center",
                    fontsize=9, fontweight="bold" if is_proposal else "normal")

    ax.set_xlim(0, 5.5)
    ax.set_ylim(0, 5.5)
    ax.set_xlabel(pm["dimensions"]["x"])
    ax.set_ylabel(pm["dimensions"]["y"])
    ax.set_title("Mapa perceptual: posición competitiva")
    ax.grid(True, alpha=0.25, linestyle="--")
    ax.axhline(y=2.5, color=COLORS["neutral"], linestyle=":", linewidth=0.8, alpha=0.5)
    ax.axvline(x=2.5, color=COLORS["neutral"], linestyle=":", linewidth=0.8, alpha=0.5)
    fig.tight_layout()
    fig.savefig(output_dir / "chart_p2_02_perceptual_map.png", dpi=DPI, bbox_inches="tight")
    plt.close(fig)


def chart_strategy_canvas(data, output_dir):
    if "strategy_canvas" not in data:
        return
    factors = data["strategy_canvas"]["factors"]
    labels = [f["short"] for f in factors]
    to_be = [f["to_be"] for f in factors]
    as_is = [f["as_is"] for f in factors]
    competitor = [f["competitor"] for f in factors]
    x = np.arange(len(labels))

    fig, ax = plt.subplots(figsize=(13, 5.5))
    ax.plot(x, to_be, marker="o", color=COLORS["accent"], linewidth=2.5, markersize=9, label="Propuesta to-be")
    ax.plot(x, as_is, marker="s", color=COLORS["neutral"], linewidth=1.8, markersize=7, label="Industria as-is")
    ax.plot(x, competitor, marker="^", color=COLORS["secondary"], linewidth=1.8, markersize=7, label="Competidor directo")
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=40, ha="right", fontsize=9)
    ax.set_ylim(0, 5.5)
    ax.set_yticks([0, 1, 2, 3, 4, 5])
    ax.set_ylabel("Nivel ofrecido (0-5)")
    ax.set_title("Strategy Canvas: curva de valor de la propuesta vs industria as-is y competidor directo")
    ax.grid(True, alpha=0.25, linestyle="--")
    ax.legend(loc="lower right", framealpha=0.95)
    fig.tight_layout()
    fig.savefig(output_dir / "chart_p2_03_strategy_canvas.png", dpi=DPI, bbox_inches="tight")
    plt.close(fig)


def chart_eric_distribution(data, output_dir):
    if "eric_distribution" not in data:
        return
    eric = data["eric_distribution"]
    cats = ["Eliminate", "Reduce", "Raise", "Create"]
    counts = [
        len(eric.get("eliminate", [])),
        len(eric.get("reduce", [])),
        len(eric.get("raise", [])),
        len(eric.get("create", [])),
    ]
    colors = [COLORS["eliminate"], COLORS["reduce"], COLORS["raise"], COLORS["create"]]

    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(cats, counts, color=colors, edgecolor="white", linewidth=1.4)
    ax.set_ylabel("Número de decisiones")
    ax.set_title("Distribución ERIC: Eliminate, Reduce, Raise, Create")
    ax.grid(True, alpha=0.25, axis="y", linestyle="--")
    for bar, c in zip(bars, counts):
        ax.text(bar.get_x() + bar.get_width() / 2, c + 0.1, str(c),
                ha="center", fontsize=11, fontweight="bold")
    fig.tight_layout()
    fig.savefig(output_dir / "chart_p2_04_eric.png", dpi=DPI, bbox_inches="tight")
    plt.close(fig)


def chart_non_clients(data, output_dir):
    if "non_clients" not in data:
        return
    items = data["non_clients"]
    tiers = [it["tier"] for it in items]
    sizes = [it["size"] for it in items]
    activation = [it["size"] * it.get("activation_factor", 0.5) for it in items]

    fig, ax = plt.subplots(figsize=(10, 5.5))
    y = np.arange(len(tiers))
    ax.barh(y, sizes, color=COLORS["neutral"], alpha=0.5, label="Tamaño total del tier")
    ax.barh(y, activation, color=COLORS["accent"], alpha=0.85, label="Activable por la propuesta")
    ax.set_yticks(y)
    ax.set_yticklabels(tiers)
    ax.set_xlabel("Tamaño estimado (unidades)")
    ax.set_title("Tres tiers de no-clientes y porción activable")
    ax.grid(True, alpha=0.25, axis="x", linestyle="--")
    ax.legend(loc="lower right", framealpha=0.95)
    for i, (s, a) in enumerate(zip(sizes, activation)):
        ax.text(s * 1.02, i, f"{int(a):,}/{int(s):,}", va="center", fontsize=9)
    fig.tight_layout()
    fig.savefig(output_dir / "chart_p2_05_non_clients.png", dpi=DPI, bbox_inches="tight")
    plt.close(fig)


def chart_targeting_roadmap(data, output_dir):
    if "targeting_roadmap" not in data:
        return
    segments = data["targeting_roadmap"]["segments"]
    fig, ax = plt.subplots(figsize=(11, 0.7 * len(segments) + 1.5))

    intensity_color = {0: "#ffffff", 1: "#dde7f0", 2: COLORS["secondary"], 3: COLORS["primary"]}
    intensity_label = {0: "—", 1: "Inicio", 2: "Activo", 3: "Foco"}

    all_years = sorted({y for seg in segments for y in seg["years"]})
    year_min, year_max = min(all_years), max(all_years)
    years_range = list(range(year_min, year_max + 1))

    for i, seg in enumerate(reversed(segments)):
        for j, year in enumerate(years_range):
            if year in seg["years"]:
                idx_in_years = seg["years"].index(year)
                intensity = seg["intensity"][idx_in_years]
            else:
                intensity = 0
            color = intensity_color.get(intensity, "#ffffff")
            ax.barh(i, 1, left=year - 0.4, color=color, edgecolor=COLORS["neutral"], linewidth=0.6)
            if intensity > 0:
                ax.text(year, i, intensity_label[intensity], ha="center", va="center", fontsize=8, color="white" if intensity >= 2 else COLORS["primary"])

    ax.set_yticks(range(len(segments)))
    ax.set_yticklabels([s["name"] for s in reversed(segments)])
    ax.set_xticks(years_range)
    ax.set_xticklabels([f"Año {y}" for y in years_range])
    ax.set_title("Roadmap de targeting plurianual")
    ax.set_xlim(year_min - 0.5, year_max + 0.5)
    fig.tight_layout()
    fig.savefig(output_dir / "chart_p2_06_targeting_roadmap.png", dpi=DPI, bbox_inches="tight")
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--inputs", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    with open(args.inputs, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}

    chart_segment_evaluation(data, args.output_dir)
    chart_perceptual_map(data, args.output_dir)
    chart_strategy_canvas(data, args.output_dir)
    chart_eric_distribution(data, args.output_dir)
    chart_non_clients(data, args.output_dir)
    chart_targeting_roadmap(data, args.output_dir)

    print(f"Gráficos de Parte 2 generados en {args.output_dir}")


if __name__ == "__main__":
    main()
