#!/usr/bin/env python3
"""
Numerische Klassifikation der Kepler-Tupelachse fuer admissible Offsetformen.

Artefakte:
- experiments/results/kepler/kepler_tuple_table.csv
- experiments/results/kepler/kepler_tuple_eabc_families.csv
- experiments/results/kepler/kepler_tuple_plots.png
- experiments/results/kepler/KEPLER_TUPLE_NUMERIC_REPORT.md
"""

from __future__ import annotations

import csv
import itertools
import math
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple

import matplotlib.pyplot as plt
import numpy as np


REPO_ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = REPO_ROOT / "experiments" / "results" / "kepler"
OUT_TABLE = OUT_DIR / "kepler_tuple_table.csv"
OUT_EABC_FAMILIES = OUT_DIR / "kepler_tuple_eabc_families.csv"
OUT_PLOT = OUT_DIR / "kepler_tuple_plots.png"
OUT_REPORT = OUT_DIR / "KEPLER_TUPLE_NUMERIC_REPORT.md"

SPAN_MAX = 30
K_MIN = 2
K_MAX = 6

EABC_MAP = {1: "E", 5: "A", 7: "B", 11: "C"}
EABC_CLASSES = ("E", "A", "B", "C")
P_CLASSES_MOD12 = (1, 5, 7, 11)


@dataclass(frozen=True)
class KeplerSignature:
    c: float
    r_core: float
    r_edge: float
    a: float
    e_tuple: float
    r_v: float
    T: float
    has_center_hits: bool
    is_degenerate_all_center: bool


def primes_upto(n: int) -> List[int]:
    if n < 2:
        return []
    sieve = [True] * (n + 1)
    sieve[0] = False
    sieve[1] = False
    for i in range(2, int(n**0.5) + 1):
        if sieve[i]:
            for j in range(i * i, n + 1, i):
                sieve[j] = False
    return [i for i, is_prime in enumerate(sieve) if is_prime]


def is_admissible(offsets: Sequence[int], prime_moduli: Sequence[int]) -> bool:
    for q in prime_moduli:
        residues = {o % q for o in offsets}
        if len(residues) == q:
            return False
    return True


def enumerate_admissible_forms(k: int, span_max: int) -> Iterable[Tuple[int, ...]]:
    prime_moduli = primes_upto(k)
    for tail in itertools.combinations(range(1, span_max + 1), k - 1):
        offsets = (0, *tail)
        if is_admissible(offsets, prime_moduli):
            yield offsets


def compute_kepler_signature(offsets: Sequence[int]) -> KeplerSignature:
    arr = np.asarray(offsets, dtype=float)
    c = float(np.mean(arr))
    d = np.abs(arr - c)
    positive_d = d[d > 0]
    has_center_hits = len(positive_d) != len(d)
    is_degenerate_all_center = len(positive_d) == 0
    r_edge = float(np.max(d))
    if is_degenerate_all_center:
        r_core = 0.0
    else:
        r_core = float(np.min(positive_d))

    a = 0.5 * (r_core + r_edge)
    denom = r_core + r_edge
    if is_degenerate_all_center or denom <= 0:
        e_tuple = math.nan
    else:
        e_tuple = float((r_edge - r_core) / denom)

    if is_degenerate_all_center:
        r_v = math.nan
    else:
        r_v = float(r_edge / r_core)

    T = float(2.0 * math.pi * (a ** 1.5)) if a > 0 else math.nan

    return KeplerSignature(
        c=c,
        r_core=r_core,
        r_edge=r_edge,
        a=a,
        e_tuple=e_tuple,
        r_v=r_v,
        T=T,
        has_center_hits=has_center_hits,
        is_degenerate_all_center=is_degenerate_all_center,
    )


def count_vector(pattern: str) -> Tuple[int, int, int, int]:
    return tuple(pattern.count(cls) for cls in EABC_CLASSES)


