#!/usr/bin/env python3
"""
Hardy-Littlewood Heuristic for H(Δr)
=====================================

Stage 5: Theoretical Connectability

Testet Kompatibilität von H(Δr) mit Hardy-Littlewood-Singularserien.

NICHT behauptet: "Hardy-Littlewood erklärt H(Δr)"
SONDERN: "Ist H(Δr) mit HL-Singularserien kompatibel?"

Ansatz:
1. Für jedes Δr: Bestimme konkrete Gaps zwischen Residue-Klassen
2. Berechne HL-Singularserie S(g) für diese Gaps
3. Konstruiere H_HL(Δr) = weighted sum of S(g)
4. Vergleiche mit H_emp(Δr): Korrelation, Skalierung
"""

import numpy as np
from scipy.stats import pearsonr
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# ============================================================================
# MODULO-30 RESIDUE SYSTEM
# ============================================================================

# Zulässige Residue-Klassen modulo 30 (coprime to 30 = 2·3·5)
residues_mod30 = [1, 7, 11, 13, 17, 19, 23, 29]

def residue_to_index(r):
    """Map residue to index 0-7"""
    return residues_mod30.index(r)

def gap_between_residues(r1, r2):
    """
    Minimal gap between residues r1 and r2 modulo 30.
    Returns the smallest positive gap.
    """
    # Direct gap
    gap_forward = (r2 - r1) % 30
    if gap_forward == 0:
        gap_forward = 30
    return gap_forward

# ============================================================================
# HARDY-LITTLEWOOD SINGULAR SERIES
# ============================================================================

def hardy_littlewood_S(g, max_prime=100):
    """
    Berechnet Hardy-Littlewood-Singularserie S(g) für Prime-Pair-Gap g.
    
    S(g) = ∏_p (1 - 1/(p-1)²) · ∏_{p|g} ((p-1)/(p-2))
    
    Für g = 2 (Twin Primes): S(2) ≈ 0.6602 (Twin Prime Constant C_2)
    Für g = 4: S(4) ≈ 1.3204
    Für g = 6 (Sexy Primes): S(6) ≈ 1.3203
    """
    # Product over all primes p
    primes = sieve_primes_simple(max_prime)
    
    # Base product: ∏_p (1 - 1/(p-1)²)
    base_product = 1.0
    for p in primes:
        if p >= 3:  # Skip p=2 for this formula
            base_product *= (1 - 1/(p-1)**2)
    
    # Correction for primes dividing g: ∏_{p|g} ((p-1)/(p-2))
    correction = 1.0
    for p in primes:
        if p >= 3 and g % p == 0:
            correction *= (p - 1) / (p - 2)
    
    S_g = base_product * correction
    
    # Known values for validation:
    # S(2) ≈ 0.6602 (Twin Prime Constant)
    # S(6) ≈ 1.3203
    
    return S_g

def sieve_primes_simple(N):
    """Simple Sieve of Eratosthenes"""
    if N < 2:
        return []
    is_prime = [True] * (N + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(N**0.5) + 1):
        if is_prime[i]:
            for j in range(i*i, N + 1, i):
                is_prime[j] = False
    return [i for i in range(N + 1) if is_prime[i]]

# ============================================================================
# GAP ENUMERATION FOR Δr
# ============================================================================

def enumerate_gaps_for_delta_r(delta_r):
    """
    Für gegebenes Δr: Welche konkreten Gaps g treten auf?
    
    Gap-Pair-Definition (Base 2 als Beispiel):
      Low:  {2, 4, 6} mod 30 → Residues {1, 7, 11, 13, 17, 19, 23, 29}
      High: {2+Δr, 4+Δr, 6+Δr}
    
    Wir betrachten alle Paare (r_low, r_high) mit Abstand Δr zwischen
    aufeinanderfolgenden Residue-Klassen.
    """
    gaps = []
    
    # Alle Paare von Residuen
    for r1 in residues_mod30:
        for r2 in residues_mod30:
            gap = gap_between_residues(r1, r2)
            # Check if this gap corresponds to Δr modulo structure
            # Simplified: Take gaps that are "near" Δr
            # This is heuristic - exact mapping depends on modular structure
            if abs(gap - delta_r) <= 6:  # Within reasonable range
                gaps.append(gap)
    
    return sorted(set(gaps))

def compute_gap_weights_for_delta_r(delta_r):
    """
    Für Δr: Gewichte für verschiedene Gaps basierend auf Häufigkeit
    in den Gap-Pair-Projektionen.
    
    Vereinfachte Heuristik:
    - Gaps nahe Δr bekommen höheres Gewicht
    - Twin-gaps (2) haben universell hohes Gewicht für kleine Δr
    """
    gaps = enumerate_gaps_for_delta_r(delta_r)
    weights = {}
    
    total_weight = 0
    for g in gaps:
        # Weight inversely proportional to distance from delta_r
        w = 1.0 / (1 + abs(g - delta_r))
        weights[g] = w
        total_weight += w
    
    # Normalize
    for g in weights:
        weights[g] /= total_weight
    
    return weights

