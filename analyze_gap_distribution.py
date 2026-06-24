#!/usr/bin/env python3
"""
Empirical Gap Distribution Analysis - Statistical Comparison
=============================================================

Analysiert die Korrelation zwischen H_emp und H_HL,emp
mit empirisch rekonstruierten Gap-Gewichten.
"""

import numpy as np
from scipy.stats import pearsonr, spearmanr
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Results from gap_distribution_analysis.cpp
data = {
    'delta_r': [2, 6, 10, 14],
    'H_emp': [0.834, 0.540, 0.422, 0.329],
    'H_HL_emp': [2.711, 3.404, 4.967, 7.686],
}

delta_r = np.array(data['delta_r'])
H_emp = np.array(data['H_emp'])
H_HL_emp = np.array(data['H_HL_emp'])

print("=" * 80)
print("EMPIRICAL GAP DISTRIBUTION - STATISTICAL ANALYSIS")
print("=" * 80)
print()

# Raw comparison
print("RAW COMPARISON")
print("-" * 60)
print("Δr    H_emp    H_HL,emp    Ratio")
print("-" * 60)
for i in range(len(delta_r)):
    ratio = H_emp[i] / H_HL_emp[i]
    print(f"{delta_r[i]:2d}    {H_emp[i]:.3f}    {H_HL_emp[i]:.3f}      {ratio:.3f}")
print()

# Compute scaling factor (ignoring Δr=18)
ratios = H_emp / H_HL_emp
mean_ratio = np.mean(ratios)
H_HL_emp_scaled = mean_ratio * H_HL_emp

print(f"Optimal scaling factor: c = {mean_ratio:.4f}")
print()

# Scaled comparison
print("SCALED COMPARISON (c · H_HL,emp)")
print("-" * 60)
print("Δr    H_emp    c·H_HL,emp   Residual")
print("-" * 60)
residuals = H_emp - H_HL_emp_scaled
for i in range(len(delta_r)):
    print(f"{delta_r[i]:2d}    {H_emp[i]:.3f}    {H_HL_emp_scaled[i]:.3f}      {residuals[i]:7.3f}")
print()

# Statistical comparison
corr_pearson, p_pearson = pearsonr(H_emp, H_HL_emp)
corr_spearman, p_spearman = spearmanr(H_emp, H_HL_emp)
corr_log, p_log = pearsonr(np.log(H_emp), np.log(H_HL_emp))

rmse = np.sqrt(np.mean(residuals**2))
mae = np.mean(np.abs(residuals))
rel_error = mae / np.mean(H_emp)

print("=" * 80)
print("STATISTICAL METRICS")
print("=" * 80)
print()
print(f"Pearson correlation:     ρ = {corr_pearson:7.4f}  (p = {p_pearson:.4f})")
print(f"Spearman correlation:    ρ = {corr_spearman:7.4f}  (p = {p_spearman:.4f})")
print(f"Log-space correlation:   ρ = {corr_log:7.4f}  (p = {p_log:.4f})")
print()
print(f"RMSE (scaled):           {rmse:.4f}")
print(f"MAE (scaled):            {mae:.4f}")
print(f"Relative error:          {100*rel_error:.1f}%")
print()

# Interpretation
print("=" * 80)
print("INTERPRETATION")
print("=" * 80)
print()

if corr_pearson > 0:
    print(f"✓ POSITIVE correlation: ρ = {corr_pearson:.3f}")
    print()
    if corr_pearson > 0.9:
        compat = "STRONG"
        interp = "H(Δr) structure is highly compatible with empirical HL"
    elif corr_pearson > 0.7:
        compat = "MODERATE"
        interp = "H(Δr) shows partial agreement with empirical HL"
    else:
        compat = "WEAK"
        interp = "H(Δr) shows weak agreement with empirical HL"
    
    print(f"Compatibility: {compat}")
    print(f"  {interp}")
    print()
    print(f"Scaling factor: c = {mean_ratio:.4f}")
    print(f"  H_HL,emp values need to be scaled down by factor ~{1/mean_ratio:.1f}")
    print()
    
    if rel_error < 0.15:
        print(f"  Relative error {100*rel_error:.1f}% suggests good quantitative agreement")
    elif rel_error < 0.30:
        print(f"  Relative error {100*rel_error:.1f}% suggests moderate quantitative agreement")
    else:
        print(f"  Relative error {100*rel_error:.1f}% suggests weak quantitative agreement")
else:
    print(f"✗ NEGATIVE correlation: ρ = {corr_pearson:.3f}")
    print()
    print("Interpretation:")
    print("  Even with empirical Gap weights, H(Δr) shows negative correlation")
    print("  with Hardy-Littlewood predictions.")
    print()
    print("  This suggests:")
    print("    - H(Δr) is NOT simply related to HL pair-gap constants")
    print("    - A different theoretical framework is needed")
    print("    - Or: H(Δr) involves higher-order correlations")

print()
print("WICHTIG:")
print("  Dies ist ein empirischer Kompatibilitätstest.")
print("  Positive Korrelation → HL-Struktur ist relevant")
print("  Negative Korrelation → H(Δr) liegt auf anderer Ebene")
print()

