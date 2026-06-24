#!/usr/bin/env python3
"""
Complete H(Δr) Extraction and Analysis
======================================

Berechnet projektionsinvariantes H(Δr) für Δr ≤ 18 mit:
- H(Δr) = mean(A_2, A_4, A_6, A_8)
- Standardabweichung über Projektionen
- Variationskoeffizient CV
- Projektionskoeffizienten c_i
- Residuen ε_i(Δr)
"""

import numpy as np
from scipy.stats import pearsonr
import sys

# Data from gap_pair_robustness test (N=100000, 5 seeds)
# Format: delta_r: [A_2, A_4, A_6, A_8]
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
delta_r_regime_I = [2, 6, 10, 14, 18]
delta_r_regime_II = [22, 24]

print("=" * 80)
print("VOLLSTÄNDIGE H(Δr)-EXTRAKTION")
print("=" * 80)
print()

# ============================================================================
# REGIME I: Δr ≤ 18 (Projection-Invariant)
# ============================================================================

print("REGIME I: Δr ≤ 18 (Projektionsinvariant)")
print("=" * 80)
print()

# Compute H(Δr) and statistics
H_values = []
std_values = []
cv_values = []

print("Δr    H(Δr)   Std    CV(%)   Interpretation")
print("-" * 70)

for dr in delta_r_regime_I:
    A_vals = np.array(data[dr])
    H = np.mean(A_vals)
    std = np.std(A_vals, ddof=1)  # Sample std
    cv = 100 * std / H if H > 0 else 0
    
    H_values.append(H)
    std_values.append(std)
    cv_values.append(cv)
    
    # Interpretation
    if dr == 2:
        interp = "Twin-Prime-Enhancement"
    elif H > 0.5:
        interp = "Strong Short-Gap-Bias"
    elif H > 0.35:
        interp = "Moderate Short-Gap-Bias"
    elif H > 0.25:
        interp = "Weak Enhancement"
    else:
        interp = "Suppression"
    
    print(f"{dr:2d}    {H:.3f}   {std:.3f}  {cv:5.1f}   {interp}")

print()
print(f"Mean CV (Δr ≤ 18): {np.mean(cv_values):.1f}%")
print()

# ============================================================================
# PROJECTION COEFFICIENTS c_i
# ============================================================================

print("=" * 80)
print("PROJEKTIONSKOEFFIZIENTEN c_i")
print("=" * 80)
print()

# Compute c_i for each projection
A_matrix = np.array([data[dr] for dr in delta_r_regime_I])
H_array = np.array(H_values)

c_values = []
print("Base   c_i     Interpretation")
print("-" * 50)

for j, base in enumerate(bases):
    A_j = A_matrix[:, j]
    # c_i = mean(A_i / H) over Δr ≤ 18
    c_j = np.mean(A_j / H_array)
    c_values.append(c_j)
    
    if c_j > 1.1:
        interp = "Hohe Amplifikation"
    elif c_j > 0.95:
        interp = "Nahe Durchschnitt"
    elif c_j > 0.85:
        interp = "Leicht reduziert"
    else:
        interp = "Niedrige Amplifikation"
    
    print(f"{base:4d}   {c_j:.3f}   {interp}")

print()
print(f"Mean:  {np.mean(c_values):.3f}")
print(f"Std:   {np.std(c_values, ddof=1):.3f}")
print(f"CV:    {100*np.std(c_values, ddof=1)/np.mean(c_values):.1f}%")
print()

# ============================================================================
# DECOMPOSITION QUALITY
# ============================================================================

print("=" * 80)
print("DEKOMPOSITIONSQUALITÄT: A_i(Δr) = c_i · H(Δr) + ε_i(Δr)")
print("=" * 80)
print()

print("Base   RMSE    MAE     Rel.Err(%)   ρ         Qualität")
print("-" * 70)

for j, base in enumerate(bases):
    A_j = A_matrix[:, j]
    A_j_pred = c_values[j] * H_array
    
    residuals = A_j - A_j_pred
    rmse = np.sqrt(np.mean(residuals**2))
    mae = np.mean(np.abs(residuals))
    rel_err = 100 * mae / np.mean(A_j)
    corr, _ = pearsonr(A_j, A_j_pred)
    
    if rel_err < 5:
        quality = "Exzellent"
    elif rel_err < 12:
        quality = "Gut"
    elif rel_err < 20:
        quality = "Moderat"
    else:
        quality = "Schwach"
    
    print(f"{base:4d}   {rmse:.4f}  {mae:.4f}  {rel_err:8.1f}     {corr:.4f}    {quality}")

print()

# ============================================================================
# RESIDUALS TABLE
# ============================================================================

print("=" * 80)
print("RESIDUEN ε_i(Δr) = A_i(Δr) - c_i · H(Δr)")
print("=" * 80)
print()

print("Δr     Base 2   Base 4   Base 6   Base 8   |  Max |ε|")
print("-" * 70)

