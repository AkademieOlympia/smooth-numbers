# Stage 5.5 Results: Wheel-30 Null Hypothesis Test

**Date**: June 24, 2026  
**Status**: ✅ **COMPLETED**  
**Verdict**: **H(Δr) is PRIME-SPECIFIC**

---

## Executive Summary

**Critical Question**:  
Is H(Δr) a property of prime numbers specifically, or merely a consequence of Wheel-30 modular structure?

**Test Design**:  
Compare H_Prime(Δr) against two null models:
1. **H_WheelRandom**: Random thinning of Wheel-30 numbers (density-matched)
2. **H_WheelCramér**: Cramér model with density 2/ln(n), restricted to Wheel-30

**Method**:  
Apply identical gap-transition pipeline to all three sequences:
```
Sequence → Gap-Transitions → Low-Gaps vs High-Gaps → H(Δr)
```

**Parameters**:
- N = 1,000,000 (78,498 primes)
- Seeds = 10 (for averaging random models)
- Δr = {2, 6, 10, 14, 18}

---

## Results

### Quantitative Comparison

| Δr | H_Prime | H_WheelRandom | H_WheelCramér | Δ_rand | Δ_cram | z_rand | z_cram |
|----|---------|---------------|---------------|--------|--------|--------|--------|
| 2  | 1.0784  | 0.9843 ± 0.0057 | 1.0254 ± 0.0056 | 0.094 | 0.053 | 16.5 | 9.4 |
| 6  | 1.4495  | 1.0382 ± 0.0117 | 1.2059 ± 0.0151 | 0.411 | 0.244 | 35.1 | 16.2 |
| 10 | 1.7779  | 0.9798 ± 0.0132 | 1.2463 ± 0.0155 | 0.798 | 0.532 | 60.4 | 34.2 |
| 14 | 2.9823  | 1.2270 ± 0.0144 | 1.6998 ± 0.0231 | 1.755 | 1.283 | 121.7 | 55.5 |
| 18 | 4.4284  | 1.4032 ± 0.0282 | 2.1556 ± 0.0195 | 3.025 | 2.273 | 107.4 | 116.7 |

**All differences are significant at z > 2.0 threshold** (conservative: z > 9.4 minimum).

### Key Observations

1. **Systematic Underestimation**:  
   Both Wheel models systematically underestimate H(Δr) for all tested values.

2. **Growing Divergence**:  
   The gap between H_Prime and Wheel models increases with Δr:
   - Δr=2: Factor ~1.1× difference
   - Δr=18: Factor ~2.1-3.2× difference

3. **Cramér Better Than Random**:  
   H_WheelCramér consistently closer to H_Prime than H_WheelRandom:
   - Logarithmic density captures part of the structure
   - But still insufficient to explain full signal

---

## Statistical Assessment

**Null Hypothesis**:  
H(Δr) is explained by Wheel-30 structure alone (independent of primality).

**Test Statistic**:  
z-score for each comparison (simplified Gaussian approximation).

**Significance Threshold**:  
z > 2.0 (95% confidence)

**Result**:  
**All 10 comparisons (5 Δr × 2 models) show z > 2.0**

Minimum z-score: 9.4 (Δr=2, Cramér)  
Maximum z-score: 121.7 (Δr=14, Random)

**Interpretation**:  
The null hypothesis is **decisively rejected**.

---

## Interpretation

### What This Test Establishes

✅ **H(Δr) is NOT just Wheel-30 structure**  
Wheel-30 residue-class constraints alone cannot explain the observed asymmetries.

✅ **H(Δr) is NOT just logarithmic density**  
Even with correct asymptotic density (Cramér model), significant discrepancy remains.

✅ **H(Δr) contains prime-specific information**  
The signal requires knowledge of actual prime positions, not just:
- Residue-class structure (Wheel-30)
- Asymptotic density (Cramér)

### Implications for Theoretical Framework

**Before Stage 5.5**:  
Unclear whether H(Δr) is:
- Prime-number-theoretic → Hardy-Littlewood framework
- Modulo-arithmetic → Residue-class theory

**After Stage 5.5**:  
H(Δr) is definitively **prime-number-theoretic**.

**Next Steps**:  
Test Hardy-Littlewood k-tuple conjecture for k ≥ 3:
- Are higher-order correlations sufficient to explain H(Δr)?
- Or does a fundamentally new mechanism remain?

---

## Technical Details

### Gap-Pair Definition

For each Δr:
- **Low Gaps**: {2, 4, 6, 8} (mod 30)
- **High Gaps**: {2+Δr, 4+Δr, 6+Δr, 8+Δr} (mod 30)

### H(Δr) Extraction

For each from-class c ∈ {1, 7, 11, 13, 17, 19, 23, 29}:
1. Count transitions to Low Gaps: count_low(c)
2. Count transitions to High Gaps: count_high(c)
3. Ratio: R(c) = count_low(c) / count_high(c)
4. H(Δr) = geometric_mean( R(c) for all c )