# ============================================================================
# CONSTRUCT H_HL(Δr) FROM HARDY-LITTLEWOOD
# ============================================================================

def compute_H_HL(delta_r):
    """
    Konstruiere H_HL(Δr) aus Hardy-Littlewood-Singularserien.
    
    H_HL(Δr) ≈ ∑_g w_g(Δr) · S(g)
    """
    gap_weights = compute_gap_weights_for_delta_r(delta_r)
    
    H_HL = 0.0
    for g, w in gap_weights.items():
        S_g = hardy_littlewood_S(g)
        H_HL += w * S_g
    
    return H_HL

# ============================================================================
# COMPARISON: H_emp vs H_HL
# ============================================================================

# Empirical H(Δr) from extraction
H_emp_data = {
    2: 0.834,
    6: 0.540,
    10: 0.422,
    14: 0.329,
    18: 0.241,
}

delta_r_values = sorted(H_emp_data.keys())

print("=" * 80)
print("HARDY-LITTLEWOOD HEURISTIC FOR H(Δr)")
print("=" * 80)
print()
print("Stage 5: Theoretical Connectability Test")
print()

# Compute H_HL for all Δr
H_HL_values = []
H_emp_values = []

print("Δr    H_emp    H_HL     Ratio    Gap weights")
print("-" * 80)

for dr in delta_r_values:
    H_emp = H_emp_data[dr]
    H_HL = compute_H_HL(dr)
    ratio = H_emp / H_HL if H_HL > 0 else 0
    
    H_emp_values.append(H_emp)
    H_HL_values.append(H_HL)
    
    gap_weights = compute_gap_weights_for_delta_r(dr)
    top_gaps = sorted(gap_weights.items(), key=lambda x: x[1], reverse=True)[:3]
    gap_str = ", ".join([f"g={g}({w:.2f})" for g, w in top_gaps])
    
    print(f"{dr:2d}    {H_emp:.3f}   {H_HL:.3f}   {ratio:.3f}    {gap_str}")

print()

# ============================================================================
# STATISTICAL COMPARISON
# ============================================================================

H_emp_array = np.array(H_emp_values)
H_HL_array = np.array(H_HL_values)

# Correlation
corr_pearson, p_pearson = pearsonr(H_emp_array, H_HL_array)
corr_log_pearson, p_log_pearson = pearsonr(np.log(H_emp_array), np.log(H_HL_array))

# Optimal scaling factor
scaling_factor = np.mean(H_emp_array / H_HL_array)
H_HL_scaled = scaling_factor * H_HL_array

# Residuals
residuals = H_emp_array - H_HL_scaled
rmse = np.sqrt(np.mean(residuals**2))
mae = np.mean(np.abs(residuals))
rel_error = mae / np.mean(H_emp_array)

print("=" * 80)
print("STATISTICAL COMPARISON: H_emp vs H_HL")
print("=" * 80)
print()

print(f"Pearson correlation:     ρ = {corr_pearson:.4f}  (p = {p_pearson:.4f})")
print(f"Log-space correlation:   ρ = {corr_log_pearson:.4f}  (p = {p_log_pearson:.4f})")
print()
print(f"Optimal scaling factor:  c = {scaling_factor:.4f}")
print(f"RMSE (scaled):           {rmse:.4f}")
print(f"MAE (scaled):            {mae:.4f}")
print(f"Relative error:          {100*rel_error:.1f}%")
print()

# ============================================================================
# INTERPRETATION
# ============================================================================

print("=" * 80)
print("INTERPRETATION")
print("=" * 80)
print()

if corr_pearson > 0.9:
    compat_verdict = "✓ STRONG compatibility"
    interp = "H(Δr) structure is highly compatible with HL predictions"
elif corr_pearson > 0.7:
    compat_verdict = "~ MODERATE compatibility"
    interp = "H(Δr) shows partial agreement with HL predictions"
else:
    compat_verdict = "✗ WEAK compatibility"
    interp = "H(Δr) structure differs significantly from HL predictions"

print(f"Compatibility: {compat_verdict}")
print()
print(f"  {interp}")
print()

if rel_error < 0.15:
    print(f"  Relative error {100*rel_error:.1f}% suggests good quantitative agreement")
    print(f"  after scaling by factor c = {scaling_factor:.3f}")
elif rel_error < 0.30:
    print(f"  Relative error {100*rel_error:.1f}% suggests moderate quantitative agreement")
else:
    print(f"  Relative error {100*rel_error:.1f}% suggests weak quantitative agreement")

print()
print("WICHTIG:")
print("  Dies ist KEIN Beweis, dass HL H(Δr) erklärt.")
print("  Es ist ein Kompatibilitätstest:")
print("  Ist H(Δr) mit HL-Struktur konsistent?")
print()

# ============================================================================
# RESIDUAL ANALYSIS
# ============================================================================

print("=" * 80)
print("RESIDUAL ANALYSIS: H_emp - c·H_HL")
print("=" * 80)
print()

print("Δr    H_emp    c·H_HL   Residual   Rel.Res(%)")
print("-" * 60)

