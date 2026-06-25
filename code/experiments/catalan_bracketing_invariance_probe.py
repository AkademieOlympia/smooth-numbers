#!/usr/bin/env python3
"""
Catalan-Bracketing-Invariance-Probe fuer EABC/Hurwitz (defensiv).

Erzeugt:
- experiments/results/catalan_bridge/catalan_bracketing_invariance.csv
- experiments/results/catalan_bridge/CATALAN_BRACKETING_INVARIANCE_REPORT.md
- optional: experiments/results/catalan_bridge/catalan_bracketing_invariance.png
"""

from __future__ import annotations

import argparse
import csv
import math
import random
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Dict, List, Sequence, Tuple, Union

HVec = Tuple[int, int, int, int]
Tree = Union[int, Tuple["Tree", "Tree"]]


@dataclass(frozen=True)
class ProbeRow:
    n: int
    omega_tot: int
    catalan_expected: int
    evaluated_trees: int
    mode: str
    h_invariant: bool
    h_reference: HVec
    toy_min: float
    toy_max: float
    toy_range: float
    distinct_toy_values: int
    factors: str


@dataclass(frozen=True)
class DemoFactor:
    name: str
    h: HVec
    norm: float


def smallest_prime_factors(limit: int) -> List[int]:
    spf = list(range(limit + 1))
    for i in range(2, int(limit**0.5) + 1):
        if spf[i] == i:
            start = i * i
            for j in range(start, limit + 1, i):
                if spf[j] == j:
                    spf[j] = i
    return spf


def factor_multiset(n: int, spf: Sequence[int]) -> List[int]:
    x = n
    out: List[int] = []
    while x > 1:
        p = spf[x]
        out.append(p)
        x //= p
    out.sort()
    return out


def prime_to_h_component(p: int) -> HVec:
    if p in (2, 3):
        return (0, 0, 0, 0)
    r = p % 12
    if r == 1:
        return (1, 0, 0, 0)  # E
    if r == 5:
        return (0, 1, 0, 0)  # A
    if r == 7:
        return (0, 0, 1, 0)  # B
    if r == 11:
        return (0, 0, 0, 1)  # C
    raise RuntimeError(f"Unerwartete Restklasse fuer Primzahl p={p}.")


def h_add(a: HVec, b: HVec) -> HVec:
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2], a[3] + b[3])


def catalan_number(m: int) -> int:
    if m < 0:
        return 0
    return math.comb(2 * m, m) // (m + 1)


@lru_cache(maxsize=None)
def full_binary_trees_for_interval(start: int, end: int) -> Tuple[Tree, ...]:
    # Halb-offenes Intervall [start, end) auf geordneter Blattliste.
    if end - start == 1:
        return (start,)
    out: List[Tree] = []
    for split in range(start + 1, end):
        lefts = full_binary_trees_for_interval(start, split)
        rights = full_binary_trees_for_interval(split, end)
        for l in lefts:
            for r in rights:
                out.append((l, r))
    return tuple(out)


def random_tree(start: int, end: int, rng: random.Random) -> Tree:
    if end - start == 1:
        return start
    split = rng.randint(start + 1, end - 1)
    return (random_tree(start, split, rng), random_tree(split, end, rng))


def eval_tree(tree: Tree, leaf_h: Sequence[HVec], leaf_logp: Sequence[float]) -> Tuple[HVec, float, float]:
    # Rueckgabe: (H-Vektor, toy_product_logsum, toy_observable).
    if isinstance(tree, int):
        return leaf_h[tree], leaf_logp[tree], 0.0

    left, right = tree
    h_l, log_l, toy_l = eval_tree(left, leaf_h, leaf_logp)
    h_r, log_r, toy_r = eval_tree(right, leaf_h, leaf_logp)

    h = h_add(h_l, h_r)
    log_total = log_l + log_r
    # Toy-Observable (explizit nicht-kanonisch):
    # Summiert lokale "Balancing-Kosten" je internem Knoten.
    toy = toy_l + toy_r + abs(log_l - log_r)
    return h, log_total, toy


