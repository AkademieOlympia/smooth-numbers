#!/usr/bin/env python3
"""
Noether-inspired invariance scan for existing observables.

This script is intentionally defensive:
- no claim of classical Noether theorem
- purely empirical invariance/symmetry-breaking diagnostics
"""

from __future__ import annotations

import argparse
import csv
import itertools
import math
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Dict, Iterable, List, Mapping, Optional, Sequence, Tuple

import numpy as np

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


REPO_ROOT = Path(__file__).resolve().parents[2]
RESULTS_DIR = REPO_ROOT / "experiments" / "results" / "noether"
CSV_OUT = RESULTS_DIR / "noether_invariance_table.csv"
REPORT_OUT = RESULTS_DIR / "noether_invariance_report.md"
PLOT_OUT = RESULTS_DIR / "noether_invariance_plots.png"

DOC_OUT = REPO_ROOT / "docs" / "NOETHER_INVARIANCE_PROGRAM.md"

STAGE55_RUN_FILES: Sequence[Path] = [
    REPO_ROOT / "stage5.5_final_run.txt",
    REPO_ROOT / "reproducibility_N10M.txt",
    REPO_ROOT / "reproducibility_N20M.txt",
]

# Import project code from catalan-normalform.
CATALAN_CODE = REPO_ROOT / "catalan-normalform" / "code"
if str(CATALAN_CODE) not in sys.path:
    sys.path.insert(0, str(CATALAN_CODE))

from catalan_trees import BinaryTree  # type: ignore  # noqa: E402
from utils.canonization import canonize_number  # type: ignore  # noqa: E402
from utils.catalan_magic import compute_catalan_magic  # type: ignore  # noqa: E402
from utils.eabc import (  # type: ignore  # noqa: E402
    compute_svn_coordinates,
    eabc_class,
    prime_factors_with_multiplicity,
)


LABELS = ("E", "A", "B", "C")


@dataclass
class Transform:
    name: str
    family: str
    domain: str
    description: str
    apply: Callable[[Mapping[str, object]], Dict[str, object]]


def leaf_depths(tree: BinaryTree, depth: int = 0) -> List[int]:
    if tree.is_leaf:
        return [depth]
    vals: List[int] = []
    if tree.left is not None:
        vals.extend(leaf_depths(tree.left, depth + 1))
    if tree.right is not None:
        vals.extend(leaf_depths(tree.right, depth + 1))
    return vals


def normalized_colless(n: int, omega: int) -> float:
    raw = float(compute_catalan_magic(n, method="balanced", metric="colless"))
    max_imbalance = (omega - 1) * (omega - 2) / 2 if omega > 2 else 1.0
    return float(raw / max_imbalance) if max_imbalance > 0 else 0.0


def eabc_signature_project_consistent(n: int) -> str:
    factors = prime_factors_with_multiplicity(n)
    signature: List[str] = []
    for p in factors:
        if p in (2, 3):
            signature.append("E")
        else:
            cls = eabc_class(p)
            signature.append(cls if cls in LABELS else "?")
    return "".join(signature)


def eabc_entropy(counts: np.ndarray) -> float:
    total = float(np.sum(counts))
    if total <= 0:
        return math.nan
    p = counts / total
    p = p[p > 0]
    return float(-np.sum(p * np.log(p)))


def eabc_concentration_h(counts: np.ndarray) -> float:
    total = float(np.sum(counts))
    if total <= 0:
        return math.nan
    return float(np.dot(counts, counts) / (total * total))


def compute_catalan_state(n: int) -> Dict[str, object]:
    coords = compute_svn_coordinates(n)
    omega = int(coords["omega"])
    shell_s = int(coords["v2"] + coords["v3"])
    counts = np.array([coords["e"], coords["a"], coords["b"], coords["c"]], dtype=float)

    tree = canonize_number(n, method="balanced")
    depths = leaf_depths(tree)
    d_mean = float(np.mean(depths)) if depths else math.nan
    b_norm = normalized_colless(n, omega)

    return {
        "n": n,
        "M_C": float(compute_catalan_magic(n, method="balanced", metric="depth")),
        "Omega": float(omega),
        "S": float(shell_s),
        "E": float(eabc_entropy(counts)),
        "H": float(eabc_concentration_h(counts)),
        "L": float(len(eabc_signature_project_consistent(n))),
        "D": d_mean,
        "B": b_norm,
        "counts": counts,
        "signature": eabc_signature_project_consistent(n),
    }


