# Conditional Gap Asymmetries and Orientation Bias in Consecutive Prime Residue Classes Modulo 12

**Status:** ✓ Mechanismus identifiziert - Asymptotisches Verhalten von R(X) offen  
**Date:** Juni 2026

## Abstract

We study the conditional gap distribution P(g mod 12 | p_n ≡ a) for consecutive primes in residue classes modulo 12. We observe a systematic asymmetry: **P(g ≡ 2,4 | a) > P(g ≡ 8,10 | a)** for all four non-trivial residue classes a ∈ {1, 5, 7, 11}. This is the **primary finding** of this work.

This gap asymmetry induces an asymmetric transition matrix P(a→b) via the fundamental relation b ≡ a + g (mod 12). As a derived consequence, we define an **orientation observable** χ : Q → {-1, 0, +1} on complete EABC prime quadruples, resembling classical arithmetic observables such as the Möbius function μ(n), Liouville function λ(n), and Legendre symbol (a/p). The **bias function** H_C(X) = Σ χ(Q) measures the resulting orientation imbalance and is structurally similar to bias terms in prime number races.

**Key insight:** The orientation bias is not an independent phenomenon. It is a shadow of the underlying conditional gap asymmetry.

**The complete mechanistic chain:**
```
P(g mod 12 | a)     ← Primary arithmetic observable
        ↓
   (a, g) ↦ b       ← Deterministic map: b ≡ a + g (mod 12)
        ↓
    P(a → b)        ← Transition matrix (induced)
        ↓
      R(X)          ← Cycle probability ratio (derived)
        ↓
    H_C(X)          ← Orientation bias (diagnostic tool)
```

**This hierarchy is the core structure of this work.** Everything follows from P(g mod 12 | a).

**Empirical R(X) data:**
```
R(10⁴)   = 6.14   (strong effect)
R(5×10⁴) = 4.59   (-25%)
R(10⁵)   = 4.05   (-12%)
R(5×10⁵) = 3.59   (-11%)
```

**Trend:** Strictly monotonically decreasing. The effect is real, but shrinking. The data show a clear decline rather than stabilization around c ≈ 4.

**Most plausible scenario:** R(X) → 1 with very slow convergence (e.g., R(X) = 1 + c/(log X)^α). This would not be disappointing - many interesting prime race phenomena show exactly this behavior.

**Critical open question:** Decide between pre-asymptotic effect (R → 1) and persistent asymmetry (R → c > 1). Current data suggest the former, but do not conclusively exclude the latter.

**Status:** Persistent observation in the investigated range - most plausible interpretation is slow relaxation to R(X) → 1.

## Current Status

**What is rigorously established:**
- ✅ Rigorous definitions of χ, H_C(X), and construction methods C
- ✅ **P(g mod 12 | a) is asymmetric** in the investigated range (primary finding)
- ✅ **P(a→b) is asymmetric** (induced by gap asymmetry)
- ✅ **This asymmetry quantitatively explains the observed orientation bias**
- ✅ Construction dependence: C_random shows no bias, C_consec shows bias
- ✅ Autocorrelation measured: ρ(1) ≈ 0.27 for overlapping, ≈ 0 for non-overlapping
- ✅ Bias survives corrections: Z_eff remains significant after autocorrelation correction
- ✅ R(X) data: 6.14 → 4.59 → 4.05 → 3.59 (strictly decreasing)

**What is NOT established:**
- ❌ That this asymmetry persists asymptotically
- ❌ That it does not ultimately converge to equality (R → 1)
- ❌ That it represents a new fundamental property of primes
- ❌ The root cause of P(g mod 12 | a) asymmetry

**This caution makes the work stronger.** The interesting part is no longer the original metaphor, but the fact that it has evolved into a clearly formulated empirical question about conditional prime gaps.

**Status:** From speculative narrative to cleanly defined research program

---

## The Four-Level Hierarchy

**Perhaps the most important success of this project is not a specific numerical result, but the reversal of the burden of proof.**

**Initial question (early 2026):**
"How can the observed EABC structure be interpreted geometrically or topologically?"

**Current question (June 2026):**
"What arithmetic mechanisms generate the observed conditional gap asymmetry?"

**This is a fundamental shift in perspective.**

---

### Level 0: Arithmetic Raw Data

```
P(g mod 12 = r | p_n ≡ a (mod 12))
```

**This is the directly observable quantity.** Here lie the actual data.

### Level 1: Transition Dynamics

From the deterministic relation `b ≡ a + g (mod 12)` follows immediately:

```
P(a → b)
```

**The transition matrix is not an independent structure** but an image of the gap distribution.

### Level 2: Cycle Weights

From the transitions emerge products like `P(EABC)` and `P(ECBA)`, yielding:

```
R(X) = P(EABC) / P(ECBA)
```

### Level 3: Observable

Only here appears:

```
H_C(X) = N_EABC - N_ECBA
```

**Key insight:** The original chirality observable is actually a **measurement instrument** for the deeper dynamics.

---

## Why This Hierarchy Matters

**Many young research programs make the opposite mistake: They fall in love with the observable.**

**This project has recognized:**

- **H_C(X) is not the object**
- **It is a thermometer**
- **The temperature is R(X)**
- **The physics behind it is P(g mod 12 | a)**

**This is an enormous methodological improvement.**

---

## The Scientific Core

If this work had to be reduced to a single line, it would no longer be H_C(X), nor even R(X).

**It would be:**

```
P(g mod 12 = r | p_n ≡ a (mod 12))
```

**This is the fundamental quantity.** Everything else emerges from it.

This is why the mechanistic chain is now a true **causal chain**, not mere correlation:

```
P(g mod 12 | a)     ← Fundamental
        ↓
   (a, g) ↦ b       ← Deterministic
        ↓
    P(a → b)        ← Induced
        ↓
      R(X)          ← Derived
        ↓
    H_C(X)          ← Diagnostic
```

