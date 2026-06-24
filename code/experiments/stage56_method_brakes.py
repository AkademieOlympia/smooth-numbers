#!/usr/bin/env python3
"""
Stage 5.6 Method Brakes
=======================

Defensive, reviewer-oriented follow-up block to Stage 5.5:
1) Quotient scaling R(Δr) = H_prime / H_wheel_cramer
2) Wheel-210 null test
3) HL-near reference analysis (proxy interface)
"""

from __future__ import annotations

import csv
import json
import math
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np

try:
    from scipy.optimize import curve_fit
except Exception:
    curve_fit = None

try:
    from scipy.stats import linregress
except Exception:
    linregress = None

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


REPO_ROOT = Path(__file__).resolve().parents[2]
RESULTS_DIR = REPO_ROOT / "experiments" / "results" / "stage56"
SCRIPT_OUT = Path(__file__).relative_to(REPO_ROOT)
CSV_OUT = RESULTS_DIR / "stage56_summary_table.csv"
PLOT_OUT = RESULTS_DIR / "stage56_plots.png"
MD_OUT = RESULTS_DIR / "STAGE56_METHOD_BRAKES.md"
JSON_OUT = RESULTS_DIR / "stage56_fit_details.json"

STAGE55_RUN_FILES: Sequence[Path] = [
    REPO_ROOT / "stage5.5_final_run.txt",        # N=1e6
    REPO_ROOT / "reproducibility_N10M.txt",      # N=1e7
    REPO_ROOT / "reproducibility_N20M.txt",      # N=2e7
]

HL_PROXY_FILE = REPO_ROOT / "reproducibility_stage6_N1M.txt"
DELTA_R_VALUES = [2, 6, 10, 14, 18]
PROJECTIONS = [2, 4, 6, 8]

WHEEL210_MODULUS = 210
WHEEL210_RANDOM_SEEDS = 6
WHEEL210_CRAMER_SEEDS = 6
BERNOULLI_BASELINE_TRIALS = 60
BERNOULLI_SEQ_LENGTH = 80_000


@dataclass
class RunData:
    n: int
    h_prime: Dict[int, float]
    h_wheel_random: Dict[int, float]
    h_wheel_cramer: Dict[int, float]


@dataclass
class FitResult:
    model_name: str
    params: Dict[str, float]
    param_se: Dict[str, float]
    r2: float
    aic: float
    bic: float
    sse: float
    y_hat: np.ndarray
    residuals: np.ndarray
    converged: bool
    note: str = ""


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
    for dr, val in re.findall(r"Δr=(\d+):\s*H_WheelCram[ée]r\s*=\s*([0-9.]+)", text):
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
        if line.startswith("Correlation:"):
            section = None
            continue
        m = re.match(r"^(\d+)\s+([0-9.]+)\s+([0-9.]+)$", line)
        if section and m:
            dr = int(m.group(1))
            proxy_val = float(m.group(3))
            if section == "k3":
                h_k3[dr] = proxy_val
            else:
                h_k4[dr] = proxy_val
    return h_k3, h_k4


def fit_linear(x: np.ndarray, y: np.ndarray) -> FitResult:
    if len(x) < 3:
        nan = np.full_like(y, np.nan, dtype=float)
        return FitResult(
            model_name="linear",
            params={"a": math.nan, "b": math.nan},
            param_se={"a": math.nan, "b": math.nan},
            r2=math.nan,
            aic=math.nan,
            bic=math.nan,
            sse=math.nan,
            y_hat=nan,
            residuals=nan,
            converged=False,
            note="Zu wenige Punkte fuer linearen Fit.",
        )

    if linregress is not None:
        fit = linregress(x, y)
        b = float(fit.slope)
        a = float(fit.intercept)
        b_se = float(getattr(fit, "stderr", math.nan))
        a_se = float(getattr(fit, "intercept_stderr", math.nan))
    else:
        coeffs, cov = np.polyfit(x, y, 1, cov=True)
        b = float(coeffs[0])
        a = float(coeffs[1])
        b_se = float(math.sqrt(max(cov[0, 0], 0.0)))
        a_se = float(math.sqrt(max(cov[1, 1], 0.0)))

    y_hat = a + b * x
    residuals = y - y_hat
    sse = float(np.sum(residuals ** 2))
    sst = float(np.sum((y - np.mean(y)) ** 2))
    r2 = float(1.0 - sse / sst) if sst > 0 else math.nan
    n = len(y)
    k = 2
    sigma2 = max(sse / n, 1e-16)
    aic = float(n * math.log(sigma2) + 2 * k)
    bic = float(n * math.log(sigma2) + k * math.log(n))

    return FitResult(
        model_name="linear",
        params={"a": a, "b": b},
        param_se={"a": a_se, "b": b_se},
        r2=r2,
        aic=aic,
        bic=bic,
        sse=sse,
        y_hat=y_hat,
        residuals=residuals,
        converged=True,
    )


def model_power_ax(x: np.ndarray, a: float, alpha: float) -> np.ndarray:
    return a * np.power(x, alpha)


def model_power_one_plus(x: np.ndarray, c: float, alpha: float) -> np.ndarray:
    return 1.0 + c * np.power(x, alpha)


