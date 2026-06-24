#!/usr/bin/env python3
"""
Test: Arithmetische Magic vs. Quantenchaos

Zentrale Hypothese: M_EABC ↑ ⟹ q_Brody ↑ ⟹ σ(s) → σ_GUE

Dieser Test führt eine systematische Parametervariation durch und misst
die Korrelation zwischen verschiedenen Magic-Maßen und dem Brody-Parameter q.

Falls M_chi stark mit q korreliert (r > 0.9), ist die chirale Kopplung β
der **Steuerparameter** des Chaos-Übergangs!
"""

import numpy as np
import matplotlib.pyplot as plt
from src.hamiltonian import EABCHamiltonian, CollatzEABCHamiltonian
from src.arithmetic_magic import ArithmeticMagic, compute_magic_vs_chaos_correlation
from src.level_spacing import compute_level_spacing, fit_level_statistics
from src.spectral import spectral_unfolding
import os


def test_beta_sweep(N=1000, k=500, save_plots=True):
    """
    Haupttest: β-Sweep (Chiralitäts-Stärke).
    
    Variiere β ∈ [0, 1] und messe:
    - Magic-Maße (M_bias, M_collatz, M_chi, M_gap, M_symbreak)
    - Brody-Parameter q
    - Korrelation zwischen Magic und q
    
    Erwartung:
    - M_chi vs. q: r > 0.9 (sehr starke Korrelation)
    - M_collatz vs. q: r > 0.6 (moderate Korrelation)
    
    Parameters
    ----------
    N : int
        Gittergröße
    k : int
        Anzahl Eigenwerte
    save_plots : bool
        Speichere Plots in figures/
    """
    print("\n" + "="*80)
    print("TEST 1: β-SWEEP (CHIRALITÄTS-STÄRKE)")
    print("="*80 + "\n")
    
    # Parameter
    beta_values = np.array([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
    gamma = 1.5
    
    # Durchführe Korrelationsanalyse
    beta_vals, results = compute_magic_vs_chaos_correlation(
        N=N,
        beta_values=beta_values,
        gamma=gamma,
        k=k
    )
    
    # ===== PLOTTING =====
    
    if save_plots:
        os.makedirs('figures', exist_ok=True)
    
    # Plot 1: M_chi vs. q (Hauptresultat!)
    fig, ax = plt.subplots(figsize=(10, 7))
    
    ax.scatter(results['M_chi'], results['q_brody'], s=100, alpha=0.7, 
               c=beta_vals, cmap='viridis', edgecolors='black', linewidths=1.5)
    
    # Lineare Regression
    from scipy.stats import linregress
    slope, intercept, r_value, p_value, std_err = linregress(results['M_chi'], results['q_brody'])
    
    x_fit = np.linspace(results['M_chi'].min(), results['M_chi'].max(), 100)
    y_fit = slope * x_fit + intercept
    ax.plot(x_fit, y_fit, 'r--', linewidth=2, label=f'Linear Fit: r = {r_value:.4f}')
    
    ax.set_xlabel('M_chi (Chiralitäts-Magic)', fontsize=14, fontweight='bold')
    ax.set_ylabel('q (Brody-Parameter)', fontsize=14, fontweight='bold')
    ax.set_title('Arithmetische Magic vs. Quantenchaos', fontsize=16, fontweight='bold')
    ax.legend(fontsize=12)
    ax.grid(alpha=0.3)
    
    # Colorbar
    cbar = plt.colorbar(ax.collections[0], ax=ax)
    cbar.set_label('β (Chiralität)', fontsize=12)
    
    plt.tight_layout()
    
    if save_plots:
        plt.savefig('figures/magic_vs_chaos_main.png', dpi=300, bbox_inches='tight')
        print("\n✓ Gespeichert: figures/magic_vs_chaos_main.png")
    else:
        plt.show()
    
    plt.close()
    
    # Plot 2: Alle Magic-Maße vs. q (Korrelations-Matrix)
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    axes = axes.flatten()
    
    magic_keys = ['M_bias', 'M_collatz', 'M_chi', 'M_gap', 'M_symbreak']
    
    for i, key in enumerate(magic_keys):
        ax = axes[i]
        
        ax.scatter(results[key], results['q_brody'], s=80, alpha=0.7,
                   c=beta_vals, cmap='plasma', edgecolors='black')
        
        # Lineare Regression
        slope, intercept, r_value, p_value, std_err = linregress(results[key], results['q_brody'])
        x_fit = np.linspace(results[key].min(), results[key].max(), 100)
        y_fit = slope * x_fit + intercept
        ax.plot(x_fit, y_fit, 'r--', linewidth=2, alpha=0.7)
        
        ax.set_xlabel(key, fontsize=12, fontweight='bold')
        ax.set_ylabel('q (Brody)', fontsize=12, fontweight='bold')
        ax.set_title(f'r = {r_value:.4f}', fontsize=14, fontweight='bold')
        ax.grid(alpha=0.3)
    
    # Letzte Subplot: β vs. q direkt
    ax = axes[5]
    ax.plot(beta_vals, results['q_brody'], 'o-', linewidth=2, markersize=8, 
            color='darkblue', alpha=0.7)
    ax.set_xlabel('β (Chiralität)', fontsize=12, fontweight='bold')
    ax.set_ylabel('q (Brody)', fontsize=12, fontweight='bold')
    ax.set_title('β vs. q (direkt)', fontsize=14, fontweight='bold')
    ax.grid(alpha=0.3)
    
    plt.suptitle('Magic-Maße vs. Quantenchaos: Korrelationsanalyse', 
                 fontsize=18, fontweight='bold', y=1.00)
    plt.tight_layout()
    
    if save_plots:
        plt.savefig('figures/magic_correlations_all.png', dpi=300, bbox_inches='tight')
        print("✓ Gespeichert: figures/magic_correlations_all.png")
    else:
        plt.show()
    
    plt.close()
    
    # Plot 3: Magic-Landschaft (β vs. alle Magic-Maße)
    fig, ax = plt.subplots(figsize=(12, 7))
    
    for key in magic_keys:
        ax.plot(beta_vals, results[key], 'o-', linewidth=2, markersize=8, 
                label=key, alpha=0.7)
    
    ax.set_xlabel('β (Chiralität)', fontsize=14, fontweight='bold')
    ax.set_ylabel('Magic-Maß', fontsize=14, fontweight='bold')
    ax.set_title('Magic-Landschaft: Alle Maße vs. β', fontsize=16, fontweight='bold')
    ax.legend(fontsize=12, loc='best')
    ax.grid(alpha=0.3)
    
    plt.tight_layout()
    
    if save_plots:
        plt.savefig('figures/magic_landscape.png', dpi=300, bbox_inches='tight')
        print("✓ Gespeichert: figures/magic_landscape.png")
    else:
        plt.show()
    
    plt.close()
    
    # ===== ZUSAMMENFASSUNG =====
    
    print("\n" + "="*80)
    print("ZUSAMMENFASSUNG: KORRELATIONEN")
    print("="*80)
    
    for key in magic_keys:
        r = np.corrcoef(results[key], results['q_brody'])[0, 1]
        interpretation = "★★★ SEHR STARK" if abs(r) > 0.9 else \
                        "★★ STARK" if abs(r) > 0.7 else \
                        "★ MODERAT" if abs(r) > 0.5 else "SCHWACH"
        print(f"  {key:15s} vs. q: r = {r:+.4f}  [{interpretation}]")
    
    print("\n" + "="*80)
    
    # Hypothese-Test
    r_chi = np.corrcoef(results['M_chi'], results['q_brody'])[0, 1]
    
    print("\nHYPOTHESE-TEST:")
    if r_chi > 0.9:
        print("  ✓ HYPOTHESE BESTÄTIGT!")
        print("    M_chi ist stark mit q korreliert (r > 0.9)")
        print("    → Die chirale Kopplung β ist der Steuerparameter des Chaos-Übergangs!")
    elif r_chi > 0.7:
        print("  ∼ HYPOTHESE TEILWEISE BESTÄTIGT")
        print("    M_chi ist moderat mit q korreliert (r > 0.7)")
        print("    → β spielt eine wichtige Rolle, aber andere Faktoren auch.")
    else:
        print("  ✗ HYPOTHESE NICHT BESTÄTIGT")
        print("    M_chi korreliert schwach mit q (r < 0.7)")
        print("    → β ist NICHT der dominante Steuerparameter.")
    
    print("="*80 + "\n")
    
    return beta_vals, results


def test_gamma_sweep(N=1000, k=500, save_plots=True):
    """
    Test 2: γ-Sweep (Primzahl-Defekt-Stärke).
    
    Variiere γ ∈ [0.5, 3.0] bei festem β = 0.5.
    
    Hypothese: γ sollte weniger Einfluss auf Magic haben als β,
    da γ nur die Amplitude, nicht die Symmetriebrechung beeinflusst.
    
    Parameters
    ----------
    N : int
        Gittergröße
    k : int
        Anzahl Eigenwerte
    save_plots : bool
        Speichere Plots
    """
    print("\n" + "="*80)
    print("TEST 2: γ-SWEEP (PRIMZAHL-DEFEKT-STÄRKE)")
    print("="*80 + "\n")
    
    gamma_values = np.array([0.5, 1.0, 1.5, 2.0, 2.5, 3.0])
    beta = 0.5  # Fest
    
    n_gamma = len(gamma_values)
    
    results = {
        'M_chi': np.zeros(n_gamma),
        'M_collatz': np.zeros(n_gamma),
        'q_brody': np.zeros(n_gamma)
    }
    
    for i, gamma in enumerate(gamma_values):
        print(f"\n[{i+1}/{n_gamma}] γ = {gamma:.2f}")
        print("-" * 80)
        
        H = EABCHamiltonian(N=N, beta=beta, gamma=gamma)
        
        # Magic
        magic = ArithmeticMagic(H)
        M_all = magic.compute_all(compute_nzm=False)
        
        results['M_chi'][i] = M_all['M_chi']
        results['M_collatz'][i] = M_all['M_collatz']
        
        # Chaos
        eigenvalues = H.compute_spectrum(k=k, which='SM', sigma=0.0)
        unfolded = spectral_unfolding(eigenvalues)
        spacings = compute_level_spacing(unfolded)
        lsd_results = fit_level_statistics(spacings, bins=50)
        
        results['q_brody'][i] = lsd_results['brody_q']
        
        print(f"  → M_chi = {M_all['M_chi']:.4f}, q = {lsd_results['brody_q']:.4f}")
    
    # Plotting
    if save_plots:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        
        # Plot 1: γ vs. Magic
        ax1.plot(gamma_values, results['M_chi'], 'o-', linewidth=2, 
                 markersize=8, label='M_chi', color='blue')
        ax1.plot(gamma_values, results['M_collatz'], 's-', linewidth=2, 
                 markersize=8, label='M_collatz', color='green')
        ax1.set_xlabel('γ (Primzahl-Defekt)', fontsize=14, fontweight='bold')
        ax1.set_ylabel('Magic-Maß', fontsize=14, fontweight='bold')
        ax1.set_title('γ vs. Magic (β = 0.5 fest)', fontsize=14, fontweight='bold')
        ax1.legend(fontsize=12)
        ax1.grid(alpha=0.3)
        
        # Plot 2: γ vs. q
        ax2.plot(gamma_values, results['q_brody'], 'o-', linewidth=2, 
                 markersize=8, color='red')
        ax2.set_xlabel('γ (Primzahl-Defekt)', fontsize=14, fontweight='bold')
        ax2.set_ylabel('q (Brody-Parameter)', fontsize=14, fontweight='bold')
        ax2.set_title('γ vs. Quantenchaos (β = 0.5 fest)', fontsize=14, fontweight='bold')
        ax2.grid(alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('figures/gamma_sweep.png', dpi=300, bbox_inches='tight')
        print("\n✓ Gespeichert: figures/gamma_sweep.png")
        plt.close()
    
    # Korrelationen
    r_chi = np.corrcoef(results['M_chi'], results['q_brody'])[0, 1]
    
    print("\n" + "="*80)
    print("ZUSAMMENFASSUNG: γ-SWEEP")
    print("="*80)
    print(f"  M_chi vs. q: r = {r_chi:+.4f}")
    print("\nInterpretation:")
    if abs(r_chi) < 0.3:
        print("  → γ hat WENIG Einfluss auf Magic (wie erwartet!)")
        print("  → γ skaliert nur die Amplitude, nicht die Symmetriebrechung.")
    else:
        print("  → γ beeinflusst Magic (unerwartet!)")
    print("="*80 + "\n")
    
    return gamma_values, results


def test_collatz_vs_uniform(N=1000, beta=0.5, gamma=1.5, k=500, save_plots=True):
    """
    Test 3: Collatz-Gewichte vs. Uniform (Kontrolle).
    
    Vergleiche:
    1. Collatz-gewichtete Defekte (physikalisch)
    2. Uniform-gewichtete Defekte (Referenz)
    3. Random-Soup (Kontrolle)
    
    Hypothese: Collatz-Gewichte verstärken Magic im Vergleich zu Uniform.
    
    Parameters
    ----------
    N : int
        Gittergröße
    beta : float
        Chiralität
    gamma : float
        Defekt-Stärke
    k : int
        Anzahl Eigenwerte
    save_plots : bool
        Speichere Plots
    """
    print("\n" + "="*80)
    print("TEST 3: COLLATZ vs. UNIFORM (KONTROLLE)")
    print("="*80 + "\n")
    
    # Drei Systeme
    print("[1/3] Uniform-Hamiltonian...")
    H_uniform = EABCHamiltonian(N=N, beta=beta, gamma=gamma)
    
    print("\n[2/3] Collatz-Hamiltonian...")
    H_collatz = CollatzEABCHamiltonian(N=N, beta=beta, gamma=gamma)
    
    print("\n[3/3] Random-Soup-Hamiltonian (Kontrolle)...")
    H_random = CollatzEABCHamiltonian(N=N, beta=beta, gamma=gamma, 
                                       use_random_soup=True, random_seed=42)
    
    # Magic berechnen
    systems = {
        'Uniform': H_uniform,
        'Collatz': H_collatz,
        'Random-Soup': H_random
    }
    
    results = {
        'M_collatz': {},
        'M_chi': {},
        'q_brody': {}
    }
    
    for name, H in systems.items():
        print(f"\n{'='*80}")
        print(f"ANALYSE: {name}")
        print('='*80)
        
        # Magic
        magic = ArithmeticMagic(H)
        M_all = magic.compute_all(compute_nzm=False)
        
        results['M_collatz'][name] = M_all['M_collatz']
        results['M_chi'][name] = M_all['M_chi']
        
        # Chaos
        eigenvalues = H.compute_spectrum(k=k, which='SM', sigma=0.0)
        unfolded = spectral_unfolding(eigenvalues)
        spacings = compute_level_spacing(unfolded)
        lsd_results = fit_level_statistics(spacings, bins=50)
        
        results['q_brody'][name] = lsd_results['brody_q']
        
        print(f"\n  M_collatz = {M_all['M_collatz']:.4f}")
        print(f"  M_chi = {M_all['M_chi']:.4f}")
        print(f"  q = {lsd_results['brody_q']:.4f}")
    
    # Plotting
    if save_plots:
        fig, axes = plt.subplots(1, 3, figsize=(18, 5))
        
        names = list(systems.keys())
        
        for i, (key, title) in enumerate([
            ('M_collatz', 'Collatz-Magic'),
            ('M_chi', 'Chiralitäts-Magic'),
            ('q_brody', 'Brody-Parameter q')
        ]):
            ax = axes[i]
            values = [results[key][name] for name in names]
            
            colors = ['blue', 'green', 'red']
            ax.bar(names, values, color=colors, alpha=0.7, edgecolor='black', linewidth=2)
            ax.set_ylabel(title, fontsize=14, fontweight='bold')
            ax.set_title(title, fontsize=14, fontweight='bold')
            ax.grid(axis='y', alpha=0.3)
        
        plt.suptitle('Collatz vs. Uniform: Magic & Chaos', 
                     fontsize=16, fontweight='bold', y=1.02)
        plt.tight_layout()
        plt.savefig('figures/collatz_vs_uniform.png', dpi=300, bbox_inches='tight')
        print("\n✓ Gespeichert: figures/collatz_vs_uniform.png")
        plt.close()
    
    print("\n" + "="*80)
    print("ZUSAMMENFASSUNG: COLLATZ vs. UNIFORM")
    print("="*80)
    
    for key in ['M_collatz', 'M_chi', 'q_brody']:
        print(f"\n{key}:")
        for name in names:
            print(f"  {name:15s}: {results[key][name]:.4f}")
    
    print("\nInterpretation:")
    if results['M_collatz']['Collatz'] > results['M_collatz']['Uniform']:
        print("  ✓ Collatz-Gewichte VERSTÄRKEN M_collatz (wie erwartet!)")
    if results['q_brody']['Collatz'] > results['q_brody']['Uniform']:
        print("  ✓ Collatz-Gewichte führen zu MEHR Chaos (interessant!)")
    
    print("="*80 + "\n")
    
    return results


if __name__ == "__main__":
    import sys
    
    # Defaults
    N = 1000
    k = 500
    
    print("\n" + "="*80)
    print("ARITHMETISCHE MAGIC vs. QUANTENCHAOS: VOLLSTÄNDIGE TEST-SUITE")
    print("="*80)
    print(f"Parameter: N = {N}, k = {k}")
    print("="*80 + "\n")
    
    try:
        # Test 1: β-Sweep (Haupttest!)
        print("\n>>> STARTE TEST 1: β-SWEEP <<<\n")
        beta_vals, beta_results = test_beta_sweep(N=N, k=k, save_plots=True)
        
        # Test 2: γ-Sweep
        print("\n>>> STARTE TEST 2: γ-SWEEP <<<\n")
        gamma_vals, gamma_results = test_gamma_sweep(N=N, k=k, save_plots=True)
        
        # Test 3: Collatz vs. Uniform
        print("\n>>> STARTE TEST 3: COLLATZ vs. UNIFORM <<<\n")
        collatz_results = test_collatz_vs_uniform(N=N, beta=0.5, gamma=1.5, k=k, save_plots=True)
        
        print("\n" + "="*80)
        print("ALLE TESTS ABGESCHLOSSEN!")
        print("="*80)
        print("\nErstelle Plots in figures/:")
        print("  - magic_vs_chaos_main.png (Hauptresultat!)")
        print("  - magic_correlations_all.png")
        print("  - magic_landscape.png")
        print("  - gamma_sweep.png")
        print("  - collatz_vs_uniform.png")
        print("="*80 + "\n")
        
    except KeyboardInterrupt:
        print("\n\n✗ Tests abgebrochen durch Benutzer.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n✗ Fehler während Tests: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