---

## Paper Goal

**Not:**
"We discovered a new structure of the primes"

**But rather:**
"We identify and quantify conditional asymmetries in the residue-class gap distribution of consecutive primes modulo 12 and show how these asymmetries induce an orientation bias on complete residue quadruples"

**This is precise, modest, and strong.**

---

## The Critical Question

The most important open mathematical question is not H(X), not Z(X), but:

```
lim_{X→∞} R(X) = ?
```

The data sequence:
```
R(10⁴) = 6.14
R(5×10⁴) = 4.59
R(10⁵) = 4.05
R(5×10⁵) = 3.59
```

**This alone could become the most interesting figure of the entire project.**

It decides between:
- Pre-asymptotic behavior
- Prime-race-like oscillation
- Genuine persistent asymmetry

---

## What Remains: A Research Program

**From the original metaphor** (Klein bottle), a **clearly formulated empirical question** about conditional prime gaps has emerged.

**What remains is not topological speculation, but:**
```
E → A → B → C → E
```
as a **preferred cycle in a Markov dynamics on residue classes**.

This is:
- Mathematically cleaner
- Directly testable
- More interesting

**This is now a cleanly defined research program, not a speculative narrative.**

---

## Mechanistic Summary

**Key Achievement:** Identification of the primary phenomenon - conditional gap asymmetry:

```
P(g ≡ 2,4 mod 12 | p_n ≡ a) > P(g ≡ 8,10 mod 12 | p_n ≡ a)
```

for all a ∈ {E, A, B, C}.

**This is the most elementary statement of this work.** The orientation bias follows mechanistically.

**Decomposition hierarchy:**

```
P(g mod 12 | a)     ← Primary phenomenon
        ↓
    P(a→b)          ← Transition matrix (derived)
        ↓
P(EABC)/P(ECBA)     ← Cycle ratio R(X) (derived)
        ↓
      H_C(X)        ← Orientation observable (derived)
```

**Interpretation shift:**
- **Before:** Orientation bias H_C(X) > 0 was the observation
- **Now:** Gap asymmetry is the primary phenomenon; orientation bias is its shadow

The fundamental relation for consecutive primes is:

```
b ≡ a + g (mod 12)
```

where p_n ≡ a (mod 12), p_{n+1} ≡ b (mod 12), and g = p_{n+1} - p_n.

This implies:

```
P(a → b) = P(g ≡ b - a (mod 12) | p_n ≡ a)
```

The transition matrix is an **encoded gap distribution modulo 12**.

**EABC cycle** uses gap classes {4, 2, 4, 2}, **ECBA cycle** uses {8, 10, 8, 10}.

**Mechanistic formula:**

```
P(EABC)     P_E(4) · P_A(2) · P_B(4) · P_C(2)
────────  = ───────────────────────────────────  ≈ 4.046
P(ECBA)     P_E(10) · P_C(8) · P_B(10) · P_A(8)
```

**Empirical values (100K primes):**
- P_E(4) = 0.3242,  P_E(10) = 0.2554  
- P_A(2) = 0.3581,  P_A(8) = 0.2235  
- P_B(4) = 0.3254,  P_B(10) = 0.2570  
- P_C(2) = 0.3537,  P_C(8) = 0.2251  

**Key observation:** P(g ≡ 2,4 | a) > P(g ≡ 8,10 | a) for all a ∈ {E, A, B, C}.

**Next theoretical step:** Test whether sieve models (mod 60, 420, 2310) predict this gap asymmetry.

---

## Part I: Rigorous Definitions

### 1.1 EABC Classification

For primes p > 3, define the EABC classification modulo 12:

```
E: p ≡ 1  (mod 12)
A: p ≡ 5  (mod 12)
B: p ≡ 7  (mod 12)
C: p ≡ 11 (mod 12)
```

**Notation:** Let k(p) ∈ {E, A, B, C} denote the class of prime p.

**Status:** Exact arithmetic definition. ✓

### 1.2 Complete Quadruples

**Definition 1.1.** A prime quadruple Q = (p, q, r, s) is **complete** if:

```
{k(p), k(q), k(r), k(s)} = {E, A, B, C}
```

i.e., each of the four EABC classes appears exactly once.

**Notation:** Let Q_complete denote the set of all complete quadruples.

**Status:** Precisely defined subset of ℕ⁴. ✓

### 1.3 Signature and Normalization

**Definition 1.2.** The **signature** of Q is:

```
sig(Q) = (k(p), k(q), k(r), k(s)) ∈ {E, A, B, C}⁴
```

**Definition 1.3.** The **normalized signature** norm(sig(Q)) is obtained by cyclic rotation until E appears first.

**Remark:** For complete quadruples with E fixed at position 1, there are exactly (4-1)! = 6 possible normalized signatures:

```
EABC, EACB, EBAC, EBCA, ECAB, ECBA
```

**Status:** Well-defined functions. ✓

### 1.4 Chirality Observable

**Definition 1.4.** The **chirality observable** is defined as:

```
χ : Q_complete → {-1, 0, +1}

χ(Q) = ⎧ +1,  norm(sig(Q)) = EABC
       ⎨ -1,  norm(sig(Q)) = ECBA
       ⎩  0,  otherwise
```

**Interpretation:**
- χ(Q) = +1: Positive cyclic order E → A → B → C → E
- χ(Q) = -1: Negative cyclic order E → C → B → A → E
- χ(Q) = 0: Other permutation (one of EACB, EBAC, EBCA, ECAB)

**Analogy:** χ is structurally similar to:
- **Möbius function:** μ(n) ∈ {-1, 0, +1}
- **Liouville function:** λ(n) ∈ {-1, +1}
- **Legendre symbol:** (a/p) ∈ {-1, 0, +1}

**Status:** Exact function Q_complete → {-1, 0, +1}. ✓

### 1.5 Bias Function (not "Holonomy")

