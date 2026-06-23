# The Geometric Origin of Prime Gap Asymmetry

[![ArXiv](https://img.shields.io/badge/arXiv-[ID]-b31b1b.svg)](https://arxiv.org/abs/[ID])
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![DOI](https://img.shields.io/badge/DOI-[DOI]-blue.svg)](https://doi.org/[DOI])

**Preprint:** *The Geometric Origin of Residue-Class Gap Asymmetry in Sparse Arithmetic Point Processes*  
**Author:** Thomas Hoffbauer  
**Date:** June 23, 2026

---

## 🎯 Abstract

We identify the observed residue-class gap asymmetry in consecutive primes modulo 12 as a **universal consequence of geometric gap statistics** rather than a uniquely prime-specific phenomenon.

**Key Result:** For Poisson processes with acceptance probability $p$:

$$R = (1-p)^{-6}$$

where $R = P(g \equiv 2,4 \bmod 12) / P(g \equiv 8,10 \bmod 12)$. Our data and model analyses suggest this geometric origin accounts for a substantial portion of the observed asymmetry in primes.

**Empirical Hierarchy (N=100,000):**

$$R_{\text{Poisson}} \approx 1.83 \quad > \quad R_{\text{Prime}} = 1.58 \quad > \quad R_{\text{Cramér}} \approx 1.36$$

**Interpretation:** Our results suggest primes occupy a regime of **structured disorder** — an equilibrium between maximal Poisson chaos and overdamped Cramér order.

---

## 📄 Paper

- **Full Paper:** [`paper_geometric_origin.pdf`](output/pdf/paper_geometric_origin.pdf) (8 pages)
- **ArXiv:** [arXiv:[ID]](https://arxiv.org/abs/[ID]) (to be uploaded)
- **Journal:** Submitted to *Experimental Mathematics*

---

## 🚀 Quick Start

### Prerequisites

- C++17 compiler (g++ or clang++)
- Make
- (Optional) LaTeX for reproducing the paper

### Clone and Build

```bash
git clone https://github.com/[username]/prime-gap-asymmetry.git
cd prime-gap-asymmetry
make all
```

### Run Core Analyses

```bash
# Null model hierarchy (the main result)
make demo-poisson-hierarchy

# Verify theoretical formula R = (1-p)^{-6}
./verify_poisson_formula 100000 42

# Gap distribution analysis (real primes)
./gap_distribution 100000

# Transition matrix analysis
./transition_matrix 100000
```

---

## 🔬 Main Results

### 1. Theoretical Formula (Poisson Asymmetry)

**Theorem 1:** For a Poisson process with constant acceptance probability $p$:

$$R_{\text{Poisson}} = \frac{P(G \equiv 2 \text{ or } 4 \bmod 12)}{P(G \equiv 8 \text{ or } 10 \bmod 12)} = (1-p)^{-6}$$

**Derivation:** Geometric gap distribution $P(G=k) = p(1-p)^{k-1}$ gives:

$$P(G \equiv r \bmod 12) = \frac{p q^{r-1}}{1-q^{12}}, \quad q = 1-p$$

Therefore:

$$R = \frac{q^1 + q^3}{q^7 + q^9} = q^{-6}$$

### 2. Empirical Hierarchy (Stable over 10 seeds)

| Model | R_gap | Interpretation |
|-------|-------|----------------|
| **Poisson** | 1.83 ± 0.06 | Short-gap bias (geometric) |
| **Real Primes** | 1.58 (fixed) | Sieve back-correlation |
| **Cramér** | 1.36 ± 0.07 | Logarithmic overdamping |

**Quantitative breakdown:**
- Poisson → Cramér: -28% (log-mixing overdamps)
- Cramér → Prime: +16% (sieve restores)
- Poisson → Prime: -14% (net regularization)

### 3. Interpretation: Structured Disorder

```
Poisson (R≈1.83)  →  [log-mixing]  →  Cramér (R≈1.36)  →  [sieve]  →  Prime (R=1.58)
  Max chaos             Overdamped            Back-correlation    Equilibrium
```

**Three mechanisms:**
1. **Short-gap bias** (geometric): Small residues $r$ favored ($\propto q^{r-1}$)
2. **Logarithmic thinning** (Cramér): Variable $p(n) = 2/\ln(n)$ creates mixing
3. **Sieve back-correlation** (primes): Twins, cousins, sexy primes enhance short gaps

---

## 📂 Repository Structure

```
.
├── paper_geometric_origin.tex        # LaTeX source
├── output/pdf/paper_geometric_origin.pdf
├── README.md                         # This file
├── ARXIV_ABSTRACT.md                 # ArXiv submission info
│
├── src/                              # C++ source files
│   ├── poisson_cramer_hierarchy.cpp # Main null model comparison
│   ├── verify_poisson_formula.cpp   # Formula verification
│   ├── gap_distribution.cpp         # Real prime gap analysis
│   ├── transition_matrix.cpp        # P(a→b) analysis
│   ├── autocorrelation_analysis.cpp # Autocorrelation tests
│   └── ratio_asymptotic.cpp         # R(X) asymptotic behavior
│
├── docs/                             # Extended documentation
│   ├── POISSON_ASYMMETRY_THEORY.md  # Full theoretical derivation
│   ├── NULL_MODEL_HIERARCHY.md      # Empirical hierarchy details
│   ├── GAPS_ANALYSIS.md             # Mechanistic explanation
│   └── CHIRALITY_OBSERVABLES_v2.md  # Original observable formulation
│
├── data/                             # (Not included - generated)
│   └── results/                     # Computation outputs
│
├── Makefile                          # Build system
└── LICENSE                           # MIT License
```

---

## 🔧 Programs

### Core Programs

1. **`poisson_cramer_hierarchy`** ⭐⭐⭐⭐⭐⭐
   - Compares Poisson, Cramér, and real primes
   - Computes gap asymmetry ratio $R$
   - **Usage:** `./poisson_cramer_hierarchy <limit> <seed>`
   - **Output:** Hierarchical comparison table

2. **`verify_poisson_formula`** ⭐⭐⭐⭐⭐⭐⭐
   - Tests theoretical formula $R = (1-p)^{-6}$
   - Systematic test over multiple $p$ values
   - **Usage:** `./verify_poisson_formula <limit> <seed>`
   - **Output:** Empirical vs. theoretical comparison

3. **`gap_distribution`** ⭐⭐⭐⭐
   - Analyzes $P(g \bmod 12 \mid p_n \equiv a)$ for real primes
   - Computes mechanistic formula
   - **Usage:** `./gap_distribution <limit>`
   - **Output:** Full gap distribution matrix

4. **`transition_matrix`** ⭐⭐⭐
   - Computes $P(a \to b)$ transition probabilities
   - Analyzes cyclic structures EABC vs ECBA
   - **Usage:** `./transition_matrix <limit>`
   - **Output:** 4×4 transition matrix

5. **`autocorrelation_analysis`** ⭐⭐⭐
   - Measures $\rho(k) = \text{Corr}(\chi_n, \chi_{n+k})$
   - Effective sample size correction
   - **Usage:** `./autocorrelation_analysis <limit>`
   - **Output:** Autocorrelation function

6. **`ratio_asymptotic`** ⭐⭐⭐⭐⭐
   - Tracks $R(X) = P(\text{EABC})/P(\text{ECBA})$ over scales
   - Tests asymptotic behavior
   - **Usage:** `./ratio_asymptotic`
   - **Output:** R(X) vs. log(X) data

### Build Targets

```bash
make all                    # Build all programs
make poisson-hierarchy      # Build null model comparison
make verify-formula         # Build formula verification
make gap                    # Build gap distribution analyzer
make transition             # Build transition matrix
make autocorr               # Build autocorrelation
make ratio                  # Build asymptotic ratio tracker

make demo-poisson-hierarchy # Run with informative output
make demo-gap               # Demo gap analysis
make clean                  # Remove binaries
make help                   # Show all targets
```

---

## 📊 Key Figures

### Figure 1: Null Model Hierarchy

```
R_gap
  │
1.83├─ Poisson ●━━━━━━━━━━━━━━━┐ Short-gap bias (geometric)
  │                            │
  │                            ▼ -28% (log-mixing)
  │
1.58├─ Prime  ●━━━━━━━━━━━━━━━┐ Structured disorder
  │                            │
  │                            ▼ +16% (sieve)
  │
1.36├─ Cramér ●━━━━━━━━━━━━━━━┘ Overdamped
  │
1.00├─────────────────────────── No asymmetry
```

### Figure 2: Gap Distribution (Real Primes, N=100,000)

| Class | P(g≡2,4) | P(g≡8,10) | Ratio |
|-------|----------|-----------|-------|
| E (1) | 35.0%    | 24.8%     | 1.413 |
| A (5) | 38.4%    | 21.0%     | 1.824 |
| B (7) | 35.6%    | 24.6%     | 1.448 |
| C (11)| 37.3%    | 22.6%     | 1.651 |

**Geometric mean:** R = 1.576

---

## 🧪 Reproducibility

All results are fully reproducible:

```bash
# Clone repository
git clone https://github.com/[username]/prime-gap-asymmetry.git
cd prime-gap-asymmetry

# Build all programs
make all

# Reproduce main results (Table 1 in paper)
./poisson_cramer_hierarchy 100000 42

# Reproduce theoretical verification
./verify_poisson_formula 100000 42

# Reproduce prime gap analysis
./gap_distribution 100000
```

**Expected runtime:** ~5 minutes total on modern hardware (2020+ CPU)

**System requirements:**
- C++17 compiler
- ~500MB RAM
- ~1GB disk space (for binaries)

---

## 📖 Documentation

### Full Theory

See [`POISSON_ASYMMETRY_THEORY.md`](docs/POISSON_ASYMMETRY_THEORY.md) for:
- Complete mathematical derivation
- Geometric gap distribution formula
- Why Cramér overdamps (mixing effect)
- Why primes restore (sieve back-correlation)
- Connection to Hardy-Littlewood conjectures

### Empirical Details

See [`NULL_MODEL_HIERARCHY.md`](docs/NULL_MODEL_HIERARCHY.md) for:
- Implementation details
- Robustness testing (10 seeds)
- Sample size statistics
- Detailed gap distributions

### Mechanistic Explanation

See [`GAPS_ANALYSIS.md`](docs/GAPS_ANALYSIS.md) for:
- Fundamental relation: $b \equiv a + g \pmod{12}$
- EABC cycle: gaps {4,2,4,2}
- ECBA cycle: gaps {8,10,8,10}
- Quantitative mechanistic formula

---

## 🔗 Related Work

### Prime Gap Distribution

- Cramér (1936): Random model for prime gaps
- Maier (1985): Primes in short intervals
- Rubinstein-Sarnak (1994): Chebyshev bias
- Granville-Martin (2006): Prime number races

### Geometric Insight

- **This work:** Gap asymmetry from geometric distribution
- **Novel contribution:** Exact formula $R = (1-p)^{-6}$
- **Novel finding:** Cramér model overdamps (not observed before)

---

## 🎓 Citation

If you use this code or results in your research, please cite:

```bibtex
@article{hoffbauer2026geometric,
  title={The Geometric Origin of Residue-Class Gap Asymmetry in Sparse Arithmetic Point Processes},
  author={Hoffbauer, Thomas},
  journal={arXiv preprint arXiv:[ID]},
  year={2026}
}
```

---

## 📧 Contact

**Author:** Thomas Hoffbauer  
**Email:** [email]  
**ArXiv:** [Profile URL]  
**GitHub:** [username]

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Inspired by classical work on prime gaps (Cramér, Hardy-Littlewood)
- Modern perspective from prime race theory (Rubinstein-Sarnak, Granville-Martin)
- Connection to Collatz conjecture noted (dynamical systems on modular lattices)

---

## 🚀 Future Work

### Short-term
- ⭕ Modulo 30 generalization (8 residue classes)
- ⭕ Modified Cramér with sieve (quantify sieve contribution)
- ⭕ Larger N (10^6, 10^7) for asymptotic behavior

### Long-term
- ⭕ Hardy-Littlewood connection (k-tuple conjectures)
- ⭕ Spectral analysis of transition matrix
- ⭕ Connection to Collatz dynamics (formalize the parallel)

---

**Preprint ready. Code available. Results reproducible.**

*June 23, 2026*
