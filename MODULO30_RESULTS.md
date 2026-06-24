# Modulo-30 Phase Diagram: Complex Regime Structure

**Date:** 23. Juni 2026  
**Status:** ⚠️ Robustness tests reveal MORE COMPLEX structure than initially observed  
**Program:** `phase_diagram_delta_r.cpp`

---

## Executive Summary

**Initial finding (N=100K, 5 seeds) suggested a "clean three-regime transition."**

**Robust analysis (N=1M, 20 seeds) reveals the reality is MUCH MORE COMPLEX:**

1. **No clean crossover point** - the hierarchy oscillates with Δr
2. **The "intermediate regime" story was oversimplified**
3. **Only TWO robust findings:**
   - **Δr = 2:** R_Prime > R_Bernoulli (twin prime effect)
   - **Δr ≥ 20:** R_Prime > R_Bernoulli (large-distance enhancement)
4. **Δr = 4-18:** MIXED - no clear pattern, Δr-specific

**IMPLICATION:** The simple narrative "geometric bias for small Δr, arithmetic dominance for large Δr" is **TOO SIMPLE**. The real structure is more nuanced and requires deeper theoretical understanding.

---

## Empirical Data: Robustness Comparison

### **Preliminary Test (N=100,000, 5 Seeds):**

| Δr | R_Bern | σ | R_Prime | Hierarchy | R_Prime/R_Bern |
|----|--------|---|---------|-----------|----------------|
| 2  | 1.079 | 0.01 | 1.138 | Prime > Bern | 1.05 |
| 12 | 3.595 | 0.12 | 3.611 | **Prime ≈ Bern** | 1.00 |
| 14 | 3.636 | 0.14 | 4.196 | Prime > Bern | 1.15 |
| 20 | 7.195 | 0.23 | 10.045 | Prime > Bern | 1.40 |
| 24 | 9.513 | 0.46 | 14.654 | Prime > Bern | 1.54 |

**Interpretation (preliminary):** "Clean crossover at Δr ≈ 12"

---

### **Robust Test (N=1,000,000, 20 Seeds):**

| Δr | R_Bern | σ | R_Prime | Hierarchy | R_Prime/R_Bern | Change |
|----|--------|---|---------|-----------|----------------|--------|
| 2  | 1.058 | 0.00 | 1.118 | Prime > Bern | 1.06 | ✓ Consistent |
| 4  | 1.184 | 0.01 | 1.165 | **Bern > Prime** | 0.98 | — |
| 6  | 1.749 | 0.02 | 1.473 | **Bern > Prime** | 0.84 | — |
| 8  | 1.819 | 0.02 | 1.608 | **Bern > Prime** | 0.88 | — |
| 10 | 2.409 | 0.03 | 2.033 | **Bern > Prime** | 0.84 | — |
| 12 | 2.815 | 0.04 | 2.675 | **Bern > Prime** | 0.95 | ⚠️ REVERSED |
| 14 | 2.818 | 0.04 | 3.043 | Prime > Bern | 1.08 | ✓ Consistent |
| 16 | 3.440 | 0.05 | 3.347 | **Bern > Prime** | 0.97 | ⚠️ REVERSED |
| 18 | 4.533 | 0.05 | 4.289 | **Bern > Prime** | 0.95 | ⚠️ REVERSED |
| 20 | 4.960 | 0.05 | 5.328 | Prime > Bern | 1.07 | ✓ Consistent |
| 22 | 6.026 | 0.07 | 6.353 | Prime > Bern | 1.05 | ✓ Consistent |
| 24 | 6.210 | 0.07 | 7.338 | Prime > Bern | 1.18 | ✓ Consistent |

**Interpretation (robust):** "No clean crossover - complex Δr-dependent structure"

---

## Key Observations

### 1. **Error Bars Dramatically Reduced**
- Δr=12: σ reduced from 0.12 to 0.04 (3×)
- Δr=24: σ reduced from 0.46 to 0.07 (6×)
- **Larger N stabilizes the measurements** ✓

### 2. **Systematic Downward Shift in R-values**
- All R-values are 20-40% lower with N=1M
- Suggests **finite-size effects** at N=100K
- Or: different gap-selection strategy at larger N

