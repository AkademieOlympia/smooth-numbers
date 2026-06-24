# Noether-Invariance Scan Report

## Scope

- Frame: **Noether-inspired heuristic** (no strong physical theorem claim).
- Catalan/EABC samples: `8000` numbers.
- Gap runs used: `3` with delta-r classes `[2, 6, 10, 14, 18]`.
- Total tested transformations: `50`.

## Transformation catalog

| Domain | Family | Count |
|---|---|---:|
| both | identity | 1 |
| catalan | chirality_flip | 1 |
| catalan | eabc_cycle | 1 |
| catalan | eabc_permutation | 23 |
| catalan | signature_reversal | 1 |
| gap | gap_chirality | 1 |
| gap | gap_cycle | 4 |
| gap | gap_transposition | 10 |
| gap | wheel210_congruence | 4 |
| gap | wheel30_congruence | 4 |

### Operations T on states/labels

| T name | Domain | Family | Operation on state |
|---|---|---|---|
| `identity` | both | identity | No transformation |
| `eabc_cycle_E_to_A_to_B_to_C` | catalan | eabc_cycle | Cycle E->A->B->C->E |
| `eabc_chirality_flip_A_C` | catalan | chirality_flip | Swap A and C labels |
| `signature_reversal` | catalan | signature_reversal | Reverse EABC signature order |
| `eabc_perm_EACB` | catalan | eabc_permutation | Permutation EABC->EACB |
| `eabc_perm_EBAC` | catalan | eabc_permutation | Permutation EABC->EBAC |
| `eabc_perm_EBCA` | catalan | eabc_permutation | Permutation EABC->EBCA |
| `eabc_perm_ECAB` | catalan | eabc_permutation | Permutation EABC->ECAB |
| `eabc_perm_ECBA` | catalan | eabc_permutation | Permutation EABC->ECBA |
| `eabc_perm_AEBC` | catalan | eabc_permutation | Permutation EABC->AEBC |
| `eabc_perm_AECB` | catalan | eabc_permutation | Permutation EABC->AECB |
| `eabc_perm_ABEC` | catalan | eabc_permutation | Permutation EABC->ABEC |
| `eabc_perm_ABCE` | catalan | eabc_permutation | Permutation EABC->ABCE |
| `eabc_perm_ACEB` | catalan | eabc_permutation | Permutation EABC->ACEB |
| `eabc_perm_ACBE` | catalan | eabc_permutation | Permutation EABC->ACBE |
| `eabc_perm_BEAC` | catalan | eabc_permutation | Permutation EABC->BEAC |
| `eabc_perm_BECA` | catalan | eabc_permutation | Permutation EABC->BECA |
| `eabc_perm_BAEC` | catalan | eabc_permutation | Permutation EABC->BAEC |
| `eabc_perm_BACE` | catalan | eabc_permutation | Permutation EABC->BACE |
| `eabc_perm_BCEA` | catalan | eabc_permutation | Permutation EABC->BCEA |
| `eabc_perm_BCAE` | catalan | eabc_permutation | Permutation EABC->BCAE |
| `eabc_perm_CEAB` | catalan | eabc_permutation | Permutation EABC->CEAB |
| `eabc_perm_CEBA` | catalan | eabc_permutation | Permutation EABC->CEBA |
| `eabc_perm_CAEB` | catalan | eabc_permutation | Permutation EABC->CAEB |
| `eabc_perm_CABE` | catalan | eabc_permutation | Permutation EABC->CABE |
| `eabc_perm_CBEA` | catalan | eabc_permutation | Permutation EABC->CBEA |
| `eabc_perm_CBAE` | catalan | eabc_permutation | Permutation EABC->CBAE |
| `dr_cycle_shift_1` | gap | gap_cycle | Cycle shift over ordered delta_r list by 1 |
| `dr_cycle_shift_2` | gap | gap_cycle | Cycle shift over ordered delta_r list by 2 |
| `dr_cycle_shift_3` | gap | gap_cycle | Cycle shift over ordered delta_r list by 3 |
| `dr_cycle_shift_4` | gap | gap_cycle | Cycle shift over ordered delta_r list by 4 |
| `dr_chirality_reverse` | gap | gap_chirality | Reverse ordered delta_r labels |
| `dr_transposition_2_6` | gap | gap_transposition | Swap delta_r=2 and delta_r=6 |
| `dr_transposition_2_10` | gap | gap_transposition | Swap delta_r=2 and delta_r=10 |
| `dr_transposition_2_14` | gap | gap_transposition | Swap delta_r=2 and delta_r=14 |
| `dr_transposition_2_18` | gap | gap_transposition | Swap delta_r=2 and delta_r=18 |
| `dr_transposition_6_10` | gap | gap_transposition | Swap delta_r=6 and delta_r=10 |
| `dr_transposition_6_14` | gap | gap_transposition | Swap delta_r=6 and delta_r=14 |
| `dr_transposition_6_18` | gap | gap_transposition | Swap delta_r=6 and delta_r=18 |
| `dr_transposition_10_14` | gap | gap_transposition | Swap delta_r=10 and delta_r=14 |
| `dr_transposition_10_18` | gap | gap_transposition | Swap delta_r=10 and delta_r=18 |
| `dr_transposition_14_18` | gap | gap_transposition | Swap delta_r=14 and delta_r=18 |
| `wheel30_add4k_1` | gap | wheel30_congruence | delta_r -> delta_r + 4*1 (wrapped over sampled classes) |
| `wheel210_add8k_1` | gap | wheel210_congruence | delta_r -> delta_r + 8*1 (wrapped over sampled classes) |
| `wheel30_add4k_2` | gap | wheel30_congruence | delta_r -> delta_r + 4*2 (wrapped over sampled classes) |
| `wheel210_add8k_2` | gap | wheel210_congruence | delta_r -> delta_r + 8*2 (wrapped over sampled classes) |
| `wheel30_add4k_3` | gap | wheel30_congruence | delta_r -> delta_r + 4*3 (wrapped over sampled classes) |
| `wheel210_add8k_3` | gap | wheel210_congruence | delta_r -> delta_r + 8*3 (wrapped over sampled classes) |
| `wheel30_add4k_4` | gap | wheel30_congruence | delta_r -> delta_r + 4*4 (wrapped over sampled classes) |
| `wheel210_add8k_4` | gap | wheel210_congruence | delta_r -> delta_r + 8*4 (wrapped over sampled classes) |