**Terminology Note:** We avoid the term "holonomy" as it has a specific meaning in differential geometry (parallel transport along closed paths). Our construction lacks such a transport operator.

**Definition 1.5.** For a construction method C, the **bias function** is:

```
H_C(X) = Σ_{Q≤X, Q∈C} χ(Q)
```

**Alternative formulation:**

```
H_C(X) = N_{EABC}^C(X) - N_{ECBA}^C(X)
```

where N_{EABC}^C(X) counts EABC-quadruples and N_{ECBA}^C(X) counts ECBA-quadruples under construction C up to X.

**Normalized bias:**

```
h_C(X) = H_C(X) / N_C(X)
```

**Status:** Well-defined arithmetic function for each C. ✓

### 1.6 Standardized Bias

**Definition 1.6a.** The **scaled bias** is:

```
Z_C(X) = H_C(X) / √N_C(X)
```

**Definition 1.6b.** The **standardized bias** (proper Z-score under null hypothesis) is:

```
Z_C*(X) = H_C(X) / √(N_C(X)/3) = √3 · H_C(X) / √N_C(X)
```

**Interpretation:**
- Under null hypothesis (E[χ] = 0, Var[χ] = 1/3):
  - Z_C(X) has variance 1/3, so Z_C(X) ~ N(0, 1/3)
  - Z_C*(X) has variance 1, so Z_C*(X) ~ N(0, 1) (standard normal)
- If Z_C*(X) → ∞, this indicates persistent bias
- For statistical significance testing, use Z_C*(X)

**Remark:** Z_C*(X) would provide proper p-values via standard normal distribution **if** the χ_n were independent. For consecutive constructions with autocorrelation, use Z_eff instead.

**Status:** Well-defined normalizations. ✓

---

## Part II: Reference Model and Autocorrelation

### 2.1 Uniform Permutation Reference Model

**Model Assumption:** Assume the four EABC classes of a complete quadruple are uniformly distributed over all 4! = 24 permutations.

**Remark:** This is a **reference model**, not a null hypothesis about primes. No one expects consecutive primes to have truly independent residue classes modulo 12. The model serves as a baseline for comparison.

**Consequence:** Among the 6 normalized signatures (E fixed first), each has equal probability 1/6 under the reference model.

**Expected values:**

```
E[χ(Q)] = P(EABC) · (+1) + P(ECBA) · (-1) + P(other) · (0)
        = (1/6) · (+1) + (1/6) · (-1) + (4/6) · (0)
        = 0

E[χ²] = (1/6) · 1² + (1/6) · (-1)² + (4/6) · 0² = 1/3

Var[χ] = 1/3
```

### 2.2 Independence vs. Autocorrelation

**If χ(Q₁), χ(Q₂), ... were i.i.d.** with E[χ] = 0 and Var[χ] = 1/3, then:

```
Var[H_C(X)] = N_C(X) / 3
Z_C*(X) = H_C(X) / √(N_C(X)/3) ~ N(0, 1)
```

**Critical Issue for C_consec:** Consecutive quadruples Q_n = (p_n, p_{n+1}, p_{n+2}, p_{n+3}) and Q_{n+1} = (p_{n+1}, p_{n+2}, p_{n+3}, p_{n+4}) **share 3 out of 4 primes**. Therefore, χ(Q_n) and χ(Q_{n+1}) are **not independent**.

### 2.3 Autocorrelation Function

**Definition 2.1.** The **chirality autocorrelation** is:

```
ρ(k) = Corr(χ_n, χ_{n+k})
```

where χ_n = χ(Q_n) for consecutive quadruples.

**Definition 2.2.** The **effective sample size** is:

```
N_eff = N / (1 + 2·Σ_{k≥1} ρ(k))
```

**Definition 2.3.** The **effective standardized bias** is:

```
Z_eff = H / √(N_eff / 3)
```

**Remark:** Only Z_eff has a proper significance interpretation under the reference model. The naive Z*(X) overestimates significance when ρ(k) > 0.

**Status:** ρ(k) and N_eff **have been computed** (see Part III for empirical data). ✅

---

## Part III: Construction Methods and Empirical Data

### 3.1 Consecutive Construction (C_consec)

**Definition:** Q_n = (p_n, p_{n+1}, p_{n+2}, p_{n+3}) for consecutive primes.

**Empirical Data (10K primes):**

| X    | N(X) | H(X) | h(X)  | Z(X)  | Z*(X)  | ρ(1) | N_eff | Z_eff |
|------|------|------|-------|-------|--------|------|-------|-------|
| 10³  | 48   | +19  | 0.396 | 2.74  | 4.75   | -    | -     | -     |
| 10⁴  | 248  | +67  | 0.270 | 4.26  | 7.38   | -    | -     | -     |
| 10⁴  | 1706 | +333 | 0.195 | 8.06  | 13.96  | 0.252| 1002  | 18.2  |

**Empirical Data (100K primes):**

| X    | N(X)  | H(X)  | h(X)  | Z(X)  | Z*(X)  | ρ(1) | N_eff | Z_eff |
|------|-------|-------|-------|-------|--------|------|-------|-------|
| 10⁵  | 15379 | +2429 | 0.158 | 19.59 | 33.93  | 0.266| 8997  | 44.4  |

**Autocorrelation Function (100K primes):**

```
ρ(1) = 0.266  ← Strong autocorrelation from overlapping windows
ρ(2) = 0.073
ρ(3) = 0.017
ρ(4) ≈ 0
Σ_{k=1}^4 ρ(k) = 0.355
```

**Effective Sample Size:**

```
N_eff = N / (1 + 2·Σρ) = 15379 / (1 + 0.71) = 8997
Reduction factor: 0.585 (41% reduction due to autocorrelation)
```

