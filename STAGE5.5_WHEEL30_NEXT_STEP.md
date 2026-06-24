# Stage 5.5: Wheel-30 Null Hypothesis (Critical Next Step)

**Status**: 🔴 **NOT YET COMPLETED** - Implementation in progress  
**Priority**: **CRITICAL before publication**  
**Date**: June 23, 2026  

---

## The Critical Question

Before claiming H(Δr) is prime-specific, we must test:

```
H_Prime(Δr) ≟ H_Wheel-30(Δr)
```

for Δr ≤ 18.

**Why this test is critical**:

A referee will immediately ask:
> "How do you know H(Δr) measures something about **primes** and not just about **modulo-30 structure**?"

This question is currently **unanswered**.

---

## Test Design

### Three Models to Compare

1. **H_Prime**: Real primes
2. **H_WheelRandom**: Random thinning of Wheel-30 numbers
   - n ≡ 1,7,11,13,17,19,23,29 (mod 30)
   - Random selection with density matching primes
3. **H_WheelCramér**: Cramér with density 2/ln(n), restricted to Wheel-30
   - Models logarithmic density + Wheel structure

### Methodology

**CRITICAL**: Apply **exact same pipeline** to all three:

```
Sequence → Gap-Transitions → A_i(Δr) → H(Δr)
```

Not just gap distributions, but the full extraction operator including:
- Same gap-pair definitions (Base 2, 4, 6, 8)
- Same Δr values (2, 6, 10, 14, 18)
- Same averaging over projections

---

## Decision Matrix

| Result | Interpretation | Next Steps |
|--------|----------------|------------|
| H_Prime ≈ H_WheelRandom | Wheel structure explains core | **No need for HL k≥3**<br>Focus on modulo-arithmetic |
| H_Prime ≈ H_WheelCramér ≠ H_WheelRandom | log-density + Wheel explains core | Prime-specific but not higher-order |
| H_Prime ≠ both | **Prime-specific correlation** | HL k-tuples (k≥3) motivated |

---

## Why This Test Comes Before k-tuple HL

**Logical sequence**:

1. ✓ **Stage 4**: H(Δr) is projection-invariant
2. ✓ **Stage 5**: H(Δr) ≉ ∑_g w_g · S_2(g)
3. **Stage 5.5**: Is H(Δr) prime-specific or just Wheel? ← **WE ARE HERE**
4. **Stage 6** (only if 5.5 → prime-specific): Test HL k≥3

**Without Stage 5.5**, jumping to k-tuple HL is premature:
- If H(Δr) is just Wheel structure, HL k-tuples are irrelevant
- Wasting effort on wrong theoretical framework

---

## Expected Outcomes

### Scenario A: H_Prime ≈ H_Wheel (either variant)

**Interpretation**: H(Δr) is **not prime-specific**

**Implications**:
- The object characterizes **modulo-30 residue-class structure**
- Not a prime-number-theoretic observable
- Theoretical direction: Modulo-arithmetic, not HL

**Publication framing**:
- "Residue-class gap asymmetries in Wheel-30 structures"
- Methodological contribution remains valid
- But not a "prime-specific" discovery

---

### Scenario B: H_Prime ≠ H_Wheel (both variants)

**Interpretation**: H(Δr) contains **prime-specific information**

**Implications**:
- Beyond modulo-30 structure alone
- Higher-order correlations plausible
- HL k-tuples (k≥3) become natural next test

**Publication framing**:
- "Prime-specific residue-class observable"
- HL k-tuple investigation motivated
- Stronger claim possible

---

## Implementation Requirements

### Technical Details

**Wheel-30 numbers**: n where n ≡ 1,7,11,13,17,19,23,29 (mod 30)

**WheelRandom generation**:
```
For each n in Wheel-30:
    Include with probability p_target
```
where p_target matches prime density.

**WheelCramér generation**:
```
For each n in Wheel-30:
    Include with probability 2/ln(n)
```

