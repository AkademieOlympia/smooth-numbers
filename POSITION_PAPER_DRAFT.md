# Position Paper: On the Empirical Isolation of A(Δr)
## Methodological Framework for Arithmetic Amplification Factors

Draft: 23. Juni 2026  
**Status: For submission after positive Gap-Pair robustness test**

---

## Abstract

The principal outcome of the present investigation is the identification of an empirical amplification factor

```
A(Δr) = R_Prime(Δr) / R_Bernoulli(Δr)
```

which separates universal geometric sparsity effects from arithmetic correlations specific to the prime numbers.

The significance of this factor does not depend on a complete theoretical explanation. Its importance derives from the fact that it appears **after subtraction of a mathematically understood baseline** and therefore represents a **residual arithmetic signal**.

The central open problem is whether A(Δr) can be derived from Hardy-Littlewood singular series or related correlation structures. Until such a derivation exists, **A(Δr) should be viewed as an experimentally observed arithmetic observable** rather than a theoretically understood quantity.

The primary criterion for its scientific relevance is **robustness under alternative projection schemes** and statistical resampling procedures.

---

## 1. Introduction: The Pattern of Mathematical Program Formation

Successful mathematical research programs often follow a characteristic pattern:

```
Observation → Null Model → Decomposition → New Object
```

This is not specific to our investigation, but represents a general methodological framework observed across diverse mathematical disciplines.

**Examples**:
- Riemann: Prime distribution → Li(x) comparison → π(x) = Li(x) + error → ζ(s) zeros
- Ramanujan: τ(n) patterns → multiplicative comparison → main term · correction → Modular forms
- Birch-Swinnerton-Dyer: Rational points → generic curves → rank + torsion → L-functions

**This work**:
- Gap asymmetry → Bernoulli comparison → R_Prime = R_Bernoulli · A → A(Δr) isolation

---

## 2. The Geometric Baseline (Mathematically Understood)

For Bernoulli point processes (discrete Poisson analogues) with constant acceptance probability p, we derive:

```
R_Bernoulli(Δr) = (1-p)^(-Δr)
```

This formula represents the **universal geometric short-gap bias** present in any sparse point process with geometric gap distribution.

**Status**: 
- ✓ Analytically proven
- ✓ Numerically verified
- ✓ Publication-ready

**Significance**: Provides a mathematically understood baseline against which prime-specific effects can be measured.

---

## 3. The Arithmetic Amplification Factor

### Definition

```
A(Δr) := R_Prime(Δr) / R_Bernoulli(Δr)
```

This factor quantifies how Hardy-Littlewood correlations amplify (A > 1) or suppress (A < 1) the universal geometric baseline.

### Empirical Properties (N=10^6, 20 seeds)

**Three robust regimes**:
1. Twin enhancement: A(2) ≈ 1.06 (±0.04)
2. Geometric suppression: A(6) ≈ 0.84 (±0.04)
3. Large-distance enhancement: A(24) ≈ 1.18 (±0.07)

**Non-monotonic structure**: A(Δr) oscillates in intermediate range (Δr = 4 to 18), suggesting competition between different k-tuple correlations.

### Why A(Δr) Matters

The significance of A(Δr) does not depend on immediate theoretical explanation. Its value lies in:

1. It appears **after subtraction of understood baseline** → represents pure arithmetic signal
2. It provides **quantitative target** for Hardy-Littlewood analysis
3. It separates **universal effects from prime-specific correlations**
4. It transforms vague question ("Why asymmetry?") into precise one ("What is A(Δr)?")

---

## 4. Robustness Criteria

The scientific relevance of A(Δr) depends on two critical tests:

### Criterion 1: Projection Invariance

**Test**: Compute A(Δr) for alternative gap-pair selections:
- {2,4,6} vs {2+Δr, 4+Δr, 6+Δr} (original)
- {4,6,8} vs {4+Δr, 6+Δr, 8+Δr}
- {6,8,10} vs {6+Δr, 8+Δr, 10+Δr}
- {8,10,12} vs {8+Δr, 10+Δr, 12+Δr}

