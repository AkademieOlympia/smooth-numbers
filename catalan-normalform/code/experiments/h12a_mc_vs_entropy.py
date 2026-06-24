"""
H12-A: M_C vs. EABC-Shannon-Entropie
====================================

Zentrale Testfrage:
Korrelieren Catalan-Magic-Asymmetrie M_C(n) und EABC-Strukturkomplexität E(n)
stärker als M_C(n) und Schale S(n) = v2(n)+v3(n)?

Definitionen:
  - M_C(n): tree-depth imbalance aus balanced-Kanonisierung.
  - E(n)   : Shannon-Entropie der EABC-Verteilung (mit Multiplizität),
             E(n) = - sum_x p_x log(p_x), x in {E,A,B,C},
             p_x = count_x / (e+a+b+c), nur p>3 in EABC.
  - S(n)   : v2(n) + v3(n), wie in H10.
  - Omega  : Anzahl Primfaktoren mit Multiplizität.

Methodik:
  - n in [2, n_max], gefiltert auf Omega(n) >= 2.
  - Gültige Entropieproben: e+a+b+c > 0.
  - Reproduzierbare deterministische Berechnung.
"""

import argparse
import json
import os
import re
import sys
import time
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, Tuple

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from utils.catalan_magic import compute_catalan_magic
from utils.eabc import compute_svn_coordinates, count_prime_factors
from utils.eabc_test_data import EABCTestData


@dataclass
class RegressionStats:
    slope: float
    intercept: float
    r2: float
    r: float
    p_value: float
    slope_ci_low: float
    slope_ci_high: float


def shannon_entropy_from_counts(e: int, a: int, b: int, c: int) -> float:
    """Shannon-Entropie aus EABC-Zaehlungen mit natuerlichem Logarithmus."""
    counts = np.array([e, a, b, c], dtype=float)
    total = counts.sum()
    if total <= 0:
        return np.nan
    probs = counts[counts > 0.0] / total
    return float(-np.sum(probs * np.log(probs)))


def fit_simple_regression(y: np.ndarray, x: np.ndarray, alpha: float = 0.05) -> RegressionStats:
    """Einfache lineare Regression y ~ x via scipy mit Konfidenzintervall."""
    reg = stats.linregress(x, y)
    r2 = float(reg.rvalue ** 2)

    n = len(x)
    if n > 2 and np.isfinite(reg.stderr):
        tcrit = stats.t.ppf(1 - alpha / 2, df=n - 2)
        delta = tcrit * reg.stderr
        ci_low = float(reg.slope - delta)
        ci_high = float(reg.slope + delta)
    else:
        ci_low = np.nan
        ci_high = np.nan

    return RegressionStats(
        slope=float(reg.slope),
        intercept=float(reg.intercept),
        r2=r2,
        r=float(reg.rvalue),
        p_value=float(reg.pvalue),
        slope_ci_low=ci_low,
        slope_ci_high=ci_high,
    )


def residual_correlation(y: np.ndarray, x1: np.ndarray, x_control: np.ndarray) -> Tuple[float, float]:
    """
    Korrelation zwischen Residuen:
      y_perp = y - E[y|control], x1_perp = x1 - E[x1|control].
    """
    y_fit = fit_simple_regression(y, x_control)
    x_fit = fit_simple_regression(x1, x_control)

    y_res = y - (y_fit.intercept + y_fit.slope * x_control)
    x_res = x1 - (x_fit.intercept + x_fit.slope * x_control)
    pearson = stats.pearsonr(y_res, x_res)
    return float(pearson.statistic), float(pearson.pvalue)


