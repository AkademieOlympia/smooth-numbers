# ArXiv Submission Abstract

**Title:** The Geometric Origin of Residue-Class Gap Asymmetry in Sparse Arithmetic Point Processes

**Authors:** Thomas Hoffbauer

**Abstract:**

We study the conditional gap distribution $P(g \bmod 12 \mid p_n \equiv a)$ for consecutive primes in residue classes modulo 12 and observe a systematic asymmetry: $P(g \equiv 2,4 \mid a) > P(g \equiv 8,10 \mid a)$ for all four non-trivial residue classes $a \in \{1, 5, 7, 11\}$.

We identify the residue-class gap asymmetry as a universal consequence of geometric gap statistics rather than a uniquely prime-specific phenomenon. For Poisson processes with acceptance probability $p$, we derive the exact formula $R = (1-p)^{-6}$, where $R$ is the ratio of gap probabilities. Our data and model analyses suggest that this geometric origin accounts for a substantial portion of the observed asymmetry in primes.

Empirical comparison with three null models reveals an unexpected hierarchy: $R_{\text{Poisson}} \approx 1.83 > R_{\text{Prime}} = 1.58 > R_{\text{Cramér}} \approx 1.36$. This indicates that the naive Cramér model (logarithmic acceptance $p(n) = 2/\ln(n)$) overdamps the asymmetry through mixing, while real primes exhibit back-correlation from sieve structure (twin, cousin, and sexy prime clustering) that partially restores the geometric short-gap bias.

Our results suggest that primes occupy a regime of structured disorder — an equilibrium between maximal Poisson chaos and overdamped Cramér order, where arithmetic correlations tune the balance between sparsity-induced asymmetry and logarithmic regularization.

---

## ArXiv Categories

**Primary:** math.NT (Number Theory)

**Secondary:** 
- math.PR (Probability)
- math.DS (Dynamical Systems)

---

## MSC 2020 Classification

**Primary:** 11N05 (Distribution of primes)

**Secondary:**
- 11N13 (Primes in progressions)
- 60G55 (Point processes)
- 11K99 (Probabilistic number theory)

---

## Keywords

Prime gaps, residue classes, Poisson process, Cramér model, gap asymmetry, geometric distribution, sparse point processes, sieve theory, Hardy-Littlewood conjecture

---

## Comments (for ArXiv)

8 pages, 1 table. Preprint. For code and data, see: [GitHub repository URL]

---

## Submission Checklist

✅ **Title:** Clear and descriptive  
✅ **Abstract:** Self-contained, <1920 characters  
✅ **Keywords:** Comprehensive  
✅ **MSC codes:** Appropriate  
✅ **References:** Complete (5 citations)  
✅ **Length:** 8 pages (appropriate for preprint)  
✅ **Figures:** None needed (empirical table included)  
✅ **Theorems:** Properly numbered and stated  
✅ **Code availability:** GitHub link in comments

---

## Suggested Journals (after ArXiv)

### Tier 1 (Top journals)
1. **Experimental Mathematics** - Perfect fit (computational + theory)
2. **Journal of Number Theory** - Traditional venue for prime gap studies
3. **Proceedings of the AMS** - Short format, rigorous

### Tier 2 (Excellent specialized journals)
4. **International Journal of Number Theory**
5. **Integers: Electronic Journal of Combinatorial Number Theory**
6. **The Ramanujan Journal**

### Tier 3 (Interdisciplinary)
7. **Chaos, Solitons & Fractals** (dynamical systems angle)
8. **Physica A** (statistical mechanics connection)

**Recommendation:** Start with **Experimental Mathematics** — perfect match for computational discovery + theoretical explanation.

---

## Cover Letter Draft

Dear Editors,

We submit for your consideration the manuscript "The Geometric Origin of Residue-Class Gap Asymmetry in Sparse Arithmetic Point Processes" for publication in [Journal Name].

This work addresses a classical question in analytic number theory: the local distribution of prime gaps in residue classes. We observe that consecutive primes modulo 12 exhibit systematic asymmetries in their gap distribution, with P(g≡2,4) > P(g≡8,10) for all starting classes.

The key contribution is showing that this phenomenon is NOT primarily prime-specific but arises from the geometric nature of gap distributions in sparse point processes. We derive the exact formula R = (1-p)^{-6} for Poisson processes and demonstrate through comparison with null models (Poisson, Cramér, real primes) that primes occupy an intermediate "structured disorder" regime.

This bridges classical analytic number theory (Hardy-Littlewood, Cramér) with modern stochastic point process theory, offering new perspectives on prime gap patterns. The results are fully reproducible with code available on GitHub.

We believe this work will be of interest to researchers in analytic number theory, probabilistic number theory, and computational mathematics.

Sincerely,
Thomas Hoffbauer

---

## Potential Reviewers

1. **Andrew Granville** (Université de Montréal) - Expert on prime races
2. **Greg Martin** (University of British Columbia) - Prime gap distributions
3. **Terence Tao** (UCLA) - Analytic number theory, Cramér model
4. **Kannan Soundararajan** (Stanford) - Distribution of primes
5. **James Maynard** (Oxford) - Recent work on prime gaps

(Note: Check journal policy on reviewer suggestions)

---

## Timeline

- **June 23, 2026:** Preprint created
- **June 24-30, 2026:** Internal review, final polishing
- **Early July 2026:** ArXiv submission
- **Mid July 2026:** Journal submission (Experimental Mathematics)
- **Expected review:** 2-3 months
- **Revisions:** ~1 month
- **Publication:** Q4 2026 or Q1 2027

---

## Data Availability Statement

All computational results are reproducible. Source code (C++17), analysis scripts, and raw data are available at: [GitHub repository URL]. The repository includes:

- C++ implementations of all three null models
- Gap distribution analysis tools
- Verification of theoretical formula R = (1-p)^{-6}
- Complete documentation and build instructions

---

## Author Contribution Statement

T.H. conceived the study, derived the theoretical results, performed all computations, and wrote the manuscript.

---

## Competing Interests

The author declares no competing interests.

---

## Funding

[If applicable]

---

**Preprint ready for submission.**  
**Date:** June 23, 2026