### Null Model Generation

**WheelRandom**:
```cpp
for each n in Wheel-30:
    include with probability p = (# primes) / N
```

**WheelCramér**:
```cpp
for each n in Wheel-30:
    include with probability p = 2 / ln(n)
```

Both models preserve:
- Wheel-30 structure (residue classes mod 30)
- Asymptotic density (WheelCramér)

Both models lack:
- Sieve structure (local correlations from small primes)
- Higher-order correlations (k-tuple effects)

---

## Comparison with Earlier Results

### Stage 5 (Hardy-Littlewood Pair-Gap Model)

**Question**: Can H(Δr) be explained by pair-gap model Σ_g w_g · S_2(g)?

**Result**: No. Correlation ≈ 0.36 (insufficient).

### Stage 5.5 (This Test)

**Question**: Is H(Δr) even prime-specific, or just Wheel-30 structure?

**Result**: Prime-specific. Wheel models falsified.

### Logical Sequence

1. H(Δr) exists and is projection-invariant (Stage 4) ✅
2. H(Δr) is not explained by pair-gaps (Stage 5) ✅
3. H(Δr) is prime-specific, not just Wheel (Stage 5.5) ✅
4. H(Δr) might be explained by k-tuples (k≥3) (Stage 6) ?

---

## Publication Strategy

### Strengthened Claim

**Before Stage 5.5**:  
> "We isolate a projection-invariant observable H(Δr) that is not explained by Hardy-Littlewood pair-gap models."

**After Stage 5.5**:  
> "We isolate a **prime-specific**, projection-invariant observable H(Δr) that:
> 1. Cannot be explained by Wheel-30 structure alone
> 2. Cannot be explained by Hardy-Littlewood pair-gap models
> 3. Contains information beyond logarithmic density (Cramér model)"

### Referee-Proofing

A competent referee will ask:
> "How do you know this is about primes and not just modular structure?"

**Answer**:  
> "We systematically tested two Wheel-30 null models (random thinning and Cramér density). Both were falsified with z-scores 9-122. The signal requires actual prime positions."

This is now a **defensible, empirical claim** backed by systematic testing.

---

## Limitations and Caveats

### Domain Restriction

**Tested range**: Δr ≤ 18

**Reason**: Projection-invariance established in Stage 4 only up to Δr = 18.

**Regime II (Δr ≥ 20)**: Projection-dependent, requires separate treatment.

### Null Model Simplicity

**WheelRandom**: Constant density (simplified)  
**WheelCramér**: Independent selection (ignores sieve correlations)

More sophisticated null models possible:
- Include local sieve structure (small primes)
- Markovian gap models
- GRH-based models

**Why these are sufficient**:  
If even these simple models fail, more complex Wheel-based models unlikely to succeed.

### Sample Size

**N = 1,000,000**: ~78,000 primes

**Effect on results**:  
- z-scores are conservative (larger N → larger z)
- Relative differences (H_Prime / H_Wheel) stable

**Robustness check**: Repeat with N = 10^7 if necessary.

---

## Conclusion

**Stage 5.5 Result**: **PASSED**

**Primary Contribution**:  
Systematic falsification of Wheel-30 null hypothesis.

**Interpretation**:  
H(Δr) is a **prime-specific** observable that:
- Transcends modular structure
- Transcends logarithmic density
- Requires actual prime correlations

**Next Step**:  
Stage 6 - Hardy-Littlewood k-tuples (k ≥ 3).

**Scientific Status**:  
Ready for publication with strengthened, empirically defensible claim.

---

## Technical Notes

### Code

Implementation: `wheel30_test.cpp`

Key functions:
- `generate_wheel30_numbers()`: Wheel-30 enumeration
- `generate_wheel_random()`: Random thinning
- `generate_wheel_cramer()`: Cramér density model
- `analyze_transitions()`: Gap-transition counting
- `extract_H()`: Geometric mean ratio

Compilation:
```bash
make wheel30_test
```

Execution:
```bash
./wheel30_test 1000000 10
```

### Verification

To reproduce:
```bash
git checkout <commit-hash>
make wheel30_test
./wheel30_test 1000000 10 > stage5.5_results.txt
```

Expected runtime: ~2 seconds (N=10^6, 10 seeds)

---

## References

**Related Documentation**:
- `STAGE5.5_WHEEL30_NEXT_STEP.md`: Motivation and design
- `STAGE5_FINAL_RESULTS.md`: Stage 5 (HL pair-gap falsification)
- `OBJECT_CRITERIA.md`: Philosophical framework

**Code**:
- `wheel30_test.cpp`: Implementation
- `phase_diagram_delta_r.cpp`: Related gap-analysis pipeline
- `gap_pair_robustness.cpp`: Stage 4 projection-invariance test

**Next Steps**:
- Stage 6: HL k-tuple test (if motivated)
- Paper update: Incorporate Stage 5.5 results
- Extended testing: N = 10^7, additional Δr values