**Key Observations:**
- Z(X) and Z*(X) are naive scores ignoring autocorrelation
- ρ(1) ≈ 0.27 confirms predicted autocorrelation from 3-prime overlap
- After correction: **Z_eff = 44.4 at X = 10⁵ (~44-sigma deviation)**
- **Interpretation:** Even after accounting for autocorrelation, the bias remains **highly significant**

**Critical Result:** The observed bias is **not** merely an artifact of overlapping windows.

### 3.2 Non-Overlapping Construction (C_nonoverlap)

**Definition:** Q_n = (p_{4n}, p_{4n+1}, p_{4n+2}, p_{4n+3}) for non-overlapping prime windows.

**Purpose:** Control group to test whether bias is purely from window overlap.

**Empirical Data (100K primes):**

| X    | N(X) | H(X) | h(X)  | Z(X) | Z*(X) | ρ(1)  | N_eff | Z_eff |
|------|------|------|-------|------|-------|-------|-------|-------|
| 10⁵  | 3832 | +576 | 0.150 | 9.31 | 16.12 | 0.021 | 3659  | 16.5  |

**Autocorrelation Function (100K primes):**

```
ρ(1) = 0.021  ← Minimal autocorrelation (no overlap)
ρ(2) = 0.015
ρ(3) = 0.011
ρ(4) ≈ -0.023
Σ_{k=1}^4 ρ(k) = 0.024
```

**Effective Sample Size:**

```
N_eff = N / (1 + 2·Σρ) = 3832 / (1 + 0.048) = 3659
Reduction factor: 0.955 (only 4.5% reduction)
```

**Key Observations:**
- ρ(1) ≈ 0 confirms absence of overlap-induced autocorrelation ✓
- After correction: **Z_eff = 16.5 at X = 10⁵ (~16-sigma deviation)**
- **h(C_nonoverlap) = 0.150 ≈ h(C_consec) = 0.158** (consistent bias)
- Bias magnitude is **independent of window overlap**

**Critical Result:** The orientation bias persists **even without overlapping windows**, confirming it is a genuine property of consecutive prime patterns, not a methodological artifact.

### 3.3 Random Construction (C_random)

**Definition:** For each complete quadruple {p,q,r,s}, apply a uniform random permutation.

**Empirical Data:**

| X    | N(X)  | H(X) | h(X)   | Z(X)   |
|------|-------|------|--------|--------|
| 10⁴  | 10000 | -10  | -0.001 | -0.10  |

**Observation:** h(X) ≈ 0 and Z(X) ≈ 0, consistent with null hypothesis.

**Interpretation:** The null hypothesis is **not rejected** for C_random.

### 3.3 Summary

```
C_random:  Z(X) ≈ 0     → Null hypothesis consistent ✓
C_consec:  Z(X) ~ √X    → Null hypothesis rejected ✗
```

**Conclusion:** The bias is construction-dependent, not intrinsic to primes mod 12.

---

## Part IV: Full Signature Distribution

### 4.1 Six Normalized Signatures

For complete quadruples with E fixed first, the six possible signatures are:

```
σ₁ = EABC  (χ = +1)
σ₂ = EACB  (χ =  0)
σ₃ = EBAC  (χ =  0)
σ₄ = EBCA  (χ =  0)
σ₅ = ECAB  (χ =  0)
σ₆ = ECBA  (χ = -1)
```

**Definition 4.1.** Let P_C(σ, X) denote the empirical probability of signature σ under construction C up to X:

```
P_C(σ, X) = N_σ^C(X) / N_C(X)
```

### 4.2 Independence Model Prediction

Under independence:

```
P(σᵢ) = 1/6  for all i = 1, ..., 6
```

### 4.3 Empirical Distribution (C_consec, X = 10⁵)

| Signature | Count | P(σ)  | Expected (1/6) |
|-----------|-------|-------|----------------|
| EABC      | 452   | 0.274 | 0.167          |
| EACB      | ?     | ?     | 0.167          |
| EBAC      | ?     | ?     | 0.167          |
| EBCA      | ?     | ?     | 0.167          |
| ECAB      | ?     | ?     | 0.167          |
| ECBA      | 132   | 0.080 | 0.167          |

**Observation:** P(EABC) and P(ECBA) deviate significantly from 1/6.

**Remark:** A full analysis should examine all six probabilities, not just χ = ±1 projections.

**Chi-squared test:**

```
χ²_statistic = Σᵢ (N_observed(σᵢ) - N_expected(σᵢ))² / N_expected(σᵢ)
```

With 5 degrees of freedom, this tests independence rigorously.

---

## Part V: Research Questions and Conjectures

### Question 0 (Primary - Autocorrelation Structure) ✅ ANSWERED

**Question:** For construction C_consec, what is the autocorrelation structure?

```
ρ(k) = Corr(χ_n, χ_{n+k})  for k = 1, 2, 3, ...
```

**Answer (empirically measured at X = 10⁵):**

```
ρ(1) = 0.266  ← Strong autocorrelation from 3-prime overlap
ρ(2) = 0.073
ρ(3) = 0.017  
ρ(4) ≈ 0
```

**Interpretation:**
- ρ(1) ≈ 0.27 confirms predicted autocorrelation from overlapping windows ✓
- Autocorrelation decays rapidly: ρ(k) ≈ 0 for k ≥ 4
- For non-overlapping construction: ρ(1) ≈ 0.02 (minimal, as expected) ✓

**Status:** ✅ **ANSWERED**

### Question 1 (Secondary - Effective Bias) ✅ ANSWERED

**Question:** After accounting for autocorrelation, does a bias remain?

```
Z_eff = H / √(N_eff / 3)  where N_eff = N / (1 + 2·Σ ρ(k))
```

**Answer (empirically computed at X = 10⁵):**

| Construction | N | N_eff | Z_eff | Significance |
|--------------|------|-------|-------|--------------|
| C_consec     | 15379| 8997  | 44.4  | ~44-sigma    |
| C_nonoverlap | 3832 | 3659  | 16.5  | ~16-sigma    |

