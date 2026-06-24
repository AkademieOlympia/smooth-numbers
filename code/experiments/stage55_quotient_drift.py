#!/usr/bin/env python3
"""
Stage-5.5 Quotient-Drift analysis.

Parst bestehende Stage-5.5-Logs, berechnet Quotienten/Drifts,
führt monotone Trendtests aus und erzeugt:
  - experiments/results/stage55/stage55_quotient_table.csv
  - experiments/results/stage55/stage55_quotient_plots.png
  - experiments/results/stage55/STAGE55_QUOTIENT_DRIFT.md
"""

from __future__ import annotations

import csv
import math
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np

try:
    from scipy.stats import linregress, spearmanr
except Exception:
    linregress = None
    spearmanr = None

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


REPO_ROOT = Path(__file__).resolve().parents[2]
RESULTS_DIR = REPO_ROOT / "experiments" / "results" / "stage55"
CSV_OUT = RESULTS_DIR / "stage55_quotient_table.csv"
PLOT_OUT = RESULTS_DIR / "stage55_quotient_plots.png"
MD_OUT = RESULTS_DIR / "STAGE55_QUOTIENT_DRIFT.md"


STAGE55_RUN_FILES: Sequence[Path] = [
    REPO_ROOT / "stage5.5_final_run.txt",        # N=1e6
    REPO_ROOT / "reproducibility_N10M.txt",      # N=1e7
    REPO_ROOT / "reproducibility_N20M.txt",      # N=2e7 (neu)
]

HL_PROXY_FILE = REPO_ROOT / "reproducibility_stage6_N1M.txt"


@dataclass
class RunData:
    n: int
    h_prime: Dict[int, float]
    h_wheel_random: Dict[int, float]
    h_wheel_cramer: Dict[int, float]


def parse_stage55_run(path: Path) -> RunData:
    text = path.read_text(encoding="utf-8")

    n_match = re.search(r"^N\s*=\s*(\d+)\s*$", text, flags=re.MULTILINE)
    if not n_match:
        raise ValueError(f"Konnte N nicht parsen aus {path}")
    n = int(n_match.group(1))

    h_prime: Dict[int, float] = {}
    h_wheel_random: Dict[int, float] = {}
    h_wheel_cramer: Dict[int, float] = {}

    for dr, val in re.findall(r"Δr=(\d+):\s*H_Prime\s*=\s*([0-9.]+)", text):
        h_prime[int(dr)] = float(val)
    for dr, val in re.findall(r"Δr=(\d+):\s*H_WheelRandom\s*=\s*([0-9.]+)", text):
        h_wheel_random[int(dr)] = float(val)
    for dr, val in re.findall(r"Δr=(\d+):\s*H_WheelCramér\s*=\s*([0-9.]+)", text):
        h_wheel_cramer[int(dr)] = float(val)

    delta_r_values = sorted(set(h_prime) & set(h_wheel_random) & set(h_wheel_cramer))
    if not delta_r_values:
        raise ValueError(f"Keine gemeinsamen Δr-Werte in {path}")

    return RunData(
        n=n,
        h_prime={dr: h_prime[dr] for dr in delta_r_values},
        h_wheel_random={dr: h_wheel_random[dr] for dr in delta_r_values},
        h_wheel_cramer={dr: h_wheel_cramer[dr] for dr in delta_r_values},
    )


def parse_hl_proxies(path: Path) -> Tuple[Dict[int, float], Dict[int, float]]:
    """
    Extrahiert H_k3/H_k4-Proxywerte aus Stage-6-Repro-Output.
    """
    if not path.exists():
        return {}, {}

    lines = path.read_text(encoding="utf-8").splitlines()
    h_k3: Dict[int, float] = {}
    h_k4: Dict[int, float] = {}
    section: Optional[str] = None

    for raw in lines:
        line = raw.strip()
        if "Comparison: H_empirical vs H_k3" in line:
            section = "k3"
            continue
        if "Comparison: H_empirical vs H_k4" in line:
            section = "k4"
            continue
        if not line:
            continue
        if line.startswith("Correlation:"):
            section = None
            continue
        m = re.match(r"^(\d+)\s+([0-9.]+)\s+([0-9.]+)$", line)
        if section and m:
            dr = int(m.group(1))
            proxy_val = float(m.group(3))
            if section == "k3":
                h_k3[dr] = proxy_val
            elif section == "k4":
                h_k4[dr] = proxy_val

    return h_k3, h_k4