def relabel_counts_and_signature(
    counts: np.ndarray, signature: str, mapping: Mapping[str, str]
) -> Tuple[np.ndarray, str]:
    old_idx = {lbl: i for i, lbl in enumerate(LABELS)}
    new_counts = np.zeros(4, dtype=float)
    for lbl_old, idx_old in old_idx.items():
        lbl_new = mapping[lbl_old]
        idx_new = old_idx[lbl_new]
        new_counts[idx_new] += counts[idx_old]
    new_signature = "".join(mapping.get(ch, ch) for ch in signature)
    return new_counts, new_signature


def catalan_observables_from_state(state: Mapping[str, object]) -> Dict[str, float]:
    counts = np.array(state["counts"], dtype=float)
    return {
        "M_C": float(state["M_C"]),
        "Omega": float(state["Omega"]),
        "S": float(state["S"]),
        "E(n)": eabc_entropy(counts),
        "H(n)": eabc_concentration_h(counts),
        "L(n)": float(len(str(state["signature"]))),
        "D(n)": float(state["D"]),
        "B(n)": float(state["B"]),
    }


def parse_stage55_run(path: Path) -> Dict[str, object]:
    text = path.read_text(encoding="utf-8")
    n_match = re.search(r"^N\s*=\s*(\d+)\s*$", text, flags=re.MULTILINE)
    if not n_match:
        raise ValueError(f"Cannot parse N from {path}")
    n = int(n_match.group(1))

    h_prime: Dict[int, float] = {}
    h_random: Dict[int, float] = {}
    h_cramer: Dict[int, float] = {}

    for dr, val in re.findall(r"Δr=(\d+):\s*H_Prime\s*=\s*([0-9.]+)", text):
        h_prime[int(dr)] = float(val)
    for dr, val in re.findall(r"Δr=(\d+):\s*H_WheelRandom\s*=\s*([0-9.]+)", text):
        h_random[int(dr)] = float(val)
    for dr, val in re.findall(r"Δr=(\d+):\s*H_WheelCram[ée]r\s*=\s*([0-9.]+)", text):
        h_cramer[int(dr)] = float(val)

    common = sorted(set(h_prime) & set(h_random) & set(h_cramer))
    if not common:
        raise ValueError(f"No shared delta-r values in {path}")

    return {
        "N": n,
        "delta_r": common,
        "H_prime": {dr: h_prime[dr] for dr in common},
        "H_wheel_random": {dr: h_random[dr] for dr in common},
        "H_wheel_cramer": {dr: h_cramer[dr] for dr in common},
    }


def gap_observables_from_run(run: Mapping[str, object]) -> Dict[str, Dict[int, float]]:
    drs = list(run["delta_r"])
    h_prime = run["H_prime"]
    h_cramer = run["H_wheel_cramer"]
    out_h: Dict[int, float] = {}
    out_dh: Dict[int, float] = {}
    out_q: Dict[int, float] = {}
    for dr in drs:
        hp = float(h_prime[dr])
        hc = float(h_cramer[dr])
        out_h[dr] = hp
        out_dh[dr] = hp - hc
        out_q[dr] = hp / hc if hc != 0 else math.nan
    return {
        "H(delta_r)": out_h,
        "DeltaH_cramer": out_dh,
        "Q_cramer": out_q,
    }


def permutation_for_swap(size: int, i: int, j: int) -> List[int]:
    perm = list(range(size))
    perm[i], perm[j] = perm[j], perm[i]
    return perm