def read_h10_reference_metrics(repo_root: Path) -> Dict[str, Optional[float]]:
    """
    Liest H10-Referenzwerte ein (falls vorhanden), ohne harte Abhaengigkeit.
    Erwartet:
      - h10_delta_r2_test.csv fuer R2(S~Omega) und R2(S~Omega+MC)
      - H10_RESULTS.md fuer Residuenkorrelation (rho(Residuen M1, M_C))
    """
    out: Dict[str, Optional[float]] = {
        "h10_r2_m1": None,
        "h10_r2_m2": None,
        "h10_delta_r2": None,
        "h10_residual_corr_mc_s_given_omega": None,
    }

    csv_path = repo_root / "experiments" / "results" / "h10" / "h10_delta_r2_test.csv"
    if csv_path.exists():
        df = pd.read_csv(csv_path)
        row_m1 = df[df["model"] == "M1"]
        row_m2 = df[df["model"] == "M2"]
        if not row_m1.empty and not row_m2.empty:
            r2_m1 = float(row_m1.iloc[0]["R2"])
            r2_m2 = float(row_m2.iloc[0]["R2"])
            out["h10_r2_m1"] = r2_m1
            out["h10_r2_m2"] = r2_m2
            out["h10_delta_r2"] = r2_m2 - r2_m1

    md_path = repo_root / "experiments" / "results" / "h10" / "H10_RESULTS.md"
    if md_path.exists():
        text = md_path.read_text(encoding="utf-8")
        m = re.search(r"ρ\(Residuen M1, M_C\)\s*=\s*([+-]?\d+(?:\.\d+)?)", text)
        if m:
            out["h10_residual_corr_mc_s_given_omega"] = float(m.group(1))

    return out


def collect_dataset(n_max: int, cache_file: Optional[Path] = None, progress_every: int = 5000) -> pd.DataFrame:
    """Berechnet Datensatz fuer H12-A deterministisch."""
    use_cache = cache_file is not None and cache_file.exists()
    cache_obj = EABCTestData(cache_file=cache_file, readonly=True) if use_cache else None

    rows = []
    t0 = time.time()
    total_checked = 0

    for n in range(2, n_max + 1):
        total_checked += 1
        omega_n = count_prime_factors(n)
        if omega_n < 2:
            continue

        if cache_obj is not None:
            coords = cache_obj.get_coordinates(n)
            e = int(coords["e"])
            a = int(coords["a"])
            b = int(coords["b"])
            c = int(coords["c"])
            shell = int(coords["shell"])
            omega = int(coords["omega"])
        else:
            coords = compute_svn_coordinates(n)
            e = int(coords["e"])
            a = int(coords["a"])
            b = int(coords["b"])
            c = int(coords["c"])
            shell = int(coords["v2"] + coords["v3"])
            omega = int(coords["omega"])

        entropy = shannon_entropy_from_counts(e, a, b, c)
        if np.isnan(entropy):
            continue

        mc = float(compute_catalan_magic(n, method="balanced", metric="depth"))

        rows.append(
            {
                "n": n,
                "M_C": mc,
                "E": float(entropy),
                "S": float(shell),
                "omega": float(omega),
                "e": e,
                "a": a,
                "b": b,
                "c": c,
            }
        )

        if total_checked % progress_every == 0:
            elapsed = time.time() - t0
            print(
                f"[Progress] n={n:,}/{n_max:,}, "
                f"gueltige Samples={len(rows):,}, elapsed={elapsed:,.1f}s"
            )

    if cache_obj is not None:
        cache_obj.close()

    return pd.DataFrame(rows)


