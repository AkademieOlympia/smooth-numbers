# Paper Outline: An Elimination Architecture for Prime Gap Asymmetries

**Target Journal**: Experimental Mathematics  
**Positioning**: Methodology-focused, computational number theory  
**Tone**: Conservative, descriptive, reproducible

---

## Title

**An Elimination Architecture for Prime Gap Asymmetries: Systematic Falsification of Standard Correlation Models**

Alternative (shorter):
**Elimination Architecture for Prime Gap Asymmetries**

---

## Abstract (Draft)

We introduce a reproducible elimination architecture for the study of prime gap asymmetry statistics. Starting from an empirical observable H(Δr) defined on residue-class gap transitions, we systematically test increasingly sophisticated explanatory frameworks, including Bernoulli models, Cramér models, Hardy-Littlewood pair-gap models, Wheel-30 null models, and low-order Hardy-Littlewood k-tuple models (k≤4).

The central result is not a theoretical explanation of H(Δr), but the construction of a documented falsification chain. Across all tested reductions, the residual signal remains stable and reproducible over sample sizes ranging from 10⁵ to 10⁷. Specifically:
- Hardy-Littlewood pair-gaps exhibit anti-correlation (ρ = -0.76)
- Wheel-30 null models are falsified with z-scores exceeding 50
- k-tuple models (k=3,4) show systematic anti-correlation (ρ ≈ -0.93)

The observable H(Δr) therefore emerges as the current survivor of a systematic elimination process. Its theoretical origin remains open. The contribution is primarily methodological: a reproducible framework for isolating arithmetic residuals through progressive null-model testing.

**Keywords**: prime gaps, elimination architecture, Hardy-Littlewood conjecture, experimental mathematics, reproducibility

---

## 1. Introduction

### 1.1 Motivation

Context:
- Gap statistics in prime sequences have been studied since Hardy-Littlewood
- Most work focuses on *explaining* observed patterns via theory
- Less attention to *systematic elimination* of candidate explanations

Our approach:
- Start with empirical observable (gap asymmetry)
- Build explicit elimination chain
- Document what survives, not what explains

### 1.2 Experimental Mathematics and Object Formation

Philosophical positioning:
- Not claiming to discover "new structure"
- Testing: Can an observable survive progressive falsification?
- Criterion: Stability under increasingly sophisticated null models

Object formation criteria (reference OBJECT_CRITERIA.md):
1. Reproducibility
2. Model-independence
3. Projection-invariance
4. Theoretical connectability (tested, not assumed)
5. Autonomy (not claimed)

### 1.3 Elimination versus Explanation

Key distinction:
- **Explanation**: H(Δr) = f(known theory)
- **Elimination**: H(Δr) ≠ f₁, ≠ f₂, ..., ≠ fₙ

Benefits of elimination approach:
- Claims remain valid even if H(Δr) explained later
- Methodological contribution independent of object interpretation
- Reproducible framework for future investigations

Structure of paper:
- Section 2: Define H(Δr)
- Section 3: Projection robustness
- Section 4: Elimination chain
- Section 5: Reproducibility tests
- Section 6: Discussion

---

## 2. Definition of the Observable

### 2.1 Gap Asymmetries in Residue Classes

**Setup**:
- Primes p > 5 lie in residue classes {1,7,11,13,17,19,23,29} mod 30
- Gap g = p_{n+1} - p_n has residue g mod 30
- Question: Are gap distributions uniform across residue classes?

**Gap transitions**:
- For prime p_n ≡ c (mod 30), count transitions to gaps g mod 30
- Define: N(c → g) = # of transitions from class c to gap g

**Asymmetry ratio** (for class c):
- Low-gaps L = {2,4,6,8} mod 30
- High-gaps H = L + Δr (shifted by Δr mod 30)
- R(c, Δr) = N(c → L) / N(c → H)

### 2.2 Projection Families

**Gap-pair projections**:
- Base 2: L = {2,4,6}, H = {2+Δr, 4+Δr, 6+Δr}
- Base 4: L = {4,6,8}, H = {4+Δr, 6+Δr, 8+Δr}
- Base 6, Base 8 (similarly)

**Motivation**: Test if asymmetry depends on gap-pair choice

**Notation**:
- A_i(Δr) = amplification ratio for projection base i
- A_i(Δr) = R_sequence(i,Δr) / R_Bernoulli(i,Δr)

### 2.3 Extraction of H(Δr)

