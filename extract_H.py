#!/usr/bin/env python3
"""
Extraction of Projection-Invariant Object H(Δr)
================================================

After correlation analysis showed ρ=0.965 for Δr ≤ 18,
we now extract the common object H(Δr) from the projections A_i(Δr).

Model: A_i(Δr) = c_i · H(Δr) + ε_i(Δr)

This script:
1. Computes H(Δr) = mean(A_2, A_4, A_6, A_8) for Δr ≤ 18
2. Determines projection coefficients c_i
3. Validates the decomposition quality
4. Updates Stage 4 verdict
"""

import numpy as np
from scipy.stats import pearsonr
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt

# Data from gap_pair_robustness test (N=100000, 5 seeds)
data = {
    2: [0.933, 0.772, 0.668, 0.962],
    6: [0.481, 0.496, 0.505, 0.680],
    10: [0.363, 0.351, 0.452, 0.523],
    14: [0.326, 0.270, 0.276, 0.445],
    18: [0.199, 0.230, 0.243, 0.294],
    22: [0.175, 0.152, 0.356, 1.094],  # Outlier regime
    24: [0.142, 0.275, 0.732, 2.078],  # Outlier regime
}

bases = [2, 4, 6, 8]
delta_r_robust = [2, 6, 10, 14, 18]  # Regime I: Projection-invariant
delta_r_outlier = [22, 24]  # Regime II: Projection-dependent

print("=" * 80)
print("EXTRACTION OF PROJECTION-INVARIANT OBJECT H(Δr)")
print("=" * 80)
print()

# Extract H(Δr) for robust range
A_robust = np.array([data[dr] for dr in delta_r_robust])
H = np.mean(A_robust, axis=1)

print("REGIME I: Δr ≤ 18 (Projection-Invariant)")
print("-" * 60)
print()
print("Extracted H(Δr):")
print()
print("  Δr    H(Δr)   Interpretation")
print("  " + "-" * 45)
for i, dr in enumerate(delta_r_robust):
    interpretation = ""
    if dr == 2:
        interpretation = "← Twin-prime enhancement"
    elif H[i] > 0.4:
        interpretation = "← Short-gap bias"
    elif H[i] < 0.3:
        interpretation = "← Suppression regime"
    print(f"  {dr:2d}    {H[i]:.3f}   {interpretation}")

print()
print("H(Δr) properties:")
print(f"  - Monotonically decreasing: {all(H[i] > H[i+1] for i in range(len(H)-1))}")
print(f"  - H(2) / H(18) ratio: {H[0] / H[-1]:.2f} (strong Δr-dependence)")
print()

# Compute projection coefficients c_i
print("=" * 80)
print("PROJECTION COEFFICIENTS c_i")
print("=" * 80)
print()

c = []
for j, base in enumerate(bases):
    A_j = A_robust[:, j]
    c_j = np.mean(A_j / H)
    c.append(c_j)
    print(f"Base {base}: c_{base} = {c_j:.3f}")

print()
print("Interpretation:")
c_mean = np.mean(c)
c_std = np.std(c)
print(f"  Mean: {c_mean:.3f}")
print(f"  Std:  {c_std:.3f}")
print(f"  CV:   {100*c_std/c_mean:.1f}%")

if c_std / c_mean < 0.15:
    print("  → Coefficients nearly identical → H is canonical!")
elif c_std / c_mean < 0.35:
    print("  → Moderate variation → Projection effect exists but small")
else:
    print("  → Large variation → Projection-dependent scaling")

print()

# Validate decomposition: A_i ≈ c_i · H
print("=" * 80)
print("DECOMPOSITION QUALITY: A_i(Δr) ≈ c_i · H(Δr)")
print("=" * 80)
print()

for j, base in enumerate(bases):
    A_j = A_robust[:, j]
    A_j_predicted = c[j] * H
    residuals = A_j - A_j_predicted
    
    rmse = np.sqrt(np.mean(residuals**2))
    mae = np.mean(np.abs(residuals))
    rel_error = mae / np.mean(A_j)
    corr, _ = pearsonr(A_j, A_j_predicted)
    
    print(f"Base {base}:")
    print(f"  RMSE: {rmse:.4f}")
    print(f"  MAE:  {mae:.4f}")
    print(f"  Relative error: {100*rel_error:.1f}%")
    print(f"  Correlation: ρ = {corr:.4f}")
    
    if rel_error < 0.05:
        print(f"  → Excellent fit!")
    elif rel_error < 0.15:
        print(f"  → Good fit")
    else:
        print(f"  → Moderate fit")
    print()

# Mean decomposition quality
all_A = A_robust.flatten()
all_A_pred = np.array([c[j] * H for j in range(len(bases))]).flatten()
overall_corr, _ = pearsonr(all_A, all_A_pred)
overall_rel_error = np.mean(np.abs(all_A - all_A_pred)) / np.mean(all_A)

print("-" * 60)
print(f"Overall decomposition quality:")
print(f"  ρ(A_observed, c·H): {overall_corr:.4f}")
print(f"  Mean relative error: {100*overall_rel_error:.1f}%")
print()

# Updated Stage 4 verdict
print("=" * 80)
print("UPDATED STAGE 4 VERDICT")
print("=" * 80)
print()