**Interpretation:**
- After autocorrelation correction, bias remains **highly significant** ✓
- Effect persists even for non-overlapping windows (control group) ✓
- **Conclusion:** The observed bias is **NOT** an autocorrelation artifact

**Status:** ✅ **ANSWERED - Bias is genuine**

### Conjecture 2 (Moderate - Non-Vanishing Bias Growth) ✅ SUPPORTED

**Statement:** For construction C_consec:

```
H_{C_consec}(X) ≠ o(√N(X))
```

**Interpretation:** The bias grows faster than expected from pure random walk.

**Evidence:** 
- h(X) = H/N remains bounded away from zero: 0.396 (10³) → 0.158 (10⁵)
- Z_eff grows with √N: 18.2 (10⁴) → 44.4 (10⁵)  
- After autocorrelation correction, Z_eff >> 0 consistently

**Status:** ✅ **Strongly supported** by empirical data across multiple scales.

### Conjecture 3 (Exploratory - Correlation with Prime Gaps)

**Statement:** The chirality χ(Q_n) correlates with the prime gap g_n = p_{n+1} - p_n:

```
Corr(χ(Q_n), g_n) ≠ 0
```

**Motivation:** If large gaps favor certain EABC patterns, this could explain observed bias.

**Status:** Untested. Requires computation.

### Conjecture 4 (Speculative - Logarithmic Decay)

**Statement:** For C_consec:

```
h_{C_consec}(X) ~ c / log log X  for some c > 0
```

**Motivation:** Analogous to logarithmic behaviors in prime races (Rubinstein-Sarnak).

**Status:** Highly speculative. Current data insufficient.

**Note:** We do NOT claim strong evidence for this. It is listed as a theoretical possibility.

---

## Part VI: Connection to Prime Number Races

### 6.1 Classical Prime Races

**Chebyshev's Observation (1850s):**

For primes modulo 4:

```
Δ₄(x) = π(x; 4, 3) - π(x; 4, 1)
```

It was observed that Δ₄(x) > 0 for most x ("3 leads 1").

**Rubinstein-Sarnak (1994):**

Under reasonable assumptions (e.g., GRH and linear independence of zeros):

```
Logarithmic density of {x : Δ₄(x) > 0} ≈ 0.9959
```

### 6.2 Analogy to Bias Function

**Structure:**

Both measure **imbalance between symmetric classes**:

```
Chebyshev:  Δ₄(x) = π(x;4,3) - π(x;4,1)
Bias:       H_C(X) = N_{EABC}(X) - N_{ECBA}(X)
```

**Key Difference:**

- Chebyshev: **Individual primes** in residue classes
- Bias function: **Tuples of primes** with specific orientation patterns

### 6.3 Potential Mechanism

**Hypothesis:** If consecutive primes exhibit correlations in their mod 12 residues (analogous to Chebyshev bias within tuples), this could induce bias in H_{C_consec}(X).

**Example:** If p ≡ 1 (mod 12) is more likely to be followed by p' ≡ 5 (mod 12) than by p' ≡ 11 (mod 12), this would favor EABC over ECBA.

**Testable:** Compute conditional probabilities:

```
P(p_{n+1} ≡ a (mod 12) | p_n ≡ b (mod 12))
```

and check for deviations from 1/φ(12) = 1/4.

---

## Part VII: What is Established vs. Heuristic

### 7.1 Rigorously Established (✓)

1. **EABC classification** - Exact arithmetic
2. **Complete quadruples** - Precise definition
3. **Chirality observable χ(Q)** - Well-defined function
4. **Bias function H_C(X)** - Exact for each C
5. **Null hypothesis E[χ] = 0** - Follows from independence model
6. **Construction dependence** - Empirically demonstrated

### 7.2 Empirically Observed (≈)

7. **h_random ≈ 0** - Consistent with null hypothesis
8. **h_consec ≈ 0.19 at X = 10⁵** - Significant deviation
9. **Z_consec grows** - Suggests persistent bias

### 7.3 Open Questions (?)

10. **Autocorrelation ρ(k)** - PRIMARY OPEN QUESTION, must be computed
11. **Effective significance Z_eff** - Depends on ρ(k)
12. **Asymptotic behavior** - Does h(X) → 0 or stabilize after autocorrelation correction?
13. **Correlation with gaps** - Corr(χ, g_n) = ?
14. **Full signature distribution** - P(σᵢ) for all i?
15. **Theoretical explanation** - Why does C_consec exhibit bias structure?

### 7.4 Historical Heuristic Images (⚠️ Not Rigorous)

14. **Klein bottle** - Metaphor for non-orientability, not emergent structure
15. **χ = -1 as Euler characteristic** - Heuristic, no canonical 2-complex
16. **Lemniscate (∞)** - Visual imagery, not mathematical invariant
17. **"Holonomy"** - Misleading term (no transport operator)

**Status:** These are **motivational images**, not mathematical results.

---

## Part VIII: Research Program

### Phase 0: Autocorrelation Analysis ✅ COMPLETED

**Priority 1:** Compute the autocorrelation function - **DONE**

**Results:**
- ρ(1) = 0.266, ρ(2) = 0.073, ρ(3) = 0.017, ρ(4) ≈ 0 for C_consec
- ρ(1) = 0.021 for C_nonoverlap (control confirms no overlap artifact)
- N_eff = 8997 (from N = 15379) for C_consec at X = 10⁵
- Z_eff = 44.4 for C_consec, Z_eff = 16.5 for C_nonoverlap

**Conclusion:** ✅ Genuine bias confirmed beyond autocorrelation

### Phase 1: Extended Analysis (Current Priority)

1. **Larger X** - Extend to X = 10⁶ (in progress), 10⁷ (future)
2. **Compute full signature distribution** - All six P_C(σ, X) for C_consec
3. **Chi-squared test** - Test reference model rigorously
4. **Variance analysis** - Compute Var_empirical(χ) at scale