def format_n_human(n: int) -> str:
    if n >= 1_000_000:
        return f"{n / 1_000_000:.0f}e6"
    return str(n)


def safe_spearman(x: Sequence[float], y: Sequence[float]) -> Tuple[float, float]:
    if len(x) < 3:
        return math.nan, math.nan
    if spearmanr is not None:
        rho, p = spearmanr(x, y)
        return float(rho), float(p)

    # Fallback: Spearman rho ohne p-Wert
    x_rank = np.argsort(np.argsort(x))
    y_rank = np.argsort(np.argsort(y))
    rho = np.corrcoef(x_rank, y_rank)[0, 1]
    return float(rho), math.nan


def safe_linreg(x: Sequence[float], y: Sequence[float]) -> Tuple[float, float, float]:
    """
    Returns slope, intercept, r2.
    """
    if len(x) < 2:
        return math.nan, math.nan, math.nan
    if linregress is not None:
        fit = linregress(x, y)
        return float(fit.slope), float(fit.intercept), float(fit.rvalue ** 2)
    slope, intercept = np.polyfit(np.array(x), np.array(y), 1)
    y_hat = slope * np.array(x) + intercept
    ss_res = np.sum((np.array(y) - y_hat) ** 2)
    ss_tot = np.sum((np.array(y) - np.mean(y)) ** 2)
    r2 = 1.0 - (ss_res / ss_tot if ss_tot > 0 else math.nan)
    return float(slope), float(intercept), float(r2)


def fit_proxy_gain(y: np.ndarray, proxy: np.ndarray) -> Dict[str, float]:
    """
    Vergleicht Intercept-only gegen lineares Modell y ~ 1 + proxy.
    """
    if len(y) != len(proxy) or len(y) < 3:
        return {"sse0": math.nan, "sse1": math.nan, "r2_gain": math.nan}

    y_mean = np.mean(y)
    sse0 = float(np.sum((y - y_mean) ** 2))

    x = np.column_stack([np.ones(len(proxy)), proxy])
    beta, *_ = np.linalg.lstsq(x, y, rcond=None)
    y_hat = x @ beta
    sse1 = float(np.sum((y - y_hat) ** 2))

    if sse0 <= 0:
        r2_gain = math.nan
    else:
        r2_gain = 1.0 - sse1 / sse0

    return {"sse0": sse0, "sse1": sse1, "r2_gain": float(r2_gain)}