def tree_expr(tree: Tree, names: Sequence[str]) -> str:
    if isinstance(tree, int):
        return names[tree]
    left, right = tree
    return f"({tree_expr(left, names)}*{tree_expr(right, names)})"


def eval_tree_demo(tree: Tree, factors: Sequence[DemoFactor]) -> Tuple[HVec, float, List[Tuple[str, HVec, float, float]]]:
    if isinstance(tree, int):
        leaf = factors[tree]
        return leaf.h, leaf.norm, []

    left, right = tree
    h_l, n_l, trace_l = eval_tree_demo(left, factors)
    h_r, n_r, trace_r = eval_tree_demo(right, factors)
    h = h_add(h_l, h_r)
    nrm = n_l * n_r
    kappa = 1.0 / nrm if nrm > 0 else float("inf")
    expr = f"({tree_expr(left, [f.name for f in factors])}*{tree_expr(right, [f.name for f in factors])})"
    trace = trace_l + trace_r + [(expr, h, nrm, kappa)]
    return h, nrm, trace


def distinct_rounded(values: Sequence[float], ndigits: int = 12) -> int:
    return len({round(v, ndigits) for v in values})


def analyze_n(
    n: int,
    spf: Sequence[int],
    exhaustive_catalan_limit: int,
    sample_trees: int,
    rng: random.Random,
) -> ProbeRow:
    factors = factor_multiset(n, spf)
    k = len(factors)
    if k < 1:
        raise ValueError("n muss >= 2 sein.")

    expected = catalan_number(k - 1)
    leaf_h = [prime_to_h_component(p) for p in factors]
    leaf_logp = [math.log(float(p)) for p in factors]

    h_values: List[HVec] = []
    toy_values: List[float] = []

    if expected <= exhaustive_catalan_limit:
        trees = full_binary_trees_for_interval(0, k)
        mode = "exhaustive"
        eval_count = len(trees)
        for t in trees:
            h, _, toy = eval_tree(t, leaf_h, leaf_logp)
            h_values.append(h)
            toy_values.append(toy)
    else:
        mode = "sampled"
        eval_count = max(1, sample_trees)
        for _ in range(eval_count):
            t = random_tree(0, k, rng)
            h, _, toy = eval_tree(t, leaf_h, leaf_logp)
            h_values.append(h)
            toy_values.append(toy)

    h_ref = h_values[0]
    h_inv = all(h == h_ref for h in h_values)
    toy_min = min(toy_values)
    toy_max = max(toy_values)
    toy_range = toy_max - toy_min
    toy_distinct = distinct_rounded(toy_values)

    return ProbeRow(
        n=n,
        omega_tot=k,
        catalan_expected=expected,
        evaluated_trees=eval_count,
        mode=mode,
        h_invariant=h_inv,
        h_reference=h_ref,
        toy_min=toy_min,
        toy_max=toy_max,
        toy_range=toy_range,
        distinct_toy_values=toy_distinct,
        factors="*".join(str(p) for p in factors),
    )


def write_csv(path: Path, rows: Sequence[ProbeRow]) -> None:
    fieldnames = [
        "n",
        "omega_tot",
        "catalan_expected",
        "evaluated_trees",
        "mode",
        "h_invariant",
        "h_reference",
        "toy_min",
        "toy_max",
        "toy_range",
        "distinct_toy_values",
        "factors",
    ]
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    "n": row.n,
                    "omega_tot": row.omega_tot,
                    "catalan_expected": row.catalan_expected,
                    "evaluated_trees": row.evaluated_trees,
                    "mode": row.mode,
                    "h_invariant": int(row.h_invariant),
                    "h_reference": str(row.h_reference),
                    "toy_min": f"{row.toy_min:.12f}",
                    "toy_max": f"{row.toy_max:.12f}",
                    "toy_range": f"{row.toy_range:.12f}",
                    "distinct_toy_values": row.distinct_toy_values,
                    "factors": row.factors,
                }
            )


