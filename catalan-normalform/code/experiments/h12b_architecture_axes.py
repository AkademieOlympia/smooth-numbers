"""
H12-B: Architekturachsen für M_C(n)
===================================

Ziel:
Teste die Hypothese, dass M_C primär eine Funktion der Faktorisierungs-
architektur (Baumgeometrie) ist und weniger von Entropie/Schale abhängt.

Erfasste Größen pro n:
- M_C(n): Catalan-Magic (depth-Metrik, balanced-Kanonisierung)
- Ω(n): Anzahl Primfaktoren mit Vielfachheit
- S(n): v2(n) + v3(n) (Shell)
- H(n): EABC-Konzentration aus utils.eabc.compute_H
- L(n): Signaturlänge der EABC-Signatur (projektkonsistent wie comparison_n1_100:
        Faktorenklassen-String mit 2/3 als "E")
- D(n): mittlere Blatttiefe des kanonischen Faktorisierungsbaums
- B(n): normierter Colless-Index als Balance-Metrik

Statistik:
- Pearson + Spearman: M_C vs {H, L, D, B, Ω, S}
- R² einfacher linearer Modelle M_C ~ X
- Partielle Residuenkorrelationen corr(M_C^⊥, X^⊥ | Ω)
- Optional multivariat: M_C ~ Ω + H + L + D + B inkl. inkrementellem ΔR²
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple
import argparse
import json
import time

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

from catalan_trees import BinaryTree
from utils.eabc import compute_svn_coordinates, prime_factors_with_multiplicity, eabc_class
from utils.catalan_magic import compute_catalan_magic
from utils.canonization import canonize_number


FEATURE_ORDER = ["H", "L", "D", "B", "omega", "S"]
MULTIVARIATE_ORDER = ["omega", "H", "L", "D", "B"]
REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT_DIR = REPO_ROOT / "experiments" / "results" / "h12"


@dataclass
class FeatureStats:
    n: int
    pearson_r: float
    pearson_p: float
    spearman_rho: float
    spearman_p: float
    r2: float
    beta: float
    intercept: float
    partial_r_given_omega: float
    partial_p_given_omega: float


def eabc_signature_project_consistent(n: int) -> str:
    """
    Projektkonsistente EABC-Signatur analog zu comparison_n1_100.py:
    - Primfaktoren mit Vielfachheit
    - 2 und 3 werden als "E" kodiert
    """
    factors = prime_factors_with_multiplicity(n)
    signature = []
    for p in factors:
        if p == 2 or p == 3:
            signature.append("E")
        else:
            cls = eabc_class(p)
            signature.append(cls if cls in {"E", "A", "B", "C"} else "?")
    return "".join(signature)


def leaf_depths(tree: BinaryTree, depth: int = 0) -> List[int]:
    if tree.is_leaf:
        return [depth]
    depths = []
    if tree.left is not None:
        depths.extend(leaf_depths(tree.left, depth + 1))
    if tree.right is not None:
        depths.extend(leaf_depths(tree.right, depth + 1))
    return depths


def normalized_colless(n: int, omega: int) -> float:
    raw = compute_catalan_magic(n, method="balanced", metric="colless")
    max_imbalance = (omega - 1) * (omega - 2) / 2 if omega > 2 else 1.0
    return float(raw / max_imbalance) if max_imbalance > 0 else 0.0


def compute_record(n: int) -> Dict[str, float]:
    coords = compute_svn_coordinates(n)
    omega = int(coords["omega"])
    S = int(coords["v2"] + coords["v3"])
    H = float(coords["H"])

    tree = canonize_number(n, method="balanced")
    depths = leaf_depths(tree)
    D = float(np.mean(depths)) if depths else np.nan

    signature = eabc_signature_project_consistent(n)
    L = float(len(signature))

    M_C = float(compute_catalan_magic(n, method="balanced", metric="depth"))
    B = normalized_colless(n, omega)

    return {
        "n": n,
        "M_C": M_C,
        "omega": float(omega),
        "S": float(S),
        "H": H,
        "L": L,
        "D": D,
        "B": B,
    }


def correlation_summary(y: np.ndarray, x: np.ndarray, omega: np.ndarray, feature_name: str) -> FeatureStats:
    mask = np.isfinite(y) & np.isfinite(x) & np.isfinite(omega)
    yv = y[mask]
    xv = x[mask]
    ov = omega[mask]
    n = len(yv)

    if n < 3:
        return FeatureStats(n, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan)

    pearson_r, pearson_p = stats.pearsonr(yv, xv)
    spearman_rho, spearman_p = stats.spearmanr(yv, xv)

    model = LinearRegression().fit(xv.reshape(-1, 1), yv)
    pred = model.predict(xv.reshape(-1, 1))
    r2 = r2_score(yv, pred)

    if feature_name == "omega":
        partial_r = np.nan
        partial_p = np.nan
    else:
        model_y = LinearRegression().fit(ov.reshape(-1, 1), yv)
        model_x = LinearRegression().fit(ov.reshape(-1, 1), xv)
        y_perp = yv - model_y.predict(ov.reshape(-1, 1))
        x_perp = xv - model_x.predict(ov.reshape(-1, 1))
        if np.std(y_perp) < 1e-12 or np.std(x_perp) < 1e-12:
            partial_r, partial_p = np.nan, np.nan
        else:
            partial_r, partial_p = stats.pearsonr(y_perp, x_perp)

    return FeatureStats(
        n=n,
        pearson_r=float(pearson_r),
        pearson_p=float(pearson_p),
        spearman_rho=float(spearman_rho),
        spearman_p=float(spearman_p),
        r2=float(r2),
        beta=float(model.coef_[0]),
        intercept=float(model.intercept_),
        partial_r_given_omega=float(partial_r) if np.isfinite(partial_r) else np.nan,
        partial_p_given_omega=float(partial_p) if np.isfinite(partial_p) else np.nan,
    )


def run_multivariate(df: pd.DataFrame) -> Dict:
    cols = ["M_C"] + MULTIVARIATE_ORDER
    work = df[cols].dropna()
    if len(work) < 20:
        return {"enabled": False, "reason": "Zu wenige vollständige Beobachtungen", "n": int(len(work))}

    X_full = work[MULTIVARIATE_ORDER].values
    y = work["M_C"].values
    model_full = LinearRegression().fit(X_full, y)
    r2_full = r2_score(y, model_full.predict(X_full))

    increments = []
    prev_r2 = 0.0
    for i in range(1, len(MULTIVARIATE_ORDER) + 1):
        sub = MULTIVARIATE_ORDER[:i]
        model_i = LinearRegression().fit(work[sub].values, y)
        r2_i = r2_score(y, model_i.predict(work[sub].values))
        increments.append({
            "model": "M_C ~ " + " + ".join(sub),
            "r2": float(r2_i),
            "delta_r2": float(r2_i - prev_r2),
        })
        prev_r2 = r2_i

    return {
        "enabled": True,
        "n": int(len(work)),
        "r2_full": float(r2_full),
        "coefficients": {k: float(v) for k, v in zip(MULTIVARIATE_ORDER, model_full.coef_)},
        "intercept": float(model_full.intercept_),
        "increments": increments,
    }


def markdown_report(
    n_max: int,
    n_samples: int,
    elapsed_s: float,
    stats_map: Dict[str, FeatureStats],
    multivariate: Dict
) -> str:
    ranked = sorted(
        stats_map.items(),
        key=lambda kv: abs(kv[1].pearson_r) if np.isfinite(kv[1].pearson_r) else -1.0,
        reverse=True
    )
    top3 = ranked[:3]

    lines = []
    lines.append("# H12-B Architekturachsen für M_C")
    lines.append("")
    lines.append(f"- **Datum:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"- **Datensatz:** n in [2, {n_max:,}] mit Ω(n) >= 2")
    lines.append(f"- **Samples:** {n_samples:,}")
    lines.append(f"- **Laufzeit:** {elapsed_s:.2f} s")
    lines.append("")
    lines.append("## Definitionen (projektkonsistent)")
    lines.append("")
    lines.append("- **M_C(n):** `compute_catalan_magic(n, method='balanced', metric='depth')`")
    lines.append("- **Ω(n):** Anzahl Primfaktoren mit Vielfachheit (`compute_svn_coordinates`)")
    lines.append("- **S(n):** `v2(n) + v3(n)` (Shell)")
    lines.append("- **H(n):** Konzentration aus `utils.eabc.compute_H`")
    lines.append("- **L(n):** Länge der EABC-Signatur (wie in `comparison_n1_100`: 2/3 als `E` kodiert)")
    lines.append("- **D(n):** mittlere Blatttiefe des balancierten Faktorisierungsbaums")
    lines.append("- **B(n):** normierter Colless-Index des balancierten Faktorisierungsbaums")
    lines.append("")
    lines.append("## Bivariate Tests M_C vs X")
    lines.append("")
    lines.append("| X | n | Pearson r | Spearman rho | R²(M_C~X) | part. r \\| Ω |")
    lines.append("|---|---:|---:|---:|---:|---:|")
    for name in FEATURE_ORDER:
        s = stats_map[name]
        pr = "nan" if not np.isfinite(s.pearson_r) else f"{s.pearson_r:+.6f}"
        sr = "nan" if not np.isfinite(s.spearman_rho) else f"{s.spearman_rho:+.6f}"
        r2v = "nan" if not np.isfinite(s.r2) else f"{s.r2:.6f}"
        par = "n/a" if not np.isfinite(s.partial_r_given_omega) else f"{s.partial_r_given_omega:+.6f}"
        lines.append(f"| {name} | {s.n:,} | {pr} | {sr} | {r2v} | {par} |")
    lines.append("")
    lines.append("## Top-3 stärkste bivariate Zusammenhänge (|Pearson|)")
    lines.append("")
    for i, (name, s) in enumerate(top3, start=1):
        lines.append(f"{i}. `{name}`: r={s.pearson_r:+.6f}, rho={s.spearman_rho:+.6f}, R²={s.r2:.6f}")
    lines.append("")
    lines.append("## Methodische Einordnung")
    lines.append("")

    d_abs = abs(stats_map["D"].pearson_r) if np.isfinite(stats_map["D"].pearson_r) else 0.0
    b_abs = abs(stats_map["B"].pearson_r) if np.isfinite(stats_map["B"].pearson_r) else 0.0
    h_abs = abs(stats_map["H"].pearson_r) if np.isfinite(stats_map["H"].pearson_r) else 0.0
    s_abs = abs(stats_map["S"].pearson_r) if np.isfinite(stats_map["S"].pearson_r) else 0.0

    if (d_abs + b_abs) > (h_abs + s_abs):
        lines.append("- Die Daten stützen die Arbeitshypothese: Architekturachsen (`D`, `B`) sind insgesamt näher an `M_C` als Entropie-/Shell-Achsen.")
    else:
        lines.append("- Die Daten stützen die Arbeitshypothese nicht klar: Entropie-/Shell-Achsen sind nicht eindeutig schwächer als Architekturachsen.")

    lines.append("- Hinweis zu `L`: Mit der projektkonsistenten Definition (Signaturlänge) ist `L` in diesem Setup effektiv gleich `Ω`; entsprechend ist der inkrementelle Beitrag von `L` nach `Ω` nahe null.")
    lines.append("- Zur vorgeschlagenen Reihenfolge `M_C -> H -> L -> M_{C,EABC}`: als heuristische Ordnung plausibel, aber nur deskriptiv belegt.")
    lines.append("- Limitationen: lineare Modelle, eine Kanonisierung (`balanced`), bivariate Auswertung ohne kausale Interpretation.")
    lines.append("")

    if multivariate.get("enabled"):
        lines.append("## Optionales multivariates Modell")
        lines.append("")
        lines.append(f"- **Modell:** `M_C ~ Ω + H + L + D + B`")
        lines.append(f"- **n:** {multivariate['n']:,}")
        lines.append(f"- **R² voll:** {multivariate['r2_full']:.6f}")
        lines.append("")
        lines.append("| Modell | R² | ΔR² |")
        lines.append("|---|---:|---:|")
        for row in multivariate["increments"]:
            lines.append(f"| {row['model']} | {row['r2']:.6f} | {row['delta_r2']:.6f} |")
        lines.append("")
    else:
        lines.append("## Optionales multivariates Modell")
        lines.append("")
        lines.append(f"- Nicht berechnet: {multivariate.get('reason', 'unbekannt')}")
        lines.append("")

    return "\n".join(lines)


def create_plots(df: pd.DataFrame, stats_map: Dict[str, FeatureStats], output_file: Path) -> None:
    fig, axes = plt.subplots(2, 3, figsize=(18, 11))
    fig.suptitle("H12-B: M_C vs Architektur-/Informationsachsen", fontsize=16, fontweight="bold")

    plotted = ["D", "B", "H", "S", "L", "omega"]
    colors = {
        "D": "tab:blue",
        "B": "tab:orange",
        "H": "tab:green",
        "S": "tab:red",
        "L": "tab:purple",
        "omega": "tab:brown",
    }

    for ax, feature in zip(axes.flat, plotted):
        work = df[["M_C", feature]].dropna()
        if len(work) == 0:
            ax.text(0.5, 0.5, f"Keine Daten für {feature}", ha="center", va="center", transform=ax.transAxes)
            continue

        x = work[feature].values
        y = work["M_C"].values
        ax.scatter(x, y, s=8, alpha=0.25, color=colors[feature])

        if len(work) > 2:
            model = LinearRegression().fit(x.reshape(-1, 1), y)
            x_grid = np.linspace(np.min(x), np.max(x), 150)
            y_grid = model.predict(x_grid.reshape(-1, 1))
            ax.plot(x_grid, y_grid, color="black", linewidth=1.5)

        st = stats_map[feature]
        pr = st.pearson_r if np.isfinite(st.pearson_r) else np.nan
        r2v = st.r2 if np.isfinite(st.r2) else np.nan
        ax.set_title(f"M_C vs {feature}\nr={pr:+.3f}, R²={r2v:.3f}")
        ax.set_xlabel(feature)
        ax.set_ylabel("M_C")
        ax.grid(alpha=0.25)

    plt.tight_layout()
    output_file.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_file, dpi=180, bbox_inches="tight")
    plt.close(fig)


def run_experiment(
    n_max: int = 100000,
    output_dir: str = str(DEFAULT_OUTPUT_DIR)
) -> Dict:
    t0 = time.time()
    out = Path(output_dir)
    if not out.is_absolute():
        out = (REPO_ROOT / out).resolve()
    out.mkdir(parents=True, exist_ok=True)

    print("=" * 80)
    print("H12-B: ARCHITEKTURACHSEN FÜR M_C")
    print("=" * 80)
    print(f"Berechne n in [2, {n_max:,}] mit Ω(n) >= 2 ...")

    records = []
    for n in range(2, n_max + 1):
        omega = len(prime_factors_with_multiplicity(n))
        if omega < 2:
            continue
        records.append(compute_record(n))
        if len(records) % 2000 == 0:
            print(f"  {len(records):,} Samples ...")

    df = pd.DataFrame(records)
    print(f"Fertig: {len(df):,} Samples")

    y = df["M_C"].values
    omega = df["omega"].values

    stats_map: Dict[str, FeatureStats] = {}
    for feature in FEATURE_ORDER:
        stats_map[feature] = correlation_summary(y, df[feature].values, omega, feature)

    multivariate = run_multivariate(df)

    csv_file = out / "h12b_results.csv"
    df.to_csv(csv_file, index=False)
    print(f"CSV gespeichert: {csv_file}")

    plot_file = out / "h12b_plots.png"
    create_plots(df, stats_map, plot_file)
    print(f"Plots gespeichert: {plot_file}")

    elapsed = time.time() - t0
    report = markdown_report(
        n_max=n_max,
        n_samples=len(df),
        elapsed_s=elapsed,
        stats_map=stats_map,
        multivariate=multivariate,
    )
    report_file = out / "H12B_ARCHITECTURE_AXES.md"
    report_file.write_text(report, encoding="utf-8")
    print(f"Report gespeichert: {report_file}")

    summary = {
        "test": "H12-B",
        "timestamp": datetime.now().isoformat(),
        "n_max": int(n_max),
        "n_samples": int(len(df)),
        "elapsed_seconds": float(elapsed),
        "features": {
            k: {
                "n": int(v.n),
                "pearson_r": float(v.pearson_r) if np.isfinite(v.pearson_r) else None,
                "pearson_p": float(v.pearson_p) if np.isfinite(v.pearson_p) else None,
                "spearman_rho": float(v.spearman_rho) if np.isfinite(v.spearman_rho) else None,
                "spearman_p": float(v.spearman_p) if np.isfinite(v.spearman_p) else None,
                "r2": float(v.r2) if np.isfinite(v.r2) else None,
                "partial_r_given_omega": float(v.partial_r_given_omega) if np.isfinite(v.partial_r_given_omega) else None,
                "partial_p_given_omega": float(v.partial_p_given_omega) if np.isfinite(v.partial_p_given_omega) else None,
            }
            for k, v in stats_map.items()
        },
        "multivariate": multivariate,
        "artifacts": {
            "csv": str(csv_file),
            "plot": str(plot_file),
            "report": str(report_file),
        },
    }

    summary_file = out / "h12b_summary.json"
    with summary_file.open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    print(f"Summary gespeichert: {summary_file}")

    print("=" * 80)
    print("H12-B ABGESCHLOSSEN")
    print("=" * 80)

    return summary


def main():
    parser = argparse.ArgumentParser(description="H12-B Architekturachsen-Test für M_C")
    parser.add_argument("--n-max", type=int, default=100000, help="Maximales n")
    parser.add_argument(
        "--output",
        type=str,
        default=str(DEFAULT_OUTPUT_DIR),
        help="Ausgabeverzeichnis",
    )
    args = parser.parse_args()
    run_experiment(n_max=args.n_max, output_dir=args.output)


if __name__ == "__main__":
    main()
