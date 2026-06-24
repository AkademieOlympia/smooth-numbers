#!/usr/bin/env python3
"""
Stage-6 Probe fuer Zeit-/Raum-/Richtungs-Aequivalente.

Nutzen:
- Liest vorhandene Stage-5.6/6/Noether-Artefakte
- Berechnet kompakte Kennzahlen fuer sofort testbare Hypothesen
- Schreibt eine flache Ergebnistabelle nach
  experiments/results/stage6/stage6_equivalent_axes_probe.csv
"""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple

import numpy as np


REPO_ROOT = Path(__file__).resolve().parents[2]
STAGE56_CSV = REPO_ROOT / "experiments" / "results" / "stage56" / "stage56_summary_table.csv"
STAGE6_PARAMS_JSON = REPO_ROOT / "experiments" / "results" / "stage6" / "stage6_model_params.json"
NOETHER_CSV = REPO_ROOT / "experiments" / "results" / "noether" / "noether_invariance_table.csv"
OUT_CSV = REPO_ROOT / "experiments" / "results" / "stage6" / "stage6_equivalent_axes_probe.csv"


def safe_spearman(x: Sequence[float], y: Sequence[float]) -> float:
    xv = np.asarray(x, dtype=float)
    yv = np.asarray(y, dtype=float)
    mask = np.isfinite(xv) & np.isfinite(yv)
    xv = xv[mask]
    yv = yv[mask]
    if len(xv) < 2:
        return math.nan
    xr = np.argsort(np.argsort(xv))
    yr = np.argsort(np.argsort(yv))
    if np.std(xr) == 0 or np.std(yr) == 0:
        return math.nan
    return float(np.corrcoef(xr, yr)[0, 1])


def flatten_upper_triangle(mat: np.ndarray) -> np.ndarray:
    idx = np.triu_indices(mat.shape[0], k=1)
    return mat[idx]


def parse_fit_notes(note: str) -> Dict[str, float]:
    out: Dict[str, float] = {}
    if not note:
        return out
    left = note.split("|", 1)[0].strip()
    for token in left.split(";"):
        token = token.strip()
        if "=" not in token:
            continue
        k, v = token.split("=", 1)
        try:
            out[k.strip()] = float(v.strip())
        except ValueError:
            continue
    return out


def append_row(rows: List[Dict[str, object]], axis_family: str, test_id: str, metric: str, value: float, note: str) -> None:
    rows.append(
        {
            "axis_family": axis_family,
            "test_id": test_id,
            "metric": metric,
            "value": value,
            "note": note,
        }
    )


def load_stage56() -> Tuple[Dict[int, Dict[int, Dict[str, float]]], Dict[int, float]]:
    """
    Returns:
      wheel_by_n_dr_metric[n][dr][metric] with metrics in {R_210, deltaH_210}
      slope_b_by_n[n] from section A linear fit.
    """
    wheel: Dict[int, Dict[int, Dict[str, float]]] = {}
    slopes: Dict[int, float] = {}

    with STAGE56_CSV.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            section = (row.get("section") or "").strip()
            scale_txt = (row.get("scale") or "").strip()
            if not scale_txt:
                continue

            if section == "A_quotient_scaling":
                model = (row.get("model") or "").strip()
                metric = (row.get("metric") or "").strip()
                if model == "linear" and metric == "fit" and scale_txt != "pooled":
                    try:
                        n = int(scale_txt)
                    except ValueError:
                        continue
                    params = parse_fit_notes(row.get("notes") or "")
                    if "b" in params:
                        slopes[n] = float(params["b"])
                continue

            if section != "B_wheel210":
                continue
            model = (row.get("model") or "").strip()
            metric = (row.get("metric") or "").strip()
            if model != "wheel210_cramer":
                continue
            if metric not in {"R_210", "deltaH_210"}:
                continue
            dr_txt = (row.get("delta_r") or "").strip()
            val_txt = (row.get("value") or "").strip()
            try:
                n = int(scale_txt)
                dr = int(dr_txt)
                val = float(val_txt)
            except ValueError:
                continue

            wheel.setdefault(n, {}).setdefault(dr, {})[metric] = val

    return wheel, slopes


def load_stage6_params() -> Dict[str, object]:
    with STAGE6_PARAMS_JSON.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_noether() -> Tuple[int, int]:
    """
    Returns:
      count_invariant_controls, count_strong_signal_breaks
    """
    invariant_controls = 0
    strong_signal = 0

    control_obs = {"M_C", "Omega", "S"}
    signal_obs = {"H(delta_r)", "DeltaH_cramer", "Q_cramer"}

    with NOETHER_CSV.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            obs = (row.get("observable") or "").strip()
            cls = (row.get("classification") or "").strip()
            if obs in control_obs and cls == "invariant":
                invariant_controls += 1
            if obs in signal_obs and cls == "strong_symmetry_breaking":
                strong_signal += 1

    return invariant_controls, strong_signal


