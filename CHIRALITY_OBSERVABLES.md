# Chirality Observables on Complete Prime Quadruples Modulo 12

## Abstract

We define a **chirality observable** χ on complete EABC prime quadruples and study the **holonomy function** H_C(X), which measures the imbalance between two canonical orientations (EABC vs. ECBA). This observable is analogous to bias terms in prime number races and may be related to known residue class biases.

---

## Part I: Exact Definitions

### 1.1 EABC Classification

For primes p > 3, define the EABC classification modulo 12:

```
E: p ≡ 1  (mod 12)
A: p ≡ 5  (mod 12)
B: p ≡ 7  (mod 12)
C: p ≡ 11 (mod 12)
```

**Status:** Exact arithmetic definition. ✓

### 1.2 Complete Quadruples

A prime quadruple Q = (p, q, r, s) is **complete** if:

```
{k_p, k_q, k_r, k_s} = {E, A, B, C}
```

Each of the four EABC classes appears exactly once.

**Status:** Precisely defined subset of ℕ⁴. ✓

### 1.3 Signature

The **signature** of Q is:

```
sig(Q) = (k_p, k_q, k_r, k_s) ∈ {E, A, B, C}⁴
```

**Status:** Exact function ℕ⁴ → {E,A,B,C}⁴. ✓

### 1.4 Normalization

The **normalized signature** norm(sig(Q)) is obtained by cyclic rotation until E appears first.

**Example:**
```
sig(Q) = (B, C, E, A) → norm(sig(Q)) = (E, A, B, C)
```

**Status:** Well-defined function {E,A,B,C}⁴ → {E,A,B,C}⁴. ✓

### 1.5 Chirality Observable

The **chirality observable** is defined as:

```
χ(Q) = ⎧ +1,  norm(sig(Q)) = EABC
       ⎨ -1,  norm(sig(Q)) = ECBA
       ⎩  0,  otherwise
```

**Interpretation:**
- χ(Q) = +1: Positive orientation E → A → B → C → E
- χ(Q) = -1: Negative orientation E → C → B → A → E
- χ(Q) = 0: Other permutation

**Status:** Exact function on complete quadruples. ✓

### 1.6 Holonomy Function

For a construction method C (a rule for selecting/ordering prime quadruples), define:

```
H_C(X) = Σ_{Q≤X, Q∈C} χ(Q)
```

where the sum runs over all complete quadruples Q up to X constructed by method C.

**Alternative formulation:**
```
H_C(X) = N_{EABC}^C(X) - N_{ECBA}^C(X)
```

where N_{EABC}^C(X) is the count of EABC-quadruples and N_{ECBA}^C(X) is the count of ECBA-quadruples under construction C.

**Status:** Well-defined arithmetic function for each C. ✓

### 1.7 Normalized Holonomy

```
h_C(X) = H_C(X) / N_C(X)
```

where N_C(X) is the total number of complete quadruples up to X under construction C.

**Status:** Well-defined function ℝ₊ → [-1, 1]. ✓

---

## Part II: Construction Methods

Different construction methods C yield different holonomy functions:

### C_consec: Consecutive primes
```
Q_n = (p_n, p_{n+1}, p_{n+2}, p_{n+3})
```

### C_random: Random permutation
```
For each complete quadruple {p,q,r,s}, apply a random permutation σ
```

### C_smooth: Smooth-shell quadruples
```
Select p from smooth shell, then next three primes outside shell
```

### C_gaps: Gap-ordered
```
Sort primes by gap sizes g_n = p_{n+1} - p_n before forming quadruples
```

**Status:** Each C is a precisely defined selection/ordering rule. ✓

---

## Part III: Empirical Observations

### 3.1 Random Construction (C_random)

**Observation:**
```
h_{C_random}(10⁴) ≈ 0.000
```

**Interpretation:** The random construction exhibits **no chirality bias**, consistent with the null hypothesis that EABC classes are symmetric.

**Status:** Empirically verified. Supports theoretical expectation.

### 3.2 Consecutive Construction (C_consec)

**Observation:**
```
h_{C_consec}(10³) ≈ 0.396
h_{C_consec}(10⁴) ≈ 0.270
h_{C_consec}(10⁵) ≈ 0.194
```

**Interpretation:** The consecutive construction shows **positive chirality bias** that appears to decrease with X, but remains significantly > 0.

**Status:** Empirically observed. Asymptotic behavior unknown.

### 3.3 Construction Dependence

**Key Finding:**