def fit_power(x: np.ndarray, y: np.ndarray, one_plus: bool) -> FitResult:
    model_name = "power_one_plus" if one_plus else "power_ax"
    if len(x) < 3:
        nan = np.full_like(y, np.nan, dtype=float)
        return FitResult(
            model_name=model_name,
            params={"c" if one_plus else "a": math.nan, "alpha": math.nan},
            param_se={"c" if one_plus else "a": math.nan, "alpha": math.nan},
            r2=math.nan,
            aic=math.nan,
            bic=math.nan,
            sse=math.nan,
            y_hat=nan,
            residuals=nan,
            converged=False,
            note="Zu wenige Punkte fuer Potenz-Fit.",
        )

    if curve_fit is None:
        # Fallback: Log-linear nur fuer a*x^alpha mit y>0
        if one_plus:
            nan = np.full_like(y, np.nan, dtype=float)
            return FitResult(
                model_name=model_name,
                params={"c": math.nan, "alpha": math.nan},
                param_se={"c": math.nan, "alpha": math.nan},
                r2=math.nan,
                aic=math.nan,
                bic=math.nan,
                sse=math.nan,
                y_hat=nan,
                residuals=nan,
                converged=False,
                note="curve_fit nicht verfuegbar (one_plus).",
            )
        if np.any(y <= 0):
            nan = np.full_like(y, np.nan, dtype=float)
            return FitResult(
                model_name=model_name,
                params={"a": math.nan, "alpha": math.nan},
                param_se={"a": math.nan, "alpha": math.nan},
                r2=math.nan,
                aic=math.nan,
                bic=math.nan,
                sse=math.nan,
                y_hat=nan,
                residuals=nan,
                converged=False,
                note="Nichtpositive y fuer log-Fallback.",
            )
        lx = np.log(x)
        ly = np.log(y)
        coeffs, cov = np.polyfit(lx, ly, 1, cov=True)
        alpha = float(coeffs[0])
        loga = float(coeffs[1])
        a = float(math.exp(loga))
        alpha_se = float(math.sqrt(max(cov[0, 0], 0.0)))
        a_se = float(a * math.sqrt(max(cov[1, 1], 0.0)))
        y_hat = model_power_ax(x, a, alpha)
        residuals = y - y_hat
    else:
        try:
            if one_plus:
                p0 = [0.1, 0.8]
                bounds = ([-10.0, -4.0], [10.0, 4.0])
                popt, pcov = curve_fit(model_power_one_plus, x, y, p0=p0, bounds=bounds, maxfev=40_000)
                c, alpha = float(popt[0]), float(popt[1])
                c_se = float(math.sqrt(max(pcov[0, 0], 0.0)))
                alpha_se = float(math.sqrt(max(pcov[1, 1], 0.0)))
                y_hat = model_power_one_plus(x, c, alpha)
                residuals = y - y_hat
                params = {"c": c, "alpha": alpha}
                param_se = {"c": c_se, "alpha": alpha_se}
            else:
                p0 = [max(float(np.mean(y)), 1e-8), 0.8]
                bounds = ([1e-12, -4.0], [50.0, 4.0])
                popt, pcov = curve_fit(model_power_ax, x, y, p0=p0, bounds=bounds, maxfev=40_000)
                a, alpha = float(popt[0]), float(popt[1])
                a_se = float(math.sqrt(max(pcov[0, 0], 0.0)))
                alpha_se = float(math.sqrt(max(pcov[1, 1], 0.0)))
                y_hat = model_power_ax(x, a, alpha)
                residuals = y - y_hat
                params = {"a": a, "alpha": alpha}
                param_se = {"a": a_se, "alpha": alpha_se}
        except Exception as exc:
            nan = np.full_like(y, np.nan, dtype=float)
            return FitResult(
                model_name=model_name,
                params={"c" if one_plus else "a": math.nan, "alpha": math.nan},
                param_se={"c" if one_plus else "a": math.nan, "alpha": math.nan},
                r2=math.nan,
                aic=math.nan,
                bic=math.nan,
                sse=math.nan,
                y_hat=nan,
                residuals=nan,
                converged=False,
                note=f"curve_fit fehlgeschlagen: {exc}",
            )

    sse = float(np.sum(residuals ** 2))
    sst = float(np.sum((y - np.mean(y)) ** 2))
    r2 = float(1.0 - sse / sst) if sst > 0 else math.nan
    n = len(y)
    k = 2
    sigma2 = max(sse / n, 1e-16)
    aic = float(n * math.log(sigma2) + 2 * k)
    bic = float(n * math.log(sigma2) + k * math.log(n))

    return FitResult(
        model_name=model_name,
        params=params,
        param_se=param_se,
        r2=r2,
        aic=aic,
        bic=bic,
        sse=sse,
        y_hat=y_hat,
        residuals=residuals,
        converged=True,
    )


def choose_best_power_fit(x: np.ndarray, y: np.ndarray) -> FitResult:
    fit_ax = fit_power(x, y, one_plus=False)
    fit_one = fit_power(x, y, one_plus=True)
    candidates = [f for f in [fit_ax, fit_one] if f.converged and not math.isnan(f.aic)]
    if not candidates:
        return fit_one if fit_one.converged else fit_ax
    return min(candidates, key=lambda f: f.aic)


def sieve_primes_upto(n: int) -> np.ndarray:
    if n < 2:
        return np.array([], dtype=np.int64)
    is_prime = np.ones(n + 1, dtype=bool)
    is_prime[:2] = False
    lim = int(math.isqrt(n))
    for p in range(2, lim + 1):
        if is_prime[p]:
            is_prime[p * p:n + 1:p] = False
    return np.flatnonzero(is_prime).astype(np.int64)