if overall_corr > 0.95 and overall_rel_error < 0.15:
    verdict = "✓ PASSED (restricted domain)"
    stage_status = "PASSED"
else:
    verdict = "~ PARTIAL"
    stage_status = "PARTIAL"

print(f"Projection Invariance (Δr ≤ 18): {verdict}")
print()

if stage_status == "PASSED":
    print("Interpretation:")
    print("  → H(Δr) is projection-invariant for Δr ≤ 18")
    print("  → A_i(Δr) = c_i · H(Δr) with <15% error")
    print("  → H(Δr) qualifies as mathematical object (Regime I)")
    print()
    print("Status:")
    print("  ✓ Stage 1: Existence")
    print("  ✓ Stage 2: Reproducibility")
    print("  ✓ Stage 3: Model Independence")
    print("  ✓ Stage 4: Projection Invariance (Δr ≤ 18)")
    print("  ? Stage 5: Theoretical Connectability (Hardy-Littlewood)")
    print("  ? Stage 6: Autonomy")
    print()
    print("Scientific conclusion:")
    print("  H(Δr) is a well-defined mathematical object characterizing")
    print("  the arithmetic amplification of short-to-medium range")
    print("  gap asymmetries in prime numbers.")
    print()
    print("Caveat:")
    print("  Domain restricted to Δr ≤ 18")
    print("  Regime II (Δr ≥ 20) requires separate treatment")

print()
print("=" * 80)

# Generate plot
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Extraction of H(Δr): Projection-Invariant Object', fontsize=14, fontweight='bold')

# Plot 1: All projections + H
ax = axes[0, 0]
for j, base in enumerate(bases):
    ax.plot(delta_r_robust, A_robust[:, j], 'o-', label=f'A_{base}(Δr)', alpha=0.6)
ax.plot(delta_r_robust, H, 's-', color='black', linewidth=2, markersize=8, label='H(Δr) = mean')
ax.set_xlabel('Δr')
ax.set_ylabel('Amplification')
ax.set_title('(a) Projections A_i(Δr) and extracted H(Δr)')
ax.legend()
ax.grid(True, alpha=0.3)

# Plot 2: Decomposition quality
ax = axes[0, 1]
for j, base in enumerate(bases):
    A_j = A_robust[:, j]
    A_j_pred = c[j] * H
    ax.scatter(A_j, A_j_pred, label=f'Base {base}', alpha=0.6, s=50)
ax.plot([0, 1], [0, 1], 'k--', alpha=0.5, label='Perfect fit')
ax.set_xlabel('A_i(Δr) observed')
ax.set_ylabel('c_i · H(Δr) predicted')
ax.set_title(f'(b) Decomposition quality (ρ={overall_corr:.3f})')
ax.legend()
ax.grid(True, alpha=0.3)

# Plot 3: Residuals
ax = axes[1, 0]
for j, base in enumerate(bases):
    A_j = A_robust[:, j]
    A_j_pred = c[j] * H
    residuals = A_j - A_j_pred
    ax.plot(delta_r_robust, residuals, 'o-', label=f'Base {base}', alpha=0.6)
ax.axhline(0, color='black', linestyle='--', alpha=0.5)
ax.set_xlabel('Δr')
ax.set_ylabel('Residual: A_i - c_i·H')
ax.set_title('(c) Residuals ε_i(Δr) = A_i - c_i·H')
ax.legend()
ax.grid(True, alpha=0.3)

# Plot 4: Projection coefficients
ax = axes[1, 1]
ax.bar(range(len(bases)), c, color=['blue', 'green', 'orange', 'red'], alpha=0.7)
ax.axhline(np.mean(c), color='black', linestyle='--', label=f'Mean = {np.mean(c):.3f}')
ax.set_xticks(range(len(bases)))
ax.set_xticklabels([f'Base {b}' for b in bases])
ax.set_ylabel('Projection coefficient c_i')
ax.set_title(f'(d) Projection coefficients (CV={100*c_std/c_mean:.1f}%)')
ax.legend()
ax.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('H_extraction_analysis.png', dpi=150, bbox_inches='tight')
print(f"Plot saved: H_extraction_analysis.png")
print()

# Save H(Δr) to file
with open('H_delta_r.txt', 'w') as f:
    f.write("# Projection-Invariant Object H(Δr)\n")
    f.write("# Extracted from A_2, A_4, A_6, A_8 projections\n")
    f.write("# Domain: Δr ≤ 18 (Regime I)\n")
    f.write("# Format: Δr  H(Δr)  [standard_error]\n")
    f.write("#\n")
    for i, dr in enumerate(delta_r_robust):
        std_err = np.std(A_robust[i, :]) / np.sqrt(len(bases))
        f.write(f"{dr:2d}  {H[i]:.4f}  {std_err:.4f}\n")

print("H(Δr) saved to: H_delta_r.txt")
print()
print("=" * 80)
print("NEXT STEPS")
print("=" * 80)
print()
print("1. Analyze Regime II (Δr ≥ 20) separately")
print("2. Connect H(Δr) to Hardy-Littlewood constants (Stage 5)")
print("3. Test H(Δr) on different moduli (30, 60, 210)")
print("4. Update OBJECT_CRITERIA.md with restricted-domain result")
print("5. Document the two-regime structure")

