#!/usr/bin/env python3
"""
Stage-6 Holdout Protocol for Prime-vs-Wheel divergence.

Goal:
- Formal out-of-sample checks for candidate model families that explain
  DeltaH(Delta r) and optional ratio targets R(Delta r).
- Defensive reporting for reviewer-oriented discussion.
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

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


REPO_ROOT = Path(__file__).resolve().parents[2]
RESULTS_DIR = REPO_ROOT / "experiments" / "results" / "stage6"
SCRIPT_PATH = Path(__file__).relative_to(REPO_ROOT)

OUT_MD = RESULTS_DIR / "STAGE6_HL_HOLDOUT_PROTOCOL.md"
OUT_CSV = RESULTS_DIR / "stage6_holdout_table.csv"
OUT_PLOT = RESULTS_DIR / "stage6_holdout_plots.png"
OUT_PARAMS = RESULTS_DIR / "stage6_model_params.json"

STAGE55_RUN_FILES: Sequence[Path] = [
    REPO_ROOT / "stage5.5_final_run.txt",
    REPO_ROOT / "reproducibility_N10M.txt",
    REPO_ROOT / "reproducibility_N20M.txt",
]
STAGE56_SUMMARY_CSV = REPO_ROOT / "experiments" / "results" / "stage56" / "stage56_summary_table.csv"
HL_PROXY_FILE = REPO_ROOT / "reproducibility_stage6_N1M.txt"

DELTA_R_EXPECTED = [2, 6, 10, 14, 18]


@dataclass
class RunData:
    n: int
    h_prime: Dict[int, float]
    h_wheel_random: Dict[int, float]
    h_wheel_cramer: Dict[int, float]


@dataclass
class DataRow:
    n: int
    delta_r: int
    targets: Dict[str, float]
    features: Dict[str, float]


def parse_stage55_run(path: Path) -> RunData:
    text = path.read_text(encoding="utf-8")

    n_match = re.search(r"^N\s*=\s*(\d+)\s*$", text, flags=re.MULTILINE)
    if not n_match:
        raise ValueError(f"Could not parse N from {path}")
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

    dr_common = sorted(set(h_prime) & set(h_wheel_random) & set(h_wheel_cramer))
    if not dr_common:
        raise ValueError(f"No common Delta-r values in {path}")

    return RunData(
        n=n,
        h_prime={dr: h_prime[dr] for dr in dr_common},
        h_wheel_random={dr: h_wheel_random[dr] for dr in dr_common},
        h_wheel_cramer={dr: h_wheel_cramer[dr] for dr in dr_common},
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
        if not line or line.startswith("Correlation:"):
            section = None if line.startswith("Correlation:") else section
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


def parse_wheel210_cramer(summary_csv: Path) -> Dict[Tuple[int, int], float]:
    out: Dict[Tuple[int, int], float] = {}
    if not summary_csv.exists():
        return out

    with summary_csv.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("section") != "B_wheel210":
                continue
            if row.get("model") != "wheel210_cramer":
                continue
            if row.get("metric") != "H_wheel210":
                continue
            scale = row.get("scale", "").strip()
            dr = row.get("delta_r", "").strip()
            value = row.get("value", "").strip()
            if not scale or not dr or not value:
                continue
            try:
                n = int(scale)
                delta_r = int(dr)
                h210 = float(value)
            except ValueError:
                continue
            if math.isnan(h210) or h210 == 0.0:
                continue
            out[(n, delta_r)] = h210
    return out


def safe_rel_error(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    denom = np.maximum(np.abs(y_true), 1e-12)
    return float(np.mean(np.abs(y_true - y_pred) / denom))


def compute_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
    err = y_true - y_pred
    mae = float(np.mean(np.abs(err)))
    rmse = float(math.sqrt(np.mean(err ** 2)))
    rel = safe_rel_error(y_true, y_pred)
    return {"mae": mae, "rmse": rmse, "rel_error": rel}


def aic_bic_from_residuals(residuals: np.ndarray, k: int) -> Tuple[float, float]:
    n = len(residuals)
    if n == 0:
        return math.nan, math.nan
    sse = float(np.sum(residuals ** 2))
    sigma2 = max(sse / n, 1e-16)
    aic = float(n * math.log(sigma2) + 2 * k)
    bic = float(n * math.log(sigma2) + k * math.log(max(n, 1)))
    return aic, bic


class BaseModel:
    family: str = "base"
    feature_name: Optional[str] = None

    def fit(self, x: np.ndarray, y: np.ndarray) -> None:
        raise NotImplementedError

    def predict(self, x: np.ndarray) -> np.ndarray:
        raise NotImplementedError

    def num_params(self) -> int:
        raise NotImplementedError

    def params(self) -> Dict[str, float]:
        raise NotImplementedError


class ConstantModel(BaseModel):
    family = "baseline_constant"

    def __init__(self) -> None:
        self.c = math.nan

    def fit(self, x: np.ndarray, y: np.ndarray) -> None:
        self.c = float(np.mean(y))

    def predict(self, x: np.ndarray) -> np.ndarray:
        return np.full(len(x), self.c, dtype=float)

    def num_params(self) -> int:
        return 1

    def params(self) -> Dict[str, float]:
        return {"c": self.c}


class LinearModel(BaseModel):
    family = "baseline_linear"

    def __init__(self) -> None:
        self.a = math.nan
        self.b = math.nan

    def fit(self, x: np.ndarray, y: np.ndarray) -> None:
        X = np.column_stack([np.ones(len(x)), x])
        beta, _, _, _ = np.linalg.lstsq(X, y, rcond=None)
        self.a = float(beta[0])
        self.b = float(beta[1])

    def predict(self, x: np.ndarray) -> np.ndarray:
        return self.a + self.b * x

    def num_params(self) -> int:
        return 2

    def params(self) -> Dict[str, float]:
        return {"a": self.a, "b": self.b}


class PowerModel(BaseModel):
    family = "baseline_power"

    def __init__(self) -> None:
        self.variant = "one_plus"
        self.p = math.nan
        self.alpha = math.nan

    def fit(self, x: np.ndarray, y: np.ndarray) -> None:
        # Small-grid robust fit (no scipy requirement).
        alphas = np.linspace(-2.0, 3.0, 251)
        best_sse = math.inf
        best_variant = "one_plus"
        best_p = math.nan
        best_alpha = math.nan

        for alpha in alphas:
            xpow = np.power(x, alpha)
            # Variant 1: y = 1 + c*x^alpha
            c = float(np.dot(xpow, (y - 1.0)) / max(np.dot(xpow, xpow), 1e-16))
            y_hat_one = 1.0 + c * xpow
            sse_one = float(np.sum((y - y_hat_one) ** 2))
            if sse_one < best_sse:
                best_sse = sse_one
                best_variant = "one_plus"
                best_p = c
                best_alpha = float(alpha)

            # Variant 2: y = a*x^alpha
            a = float(np.dot(xpow, y) / max(np.dot(xpow, xpow), 1e-16))
            y_hat_ax = a * xpow
            sse_ax = float(np.sum((y - y_hat_ax) ** 2))
            if sse_ax < best_sse:
                best_sse = sse_ax
                best_variant = "ax"
                best_p = a
                best_alpha = float(alpha)

        self.variant = best_variant
        self.p = best_p
        self.alpha = best_alpha

    def predict(self, x: np.ndarray) -> np.ndarray:
        xpow = np.power(x, self.alpha)
        if self.variant == "one_plus":
            return 1.0 + self.p * xpow
        return self.p * xpow

    def num_params(self) -> int:
        return 2

    def params(self) -> Dict[str, float]:
        key = "c" if self.variant == "one_plus" else "a"
        return {"variant": self.variant, key: self.p, "alpha": self.alpha}


class HLProxyLinearModel(BaseModel):
    family = "hl_proxy_linear"

    def __init__(self, feature_name: str) -> None:
        self.feature_name = feature_name
        self.a = math.nan
        self.b = math.nan

    def fit(self, x: np.ndarray, y: np.ndarray) -> None:
        X = np.column_stack([np.ones(len(x)), x])
        beta, _, _, _ = np.linalg.lstsq(X, y, rcond=None)
        self.a = float(beta[0])
        self.b = float(beta[1])

    def predict(self, x: np.ndarray) -> np.ndarray:
        return self.a + self.b * x

    def num_params(self) -> int:
        return 2

    def params(self) -> Dict[str, float]:
        return {"proxy": self.feature_name, "a": self.a, "b": self.b}


def build_rows() -> Tuple[List[DataRow], List[int], List[int], List[str]]:
    runs: List[RunData] = []
    for p in STAGE55_RUN_FILES:
        if p.exists():
            runs.append(parse_stage55_run(p))
    if len(runs) < 2:
        raise RuntimeError("Need at least two Stage-5.5 scales for holdout protocol.")

    runs.sort(key=lambda r: r.n)
    scales = [r.n for r in runs]
    common_dr = sorted(set.intersection(*[set(r.h_prime.keys()) for r in runs]))
    common_dr = [dr for dr in common_dr if dr in DELTA_R_EXPECTED]
    if len(common_dr) < 4:
        raise RuntimeError("Need at least 4 common Delta-r classes for fold holdout.")

    h_k3, h_k4 = parse_hl_proxies(HL_PROXY_FILE)
    wheel210 = parse_wheel210_cramer(STAGE56_SUMMARY_CSV)

    rows: List[DataRow] = []
    targets_available = {
        "deltaH_30_cramer": True,
        "deltaH_30_random": True,
        "ratio_30_cramer": True,
        "deltaH_210_cramer": all((n, dr) in wheel210 for n in scales for dr in common_dr),
    }

    for run in runs:
        for dr in common_dr:
            h_prime = run.h_prime[dr]
            h_w30_c = run.h_wheel_cramer[dr]
            h_w30_r = run.h_wheel_random[dr]
            h210 = wheel210.get((run.n, dr), math.nan)

            targets = {
                "deltaH_30_cramer": h_prime - h_w30_c,
                "deltaH_30_random": h_prime - h_w30_r,
                "ratio_30_cramer": h_prime / h_w30_c if h_w30_c != 0 else math.nan,
            }
            if targets_available["deltaH_210_cramer"] and not math.isnan(h210):
                targets["deltaH_210_cramer"] = h_prime - h210

            features = {
                "delta_r": float(dr),
                "hl_k3": float(h_k3.get(dr, math.nan)),
                "hl_k4": float(h_k4.get(dr, math.nan)),
            }
            rows.append(DataRow(n=run.n, delta_r=dr, targets=targets, features=features))

    targets = [k for k, ok in targets_available.items() if ok]
    return rows, scales, common_dr, targets


def make_model_instances(rows: List[DataRow], target: str) -> List[BaseModel]:
    _ = target  # keeps interface uniform for future target-specific models.
    models: List[BaseModel] = [ConstantModel(), LinearModel(), PowerModel()]

    # Only include HL proxy models if the feature exists in all relevant rows.
    for feat in ["hl_k3", "hl_k4"]:
        valid = [r for r in rows if target in r.targets and not math.isnan(r.features.get(feat, math.nan))]
        if len(valid) >= 4:
            models.append(HLProxyLinearModel(feat))
    return models


def filter_rows(rows: List[DataRow], target: str) -> List[DataRow]:
    out: List[DataRow] = []
    for r in rows:
        y = r.targets.get(target, math.nan)
        if not math.isnan(y):
            out.append(r)
    return out


def fold_rankings(items: List[Dict[str, object]], metric_key: str = "test_rmse") -> None:
    vals = [(idx, float(it[metric_key])) for idx, it in enumerate(items)]
    vals.sort(key=lambda x: x[1])
    rank = 1
    for pos, (idx, _) in enumerate(vals):
        if pos > 0 and not math.isclose(vals[pos][1], vals[pos - 1][1], rel_tol=1e-12, abs_tol=1e-12):
            rank = pos + 1
        items[idx]["rank"] = rank


def run_delta_r_holdout(rows: List[DataRow], target: str, scales: List[int], delta_rs: List[int]) -> List[Dict[str, object]]:
    per_target_rows = filter_rows(rows, target)
    results: List[Dict[str, object]] = []

    for n in scales:
        scale_rows = [r for r in per_target_rows if r.n == n]
        models = make_model_instances(scale_rows, target)

        for holdout_dr in delta_rs:
            train = [r for r in scale_rows if r.delta_r != holdout_dr]
            test = [r for r in scale_rows if r.delta_r == holdout_dr]
            if len(train) < 3 or len(test) < 1:
                continue

            fold_items: List[Dict[str, object]] = []
            for model in models:
                if isinstance(model, HLProxyLinearModel):
                    feat = model.feature_name or ""
                    train_valid = [r for r in train if not math.isnan(r.features.get(feat, math.nan))]
                    test_valid = [r for r in test if not math.isnan(r.features.get(feat, math.nan))]
                    if len(train_valid) < 3 or len(test_valid) < 1:
                        continue
                    x_train = np.array([r.features[feat] for r in train_valid], dtype=float)
                    y_train = np.array([r.targets[target] for r in train_valid], dtype=float)
                    x_test = np.array([r.features[feat] for r in test_valid], dtype=float)
                    y_test = np.array([r.targets[target] for r in test_valid], dtype=float)
                else:
                    x_train = np.array([r.features["delta_r"] for r in train], dtype=float)
                    y_train = np.array([r.targets[target] for r in train], dtype=float)
                    x_test = np.array([r.features["delta_r"] for r in test], dtype=float)
                    y_test = np.array([r.targets[target] for r in test], dtype=float)

                model.fit(x_train, y_train)
                yhat_train = model.predict(x_train)
                yhat_test = model.predict(x_test)
                train_m = compute_metrics(y_train, yhat_train)
                test_m = compute_metrics(y_test, yhat_test)
                aic, bic = aic_bic_from_residuals(y_train - yhat_train, model.num_params())

                item = {
                    "protocol": "delta_r_leave_one_out",
                    "target": target,
                    "scale": n,
                    "fold_id": f"dr={holdout_dr}",
                    "holdout_label": str(holdout_dr),
                    "model_family": model.family,
                    "model_detail": model.params(),
                    "train_mae": train_m["mae"],
                    "train_rmse": train_m["rmse"],
                    "train_rel_error": train_m["rel_error"],
                    "test_mae": test_m["mae"],
                    "test_rmse": test_m["rmse"],
                    "test_rel_error": test_m["rel_error"],
                    "train_aic": aic,
                    "train_bic": bic,
                    "rank": math.nan,
                }
                fold_items.append(item)

            if fold_items:
                fold_rankings(fold_items, metric_key="test_rmse")
                results.extend(fold_items)

    return results


def run_cross_scale_holdout(rows: List[DataRow], target: str, scales: List[int]) -> List[Dict[str, object]]:
    per_target_rows = filter_rows(rows, target)
    results: List[Dict[str, object]] = []
    models = make_model_instances(per_target_rows, target)

    for holdout_n in scales:
        train = [r for r in per_target_rows if r.n != holdout_n]
        test = [r for r in per_target_rows if r.n == holdout_n]
        if len(train) < 6 or len(test) < 3:
            continue

        fold_items: List[Dict[str, object]] = []
        for model in models:
            if isinstance(model, HLProxyLinearModel):
                feat = model.feature_name or ""
                train_valid = [r for r in train if not math.isnan(r.features.get(feat, math.nan))]
                test_valid = [r for r in test if not math.isnan(r.features.get(feat, math.nan))]
                if len(train_valid) < 6 or len(test_valid) < 3:
                    continue
                x_train = np.array([r.features[feat] for r in train_valid], dtype=float)
                y_train = np.array([r.targets[target] for r in train_valid], dtype=float)
                x_test = np.array([r.features[feat] for r in test_valid], dtype=float)
                y_test = np.array([r.targets[target] for r in test_valid], dtype=float)
            else:
                x_train = np.array([r.features["delta_r"] for r in train], dtype=float)
                y_train = np.array([r.targets[target] for r in train], dtype=float)
                x_test = np.array([r.features["delta_r"] for r in test], dtype=float)
                y_test = np.array([r.targets[target] for r in test], dtype=float)

            model.fit(x_train, y_train)
            yhat_train = model.predict(x_train)
            yhat_test = model.predict(x_test)
            train_m = compute_metrics(y_train, yhat_train)
            test_m = compute_metrics(y_test, yhat_test)
            aic, bic = aic_bic_from_residuals(y_train - yhat_train, model.num_params())

            item = {
                "protocol": "cross_scale_leave_one_scale_out",
                "target": target,
                "scale": "all",
                "fold_id": f"N={holdout_n}",
                "holdout_label": str(holdout_n),
                "model_family": model.family,
                "model_detail": model.params(),
                "train_mae": train_m["mae"],
                "train_rmse": train_m["rmse"],
                "train_rel_error": train_m["rel_error"],
                "test_mae": test_m["mae"],
                "test_rmse": test_m["rmse"],
                "test_rel_error": test_m["rel_error"],
                "train_aic": aic,
                "train_bic": bic,
                "rank": math.nan,
            }
            fold_items.append(item)

        if fold_items:
            fold_rankings(fold_items, metric_key="test_rmse")
            results.extend(fold_items)

    return results


def summarize_results(all_results: List[Dict[str, object]]) -> Dict[str, object]:
    if not all_results:
        raise RuntimeError("No holdout results generated.")

    # Aggregate by model family for out-of-sample metrics.
    agg: Dict[str, Dict[str, List[float]]] = {}
    per_target: Dict[str, Dict[str, List[float]]] = {}
    param_by_model: Dict[str, Dict[str, List[float]]] = {}

    for r in all_results:
        fam = str(r["model_family"])
        tgt = str(r["target"])
        agg.setdefault(fam, {"rmse": [], "mae": [], "rel": [], "rank": []})
        agg[fam]["rmse"].append(float(r["test_rmse"]))
        agg[fam]["mae"].append(float(r["test_mae"]))
        agg[fam]["rel"].append(float(r["test_rel_error"]))
        agg[fam]["rank"].append(float(r["rank"]))

        per_target.setdefault(tgt, {})
        per_target[tgt].setdefault(fam, [])
        per_target[tgt][fam].append(float(r["test_rmse"]))

        detail = r.get("model_detail", {})
        if isinstance(detail, dict):
            param_by_model.setdefault(fam, {})
            for k, v in detail.items():
                if isinstance(v, (int, float)) and not math.isnan(float(v)):
                    param_by_model[fam].setdefault(str(k), [])
                    param_by_model[fam][str(k)].append(float(v))

    leaderboard: List[Dict[str, object]] = []
    for fam, vals in agg.items():
        leaderboard.append(
            {
                "model_family": fam,
                "mean_test_rmse": float(np.mean(vals["rmse"])),
                "mean_test_mae": float(np.mean(vals["mae"])),
                "mean_test_rel_error": float(np.mean(vals["rel"])),
                "mean_rank": float(np.mean(vals["rank"])),
                "n_folds": len(vals["rmse"]),
            }
        )
    leaderboard.sort(key=lambda x: (x["mean_rank"], x["mean_test_rmse"]))

    by_target_leader: Dict[str, List[Dict[str, object]]] = {}
    for tgt, fam_vals in per_target.items():
        rows = []
        for fam, rmses in fam_vals.items():
            rows.append({"model_family": fam, "mean_test_rmse": float(np.mean(rmses)), "n_folds": len(rmses)})
        rows.sort(key=lambda x: x["mean_test_rmse"])
        by_target_leader[tgt] = rows

    param_stability: Dict[str, Dict[str, float]] = {}
    for fam, pmap in param_by_model.items():
        param_stability[fam] = {}
        for p, vals in pmap.items():
            if len(vals) < 2:
                continue
            mean_v = float(np.mean(vals))
            std_v = float(np.std(vals, ddof=1))
            cv = float(std_v / max(abs(mean_v), 1e-12))
            param_stability[fam][f"{p}_mean"] = mean_v
            param_stability[fam][f"{p}_std"] = std_v
            param_stability[fam][f"{p}_cv"] = cv

    return {
        "leaderboard": leaderboard,
        "by_target_leaderboard": by_target_leader,
        "param_stability": param_stability,
    }


def write_csv(results: List[Dict[str, object]]) -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "protocol",
        "target",
        "scale",
        "fold_id",
        "holdout_label",
        "model_family",
        "rank",
        "train_mae",
        "train_rmse",
        "train_rel_error",
        "test_mae",
        "test_rmse",
        "test_rel_error",
        "train_aic",
        "train_bic",
        "model_detail_json",
    ]
    with OUT_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in results:
            row = dict(r)
            row["model_detail_json"] = json.dumps(r.get("model_detail", {}), ensure_ascii=True, sort_keys=True)
            for k in ["rank", "train_mae", "train_rmse", "train_rel_error", "test_mae", "test_rmse", "test_rel_error", "train_aic", "train_bic"]:
                if k in row and isinstance(row[k], (float, int)):
                    row[k] = f"{float(row[k]):.10g}"
            writer.writerow({k: row.get(k, "") for k in fieldnames})


def write_plots(results: List[Dict[str, object]], summary: Dict[str, object]) -> None:
    families = sorted({str(r["model_family"]) for r in results})
    targets = sorted({str(r["target"]) for r in results})

    fig, axes = plt.subplots(2, 2, figsize=(16, 11))
    fig.suptitle("Stage 6 Holdout Protocol", fontsize=15, fontweight="bold")

    # Plot 1: RMSE distribution by family
    ax = axes[0, 0]
    data = []
    labels = []
    for fam in families:
        vals = [float(r["test_rmse"]) for r in results if str(r["model_family"]) == fam]
        if vals:
            data.append(vals)
            labels.append(fam)
    if data:
        ax.boxplot(data, tick_labels=labels, showmeans=True)
    ax.set_title("Holdout RMSE by model family")
    ax.set_ylabel("test RMSE")
    ax.grid(alpha=0.3, axis="y")
    ax.tick_params(axis="x", rotation=25)

    # Plot 2: mean rank bar
    ax = axes[0, 1]
    leaderboard = summary["leaderboard"]
    x = np.arange(len(leaderboard))
    y = [float(it["mean_rank"]) for it in leaderboard]
    ax.bar(x, y, alpha=0.85)
    ax.set_xticks(x)
    ax.set_xticklabels([str(it["model_family"]) for it in leaderboard], rotation=25)
    ax.set_title("Average fold rank (lower is better)")
    ax.set_ylabel("mean rank")
    ax.grid(alpha=0.3, axis="y")

    # Plot 3: target-wise winner margin (RMSE)
    ax = axes[1, 0]
    by_target = summary["by_target_leaderboard"]
    t_names = []
    margins = []
    for tgt in targets:
        rows = by_target.get(tgt, [])
        if len(rows) >= 2:
            margin = float(rows[1]["mean_test_rmse"]) - float(rows[0]["mean_test_rmse"])
            t_names.append(tgt)
            margins.append(margin)
    if margins:
        ax.bar(np.arange(len(margins)), margins, alpha=0.85)
        ax.set_xticks(np.arange(len(margins)))
        ax.set_xticklabels(t_names, rotation=20)
    ax.set_title("Winner margin vs runner-up (RMSE)")
    ax.set_ylabel("RMSE gap")
    ax.grid(alpha=0.3, axis="y")

    # Plot 4: protocol split comparison for top families
    ax = axes[1, 1]
    protocols = sorted({str(r["protocol"]) for r in results})
    top_families = [str(it["model_family"]) for it in leaderboard[:3]]
    width = 0.25
    for i, fam in enumerate(top_families):
        vals = []
        for p in protocols:
            arr = [float(r["test_rmse"]) for r in results if str(r["model_family"]) == fam and str(r["protocol"]) == p]
            vals.append(float(np.mean(arr)) if arr else math.nan)
        xpos = np.arange(len(protocols)) + (i - 1) * width
        ax.bar(xpos, vals, width=width, label=fam, alpha=0.85)
    ax.set_xticks(np.arange(len(protocols)))
    ax.set_xticklabels(protocols, rotation=15)
    ax.set_title("Mean RMSE by protocol")
    ax.set_ylabel("mean test RMSE")
    ax.grid(alpha=0.3, axis="y")
    ax.legend(fontsize=9)

    plt.tight_layout()
    plt.savefig(OUT_PLOT, dpi=180, bbox_inches="tight")


def write_markdown(
    results: List[Dict[str, object]],
    summary: Dict[str, object],
    scales: List[int],
    delta_rs: List[int],
    targets: List[str],
) -> None:
    lb = summary["leaderboard"]
    winner = lb[0] if lb else None
    by_target = summary["by_target_leaderboard"]
    param_stability = summary["param_stability"]

    lines: List[str] = []
    lines.append("# Stage 6 Holdout Protocol: Prime-vs-Wheel Divergence")
    lines.append("")
    lines.append("## Scope and data basis")
    lines.append("")
    lines.append("- Input basis: existing Stage-5.5/5.6 outputs only (no new in-sample generation).")
    lines.append("- Scales used: " + ", ".join([f"`N={n:,}`" for n in scales]))
    lines.append("- Delta-r classes used: " + ", ".join([f"`{dr}`" for dr in delta_rs]))
    lines.append("- Targets: " + ", ".join([f"`{t}`" for t in targets]))
    lines.append("")
    lines.append("## Candidate model families (uniform API)")
    lines.append("")
    lines.append("- `baseline_constant`: no Delta-r structure.")
    lines.append("- `baseline_linear`: `a + b*Delta-r`.")
    lines.append("- `baseline_power`: best of `1 + c*Delta-r^alpha` and `a*Delta-r^alpha` on train folds.")
    lines.append("- `hl_proxy_linear`: linear proxy family with available HL proxies (`k3`, `k4`).")
    lines.append("")
    lines.append("## Holdout protocol")
    lines.append("")
    lines.append("- Protocol A: rotating leave-one-Delta-r-out per scale.")
    lines.append("- Protocol B: leave-one-scale-out cross-scale check.")
    lines.append("- Per fold reported: train metrics, holdout MAE/RMSE/relative error, train AIC/BIC (secondary), fold rank.")
    lines.append("- Primary criterion: out-of-sample error; parameter stability and AIC/BIC are secondary.")
    lines.append("")
    lines.append("## Overall out-of-sample leaderboard")
    lines.append("")
    lines.append("| rank | model_family | mean holdout RMSE | mean holdout MAE | mean holdout rel.err | mean fold rank | n folds |")
    lines.append("|---:|---|---:|---:|---:|---:|---:|")
    for i, row in enumerate(lb, start=1):
        lines.append(
            f"| {i} | {row['model_family']} | {row['mean_test_rmse']:.6g} | {row['mean_test_mae']:.6g} | "
            f"{row['mean_test_rel_error']:.6g} | {row['mean_rank']:.4f} | {row['n_folds']} |"
        )
    lines.append("")
    lines.append("## Target-wise winner check")
    lines.append("")
    lines.append("| target | winner | mean holdout RMSE | runner-up RMSE | note |")
    lines.append("|---|---|---:|---:|---|")
    for t in targets:
        rows = by_target.get(t, [])
        if not rows:
            continue
        w = rows[0]
        if len(rows) > 1:
            lines.append(
                f"| {t} | {w['model_family']} | {w['mean_test_rmse']:.6g} | {rows[1]['mean_test_rmse']:.6g} | "
                f"gap={rows[1]['mean_test_rmse'] - w['mean_test_rmse']:.6g} |"
            )
        else:
            lines.append(f"| {t} | {w['model_family']} | {w['mean_test_rmse']:.6g} | n/a | single candidate |")
    lines.append("")
    lines.append("## Parameter stability (secondary)")
    lines.append("")
    if param_stability:
        for fam, vals in param_stability.items():
            if not vals:
                continue
            lines.append(f"- `{fam}`: " + ", ".join([f"{k}={vals[k]:.6g}" for k in sorted(vals)]))
    else:
        lines.append("- Limited fold variation prevented stable parameter spread estimates.")
    lines.append("")
    lines.append("## Defensive interpretation")
    lines.append("")
    if winner:
        lines.append(
            f"- Current out-of-sample winner by primary criterion is `{winner['model_family']}` "
            f"(mean fold rank `{winner['mean_rank']:.3f}`, mean RMSE `{winner['mean_test_rmse']:.6g}`)."
        )
    else:
        lines.append("- No winner available because no fold results were generated.")

    hl_rows = [r for r in lb if str(r["model_family"]).startswith("hl_proxy")]
    if hl_rows:
        best_hl = min(hl_rows, key=lambda x: (x["mean_rank"], x["mean_test_rmse"]))
        lines.append(
            f"- Best HL-proxy family currently: `{best_hl['model_family']}` with mean RMSE `{best_hl['mean_test_rmse']:.6g}` "
            f"and mean rank `{best_hl['mean_rank']:.3f}`."
        )
        if winner and best_hl["model_family"] != winner["model_family"]:
            lines.append("- HL-proxy families are currently not the top out-of-sample performer in this protocol.")
        else:
            lines.append("- HL-proxy family is currently competitive in this finite-sample protocol.")
    else:
        lines.append("- No HL-proxy family could be evaluated due to missing proxy features.")

    lines.append("- Mechanism status: still open. Current protocol narrows plausible families but does not identify a unique mechanism.")
    lines.append(
        "- Next data step: extend to higher scales (`N=1e8` and ideally `N=1e9`) plus additional Delta-r classes and stronger HL feature engineering."
    )
    lines.append("")
    lines.append("## Reproducibility")
    lines.append("")
    lines.append(f"- Script: `{SCRIPT_PATH}`")
    lines.append(f"- Holdout table: `{OUT_CSV.relative_to(REPO_ROOT)}`")
    lines.append(f"- Plots: `{OUT_PLOT.relative_to(REPO_ROOT)}`")
    lines.append(f"- Model params: `{OUT_PARAMS.relative_to(REPO_ROOT)}`")
    lines.append("")
    lines.append("## Caution")
    lines.append("")
    lines.append("- Fold sizes are small; all model ranking statements are uncertainty-aware and protocol-conditional.")
    lines.append("- AIC/BIC are in-sample only and reported strictly as secondary diagnostics.")

    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    rows, scales, delta_rs, targets = build_rows()

    all_results: List[Dict[str, object]] = []
    for target in targets:
        all_results.extend(run_delta_r_holdout(rows, target, scales, delta_rs))
        all_results.extend(run_cross_scale_holdout(rows, target, scales))

    summary = summarize_results(all_results)

    write_csv(all_results)
    write_plots(all_results, summary)
    write_markdown(all_results, summary, scales, delta_rs, targets)

    payload = {
        "inputs": {
            "stage55_files": [str(p.relative_to(REPO_ROOT)) for p in STAGE55_RUN_FILES if p.exists()],
            "stage56_summary_csv": str(STAGE56_SUMMARY_CSV.relative_to(REPO_ROOT)) if STAGE56_SUMMARY_CSV.exists() else None,
            "hl_proxy_file": str(HL_PROXY_FILE.relative_to(REPO_ROOT)) if HL_PROXY_FILE.exists() else None,
            "scales": scales,
            "delta_r": delta_rs,
            "targets": targets,
        },
        "summary": summary,
    }
    OUT_PARAMS.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print(f"Wrote: {OUT_CSV}")
    print(f"Wrote: {OUT_PLOT}")
    print(f"Wrote: {OUT_MD}")
    print(f"Wrote: {OUT_PARAMS}")


if __name__ == "__main__":
    main()