def create_plots(df: pd.DataFrame, stats_dict: Dict[str, float], output_path: Path) -> None:
    """Erzeugt H12A-Plot-Grid."""
    x_e = df["E"].to_numpy()
    y_mc = df["M_C"].to_numpy()
    x_s = df["S"].to_numpy()
    x_omega = df["omega"].to_numpy()

    reg_e = fit_simple_regression(y_mc, x_e)
    reg_s = fit_simple_regression(y_mc, x_s)
    reg_omega = fit_simple_regression(y_mc, x_omega)
    corr_res_mc_e, _ = residual_correlation(y_mc, x_e, x_omega)
    corr_res_mc_s, _ = residual_correlation(y_mc, x_s, x_omega)

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle("H12-A: M_C vs EABC-Entropie", fontsize=14, fontweight="bold")

    # Panel 1: M_C vs E
    ax = axes[0, 0]
    order = np.argsort(x_e)
    ax.scatter(x_e, y_mc, s=8, alpha=0.2, color="tab:green")
    ax.plot(
        x_e[order],
        reg_e.intercept + reg_e.slope * x_e[order],
        color="black",
        linewidth=1.8,
    )
    ax.set_xlabel("E(n)")
    ax.set_ylabel("M_C(n)")
    ax.set_title(f"M_C ~ E | corr={reg_e.r:.4f}, R²={reg_e.r2:.4f}")
    ax.grid(alpha=0.25)

    # Panel 2: M_C vs S
    ax = axes[0, 1]
    order = np.argsort(x_s)
    ax.scatter(x_s, y_mc, s=8, alpha=0.2, color="tab:purple")
    ax.plot(
        x_s[order],
        reg_s.intercept + reg_s.slope * x_s[order],
        color="black",
        linewidth=1.8,
    )
    ax.set_xlabel("S(n) = v2 + v3")
    ax.set_ylabel("M_C(n)")
    ax.set_title(f"M_C ~ S | corr={reg_s.r:.4f}, R²={reg_s.r2:.4f}")
    ax.grid(alpha=0.25)

    # Panel 3: Korrelationsvergleich
    ax = axes[1, 0]
    labels = ["corr(M_C,E)", "corr(M_C,S)", "corr(M_C,Omega)"]
    vals = [
        stats_dict["corr_mc_e_pearson"],
        stats_dict["corr_mc_s_pearson"],
        stats_dict["corr_mc_omega_pearson"],
    ]
    bars = ax.bar(labels, vals, color=["tab:green", "tab:purple", "tab:blue"], alpha=0.8)
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width() / 2.0, v, f"{v:.3f}", ha="center", va="bottom", fontsize=9)
    ax.axhline(0.0, color="black", linewidth=1)
    ax.set_ylim(min(vals) - 0.08, max(vals) + 0.08)
    ax.set_title("Direkte Pearson-Korrelationen")
    ax.grid(alpha=0.25, axis="y")

    # Panel 4: Residualvergleich
    ax = axes[1, 1]
    ax.bar(
        ["corr(M_C^⊥,E^⊥|Omega)", "corr(M_C^⊥,S^⊥|Omega)"],
        [corr_res_mc_e, corr_res_mc_s],
        color=["tab:green", "tab:purple"],
        alpha=0.8,
    )
    ax.axhline(0.0, color="black", linewidth=1)
    ax.set_title("Residuen-Korrelationen nach Omega-Entfernung")
    ax.grid(alpha=0.25, axis="y")

    plt.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=180, bbox_inches="tight")
    plt.close(fig)


