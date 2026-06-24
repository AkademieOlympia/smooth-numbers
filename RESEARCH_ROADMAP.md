# Research Roadmap (Architecture v2)

## Research Architecture v2

The symmetry analysis separates the research space into two complementary parts: stable invariant axes and active signal directions. The stable invariants `M_C`, `Omega`, and `S=v2+v3` define background coordinates that track global structure and comparability across scales, but they are not treated as primary signal detectors. The active symmetry-breaking directions `DeltaH_cramer`, `H(Delta-r)`, and `Q_cramer` are the main discovery axes. Stage 6 therefore prioritizes out-of-sample HL/Singular-Series modeling on those three signal axes, with invariants retained as background coordinates for control and interpretation.

## Axis Roles

### Control Axes (stable invariants)

- `M_C`
- `Omega`
- `S=v2+v3`
- Role: coordinate/background system for normalization, comparability, and sanity checks.

### Signal Axes (active symmetry breaking)

- `DeltaH_cramer`
- `H(Delta-r)`
- `Q_cramer`
- Role: primary Stage-6 detection and model-selection targets.

## Stage-6 Model Program (explicit)

### Objective

Fit and compare HL/Singular-Series family models on the three signal axes (`DeltaH_cramer`, `H(Delta-r)`, `Q_cramer`) under strict out-of-sample evaluation.

### Required Protocol

- Train/Holdout split on each experiment run.
- `Delta-r` holdout: rotating leave-one-`Delta-r`-class-out.
- Scale holdout: leave-one-scale-out (`N`) cross-scale tests.
- Report AIC/BIC as secondary in-sample diagnostics (never primary ranking metric).
- Residual diagnostics required per winning family (structure, heteroskedasticity, outlier concentration).
- Explicit benchmark comparison against Wheel-210 baselines.

### Decision Rule

- Primary ranking: out-of-sample error metrics on holdout folds.
- Secondary checks: parameter stability, AIC/BIC, residual behavior, and Wheel-210 robustness gap.
- Interpretation stance: mechanism remains open until signal-axis winners remain stable across both holdout regimes and Wheel-210 comparisons.

## Immediate Next Priorities

1. Freeze Stage-6 signal-axis benchmark table for `DeltaH_cramer`, `H(Delta-r)`, `Q_cramer`.
2. Run full `Delta-r` holdout cycle with unified error leaderboard and residual diagnostics.
3. Run scale-holdout (`N`) validation and compare winner stability.
4. Perform explicit Wheel-210 counterfactual benchmark against all shortlisted HL/Singular-Series families.
5. Promote only cross-holdout stable winners to Stage-7 mechanistic interpretation.