## Method

- Invariance score: `I_T(O)=mean|O - O o T|`.
- Normalized score: `I_norm = I_T(O)/(mean|O|+eps)`.
- Classification thresholds:
  - `invariant` (`I_norm < 0.03`)
  - `weak_sensitive` (`0.03 <= I_norm < 0.15`)
  - `strong_symmetry_breaking` (`I_norm >= 0.15`)
- Permutation p-value is reported as an invariance diagnostic (small p means unusually invariant).

## Most invariant observables (aggregate over non-identity transforms)

1. `M_C` with mean `I_norm=0.000000`
2. `Omega` with mean `I_norm=0.000000`
3. `S` with mean `I_norm=0.000000`

## Strongest symmetry-breaking observables (aggregate over non-identity transforms)

1. `DeltaH_cramer` with mean `I_norm=0.851579`
2. `H(delta_r)` with mean `I_norm=0.450727`
3. `Q_cramer` with mean `I_norm=0.223465`

## Noether-inspired interpretation (defensive)

- Observables with near-zero sensitivity are robust candidates for structural descriptors.
- Observables with larger sensitivity under wheel/cycle/permutation-like transforms are symmetry-break indicators.
- For ongoing program logic: symmetry-breaking channels provide concrete targets for Stage-6 HL-aligned modeling.

## Relation to Stage-5.5/5.6 signals

- The strongest symmetry breaks concentrate in gap-strand observables `H(delta_r)`, `DeltaH_cramer`, and `Q_cramer`.
- This is consistent with Stage-5.5/5.6 where wheel-based controls do not absorb the prime-side signal.
- Practical reading: robust structural axes are mostly in Catalan/EABC scalar geometry, while residual signal lives in gap symmetry-breaking channels.

## Artifacts

- Table: `experiments/results/noether/noether_invariance_table.csv`
- Plot: `experiments/results/noether/noether_invariance_plots.png`
- Program doc: `docs/NOETHER_INVARIANCE_PROGRAM.md`
- Script: `code/experiments/noether_invariance_scan.py`