**Observation** (Stage 4):
- For Δr ≤ 18: A_2, A_4, A_6, A_8 highly correlated (ρ > 0.96)
- For Δr ≥ 20: Projections diverge (ρ < 0.5)

**Definition**:
- Regime I (Δr ≤ 18): H(Δr) = geometric_mean(A_2, A_4, A_6, A_8)
- Regime II (Δr ≥ 20): Projection-dependent (not studied here)

**Domain restriction**: This paper focuses on Regime I (Δr ≤ 18)

**Numerical values** (N=10⁷):
```
Δr    H(Δr)
2     1.075
6     1.498
10    2.012
14    2.686
18    3.554
```

---

## 3. Projection Robustness

### 3.1 Gap-Pair Family

**Test design**:
- Compute A_i(Δr) for 4 independent projections
- Test null hypothesis: A_i are independent statistics

**Method**:
- Correlation matrix ρ_{ij} for projections i,j
- Test significance via bootstrap

### 3.2 Correlation Analysis

**Results**:
- Δr=2: ρ_min = 0.94
- Δr=6: ρ_min = 0.97
- Δr=10: ρ_min = 0.98
- Δr=14: ρ_min = 0.97
- Δr=18: ρ_min = 0.96

**Interpretation**: High correlation → common underlying signal H(Δr)

### 3.3 Emergence of Regime I

**Crossover at Δr ≈ 20**:
- Regime I (Δr ≤ 18): ρ > 0.9 (projection-invariant)
- Regime II (Δr ≥ 20): ρ < 0.5 (projection-dependent)

**Consequence**: H(Δr) well-defined only for Δr ≤ 18

**Figure 1**: Correlation heatmap ρ(A_i, A_j) as function of Δr

---

## 4. Elimination Architecture

This is the **core section** - most important for Experimental Mathematics audience.

### 4.1 Stage 1-2: Bernoulli and Cramér Baselines

**Bernoulli model**:
- Random thinning with geometric gaps
- Restricted to Wheel-30 residues
- Purpose: Test if H(Δr) is purely statistical noise

**Result**: H_Prime ≫ H_Bernoulli (all Δr)

**Cramér model**:
- Independent selection with density 2/ln(n)
- Restricted to Wheel-30
- Purpose: Test if logarithmic density sufficient

**Result**: H_Prime ≫ H_Cramér (all Δr)

### 4.2 Stage 5: Hardy-Littlewood Pair-Gap Model

**HL pair model**:
- H_HL(Δr) = Σ_g w_g(Δr) · S₂(g)
- S₂(g) = Hardy-Littlewood singular series for gap g
- w_g(Δr) = weight based on Δr-relevance

**Test**: Correlation ρ(H_Prime, H_HL)

**Result**: ρ = -0.76 (p < 0.05)
- **Strong anti-correlation**, not independence
- H(Δr) exhibits opposite trend to HL pair predictions

**Interpretation**: 
- H(Δr) ≠ f(S₂) for tested construction f
- Does NOT exclude all HL pair models

### 4.3 Stage 5.5: Wheel-30 Null Models

**Motivation**: Before attributing H(Δr) to prime-specific correlations, test simpler alternative: Is it just Wheel-30 arithmetic?

**Two null models**:

1. **WheelRandom**:
   - Random thinning of Wheel-30 numbers
   - Density matched to actual primes
   - Tests: Is H(Δr) just residue-class structure?

2. **WheelCramér**:
   - Cramér density (2/ln(n)) restricted to Wheel-30
   - Tests: Is logarithmic density + Wheel sufficient?

**Method**: Apply identical pipeline (gap-transitions → H(Δr))

**Results** (N=10⁷, 5 seeds):

| Δr | H_Prime | H_WheelRandom | H_WheelCramér | z_rand | z_cram |
|----|---------|---------------|---------------|--------|--------|
| 2  | 1.075   | 0.981 ± 0.002 | 1.021 ± 0.001 | 55     | 52     |
| 6  | 1.498   | 1.117 ± 0.008 | 1.260 ± 0.003 | 46     | 93     |
| 10 | 2.012   | 1.197 ± 0.008 | 1.462 ± 0.003 | 109    | 200    |
| 14 | 2.686   | 1.247 ± 0.004 | 1.643 ± 0.002 | 334    | 453    |
| 18 | 3.554   | 1.379 ± 0.004 | 1.951 ± 0.005 | 573    | 327    |