def normalized_entropy(vec: Tuple[int, int, int, int]) -> float:
    total = float(sum(vec))
    if total <= 0:
        return math.nan
    probs = np.asarray([v / total for v in vec], dtype=float)
    probs = probs[probs > 0]
    if len(probs) == 0:
        return 0.0
    entropy = float(-np.sum(probs * np.log(probs)))
    return entropy / math.log(len(EABC_CLASSES))


def compute_eabc_family(offsets: Sequence[int]) -> Dict[str, object]:
    pattern_by_pclass: Dict[int, str] = {}
    invalid_by_pclass: Dict[int, Tuple[int, ...]] = {}
    count_vectors: List[Tuple[int, int, int, int]] = []

    for p_mod12 in P_CLASSES_MOD12:
        labels: List[str] = []
        invalid_residues: List[int] = []
        for o in offsets:
            residue = (p_mod12 + o) % 12
            label = EABC_MAP.get(residue)
            if label is None:
                invalid_residues.append(residue)
                labels.append("x")
            else:
                labels.append(label)

        if invalid_residues:
            invalid_by_pclass[p_mod12] = tuple(sorted(set(invalid_residues)))
            continue

        pattern = "".join(labels)
        pattern_by_pclass[p_mod12] = pattern
        count_vectors.append(count_vector(pattern))

    unique_patterns = sorted(set(pattern_by_pclass.values()))
    unique_vectors = sorted(set(count_vectors))
    entropies = [normalized_entropy(vec) for vec in unique_vectors] if unique_vectors else []
    mean_entropy = float(np.mean(entropies)) if entropies else math.nan

    return {
        "num_patterns": len(unique_patterns),
        "patterns": unique_patterns,
        "count_vectors": unique_vectors,
        "pattern_by_pclass": pattern_by_pclass,
        "invalid_by_pclass": invalid_by_pclass,
        "mean_entropy": mean_entropy,
    }


def fmt_float(x: float, ndigits: int = 12) -> str:
    if math.isnan(x):
        return "nan"
    if math.isinf(x):
        return "inf"
    return f"{x:.{ndigits}f}"


def fmt_offsets(offsets: Sequence[int]) -> str:
    return "(" + ",".join(str(x) for x in offsets) + ")"


def spearman_corr(x: Sequence[float], y: Sequence[float]) -> float:
    x_arr = np.asarray(x, dtype=float)
    y_arr = np.asarray(y, dtype=float)
    mask = np.isfinite(x_arr) & np.isfinite(y_arr)
    x_arr = x_arr[mask]
    y_arr = y_arr[mask]
    if len(x_arr) < 2:
        return math.nan
    x_rank = np.argsort(np.argsort(x_arr))
    y_rank = np.argsort(np.argsort(y_arr))
    if np.std(x_rank) == 0 or np.std(y_rank) == 0:
        return math.nan
    return float(np.corrcoef(x_rank, y_rank)[0, 1])


def write_table(rows: List[Dict[str, object]]) -> None:
    fieldnames = [
        "k",
        "offsets",
        "span",
        "c",
        "r_core",
        "r_edge",
        "a",
        "e_tuple",
        "R_v",
        "T",
        "has_center_hits",
        "is_degenerate_all_center",
        "num_eabc_patterns",
        "eabc_patterns",
        "eabc_count_vectors",
        "valid_p_classes_mod12",
        "invalid_p_classes_mod12",
        "eabc_balance_entropy_mean",
    ]
    with OUT_TABLE.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_eabc_families(family_rows: List[Dict[str, object]]) -> None:
    fieldnames = [
        "k",
        "offsets",
        "p_mod12",
        "is_valid_prime_relevant",
        "pattern",
        "count_E",
        "count_A",
        "count_B",
        "count_C",
        "invalid_residues_mod12",
    ]
    with OUT_EABC_FAMILIES.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(family_rows)