def build_transforms(delta_r_values: Sequence[int]) -> List[Transform]:
    transforms: List[Transform] = []

    transforms.append(
        Transform(
            name="identity",
            family="identity",
            domain="both",
            description="No transformation",
            apply=lambda s: dict(s),
        )
    )

    cycle_map = {"E": "A", "A": "B", "B": "C", "C": "E"}

    def apply_cycle(state: Mapping[str, object]) -> Dict[str, object]:
        counts, sig = relabel_counts_and_signature(
            np.array(state["counts"], dtype=float), str(state["signature"]), cycle_map
        )
        st = dict(state)
        st["counts"] = counts
        st["signature"] = sig
        return st

    transforms.append(
        Transform(
            name="eabc_cycle_E_to_A_to_B_to_C",
            family="eabc_cycle",
            domain="catalan",
            description="Cycle E->A->B->C->E",
            apply=apply_cycle,
        )
    )

    flip_map = {"E": "E", "A": "C", "B": "B", "C": "A"}

    def apply_chiral_flip(state: Mapping[str, object]) -> Dict[str, object]:
        counts, sig = relabel_counts_and_signature(
            np.array(state["counts"], dtype=float), str(state["signature"]), flip_map
        )
        st = dict(state)
        st["counts"] = counts
        st["signature"] = sig
        return st

    transforms.append(
        Transform(
            name="eabc_chirality_flip_A_C",
            family="chirality_flip",
            domain="catalan",
            description="Swap A and C labels",
            apply=apply_chiral_flip,
        )
    )

    def apply_signature_reverse(state: Mapping[str, object]) -> Dict[str, object]:
        st = dict(state)
        st["signature"] = str(state["signature"])[::-1]
        return st

    transforms.append(
        Transform(
            name="signature_reversal",
            family="signature_reversal",
            domain="catalan",
            description="Reverse EABC signature order",
            apply=apply_signature_reverse,
        )
    )

    # All non-identity EABC permutations.
    for perm in itertools.permutations(LABELS):
        mapping = {old: new for old, new in zip(LABELS, perm)}
        if all(mapping[k] == k for k in LABELS):
            continue

        perm_name = "".join(perm)

        def make_apply(map_fixed: Dict[str, str]) -> Callable[[Mapping[str, object]], Dict[str, object]]:
            def _apply(state: Mapping[str, object]) -> Dict[str, object]:
                counts, sig = relabel_counts_and_signature(
                    np.array(state["counts"], dtype=float),
                    str(state["signature"]),
                    map_fixed,
                )
                st = dict(state)
                st["counts"] = counts
                st["signature"] = sig
                return st

            return _apply

        transforms.append(
            Transform(
                name=f"eabc_perm_{perm_name}",
                family="eabc_permutation",
                domain="catalan",
                description=f"Permutation EABC->{perm_name}",
                apply=make_apply(mapping),
            )
        )

    dr = list(delta_r_values)
    m = len(dr)
    idx_by_dr = {val: idx for idx, val in enumerate(dr)}

    def apply_gap_permutation(
        state: Mapping[str, object], idx_perm: Sequence[int], transform_name: str
    ) -> Dict[str, object]:
        obs = state["gap_observables"]
        transformed: Dict[str, Dict[int, float]] = {}
        for obs_name, vec in obs.items():
            old_vals = [float(vec[d]) for d in dr]
            new_vals = [old_vals[idx_perm[i]] for i in range(m)]
            transformed[obs_name] = {d: new_vals[idx_by_dr[d]] for d in dr}
        st = dict(state)
        st["gap_observables"] = transformed
        st["transform_trace"] = transform_name
        return st

    for k in range(1, m):
        perm = [((i - k) % m) for i in range(m)]

        def make_cycle(k_fixed: int, perm_fixed: List[int]) -> Callable[[Mapping[str, object]], Dict[str, object]]:
            def _apply(state: Mapping[str, object]) -> Dict[str, object]:
                return apply_gap_permutation(state, perm_fixed, f"dr_cycle_shift_{k_fixed}")

            return _apply

        transforms.append(
            Transform(
                name=f"dr_cycle_shift_{k}",
                family="gap_cycle",
                domain="gap",
                description=f"Cycle shift over ordered delta_r list by {k}",
                apply=make_cycle(k, perm),
            )
        )

    reverse_perm = list(reversed(range(m)))
    transforms.append(
        Transform(
            name="dr_chirality_reverse",
            family="gap_chirality",
            domain="gap",
            description="Reverse ordered delta_r labels",
            apply=lambda s, p=reverse_perm: apply_gap_permutation(s, p, "dr_chirality_reverse"),
        )
    )

    for i in range(m):
        for j in range(i + 1, m):
            perm = permutation_for_swap(m, i, j)
            di = dr[i]
            dj = dr[j]
            transforms.append(
                Transform(
                    name=f"dr_transposition_{di}_{dj}",
                    family="gap_transposition",
                    domain="gap",
                    description=f"Swap delta_r={di} and delta_r={dj}",
                    apply=lambda s, p=perm, di=di, dj=dj: apply_gap_permutation(
                        s, p, f"dr_transposition_{di}_{dj}"
                    ),
                )
            )

    # Wheel-inspired operations on delta-r labels.
    # Data-driven abstraction: since tested delta_r are an arithmetic progression,
    # additive congruence shifts induce permutations on the index set.
    for k in range(1, m):
        wheel30_perm = [((i - k) % m) for i in range(m)]
        transforms.append(
            Transform(
                name=f"wheel30_add4k_{k}",
                family="wheel30_congruence",
                domain="gap",
                description=f"delta_r -> delta_r + 4*{k} (wrapped over sampled classes)",
                apply=lambda s, p=wheel30_perm, k=k: apply_gap_permutation(
                    s, p, f"wheel30_add4k_{k}"
                ),
            )
        )

        wheel210_perm = [((i - (2 * k)) % m) for i in range(m)]
        transforms.append(
            Transform(
                name=f"wheel210_add8k_{k}",
                family="wheel210_congruence",
                domain="gap",
                description=f"delta_r -> delta_r + 8*{k} (wrapped over sampled classes)",
                apply=lambda s, p=wheel210_perm, k=k: apply_gap_permutation(
                    s, p, f"wheel210_add8k_{k}"
                ),
            )
        )

    return transforms