**Statistical assessment**:
- All z > 45 (p < 10⁻⁹)
- Systematic underestimation by factors 1.05-2.58

**Interpretation**:
- Tested Wheel-30 models falsified
- H(Δr) contains structure beyond:
  - Residue-class constraints
  - Independent density effects
- Does NOT exclude all Wheel-based models (e.g., Wheel-210, Markov-Wheel)

**Figure 2**: H_Prime vs H_Wheel comparison (bar chart + scatter)

### 4.4 Stage 6: Hardy-Littlewood k-Tuple Screening

**Motivation**: After pair-gap failure (k=2), test higher-order correlations (k=3,4)

**Important**: This is a **screening test**, not complete k-tuple theory

**Method**:
- Count k-tuple patterns (k=3,4) in primes up to 10⁶
- Compute HL constants S₃(H), S₄(H) for patterns
- Construct H_k3(Δr), H_k4(Δr) via relevance-weighted sum
- Test correlation with H_Prime(Δr)

**Results** (N=10⁶):

| Model | Correlation | p-value | Interpretation |
|-------|-------------|---------|----------------|
| k=3 (triples) | ρ = -0.935 | 0.020 | Strong anti-correlation |
| k=4 (quads) | ρ = -0.925 | 0.024 | Strong anti-correlation |

**Residue-class sensitivity**:
- CV(S₃ by residue) = 0.048
- Weak residue-dependence (not strong enough to explain H)

**Interpretation**:
- Tested HL k-tuple constructions exhibit **opposite trends** to H(Δr)
- H(Δr) incompatible with standard low-order HL observables
- Does NOT exclude:
  - Residue-class-specific k-tuple models
  - Higher k (k ≫ 4)
  - Non-HL frameworks (sieve theory, etc.)

**Figure 3**: Correlation scatter plots (H_k3 vs H_Prime, H_k4 vs H_Prime)

---

## 5. Reproducibility

### 5.1 N-Scaling Tests

**Test**: Do results hold at higher statistics?

**Stage 5.5 scaling** (WheelCramér z-scores):
- N=10⁵: z ∈ [8, 50]
- N=10⁶: z ∈ [16, 164]
- N=10⁷: z ∈ [52, 453]

**Observation**: z-scores scale as √N (expected for genuine signal)

**Stage 6 correlation stability**:
- N=10⁵: ρ(k=3) = -0.936
- N=10⁶: ρ(k=3) = -0.935
- Change: Δρ = 0.001

**Conclusion**: Results robust across two orders of magnitude

### 5.2 H(Δr) Convergence

**Observation**: H(Δr) values decrease with larger N

| Δr | N=10⁵ | N=10⁶ | N=10⁷ | Trend |
|----|-------|-------|-------|-------|
| 2  | 1.162 | 1.104 | 1.075 | ↓ Converging |
| 18 | 8.121 | 4.750 | 3.554 | ↓ Converging |

**Interpretation**: Finite-size effects present at N=10⁵

**Consequence**: Report N=10⁷ values as primary

### 5.3 Numerical Robustness

**Code availability**: All code in public repository
**Compilation**: Standard C++17, no special libraries
**Runtime**: ~3 seconds for N=10⁷ test

**Reproducibility command**:
```bash
make wheel30_test
./wheel30_test 10000000 5
```

**Table 1**: Full numerical results with error bars

---

## 6. Discussion

### 6.1 What Has Been Eliminated

Summary of falsified models:
1. **Bernoulli/Cramér**: Independent thinning insufficient
2. **HL pair-gaps (k=2)**: Anti-correlation (ρ = -0.76)
3. **Wheel-30 Random**: z-scores > 45
4. **Wheel-30 Cramér**: z-scores > 50
5. **HL triples (k=3)**: Anti-correlation (ρ = -0.94)
6. **HL quads (k=4)**: Anti-correlation (ρ = -0.93)

**Common pattern**: Tested models either:
- Underestimate H(Δr) systematically (Wheel models)
- Exhibit opposite trends (HL models)

### 6.2 What Remains Open

**Unexplored frameworks**:
- Wheel-210, Wheel-2310 (higher-order sieve)
- Markovian Wheel models (local correlations)
- Residue-class-specific HL k-tuples
- Higher k (k > 4)
- Sieve theory beyond Wheel
- Random matrix analogies

**Key limitation**: We tested *specific implementations* of HL theory
- Does NOT exclude all HL-based explanations
- Shows that *naive* HL observables fail