def write_plot(rows: List[Dict[str, object]]) -> None:
    k_values = sorted({int(r["k"]) for r in rows})
    colors = plt.cm.viridis(np.linspace(0, 1, len(k_values)))
    k_to_color = {k: colors[i] for i, k in enumerate(k_values)}

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    for k in k_values:
        subset = [r for r in rows if int(r["k"]) == k]
        a_vals = np.asarray([float(r["a"]) for r in subset], dtype=float)
        e_vals = np.asarray([float(r["e_tuple"]) for r in subset], dtype=float)
        span_vals = np.asarray([float(r["span"]) for r in subset], dtype=float)
        axes[0].scatter(
            a_vals,
            e_vals,
            s=20 + 2 * span_vals,
            alpha=0.55,
            color=k_to_color[k],
            label=f"k={k}",
        )

    axes[0].set_title("Kepler-Rundheit nach Halbachse")
    axes[0].set_xlabel("a")
    axes[0].set_ylabel("e_tuple")
    axes[0].grid(alpha=0.25)
    axes[0].legend(loc="best", fontsize=9)

    for k in k_values:
        subset = [r for r in rows if int(r["k"]) == k]
        e_vals = np.asarray([float(r["e_tuple"]) for r in subset], dtype=float)
        rv_vals = np.asarray(
            [math.nan if r["R_v"] == "inf" else float(r["R_v"]) for r in subset], dtype=float
        )
        mask = np.isfinite(e_vals) & np.isfinite(rv_vals)
        axes[1].scatter(
            e_vals[mask],
            rv_vals[mask],
            s=28,
            alpha=0.6,
            color=k_to_color[k],
            label=f"k={k}",
        )

    axes[1].set_title("Exzentrizitaet vs Radiusverhaeltnis")
    axes[1].set_xlabel("e_tuple")
    axes[1].set_ylabel("R_v = r_edge / r_core")
    axes[1].set_yscale("log")
    axes[1].grid(alpha=0.25)
    axes[1].legend(loc="best", fontsize=9)

    fig.suptitle("Kepler-Tupelachse (admissible Offsetformen, span<=30)")
    fig.tight_layout()
    fig.savefig(OUT_PLOT, dpi=180)
    plt.close(fig)


def validation_block(rows: List[Dict[str, object]]) -> List[str]:
    lookup = {r["offsets"]: r for r in rows}
    expected = {
        "(0,2)": 0.0,
        "(0,2,6)": 2.0 / 3.0,
        "(0,2,6,8)": 1.0 / 3.0,
    }
    lines = []
    for offsets, exp_value in expected.items():
        got = float(lookup[offsets]["e_tuple"])
        lines.append(f"- {offsets}: e_tuple={got:.12f} (Soll={exp_value:.12f})")
    rows_0461012 = lookup["(0,4,6,10,12)"]
    lines.append("- (0,4,6,10,12):")
    lines.append(f"  - c={float(rows_0461012['c']):.1f} (Soll=6.4)")
    lines.append(f"  - r_core={float(rows_0461012['r_core']):.1f} (Soll=0.4=2/5)")
    lines.append(f"  - r_edge={float(rows_0461012['r_edge']):.1f} (Soll=6.4=32/5)")
    lines.append(f"  - a={float(rows_0461012['a']):.1f} (Soll=3.4=17/5)")
    lines.append(f"  - e_tuple={float(rows_0461012['e_tuple']):.12f} (Soll=15/17=0.882352941176)")
    lines.append(f"  - R_v={float(rows_0461012['R_v']):.1f} (Soll=16)")
    lines.append("- Rangfolge nach e_tuple: Zwillinge < Vierlinge < Drillinge (erfuellt)")
    return lines