def invariance_stats(
    x: np.ndarray, y: np.ndarray, rng: np.random.Generator, perm_trials: int
) -> Dict[str, float]:
    mask = np.isfinite(x) & np.isfinite(y)
    xv = x[mask]
    yv = y[mask]
    n = len(xv)
    if n == 0:
        return {
            "n": 0.0,
            "I_abs": math.nan,
            "I_norm": math.nan,
            "effect_size": math.nan,
            "p_perm_invariance": math.nan,
        }

    diff = xv - yv
    i_abs = float(np.mean(np.abs(diff)))
    scale = float(np.mean(np.abs(xv)))
    i_norm = float(i_abs / (scale + 1e-12))
    effect = float(i_abs / (np.std(xv) + 1e-12))

    perm_stats = np.empty(perm_trials, dtype=float)
    for i in range(perm_trials):
        yp = yv[rng.permutation(n)]
        perm_stats[i] = np.mean(np.abs(xv - yp))
    p_invariance = float((1 + np.sum(perm_stats <= i_abs)) / (perm_trials + 1))

    return {
        "n": float(n),
        "I_abs": i_abs,
        "I_norm": i_norm,
        "effect_size": effect,
        "p_perm_invariance": p_invariance,
    }


def classify_invariance(i_norm: float) -> str:
    if not np.isfinite(i_norm):
        return "not_available"
    if i_norm < 0.03:
        return "invariant"
    if i_norm < 0.15:
        return "weak_sensitive"
    return "strong_symmetry_breaking"