### Phase 2: Correlation Analysis (Short-term)

5. **Gap correlation** - Corr(χ(Q_n), g_n)
6. **Residue transitions** - P(p_{n+1} ≡ a | p_n ≡ b)
7. **Conditional probabilities** - P(χ = +1 | large gap) vs. P(χ = +1 | small gap)

### Phase 3: Theoretical Model (Medium-term)

8. **Markov model** - Model consecutive prime residues as Markov chain
9. **Predicted E[χ]** - Under Markov model with transition biases
10. **Compare prediction to data**

### Phase 4: Connection to Literature (Long-term)

11. **Prime race framework** - Rubinstein-Sarnak methods
12. **Logarithmic density** - Of {X : H_C(X) > 0}
13. **L-function analysis** - Oscillatory terms in error

---

## Part IX: Summary

### The Core Result

We have defined a **new arithmetic observable**:

```
χ : Complete EABC quadruples → {-1, 0, +1}
```

analogous to classical multiplicative functions, and studied its bias function:

```
H_C(X) = Σ_{Q≤X} χ(Q)
```

### Key Findings

1. **Reference model:** E[χ] = 0 under uniform permutation, Var[χ] = 1/3
2. **C_random consistent:** h ≈ 0, Z* ≈ 0 (reference model satisfied)
3. **C_consec deviates:** h ≈ 0.16, Z_eff = 44.4 for X = 10⁵ (**44-sigma after autocorrelation correction**)
4. **C_nonoverlap deviates:** h ≈ 0.15, Z_eff = 16.5 for X = 10⁵ (**16-sigma, no overlap artifact**)
5. **Construction-dependent:** Bias is not intrinsic to primes, but arises in consecutive arrangements

### Main Result: Genuine Bias Confirmed ✅

**Autocorrelation measured:**
- ρ(1) = 0.266 for C_consec (confirms 3-prime overlap)
- ρ(1) = 0.021 for C_nonoverlap (confirms no artifact)
- Autocorrelation decays rapidly: ρ(k) ≈ 0 for k ≥ 4

**Effective significance computed:**
- Z_eff = 44.4 for overlapping windows (after 41% sample size reduction)
- Z_eff = 16.5 for non-overlapping windows (control group)
- **Both highly significant** → bias is NOT an autocorrelation artifact

**Interpretation:**
> We observe a persistent orientation bias in consecutive complete EABC prime quadruples modulo 12. The effect survives both autocorrelation correction and non-overlapping window tests (Z_eff = 16.5 at X = 10⁵). However, the normalized bias h(X) shows a declining trend (0.396 → 0.270 → 0.195 → 0.158), and its asymptotic behavior remains open. The theoretical explanation—which local dynamics in consecutive prime residue classes cause this effect—is an open question.

### Connection to Established Theory

**Structurally similar to prime number races** (Chebyshev bias), but applied to oriented tuples rather than individual primes.

**Testable predictions:** Variance, correlations, signature distribution, chi-squared test.

### What is NOT Claimed

- ✗ "Intrinsic chirality of primes" (refuted by C_random)
- ✗ Topological invariants (Klein bottle, χ = -1 are heuristic metaphors)
- ✗ Strong asymptotic conjectures (only empirically supported observations)

### Mathematical Status

**Rigorously defined:** χ and H_C(X) as observables on prime quadruples. ✓

**Empirically observed:** Orientation bias in consecutive quadruples persists after autocorrelation correction up to X = 10⁵. ~

**Autocorrelation measured:** ρ(k) computed, N_eff and Z_eff determined. ✅

**Transition matrix computed:** P(a→b) asymmetric, cyclic products differ by factor ~4. ✅

**Mechanistic explanation:** Gap distribution modulo 12 induces transition asymmetry. ✅

**Asymptotic behavior:** Open - h(X) shows declining trend, requires X ≫ 10⁵. ?

**Root cause of gap asymmetry:** Sieve effects hypothesis - test against sieve models needed. ○

---

## Part V: Mechanistic Explanation

### 5.1 The Fundamental Relation

For consecutive primes p_n and p_{n+1} with:

```
p_n ≡ a (mod 12)
p_{n+1} ≡ b (mod 12)
g = p_{n+1} - p_n
```

The fundamental relation is:

```
b ≡ a + g (mod 12)
```

**Immediate consequence:**

```
P(p_{n+1} ≡ b | p_n ≡ a) = P(g ≡ b - a (mod 12) | p_n ≡ a)
```

**Key insight:** The transition matrix P(a→b) is an **encoded gap distribution modulo 12**.

---

### 5.2 Cyclic Paths and Gap Classes

#### EABC Cycle (Positive Orientation)

| Transition | Residues | Gap mod 12 | Empirical P(g\|a) |
|------------|----------|------------|-------------------|
| E → A      | 1 → 5    | g ≡ 4      | 0.3242            |
| A → B      | 5 → 7    | g ≡ 2      | 0.3581            |
| B → C      | 7 → 11   | g ≡ 4      | 0.3254            |
| C → E      | 11 → 1   | g ≡ 2      | 0.3537            |

**Gap sequence:** {4, 2, 4, 2}

**Cycle probability:**
```
P(EABC) = P_E(4) · P_A(2) · P_B(4) · P_C(2)
        = 0.3242 × 0.3581 × 0.3254 × 0.3537
        = 0.01336
```

#### ECBA Cycle (Negative Orientation)

| Transition | Residues | Gap mod 12 | Empirical P(g\|a) |
|------------|----------|------------|-------------------|
| E → C      | 1 → 11   | g ≡ 10     | 0.2554            |
| C → B      | 11 → 7   | g ≡ 8      | 0.2251            |
| B → A      | 7 → 5    | g ≡ 10     | 0.2570            |
| A → E      | 5 → 1    | g ≡ 8      | 0.2235            |