def write_markdown_report(
    output_md: Path,
    stats_dict: Dict[str, float],
    reg_mc_e: RegressionStats,
    reg_mc_s: RegressionStats,
    reg_mc_omega: RegressionStats,
    corr_res_mc_e: Tuple[float, float],
    corr_res_mc_s: Tuple[float, float],
    h10_ref: Dict[str, Optional[float]],
) -> None:
    """Schreibt H12A-Bericht mit methodischer Einordnung."""
    output_md.parent.mkdir(parents=True, exist_ok=True)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    res_e_corr, res_e_p = corr_res_mc_e
    res_s_corr, res_s_p = corr_res_mc_s

    h10_residual = h10_ref["h10_residual_corr_mc_s_given_omega"]
    h10_delta_r2 = h10_ref["h10_delta_r2"]
    h10_delta_r2_str = "n/a" if h10_delta_r2 is None else f"{h10_delta_r2:.6f}"
    h10_resid_str = "n/a" if h10_residual is None else f"{h10_residual:.6f}"

    support_entropy_over_s = (
        abs(stats_dict["corr_mc_e_pearson"]) > abs(stats_dict["corr_mc_s_pearson"])
        and stats_dict["r2_mc_e"] > stats_dict["r2_mc_s"]
    )

    with output_md.open("w", encoding="utf-8") as f:
        f.write("# H12-A: M_C vs. EABC-Shannon-Entropie\n\n")
        f.write(f"**Zeitpunkt:** {now}\n\n")
        f.write("## Definitionen\n\n")
        f.write("- **M_C(n):** `compute_catalan_magic(n, method='balanced', metric='depth')`\n")
        f.write("- **E(n):** `-sum_x p_x log(p_x)` mit `x in {E,A,B,C}` und `p_x = count_x / (e+a+b+c)`\n")
        f.write("- **S(n):** `v2(n) + v3(n)` (H10-konform)\n")
        f.write("- **Stichprobe:** `n in [2, n_max]`, nur `Omega(n) >= 2`, und nur Faelle mit `e+a+b+c > 0`\n\n")

        f.write("## Stichprobe und Grenzen\n\n")
        f.write(f"- Gepruefte `n`: {int(stats_dict['n_checked']):,}\n")
        f.write(f"- Gueltige H12A-Samples: {int(stats_dict['n_valid']):,}\n")
        f.write(f"- Ausschlussgrund: fehlende EABC-Masse (`e+a+b+c = 0`, nur Shell-Faktoren)\n")
        f.write("- Analyse ist beobachtend (Korrelation/Regression), keine Kausalinterpretation.\n\n")

        f.write("## Hauptergebnisse\n\n")
        f.write(f"- `corr(M_C, E)` (Pearson): **{stats_dict['corr_mc_e_pearson']:.6f}**\n")
        f.write(f"- `corr(M_C, E)` (Spearman): **{stats_dict['corr_mc_e_spearman']:.6f}**\n")
        f.write(f"- `R²(M_C ~ E)`: **{stats_dict['r2_mc_e']:.6f}**\n")
        f.write(f"- `corr(M_C, S)` (Pearson): **{stats_dict['corr_mc_s_pearson']:.6f}**\n")
        f.write(f"- `R²(M_C ~ S)`: **{stats_dict['r2_mc_s']:.6f}**\n")
        f.write(f"- `corr(M_C, Omega)`: **{stats_dict['corr_mc_omega_pearson']:.6f}**\n")
        f.write(f"- `R²(M_C ~ Omega)`: **{stats_dict['r2_mc_omega']:.6f}**\n\n")

        f.write("## Residuenvergleich nach Omega-Kontrolle\n\n")
        f.write(f"- `corr(M_C^⊥, E^⊥ | Omega)` = **{res_e_corr:.6f}** (p={res_e_p:.3e})\n")
        f.write(f"- `corr(M_C^⊥, S^⊥ | Omega)` = **{res_s_corr:.6f}** (p={res_s_p:.3e})\n")
        f.write(f"- H10-Referenz `corr(Residuen M1, M_C)` = **{h10_resid_str}** (nahe 0 erwartet)\n\n")

        f.write("## Regressionsparameter (95% CI fuer Steigung)\n\n")
        f.write("| Modell | Steigung | 95%-CI | Intercept | R² |\n")
        f.write("|---|---:|---:|---:|---:|\n")
        f.write(
            f"| `M_C ~ E` | {reg_mc_e.slope:.6f} | [{reg_mc_e.slope_ci_low:.6f}, {reg_mc_e.slope_ci_high:.6f}] | "
            f"{reg_mc_e.intercept:.6f} | {reg_mc_e.r2:.6f} |\n"
        )
        f.write(
            f"| `M_C ~ S` | {reg_mc_s.slope:.6f} | [{reg_mc_s.slope_ci_low:.6f}, {reg_mc_s.slope_ci_high:.6f}] | "
            f"{reg_mc_s.intercept:.6f} | {reg_mc_s.r2:.6f} |\n"
        )
        f.write(
            f"| `M_C ~ Omega` | {reg_mc_omega.slope:.6f} | [{reg_mc_omega.slope_ci_low:.6f}, {reg_mc_omega.slope_ci_high:.6f}] | "
            f"{reg_mc_omega.intercept:.6f} | {reg_mc_omega.r2:.6f} |\n\n"
        )

        f.write("## Vergleich zu H10\n\n")
        f.write(f"- H10: `Delta R² (S ~ Omega + M_C)` = **{h10_delta_r2_str}** (nahe 0)\n")
        f.write(f"- H10: Residuen-Korrelation `M_C` vs. `S` nach Omega-Kontrolle = **{h10_resid_str}**\n")
        f.write("- H12A ergaenzt dies durch direkten Strukturtest `M_C` vs. Entropie `E`.\n\n")

        f.write("## Interpretation (vorsichtig)\n\n")
        if support_entropy_over_s:
            f.write(
                "- In dieser Stichprobe ist der lineare Zusammenhang von `M_C` mit `E` staerker als mit `S` "
                "(nach den hier verwendeten Kennzahlen).\n"
            )
        else:
            f.write(
                "- In dieser Stichprobe ist der Zusammenhang von `M_C` mit `E` nicht staerker als mit `S` "
                "(nach den hier verwendeten Kennzahlen).\n"
            )
        f.write(
            "- Die Effekte sind korrelativ; sie zeigen Assoziationen, aber keine kausale Mechanik.\n"
        )
        f.write(
            "- Aussagegueltigkeit ist auf die gewaehlte Stichprobe und die aktuelle M_C-Definition begrenzt.\n"
        )