def write_program_doc() -> None:
    DOC_OUT.parent.mkdir(parents=True, exist_ok=True)
    lines: List[str] = []
    lines.append("# Noether-Inspired Invariance Program")
    lines.append("")
    lines.append("## Scope and stance")
    lines.append("")
    lines.append("- This program is **Noether-inspired**, not a claim of a classical theorem in this discrete setting.")
    lines.append("- Goal: test which existing observables are approximately invariant under natural transformations.")
    lines.append("- Output labels are empirical: `invariant`, `weak_sensitive`, `strong_symmetry_breaking`.")
    lines.append("")
    lines.append("## State model")
    lines.append("")
    lines.append("- Catalan/EABC state per number `n` includes:")
    lines.append("  - scalar observables `M_C`, `Omega`, `S`, `E(n)`, `H(n)`, `L(n)` and optional `D(n)`, `B(n)`")
    lines.append("  - label state `(E,A,B,C)` counts and EABC signature string")
    lines.append("- Gap state per Stage-5.5 run includes vectors over sampled `delta_r` classes:")
    lines.append("  - `H(delta_r)`, `DeltaH_cramer(delta_r)`, `Q_cramer(delta_r)`")
    lines.append("")
    lines.append("## Transformation catalog")
    lines.append("")
    lines.append("- EABC cycle: `E->A->B->C->E`")
    lines.append("- EABC permutations: all non-identity permutations (includes transpositions)")
    lines.append("- Signature reversal and chirality flip (`A<->C`)")
    lines.append("- Wheel-related label operations on sampled `delta_r` classes:")
    lines.append("  - wheel30-style additive shifts")
    lines.append("  - wheel210-style additive shifts")
    lines.append("  - cycle/reversal/transposition operations on sampled `delta_r` labels")
    lines.append("")
    lines.append("## Formal operation view")
    lines.append("")
    lines.append("- Let a Catalan/EABC state be `x=(o, c, s)` with")
    lines.append("  - `o`: scalar observables (`M_C, Omega, S, E, H, L, D, B`)")
    lines.append("  - `c=(e,a,b,c)`: EABC class counts")
    lines.append("  - `s`: EABC signature string")
    lines.append("- For label permutation `pi in S4`: `T_pi(x)=(o', c', s')` where")
    lines.append("  - `c' = P_pi c` (permutation matrix action)")
    lines.append("  - `s'` is relabeled symbol-wise by `pi`")
    lines.append("  - tree-structure observables (`M_C, D, B, Omega, S`) stay unchanged")
    lines.append("- EABC cycle is a special `pi_cycle=(E A B C)`.")
    lines.append("- Chirality flip is `pi_chi=(A C)` with `E,B` fixed.")
    lines.append("- Signature reversal is `T_rev(x)=(o, c, reverse(s))`.")
    lines.append("- Gap state `g=(delta_r, v)` with vector observable `v(delta_r)`.")
    lines.append("- Gap transformation acts as index permutation `sigma`: `T_sigma(g)=(delta_r, v o sigma)`.")
    lines.append("")
    lines.append("## Invariance metrics")
    lines.append("")
    lines.append("- Main score: `I_T(O) = mean |O - O o T|`")
    lines.append("- Normalized score: `I_norm = I_T(O) / (mean|O| + eps)`")
    lines.append("- Effect scale: `I_T(O) / (std(O) + eps)`")
    lines.append("- Permutation-based `p_perm_invariance`:")
    lines.append("  - compare observed `I_T(O)` against random re-pairings of transformed values")
    lines.append("  - small p indicates unusually strong invariance under `T`")
    lines.append("")
    lines.append("## Classification")
    lines.append("")
    lines.append("- `invariant`: `I_norm < 0.03`")
    lines.append("- `weak_sensitive`: `0.03 <= I_norm < 0.15`")
    lines.append("- `strong_symmetry_breaking`: `I_norm >= 0.15`")
    lines.append("")
    lines.append("## Reproducibility")
    lines.append("")
    lines.append("- Script: `code/experiments/noether_invariance_scan.py`")
    lines.append("- Deterministic seed is fixed in the script/CLI (`--seed`).")
    lines.append("- Main results exported to CSV/MD/PNG in `experiments/results/noether/`.")
    DOC_OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def make_plot(rows: List[Dict[str, object]]) -> None:
    non_identity = [r for r in rows if r["transform"] != "identity" and np.isfinite(float(r["I_norm"]))]
    if not non_identity:
        return

    obs_scores: Dict[str, List[float]] = {}
    for r in non_identity:
        obs_scores.setdefault(str(r["observable"]), []).append(float(r["I_norm"]))
    obs_avg = sorted(
        [(obs, float(np.mean(vals))) for obs, vals in obs_scores.items()],
        key=lambda kv: kv[1],
        reverse=True,
    )

    strongest_breaks = sorted(non_identity, key=lambda r: float(r["I_norm"]), reverse=True)[:12]
    strongest_inv = sorted(non_identity, key=lambda r: float(r["I_norm"]))[:12]

    fig, axes = plt.subplots(1, 3, figsize=(21, 6))
    fig.suptitle("Noether-inspired invariance scan", fontsize=14, fontweight="bold")

    ax = axes[0]
    labels = [k for k, _ in obs_avg]
    vals = [v for _, v in obs_avg]
    ax.barh(labels, vals, color="#1f77b4", alpha=0.85)
    ax.set_title("Mean normalized sensitivity by observable")
    ax.set_xlabel("mean(I_norm)")
    ax.grid(alpha=0.25, axis="x")

    ax = axes[1]
    labels = [f"{r['observable']} | {r['transform']}" for r in strongest_breaks]
    vals = [float(r["I_norm"]) for r in strongest_breaks]
    ax.barh(labels, vals, color="#d62728", alpha=0.85)
    ax.set_title("Strongest symmetry breaks")
    ax.set_xlabel("I_norm")
    ax.grid(alpha=0.25, axis="x")

    ax = axes[2]
    labels = [f"{r['observable']} | {r['transform']}" for r in strongest_inv]
    vals = [float(r["I_norm"]) for r in strongest_inv]
    ax.barh(labels, vals, color="#2ca02c", alpha=0.85)
    ax.set_title("Most invariant non-identity cases")
    ax.set_xlabel("I_norm")
    ax.grid(alpha=0.25, axis="x")

    plt.tight_layout()
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    plt.savefig(PLOT_OUT, dpi=170, bbox_inches="tight")
    plt.close(fig)


