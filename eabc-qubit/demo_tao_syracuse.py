"""
Demo: Tao-Syracuse-Erweiterung für EABC-Qubit

Dieses Skript demonstriert die vollständige Funktionalität der Tao-Syracuse-Erweiterung:

1. Syracuse-Dynamik: Trajektorien und Drift-Statistiken
2. Tao-Syracuse-Hamiltonian: Zeitabhängiger Hamiltonian mit echter Dynamik
3. Spektralanalyse: Vergleich mit statischen Collatz-Gewichten
4. Visualisierung: Plots und Statistiken

Basierend auf:
    T. Tao, "Almost all Collatz orbits attain almost bounded values" (2019)
"""

import numpy as np
import matplotlib.pyplot as plt
from src.hamiltonian import TaoSyracuseHamiltonian, CollatzEABCHamiltonian
from src.syracuse_dynamics import (
    syracuse_trajectory,
    trajectory_statistics,
    compare_empirical_vs_geom2,
    geom2_expected_drift
)
from src.level_spacing import compute_level_spacing
from src.spectral import spectral_unfolding, fit_wigner_surmise


def demo_syracuse_dynamics():
    """
    Demo 1: Syracuse-Funktion und Trajektorien-Analyse.
    """
    print("="*70)
    print("DEMO 1: SYRACUSE-DYNAMIK")
    print("="*70)
    
    # Bekannte interessante Startwerte
    interesting_starts = [27, 31, 47, 71, 97]
    
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    axes = axes.flatten()
    
    for i, start in enumerate(interesting_starts):
        print(f"\n[{i+1}/{len(interesting_starts)}] Analysiere Trajektorie für N₀ = {start}...")
        
        # Berechne Trajektorie
        trajectory, valuations = syracuse_trajectory(start, max_steps=100)
        stats = trajectory_statistics(trajectory, valuations)
        
        # Statistik ausgeben
        print(f"  Stopping Time:      {stats['stopping_time']}")
        print(f"  Max. Wert:          {stats['max_value']}")
        print(f"  ⟨a_j⟩:              {stats['mean_valuation']:.3f} (Theorie: 2.0)")
        print(f"  ⟨λ_j⟩:              {stats['mean_lambda']:.4f} (Theorie: {geom2_expected_drift():.4f})")
        print(f"  Gesamtdrift Σλ_j:   {stats['total_drift']:.4f}")
        
        # Plot: Trajektorie
        ax = axes[i]
        steps = range(len(trajectory))
        ax.plot(steps, trajectory, 'o-', color='blue', markersize=4, linewidth=1.5)
        ax.axhline(y=1, color='red', linestyle='--', linewidth=2, label='Ziel: 1')
        ax.set_title(f"N₀ = {start}\nτ = {stats['stopping_time']}, max = {stats['max_value']}")
        ax.set_xlabel('Schritt j')
        ax.set_ylabel('S_j(N₀)')
        ax.set_yscale('log')
        ax.grid(alpha=0.3)
        ax.legend()
    
    # Letzter Plot: Drift-Statistik
    ax = axes[-1]
    print("\n[Geom(2)-Vergleich] Empirisch vs. Theorie...")
    comparison = compare_empirical_vs_geom2(N=1000, n_trajectories=100, seed=42)
    
    categories = ['⟨a_j⟩', '⟨λ_j⟩']
    empirical = [comparison['empirical_mean_a'], comparison['empirical_mean_lambda']]
    theory = [comparison['geom2_expected_a'], comparison['geom2_expected_lambda']]
    
    x = np.arange(len(categories))
    width = 0.35
    
    ax.bar(x - width/2, empirical, width, label='Empirisch', color='blue', alpha=0.7)
    ax.bar(x + width/2, theory, width, label='Tao Theorie', color='red', alpha=0.7)
    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    ax.set_ylabel('Wert')
    ax.set_title('Geom(2)-Vergleich\n(100 Trajektorien)')
    ax.legend()
    ax.grid(alpha=0.3, axis='y')
    ax.axhline(y=0, color='black', linewidth=0.8)
    
    plt.suptitle("Syracuse-Trajektorien und Tao's Drift-Statistik", fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig('figures/demo_syracuse_trajectories.png', dpi=300, bbox_inches='tight')
    print("\n✓ Plot gespeichert: figures/demo_syracuse_trajectories.png")
    plt.show()


def demo_tao_hamiltonian():
    """
    Demo 2: Tao-Syracuse-Hamiltonian und Spektralanalyse.
    """
    print("\n\n" + "="*70)
    print("DEMO 2: TAO-SYRACUSE-HAMILTONIAN")
    print("="*70)
    
    # Parameter
    N = 1000
    start_n = 27
    trajectory_length = 50
    k = 500
    
    print(f"\nParameter:")
    print(f"  Gittergröße N:        {N}")
    print(f"  Startwert N₀:         {start_n}")
    print(f"  Trajektorienlänge:    {trajectory_length}")
    print(f"  Eigenwerte k:         {k}")
    
    # Konstruiere Hamiltonian
    print("\n[1/2] Konstruiere Tao-Syracuse-Hamiltonian...")
    H_tao = TaoSyracuseHamiltonian(
        N=N,
        start_n=start_n,
        trajectory_length=trajectory_length,
        alpha=1.0,
        beta=0.5,
        gamma=1.5
    )
    H_tao.info()
    
    # Berechne Spektrum
    print("\n[2/2] Berechne Spektrum und Level-Spacing...")
    E_tao = H_tao.compute_spectrum(k=k, which='SM')
    E_unfolded = spectral_unfolding(E_tao)
    spacings = compute_level_spacing(E_unfolded)
    
    # Statistik
    mean_s = np.mean(spacings)
    std_s = np.std(spacings)
    beta_fit = fit_wigner_surmise(spacings)
    
    print(f"\nSpektralstatistik:")
    print(f"  Energiebereich:       [{E_tao[0]:.4f}, {E_tao[-1]:.4f}]")
    print(f"  ⟨s⟩:                  {mean_s:.6f}")
    print(f"  σ(s):                 {std_s:.6f}")
    print(f"  β (Wigner-Fit):       {beta_fit:.3f}")
    
    # Plot: Spektrum und Level-Spacing
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # (a) Eigenspektrum
    ax = axes[0, 0]
    ax.plot(E_tao, 'o', markersize=3, color='blue', alpha=0.6)
    ax.set_xlabel('Index n')
    ax.set_ylabel('Eigenwert E_n')
    ax.set_title('(a) Eigenspektrum')
    ax.grid(alpha=0.3)
    
    # (b) Spectral Unfolding
    ax = axes[0, 1]
    ax.plot(E_tao, np.arange(len(E_tao)), 'o', markersize=3, color='green', alpha=0.6, label='Empirisch')
    ax.plot(E_tao, E_unfolded, '-', linewidth=2, color='red', label='Unfolded')
    ax.set_xlabel('Energie E')
    ax.set_ylabel('Integrierte Zustandsdichte N(E)')
    ax.set_title('(b) Spectral Unfolding')
    ax.legend()
    ax.grid(alpha=0.3)
    
    # (c) Level-Spacing Histogram
    ax = axes[1, 0]
    ax.hist(spacings, bins=50, density=True, alpha=0.7, color='blue', edgecolor='black', label='Empirisch')
    
    # Wigner-Surmise (GUE)
    s = np.linspace(0, 4, 200)
    p_gue = (32 / np.pi**2) * s**2 * np.exp(-4 * s**2 / np.pi)
    ax.plot(s, p_gue, 'r--', linewidth=2, label='GUE (β=2)')
    
    # Poisson (integrabel)
    p_poisson = np.exp(-s)
    ax.plot(s, p_poisson, 'g--', linewidth=2, label='Poisson (β=0)')
    
    ax.set_xlabel('Level Spacing s')
    ax.set_ylabel('P(s)')
    ax.set_title(f'(c) Level-Spacing\nσ={std_s:.4f}, β≈{beta_fit:.2f}')
    ax.legend()
    ax.grid(alpha=0.3)
    
    # (d) Lokale Drifts λ_j
    ax = axes[1, 1]
    lambdas = H_tao.lambdas
    ax.plot(lambdas, 'o-', markersize=5, color='purple', linewidth=1.5)
    ax.axhline(y=geom2_expected_drift(), color='red', linestyle='--', linewidth=2, 
               label=f'E[λ] = log(3/4) ≈ {geom2_expected_drift():.3f}')
    ax.axhline(y=0, color='black', linewidth=0.8)
    ax.set_xlabel('Schritt j')
    ax.set_ylabel('λ_j = log(3) - a_j·log(2)')
    ax.set_title(f"(d) Lokale Tao-Drifts\n⟨λ_j⟩ = {np.mean(lambdas):.4f}")
    ax.legend()
    ax.grid(alpha=0.3)
    
    plt.suptitle(f"Tao-Syracuse-Hamiltonian (N={N}, N₀={start_n})", fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig('figures/demo_tao_hamiltonian.png', dpi=300, bbox_inches='tight')
    print("\n✓ Plot gespeichert: figures/demo_tao_hamiltonian.png")
    plt.show()


def demo_comparison():
    """
    Demo 3: Direkter Vergleich statisch vs. dynamisch.
    """
    print("\n\n" + "="*70)
    print("DEMO 3: STATISCH VS. DYNAMISCH")
    print("="*70)
    
    # Parameter
    N = 1000
    start_n = 27
    trajectory_length = 50
    k = 500
    
    # 1. Statisch (Collatz)
    print("\n[1/2] Konstruiere statischen Collatz-Hamiltonian...")
    H_static = CollatzEABCHamiltonian(N=N, alpha=1.0, beta=0.5, gamma=1.5)
    E_static = H_static.compute_spectrum(k=k, which='SM')
    E_static_unfolded = spectral_unfolding(E_static)
    spacings_static = compute_level_spacing(E_static_unfolded)
    
    sigma_static = np.std(spacings_static)
    beta_static = fit_wigner_surmise(spacings_static)
    
    print(f"  σ_static = {sigma_static:.4f}")
    print(f"  β_static = {beta_static:.3f}")
    
    # 2. Dynamisch (Tao-Syracuse)
    print("\n[2/2] Konstruiere dynamischen Tao-Syracuse-Hamiltonian...")
    H_dynamic = TaoSyracuseHamiltonian(N=N, start_n=start_n, trajectory_length=trajectory_length,
                                       alpha=1.0, beta=0.5, gamma=1.5)
    E_dynamic = H_dynamic.compute_spectrum(k=k, which='SM')
    E_dynamic_unfolded = spectral_unfolding(E_dynamic)
    spacings_dynamic = compute_level_spacing(E_dynamic_unfolded)
    
    sigma_dynamic = np.std(spacings_dynamic)
    beta_dynamic = fit_wigner_surmise(spacings_dynamic)
    
    print(f"  σ_dynamic = {sigma_dynamic:.4f}")
    print(f"  β_dynamic = {beta_dynamic:.3f}")
    
    # Vergleich
    print("\n" + "="*70)
    print("VERGLEICH")
    print("="*70)
    print(f"\nLevel-Spacing Standardabweichung σ(s):")
    print(f"  Statisch:   {sigma_static:.4f}")
    print(f"  Dynamisch:  {sigma_dynamic:.4f}")
    print(f"  GUE:        ~0.52")
    print(f"\nDifferenz:    |σ_static - σ_dynamic| = {abs(sigma_static - sigma_dynamic):.4f}")
    
    threshold = 0.05
    if abs(sigma_static - sigma_dynamic) < threshold:
        print(f"\n✓ Statisch ≈ Dynamisch (innerhalb {threshold*100:.0f}% Toleranz)")
        print("  → Die GUE-Signatur ist robust gegen Gewichtswahl!")
    else:
        print(f"\n✗ Statisch ≠ Dynamisch (Differenz > {threshold*100:.0f}%)")
        print("  → Die statischen Gewichte sind speziell.")
    
    # Side-by-Side Plot
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Statisch
    ax = axes[0]
    ax.hist(spacings_static, bins=50, density=True, alpha=0.7, color='blue', edgecolor='black')
    s = np.linspace(0, 4, 200)
    p_gue = (32 / np.pi**2) * s**2 * np.exp(-4 * s**2 / np.pi)
    ax.plot(s, p_gue, 'r--', linewidth=2, label='GUE')
    ax.set_title(f"Statisch (Collatz-EABC)\nσ={sigma_static:.4f}, β≈{beta_static:.2f}")
    ax.set_xlabel('Level Spacing s')
    ax.set_ylabel('P(s)')
    ax.legend()
    ax.grid(alpha=0.3)
    
    # Dynamisch
    ax = axes[1]
    ax.hist(spacings_dynamic, bins=50, density=True, alpha=0.7, color='red', edgecolor='black')
    ax.plot(s, p_gue, 'k--', linewidth=2, label='GUE')
    ax.set_title(f"Dynamisch (Tao-Syracuse)\nσ={sigma_dynamic:.4f}, β≈{beta_dynamic:.2f}")
    ax.set_xlabel('Level Spacing s')
    ax.set_ylabel('P(s)')
    ax.legend()
    ax.grid(alpha=0.3)
    
    plt.suptitle(f"Statisch vs. Dynamisch (N={N}, k={k})", fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig('figures/demo_static_vs_dynamic.png', dpi=300, bbox_inches='tight')
    print("\n✓ Plot gespeichert: figures/demo_static_vs_dynamic.png")
    plt.show()
    
    # Spektrum-Differenz
    fig, ax = plt.subplots(figsize=(10, 6))
    delta_E = E_dynamic - E_static
    ax.plot(delta_E, 'o', markersize=4, color='purple', alpha=0.6)
    ax.axhline(y=0, color='black', linewidth=1)
    ax.set_xlabel('Eigenwert-Index n')
    ax.set_ylabel('ΔE_n = E_n^{dynamic} - E_n^{static}')
    ax.set_title(f"Spektrum-Differenz: Dynamisch - Statisch\n⟨ΔE⟩ = {np.mean(delta_E):.6f}, σ(ΔE) = {np.std(delta_E):.6f}")
    ax.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig('figures/demo_spectrum_difference.png', dpi=300, bbox_inches='tight')
    print("✓ Plot gespeichert: figures/demo_spectrum_difference.png")
    plt.show()


if __name__ == "__main__":
    print("\n" + "="*70)
    print("TAO-SYRACUSE-ERWEITERUNG: DEMO")
    print("="*70)
    print("\nDieses Demo zeigt die vollständige Funktionalität der Tao-Syracuse-Erweiterung.")
    print("Es werden drei Teile ausgeführt:")
    print("  1. Syracuse-Dynamik und Trajektorien")
    print("  2. Tao-Syracuse-Hamiltonian und Spektralanalyse")
    print("  3. Direkter Vergleich statisch vs. dynamisch")
    print("\nDies kann einige Minuten dauern...")
    
    import os
    os.makedirs('figures', exist_ok=True)
    
    # Demo 1: Syracuse-Dynamik
    demo_syracuse_dynamics()
    
    # Demo 2: Tao-Hamiltonian
    demo_tao_hamiltonian()
    
    # Demo 3: Vergleich
    demo_comparison()
    
    print("\n" + "="*70)
    print("DEMO ABGESCHLOSSEN")
    print("="*70)
    print("\nAlle Plots wurden im Ordner 'figures/' gespeichert:")
    print("  - demo_syracuse_trajectories.png")
    print("  - demo_tao_hamiltonian.png")
    print("  - demo_static_vs_dynamic.png")
    print("  - demo_spectrum_difference.png")
    print("\n" + "="*70)