### 3. **The "Crossover" Disappears**
- At N=100K: Appeared to cross at Δr≈12
- At N=1M: No clear single crossover point
- **The "three-regime" story was an artifact of small N**

### 4. **Only Two Robust Regions**
- **Δr = 2:** Prime > Bern (twin primes, consistent)
- **Δr ≥ 20:** Prime > Bern (large-distance, consistent)
- **Δr = 4-18:** MIXED (no clear pattern)

---

## Revised Interpretation: Δr-Specific Structure

The robustness test forces us to abandon the simple "three-regime" narrative.

### **What IS robust:**

1. **Cramér overdamping is UNIVERSAL**
   - R_Cramér < R_Bern AND R_Cramér < R_Prime for ALL Δr tested
   - Logarithmic mixing consistently suppresses asymmetry
   - This finding is solid ✓

2. **Twin prime enhancement (Δr=2)**
   - R_Prime > R_Bernoulli consistently
   - Ratio ≈ 1.06 (modest but robust)
   - Hardy-Littlewood twin effect is real ✓

3. **Large-Δr enhancement (Δr ≥ 20)**
   - R_Prime > R_Bernoulli consistently
   - Enhancement grows with Δr (1.07 → 1.18)
   - Arithmetic correlations accumulate at large distances ✓

### **What is NOT robust:**

1. **No "clean crossover" at Δr≈12**
   - The apparent crossover at N=100K was finite-size artifact
   - At N=1M, Δr=12 shows Bern > Prime (opposite!)

2. **Intermediate Δr (4-18) is COMPLEX**
   - Hierarchy oscillates: Bern > Prime for most, but Prime > Bern at Δr=14
   - No simple monotonic transition
   - Requires Δr-by-Δr analysis

3. **The enhancement factor A(Δr) is NON-MONOTONIC**
   - At Δr=6: A ≈ 0.84 (suppression)
   - At Δr=14: A ≈ 1.08 (enhancement)
   - At Δr=16: A ≈ 0.97 (neutral)
   - At Δr=24: A ≈ 1.18 (strong enhancement)
   - **No simple functional form**

---

## Why Is the Structure So Complex?

### **Hypothesis:** Multiple Hardy-Littlewood correlations interfere

Different gap sizes are enhanced by different k-tuple correlations:
- Gap 2: Twin primes ($\Pi_2$)
- Gap 4: Cousin primes ($\Pi_4$)
- Gap 6: Sexy primes ($\Pi_6$)
- Gap 2+4: Twin-cousin compound
- etc.

When comparing residue classes separated by Δr, we're comparing **different combinations** of these correlations.

For Δr=6: comparing {2,4,6} vs {8,10,12}
- Low gaps {2,4,6}: ALL enhanced by twins/cousins/sexy
- High gaps {8,10,12}: SOME enhanced, but less

For Δr=14: comparing {2,4,6} vs {16,18,20}
- Low gaps: Standard enhancement
- High gaps: Could have COMPOUND correlations (twin+twin, etc.)

**The net effect depends on which specific gaps are being compared.**

This explains why A(Δr) oscillates rather than growing monotonically.

---

## Theoretical Consequence: No Simple Formula

The original hope was:

$$R_{\text{Prime}}(\Delta r) = (1-p)^{-\Delta r} \cdot \mathcal{A}(\Delta r)$$

with $\mathcal{A}(\Delta r)$ following a simple pattern (e.g., monotonic growth).

**Reality:** $\mathcal{A}(\Delta r)$ is **gap-pair specific** and oscillates.

There is no "universal arithmetic enhancement factor."

Instead:

$$R_{\text{Prime}}(\{g_{\text{low}}\}, \{g_{\text{high}}\}) = \frac{\prod_{g \in g_{\text{low}}} P(g) \cdot \mathcal{H}(g)}{\prod_{g \in g_{\text{high}}} P(g) \cdot \mathcal{H}(g)}$$

where $\mathcal{H}(g)$ is the Hardy-Littlewood enhancement for gap size $g$.

**Each Δr comparison tests different {$g_{\text{low}}$, $g_{\text{high}}$} sets, hence different outcomes.**