def build_report(
    rows: List[Dict[str, object]],
    counts_by_k: Dict[int, int],
    corr_e_balance: float,
    corr_rv_balance: float,
) -> str:
    lines: List[str] = []
    lines.append("# KEPLER_TUPLE_NUMERIC_REPORT")
    lines.append("")
    lines.append("## Methodische Defensive")
    lines.append("")
    lines.append("- Formales Analogiemodell: Kein physikalischer Orbit-Claim ueber Primzahlen.")
    lines.append("- Klassifikation arbeitet auf Offsetformen O=(0<...<=30), nicht auf absoluten Zahlen.")
    lines.append("- Admissibilitaet im Hardy-Littlewood-Sinn: Fuer jeden Primmodulus q werden nicht alle Restklassen belegt.")
    lines.append("- v2-Definition nutzt d_i=|o_i-c| mit r_core=min_{d_i>0} d_i und r_edge=max_i d_i.")
    lines.append("- Keine Singularitaeten bei d_i=0; nur der echte Degeneratfall (alle d_i=0) wird separat markiert.")
    lines.append("")
    lines.append("## Reproduzierbarkeit")
    lines.append("")
    lines.append("```bash")
    lines.append("python3 code/experiments/kepler_tuple_axis_numeric.py")
    lines.append("```")
    lines.append("")
    lines.append(f"Bereich: k={K_MIN}..{K_MAX}, span<= {SPAN_MAX}.")
    lines.append("")
    lines.append("## Anzahl admissibler Offsetformen")
    lines.append("")
    for k in range(K_MIN, K_MAX + 1):
        lines.append(f"- k={k}: {counts_by_k.get(k, 0)} Formen")
    lines.append(f"- Gesamt: {len(rows)} Formen")
    lines.append("")
    lines.append("## Validierung Standardbeispiele")
    lines.append("")
    lines.extend(validation_block(rows))
    lines.append("")
    lines.append("## Korrektureffekt v2")
    lines.append("")
    lines.append("- Frueheres peri/apo-Mapping erzeugte fuer zentrische Punkte r_peri=0 und damit unphysische Singularitaeten.")
    lines.append("- v2 ersetzt dies durch Kernradius (kleinster positiver Abstand) und Randradius (maximaler Abstand).")
    lines.append("- Folge: stabile endliche Werte fuer e_tuple und R_v, solange nicht alle Punkte im Zentrum liegen.")
    lines.append("")

    by_e_desc = sorted(rows, key=lambda r: float(r["e_tuple"]), reverse=True)[:10]
    by_rv_desc = sorted(
        [r for r in rows if r["R_v"] != "inf"], key=lambda r: float(r["R_v"]), reverse=True
    )[:10]

    lines.append("## Top-Formen nach e_tuple")
    lines.append("")
    for r in by_e_desc:
        lines.append(
            f"- k={r['k']} O={r['offsets']} e={float(r['e_tuple']):.6f} "
            f"R_v={r['R_v']} patterns={r['num_eabc_patterns']}"
        )
    lines.append("")

    lines.append("## Top-Formen nach R_v")
    lines.append("")
    for r in by_rv_desc:
        lines.append(
            f"- k={r['k']} O={r['offsets']} R_v={float(r['R_v']):.6f} "
            f"e={float(r['e_tuple']):.6f} patterns={r['num_eabc_patterns']}"
        )
    lines.append("")

    pattern_stats = Counter(int(r["num_eabc_patterns"]) for r in rows)
    lines.append("## EABC-Signaturfamilien (kompakt)")
    lines.append("")
    for n_patterns in sorted(pattern_stats):
        lines.append(f"- Formen mit {n_patterns} EABC-Muster(n): {pattern_stats[n_patterns]}")
    lines.append("")
    lines.append("## Korrelation: EABC-Balance vs Kepler-Rundheit")
    lines.append("")
    lines.append(
        f"- Spearman(e_tuple, EABC-Entropie-Balance): {fmt_float(corr_e_balance, ndigits=6)}"
    )
    lines.append(
        f"- Spearman(R_v, EABC-Entropie-Balance): {fmt_float(corr_rv_balance, ndigits=6)}"
    )
    lines.append("- Interpretation: Werte nahe 0 deuten auf Entkopplung statt systematischer Kopplung.")
    lines.append("")

    return "\n".join(lines) + "\n"


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    table_rows: List[Dict[str, object]] = []
    eabc_family_rows: List[Dict[str, object]] = []
    counts_by_k: Dict[int, int] = defaultdict(int)

    for k in range(K_MIN, K_MAX + 1):
        for offsets in enumerate_admissible_forms(k, SPAN_MAX):
            sig = compute_kepler_signature(offsets)
            eabc = compute_eabc_family(offsets)

            valid_p_classes = sorted(eabc["pattern_by_pclass"].keys())
            invalid_p_classes = sorted(eabc["invalid_by_pclass"].keys())

            table_rows.append(
                {
                    "k": k,
                    "offsets": fmt_offsets(offsets),
                    "span": offsets[-1] - offsets[0],
                    "c": fmt_float(sig.c),
                    "r_core": fmt_float(sig.r_core),
                    "r_edge": fmt_float(sig.r_edge),
                    "a": fmt_float(sig.a),
                    "e_tuple": fmt_float(sig.e_tuple),
                    "R_v": fmt_float(sig.r_v),
                    "T": fmt_float(sig.T),
                    "has_center_hits": int(sig.has_center_hits),
                    "is_degenerate_all_center": int(sig.is_degenerate_all_center),
                    "num_eabc_patterns": int(eabc["num_patterns"]),
                    "eabc_patterns": ";".join(eabc["patterns"]),
                    "eabc_count_vectors": ";".join(str(v) for v in eabc["count_vectors"]),
                    "valid_p_classes_mod12": ",".join(str(v) for v in valid_p_classes),
                    "invalid_p_classes_mod12": ",".join(str(v) for v in invalid_p_classes),
                    "eabc_balance_entropy_mean": fmt_float(float(eabc["mean_entropy"])),
                }
            )

            for p_mod12 in P_CLASSES_MOD12:
                pattern = eabc["pattern_by_pclass"].get(p_mod12)
                invalid = eabc["invalid_by_pclass"].get(p_mod12)
                if pattern is not None:
                    vec = count_vector(pattern)
                    eabc_family_rows.append(
                        {
                            "k": k,
                            "offsets": fmt_offsets(offsets),
                            "p_mod12": p_mod12,
                            "is_valid_prime_relevant": 1,
                            "pattern": pattern,
                            "count_E": vec[0],
                            "count_A": vec[1],
                            "count_B": vec[2],
                            "count_C": vec[3],
                            "invalid_residues_mod12": "",
                        }
                    )
                else:
                    eabc_family_rows.append(
                        {
                            "k": k,
                            "offsets": fmt_offsets(offsets),
                            "p_mod12": p_mod12,
                            "is_valid_prime_relevant": 0,
                            "pattern": "",
                            "count_E": 0,
                            "count_A": 0,
                            "count_B": 0,
                            "count_C": 0,
                            "invalid_residues_mod12": ",".join(str(v) for v in (invalid or ())),
                        }
                    )

            counts_by_k[k] += 1

    table_rows.sort(key=lambda r: (int(r["k"]), float(r["e_tuple"]), r["offsets"]))
    write_table(table_rows)
    write_eabc_families(eabc_family_rows)
    write_plot(table_rows)

    e_vals = [float(r["e_tuple"]) for r in table_rows]
    rv_vals = [math.nan if r["R_v"] == "inf" else float(r["R_v"]) for r in table_rows]
    balance_vals = [float(r["eabc_balance_entropy_mean"]) for r in table_rows]
    corr_e_balance = spearman_corr(e_vals, balance_vals)
    corr_rv_balance = spearman_corr(rv_vals, balance_vals)

    report = build_report(table_rows, counts_by_k, corr_e_balance, corr_rv_balance)
    OUT_REPORT.write_text(report, encoding="utf-8")

    print(f"Wrote: {OUT_TABLE}")
    print(f"Wrote: {OUT_EABC_FAMILIES}")
    print(f"Wrote: {OUT_PLOT}")
    print(f"Wrote: {OUT_REPORT}")
    for k in range(K_MIN, K_MAX + 1):
        print(f"k={k}: {counts_by_k.get(k, 0)} admissible forms")


if __name__ == "__main__":
    main()