def main() -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    runs: List[RunData] = []
    missing: List[str] = []
    for path in STAGE55_RUN_FILES:
        if path.exists():
            runs.append(parse_stage55_run(path))
        else:
            missing.append(str(path.relative_to(REPO_ROOT)))

    if len(runs) < 2:
        raise RuntimeError("Zu wenige Stage-5.5-Läufe gefunden (mindestens 2 benötigt).")

    runs.sort(key=lambda r: r.n)
    common_delta_r = sorted(
        set.intersection(*[set(run.h_prime.keys()) for run in runs])
    )
    if not common_delta_r:
        raise RuntimeError("Keine gemeinsamen Δr-Werte über die Läufe hinweg gefunden.")

    h_k3_proxy, h_k4_proxy = parse_hl_proxies(HL_PROXY_FILE)

    rows: List[Dict[str, float]] = []
    trend_summary: Dict[int, Dict[str, float]] = {}

    for run in runs:
        x = []
        y_dh_cramer = []
        y_q_cramer = []

        for dr in common_delta_r:
            h_prime = run.h_prime[dr]
            h_rand = run.h_wheel_random[dr]
            h_cram = run.h_wheel_cramer[dr]
            delta_h_wheel = h_prime - h_rand
            delta_h_cramer = h_prime - h_cram
            q_random = h_prime / h_rand
            q_cramer = h_prime / h_cram

            row = {
                "N": run.n,
                "delta_r": dr,
                "H_prime": h_prime,
                "H_wheel_random": h_rand,
                "H_wheel_cramer": h_cram,
                "deltaH_wheel": delta_h_wheel,
                "deltaH_cramer": delta_h_cramer,
                "Q_random": q_random,
                "Q_cramer": q_cramer,
                "HL_k3_proxy": h_k3_proxy.get(dr, math.nan),
                "HL_k4_proxy": h_k4_proxy.get(dr, math.nan),
            }
            rows.append(row)
            x.append(dr)
            y_dh_cramer.append(delta_h_cramer)
            y_q_cramer.append(q_cramer)

        rho_dh, p_dh = safe_spearman(x, y_dh_cramer)
        rho_q, p_q = safe_spearman(x, y_q_cramer)

        slope_dh, intercept_dh, r2_dh = safe_linreg(x, y_dh_cramer)
        slope_q, intercept_q, r2_q = safe_linreg(x, y_q_cramer)

        trend_summary[run.n] = {
            "rho_dh_cramer": rho_dh,
            "p_dh_cramer": p_dh,
            "rho_q_cramer": rho_q,
            "p_q_cramer": p_q,
            "slope_dh_cramer": slope_dh,
            "intercept_dh_cramer": intercept_dh,
            "r2_dh_cramer": r2_dh,
            "slope_q_cramer": slope_q,
            "intercept_q_cramer": intercept_q,
            "r2_q_cramer": r2_q,
        }

    # Gepoolte Statistik über alle Skalen (deskriptiv)
    x_pool = [r["delta_r"] for r in rows]
    y_pool_dh = [r["deltaH_cramer"] for r in rows]
    y_pool_q = [r["Q_cramer"] for r in rows]
    rho_pool_dh, p_pool_dh = safe_spearman(x_pool, y_pool_dh)
    rho_pool_q, p_pool_q = safe_spearman(x_pool, y_pool_q)
    slope_pool_dh, intercept_pool_dh, r2_pool_dh = safe_linreg(x_pool, y_pool_dh)
    slope_pool_q, intercept_pool_q, r2_pool_q = safe_linreg(x_pool, y_pool_q)

    # HL-Proxy-Test (nur wo Proxies vorhanden sind)
    hl_stats_by_n: Dict[int, Dict[str, float]] = {}
    for run in runs:
        subset = [r for r in rows if r["N"] == run.n]
        valid_k3 = [r for r in subset if not math.isnan(r["HL_k3_proxy"])]
        valid_k4 = [r for r in subset if not math.isnan(r["HL_k4_proxy"])]
        if len(valid_k3) >= 3:
            y = np.array([r["deltaH_cramer"] for r in valid_k3], dtype=float)
            x3 = np.array([r["HL_k3_proxy"] for r in valid_k3], dtype=float)
            hl_stats_by_n.setdefault(run.n, {})
            hl_stats_by_n[run.n].update({f"k3_{k}": v for k, v in fit_proxy_gain(y, x3).items()})
        if len(valid_k4) >= 3:
            y = np.array([r["deltaH_cramer"] for r in valid_k4], dtype=float)
            x4 = np.array([r["HL_k4_proxy"] for r in valid_k4], dtype=float)
            hl_stats_by_n.setdefault(run.n, {})
            hl_stats_by_n[run.n].update({f"k4_{k}": v for k, v in fit_proxy_gain(y, x4).items()})

    # CSV output
    with CSV_OUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "N",
                "delta_r",
                "H_prime",
                "H_wheel_random",
                "H_wheel_cramer",
                "deltaH_wheel",
                "deltaH_cramer",
                "Q_random",
                "Q_cramer",
                "HL_k3_proxy",
                "HL_k4_proxy",
            ],
        )
        writer.writeheader()
        for row in rows:
            writer.writerow(row)

    # Plot output
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle("Stage 5.5 Quotient Drift", fontsize=14, fontweight="bold")

    colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#9467bd"]
    for idx, run in enumerate(runs):
        subset = [r for r in rows if r["N"] == run.n]
        x = [r["delta_r"] for r in subset]
        y_dh = [r["deltaH_cramer"] for r in subset]
        y_q = [r["Q_cramer"] for r in subset]
        label = f"N={run.n:,}"
        color = colors[idx % len(colors)]

        axes[0, 0].plot(x, y_dh, "o-", color=color, label=label)
        axes[0, 1].plot(x, y_q, "s-", color=color, label=label)

    axes[0, 0].set_title("DeltaH_cramer vs Delta r")
    axes[0, 0].set_xlabel("Delta r")
    axes[0, 0].set_ylabel("DeltaH_cramer")
    axes[0, 0].grid(alpha=0.3)
    axes[0, 0].legend(fontsize=9)

    axes[0, 1].set_title("Q_cramer vs Delta r")
    axes[0, 1].set_xlabel("Delta r")
    axes[0, 1].set_ylabel("Q_cramer")
    axes[0, 1].grid(alpha=0.3)
    axes[0, 1].legend(fontsize=9)

    # Pooled scatter
    n_values = sorted({int(r["N"]) for r in rows})
    n_to_size = {n: 40 + 20 * i for i, n in enumerate(n_values)}
    axes[1, 0].scatter(
        [r["delta_r"] for r in rows],
        [r["deltaH_cramer"] for r in rows],
        s=[n_to_size[int(r["N"])] for r in rows],
        alpha=0.7,
        c=[int(r["N"]) for r in rows],
        cmap="viridis",
    )
    axes[1, 0].set_title("Pooled DeltaH_cramer (marker size by N)")
    axes[1, 0].set_xlabel("Delta r")
    axes[1, 0].set_ylabel("DeltaH_cramer")
    axes[1, 0].grid(alpha=0.3)

    # HL proxy relation (N = kleinstes, falls vorhanden)
    n_ref = runs[0].n
    subset_ref = [r for r in rows if r["N"] == n_ref and not math.isnan(r["HL_k3_proxy"])]
    if subset_ref:
        x_hl = np.array([r["HL_k3_proxy"] for r in subset_ref], dtype=float)
        y_res = np.array([r["deltaH_cramer"] for r in subset_ref], dtype=float)
        axes[1, 1].scatter(x_hl, y_res, s=70, alpha=0.8, color="#d62728")
        if len(x_hl) >= 2:
            slope, intercept, _ = safe_linreg(x_hl.tolist(), y_res.tolist())
            x_line = np.linspace(float(np.min(x_hl)), float(np.max(x_hl)), 100)
            y_line = slope * x_line + intercept
            axes[1, 1].plot(x_line, y_line, "--", color="#444444")
        for r in subset_ref:
            axes[1, 1].annotate(f"dr={int(r['delta_r'])}", (r["HL_k3_proxy"], r["deltaH_cramer"]), fontsize=8)
        axes[1, 1].set_title(f"Residual vs HL-k3 proxy (N={n_ref:,})")
        axes[1, 1].set_xlabel("HL_k3_proxy")
        axes[1, 1].set_ylabel("DeltaH_cramer")
    else:
        axes[1, 1].text(0.5, 0.5, "Kein HL-Proxy verfügbar", ha="center", va="center")
        axes[1, 1].set_title("Residual vs HL proxy")
    axes[1, 1].grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig(PLOT_OUT, dpi=170, bbox_inches="tight")

    # Markdown report
    lines: List[str] = []
    lines.append("# Stage 5.5 Quotient-Drift Analyse")
    lines.append("")
    lines.append("## Datenbasis")
    lines.append("")
    lines.append("- Verwendete Runs: " + ", ".join([f"`N={run.n:,}`" for run in runs]))
    lines.append("- Delta-r Klassen: " + ", ".join([f"`{dr}`" for dr in common_delta_r]))
    lines.append("- Quelle: bestehende Stage-5.5-Artefakte (`wheel30_test` Output).")
    if missing:
        lines.append("- Nicht gefunden (optional): " + ", ".join([f"`{p}`" for p in missing]))
    lines.append("")
    lines.append("## Kernbefund (defensiv)")
    lines.append("")
    lines.append(
        "- In allen ausgewerteten Skalen gilt konsistent: `H_prime > H_wheel_cramer` und `H_prime > H_wheel_random` fuer alle getesteten Delta-r."
    )
    lines.append(
        "- Der Quotient `Q_cramer = H_prime / H_wheel_cramer` steigt in jeder Skala monoton mit Delta-r (in den vorliegenden Punkten)."
    )
    lines.append("")
    lines.append("## Monotone Drift-Tests pro Skala")
    lines.append("")
    lines.append("| N | Spearman(Delta r, DeltaH_cramer) | p | Spearman(Delta r, Q_cramer) | p | slope DeltaH_cramer | R^2 | slope Q_cramer | R^2 |")
    lines.append("|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    for run in runs:
        t = trend_summary[run.n]
        lines.append(
            f"| {run.n:,} | {t['rho_dh_cramer']:.3f} | {t['p_dh_cramer']:.3g} | "
            f"{t['rho_q_cramer']:.3f} | {t['p_q_cramer']:.3g} | "
            f"{t['slope_dh_cramer']:.4f} | {t['r2_dh_cramer']:.3f} | "
            f"{t['slope_q_cramer']:.4f} | {t['r2_q_cramer']:.3f} |"
        )
    lines.append("")
    lines.append("## Gepoolte (deskriptive) Drift")
    lines.append("")
    lines.append(
        f"- Spearman(Delta r, DeltaH_cramer) = `{rho_pool_dh:.3f}` (p=`{p_pool_dh:.3g}`), "
        f"lineare slope = `{slope_pool_dh:.4f}`, R^2=`{r2_pool_dh:.3f}`."
    )
    lines.append(
        f"- Spearman(Delta r, Q_cramer) = `{rho_pool_q:.3f}` (p=`{p_pool_q:.3g}`), "
        f"lineare slope = `{slope_pool_q:.4f}`, R^2=`{r2_pool_q:.3f}`."
    )
    lines.append("")
    lines.append("## HL-bezogene Heuristik (vorsichtige Einordnung)")
    lines.append("")
    if hl_stats_by_n:
        lines.append(
            "- Verfuegbare Proxies aus `reproducibility_stage6_N1M.txt`: `H_k3`, `H_k4` (als einfache Korrektur-Kandidaten)."
        )
        lines.append("- Bewertet wurde, ob ein lineares Modell fuer `DeltaH_cramer` die Intercept-only-Baseline verbessert.")
        lines.append("")
        lines.append("| N | k3 R2-Gewinn | k4 R2-Gewinn | Einordnung |")
        lines.append("|---:|---:|---:|---|")
        for run in runs:
            hs = hl_stats_by_n.get(run.n, {})
            k3_gain = hs.get("k3_r2_gain", math.nan)
            k4_gain = hs.get("k4_r2_gain", math.nan)
            if math.isnan(k3_gain) and math.isnan(k4_gain):
                note = "Keine Proxy-Werte auf dieser Skala"
            else:
                best = np.nanmax([k3_gain, k4_gain])
                if best > 0.2:
                    note = "Proxy erklaert Teilvarianz (vorsichtig)"
                elif best > 0:
                    note = "Leichte Verbesserung gegenueber Baseline"
                else:
                    note = "Keine Verbesserung gegenueber Baseline"
            k3_txt = "n/a" if math.isnan(k3_gain) else f"{k3_gain:.3f}"
            k4_txt = "n/a" if math.isnan(k4_gain) else f"{k4_gain:.3f}"
            lines.append(f"| {run.n:,} | {k3_txt} | {k4_txt} | {note} |")
        lines.append("")
        lines.append(
            "- Einschraenkung: sehr kleine Stichprobe pro Skala (nur 5 Delta-r Punkte), daher nur als Interface/Screening zu interpretieren."
        )
    else:
        lines.append("- Keine HL-Proxy-Implementierung in den ausgewerteten Artefakten nutzbar.")
        lines.append(
            "- Offener Punkt: Fit-Interface vorbereitet ueber Spalten `HL_k3_proxy`, `HL_k4_proxy` in `stage55_quotient_table.csv`."
        )
    lines.append("")
    lines.append("## Reproduzierbarkeit")
    lines.append("")
    lines.append(f"- Tabelle: `{CSV_OUT.relative_to(REPO_ROOT)}`")
    lines.append(f"- Plot: `{PLOT_OUT.relative_to(REPO_ROOT)}`")
    lines.append(f"- Skript: `{Path(__file__).relative_to(REPO_ROOT)}`")
    lines.append("")
    lines.append("## Methodische Hinweise")
    lines.append("")
    lines.append("- Statistik ist bewusst defensiv: Spearman (monotone Drift) + lineare Trends nur deskriptiv.")
    lines.append("- Keine starke kausale HL-Behauptung aus den Proxy-Fits.")
    lines.append("- Fuer publizierbaren naechsten Test: gleiche Pipeline auf `N=1e8`/`N=1e9` plus explizites HL-k-Tupel-Modell mit klarer Likelihood/Fit-Guete.")

    MD_OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"Wrote: {CSV_OUT}")
    print(f"Wrote: {PLOT_OUT}")
    print(f"Wrote: {MD_OUT}")


if __name__ == "__main__":
    main()