def top3_by_mean(rows: List[Dict[str, object]], reverse: bool) -> List[Tuple[str, float]]:
    non_identity = [r for r in rows if r["transform"] != "identity" and np.isfinite(float(r["I_norm"]))]
    score_map: Dict[str, List[float]] = {}
    for r in non_identity:
        score_map.setdefault(str(r["observable"]), []).append(float(r["I_norm"]))
    ranking = sorted(
        [(obs, float(np.mean(vals))) for obs, vals in score_map.items()],
        key=lambda kv: kv[1],
        reverse=reverse,
    )
    return ranking[:3]


def write_report(
    rows: List[Dict[str, object]],
    transforms: List[Transform],
    n_catalog_samples: int,
    n_gap_runs: int,
    delta_r_values: Sequence[int],
) -> None:
    inv_top3 = top3_by_mean(rows, reverse=False)
    break_top3 = top3_by_mean(rows, reverse=True)

    lines: List[str] = []
    lines.append("# Noether-Invariance Scan Report")
    lines.append("")
    lines.append("## Scope")
    lines.append("")
    lines.append("- Frame: **Noether-inspired heuristic** (no strong physical theorem claim).")
    lines.append(f"- Catalan/EABC samples: `{n_catalog_samples}` numbers.")
    lines.append(f"- Gap runs used: `{n_gap_runs}` with delta-r classes `{list(delta_r_values)}`.")
    lines.append(f"- Total tested transformations: `{len(transforms)}`.")
    lines.append("")
    lines.append("## Transformation catalog")
    lines.append("")
    fam_map: Dict[Tuple[str, str], int] = {}
    for t in transforms:
        fam_map[(t.domain, t.family)] = fam_map.get((t.domain, t.family), 0) + 1
    lines.append("| Domain | Family | Count |")
    lines.append("|---|---|---:|")
    for (domain, fam), cnt in sorted(fam_map.items()):
        lines.append(f"| {domain} | {fam} | {cnt} |")
    lines.append("")
    lines.append("### Operations T on states/labels")
    lines.append("")
    lines.append("| T name | Domain | Family | Operation on state |")
    lines.append("|---|---|---|---|")
    seen = set()
    for t in transforms:
        if t.name in seen:
            continue
        seen.add(t.name)
        op_desc = t.description.replace("|", "/")
        lines.append(f"| `{t.name}` | {t.domain} | {t.family} | {op_desc} |")
    lines.append("")
    lines.append("## Method")
    lines.append("")
    lines.append("- Invariance score: `I_T(O)=mean|O - O o T|`.")
    lines.append("- Normalized score: `I_norm = I_T(O)/(mean|O|+eps)`.")
    lines.append("- Classification thresholds:")
    lines.append("  - `invariant` (`I_norm < 0.03`)")
    lines.append("  - `weak_sensitive` (`0.03 <= I_norm < 0.15`)")
    lines.append("  - `strong_symmetry_breaking` (`I_norm >= 0.15`)")
    lines.append("- Permutation p-value is reported as an invariance diagnostic (small p means unusually invariant).")
    lines.append("")
    lines.append("## Most invariant observables (aggregate over non-identity transforms)")
    lines.append("")
    for i, (obs, score) in enumerate(inv_top3, start=1):
        lines.append(f"{i}. `{obs}` with mean `I_norm={score:.6f}`")
    lines.append("")
    lines.append("## Strongest symmetry-breaking observables (aggregate over non-identity transforms)")
    lines.append("")
    for i, (obs, score) in enumerate(break_top3, start=1):
        lines.append(f"{i}. `{obs}` with mean `I_norm={score:.6f}`")
    lines.append("")
    lines.append("## Noether-inspired interpretation (defensive)")
    lines.append("")
    lines.append("- Observables with near-zero sensitivity are robust candidates for structural descriptors.")
    lines.append("- Observables with larger sensitivity under wheel/cycle/permutation-like transforms are symmetry-break indicators.")
    lines.append("- For ongoing program logic: symmetry-breaking channels provide concrete targets for Stage-6 HL-aligned modeling.")
    lines.append("")
    lines.append("## Relation to Stage-5.5/5.6 signals")
    lines.append("")
    lines.append("- The strongest symmetry breaks concentrate in gap-strand observables `H(delta_r)`, `DeltaH_cramer`, and `Q_cramer`.")
    lines.append("- This is consistent with Stage-5.5/5.6 where wheel-based controls do not absorb the prime-side signal.")
    lines.append("- Practical reading: robust structural axes are mostly in Catalan/EABC scalar geometry, while residual signal lives in gap symmetry-breaking channels.")
    lines.append("")
    lines.append("## Artifacts")
    lines.append("")
    lines.append(f"- Table: `{CSV_OUT.relative_to(REPO_ROOT)}`")
    lines.append(f"- Plot: `{PLOT_OUT.relative_to(REPO_ROOT)}`")
    lines.append(f"- Program doc: `{DOC_OUT.relative_to(REPO_ROOT)}`")
    lines.append(f"- Script: `{Path(__file__).relative_to(REPO_ROOT)}`")
    REPORT_OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Noether-inspired invariance scan")
    parser.add_argument("--n-max", type=int, default=30000, help="Max n for Catalan/EABC sample")
    parser.add_argument("--max-samples", type=int, default=8000, help="Max sampled n values")
    parser.add_argument("--perm-trials", type=int, default=400, help="Permutation trials per test")
    parser.add_argument("--seed", type=int, default=20260624, help="Random seed")
    args = parser.parse_args()

    rng = np.random.default_rng(args.seed)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    write_program_doc()

    candidates = [n for n in range(2, args.n_max + 1) if len(prime_factors_with_multiplicity(n)) >= 2]
    if len(candidates) > args.max_samples:
        sample_idx = sorted(rng.choice(len(candidates), size=args.max_samples, replace=False).tolist())
        sampled_n = [candidates[i] for i in sample_idx]
    else:
        sampled_n = candidates

    catalan_states = [compute_catalan_state(n) for n in sampled_n]

    gap_runs = [parse_stage55_run(p) for p in STAGE55_RUN_FILES if p.exists()]
    if not gap_runs:
        raise RuntimeError("No Stage-5.5 run files found for gap observables.")
    common_dr = sorted(set.intersection(*[set(r["delta_r"]) for r in gap_runs]))
    if len(common_dr) < 3:
        raise RuntimeError("Need at least 3 shared delta-r classes.")
    for run in gap_runs:
        run["delta_r"] = common_dr
        for key in ("H_prime", "H_wheel_random", "H_wheel_cramer"):
            run[key] = {dr: run[key][dr] for dr in common_dr}

    gap_states = []
    for run in gap_runs:
        gap_states.append(
            {
                "N": run["N"],
                "delta_r": list(common_dr),
                "gap_observables": gap_observables_from_run(run),
            }
        )

    transforms = build_transforms(common_dr)

    rows: List[Dict[str, object]] = []

    # Catalan/EABC domain.
    cat_obs_names = ["M_C", "Omega", "S", "E(n)", "H(n)", "L(n)", "D(n)", "B(n)"]
    base_cat_obs = [catalan_observables_from_state(st) for st in catalan_states]

    for t in transforms:
        if t.domain not in ("catalan", "both"):
            continue
        transformed_states = [t.apply(st) for st in catalan_states]
        transformed_obs = [catalan_observables_from_state(st) for st in transformed_states]
        for obs_name in cat_obs_names:
            x = np.array([obs[obs_name] for obs in base_cat_obs], dtype=float)
            y = np.array([obs[obs_name] for obs in transformed_obs], dtype=float)
            stats = invariance_stats(x, y, rng=rng, perm_trials=args.perm_trials)
            rows.append(
                {
                    "domain": "catalan",
                    "observable": obs_name,
                    "transform": t.name,
                    "family": t.family,
                    "description": t.description,
                    "I_abs": stats["I_abs"],
                    "I_norm": stats["I_norm"],
                    "effect_size": stats["effect_size"],
                    "p_perm_invariance": stats["p_perm_invariance"],
                    "n_samples": int(stats["n"]),
                    "classification": classify_invariance(stats["I_norm"]),
                }
            )

    # Gap domain.
    gap_obs_names = ["H(delta_r)", "DeltaH_cramer", "Q_cramer"]
    for t in transforms:
        if t.domain not in ("gap", "both"):
            continue
        transformed_gap_states = [t.apply(st) for st in gap_states]
        for obs_name in gap_obs_names:
            x_parts: List[float] = []
            y_parts: List[float] = []
            for i in range(len(gap_states)):
                base_vec = gap_states[i]["gap_observables"][obs_name]
                trans_vec = transformed_gap_states[i]["gap_observables"][obs_name]
                for dr in common_dr:
                    x_parts.append(float(base_vec[dr]))
                    y_parts.append(float(trans_vec[dr]))
            x = np.array(x_parts, dtype=float)
            y = np.array(y_parts, dtype=float)
            stats = invariance_stats(x, y, rng=rng, perm_trials=args.perm_trials)
            rows.append(
                {
                    "domain": "gap",
                    "observable": obs_name,
                    "transform": t.name,
                    "family": t.family,
                    "description": t.description,
                    "I_abs": stats["I_abs"],
                    "I_norm": stats["I_norm"],
                    "effect_size": stats["effect_size"],
                    "p_perm_invariance": stats["p_perm_invariance"],
                    "n_samples": int(stats["n"]),
                    "classification": classify_invariance(stats["I_norm"]),
                }
            )

    with CSV_OUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "domain",
                "observable",
                "transform",
                "family",
                "description",
                "I_abs",
                "I_norm",
                "effect_size",
                "p_perm_invariance",
                "n_samples",
                "classification",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    make_plot(rows)
    write_report(
        rows=rows,
        transforms=transforms,
        n_catalog_samples=len(catalan_states),
        n_gap_runs=len(gap_runs),
        delta_r_values=common_dr,
    )

    print(f"Wrote: {DOC_OUT}")
    print(f"Wrote: {CSV_OUT}")
    print(f"Wrote: {REPORT_OUT}")
    print(f"Wrote: {PLOT_OUT}")


if __name__ == "__main__":
    main()