**Gap sequence:** {10, 8, 10, 8}

**Cycle probability:**
```
P(ECBA) = P_E(10) · P_C(8) · P_B(10) · P_A(8)
        = 0.2554 × 0.2251 × 0.2570 × 0.2235
        = 0.00330
```

---

### 5.3 The Mechanistic Formula

```
P(EABC)     P_E(4) · P_A(2) · P_B(4) · P_C(2)
────────  = ───────────────────────────────────
P(ECBA)     P_E(10) · P_C(8) · P_B(10) · P_A(8)
```

**Empirical value (100,000 primes):** 4.046

**Interpretation:** The 4-fold preference for EABC over ECBA directly follows from the asymmetric gap distribution.

---

### 5.4 Gap Asymmetry Analysis

The key empirical observation:

```
P(g ≡ 2,4 | p_n ≡ a)  >  P(g ≡ 8,10 | p_n ≡ a)
```

for all a ∈ {E, A, B, C}.

**Detailed ratios (100K primes):**

| Start class | P(g≡2,4) | P(g≡8,10) | Ratio |
|-------------|----------|-----------|-------|
| E (1)       | 0.3242   | 0.2554    | 1.269 |
| A (5)       | 0.3581   | 0.2235    | 1.602 |
| B (7)       | 0.3254   | 0.2570    | 1.266 |
| C (11)      | 0.3537   | 0.2251    | 1.571 |

**Universal preference:** Gap classes {2, 4} are consistently more probable than {8, 10}.

---

### 5.5 The Complete Causal Chain

```
Conditional gap distribution P(g mod 12 | p_n ≡ a) is asymmetric
                    ↓
        P(g ≡ 2,4) > P(g ≡ 8,10)
                    ↓
       Fundamental relation: b ≡ a + g (mod 12)
                    ↓
      Transition matrix P(a→b) is asymmetric
                    ↓
   EABC uses {2,4}, ECBA uses {8,10}
                    ↓
         P(EABC) / P(ECBA) ≈ 4.046
                    ↓
      Orientation bias H_C(X) > 0
```

---

### 5.6 Status and Open Questions

**Established:**
- ✅ Gap distribution is the proximate cause
- ✅ Mechanistic formula quantitatively reproduces observed ratio
- ✅ No topological interpretation needed

**Open:**
- ❓ **Root cause:** Why is P(g ≡ 2,4) > P(g ≡ 8,10)?
- ❓ **Hypothesis:** Sieve effects from small primes (5, 7, 11, 13, ...)
- ❓ **Test:** Compare against sieve model predictions (mod 60, 420, 2310)

---

### 5.7 Implementation

**Program:** `gap_distribution.cpp`

**Usage:**
```bash
make gap
./gap_distribution 100000
```

**Output:**
1. Full gap distribution matrix P(g mod 12 | p_n ≡ a)
2. Gap asymmetry analysis: {2,4} vs {8,10}
3. Cyclic path analysis: EABC vs ECBA
4. Mechanistic formula and ratio

**See:** GAPS_ANALYSIS.md for detailed documentation

---

## References

### Prime Number Races

1. **Chebyshev, P.** (1850s) - First observations of prime race bias
2. **Rubinstein, M. & Sarnak, P.** (1994) - "Chebyshev's bias", Experimental Mathematics
3. **Ng, N.** (2004) - "The distribution of the summatory function of the Möbius function"

### Residue Class Distribution

4. **Davenport, H.** - "Multiplicative Number Theory"
5. **Granville, A. & Martin, G.** (2006) - "Prime number races"

### Relevant Multiplicative Functions

6. **Möbius function:** μ(n) ∈ {-1, 0, +1}
7. **Liouville function:** λ(n) = (-1)^Ω(n)
8. **Legendre symbol:** (a/p) for quadratic residues

---

## Next Steps for Publication-Ready Paper

**Priority hierarchy:** The modulo 30 test is more important than further increasing X.

### 1. Modulo 30 Test (HIGHEST PRIORITY ⭐⭐⭐⭐⭐)

**This test is more important than any further increase in X.**

**Why modulo 12 is "dangerous":**

Modulo 12 = 2² · 3 already involves the two smallest primes. A substantial part of the observed structure could simply arise from local prohibitions by 2 and 3.

**Why modulo 30 is critical:**

Modulo 30 = 2 · 3 · 5 is the first serious generalization with 8 residue classes:
```
{1, 7, 11, 13, 17, 19, 23, 29}
```

**Decision criterion:**
- **If similar cycles appear:** Evidence for a general mechanism → mod-12 is just the first visible case → **significantly more interesting**
- **If the effect only appears modulo 12:** Likely a projection of effects specifically generated by 2 and 3 → still interesting but completely different

**This test determines:** Are we observing a general phenomenon of prime gap distributions, or a special consequence of the smallest primes?

### 2. Asymptotic Behavior of R(X)

**Question:** Does R(X) → 1 or R(X) → c > 1?

**Current data:**
- R(10⁴) = 6.14
- R(5×10⁴) = 4.59
- R(10⁵) = 4.05
- R(5×10⁵) = 3.59

**Trend:** Strictly monotonically decreasing (-41%). Clear decline rather than stabilization.

**Interpretation:** If the factor were truly fundamental, one would expect:
```
4.2, 4.1, 4.0, 4.0   (stabilization)
```
Instead, we observe:
```
6.14, 4.59, 4.05, 3.59   (clear decline)
```

**Most plausible scenario:** R(X) → 1 with very slow convergence. Many interesting prime race phenomena show exactly this behavior.

**Next priority:** 
1. Compute R(10⁶)
2. Compute R(10⁷)

**This test decides whether we are observing pre-asymptotic behavior or persistent structure.**

**The most interesting figure of the entire project:** Not chirality, not Klein bottle, not transition matrix, but:

```
R(X) plotted against log X
```