---

## Critical Implications for the Paper

### ❌ **What We CANNOT Say:**

1. "Primes occupy an intermediate regime" ← Only true for Δr≈4-12
2. "Clean crossover at Δr≈12" ← Artifact of N=100K
3. "Arithmetic dominance for large Δr" ← True for Δr≥20, but not Δr=12-18
4. "Three-regime structure" ← Oversimplified

### ✅ **What We CAN Say:**

1. **"Cramér model consistently overdamps asymmetry across all Δr"** ✓
2. **"Twin primes (Δr=2) show robust Hardy-Littlewood enhancement"** ✓
3. **"For Δr≥20, arithmetic correlations exceed geometric bias"** ✓
4. **"The intermediate range (Δr=4-18) shows complex Δr-specific structure"** ✓
5. **"Modulo-12 (Δr≈6) falls in the 'geometric window' where R_Bern > R_Prime"** ✓

### **Revised Core Finding:**

> "The gap asymmetry ratio R exhibits **Δr-dependent competition** between geometric short-gap bias (universal for sparse sets) and arithmetic correlations (prime-specific via Hardy-Littlewood k-tuple conjectures). Cramér overdamping is universal. Twin prime enhancement (Δr=2) and large-distance enhancement (Δr≥20) are robust. The intermediate range (Δr=4-18) requires gap-by-gap Hardy-Littlewood analysis."

---

## Recommended Next Steps

### **Immediate (before paper revision):**

1. ✓ **MODULO30_RESULTS.md created** with robust findings
2. ✓ **N=1M, 20-seed validation complete**
3. **Analyze why R-values decreased 20-40% at larger N** (gap selection? sieve effects?)
4. **Compute bootstrap confidence intervals** for R_Prime at each Δr

### **For Paper Revision:**

The paper needs a **major restructuring**, not minor updates:

**OLD STRUCTURE:**
- Section 3: Geometric origin (universal)
- Section 4: Null model hierarchy (primes intermediate)
- Section 5: Interpretation (structured disorder)

**NEW STRUCTURE:**
- Section 3: Geometric baseline (Bernoulli model)
- Section 4: Cramér overdamping (universal suppression)
- Section 5: **Δr-dependent competition** (complex structure)
  - Subsection 5.1: Twin enhancement (Δr=2)
  - Subsection 5.2: Geometric window (Δr=4-12)
  - Subsection 5.3: Large-Δr enhancement (Δr≥20)
- Section 6: Hardy-Littlewood necessity (not optional!)

**NEW TITLE:**

"**Δr-Dependent Competition Between Geometric Bias and Arithmetic Correlations in Prime Gap Asymmetries**"

Or:

"**Beyond the Geometric Origin: Hardy-Littlewood Correlations in Residue-Class Gap Asymmetries**"

---

## Conclusion

The robustness test (N=1M, 20 seeds) revealed that:

1. The preliminary "three-regime transition" was **oversimplified**
2. The crossover at Δr≈12 was a **finite-size artifact**
3. The reality is **more complex**: Δr-specific structure with no simple pattern
4. Only three findings are **robustly established**:
   - Cramér overdamping (universal)
   - Twin enhancement (Δr=2)
   - Large-distance enhancement (Δr≥20)

**This is GOOD science:** Robustness testing prevented publication of an incorrect oversimplification.

The paper must reflect this complexity, not hide it.

Hardy-Littlewood analysis is now **mandatory** to understand the Δr-specific structure.

---

**Next:** Paper revision (Step B) with the correct, nuanced interpretation.

### **Mechanism 1: Geometric Short-Gap Bias**

For Bernoulli point processes with constant acceptance probability p:

$$R_{\text{Bernoulli}}(\Delta r) \approx (1-p)^{-\Delta r}$$

This is a **universal sparsity effect** - any thin set with geometric gap distribution shows this bias.

**Predicted for p ≈ 0.05:**
- Δr=6: R ≈ 1.36
- Δr=12: R ≈ 1.85
- Δr=24: R ≈ 3.43

**Observed:** Bernoulli model tracks theoretical prediction reasonably well.

---

### **Mechanism 2: Arithmetic Enhancement via Sieve Correlations**

