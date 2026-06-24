# Noether-Inspired Invariance Program

## Scope and stance

- This program is **Noether-inspired**, not a claim of a classical theorem in this discrete setting.
- Goal: test which existing observables are approximately invariant under natural transformations.
- Output labels are empirical: `invariant`, `weak_sensitive`, `strong_symmetry_breaking`.

## Research Architecture v2 alignment

The symmetry program now uses a two-layer architecture:

- Stable invariant axes (`M_C`, `Omega`, `S=v2+v3`) form the coordinate background.
- Active symmetry-breaking axes (`DeltaH_cramer`, `H(Delta-r)`, `Q_cramer`) form the discovery space.

Interpretation rule: invariants provide control coordinates and comparability; primary Stage-6 model selection is driven by the signal axes.

## State model

- Catalan/EABC state per number `n` includes:
  - scalar observables `M_C`, `Omega`, `S` (control coordinates), `E(n)`, `H(n)`, `L(n)` and optional `D(n)`, `B(n)`
  - label state `(E,A,B,C)` counts and EABC signature string
- Gap state per Stage-5.5 run includes vectors over sampled `delta_r` classes:
  - `H(delta_r)`, `DeltaH_cramer(delta_r)`, `Q_cramer(delta_r)` (primary Stage-6 signal axes)

## Transformation catalog

- EABC cycle: `E->A->B->C->E`
- EABC permutations: all non-identity permutations (includes transpositions)
- Signature reversal and chirality flip (`A<->C`)
- Wheel-related label operations on sampled `delta_r` classes:
  - wheel30-style additive shifts
  - wheel210-style additive shifts
  - cycle/reversal/transposition operations on sampled `delta_r` labels

## Formal operation view

- Let a Catalan/EABC state be `x=(o, c, s)` with
  - `o`: scalar observables (`M_C, Omega, S, E, H, L, D, B`)
  - `c=(e,a,b,c)`: EABC class counts
  - `s`: EABC signature string
- For label permutation `pi in S4`: `T_pi(x)=(o', c', s')` where
  - `c' = P_pi c` (permutation matrix action)
  - `s'` is relabeled symbol-wise by `pi`
  - tree-structure observables (`M_C, D, B, Omega, S`) stay unchanged
- EABC cycle is a special `pi_cycle=(E A B C)`.
- Chirality flip is `pi_chi=(A C)` with `E,B` fixed.
- Signature reversal is `T_rev(x)=(o, c, reverse(s))`.
- Gap state `g=(delta_r, v)` with vector observable `v(delta_r)`.
- Gap transformation acts as index permutation `sigma`: `T_sigma(g)=(delta_r, v o sigma)`.

## Invariance metrics

- Main score: `I_T(O) = mean |O - O o T|`
- Normalized score: `I_norm = I_T(O) / (mean|O| + eps)`
- Effect scale: `I_T(O) / (std(O) + eps)`
- Permutation-based `p_perm_invariance`:
  - compare observed `I_T(O)` against random re-pairings of transformed values
  - small p indicates unusually strong invariance under `T`

## Classification

- `invariant`: `I_norm < 0.03`
- `weak_sensitive`: `0.03 <= I_norm < 0.15`
- `strong_symmetry_breaking`: `I_norm >= 0.15`

## Reproducibility

- Script: `code/experiments/noether_invariance_scan.py`
- Deterministic seed is fixed in the script/CLI (`--seed`).
- Main results exported to CSV/MD/PNG in `experiments/results/noether/`.

## Stage-6 interface requirements

- Stage 6 uses HL/Singular-Series family modeling on `DeltaH_cramer`, `H(delta_r)`, `Q_cramer`.
- Validation is out-of-sample by design: Train/Holdout, `Delta-r` holdout, and scale holdout.
- AIC/BIC are tracked as secondary diagnostics only.
- Residual diagnostics are mandatory before promotion of a candidate family.
- All selected families are compared against Wheel-210 benchmarks before mechanistic claims.
