#!/usr/bin/env python3
"""
Quick Test: M_arith vs q Korrelation (MINIMAL VERSION)

Vereinfachter Test mit kleinem System für schnelle Validierung.
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import sys

# Füge src zum Path hinzu
sys.path.insert(0, str(Path(__file__).parent))

from src.hamiltonian import CollatzEABCHamiltonian
from src.level_spacing import compute_level_spacing, fit_level_statistics
from src.spectral import spectral_unfolding
from src.arithmetic_magic import ArithmeticMagic

# Konfiguration
N = 500  # Kleineres System für schnellen Test
K = 200  # Weniger Eigenwerte
GAMMA_VALUES = np.array([0.5, 1.0, 1.5, 2.0])  # Weniger Punkte

print("="*80)
print(" "*20 + "QUICK TEST: M_ARITH VS Q KORRELATION")
print("="*80)
print(f"\nSystem: N = {N}, k = {K}")
print(f"Parameter-Sweep: gamma ∈ {GAMMA_VALUES}")
print("="*80 + "\n")

# Ergebnis-Arrays
results = {
    'gamma': GAMMA_VALUES,
    'M_near_zero': np.zeros(len(GAMMA_VALUES)),
    'n_nzm': np.zeros(len(GAMMA_VALUES)),
    'brody_q': np.zeros(len(GAMMA_VALUES)),
    'sigma': np.zeros(len(GAMMA_VALUES))
}

for i, gamma in enumerate(GAMMA_VALUES):
    print(f"\n[{i+1}/{len(GAMMA_VALUES)}] γ = {gamma:.2f}")
    print("-" * 80)
    
    try:
        # Konstruiere Hamiltonian
        print("  [1/4] Konstruiere Hamiltonian...")
        H = CollatzEABCHamiltonian(N=N, gamma=gamma, beta=0.5, alpha=1.0)
        
        # Near-Zero Magic (count mode - schnellster!)
        print("  [2/4] Berechne Near-Zero Magic...")
        magic = ArithmeticMagic(H)
        nz_results = magic.compute_near_zero_magic(
            epsilon=0.1,
            k=K,
            mode='count'  # Schnellster Modus
        )
        
        results['M_near_zero'][i] = nz_results['M_near_zero']
        results['n_nzm'][i] = nz_results['n_nzm']
        
        # Berechne Spektrum
        print("  [3/4] Berechne Spektrum...")
        eigenvalues = H.compute_spectrum(k=K, which='SM', sigma=0.0)
        
        # Unfolding und Level Spacings
        print("  [4/4] Berechne Level Spacings und q...")
        unfolded = spectral_unfolding(eigenvalues)
        spacings = compute_level_spacing(unfolded)
        
        # σ
        sigma = np.std(spacings)
        results['sigma'][i] = sigma
        
        # Brody-q
        try:
            lsd_results = fit_level_statistics(spacings, bins=50)
            q = lsd_results['brody_q']
            if not np.isnan(q) and 0 <= q <= 1:
                results['brody_q'][i] = q
            else:
                results['brody_q'][i] = np.nan
        except:
            results['brody_q'][i] = np.nan
        
        # Ausgabe
        print(f"\n  ERGEBNISSE:")
        print(f"    M_near_zero = {results['M_near_zero'][i]:.6f}")
        print(f"    n_nzm       = {results['n_nzm'][i]:.0f}")
        print(f"    q           = {results['brody_q'][i]:.4f}")
        print(f"    σ           = {results['sigma'][i]:.4f}")
        print("-" * 80)
    
    except Exception as e:
        print(f"  ✗ FEHLER: {e}")
        import traceback
        traceback.print_exc()
        results['M_near_zero'][i] = np.nan
        results['brody_q'][i] = np.nan
        results['sigma'][i] = np.nan

# Korrelationsanalyse
print("\n" + "="*80)
print("KORRELATIONSANALYSE")
print("="*80)

# Filtere NaN-Werte
valid_mask = ~np.isnan(results['brody_q']) & ~np.isnan(results['M_near_zero'])

if np.sum(valid_mask) >= 3:
    corr = np.corrcoef(
        results['M_near_zero'][valid_mask], 
        results['brody_q'][valid_mask]
    )[0, 1]
    
    print(f"\nKorrelation M_near_zero vs q: r = {corr:+.4f}")
    
    if abs(corr) > 0.7:
        print(f"\n✓✓✓ STARKE KORRELATION: |r| = {abs(corr):.3f} > 0.7")
        print(f"    → Arithmetische Magic als Steuerparameter BESTÄTIGT!")
    elif abs(corr) > 0.5:
        print(f"\n✓✓ MODERATE KORRELATION: |r| = {abs(corr):.3f} > 0.5")
        print(f"   → Hinweise auf Zusammenhang")
    elif abs(corr) > 0.3:
        print(f"\n✓ SCHWACHE KORRELATION: |r| = {abs(corr):.3f} > 0.3")
        print(f"  → Tendenzieller Zusammenhang")
    else:
        print(f"\n✗ KEINE KORRELATION: |r| = {abs(corr):.3f} < 0.3")
else:
    print("\n✗ Zu wenige gültige Datenpunkte!")
    corr = np.nan

print("="*80 + "\n")

# Plot
print("Erstelle Plot...")
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Panel 1: M_near_zero vs q
ax1 = axes[0]
ax1.plot(results['M_near_zero'][valid_mask], results['brody_q'][valid_mask], 
         'o-', markersize=10, linewidth=2)
ax1.set_xlabel(r'$M_{\mathrm{near\_zero}}$', fontsize=12)
ax1.set_ylabel(r'Brody-Parameter $q$', fontsize=12)
ax1.set_title('Near-Zero Magic vs. Chaos', fontsize=13, fontweight='bold')
ax1.grid(True, alpha=0.3)

if not np.isnan(corr):
    ax1.text(0.05, 0.95, f'r = {corr:+.3f}', 
            transform=ax1.transAxes, fontsize=11,
            verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

# Panel 2: gamma vs q
ax2 = axes[1]
ax2.plot(GAMMA_VALUES[valid_mask], results['brody_q'][valid_mask], 
         '^-', markersize=10, linewidth=2, color='C2')
ax2.set_xlabel(r'Parameter $\gamma$', fontsize=12)
ax2.set_ylabel(r'Brody-Parameter $q$', fontsize=12)
ax2.set_title(r'$\gamma$ vs. q', fontsize=13, fontweight='bold')
ax2.grid(True, alpha=0.3)

plt.tight_layout()
output_path = Path(__file__).parent / 'figures' / 'quick_test_magic_correlation.png'
output_path.parent.mkdir(exist_ok=True)
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"✓ Plot gespeichert: {output_path}")
plt.close()

print("\nQUICK TEST ABGESCHLOSSEN!")
print("="*80)