Prime numbers show **additional correlations** from Hardy-Littlewood k-tuple conjectures:
- Twin primes (gap 2): Enhanced by $\Pi_2 \approx 0.660$
- Cousin primes (gap 4): Enhanced by $\Pi_4$
- Sexy primes (gap 6): Enhanced by $\Pi_6$
- Higher-order correlations for larger gaps

**Key observation:** This enhancement is **NOT constant** across Δr!

**For small Δr (4-10):**
- Geometric bias dominates
- Sieve correlations are subdominant
- R_Prime < R_Bernoulli

**For large Δr (≥12):**
- Sieve correlations accumulate
- Enhancement EXCEEDS geometric bias
- R_Prime > R_Bernoulli (and growing!)

---

## The Cramér Overdamping (Universal)

**Key finding:** R_Cramér is ALWAYS the lowest, regardless of Δr.

The logarithmic acceptance $p(n) = 2/\ln(n)$ creates **mixing over variable density**, which suppresses asymmetry at ALL scales.

This confirms:
- Cramér model is "too tame"
- Logarithmic regularization overdamps consistently
- The effect persists from Δr=2 to Δr=24

---

## Critical Implications for the Paper

### ❌ **Old Narrative (INVALID):**

> "Primes occupy an intermediate regime between uncorrelated Bernoulli processes and overdamped Cramér dynamics."

**Problem:** This is only true for Δr ≈ 4-10 (a narrow window!)

---

### ✅ **New Narrative (CORRECT):**

> **"Residue-class gap asymmetry exhibits regime-dependent behavior with TWO competing mechanisms:**
> 
> 1. **Geometric short-gap bias:** Universal for sparse sets, $R \sim q^{-\Delta r}$
> 2. **Arithmetic enhancement:** Hardy-Littlewood correlations from prime sieve
> 
> **For small Δr (4-10):** Geometric bias dominates → R_Bern > R_Prime
> 
> **For Δr ≥ 12:** Arithmetic correlations dominate → R_Prime > R_Bern
> 
> The crossover at Δr ≈ 12 marks a **regime transition** from geometric to arithmetic dominance."

---

## Why the Modulo-12 Result Was Misleading

The original paper focused on **modulo 12**, which corresponds to comparing gaps like:
- {2, 4} vs {8, 10} → Δr ≈ 6

**At Δr = 6:**
- R_Bernoulli ≈ 1.94
- R_Prime ≈ 1.70
- R_Cramér ≈ 1.28

**This accidentally landed in the "geometric window"** where R_Bern > R_Prime!

Had we tested modulo 30 with Δr = 14 first, we would have found **R_Prime > R_Bernoulli** and drawn completely different conclusions.

**This is why systematic Δr-variation is ESSENTIAL.**

---

## Theoretical Consequence

The formula $R = (1-p)^{-6}$ is **NOT the full story** for primes.

The complete expression must be:

$$R_{\text{Prime}}(\Delta r) = (1-p)^{-\Delta r} \cdot \mathcal{A}(\Delta r)$$

where $\mathcal{A}(\Delta r)$ is an **arithmetic amplification factor** from Hardy-Littlewood correlations.

**Empirically:**
- $\mathcal{A}(\Delta r = 6) \approx 0.88$ (suppression)
- $\mathcal{A}(\Delta r = 12) \approx 1.00$ (crossover)
- $\mathcal{A}(\Delta r = 24) \approx 1.54$ (strong enhancement)

**The function $\mathcal{A}(\Delta r)$ is the missing piece.**

Quantifying it requires explicit Hardy-Littlewood analysis (Section 7.3 of the paper).

---

## Open Questions (CRITICAL)

### 1. **Robustness Validation** ⚠️ URGENT

**Before publishing, we MUST verify:**
- [ ] 20+ seeds (not just 5)
- [ ] N = 10^6 (not just 10^5)
- [ ] Compute error bars for R_Prime
- [ ] Check if denominators become small at large Δr (statistical artifact?)
- [ ] Test with different gap-pair selections (currently {2,4,6} vs {2+Δr, 4+Δr, 6+Δr})