**Expected result**: Qualitative structure (three regimes, non-monotonicity) should persist with quantitative variation.

**Interpretation**:
- If robust → A(Δr) is intrinsic property of prime correlations
- If not robust → A(Δr) is partially projection-dependent artifact

### Criterion 2: Statistical Significance

**Test**: Bootstrap confidence intervals, formal significance tests for regime distinctions.

**Expected result**: Regime differences should be statistically significant at α = 0.05 level.

**Interpretation**:
- If significant → Oscillations are real structure, not sampling noise
- If not significant → Larger sample sizes or finer analysis required

---

## 5. Open Theoretical Questions

### Primary Question: Can A(Δr) Be Derived?

We hypothesize a singular-series decomposition:

```
A(Δr) = ∑_g w_g(Δr) · H(g)
```

where:
- H(g) = Hardy-Littlewood singular series for gap g
- w_g(Δr) = weight function (depends on residue-class structure)

**Predictions**:
1. At Δr=2: Twin prime constant Π₂ ≈ 0.660 should dominate
2. At larger Δr: Multiple k-tuple correlations (cousins, sexy primes, etc.) interfere
3. Non-monotonicity: Different g values dominate at different Δr

**Status**: Speculative. Requires explicit computation of w_g(Δr) from residue-class geometry.

### Secondary Questions

1. Does A(Δr) generalize to other moduli (60, 210, ...)?
2. What is the asymptotic behavior as Δr → ∞?
3. Can modified Cramér models (with sieve) explain intermediate suppression?
4. Is there a connection to Chebyshev bias or prime number races?

---

## 6. A(Δr) as an Experimentally Observed Arithmetic Observable

Until a theoretical derivation exists, we propose viewing A(Δr) as an **empirical arithmetic observable** with the following characteristics:

**Empirical Status**:
- ✓ Well-defined mathematically
- ✓ Robustly measured (20 seeds, N=10^6)
- ✓ Consistent across multiple moduli (12, 30)
- ? Projection-invariant (pending Gap-Pair test)
- ? Statistically significant oscillations (pending Bootstrap)

**Theoretical Status**:
- ? Hardy-Littlewood connection (conjectured)
- ? Singular-series decomposition (speculative)
- ? Asymptotic behavior (open)

**Scientific Relevance**:
The value of A(Δr) lies not in immediate explanation, but in:
1. **Precision**: Transforms vague question into quantitative target
2. **Isolation**: Separates what needs explaining from what's understood
3. **Robustness**: Multiple independent measurements converge
4. **Falsifiability**: Clear criteria for rejection (projection dependence)

---

## 7. Conclusion: The Beginning of a Research Program

If gap-pair robustness tests confirm projection invariance, A(Δr) transitions from "interesting quotient" to "intrinsic mathematical object."

This transition marks the beginning of a research program rather than its conclusion:

**Phase I** (current): Empirical isolation and robustness testing  
**Phase II** (next 1-2 years): Systematic investigation across moduli  
**Phase III** (long-term): Theoretical derivation from Hardy-Littlewood

The shift from "Why do primes exhibit asymmetry?" to "What is the structure of A(Δr)?" represents scientific maturation: not premature explanation, but precise problem formulation.

**The meta-theoretical lesson**: Successful mathematical programs often begin not with answers, but with isolation of the right questions.

---

## Suggested Target Journals

- **Experimental Mathematics**: Primary target (empirical focus)
- **Notices of the AMS**: Methodological essay
- **Mathematical Intelligencer**: Philosophy of mathematics angle
- **Bulletin of the AMS**: Broader mathematical audience (if results strengthen)

---

## Acknowledgments

[To be added after completion of robustness tests]

---

## References

[To be added based on Hardy-Littlewood literature and relevant experimental mathematics papers]