The chirality bias depends critically on the construction method C:

```
|h_{C_consec}(X)| >> |h_{C_random}(X)| ≈ 0
```

**Implication:** There is no "intrinsic chirality of primes mod 12". The bias is a property of the construction, not the primes themselves.

**Status:** Established by robustness tests.

---

## Part IV: Open Questions

### Question 1: Asymptotic Behavior

**Primary Question:**

For the consecutive construction, does:

```
lim_{X→∞} h_{C_consec}(X) = 0?
```

Or does a persistent bias exist:

```
limsup_{X→∞} |h_{C_consec}(X)| > 0?
```

**Current Evidence:**
- h(X) decreases from 0.4 to 0.19 over three orders of magnitude
- But convergence to 0 not established

**Status:** Open.

### Question 2: Correlation with Prime Gaps

**Hypothesis:**

```
Corr(χ(Q_n), g_n) ≠ 0?
```

where g_n = p_{n+1} - p_n is the prime gap.

**Rationale:** Large gaps might correlate with specific EABC patterns.

**Status:** Untested.

### Question 3: Connection to Prime Races

**Analogy:**

Classic prime race (Chebyshev bias):
```
π(x; 4, 3) - π(x; 4, 1) > 0  for most x
```

counts primes 3 (mod 4) vs. primes 1 (mod 4).

Our holonomy:
```
H_C(X) = N_{EABC}(X) - N_{ECBA}(X)
```

counts EABC-oriented vs. ECBA-oriented quadruples.

**Question:** Is H_C(X) related to known residue class biases?

**Status:** Unexplored connection to established theory.

### Question 4: Extremal Constructions

**Optimization Problem:**

```
max/min H_C(X)  over all constructions C
```

**Interpretation:** Which ordering of primes maximizes/minimizes chirality bias?

**Status:** Computational problem, unsolved.

### Question 5: Other Moduli

**Generalization:**

Do analogous chirality observables exist for:
- Modulo 30 (8 prime classes)
- Modulo 60 (16 prime classes)
- General modulo q

**Status:** Framework extends naturally, but unstudied.

---

## Part V: What is NOT Established

### 5.1 Intrinsic Chirality

**Claim (FALSE):**
> "Primes mod 12 prefer the ABCEA orientation."

**Correction:**
The bias is construction-dependent. Under random ordering, h(X) ≈ 0.

**Status:** Refuted by robustness tests.

### 5.2 Topological Invariants

**Claim (FALSE):**
> "χ = -1 is an emergent topological property of primes."

**Correction:**
No canonical 2-complex exists. The value χ = V - E + F = -1 depends on heuristic face counting in a specific graph construction.

**Status:** Not a rigorous topological invariant.

### 5.3 Klein Bottle Structure

**Claim (FALSE):**
> "Primes form a discrete Klein bottle."

**Correction:**
The Klein bottle is a **metaphor** for the two orientations (EABC ↔ positive, ECBA ↔ negative). It is not a rigorously emergent structure.

**Status:** Heuristic imagery, not mathematics.

---

## Part VI: Connection to Prime Number Races

### 6.1 Chebyshev Bias

**Classical Result:**

For primes mod 4:
```
π(x; 4, 3) > π(x; 4, 1)  for "most" x < 10²⁶
```

Despite both residue classes having the same asymptotic density by Dirichlet's theorem.

**Rubinstein-Sarnak (1994):**
Logarithmic density of {x : π(x;4,3) > π(x;4,1)} ≈ 0.9959.

### 6.2 Analogy to H_C(X)

**Structure:**

Both measure **imbalance between symmetric classes**:

```
Chebyshev: π(x;4,3) - π(x;4,1)
Holonomy:  N_{EABC}(X) - N_{ECBA}(X)
```

**Key Difference:**

Chebyshev bias involves **individual primes** in residue classes.
Holonomy bias involves **tuples** of primes with specific patterns.

### 6.3 Potential Connection

**Hypothesis:**

If consecutive primes exhibit correlations in their mod 12 residues, this could induce a bias in H_{C_consec}(X).

**Example:**
If p ≡ 1 (mod 12) is slightly more likely to be followed by p' ≡ 5 (mod 12) than by p' ≡ 11 (mod 12), this could favor EABC over ECBA.

**Status:** Speculative but testable.

---

## Part VII: Research Program

### Phase 1: Large-Scale Computation (Immediate)

**Goal:** Compute h_{C_consec}(X) for X = 10⁶, 10⁷, 10⁸.