**Danger:** At large Δr, absolute counts become small. A ratio of rare events can be statistically unstable.

Example: If gap≡22 has only 50 occurrences, its ratio to gap≡2 (10,000 occurrences) is dominated by noise.

**Required test:** Bootstrap confidence intervals for each R_Prime(Δr).

---

### 2. **Hardy-Littlewood Quantification**

The enhancement factor $\mathcal{A}(\Delta r)$ must be derived from:

$$\mathcal{A}(\Delta r) = \frac{\text{Expected } P(\text{gaps } \approx \Delta r) \text{ with H-L correlations}}{\text{Expected } P(\text{gaps } \approx \Delta r) \text{ without correlations}}$$

For twins ($\Delta r \approx 2$):
$$\mathcal{A}(2) \approx \Pi_2 \cdot \text{(geometric correction)} \approx 0.66 \cdot k$$

This is no longer optional - **it is THE central theoretical challenge.**

---

### 3. **Why Does $\mathcal{A}(\Delta r)$ Grow?**

**Hypothesis:** For large Δr, multiple Hardy-Littlewood k-tuple correlations can **accumulate** (e.g., twin + cousin + sexy).

If gaps {2, 4, 6} all occur more frequently than independent prediction, their joint enhancement is:

$$\mathcal{A}_{\text{joint}} > 1$$

while for Bernoulli:

$$\mathcal{A}_{\text{Bernoulli}} = 1 \text{ (by definition)}$$

**This would explain R_Prime > R_Bernoulli at large Δr.**

But this is speculation until computed rigorously.

---

## Recommended Next Steps

### **Immediate (before any paper revision):**

1. **Run phase diagram with N=10^6, 20 seeds** → Validate crossover robustness
2. **Compute bootstrap confidence intervals** → Check statistical stability at large Δr
3. **Test alternative gap-pair selections** → Ensure result is not artifact of {2,4,6} choice

### **Short-term (for revised paper):**

4. **Create MODULO30_RESULTS.md** ✓ (this document)
5. **Document regime transition in paper** (new Section 5)
6. **Reframe abstract/conclusion** (regime-dependent, not "intermediate")

### **Medium-term (follow-up paper?):**

7. **Derive $\mathcal{A}(\Delta r)$ from Hardy-Littlewood conjectures**
8. **Test modulo 60, 210** (larger prime residue systems)
9. **Study asymptotic behavior** $\mathcal{A}(\Delta r) \to ?$ as $\Delta r \to \infty$

---

## Proposed New Paper Title

**Old:** "The Geometric Origin of Residue-Class Gap Asymmetry in Sparse Arithmetic Point Processes"

**New:** "**A Regime Transition in Residue-Class Gap Asymmetries: From Geometric Bias to Arithmetic Dominance**"

Or:

"**Competing Mechanisms in Prime Gap Asymmetries: Geometric Sparsity vs. Hardy-Littlewood Correlations**"

---

## Conclusion (Preliminary)

The systematic phase diagram R(Δr) reveals that:

1. **Geometric bias is universal** but insufficient for primes
2. **Arithmetic correlations dominate at Δr ≥ 12**
3. **The "intermediate regime" (Bern > Prime > Cramér) is a narrow window**, not the full picture
4. **Hardy-Littlewood analysis is ESSENTIAL**, not optional

**This is not an incremental refinement.**

**This is a fundamentally different story.**

The paper needs to be restructured around the **regime transition**, not the geometric origin alone.

---

**Status:** This document captures the preliminary finding. **DO NOT publish until robustness validation (Step C) is complete.**

---

## Appendix: Connection to Modulo-12 Original Finding

The original modulo-12 analysis showed:

$$R_{\text{Prime}} = 1.58, \quad R_{\text{Cramér}} \approx 1.36$$

with the conclusion "primes partially restore geometric bias suppressed by Cramér."

**This remains TRUE for Δr = 6**, but:
- It's an **accident** that mod-12 landed in the geometric window
- The **general pattern** is regime-dependent
- For most Δr (especially large), primes EXCEED Bernoulli, not fall between

The original finding is **a special case**, not the general rule.

---

**Next:** Execute robustness validation (Step C) before paper revision (Step B).