# Check monotonicity
H_emp_mono = all(H_emp[i] > H_emp[i+1] for i in range(len(H_emp)-1))
H_HL_emp_mono = all(H_HL_emp[i] > H_HL_emp[i+1] for i in range(len(H_HL_emp)-1))

print("=" * 80)
print("MONOTONICITY CHECK")
print("=" * 80)
print()
print(f"H_emp monotonically decreasing:     {H_emp_mono}  ✓" if H_emp_mono else f"H_emp monotonically decreasing:     {H_emp_mono}  ✗")
print(f"H_HL,emp monotonically decreasing:  {H_HL_emp_mono}  ✓" if H_HL_emp_mono else f"H_HL,emp monotonically decreasing:  {H_HL_emp_mono}  ✗")
print()

if not H_HL_emp_mono:
    print("PROBLEM: H_HL,emp is NOT monotonic!")
    print("  This suggests the HL pair-gap model is incomplete.")
    print("  Possible reasons:")
    print("    - Gap mixing effects not captured")
    print("    - Higher-order correlations needed")
    print("    - Different HL formulation required")
    print()

# Stage 5 Verdict
print("=" * 80)
print("STAGE 5 VERDICT (Empirical Gap Weights)")
print("=" * 80)
print()

if corr_pearson > 0.85 and rel_error < 0.20:
    verdict = "✓ PASSED"
    status = "H(Δr) compatible with HL structure"
    next_step = "Refine theoretical model, proceed to Stage 6"
elif corr_pearson > 0.5 or (corr_pearson > 0 and rel_error < 0.35):
    verdict = "~ PARTIAL"
    status = "Partial HL compatibility"
    next_step = "Investigate deviations, refine model"
else:
    verdict = "✗ NOT PASSED"
    status = "H(Δr) not compatible with simple HL model"
    next_step = "Alternative theoretical framework needed"

print(f"Verdict: {verdict}")
print(f"  ρ = {corr_pearson:.3f}")
print(f"  Relative error = {100*rel_error:.1f}%")
print(f"  Status: {status}")
print()
print(f"Next step: {next_step}")
print()

# Generate plots
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Empirical Gap Distribution Analysis', fontsize=14, fontweight='bold')

# Plot 1: H_emp vs H_HL,emp (raw)
ax = axes[0, 0]
ax.plot(delta_r, H_emp, 'o-', label='H_emp (observed)', linewidth=2, markersize=8)
ax.plot(delta_r, H_HL_emp, 's--', label='H_HL,emp (empirical gaps)', linewidth=2, markersize=8, alpha=0.7)
ax.set_xlabel('Δr')
ax.set_ylabel('H(Δr)')
ax.set_title(f'(a) H_emp vs H_HL,emp (raw, ρ={corr_pearson:.3f})')
ax.legend()
ax.grid(True, alpha=0.3)

# Plot 2: H_emp vs c·H_HL,emp (scaled)
ax = axes[0, 1]
ax.plot(delta_r, H_emp, 'o-', label='H_emp', linewidth=2, markersize=8)
ax.plot(delta_r, H_HL_emp_scaled, 's--', label=f'c·H_HL,emp (c={mean_ratio:.3f})', linewidth=2, markersize=8, alpha=0.7)
ax.set_xlabel('Δr')
ax.set_ylabel('H(Δr)')
ax.set_title(f'(b) H_emp vs c·H_HL,emp (scaled)')
ax.legend()
ax.grid(True, alpha=0.3)

# Plot 3: Correlation plot
ax = axes[1, 0]
ax.scatter(H_HL_emp_scaled, H_emp, s=100, alpha=0.6)
for i in range(len(delta_r)):
    ax.annotate(f'Δr={delta_r[i]}', (H_HL_emp_scaled[i], H_emp[i]), fontsize=9, ha='right')
lim_max = max(max(H_emp), max(H_HL_emp_scaled))
ax.plot([0, lim_max], [0, lim_max], 'k--', alpha=0.5, label='Perfect agreement')
ax.set_xlabel('c·H_HL,emp (predicted)')
ax.set_ylabel('H_emp (observed)')
ax.set_title(f'(c) Correlation (ρ={corr_pearson:.3f})')
ax.legend()
ax.grid(True, alpha=0.3)

# Plot 4: Residuals
ax = axes[1, 1]
ax.bar(range(len(delta_r)), residuals, color='red', alpha=0.6)
ax.axhline(0, color='black', linestyle='--', alpha=0.5)
ax.set_xticks(range(len(delta_r)))
ax.set_xticklabels([f'Δr={dr}' for dr in delta_r])
ax.set_ylabel('Residual: H_emp - c·H_HL,emp')
ax.set_title(f'(d) Residuals (MAE={mae:.3f})')
ax.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('gap_distribution_analysis.png', dpi=150, bbox_inches='tight')
print("Plot saved: gap_distribution_analysis.png")
print()
print("=" * 80)

