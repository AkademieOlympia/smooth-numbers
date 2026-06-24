#!/usr/bin/env python3
"""
Correlation Analysis of A(Δr) Projections
==========================================

Analyzes structural similarity between A_2, A_4, A_6, A_8
to determine if a common object H exists.

Input: Results from gap_pair_robustness test
Output: Correlation matrix and interpretation
"""

import numpy as np
from scipy.stats import pearsonr, spearmanr
import sys

# Data from gap_pair_robustness test (N=100000, 5 seeds)
data = {
    2: [0.933, 0.772, 0.668, 0.962],  # Δr=2 for bases 2,4,6,8
    6: [0.481, 0.496, 0.505, 0.680],
    10: [0.363, 0.351, 0.452, 0.523],
    14: [0.326, 0.270, 0.276, 0.445],
    18: [0.199, 0.230, 0.243, 0.294],
    22: [0.175, 0.152, 0.356, 1.094],
    24: [0.142, 0.275, 0.732, 2.078],
}

bases = [2, 4, 6, 8]
delta_r_values = sorted(data.keys())

print("=" * 80)
print("CORRELATION ANALYSIS OF A(Δr) PROJECTIONS")
print("=" * 80)
print()
print("Question: Are A_2, A_4, A_6, A_8 structurally similar?")
print()

# Create matrix form
A = np.array([data[dr] for dr in delta_r_values])
print(f"Data shape: {A.shape[0]} Δr values × {A.shape[1]} base offsets")
print()

# Pairwise correlations
print("PAIRWISE CORRELATIONS")
print("-" * 60)

correlations = []
for i in range(len(bases)):
    for j in range(i + 1, len(bases)):
        values_i = A[:, i]
        values_j = A[:, j]
        
        pearson, p_pearson = pearsonr(values_i, values_j)
        spearman, p_spearman = spearmanr(values_i, values_j)
        
        correlations.append(pearson)
        
        print(f"Base {bases[i]} vs Base {bases[j]}:")
        print(f"  Pearson:  ρ = {pearson:6.3f} (p={p_pearson:.4f})")
        print(f"  Spearman: ρ = {spearman:6.3f} (p={p_spearman:.4f})", end="")
        
        if pearson > 0.8:
            print("  ← STRONG correlation")
        elif pearson > 0.5:
            print("  ← MODERATE correlation")
        elif pearson > 0.2:
            print("  ← WEAK correlation")
        else:
            print("  ← NO correlation")

print("-" * 60)

mean_corr = np.mean(correlations)
print(f"\nMean pairwise correlation: {mean_corr:.3f}")
print(f"Std dev of correlations: {np.std(correlations):.3f}")
print()

# Structural similarity analysis
print("=" * 80)
print("STRUCTURAL SIMILARITY ANALYSIS")
print("=" * 80)
print()

# Check if all curves have similar peaks
peaks = [np.argmax(A[:, i]) for i in range(len(bases))]
print(f"Peak locations (Δr index): {peaks}")
print(f"Peak Δr values: {[delta_r_values[p] for p in peaks]}")

# Check if all curves show monotonic trends in certain regions
print()
print("Monotonicity analysis (Δr=2 to 18):")
for i, base in enumerate(bases):
    values = A[:-2, i]  # Exclude Δr=22,24 (outliers)
    diffs = np.diff(values)
    if all(d <= 0 for d in diffs):
        print(f"  Base {base}: Monotonically DECREASING")
    elif all(d >= 0 for d in diffs):
        print(f"  Base {base}: Monotonically INCREASING")
    else:
        print(f"  Base {base}: NON-MONOTONIC ({sum(d>0 for d in diffs)}/{len(diffs)} increases)")

print()
print("=" * 80)
print("INTERPRETATION")
print("=" * 80)
print()

if mean_corr > 0.75:
    print("✓ STRONG structural similarity detected!")
    print()
    print("Interpretation:")
    print("  → Projections likely arise from common H(Δr)")
    print("  → Model: A_i(Δr) = c_i · H(Δr) + ε_i(Δr)")
    print("  → Despite CV=37.5%, structure is preserved")
    print()
    print("Next steps:")
    print("  1. Extract projection-invariant H(Δr)")
    print("  2. Characterize projection operators P_i")
    print("  3. Test H(Δr) for Stage 4 invariance")
    
elif mean_corr > 0.4:
    print("~ MODERATE structural similarity")
    print()
    print("Interpretation:")
    print("  → Partial common core exists")
    print("  → Model: H_common(Δr) + H_projection(Δr, i)")
    print("  → Some Δr show consistency, others don't")
    print()
    print("Next steps:")
    print("  1. Identify which Δr are robust (Δr=2-18)")
    print("  2. Separate Δr=22-24 as different regime")
    print("  3. Define A(Δr) only for robust range")
    
else:
    print("✗ WEAK or NO structural similarity")
    print()
    print("Interpretation:")
    print("  → No simple common object H")
    print("  → A(Δr) is truly projection-dependent")
    print("  → Current definition insufficient")
    print()
    print("Next steps:")
    print("  1. Reformulate decomposition approach")
    print("  2. Consider alternative observables")
    print("  3. Or: Document failure mode (still valuable)")

print()
print("=" * 80)

# Additional: Test if excluding outliers helps
print()
print("ROBUSTNESS CHECK: Excluding Δr=22,24 outliers")
print("-" * 60)

A_restricted = A[:-2, :]  # Only Δr=2 to 18
correlations_restricted = []

for i in range(len(bases)):
    for j in range(i + 1, len(bases)):
        pearson_r, _ = pearsonr(A_restricted[:, i], A_restricted[:, j])
        correlations_restricted.append(pearson_r)

mean_corr_restricted = np.mean(correlations_restricted)
print(f"Mean correlation (Δr=2-18 only): {mean_corr_restricted:.3f}")

if mean_corr_restricted > mean_corr + 0.15:
    print("→ SIGNIFICANT improvement without outliers!")
    print("→ Suggests: Define A(Δr) only for Δr ≤ 18")
    print("→ Large-Δr regime (≥20) may need separate treatment")
else:
    print("→ Outlier removal doesn't significantly improve correlation")
    print("→ Projection dependence is pervasive")