def wheel_residues(modulus: int) -> np.ndarray:
    residues = [r for r in range(1, modulus) if math.gcd(r, modulus) == 1]
    return np.array(sorted(residues), dtype=np.int64)


def generate_wheel_numbers(n: int, modulus: int, residues: np.ndarray) -> np.ndarray:
    blocks = np.arange(0, n // modulus + 1, dtype=np.int64)
    grid = modulus * blocks[:, None] + residues[None, :]
    values = grid.ravel()
    values = values[(values >= 1) & (values <= n)]
    values.sort()
    return values


def typical_gaps_for_wheel(modulus: int, residues: np.ndarray) -> np.ndarray:
    r = np.sort(residues)
    diffs = np.diff(np.concatenate([r, [r[0] + modulus]]))
    uniq = sorted({int(v) for v in diffs if v > 0 and v % 2 == 0})
    return np.array(uniq, dtype=np.int64)


def compute_R_gap(gaps: np.ndarray, delta_r: int, base_offsets: Sequence[int], modulus: int) -> float:
    if len(gaps) < 2:
        return math.nan
    target = set(base_offsets + [g + delta_r for g in base_offsets])
    g1 = gaps[:-1]
    g2 = gaps[1:]
    mask = np.isin(g1, list(target)) & np.isin(g2, list(target))
    if not np.any(mask):
        return math.nan
    r1 = np.mod(g1[mask], modulus)
    r2 = np.mod(g2[mask], modulus)
    dist = np.abs(r1 - r2)
    dist = np.minimum(dist, modulus - dist)
    match = int(np.sum(dist == delta_r))
    total = int(np.sum(mask))
    nomatch = total - match
    if nomatch <= 0:
        return math.nan
    return float(match / nomatch)


def compute_H_from_sequence(
    sequence: np.ndarray,
    delta_r_values: Sequence[int],
    projections: Sequence[int],
    bernoulli_baselines: Dict[Tuple[int, int], float],
    modulus: int,
) -> Dict[int, float]:
    if len(sequence) < 3:
        return {dr: math.nan for dr in delta_r_values}
    gaps = np.diff(sequence)
    out: Dict[int, float] = {}
    for dr in delta_r_values:
        a_vals: List[float] = []
        for base in projections:
            key = (dr, base)
            base_offsets = [base, base + 2, base + 4]
            baseline = bernoulli_baselines.get(key, math.nan)
            if baseline <= 0 or math.isnan(baseline):
                continue
            r_seq = compute_R_gap(gaps, dr, base_offsets, modulus)
            if math.isnan(r_seq):
                continue
            a_vals.append(r_seq / baseline)
        out[dr] = float(np.mean(a_vals)) if a_vals else math.nan
    return out


def compute_bernoulli_baselines(
    delta_r_values: Sequence[int],
    projections: Sequence[int],
    modulus: int,
    typical_gaps: np.ndarray,
    num_trials: int,
    seq_length: int,
    seed: int = 1729,
) -> Dict[Tuple[int, int], float]:
    rng = np.random.default_rng(seed)
    baselines: Dict[Tuple[int, int], float] = {}
    for dr in delta_r_values:
        for base in projections:
            base_offsets = [base, base + 2, base + 4]
            rs: List[float] = []
            for _ in range(num_trials):
                random_gaps = rng.choice(typical_gaps, size=seq_length, replace=True)
                r_val = compute_R_gap(random_gaps, dr, base_offsets, modulus)
                if not math.isnan(r_val):
                    rs.append(r_val)
            baselines[(dr, base)] = float(np.mean(rs)) if rs else math.nan
    return baselines


def nanmean_std(vals: Sequence[float]) -> Tuple[float, float]:
    arr = np.array(vals, dtype=float)
    arr = arr[~np.isnan(arr)]
    if len(arr) == 0:
        return math.nan, math.nan
    if len(arr) == 1:
        return float(arr[0]), math.nan
    return float(np.mean(arr)), float(np.std(arr, ddof=1))


def run_wheel210_controls_for_n(
    n: int,
    delta_r_values: Sequence[int],
    projections: Sequence[int],
    seeds_random: int,
    seeds_cramer: int,
) -> Dict[str, Dict[int, Dict[str, float]]]:
    primes = sieve_primes_upto(n)
    prime_density = len(primes) / n if n > 0 else 0.0
    residues = wheel_residues(WHEEL210_MODULUS)
    wheel_vals = generate_wheel_numbers(n, WHEEL210_MODULUS, residues)
    # Defensive choice: broad even-gap support for the Bernoulli baseline.
    # If baseline gaps are too narrow (e.g. only primitive wheel micro-gaps),
    # higher Δr classes can become numerically degenerate.
    primitive_gaps = typical_gaps_for_wheel(WHEEL210_MODULUS, residues)
    broad_even_gaps = np.arange(2, 62, 2, dtype=np.int64)
    typical_gaps = np.array(sorted(set(primitive_gaps.tolist()) | set(broad_even_gaps.tolist())), dtype=np.int64)

    baselines = compute_bernoulli_baselines(
        delta_r_values=delta_r_values,
        projections=projections,
        modulus=WHEEL210_MODULUS,
        typical_gaps=typical_gaps,
        num_trials=BERNOULLI_BASELINE_TRIALS,
        seq_length=BERNOULLI_SEQ_LENGTH,
    )

    h_random_runs: List[Dict[int, float]] = []
    h_cramer_runs: List[Dict[int, float]] = []

    for seed in range(seeds_random):
        rng = np.random.default_rng(10_000 + seed + n)
        mask = rng.random(len(wheel_vals)) < prime_density
        seq = wheel_vals[mask]
        h_random_runs.append(
            compute_H_from_sequence(seq, delta_r_values, projections, baselines, WHEEL210_MODULUS)
        )

    for seed in range(seeds_cramer):
        rng = np.random.default_rng(20_000 + seed + n)
        x = np.maximum(wheel_vals, 3)
        p = 2.0 / np.log(x)
        p = np.clip(p, 0.0, 1.0)
        mask = rng.random(len(wheel_vals)) < p
        seq = wheel_vals[mask]
        h_cramer_runs.append(
            compute_H_from_sequence(seq, delta_r_values, projections, baselines, WHEEL210_MODULUS)
        )

    random_stats: Dict[int, Dict[str, float]] = {}
    cramer_stats: Dict[int, Dict[str, float]] = {}
    for dr in delta_r_values:
        mean_r, std_r = nanmean_std([run.get(dr, math.nan) for run in h_random_runs])
        mean_c, std_c = nanmean_std([run.get(dr, math.nan) for run in h_cramer_runs])
        random_stats[dr] = {"mean": mean_r, "std": std_r}
        cramer_stats[dr] = {"mean": mean_c, "std": std_c}

    return {
        "random": random_stats,
        "cramer": cramer_stats,
        "meta": {
            "prime_density": prime_density,
            "wheel_count": float(len(wheel_vals)),
            "typical_gap_count": float(len(typical_gaps)),
        },
    }


def fit_ols_metrics(y: np.ndarray, x_columns: List[np.ndarray], names: List[str]) -> Dict[str, float]:
    n = len(y)
    x = np.column_stack([np.ones(n)] + x_columns)
    beta, _, _, _ = np.linalg.lstsq(x, y, rcond=None)
    y_hat = x @ beta
    resid = y - y_hat
    sse = float(np.sum(resid ** 2))
    sst = float(np.sum((y - np.mean(y)) ** 2))
    r2 = float(1.0 - sse / sst) if sst > 0 else math.nan
    k = x.shape[1]
    sigma2 = max(sse / n, 1e-16)
    aic = float(n * math.log(sigma2) + 2 * k)
    bic = float(n * math.log(sigma2) + k * math.log(n))

    xtx_inv = np.linalg.pinv(x.T @ x)
    dof = max(n - k, 1)
    sigma2_unbiased = sse / dof
    cov = sigma2_unbiased * xtx_inv
    se = np.sqrt(np.clip(np.diag(cov), 0.0, None))

    out = {
        "n": float(n),
        "k": float(k),
        "r2": r2,
        "aic": aic,
        "bic": bic,
        "sse": sse,
    }
    out["intercept"] = float(beta[0])
    out["intercept_se"] = float(se[0]) if len(se) > 0 else math.nan
    for i, name in enumerate(names, start=1):
        out[name] = float(beta[i])
        out[f"{name}_se"] = float(se[i]) if i < len(se) else math.nan
    return out


def main() -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    runs: List[RunData] = []
    missing: List[str] = []
    for p in STAGE55_RUN_FILES:
        if p.exists():
            runs.append(parse_stage55_run(p))
        else:
            missing.append(str(p.relative_to(REPO_ROOT)))

    if not runs:
        raise RuntimeError("Keine Stage-5.5-Runs gefunden.")
    runs.sort(key=lambda r: r.n)

    common_dr = sorted(set.intersection(*[set(r.h_prime.keys()) for r in runs]))
    common_dr = [dr for dr in common_dr if dr in DELTA_R_VALUES]
    if len(common_dr) < 3:
        raise RuntimeError("Zu wenige gemeinsame Δr-Werte fuer stabile Fits.")

    # A) Quotient scaling fits
    quotient_fits: Dict[str, Dict[str, Dict[str, object]]] = {}
    pooled_x: List[float] = []
    pooled_y: List[float] = []

    for run in runs:
        x = np.array(common_dr, dtype=float)
        y = np.array([run.h_prime[dr] / run.h_wheel_cramer[dr] for dr in common_dr], dtype=float)
        pooled_x.extend(x.tolist())
        pooled_y.extend(y.tolist())

        f_lin = fit_linear(x, y)
        f_pow = choose_best_power_fit(x, y)
        quotient_fits[str(run.n)] = {
            "linear": {
                "params": f_lin.params,
                "param_se": f_lin.param_se,
                "r2": f_lin.r2,
                "aic": f_lin.aic,
                "bic": f_lin.bic,
                "sse": f_lin.sse,
                "residuals": f_lin.residuals.tolist(),
                "fitted": f_lin.y_hat.tolist(),
                "note": f_lin.note,
                "converged": f_lin.converged,
            },
            "power": {
                "model_name": f_pow.model_name,
                "params": f_pow.params,
                "param_se": f_pow.param_se,
                "r2": f_pow.r2,
                "aic": f_pow.aic,
                "bic": f_pow.bic,
                "sse": f_pow.sse,
                "residuals": f_pow.residuals.tolist(),
                "fitted": f_pow.y_hat.tolist(),
                "note": f_pow.note,
                "converged": f_pow.converged,
            },
        }

    x_pool = np.array(pooled_x, dtype=float)
    y_pool = np.array(pooled_y, dtype=float)
    f_lin_pool = fit_linear(x_pool, y_pool)
    f_pow_pool = choose_best_power_fit(x_pool, y_pool)
    quotient_fits["pooled"] = {
        "linear": {
            "params": f_lin_pool.params,
            "param_se": f_lin_pool.param_se,
            "r2": f_lin_pool.r2,
            "aic": f_lin_pool.aic,
            "bic": f_lin_pool.bic,
            "sse": f_lin_pool.sse,
            "residuals": f_lin_pool.residuals.tolist(),
            "fitted": f_lin_pool.y_hat.tolist(),
            "note": f_lin_pool.note,
            "converged": f_lin_pool.converged,
        },
        "power": {
            "model_name": f_pow_pool.model_name,
            "params": f_pow_pool.params,
            "param_se": f_pow_pool.param_se,
            "r2": f_pow_pool.r2,
            "aic": f_pow_pool.aic,
            "bic": f_pow_pool.bic,
            "sse": f_pow_pool.sse,
            "residuals": f_pow_pool.residuals.tolist(),
            "fitted": f_pow_pool.y_hat.tolist(),
            "note": f_pow_pool.note,
            "converged": f_pow_pool.converged,
        },
    }

    # B) Wheel-210 null test
    wheel210_by_n: Dict[str, Dict[str, Dict[int, Dict[str, float]]]] = {}
    for run in runs:
        wheel210_by_n[str(run.n)] = run_wheel210_controls_for_n(
            n=run.n,
            delta_r_values=common_dr,
            projections=PROJECTIONS,
            seeds_random=WHEEL210_RANDOM_SEEDS,
            seeds_cramer=WHEEL210_CRAMER_SEEDS,
        )

    # C) HL-near proxy analysis
    h_k3_proxy, h_k4_proxy = parse_hl_proxies(HL_PROXY_FILE)
    hl_by_n: Dict[str, Dict[str, float]] = {}
    hl_status = "open"
    if all(dr in h_k3_proxy for dr in common_dr) and all(dr in h_k4_proxy for dr in common_dr):
        hl_status = "proxy_available"
        for run in runs:
            y = np.array([run.h_prime[dr] - run.h_wheel_cramer[dr] for dr in common_dr], dtype=float)
            x_dr = np.array(common_dr, dtype=float)
            x_k3 = np.array([h_k3_proxy[dr] for dr in common_dr], dtype=float)
            x_k4 = np.array([h_k4_proxy[dr] for dr in common_dr], dtype=float)

            base = fit_ols_metrics(y, [x_dr], names=["dr"])
            with_k3 = fit_ols_metrics(y, [x_dr, x_k3], names=["dr", "k3"])
            with_k4 = fit_ols_metrics(y, [x_dr, x_k4], names=["dr", "k4"])
            hl_by_n[str(run.n)] = {
                **{f"base_{k}": v for k, v in base.items()},
                **{f"k3_{k}": v for k, v in with_k3.items()},
                **{f"k4_{k}": v for k, v in with_k4.items()},
                "k3_aic_gain": base["aic"] - with_k3["aic"],
                "k4_aic_gain": base["aic"] - with_k4["aic"],
                "k3_r2_gain": with_k3["r2"] - base["r2"],
                "k4_r2_gain": with_k4["r2"] - base["r2"],
            }
    else:
        hl_status = "proxy_missing_or_incomplete"

    # Summary CSV
    csv_rows: List[Dict[str, object]] = []

    for scale_key, payload in quotient_fits.items():
        for model_key in ["linear", "power"]:
            m = payload[model_key]
            params = m.get("params", {})
            se = m.get("param_se", {})
            param_txt = ";".join([f"{k}={params[k]:.8g}" for k in sorted(params)])
            se_txt = ";".join([f"{k}_se={se[k]:.8g}" for k in sorted(se)])
            csv_rows.append(
                {
                    "section": "A_quotient_scaling",
                    "scale": scale_key,
                    "model": m.get("model_name", model_key),
                    "metric": "fit",
                    "delta_r": "",
                    "value": "",
                    "std_or_se": "",
                    "r2": f"{m.get('r2', math.nan):.8g}",
                    "aic": f"{m.get('aic', math.nan):.8g}",
                    "bic": f"{m.get('bic', math.nan):.8g}",
                    "notes": f"{param_txt} | {se_txt}",
                }
            )

    for run in runs:
        n_key = str(run.n)
        for dr in common_dr:
            hp = run.h_prime[dr]
            for model in ["random", "cramer"]:
                h210_mean = wheel210_by_n[n_key][model][dr]["mean"]
                h210_std = wheel210_by_n[n_key][model][dr]["std"]
                delta_h = hp - h210_mean if not math.isnan(h210_mean) else math.nan
                r210 = hp / h210_mean if (not math.isnan(h210_mean) and h210_mean != 0) else math.nan
                csv_rows.append(
                    {
                        "section": "B_wheel210",
                        "scale": n_key,
                        "model": f"wheel210_{model}",
                        "metric": "H_wheel210",
                        "delta_r": dr,
                        "value": f"{h210_mean:.8g}" if not math.isnan(h210_mean) else "nan",
                        "std_or_se": f"{h210_std:.8g}" if not math.isnan(h210_std) else "nan",
                        "r2": "",
                        "aic": "",
                        "bic": "",
                        "notes": "",
                    }
                )
                csv_rows.append(
                    {
                        "section": "B_wheel210",
                        "scale": n_key,
                        "model": f"wheel210_{model}",
                        "metric": "deltaH_210",
                        "delta_r": dr,
                        "value": f"{delta_h:.8g}" if not math.isnan(delta_h) else "nan",
                        "std_or_se": "",
                        "r2": "",
                        "aic": "",
                        "bic": "",
                        "notes": "",
                    }
                )
                csv_rows.append(
                    {
                        "section": "B_wheel210",
                        "scale": n_key,
                        "model": f"wheel210_{model}",
                        "metric": "R_210",
                        "delta_r": dr,
                        "value": f"{r210:.8g}" if not math.isnan(r210) else "nan",
                        "std_or_se": "",
                        "r2": "",
                        "aic": "",
                        "bic": "",
                        "notes": "",
                    }
                )

    if hl_by_n:
        for n_key, stats in hl_by_n.items():
            csv_rows.append(
                {
                    "section": "C_hl_proxy",
                    "scale": n_key,
                    "model": "baseline_vs_proxy",
                    "metric": "k3_aic_gain",
                    "delta_r": "",
                    "value": f"{stats['k3_aic_gain']:.8g}",
                    "std_or_se": "",
                    "r2": f"{stats['k3_r2_gain']:.8g}",
                    "aic": "",
                    "bic": "",
                    "notes": "gain > 0 favors proxy-augmented model",
                }
            )
            csv_rows.append(
                {
                    "section": "C_hl_proxy",
                    "scale": n_key,
                    "model": "baseline_vs_proxy",
                    "metric": "k4_aic_gain",
                    "delta_r": "",
                    "value": f"{stats['k4_aic_gain']:.8g}",
                    "std_or_se": "",
                    "r2": f"{stats['k4_r2_gain']:.8g}",
                    "aic": "",
                    "bic": "",
                    "notes": "gain > 0 favors proxy-augmented model",
                }
            )
    else:
        csv_rows.append(
            {
                "section": "C_hl_proxy",
                "scale": "all",
                "model": "status",
                "metric": "proxy_status",
                "delta_r": "",
                "value": hl_status,
                "std_or_se": "",
                "r2": "",
                "aic": "",
                "bic": "",
                "notes": "TODO: Stage 6 robust HL module",
            }
        )

    with CSV_OUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "section",
                "scale",
                "model",
                "metric",
                "delta_r",
                "value",
                "std_or_se",
                "r2",
                "aic",
                "bic",
                "notes",
            ],
        )
        writer.writeheader()
        writer.writerows(csv_rows)

    # Plot
    fig, axes = plt.subplots(2, 2, figsize=(16, 11))
    fig.suptitle("Stage 5.6 Method Brakes", fontsize=15, fontweight="bold")

    # A1: Quotient scaling with pooled fits
    ax = axes[0, 0]
    colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#9467bd"]
    for i, run in enumerate(runs):
        x = np.array(common_dr, dtype=float)
        y = np.array([run.h_prime[dr] / run.h_wheel_cramer[dr] for dr in common_dr], dtype=float)
        ax.plot(x, y, "o-", color=colors[i % len(colors)], label=f"N={run.n:,}", alpha=0.85)

    x_line = np.linspace(min(common_dr), max(common_dr), 200)
    pool_linear = quotient_fits["pooled"]["linear"]
    a_lin = pool_linear["params"]["a"]
    b_lin = pool_linear["params"]["b"]
    y_lin = a_lin + b_lin * x_line
    ax.plot(x_line, y_lin, "--", color="black", lw=1.8, label="Pooled linear")

    pool_power = quotient_fits["pooled"]["power"]
    if pool_power["model_name"] == "power_ax":
        a = pool_power["params"]["a"]
        alpha = pool_power["params"]["alpha"]
        y_pow = model_power_ax(x_line, a, alpha)
    else:
        c = pool_power["params"]["c"]
        alpha = pool_power["params"]["alpha"]
        y_pow = model_power_one_plus(x_line, c, alpha)
    ax.plot(x_line, y_pow, ":", color="#d62728", lw=2.0, label=f"Pooled {pool_power['model_name']}")

    ax.set_title("A) R(Δr)=H_prime/H_wheel_cramer")
    ax.set_xlabel("Δr")
    ax.set_ylabel("R(Δr)")
    ax.grid(alpha=0.3)
    ax.legend(fontsize=9)

    # A2: Residuals pooled
    ax = axes[0, 1]
    x_pool_arr = np.array(pooled_x, dtype=float)
    res_lin = np.array(pool_linear["residuals"], dtype=float)
    res_pow = np.array(pool_power["residuals"], dtype=float)
    ax.scatter(x_pool_arr - 0.2, res_lin, s=40, alpha=0.75, label="Linear residuals")
    ax.scatter(x_pool_arr + 0.2, res_pow, s=40, alpha=0.75, label=f"{pool_power['model_name']} residuals")
    ax.axhline(0.0, color="black", linestyle="--", lw=1.0)
    ax.set_title("A) Residual diagnostics (pooled)")
    ax.set_xlabel("Δr")
    ax.set_ylabel("Residual")
    ax.grid(alpha=0.3)
    ax.legend(fontsize=9)

    # B1: Wheel-210 ratio comparison for largest N
    ax = axes[1, 0]
    run_ref = runs[-1]
    n_ref_key = str(run_ref.n)
    hp = np.array([run_ref.h_prime[dr] for dr in common_dr], dtype=float)
    r_rand = []
    r_cram = []
    for dr in common_dr:
        h_rand = wheel210_by_n[n_ref_key]["random"][dr]["mean"]
        h_cram = wheel210_by_n[n_ref_key]["cramer"][dr]["mean"]
        r_rand.append(hp[common_dr.index(dr)] / h_rand if h_rand and not math.isnan(h_rand) else math.nan)
        r_cram.append(hp[common_dr.index(dr)] / h_cram if h_cram and not math.isnan(h_cram) else math.nan)
    ax.plot(common_dr, r_rand, "o-", label=f"R_210 random (N={run_ref.n:,})", alpha=0.8)
    ax.plot(common_dr, r_cram, "s-", label=f"R_210 cramer (N={run_ref.n:,})", alpha=0.8)
    ax.axhline(1.0, color="black", linestyle="--", lw=1.0)
    ax.set_title("B) Wheel-210 Nulltest: R_210")
    ax.set_xlabel("Δr")
    ax.set_ylabel("R_210 = H_prime / H_wheel210")
    ax.grid(alpha=0.3)
    ax.legend(fontsize=9)

    # C1: HL proxy gain by scale
    ax = axes[1, 1]
    if hl_by_n:
        x_pos = np.arange(len(runs))
        k3_gain = [hl_by_n[str(run.n)]["k3_aic_gain"] for run in runs]
        k4_gain = [hl_by_n[str(run.n)]["k4_aic_gain"] for run in runs]
        width = 0.35
        ax.bar(x_pos - width / 2, k3_gain, width=width, label="AIC gain with k3 proxy", alpha=0.8)
        ax.bar(x_pos + width / 2, k4_gain, width=width, label="AIC gain with k4 proxy", alpha=0.8)
        ax.axhline(0.0, color="black", linestyle="--", lw=1.0)
        ax.set_xticks(x_pos)
        ax.set_xticklabels([f"N={run.n:,}" for run in runs], rotation=0)
        ax.set_ylabel("AIC gain vs baseline")
        ax.set_title("C) HL-proxy defensiver Mehrwerttest")
        ax.legend(fontsize=9)
        ax.grid(alpha=0.3, axis="y")
    else:
        ax.text(0.5, 0.5, "Kein robuster HL-Proxy verfuegbar\nTODO fuer Stage 6", ha="center", va="center")
        ax.set_title("C) HL-proxy defensiver Mehrwerttest")
        ax.set_xticks([])
        ax.set_yticks([])

    plt.tight_layout()
    plt.savefig(PLOT_OUT, dpi=180, bbox_inches="tight")

    # JSON details
    details = {
        "inputs": {
            "stage55_runs": [str(p.relative_to(REPO_ROOT)) for p in STAGE55_RUN_FILES if p.exists()],
            "missing_runs": missing,
            "delta_r_values": common_dr,
        },
        "quotient_fits": quotient_fits,
        "wheel210": wheel210_by_n,
        "hl_proxy_status": hl_status,
        "hl_proxy_fits": hl_by_n,
        "config": {
            "wheel210_random_seeds": WHEEL210_RANDOM_SEEDS,
            "wheel210_cramer_seeds": WHEEL210_CRAMER_SEEDS,
            "bernoulli_trials": BERNOULLI_BASELINE_TRIALS,
            "bernoulli_seq_length": BERNOULLI_SEQ_LENGTH,
        },
    }
    JSON_OUT.write_text(json.dumps(details, indent=2), encoding="utf-8")

    # Markdown report
    lines: List[str] = []
    lines.append("# Stage 5.6 Method Brakes")
    lines.append("")
    lines.append("## Datenbasis und Scope")
    lines.append("")
    lines.append("- Verwendete Stage-5.5-Skalen: " + ", ".join([f"`N={run.n:,}`" for run in runs]))
    lines.append("- Δr-Klassen: " + ", ".join([f"`{dr}`" for dr in common_dr]))
    lines.append("- Methodik defensiv: kleine Δr-Stichprobe (`n=5` je Skala), daher keine starken Extrapolationen.")
    if missing:
        lines.append("- Nicht gefunden (optional): " + ", ".join([f"`{m}`" for m in missing]))
    lines.append("")
    lines.append("## A) Quotienten-Skalierung `R(Δr)=H_prime/H_wheel_cramer`")
    lines.append("")
    lines.append("- Modelle: linear `R=a+b·Δr` sowie Potenz (`a·Δr^alpha` oder `1+c·Δr^alpha`).")
    lines.append("- Reported: Parameter ± Unsicherheit (SE), `R²`, `AIC`, `BIC`, Residuen.")
    lines.append("")
    lines.append("| Skala | Modell | Parameter | R² | AIC | BIC |")
    lines.append("|---|---|---|---:|---:|---:|")
    for key in [str(r.n) for r in runs] + ["pooled"]:
        lin = quotient_fits[key]["linear"]
        powf = quotient_fits[key]["power"]
        p_lin = lin["params"]
        s_lin = lin["param_se"]
        lines.append(
            f"| {key} | linear | a={p_lin['a']:.5f}±{s_lin['a']:.5f}, b={p_lin['b']:.5f}±{s_lin['b']:.5f} | "
            f"{lin['r2']:.3f} | {lin['aic']:.2f} | {lin['bic']:.2f} |"
        )
        if powf["model_name"] == "power_ax":
            p_txt = f"a={powf['params']['a']:.5f}±{powf['param_se']['a']:.5f}, alpha={powf['params']['alpha']:.5f}±{powf['param_se']['alpha']:.5f}"
        else:
            p_txt = f"c={powf['params']['c']:.5f}±{powf['param_se']['c']:.5f}, alpha={powf['params']['alpha']:.5f}±{powf['param_se']['alpha']:.5f}"
        lines.append(
            f"| {key} | {powf['model_name']} | {p_txt} | {powf['r2']:.3f} | {powf['aic']:.2f} | {powf['bic']:.2f} |"
        )
    lines.append("")
    lines.append(
        "- Bewertungslogik: niedrigeres `AIC/BIC` ist besser; bei sehr kleinem `n` nur als robuste Tendenz lesen, nicht als harte Modellselektion."
    )
    lines.append("")
    lines.append("## B) Wheel-210 Nulltest")
    lines.append("")
    lines.append(
        "- Wheel-210 Kontrollmodelle (`2·3·5·7`): `H_wheel210_random` und `H_wheel210_cramer` "
        f"mit je `{WHEEL210_RANDOM_SEEDS}`/`{WHEEL210_CRAMER_SEEDS}` Seeds."
    )
    lines.append("- Kenngroessen je Δr: `ΔH_210 = H_prime - H_wheel210_*`, `R_210 = H_prime / H_wheel210_*`.")
    lines.append("")
    lines.append("| N | Modell | mean(R_210) ueber Δr | min(R_210) | max(R_210) |")
    lines.append("|---:|---|---:|---:|---:|")
    for run in runs:
        n_key = str(run.n)
        for model in ["random", "cramer"]:
            ratios = []
            for dr in common_dr:
                h210 = wheel210_by_n[n_key][model][dr]["mean"]
                hp = run.h_prime[dr]
                if not math.isnan(h210) and h210 != 0:
                    ratios.append(hp / h210)
            if ratios:
                lines.append(
                    f"| {run.n:,} | wheel210_{model} | {np.mean(ratios):.3f} | {np.min(ratios):.3f} | {np.max(ratios):.3f} |"
                )
            else:
                lines.append(f"| {run.n:,} | wheel210_{model} | n/a | n/a | n/a |")
    lines.append("")
    lines.append(
        "- Defensiver Prüfpunkt: Falls `R_210` nahe `1` und deutlich kleiner als Stage-5.5-Quotienten wird, spricht das fuer starken mod-7-Anteil; "
        "bleibt `R_210` signifikant > 1, bleibt ein substanzieller Prime-vs-Control-Abstand."
    )
    lines.append("")
    lines.append("## C) HL-nahe Referenzanalyse (defensiv)")
    lines.append("")
    if hl_by_n:
        lines.append(
            "- HL-nahe Proxies (`k3`, `k4`) aus bestehender Stage-6-Reprodatei wurden als Zusatzregressoren getestet."
        )
        lines.append("- Zielvariable: `ΔH(Δr)=H_prime-H_wheel_cramer`; Baseline: `ΔH ~ 1 + Δr`.")
        lines.append("- Vergleich: Proxy-augmentierte Modelle via `AIC`-Gewinn und `R²`-Gewinn.")
        lines.append("")
        lines.append("| N | k3 AIC gain | k3 R² gain | k4 AIC gain | k4 R² gain |")
        lines.append("|---:|---:|---:|---:|---:|")
        for run in runs:
            hs = hl_by_n[str(run.n)]
            lines.append(
                f"| {run.n:,} | {hs['k3_aic_gain']:.3f} | {hs['k3_r2_gain']:.3f} | {hs['k4_aic_gain']:.3f} | {hs['k4_r2_gain']:.3f} |"
            )
        lines.append("")
        lines.append(
            "- Methodische Einschränkung: Proxies sind heuristisch und nicht skalenspezifisch rekalibriert; Ergebnis als Interface-Test, nicht als Theoriebeweis."
        )
    else:
        lines.append("- Keine robuste HL-Proxy-Implementierung fuer diese Datenlage gefunden.")
        lines.append("- Fit-Interface vorbereitet (`baseline` vs `+k3/+k4`) und in JSON/CSV dokumentiert.")
        lines.append("- TODO Stage 6:")
        lines.append("  1. formal definierte Singular-Series-Proxy-Familie")
        lines.append("  2. skalenspezifische Parameterschaetzung (mind. N=1e6..1e8)")
        lines.append("  3. robustes Out-of-sample-Kriterium")
    lines.append("")
    lines.append("## Artefakte")
    lines.append("")
    lines.append(f"- Skript: `{SCRIPT_OUT}`")
    lines.append(f"- Markdown: `{MD_OUT.relative_to(REPO_ROOT)}`")
    lines.append(f"- Summary-CSV: `{CSV_OUT.relative_to(REPO_ROOT)}`")
    lines.append(f"- Plots: `{PLOT_OUT.relative_to(REPO_ROOT)}`")
    lines.append(f"- Fit-Details (JSON): `{JSON_OUT.relative_to(REPO_ROOT)}`")
    lines.append("")
    lines.append("## Reviewer-sichere Einordnung")
    lines.append("")
    lines.append("- Keine Kausalclaims aus 5-Punkt-Δr-Reihen.")
    lines.append("- Modellvergleiche nur als Konsistenz-/Robustheitschecks.")
    lines.append("- Stage 6 sollte den naechsten publizierbaren Test auf echte HL-Singular-Series-Konstruktion mit klaren out-of-sample Kriterien fokussieren.")

    MD_OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"Wrote: {CSV_OUT}")
    print(f"Wrote: {PLOT_OUT}")
    print(f"Wrote: {MD_OUT}")
    print(f"Wrote: {JSON_OUT}")


if __name__ == "__main__":
    main()

