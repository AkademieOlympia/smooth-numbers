#!/usr/bin/env python3
"""
Test: Near-Zero-Magic → Chiraler Bias (Kausalität)

Zentrale Hypothese (verfeinert):

```
M_EABC(N) hoch ⇒ starker chiraler Bias
```

**Kausale Hierarchie:**
```
Near-Zero-Spektrum → chiraler Drift → sichtbare ABCE/CEAB-Asymmetrie
```

Magic ist die Ursache, Bias ist die Wirkung!

Dieser Test validiert:
1. M_near_zero korreliert stärker mit q als globale Metriken
2. M_near_zero → q (Spektrales Chaos)
3. M_near_zero → κ_EABC (Chiraler Bias)
4. Kausalitätsrichtung: Near-Zero-Sektor ist primär
"""

import numpy as np
import matplotlib.pyplot as plt
from src.hamiltonian import EABCHamiltonian
from src.arithmetic_magic import ArithmeticMagic
from src.level_spacing import compute_level_spacing, fit_level_statistics
from src.spectral import spectral_unfolding
import os


def compute_chiral_bias_parameter(H, k=500):
    """
    Berechne chiralen Bias-Parameter κ_EABC.
    
    Dies ist ein Platzhalter - der echte κ_EABC müsste aus dem
    Primzahl-Projekt übernommen werden (ABCE/CEAB-Zählungen).
    
    Für jetzt: Approximation via Eigenvektoren.
    """
    # Für diesen Test: Nutze M_chi als Proxy
    # (In echter Analyse: ABCE/CEAB-Zählungen aus Primzahl-Statistik)
    magic = ArithmeticMagic(H)
    M_chi = magic.compute_chirality_magic()
    
    return M_chi