for i, dr in enumerate(delta_r_values):
    res = residuals[i]
    rel_res = 100 * res / H_emp_array[i]
    print(f"{dr:2d}    {H_emp_array[i]:.3f}   {H_HL_scaled[i]:.3f}   {res:7.3f}   {rel_res:8.1f}")

print()
print(f"Max absolute residual: {np.max(np.abs(residuals)):.3f} at Δr={delta_r_values[np.argmax(np.abs(residuals))]}")
print()

# ============================================================================
# STAGE 5 VERDICT
# ============================================================================

print("=" * 80)
print("STAGE 5 VERDICT: Theoretical Connectability")
print("=" * 80)
print()

if corr_pearson > 0.85 and rel_error < 0.20:
    verdict = "✓ PASSED"
    stage5_status = "Compatible"
    next_step = "Stage 6 (Autonomy) can proceed"
elif corr_pearson > 0.6 or rel_error < 0.35:
    verdict = "~ PARTIAL"
    stage5_status = "Partially compatible"
    next_step = "Refine HL model or investigate deviations"
else:
    verdict = "✗ NOT PASSED"
    stage5_status = "Incompatible"
    next_step = "Alternative theoretical framework needed"

print(f"Verdict: {verdict}")
print(f"  ρ = {corr_pearson:.3f}")
print(f"  Relative error = {100*rel_error:.1f}%")
print(f"  Status: {stage5_status}")
print()
print(f"Next step: {next_step}")
print()

# ============================================================================
# SAVE RESULTS
# ============================================================================

with open('H_hardy_littlewood_comparison.txt', 'w') as f:
    f.write("# Hardy-Littlewood Heuristic Comparison\n")
    f.write("# Δr   H_emp   H_HL   c·H_HL   Residual\n")
    for i, dr in enumerate(delta_r_values):
        f.write(f"{dr:3d}  {H_emp_array[i]:.4f}  {H_HL_array[i]:.4f}  {H_HL_scaled[i]:.4f}  {residuals[i]:7.4f}\n")
    f.write(f"#\n")
    f.write(f"# Correlation: {corr_pearson:.4f}\n")
    f.write(f"# Scaling factor: {scaling_factor:.4f}\n")
    f.write(f"# Relative error: {100*rel_error:.2f}%\n")

print("Results saved to: H_hardy_littlewood_comparison.txt")
print()

# ============================================================================
# PLOT
# ============================================================================

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Hardy-Littlewood Heuristic for H(Δr)', fontsize=14, fontweight='bold')

# Plot 1: H_emp vs H_HL (raw)
ax = axes[0, 0]
ax.plot(delta_r_values, H_emp_array, 'o-', label='H_emp (empirical)', linewidth=2, markersize=8)
ax.plot(delta_r_values, H_HL_array, 's--', label='H_HL (Hardy-Littlewood)', linewidth=2, markersize=8, alpha=0.7)
ax.set_xlabel('Δr')
ax.set_ylabel('H(Δr)')
ax.set_title(f'(a) H_emp vs H_HL (raw)')
ax.legend()
ax.grid(True, alpha=0.3)

# Plot 2: H_emp vs c·H_HL (scaled)
ax = axes[0, 1]
ax.plot(delta_r_values, H_emp_array, 'o-', label='H_emp', linewidth=2, markersize=8)
ax.plot(delta_r_values, H_HL_scaled, 's--', label=f'c·H_HL (c={scaling_factor:.3f})', linewidth=2, markersize=8, alpha=0.7)
ax.set_xlabel('Δr')
ax.set_ylabel('H(Δr)')
ax.set_title(f'(b) H_emp vs c·H_HL (ρ={corr_pearson:.3f})')
ax.legend()
ax.grid(True, alpha=0.3)

# Plot 3: Correlation plot
ax = axes[1, 0]
ax.scatter(H_HL_scaled, H_emp_array, s=100, alpha=0.6)
for i, dr in enumerate(delta_r_values):
    ax.annotate(f'Δr={dr}', (H_HL_scaled[i], H_emp_array[i]), fontsize=9, ha='right')
ax.plot([0, max(H_emp_array)], [0, max(H_emp_array)], 'k--', alpha=0.5, label='Perfect agreement')
ax.set_xlabel('c·H_HL (predicted)')
ax.set_ylabel('H_emp (observed)')
ax.set_title(f'(c) Correlation (ρ={corr_pearson:.3f}, err={100*rel_error:.1f}%)')
ax.legend()
ax.grid(True, alpha=0.3)

# Plot 4: Residuals
ax = axes[1, 1]
ax.bar(range(len(delta_r_values)), residuals, color='red', alpha=0.6)
ax.axhline(0, color='black', linestyle='--', alpha=0.5)
ax.set_xticks(range(len(delta_r_values)))
ax.set_xticklabels([f'Δr={dr}' for dr in delta_r_values])
ax.set_ylabel('Residual: H_emp - c·H_HL')
ax.set_title(f'(d) Residuals (MAE={mae:.3f})')
ax.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('H_hardy_littlewood_analysis.png', dpi=150, bbox_inches='tight')
print("Plot saved: H_hardy_littlewood_analysis.png")
print()

print("=" * 80)
print("STAGE 5 COMPLETED")
print("=" * 80)

