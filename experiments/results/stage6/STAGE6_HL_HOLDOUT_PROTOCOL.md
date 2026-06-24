# Stage 6 Holdout Protocol: Signal-Axis HL/Singular-Series Program

## Research Architecture v2

The symmetry analysis separates the model space into stable invariant axes and active signal directions. Stable invariants (`M_C`, `Omega`, `S=v2+v3`) are treated as background coordinates for control, normalization, and comparability. Active symmetry-breaking directions (`DeltaH_cramer`, `H(Delta-r)`, `Q_cramer`) are treated as the primary Stage-6 signal axes.

Stage 6 is therefore defined as out-of-sample HL/Singular-Series modeling on the three signal axes, while invariants remain background coordinates.

## Scope and data basis

- Input basis: existing Stage-5.5/5.6 outputs only (no new in-sample generation).
- Scales used: `N=1,000,000`, `N=10,000,000`, `N=20,000,000`
- Delta-r classes used: `2`, `6`, `10`, `14`, `18`
- Signal-axis targets: `DeltaH_cramer`, `H(Delta-r)`, `Q_cramer`
- Backward-compatible derived targets currently tracked in files/tables: `deltaH_30_cramer`, `deltaH_30_random`, `ratio_30_cramer`, `deltaH_210_cramer`

## Candidate model families (uniform API)

- `baseline_constant`: no Delta-r structure.
- `baseline_linear`: `a + b*Delta-r`.
- `baseline_power`: best of `1 + c*Delta-r^alpha` and `a*Delta-r^alpha` on train folds.
- `hl_proxy_linear`: linear proxy family with available HL proxies (`k3`, `k4`).

## Holdout protocol

- Train/Holdout split is mandatory for every run.
- Protocol A: rotating leave-one-Delta-r-out per scale (`Delta-r` holdout).
- Protocol B: leave-one-scale-out cross-scale check (`N` holdout).
- Per fold reported: train metrics, holdout MAE/RMSE/relative error, train AIC/BIC (secondary), fold rank.
- Residual diagnostics are required for top-ranked families (pattern checks, variance structure, outlier concentration).
- Primary criterion: out-of-sample error; parameter stability, AIC/BIC, and residual diagnostics are secondary.
- Required comparator: explicit benchmark versus Wheel-210 families/baselines.

## Overall out-of-sample leaderboard

| rank | model_family | mean holdout RMSE | mean holdout MAE | mean holdout rel.err | mean fold rank | n folds |
|---:|---|---:|---:|---:|---:|---:|
| 1 | baseline_power | 0.26195 | 0.250479 | 0.269092 | 1.4583 | 72 |
| 2 | baseline_linear | 0.302288 | 0.292073 | 0.758291 | 2.3889 | 72 |
| 3 | hl_proxy_linear | 0.478717 | 0.460009 | 0.543235 | 3.3542 | 144 |
| 4 | baseline_constant | 0.798031 | 0.773468 | 2.02583 | 4.2778 | 72 |

## Target-wise winner check

| target | winner | mean holdout RMSE | runner-up RMSE | note |
|---|---|---:|---:|---|
| deltaH_30_cramer | baseline_power | 0.0785782 | 0.269364 | gap=0.190786 |
| deltaH_30_random | baseline_power | 0.110711 | 0.317894 | gap=0.207183 |
| ratio_30_cramer | baseline_power | 0.0497503 | 0.0655879 | gap=0.0158376 |
| deltaH_210_cramer | baseline_linear | 0.556305 | 0.808759 | gap=0.252454 |

## Parameter stability (secondary)

- `baseline_constant`: c_cv=0.317591, c_mean=1.14014, c_std=0.362097
- `baseline_linear`: a_cv=4.11221, a_mean=-0.163843, a_std=0.673757, b_cv=0.487936, b_mean=0.129619, b_std=0.0632458
- `baseline_power`: a_cv=0.47441, a_mean=0.0163566, a_std=0.00775975, alpha_cv=0.443401, alpha_mean=1.59417, alpha_std=0.706855, c_cv=3.41097, c_mean=-0.56345, c_std=1.92191
- `hl_proxy_linear`: a_cv=0.580868, a_mean=26.8458, a_std=15.5939, b_cv=0.611326, b_mean=-37.7899, b_std=23.102

## Defensive interpretation

- Current out-of-sample winner by primary criterion is `baseline_power` (mean fold rank `1.458`, mean RMSE `0.26195`).
- Best HL-proxy family currently: `hl_proxy_linear` with mean RMSE `0.478717` and mean rank `3.354`.
- HL-proxy families are currently not the top out-of-sample performer in this protocol.
- Mechanism status: still open. Current protocol narrows plausible families but does not identify a unique mechanism.
- Next data step: extend to higher scales (`N=1e8` and ideally `N=1e9`) plus additional Delta-r classes and stronger HL feature engineering.
- Architecture v2 stance: keep invariants as coordinate background; prioritize Stage-6 discovery decisions on the signal axes (`DeltaH_cramer`, `H(Delta-r)`, `Q_cramer`) with explicit Wheel-210 comparison.

## Reproducibility

- Script: `code/experiments/stage6_hl_holdout.py`
- Holdout table: `experiments/results/stage6/stage6_holdout_table.csv`
- Plots: `experiments/results/stage6/stage6_holdout_plots.png`
- Model params: `experiments/results/stage6/stage6_model_params.json`

## Caution

- Fold sizes are small; all model ranking statements are uncertainty-aware and protocol-conditional.
- AIC/BIC are in-sample only and reported strictly as secondary diagnostics.