max_residuals = []
for i, dr in enumerate(delta_r_regime_I):
    residuals_row = []
    for j, base in enumerate(bases):
        epsilon = A_matrix[i, j] - c_values[j] * H_array[i]
        residuals_row.append(epsilon)
    
    max_abs_res = max(abs(r) for r in residuals_row)
    max_residuals.append(max_abs_res)
    
    print(f"{dr:2d}    {residuals_row[0]:7.3f}  {residuals_row[1]:7.3f}  {residuals_row[2]:7.3f}  {residuals_row[3]:7.3f}   {max_abs_res:7.3f}")

print()
print(f"Mean max |ε|: {np.mean(max_residuals):.3f}")
print(f"Max  max |ε|: {np.max(max_residuals):.3f}")
print()

# ============================================================================
# REGIME II: Δr ≥ 20 (Outlier Regime)
# ============================================================================

print("=" * 80)
print("REGIME II: Δr ≥ 20 (Projektionssensitiv / Outlier)")
print("=" * 80)
print()

print("Δr     A_2      A_4      A_6      A_8      Mean    Std     CV(%)")
print("-" * 80)

for dr in delta_r_regime_II:
    A_vals = np.array(data[dr])
    mean_val = np.mean(A_vals)
    std_val = np.std(A_vals, ddof=1)
    cv_val = 100 * std_val / mean_val if mean_val > 0 else 0
    
    print(f"{dr:2d}    {A_vals[0]:7.3f}  {A_vals[1]:7.3f}  {A_vals[2]:7.3f}  {A_vals[3]:7.3f}  {mean_val:6.3f}  {std_val:6.3f}  {cv_val:6.1f}")

print()
print("Interpretation:")
print("  → CV >> 30% für beide Δr")
print("  → Keine projektionsrobuste Struktur")
print("  → Separater physikalischer Mechanismus")
print()

# ============================================================================
# FINAL TABLE FOR PUBLICATION
# ============================================================================

print("=" * 80)
print("PUBLIKATIONSTABELLE: H(Δr) für Regime I")
print("=" * 80)
print()

print("Table 1: Projection-Invariant Core Structure H(Δr)")
print()
print("  Δr    H(Δr)    σ_H    CV_H(%)   Projections: A_2, A_4, A_6, A_8")
print("  " + "-" * 75)

for i, dr in enumerate(delta_r_regime_I):
    A_vals = data[dr]
    print(f"  {dr:2d}    {H_values[i]:.3f}   {std_values[i]:.3f}   {cv_values[i]:5.1f}     "
          f"{A_vals[0]:.3f}, {A_vals[1]:.3f}, {A_vals[2]:.3f}, {A_vals[3]:.3f}")

print()
print("Projection coefficients:")
for j, base in enumerate(bases):
    print(f"  c_{base} = {c_values[j]:.3f}")
print()
print(f"Mean CV_H: {np.mean(cv_values):.1f}%  (robust!)")
print()

# ============================================================================
# VERDICT
# ============================================================================

print("=" * 80)
print("STAGE 4 VERDICT")
print("=" * 80)
print()

mean_cv_regime_I = np.mean(cv_values)

if mean_cv_regime_I < 20:
    verdict = "✓ PASSED"
    status = "Projektionsinvariant"
else:
    verdict = "~ PARTIAL"
    status = "Moderate Projektionsabhängigkeit"

print(f"Regime I (Δr ≤ 18): {verdict}")
print(f"  Mean CV_H = {mean_cv_regime_I:.1f}%")
print(f"  Status: {status}")
print()
print("Regime II (Δr ≥ 20): ✗ NOT PASSED")
print("  CV > 60%")
print("  Status: Projektionssensitiv")
print()
print("=" * 80)
print("GESAMTVERDIKT:")
print()
print("  H(Δr) ist ein projektionsinvariantes mathematisches Objekt")
print("  für den Bereich Δr ∈ {2, 6, 10, 14, 18}.")
print()
print("  Dekomposition: A_i(Δr) = c_i · H(Δr) + ε_i(Δr)")
print("  mit <12% mittlerem Fehler.")
print()
print("  Stage 4: PARTIALLY PASSED (restricted domain)")
print("=" * 80)

# Save detailed results to file
with open('H_complete_analysis.txt', 'w') as f:
    f.write("# Complete H(Δr) Analysis\n")
    f.write("# Regime I: Δr ≤ 18 (Projection-Invariant)\n")
    f.write("#\n")
    f.write("# Δr   H(Δr)   σ_H    CV_H(%)   A_2     A_4     A_6     A_8\n")
    for i, dr in enumerate(delta_r_regime_I):
        A_vals = data[dr]
        f.write(f"{dr:3d}  {H_values[i]:.4f}  {std_values[i]:.4f}  {cv_values[i]:6.2f}  "
                f"{A_vals[0]:.4f}  {A_vals[1]:.4f}  {A_vals[2]:.4f}  {A_vals[3]:.4f}\n")
    f.write("#\n")
    f.write("# Projection Coefficients:\n")
    for j, base in enumerate(bases):
        f.write(f"# c_{base} = {c_values[j]:.4f}\n")
    f.write("#\n")
    f.write(f"# Mean CV_H = {mean_cv_regime_I:.2f}%\n")

print()
print("Detailed results saved to: H_complete_analysis.txt")