### 6.3 Candidate Interpretations

**Speculation** (clearly labeled as such):

1. **Higher-order sieve structure**:
   - H(Δr) may reflect k-tuple correlations with k ≫ 4
   - Requires residue-class-specific singular series

2. **Non-HL correlations**:
   - Beyond standard HL framework
   - Possible connection to sieve irregularities

3. **Finite-N artifact**:
   - Converging trend suggests eventual decay
   - But signal stable through N=10⁷

**Conservative position**: Theoretical origin currently unknown

---

## 7. Conclusion

**Main result**: Construction of reproducible elimination architecture for prime gap asymmetries

**Key components**:
1. Observable H(Δr) defined via projection-invariance
2. Systematic falsification of 6 null model classes
3. Reproducibility verified across N ∈ [10⁵, 10⁷]

**Scientific contribution**:
- Primarily **methodological**: elimination framework
- Secondarily: identification of residual signal H(Δr)

**Long-term value**: Framework applicable to other arithmetic problems
- Template for testing observable candidates
- Explicit null-model hierarchy
- Reproducible computational pipeline

**Future work**:
- Extend to Δr > 18 (Regime II)
- Test Wheel-210, higher k-tuples
- Seek theoretical explanation

**Final statement**:
> The contribution is not primarily the observable H(Δr), but a documented elimination architecture capable of separating arithmetic signals from progressively stronger null models. H(Δr) emerges as the current survivor. Its theoretical origin remains open.

---

## Appendices

### Appendix A: Numerical Tables

Full tables:
- H(Δr) values at N=10⁵, 10⁶, 10⁷
- Wheel model comparisons with error bars
- k-tuple pattern frequencies

### Appendix B: Code Availability

- GitHub repository link
- Compilation instructions
- Reproducibility checklist

### Appendix C: Additional Figures

- Full correlation matrices
- Convergence plots
- Gap-pair projections

---

## Figures (Priority List)

**Figure 1**: Projection robustness
- (a) Correlation heatmap ρ(A_i, A_j)
- (b) Crossover at Δr=20

**Figure 2**: Stage 5.5 (Wheel-30 falsification)
- (a) Bar chart: H_Prime vs H_WheelRandom vs H_WheelCramér
- (b) Scatter: H_Prime vs H_Wheel (both models)

**Figure 3**: Stage 6 (k-tuple screening)
- (a) Scatter: H_Prime vs H_k3
- (b) Scatter: H_Prime vs H_k4
- (c) Bar: Correlation summary

**Figure 4**: Reproducibility
- (a) N-scaling of z-scores (log-log plot)
- (b) H(Δr) convergence with N

**Figure 5**: Elimination chain summary
- Flow diagram showing all 6 stages
- With verdicts (falsified/anti-correlated)

---

## Writing Timeline (Estimated)

**Day 1**: Sections 1-2 (Introduction + Definition)
**Day 2**: Section 3-4.1 (Projection tests + early stages)
**Day 3**: Section 4.2-4.4 (HL tests + Wheel tests + k-tuples)
**Day 4**: Section 5-6 (Reproducibility + Discussion)
**Day 5**: Section 7 + Abstract + Figures
**Day 6**: Polish + Appendices + Bibliography
**Day 7**: Final review + submission prep

**Total**: 1 week focused writing

---

## Language Guidelines

**AVOID**:
- "discovery", "breakthrough", "fundamental"
- "proves", "demonstrates" (use "suggests", "indicates")
- "new theory", "paradigm shift"
- Overclaiming theoretical significance

**PREFER**:
- "observable", "candidate object", "residual signal"
- "elimination", "falsification", "incompatible with"
- "reproducible", "documented", "systematic"
- Methodological framing

**Tone**: Factual, conservative, methodology-focused

---

## Target: Experimental Mathematics

**Why good fit**:
- Methodology-focused journal
- Values reproducibility
- Accepts "objects without full theory"
- Computational emphasis
- Elimination/falsification approach welcome

**Typical length**: 15-25 pages (perfect for this paper)

**Submission format**: LaTeX (standard article class)

---

## Next Steps

1. ✓ Outline complete
2. → Start writing Section 1 (Introduction)
3. → Generate Figure 1 (projection robustness)
4. → Draft Abstract (iterate after full draft)
5. → Section-by-section writing
6. → Figure generation (Python/matplotlib)
7. → Bibliography (BibTeX)
8. → Polish + submission

**Ready to begin writing.**