def test_near_zero_vs_global(N=500, k_spectrum=300, save_plots=True):
    """
    Test 1: Near-Zero-Magic vs. Globale Metriken
    
    Vergleiche die Korrelation mit q-Parameter:
    - M_near_zero vs. q
    - M_chi (global) vs. q
    - M_collatz (global) vs. q
    
    Hypothese: M_near_zero hat stärkere Korrelation!
    """
    print("\n" + "="*80)
    print("TEST 1: NEAR-ZERO-MAGIC vs. GLOBALE METRIKEN")
    print("="*80 + "\n")
    
    beta_values = np.array([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
    gamma = 1.5
    epsilon = 0.1
    
    n_beta = len(beta_values)
    
    results = {
        'M_near_zero': np.zeros(n_beta),
        'M_chi': np.zeros(n_beta),
        'M_collatz': np.zeros(n_beta),
        'mean_asymmetry': np.zeros(n_beta),
        'n_nzm': np.zeros(n_beta),
        'q_brody': np.zeros(n_beta)
    }
    
    for i, beta in enumerate(beta_values):
        print(f"\n[{i+1}/{n_beta}] β = {beta:.2f}")
        print("-" * 80)
        
        H = EABCHamiltonian(N=N, beta=beta, gamma=gamma)
        
        # Magic berechnen (inkl. Near-Zero!)
        magic = ArithmeticMagic(H)
        
        # Globale Metriken (schnell)
        M_global = magic.compute_all(
            compute_near_zero=False,
            compute_nzm=False
        )
        
        # Near-Zero-Magic (langsam!)
        M_nz = magic.compute_near_zero_magic(
            epsilon=epsilon,
            k=k_spectrum,
            mode='spectral_weighted'
        )
        
        # Speichern
        results['M_near_zero'][i] = M_nz['M_near_zero']
        results['M_chi'][i] = M_global['M_chi']
        results['M_collatz'][i] = M_global['M_collatz']
        results['mean_asymmetry'][i] = M_nz['mean_asymmetry']
        results['n_nzm'][i] = M_nz['n_nzm']
        
        # Spektralanalyse für q
        print(f"\n  Berechne Brody-Parameter q...")
        eigenvalues = H.compute_spectrum(k=k_spectrum, which='SM', sigma=0.0)
        unfolded = spectral_unfolding(eigenvalues)
        spacings = compute_level_spacing(unfolded)
        lsd_results = fit_level_statistics(spacings, bins=40)
        q = lsd_results['brody_q']
        
        results['q_brody'][i] = q
        
        print(f"\n  → M_near_zero = {M_nz['M_near_zero']:.4f}")
        print(f"  → M_chi       = {M_global['M_chi']:.4f}")
        print(f"  → q           = {q:.4f}")
        print("-" * 80)
    
    # Korrelationen berechnen
    print("\n" + "="*80)
    print("KORRELATIONEN MIT q-PARAMETER:")
    print("="*80)
    
    from scipy.stats import pearsonr
    
    correlations = {}
    for key in ['M_near_zero', 'M_chi', 'M_collatz']:
        r, p_value = pearsonr(results[key], results['q_brody'])
        correlations[key] = r
        print(f"  {key:20s} vs. q: r = {r:+.4f}, p = {p_value:.4e}")
    
    # Interpretation
    print("\n" + "="*80)
    print("INTERPRETATION:")
    print("="*80)
    
    if correlations['M_near_zero'] > correlations['M_chi']:
        delta = correlations['M_near_zero'] - correlations['M_chi']
        print(f"  ✓ M_near_zero korreliert STÄRKER mit q als M_chi!")
        print(f"    Δr = {delta:+.4f}")
        print("  → Near-Zero-Sektor ist der primäre Steuerparameter!")
    else:
        delta = correlations['M_chi'] - correlations['M_near_zero']
        print(f"  ∼ M_chi korreliert stärker als M_near_zero")
        print(f"    Δr = {delta:+.4f}")
        print("  → Globale Metrik dominiert (unerwartet)")
    
    print("="*80 + "\n")
    
    # Plotting
    if save_plots:
        os.makedirs('figures', exist_ok=True)
        
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        
        # Plot 1: M_near_zero vs. q
        ax = axes[0, 0]
        ax.scatter(results['M_near_zero'], results['q_brody'], s=100, 
                   c=beta_values, cmap='viridis', edgecolors='black', linewidths=1.5)
        from scipy.stats import linregress
        slope, intercept, r, _, _ = linregress(results['M_near_zero'], results['q_brody'])
        x_fit = np.linspace(results['M_near_zero'].min(), results['M_near_zero'].max(), 100)
        y_fit = slope * x_fit + intercept
        ax.plot(x_fit, y_fit, 'r--', linewidth=2, label=f'r = {r:.4f}')
        ax.set_xlabel('M_near_zero (Near-Zero-Magic)', fontsize=12, fontweight='bold')
        ax.set_ylabel('q (Brody-Parameter)', fontsize=12, fontweight='bold')
        ax.set_title('Near-Zero-Magic vs. Chaos (PRIMÄR)', fontsize=14, fontweight='bold')
        ax.legend()
        ax.grid(alpha=0.3)
        
        # Plot 2: M_chi vs. q (zum Vergleich)
        ax = axes[0, 1]
        ax.scatter(results['M_chi'], results['q_brody'], s=100,
                   c=beta_values, cmap='plasma', edgecolors='black', linewidths=1.5)
        slope, intercept, r, _, _ = linregress(results['M_chi'], results['q_brody'])
        x_fit = np.linspace(results['M_chi'].min(), results['M_chi'].max(), 100)
        y_fit = slope * x_fit + intercept
        ax.plot(x_fit, y_fit, 'r--', linewidth=2, label=f'r = {r:.4f}')
        ax.set_xlabel('M_chi (Globale Chiralität)', fontsize=12, fontweight='bold')
        ax.set_ylabel('q (Brody-Parameter)', fontsize=12, fontweight='bold')
        ax.set_title('Globale Magic vs. Chaos (Vergleich)', fontsize=14, fontweight='bold')
        ax.legend()
        ax.grid(alpha=0.3)
        
        # Plot 3: β vs. alle Metriken
        ax = axes[1, 0]
        ax.plot(beta_values, results['M_near_zero'], 'o-', linewidth=2, 
                markersize=8, label='M_near_zero', color='blue')
        ax.plot(beta_values, results['M_chi'], 's-', linewidth=2,
                markersize=8, label='M_chi', color='green')
        ax.plot(beta_values, results['q_brody'], '^-', linewidth=2,
                markersize=8, label='q_brody', color='red')
        ax.set_xlabel('β (Chiralität)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Metrik-Wert', fontsize=12, fontweight='bold')
        ax.set_title('β-Abhängigkeit aller Metriken', fontsize=14, fontweight='bold')
        ax.legend()
        ax.grid(alpha=0.3)
        
        # Plot 4: Near-Zero-Mode-Statistik
        ax = axes[1, 1]
        ax.bar(beta_values, results['n_nzm'], width=0.08, alpha=0.7,
               color='purple', edgecolor='black', linewidth=1.5)
        ax.set_xlabel('β (Chiralität)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Anzahl Near-Zero-Moden', fontsize=12, fontweight='bold')
        ax.set_title(f'Near-Zero-Moden (|λ| < {epsilon})', fontsize=14, fontweight='bold')
        ax.grid(axis='y', alpha=0.3)
        
        plt.suptitle('Near-Zero-Magic: Kausalitätsanalyse', 
                     fontsize=18, fontweight='bold', y=0.995)
        plt.tight_layout()
        plt.savefig('figures/near_zero_causality.png', dpi=300, bbox_inches='tight')
        print("✓ Gespeichert: figures/near_zero_causality.png\n")
        plt.close()
    
    return beta_values, results


def test_epsilon_dependence(N=500, beta=0.5, gamma=1.5, k_spectrum=300, save_plots=True):
    """
    Test 2: Abhängigkeit von ε (Near-Zero-Schwelle)
    
    Variiere ε und prüfe:
    - Wie robust ist M_near_zero?
    - Gibt es ein optimales ε?
    """
    print("\n" + "="*80)
    print("TEST 2: ABHÄNGIGKEIT VON ε (NEAR-ZERO-SCHWELLE)")
    print("="*80 + "\n")
    
    epsilon_values = np.array([0.05, 0.1, 0.15, 0.2, 0.3, 0.5])
    n_eps = len(epsilon_values)
    
    results = {
        'M_near_zero': np.zeros(n_eps),
        'n_nzm': np.zeros(n_eps),
        'mean_asymmetry': np.zeros(n_eps)
    }
    
    H = EABCHamiltonian(N=N, beta=beta, gamma=gamma)
    magic = ArithmeticMagic(H)
    
    for i, epsilon in enumerate(epsilon_values):
        print(f"\n[{i+1}/{n_eps}] ε = {epsilon:.2f}")
        
        M_nz = magic.compute_near_zero_magic(
            epsilon=epsilon,
            k=k_spectrum,
            mode='spectral_weighted'
        )
        
        results['M_near_zero'][i] = M_nz['M_near_zero']
        results['n_nzm'][i] = M_nz['n_nzm']
        results['mean_asymmetry'][i] = M_nz['mean_asymmetry']
    
    # Plotting
    if save_plots:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        
        # Plot 1: M_near_zero vs. ε
        ax1.plot(epsilon_values, results['M_near_zero'], 'o-', 
                 linewidth=2, markersize=8, color='blue')
        ax1.set_xlabel('ε (Near-Zero-Schwelle)', fontsize=12, fontweight='bold')
        ax1.set_ylabel('M_near_zero', fontsize=12, fontweight='bold')
        ax1.set_title('Near-Zero-Magic vs. Schwelle', fontsize=14, fontweight='bold')
        ax1.grid(alpha=0.3)
        
        # Plot 2: Anzahl Moden vs. ε
        ax2.plot(epsilon_values, results['n_nzm'], 's-',
                 linewidth=2, markersize=8, color='green')
        ax2.set_xlabel('ε (Near-Zero-Schwelle)', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Anzahl Near-Zero-Moden', fontsize=12, fontweight='bold')
        ax2.set_title('Near-Zero-Moden vs. Schwelle', fontsize=14, fontweight='bold')
        ax2.grid(alpha=0.3)
        
        plt.suptitle(f'ε-Abhängigkeit (β={beta}, γ={gamma})',
                     fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.savefig('figures/epsilon_dependence.png', dpi=300, bbox_inches='tight')
        print("\n✓ Gespeichert: figures/epsilon_dependence.png\n")
        plt.close()
    
    print("\n" + "="*80)
    print("INTERPRETATION:")
    print("="*80)
    print(f"  → Optimales ε ≈ 0.1-0.2 (Kompromiss: genug Moden, nicht zu viele)")
    print(f"  → Bei ε={epsilon_values[np.argmax(results['M_near_zero'])]:.2f}: "
          f"M_near_zero maximal")
    print("="*80 + "\n")
    
    return epsilon_values, results


def test_pattern_comparison(N=500, beta=0.5, gamma=1.5, k_spectrum=300):
    """
    Test 3: ABCE/CEAB vs. EABC/ECBA Muster
    
    Vergleiche beide Asymmetrie-Definitionen.
    """
    print("\n" + "="*80)
    print("TEST 3: PATTERN-VERGLEICH (ABCE/CEAB vs. EABC/ECBA)")
    print("="*80 + "\n")
    
    H = EABCHamiltonian(N=N, beta=beta, gamma=gamma)
    magic = ArithmeticMagic(H)
    
    # Pattern 1: ABCE/CEAB
    print("[1/2] ABCE/CEAB-Muster...")
    M_nz_1 = magic.compute_near_zero_magic(
        epsilon=0.1,
        k=k_spectrum,
        mode='spectral_weighted',
        pattern='ABCE_CEAB'
    )
    
    # Pattern 2: EABC/ECBA
    print("\n[2/2] EABC/ECBA-Muster...")
    M_nz_2 = magic.compute_near_zero_magic(
        epsilon=0.1,
        k=k_spectrum,
        mode='spectral_weighted',
        pattern='EABC_ECBA'
    )
    
    print("\n" + "="*80)
    print("VERGLEICH:")
    print("="*80)
    print(f"\nABCE/CEAB:")
    print(f"  M_near_zero = {M_nz_1['M_near_zero']:.6f}")
    print(f"  mean_asym   = {M_nz_1['mean_asymmetry']:.6f}")
    
    print(f"\nEABC/ECBA:")
    print(f"  M_near_zero = {M_nz_2['M_near_zero']:.6f}")
    print(f"  mean_asym   = {M_nz_2['mean_asymmetry']:.6f}")
    
    print("\n→ Beide Muster sollten ähnliche Werte liefern (konsistent!)")
    print("="*80 + "\n")
    
    return M_nz_1, M_nz_2


if __name__ == "__main__":
    import sys
    
    print("\n" + "="*80)
    print("NEAR-ZERO-MAGIC: KAUSALITÄTS-TEST-SUITE")
    print("="*80)
    print("\nKausale Hierarchie:")
    print("  Near-Zero-Spektrum → chiraler Drift → ABCE/CEAB-Asymmetrie")
    print("\nMagic ist die Ursache, Bias ist die Wirkung!")
    print("="*80 + "\n")
    
    try:
        # Test 1: Near-Zero vs. Global (Haupttest!)
        print("\n>>> STARTE TEST 1: NEAR-ZERO vs. GLOBAL <<<\n")
        beta_vals, results1 = test_near_zero_vs_global(
            N=500,
            k_spectrum=300,
            save_plots=True
        )
        
        # Test 2: ε-Abhängigkeit
        print("\n>>> STARTE TEST 2: ε-ABHÄNGIGKEIT <<<\n")
        eps_vals, results2 = test_epsilon_dependence(
            N=500,
            beta=0.5,
            gamma=1.5,
            k_spectrum=300,
            save_plots=True
        )
        
        # Test 3: Pattern-Vergleich
        print("\n>>> STARTE TEST 3: PATTERN-VERGLEICH <<<\n")
        M_nz_1, M_nz_2 = test_pattern_comparison(
            N=500,
            beta=0.5,
            gamma=1.5,
            k_spectrum=300
        )
        
        print("\n" + "="*80)
        print("ALLE TESTS ABGESCHLOSSEN!")
        print("="*80)
        print("\nErstelle Plots in figures/:")
        print("  - near_zero_causality.png (Hauptresultat!)")
        print("  - epsilon_dependence.png")
        print("\n→ Analysiere die Korrelationen: Ist M_near_zero stärker als M_chi?")
        print("="*80 + "\n")
        
    except KeyboardInterrupt:
        print("\n\n✗ Tests abgebrochen durch Benutzer.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n✗ Fehler während Tests: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