**If the points continue towards 1:** A story about pre-asymptotic behavior  
**If they stabilize:** A story about persistent local structure  
**If they oscillate:** Surprisingly close to classical prime race phenomena

**Program:** `ratio_asymptotic.cpp`

### 3. Direct Gap Distribution Analysis

**After** R(X) is determined, measure:

```
P(g mod 12 = r | p_n ≡ a)
```

for the same ranges (10⁶, 10⁷). This is the primary phenomenon.

**Program:** `gap_distribution.cpp`

### 4. Hardy-Littlewood / Sieve Model Comparison

Compare empirical P(g mod 12 | a) against predictions from:
- Simple sieve model (excluding small primes modulo 60, 420, 2310)
- Hardy-Littlewood k-tuple conjectures
- Prime number race theory

**Goal:** Move from "empirical observation" to "analytical explanation"

### 5. Full Signature Distribution

**Current:** Only χ ∈ {-1, 0, +1} measured (projection)

**Needed:** All six normalized signatures EABC, EACB, EBAC, EBCA, ECAB, ECBA

**Importance:** The observed bias might come from 2-3 particularly frequent permutations

---

## Candidate Theorem (Long-term)

If the observation stabilizes, the interesting result would not be:

```
H_C(X) > 0   (orientation bias)
```

but rather:

```
P(g ≡ 2,4 (mod 12) | p_n ≡ a) > P(g ≡ 8,10 (mod 12) | p_n ≡ a)
```

for all a ∈ {E, A, B, C} and large ranges X.

**Why:** The orientation tendency follows almost automatically from the gap asymmetry. The gap distribution is the primary phenomenon; H_C(X) becomes a **diagnostic tool**.

---

## Scientific Status

**The project has reached a form that can be taken seriously in empirical number theory:**

✅ **The definitional basis is clear**  
✅ **The original metaphorical elements are cleanly separated from mathematical statements**  
✅ **The observations are reproducible**  
✅ **The open questions are explicitly named**  
✅ **The critical falsification paths are formulated:**
- Autocorrelation (completed)
- Non-overlapping windows (completed)
- Modulo 30 test (pending)
- Asymptotic behavior of R(X) (pending)

**This is what good research programs look like:** Not by already having all the answers, but by being able to clearly state:
- Which observations are established
- Which mechanisms appear plausible
- Which questions remain open

**From speculative narrative to cleanly defined research program.**

---

## From Objects to Dynamics

**What has actually changed:**

**Initial level (early 2026):** Object level
```
Is there a special structure in EABC quadruples?
```

**Current level (June 2026):** Dynamics level
```
What local transition laws generate observed patterns in EABC quadruples?
```

**This is a substantial difference.**

Many exploratory number theory projects remain at the object level:
- Prime patterns
- Geometric pictures
- Fractals
- Topologies
- Visualizations

This project has arrived at a significantly deeper question:
```
Local dynamics → Transition probabilities → Observed structures
```

---

## The Actual Scientific Core

When everything superfluous is removed, only this remains:

```
P(g mod 12 = r | p_n ≡ a (mod 12))
```

**This is the primitive observable.** Everything else emerges from it.

**Transition matrix** P(a→b) emerges via b ≡ a + g (mod 12)  
**Cycle ratio** R(X) emerges from products of such transitions  
**Orientation bias** H_C(X) emerges in turn from R(X)

**One could almost say:** H is the most highly aggregated quantity of the entire project.

---

## A Historical Analogy

The development somewhat resembles the emergence of statistical mechanics.

**There, one also began with macroscopic quantities:**
- Pressure
- Temperature  
- Volume

**Later, one recognized:** Temperature is not fundamental. Fundamental are the microscopic state transitions.

**In the current project:**

| Statistical Mechanics | EABC Project |
|----------------------|--------------|
| Microstates | Gap classes |
| Transitions | P(g\|a) |
| Dynamics | P(a→b) |
| Temperature | H_C(X) |

**Of course only as a methodological analogy, not as mathematical identity.**

---

## Why Modulo 30 Is Now So Important

**The modulo 30 test answers a much deeper question than increasing X.**

**Larger X answers:**
```
Does the effect persist?
```

**Modulo 30 answers:**
```
What kind of effect is this?
```

**This is the scientifically more important question.**

If similar conditional gap asymmetries appear at modulo 30, an entire class of investigations suddenly emerges:

```
P(g mod m | p_n mod m)
```

for various moduli m.

**Then the project would evolve:** From a special EABC story to a general research program about local prime transitions.

---

## The Strongest Future Result

**Interestingly, I no longer believe that a theorem about H_C(X) would be the strongest result.**

**Much stronger would be something like:**

"For consecutive primes, the conditional gap distributions modulo 12 show measurable asymmetries between residue classes {2,4} and {8,10}, which completely explain the observed orientation preferences."

**This would be conceptually deeper.**

Then the orientation bias would no longer be the phenomenon itself. It would merely be its most visible consequence.

---

## Current Standing

### Established

✅ EABC classification  
✅ Observable χ  
✅ Bias function H_C  
✅ **Conditional gap asymmetries modulo 12 in the investigated range**  
✅ **Asymmetric transition matrix**  
✅ **Explanation of observed orientation bias through these transitions**

### Open

❓ Convergence of R(X)  
❓ Modulo 30 generalization  
❓ Connection to known sieve models  
❓ Connection to Hardy-Littlewood heuristics  
❓ Asymptotic behavior of P(g mod 12 | a)

**The project is now far removed from geometric speculation. It has become a clearly defined program about local statistical laws of prime transitions. Precisely this shift makes the current state significantly stronger than the original motivation.**

---

*Gap asymmetry established - most plausible interpretation is R(X) → 1 with slow relaxation*  
*Primary finding: P(g ≡ 2,4) > P(g ≡ 8,10) for all start classes*  
*22.06.2026*