def compute_time_metrics(rows: List[Dict[str, object]], wheel: Dict[int, Dict[int, Dict[str, float]]], slopes: Dict[int, float]) -> None:
    ns = sorted(wheel)
    if not ns:
        return
    drs = sorted(next(iter(wheel.values())).keys())

    # Z1: Spearman(dr, R_210) je N
    rhos = []
    monotone_pos_share_by_n = []
    for n in ns:
        vals = [wheel[n][dr].get("R_210", math.nan) for dr in drs]
        rho = safe_spearman(drs, vals)
        rhos.append(rho)
        diffs = np.diff(np.asarray(vals, dtype=float))
        diffs = diffs[np.isfinite(diffs)]
        if len(diffs) > 0:
            monotone_pos_share_by_n.append(float(np.mean(diffs > 0)))

    append_row(rows, "time", "Z1_scale_direction", "mean_spearman_rho_dr_vs_R210", float(np.nanmean(rhos)), "Hoeher bedeutet stabilere positive Drift ueber dr.")
    append_row(rows, "time", "Z1_scale_direction", "min_spearman_rho_dr_vs_R210", float(np.nanmin(rhos)), "Worst-case Skala fuer Drift-Richtung.")
    append_row(rows, "time", "Z1_scale_direction", "mean_positive_diff_share", float(np.nanmean(monotone_pos_share_by_n)), "Anteil positiver lokaler Drift-Schritte.")

    # Z2: Pfeil der Skala ueber Amplitude A(N)=R210(18)-R210(2)
    amps = []
    for n in ns:
        low = wheel[n].get(min(drs), {}).get("R_210", math.nan)
        high = wheel[n].get(max(drs), {}).get("R_210", math.nan)
        amps.append(float(high - low) if np.isfinite(low) and np.isfinite(high) else math.nan)
    rho_scale = safe_spearman(np.log10(np.asarray(ns, dtype=float)), amps)
    append_row(rows, "time", "Z2_scale_arrow", "spearman_rho_logN_vs_amplitude", rho_scale, "Amplitude = R210(max dr) - R210(min dr).")
    append_row(rows, "time", "Z2_scale_arrow", "mean_amplitude", float(np.nanmean(amps)), "Mittlere Driftamplitude ueber Skalen.")

    # Z3: slope-Stabilitaet aus Stage-5.6 linear fit
    if slopes:
        slope_vals = np.asarray([slopes[n] for n in sorted(slopes)], dtype=float)
        mean_s = float(np.mean(slope_vals))
        std_s = float(np.std(slope_vals, ddof=1)) if len(slope_vals) > 1 else 0.0
        cv = float(std_s / max(abs(mean_s), 1e-12))
        sign_stability = float(np.mean(np.sign(slope_vals) == np.sign(mean_s)))
        append_row(rows, "time", "Z3_fit_time", "mean_linear_slope_b", mean_s, "Aus Stage-5.6 Quotientenfit R=a+b*dr.")
        append_row(rows, "time", "Z3_fit_time", "slope_cv", cv, "Variationskoeffizient der b(N)-Schaetzungen.")
        append_row(rows, "time", "Z3_fit_time", "slope_sign_stability", sign_stability, "Anteil gleicher Vorzeichen von b(N).")


def compute_space_metrics(rows: List[Dict[str, object]], wheel: Dict[int, Dict[int, Dict[str, float]]], invariant_controls: int, strong_signal: int) -> None:
    ns = sorted(wheel)
    if not ns:
        return
    drs = sorted(next(iter(wheel.values())).keys())

    # R1: Distanzabhaengigkeit je N
    rhos_dh = []
    for n in ns:
        y = [wheel[n][dr].get("deltaH_210", math.nan) for dr in drs]
        rhos_dh.append(safe_spearman(drs, y))
    append_row(rows, "space", "R1_gap_distance", "mean_spearman_rho_dr_vs_deltaH210", float(np.nanmean(rhos_dh)), "Positiv deutet auf Distanzabhaengigkeit hin.")
    append_row(rows, "space", "R1_gap_distance", "min_spearman_rho_dr_vs_deltaH210", float(np.nanmin(rhos_dh)), "Worst-case Skala.")

    # R2: Geometrie in Feature-Raum ueber dr-Aggregation
    vecs = []
    for dr in drs:
        vals_dh = [wheel[n][dr].get("deltaH_210", math.nan) for n in ns]
        vals_r = [wheel[n][dr].get("R_210", math.nan) for n in ns]
        vecs.append([float(np.nanmean(vals_dh)), float(np.nanmean(vals_r))])
    X = np.asarray(vecs, dtype=float)
    Xc = X - np.mean(X, axis=0, keepdims=True)
    cov = np.cov(Xc.T)
    evals, _ = np.linalg.eigh(cov)
    evals = np.sort(evals)[::-1]
    pc1_share = float(evals[0] / max(np.sum(evals), 1e-12))

    # Distanzkonsistenz: |dr_i-dr_j| vs. Featuredistanz
    d_gap = np.abs(np.subtract.outer(np.asarray(drs, dtype=float), np.asarray(drs, dtype=float)))
    d_feat = np.linalg.norm(X[:, None, :] - X[None, :, :], axis=2)
    corr_dist = float(np.corrcoef(flatten_upper_triangle(d_gap), flatten_upper_triangle(d_feat))[0, 1])

    append_row(rows, "space", "R2_feature_geometry", "pc1_variance_share", pc1_share, "Anteil der ersten Hauptkomponente.")
    append_row(rows, "space", "R2_feature_geometry", "corr_gapdist_vs_featuredist", corr_dist, "Korrelation zwischen Gap- und Feature-Distanzen.")

    # R3: Noether separation
    append_row(rows, "space", "R3_noether_separation", "count_invariant_control_rows", float(invariant_controls), "Anzahl invariant klassifizierter Kontrollzeilen.")
    append_row(rows, "space", "R3_noether_separation", "count_strong_signal_rows", float(strong_signal), "Anzahl starker Symmetriebruch-Zeilen fuer Signalachsen.")