def maybe_make_plot(path: Path, rows: Sequence[ProbeRow]) -> bool:
    try:
        import matplotlib.pyplot as plt  # type: ignore
    except Exception:
        return False

    labels = [f"n={r.n} (k={r.omega_tot})" for r in rows]
    y = [r.toy_range for r in rows]
    colors = ["#3b7ddd" if r.h_invariant else "#d9534f" for r in rows]

    fig, ax = plt.subplots(figsize=(max(8, 0.9 * len(rows) + 3), 4.6))
    ax.bar(labels, y, color=colors)
    ax.set_ylabel("Toy-Observable Range ueber Baeume")
    ax.set_title("Catalan-Baumabhaengigkeit (Toy) bei gleichbleibendem H(n)")
    ax.tick_params(axis="x", rotation=55, labelsize=8)
    ax.grid(axis="y", alpha=0.2)
    fig.tight_layout()
    fig.savefig(path, dpi=170)
    plt.close(fig)
    return True


def write_report(path: Path, rows: Sequence[ProbeRow], plot_written: bool) -> None:
    all_h_invariant = all(r.h_invariant for r in rows)
    any_toy_dep = any(r.toy_range > 1e-12 and r.distinct_toy_values > 1 for r in rows)
    exhaustive_rows = [r for r in rows if r.mode == "exhaustive"]
    sampled_rows = [r for r in rows if r.mode == "sampled"]

    lines: List[str] = [
        "# Catalan Bracketing Invariance Probe (EABC/Hurwitz)",
        "",
        "## Ziel",
        "",
        "- Pruefen, ob `H(n)=(E,A,B,C)` gegen Catalan-Klammerung invariant bleibt.",
        "- Parallel eine explizit nicht-kanonische Toy-Observable auswerten,",
        "  die baumabhaengige Rekonstruktionspfade sichtbar machen kann.",
        "",
        "## Methodik (defensiv)",
        "",
        "- Fuer jedes `n` mit `Omega_tot(n)=k` gibt es theoretisch `C_{k-1}` Klammerungen.",
        "- Bei moderatem `C_{k-1}`: exhaustive Auswertung aller vollen Binaerbaeume.",
        "- Bei grossem `C_{k-1}`: deterministische Stichprobe (`sampled`) als Machbarkeitsmodus.",
        "- `H(n)` wird rein additiv ueber Blattbeitraege aggregiert.",
        "- Toy-Observable: Summe lokaler Balancing-Kosten `|log(L)-log(R)|` ueber innere Knoten.",
        "",
        "## Ergebnisueberblick",
        "",
        f"- Globales Invarianzresultat fuer `H(n)`: `{'ja' if all_h_invariant else 'nein'}`.",
        f"- Sichtbare Baumabhaengigkeit der Toy-Observable: `{'ja' if any_toy_dep else 'nein'}`.",
        f"- Exhaustive Faelle: `{len(exhaustive_rows)}`, sampled Faelle: `{len(sampled_rows)}`.",
        "",
        "## Detail je n",
        "",
    ]

    for row in rows:
        lines.append(
            "- "
            f"`n={row.n}`, `k={row.omega_tot}`, `C_(k-1)={row.catalan_expected}`, "
            f"mode=`{row.mode}`, trees=`{row.evaluated_trees}`, "
            f"`H`-invariant=`{'ja' if row.h_invariant else 'nein'}`, "
            f"toy-range=`{row.toy_range:.6f}`, toy-distinct=`{row.distinct_toy_values}`."
        )

    lines.extend(
        [
            "",
            "## Einordnung",
            "",
            "- Das positive Invarianzresultat fuer `H(n)` ist konsistent mit Additivitaet/Assoziativitaet,",
            "  aber als numerische Probe kein formaler Vollbeweis.",
            "- Die Toy-Observable dient nur als Demonstrator fuer rekonstruktionspfadabhaengige Groessen,",
            "  nicht als kanonische EABC- oder Hurwitz-Metrik.",
            "",
            "## Artefakte",
            "",
            "- `experiments/results/catalan_bridge/catalan_bracketing_invariance.csv`",
            "- `experiments/results/catalan_bridge/CATALAN_BRACKETING_INVARIANCE_REPORT.md`",
            "- `experiments/results/catalan_bridge/catalan_bracketing_invariance.png` (optional)",
            "",
            f"Plot erzeugt: `{'ja' if plot_written else 'nein (matplotlib nicht verfuegbar)'}`",
        ]
    )

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_catalan_4factor_demo(outdir: Path) -> None:
    factors: List[DemoFactor] = [
        DemoFactor(name="q1", h=(1, 0, 0, 0), norm=2.0),
        DemoFactor(name="q2", h=(0, 0, 0, 0), norm=1.0),
        DemoFactor(name="q3", h=(0, 1, 0, 0), norm=3.0),
        DemoFactor(name="q4", h=(0, 0, 1, 0), norm=5.0),
    ]
    names = [f.name for f in factors]
    trees = full_binary_trees_for_interval(0, len(factors))
    expr_to_tree = {tree_expr(t, names): t for t in trees}

    protocol_order = [
        ("P1", "(((q1*q2)*q3)*q4)"),
        ("P2", "((q1*(q2*q3))*q4)"),
        ("P3", "(q1*(q2*(q3*q4)))"),
        ("P4", "((q1*q2)*(q3*q4))"),
        ("P5", "(q1*((q2*q3)*q4))"),
    ]

    csv_path = outdir / "catalan_4factor_path_protocol.csv"
    md_path = outdir / "CATALAN_4FACTOR_PATH_PROTOCOL.md"

    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["path_id", "step", "expr", "signature", "norm", "kappa"],
        )
        writer.writeheader()
        for path_id, expr in protocol_order:
            tree = expr_to_tree[expr]
            h_end, norm_end, trace = eval_tree_demo(tree, factors)
            _ = h_end, norm_end
            for i, (node_expr, h, nrm, kappa) in enumerate(trace, start=1):
                writer.writerow(
                    {
                        "path_id": path_id,
                        "step": i,
                        "expr": node_expr,
                        "signature": str(h),
                        "norm": f"{nrm:.6f}",
                        "kappa": f"{kappa:.6f}",
                    }
                )

    lines: List[str] = [
        "# Catalan 4-Factor Path Protocol",
        "",
        "Defensive Demo-Auswertung fuer 4 Faktoren und 5 Catalan-Klammerungen.",
        "Die Auswertung ist rein algebraisch (`H` additiv, `norm` multiplikativ).",
        "",
        "## Demo-Faktoren",
        "",
        "- `q1`: `H=(1,0,0,0)`, `norm=2`, `kappa=0.5`",
        "- `q2`: `H=(0,0,0,0)`, `norm=1`, `kappa=1`",
        "- `q3`: `H=(0,1,0,0)`, `norm=3`, `kappa=0.333333`",
        "- `q4`: `H=(0,0,1,0)`, `norm=5`, `kappa=0.2`",
        "",
        "Endzustand fuer alle Pfade:",
        "- `H_end=(1,1,1,0)`",
        "- `norm_end=30`",
        "- `kappa_end=0.033333`",
        "",
        "## Pfadprotokolle",
        "",
    ]

    for path_id, expr in protocol_order:
        tree = expr_to_tree[expr]
        h_end, norm_end, trace = eval_tree_demo(tree, factors)
        kappas = [step[3] for step in trace]
        norms = [step[2] for step in trace]
        lines.append(f"### {path_id}: `{expr}`")
        lines.append("")
        for i, (node_expr, h, nrm, kappa) in enumerate(trace, start=1):
            lines.append(
                f"- Schritt {i}: `{node_expr}` -> `H={h}`, `norm={nrm:.6f}`, `kappa={kappa:.6f}`"
            )
        lines.append(
            f"- Pfadsequenz `norm`: `{', '.join(f'{x:.6f}' for x in norms)}`"
        )
        lines.append(
            f"- Pfadsequenz `kappa`: `{', '.join(f'{x:.6f}' for x in kappas)}`"
        )
        if path_id == "P3" and len(trace) >= 3:
            lines.append(
                "- Hinweis P3: vor dem letzten Merge liegen Teilsysteme mit `norm=2` und `norm=15` vor."
            )
        lines.append(
            f"- Endcheck: `H_end={h_end}`, `norm_end={norm_end:.6f}`, `kappa_end={1.0 / norm_end:.6f}`"
        )
        lines.append("")

    lines.extend(
        [
            "## Defensiver Befund",
            "",
            "- Endsignatur/-norm sind in dieser Demo klammerungsinvariant.",
            "- Zwischenverlaeufe der Geometrieproxies (`norm`, `kappa`) sind pfadabhaengig.",
            "- Die Demo zeigt numerische Evidenz, aber keinen Vollbeweis fuer allgemeine Observable-Klassen.",
            "",
            "## Artefakte",
            "",
            "- `experiments/results/catalan_bridge/catalan_4factor_path_protocol.csv`",
            "- `experiments/results/catalan_bridge/CATALAN_4FACTOR_PATH_PROTOCOL.md`",
        ]
    )

    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_int_list(raw: str) -> List[int]:
    out: List[int] = []
    for part in raw.split(","):
        s = part.strip()
        if not s:
            continue
        out.append(int(s))
    if not out:
        raise ValueError("Liste darf nicht leer sein.")
    return sorted(set(out))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Probe fuer Catalan-Klammerungsinvarianz von H(n).")
    parser.add_argument(
        "--n-list",
        type=str,
        default="60,72,84,90,120,180,210,360",
        help="Kommagetrennte n-Liste mit Omega_tot>=3.",
    )
    parser.add_argument(
        "--exhaustive-catalan-limit",
        type=int,
        default=5000,
        help="Bis zu diesem C_(k-1) wird exhaustiv ueber alle Baeume gerechnet.",
    )
    parser.add_argument(
        "--sample-trees",
        type=int,
        default=600,
        help="Anzahl Sample-Baeume je n, falls nicht-exhaustiv.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=20260625,
        help="Seed fuer sampled Baumziehung.",
    )
    parser.add_argument(
        "--outdir",
        type=Path,
        default=Path("experiments/results/catalan_bridge"),
        help="Output-Verzeichnis fuer CSV/MD/optional PNG.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    n_list = parse_int_list(args.n_list)
    if min(n_list) < 2:
        raise ValueError("Alle n muessen >= 2 sein.")
    if args.exhaustive_catalan_limit < 1:
        raise ValueError("exhaustive-catalan-limit muss >= 1 sein.")
    if args.sample_trees < 1:
        raise ValueError("sample-trees muss >= 1 sein.")

    outdir = args.outdir
    outdir.mkdir(parents=True, exist_ok=True)

    spf = smallest_prime_factors(max(n_list))
    rng = random.Random(args.seed)

    rows: List[ProbeRow] = []
    for n in n_list:
        factors = factor_multiset(n, spf)
        if len(factors) < 3:
            continue
        row = analyze_n(
            n=n,
            spf=spf,
            exhaustive_catalan_limit=args.exhaustive_catalan_limit,
            sample_trees=args.sample_trees,
            rng=rng,
        )
        rows.append(row)

    if not rows:
        raise ValueError("Keine gueltigen n mit Omega_tot>=3 nach Filter gefunden.")

    csv_path = outdir / "catalan_bracketing_invariance.csv"
    report_path = outdir / "CATALAN_BRACKETING_INVARIANCE_REPORT.md"
    plot_path = outdir / "catalan_bracketing_invariance.png"

    write_csv(csv_path, rows)
    plot_written = maybe_make_plot(plot_path, rows)
    write_report(report_path, rows, plot_written)
    write_catalan_4factor_demo(outdir)

    all_h_invariant = all(r.h_invariant for r in rows)
    any_toy_dep = any(r.toy_range > 1e-12 and r.distinct_toy_values > 1 for r in rows)
    print("Catalan bracketing invariance probe completed.")
    print(f"n_list={n_list}")
    print(f"rows={len(rows)}, all_h_invariant={all_h_invariant}, toy_dependence_seen={any_toy_dep}")
    print(f"outputs={outdir}")


if __name__ == "__main__":
    main()