def run_h12a(n_max: int, output_dir: Path, cache_file: Optional[Path]) -> Dict[str, float]:
    """Fuehrt H12-A komplett aus."""
    t0 = time.time()
    output_dir.mkdir(parents=True, exist_ok=True)
    repo_root = Path(__file__).resolve().parents[2]

    print("=" * 80)
    print("H12-A: M_C vs EABC-Entropie")
    print("=" * 80)
    print(f"n_max={n_max:,}")
    print(f"Output={output_dir}")
    print(f"Cache={cache_file if cache_file else 'none'}")
    print()

    df = collect_dataset(n_max=n_max, cache_file=cache_file)
    if df.empty:
        raise RuntimeError("Keine gueltigen Samples erzeugt.")

    x_e = df["E"].to_numpy()
    y_mc = df["M_C"].to_numpy()
    x_s = df["S"].to_numpy()
    x_omega = df["omega"].to_numpy()

    pearson_e = stats.pearsonr(y_mc, x_e)
    pearson_s = stats.pearsonr(y_mc, x_s)
    pearson_omega = stats.pearsonr(y_mc, x_omega)
    spearman_e = stats.spearmanr(y_mc, x_e)

    reg_mc_e = fit_simple_regression(y_mc, x_e)
    reg_mc_s = fit_simple_regression(y_mc, x_s)
    reg_mc_omega = fit_simple_regression(y_mc, x_omega)

    corr_res_mc_e = residual_correlation(y_mc, x_e, x_omega)
    corr_res_mc_s = residual_correlation(y_mc, x_s, x_omega)

    stats_dict: Dict[str, float] = {
        "timestamp": datetime.now().isoformat(),
        "n_max": float(n_max),
        "n_checked": float(n_max - 1),
        "n_valid": float(len(df)),
        "corr_mc_e_pearson": float(pearson_e.statistic),
        "p_mc_e_pearson": float(pearson_e.pvalue),
        "corr_mc_e_spearman": float(spearman_e.statistic),
        "p_mc_e_spearman": float(spearman_e.pvalue),
        "corr_mc_s_pearson": float(pearson_s.statistic),
        "p_mc_s_pearson": float(pearson_s.pvalue),
        "corr_mc_omega_pearson": float(pearson_omega.statistic),
        "p_mc_omega_pearson": float(pearson_omega.pvalue),
        "r2_mc_e": reg_mc_e.r2,
        "r2_mc_s": reg_mc_s.r2,
        "r2_mc_omega": reg_mc_omega.r2,
        "corr_mc_resid_e_given_omega": float(corr_res_mc_e[0]),
        "p_mc_resid_e_given_omega": float(corr_res_mc_e[1]),
        "corr_mc_resid_s_given_omega": float(corr_res_mc_s[0]),
        "p_mc_resid_s_given_omega": float(corr_res_mc_s[1]),
        "elapsed_sec": float(time.time() - t0),
    }

    csv_path = output_dir / "h12a_results.csv"
    plot_path = output_dir / "h12a_plots.png"
    md_path = output_dir / "H12A_MC_VS_ENTROPY.md"
    summary_json_path = output_dir / "h12a_summary.json"

    df.to_csv(csv_path, index=False)
    create_plots(df, stats_dict, plot_path)

    h10_ref = read_h10_reference_metrics(repo_root)
    write_markdown_report(
        output_md=md_path,
        stats_dict=stats_dict,
        reg_mc_e=reg_mc_e,
        reg_mc_s=reg_mc_s,
        reg_mc_omega=reg_mc_omega,
        corr_res_mc_e=corr_res_mc_e,
        corr_res_mc_s=corr_res_mc_s,
        h10_ref=h10_ref,
    )

    payload = {
        "stats": stats_dict,
        "regression_mc_e": asdict(reg_mc_e),
        "regression_mc_s": asdict(reg_mc_s),
        "regression_mc_omega": asdict(reg_mc_omega),
        "h10_reference": h10_ref,
        "artifacts": {
            "csv": str(csv_path),
            "plot": str(plot_path),
            "report": str(md_path),
        },
    }
    with summary_json_path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    print("Artefakte geschrieben:")
    print(f"  - {csv_path}")
    print(f"  - {plot_path}")
    print(f"  - {md_path}")
    print(f"  - {summary_json_path}")
    print()
    print(
        f"Kennzahlen: corr(M_C,E)={stats_dict['corr_mc_e_pearson']:.6f}, "
        f"R²(M_C~E)={stats_dict['r2_mc_e']:.6f}, "
        f"corr(M_C,S)={stats_dict['corr_mc_s_pearson']:.6f}, "
        f"R²(M_C~S)={stats_dict['r2_mc_s']:.6f}"
    )
    print(f"Laufzeit: {stats_dict['elapsed_sec']:.1f}s")
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="H12-A: M_C vs EABC-Shannon-Entropie")
    parser.add_argument("--n-max", type=int, default=10_000, help="Maximales n (>= 10_000 empfohlen)")
    parser.add_argument(
        "--output-dir",
        type=str,
        default=str(Path("experiments/results/h12")),
        help="Ausgabeverzeichnis fuer Artefakte",
    )
    parser.add_argument(
        "--cache-file",
        type=str,
        default=None,
        help="Optionale HDF5-Cache-Datei fuer EABC-Koordinaten",
    )
    parser.add_argument(
        "--try-100k-if-stable",
        action="store_true",
        help="Fuehre nach erfolgreichem 10k-Lauf optional einen 100k-Lauf aus.",
    )
    parser.add_argument(
        "--stable-seconds-threshold",
        type=float,
        default=180.0,
        help="Max. Laufzeit fuer 10k, um automatisch 100k zu starten.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    cache_path = Path(args.cache_file) if args.cache_file else None
    out_dir = Path(args.output_dir)

    # Primarlauf
    result = run_h12a(n_max=args.n_max, output_dir=out_dir, cache_file=cache_path)

    # Optionaler stabilitaetsbasierter 100k-Lauf
    if args.try_100k_if_stable and args.n_max <= 10_000:
        elapsed = result["stats"]["elapsed_sec"]
        if elapsed <= args.stable_seconds_threshold:
            print("\n10k-Lauf war stabil. Starte optionalen 100k-Lauf ...\n")
            run_h12a(n_max=100_000, output_dir=out_dir, cache_file=cache_path)
        else:
            print(
                "\n100k-Lauf uebersprungen: 10k-Lauf war zu langsam "
                f"({elapsed:.1f}s > {args.stable_seconds_threshold:.1f}s)."
            )