def compute_direction_metrics(rows: List[Dict[str, object]], wheel: Dict[int, Dict[int, Dict[str, float]]], stage6_params: Dict[str, object]) -> None:
    ns = sorted(wheel)
    if not ns:
        return
    drs = sorted(next(iter(wheel.values())).keys())

    # D1: Monotone Drift
    pos_shares = []
    for n in ns:
        vals = np.asarray([wheel[n][dr].get("R_210", math.nan) for dr in drs], dtype=float)
        diffs = np.diff(vals)
        diffs = diffs[np.isfinite(diffs)]
        if len(diffs) > 0:
            pos_shares.append(float(np.mean(diffs > 0)))
    append_row(rows, "direction", "D1_monotone_drift", "mean_positive_diff_share_R210", float(np.nanmean(pos_shares)), "Anteil positiver lokaler Drift in R_210.")

    # D2: Fiedler-Richtung auf Pfadgraph ueber dr
    m = len(drs)
    A = np.zeros((m, m), dtype=float)
    for i in range(m - 1):
        A[i, i + 1] = 1.0
        A[i + 1, i] = 1.0
    D = np.diag(np.sum(A, axis=1))
    L = D - A
    evals, evecs = np.linalg.eigh(L)
    if len(evals) >= 2:
        fiedler = evecs[:, 1]
        corrs = []
        for n in ns:
            y = np.asarray([wheel[n][dr].get("deltaH_210", math.nan) for dr in drs], dtype=float)
            if np.all(np.isfinite(y)) and np.std(y) > 0 and np.std(fiedler) > 0:
                corrs.append(float(np.corrcoef(y, fiedler)[0, 1]))
        if corrs:
            append_row(rows, "direction", "D2_spectral_direction", "mean_corr_deltaH210_vs_fiedler", float(np.mean(corrs)), "Vorzeichenstabilitaet der Spektralprojektion.")
            append_row(rows, "direction", "D2_spectral_direction", "sign_stability", float(np.mean(np.sign(corrs) == np.sign(np.mean(corrs)))), "Anteil gleicher Vorzeichen ueber N.")

    # D3: Richtung im Modellfehlerraum
    summary = stage6_params.get("summary", {})
    by_target = summary.get("by_target_leaderboard", {})
    if isinstance(by_target, dict):
        margins_struct_vs_const = []
        for _target, ranking in by_target.items():
            if not isinstance(ranking, list):
                continue
            best_structured = math.nan
            constant = math.nan
            for row in ranking:
                fam = row.get("model_family")
                rmse = row.get("mean_test_rmse")
                if not isinstance(rmse, (float, int)):
                    continue
                rmse = float(rmse)
                if fam == "baseline_constant":
                    constant = rmse
                elif fam in {"baseline_power", "baseline_linear", "hl_proxy_linear"}:
                    best_structured = rmse if math.isnan(best_structured) else min(best_structured, rmse)
            if np.isfinite(best_structured) and np.isfinite(constant):
                margins_struct_vs_const.append(best_structured - constant)
        if margins_struct_vs_const:
            append_row(rows, "direction", "D3_residual_direction", "mean_structured_minus_constant_rmse", float(np.mean(margins_struct_vs_const)), "Negativ => strukturierte Modelle besser.")
            append_row(rows, "direction", "D3_residual_direction", "share_negative_margins", float(np.mean(np.asarray(margins_struct_vs_const) < 0)), "Anteil Targets mit strukturiertem Vorteil.")


def main() -> None:
    if not STAGE56_CSV.exists():
        raise FileNotFoundError(f"Missing input: {STAGE56_CSV}")
    if not STAGE6_PARAMS_JSON.exists():
        raise FileNotFoundError(f"Missing input: {STAGE6_PARAMS_JSON}")
    if not NOETHER_CSV.exists():
        raise FileNotFoundError(f"Missing input: {NOETHER_CSV}")

    wheel, slopes = load_stage56()
    stage6_params = load_stage6_params()
    invariant_controls, strong_signal = load_noether()

    rows: List[Dict[str, object]] = []
    compute_time_metrics(rows, wheel, slopes)
    compute_space_metrics(rows, wheel, invariant_controls, strong_signal)
    compute_direction_metrics(rows, wheel, stage6_params)

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["axis_family", "test_id", "metric", "value", "note"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote: {OUT_CSV}")


if __name__ == "__main__":
    main()