**Critical**: Use **same gap-transition analysis** as for primes.

---

## Why Implementation is Non-Trivial

### The Challenge

The gap-pair extraction operator is complex:
- Depends on gap modulo 30
- Depends on residue-class transitions
- Multiple projection bases (2, 4, 6, 8)
- Averaging over projections to get H(Δr)

**Must replicate exact pipeline** from:
- `phase_diagram_delta_r.cpp`
- `gap_pair_robustness.cpp`

**Current status**: Implementation in progress, debugging gap-pair logic.

---

## Publication Strategy

### Before Stage 5.5 Completion

**Current claim** (conservative):
> "We isolate a projection-invariant observable H(Δr) and show it is not explained by Hardy-Littlewood pair-gap models."

**Limitation acknowledged**:
> "Further investigation is needed to determine whether H(Δr) is prime-specific or a general property of Wheel-30 structures."

**Framing**:
- Methodological contribution (projection-invariance testing)
- Falsification of HL k=2 models
- Framework for future investigation

---

### After Stage 5.5 Completion

**If H_Prime ≠ H_Wheel** (Scenario B):

Upgrade claim to:
> "We isolate a **prime-specific**, projection-invariant observable H(Δr)..."

Remove limitation, add:
> "Systematic comparison with Wheel-30 null models demonstrates H(Δr) contains information beyond simple modulo structure."

**If H_Prime ≈ H_Wheel** (Scenario A):

Downgrade claim to:
> "We isolate a projection-invariant property of Wheel-30 residue-class structures..."

Shift focus to:
- Modulo-arithmetic interpretation
- Not prime-number-theory per se

---

## Timeline

### Immediate (Before Submission)

1. **Complete Stage 5.5 implementation** (debugging gap-pair logic)
2. **Run test** with N = 10^6, multiple seeds
3. **Update paper** based on outcome
4. **Submit**

**Estimated time**: 2-4 hours additional implementation + testing

---

## Why This Cannot Be Skipped

### Referee Perspective

A competent referee will **immediately** ask:

> "Your observable is defined over residue-classes modulo 30. How do you know it's not just a property of the residue system itself, independent of primality?"

**Without Stage 5.5**, we have no answer.

**With Stage 5.5**:
- **Scenario A**: "You're right, it's Wheel structure" (important negative result)
- **Scenario B**: "We tested that - it's prime-specific" (strong positive result)

---

## Current Understanding

### What We Know

1. ✓ H(Δr) exists (Stage 1)
2. ✓ H(Δr) is reproducible (Stage 2)
3. ✓ H(Δr) is model-independent (Stage 3)
4. ✓ H(Δr) is projection-invariant for Δr ≤ 18 (Stage 4)
5. ✓ H(Δr) ≉ ∑_g w_g · S_2(g) (Stage 5)

### What We Don't Know

6. **Is H(Δr) prime-specific or Wheel-30 structure?** ← Stage 5.5
7. **Can H(Δr) be explained by HL k-tuples (k≥3)?** ← Stage 6 (if 5.5 → prime-specific)

---

## Conclusion

**Stage 5.5 is the next critical test** before any publication.

**It determines**:
- Whether H(Δr) is a **prime-number-theoretic** observable
- Or a **modulo-arithmetic** property

**Both outcomes are valuable**, but they lead to **different theoretical frameworks**:
- Prime-specific → Hardy-Littlewood k-tuples
- Wheel structure → Modulo-arithmetic theory

**Action item**: Complete implementation, run test, update paper accordingly.

---

## References for Implementation

**Working code to adapt**:
- `phase_diagram_delta_r.cpp` - Gap-transition analysis
- `gap_pair_robustness.cpp` - Projection-invariance pipeline

**Key functions needed**:
- `analyze_gaps()` - Gap-transition matrix
- `generate_gap_pairs_for_delta_r()` - Gap-pair definitions
- `compute_mean_ratio()` - R_gap calculation
- `extract_H()` - Averaging over projections