**Question:** Does h(X) → 0 or stabilize at positive value?

### Phase 2: Correlation Analysis (Short-term)

**Goal:** Compute:
- Corr(χ(Q_n), g_n) - correlation with prime gaps
- Corr(χ(Q_n), consecutive residue patterns)
- Conditional probabilities P(Q_{n+1} = EABC | Q_n = EABC)

### Phase 3: Theoretical Model (Medium-term)

**Goal:** Develop heuristic probabilistic model:
- Assume primes mod 12 are "random" with weak correlations
- Predict E[H_C(X)] and Var[H_C(X)]
- Compare to empirical data

### Phase 4: Connection to Prime Races (Long-term)

**Goal:** Relate H_C(X) to established results:
- Rubinstein-Sarnak framework for prime races
- Correlation structure of consecutive prime residues
- Logarithmic density of bias regions

---

## Part VIII: Precise Mathematical Claims

### Theorem 1 (Trivial)

For construction C_random (random permutation):

```
E[H_{C_random}(X)] = 0
```

**Proof:** By symmetry, P(EABC) = P(ECBA) = 1/6 among 4! = 24 permutations that normalize to E-first. □

### Theorem 2 (Empirical)

For construction C_consec on data up to X = 10⁵:

```
h_{C_consec}(X) > 0.1
```

**Proof:** Direct computation. See ROBUSTNESS_TESTS.md. □

### Conjecture 1 (Weak)

For "symmetric" constructions C (including random orderings):

```
H_C(X) = o(N_C(X))
```

**Status:** Open. Supported by C_random data.

### Conjecture 2 (Strong)

For C_consec:

```
h_{C_consec}(X) ∼ c / log X  for some c > 0
```

**Motivation:** Analogous to logarithmic decrease in prime race biases.

**Status:** Speculative.

### Conjecture 3 (Connection to Gaps)

```
Corr(χ(Q_n), g_n) = O(1/log p_n)
```

**Motivation:** Weak but non-zero correlation between chirality and local prime distribution.

**Status:** Untested.

---

## Part IX: Summary

### What is Rigorously Defined

1. ✓ EABC classification (mod 12)
2. ✓ Complete quadruples
3. ✓ Signature and normalization
4. ✓ Chirality observable χ(Q)
5. ✓ Holonomy function H_C(X)
6. ✓ Construction-dependent framework

### What is Empirically Observed

7. ✓ h_{C_random} ≈ 0 (symmetry under random ordering)
8. ✓ h_{C_consec} ≈ 0.19 (bias under consecutive ordering)
9. ✓ h(X) appears to decrease slowly

### What Remains Open

10. ? Asymptotic behavior: lim h(X) = 0 or > 0?
11. ? Correlation with prime gaps, residue patterns
12. ? Connection to classical prime races
13. ? Optimal constructions: max/min H(X)

### What is NOT Claimed

14. ✗ "Intrinsic chirality of primes" (refuted)
15. ✗ χ = -1 as topological invariant (not rigorous)
16. ✗ Klein bottle structure (metaphor only)

---

## Part X: Relation to Existing Literature

### Prime Number Races

- Chebyshev (1850s): First observations of prime race bias
- Rubinstein & Sarnak (1994): "Chebyshev's bias"
- Ng (2004): Generalized prime races mod q

**Our work:** Extends race concept from individual primes to oriented tuples.

### Prime Gaps

- Cramér conjecture: g_n = O((log p_n)²)
- Maier (1985): Irregularities in prime gaps
- Zhang (2013): Bounded gaps

**Potential connection:** H_C(X) may correlate with gap distribution.

### Modular Forms and L-functions

- Dirichlet L-functions encode residue class information
- Oscillatory behavior of π(x;q,a) - Li(x)/φ(q)

**Speculative:** Could H_C(X) be related to L-function oscillations?

---

## Conclusion

The **chirality observable χ** on complete EABC prime quadruples induces the **holonomy function H_C(X)**, a well-defined arithmetic observable that measures orientation bias under construction method C.

**Key insight:** The bias is construction-dependent, not intrinsic to primes.

**Open question:** Does a "natural" or "canonical" construction exhibit persistent bias?

**Potential significance:** If h_C(X) correlates with known prime distribution phenomena (gaps, races), it provides a new lens on local prime structure beyond simple residue classes.

**The claim is modest but rigorous:** We have defined a new observable. Its asymptotic behavior and potential connections remain to be explored.

---

*Mathematical formulation clarified, 22.06.2026*
