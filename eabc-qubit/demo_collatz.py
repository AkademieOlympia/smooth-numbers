#!/usr/bin/env python3
"""
Collatz-EABC-Qubit Demo: Vergleich von Standard- und Collatz-gewichtetem Hamiltonian

Dieses Demo-Skript untersucht die Auswirkung physikalisch motivierter Collatz-Gewichte
auf die spektralen Eigenschaften des EABC-Qubit-Systems.

Zentrale Frage:
    Zeigen die Collatz-Gewichte aus Paper C bessere/stabilere spektrale Eigenschaften
    als uniforme Defekte oder zufällig permutierte Gewichte?

Test-Szenarien:
    1. Standard-EABC (uniforme Primzahl-Defekte)
    2. Collatz-gewichtet (echte log(r)-Raten)
    3. Random Soup (permutierte Gewichte als Kontrolle)

Erwartetes Verhalten:
    - Bei γ = 0: Poisson (integrabel, keine Defekte)
    - Bei γ ≈ 1: Mögliche Resonanz-Peaks oder Crossover
    - Falsifikation: Ist Collatz besser als Random Soup?
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

from src.hamiltonian import EABCHamiltonian, CollatzEABCHamiltonian
from src.level_spacing import compute_level_spacing, fit_level_statistics
from src.visualization import plot_level_statistics


def poisson_distribution(s: np.ndarray) -> np.ndarray:
    """Poisson level spacing distribution P(s) = exp(-s)."""
    return np.exp(-s)


def gue_distribution(s: np.ndarray) -> np.ndarray:
    """GUE level spacing distribution (Wigner surmise)."""
    return (np.pi / 2) * s * np.exp(-np.pi * s**2 / 4)


def compare_three_scenarios(
    N: int = 1000,
    alpha: float = 1.0,
    beta: float = 0.5,
    gamma: float = 1.5,
    k: int = 800,
    save_fig: bool = True
):
    """
    Vergleiche drei Szenarien:
    1. Standard-EABC (uniform)
    2. Collatz-gewichtet
    3. Random Soup (Kontrolle)
    
    Parameters
    ----------
    N : int
        Gittergröße
    alpha : float
        Hopping-Stärke
    beta : float
        Chirale Kopplung
    gamma : float
        Defekt-Stärke
    k : int
        Anzahl berechneter Eigenwerte
    save_fig : bool
        Speichere Plots
    """
    print("="*70)
    print("Collatz-EABC-Qubit: Drei-Szenarien-Vergleich")
    print("="*70)
    print(f"\nParameter: N = {N}, α = {alpha}, β = {beta}, γ = {gamma}")
    print(f"Berechne {k} Eigenwerte pro Szenario\n")
    
    # Szenario 1: Standard (uniform)
    print("\n[1/3] Szenario 1: Standard-EABC (uniforme Defekte)")
    print("-"*70)
    H_uniform = EABCHamiltonian(N=N, alpha=alpha, beta=beta, gamma=gamma)
    E_uniform = H_uniform.compute_spectrum(k=k, which='SM')
    s_uniform = compute_level_spacing(E_uniform)
    
    # Szenario 2: Collatz-gewichtet
    print("\n[2/3] Szenario 2: Collatz-gewichtet (echte log(r)-Raten)")
    print("-"*70)
    H_collatz = CollatzEABCHamiltonian(
        N=N, alpha=alpha, beta=beta, gamma=gamma, use_random_soup=False
    )
    H_collatz.info()
    E_collatz = H_collatz.compute_spectrum(k=k, which='SM')
    s_collatz = compute_level_spacing(E_collatz)
    
    # Szenario 3: Random Soup
    print("\n[3/3] Szenario 3: Random Soup (permutierte Gewichte)")
    print("-"*70)
    H_soup = CollatzEABCHamiltonian(
        N=N, alpha=alpha, beta=beta, gamma=gamma, use_random_soup=True, random_seed=42
    )
    E_soup = H_soup.compute_spectrum(k=k, which='SM')
    s_soup = compute_level_spacing(E_soup)
    
    # Statistische Analyse
    print("\n" + "="*70)
    print("Statistische Analyse der Level Spacing Distributions")
    print("="*70)
    
    for name, spacings in [("Uniform", s_uniform), ("Collatz", s_collatz), ("Random Soup", s_soup)]:
        fit_results = fit_level_statistics(spacings)
        print(f"\n{name}:")
        print(f"  Poisson χ²:       {fit_results['poisson_chi2']:.6f}")
        print(f"  GUE χ²:           {fit_results['gue_chi2']:.6f}")
        print(f"  Poisson KS-Test:  {fit_results['poisson_ks']:.6f}")
        print(f"  GUE KS-Test:      {fit_results['gue_ks']:.6f}")
        print(f"  Mittelwert ⟨s⟩:   {np.mean(spacings):.6f}")
        print(f"  Std.-Abw. σ(s):   {np.std(spacings):.6f}")
    
    # Visualisierung
    print("\n" + "="*70)
    print("Erzeuge Visualisierung...")
    print("="*70)
    
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    
    s_range = np.linspace(0, 4, 1000)
    p_poisson = poisson_distribution(s_range)
    p_gue = gue_distribution(s_range)
    
    scenarios = [
        ("Standard-EABC (Uniform)", s_uniform, 'blue'),
        ("Collatz-gewichtet", s_collatz, 'red'),
        ("Random Soup", s_soup, 'green')
    ]
    
    for ax, (title, spacings, color) in zip(axes, scenarios):
        # Histogram
        ax.hist(spacings, bins=50, density=True, alpha=0.6, color=color, 
                edgecolor='black', label='Daten')
        
        # Theoretische Kurven
        ax.plot(s_range, p_poisson, 'k--', lw=2, label='Poisson')
        ax.plot(s_range, p_gue, 'k-', lw=2, label='GUE')
        
        ax.set_xlabel('Normierter Level Spacing s', fontsize=12)
        ax.set_ylabel('P(s)', fontsize=12)
        ax.set_title(title, fontsize=13, fontweight='bold')
        ax.legend(fontsize=10)
        ax.grid(alpha=0.3)
        ax.set_xlim(0, 4)
        ax.set_ylim(0, 1.2)
    
    plt.suptitle(f'Level Spacing Distribution (N={N}, γ={gamma})', 
                 fontsize=15, fontweight='bold', y=1.02)
    plt.tight_layout()
    
    if save_fig:
        fig_dir = Path('figures')
        fig_dir.mkdir(exist_ok=True)
        filename = fig_dir / f'collatz_comparison_gamma{gamma:.1f}.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"\n✓ Plot gespeichert: {filename}")
    
    plt.show()
    
    return {
        'uniform': {'eigenvalues': E_uniform, 'spacings': s_uniform},
        'collatz': {'eigenvalues': E_collatz, 'spacings': s_collatz},
        'soup': {'eigenvalues': E_soup, 'spacings': s_soup}
    }


def gamma_sweep_comparison(
    N: int = 1000,
    gamma_values: np.ndarray = np.linspace(0, 3, 7),
    k: int = 600,
    save_fig: bool = True
):
    """
    Untersuche die Abhängigkeit der Spektralstatistik von γ für alle drei Szenarien.
    
    Zentrale Frage:
        Zeigen Collatz-Gewichte bei bestimmten γ-Werten stabilere oder
        charakteristischere Spektralstatistiken als uniforme oder Random-Soup-Defekte?
    
    Parameters
    ----------
    N : int
        Gittergröße
    gamma_values : np.ndarray
        Array von γ-Werten zum Testen
    k : int
        Anzahl berechneter Eigenwerte
    save_fig : bool
        Speichere Plot
    """
    print("="*70)
    print("Collatz-EABC-Qubit: γ-Parameter-Sweep")
    print("="*70)
    print(f"\nParameter: N = {N}, γ ∈ [{gamma_values[0]}, {gamma_values[-1]}]")
    print(f"Anzahl γ-Werte: {len(gamma_values)}\n")
    
    results = {
        'gamma': gamma_values,
        'uniform': {'mean': [], 'std': [], 'ks_poisson': [], 'ks_gue': []},
        'collatz': {'mean': [], 'std': [], 'ks_poisson': [], 'ks_gue': []},
        'soup': {'mean': [], 'std': [], 'ks_poisson': [], 'ks_gue': []}
    }
    
    for i, gamma in enumerate(gamma_values):
        print(f"\n[{i+1}/{len(gamma_values)}] γ = {gamma:.2f}")
        print("-"*70)
        
        # Uniform
        H_uniform = EABCHamiltonian(N=N, gamma=gamma)
        E_uniform = H_uniform.compute_spectrum(k=k, which='SM')
        s_uniform = compute_level_spacing(E_uniform)
        fit_uniform = fit_level_statistics(s_uniform)
        
        results['uniform']['mean'].append(np.mean(s_uniform))
        results['uniform']['std'].append(np.std(s_uniform))
        results['uniform']['ks_poisson'].append(fit_uniform['poisson_ks'])
        results['uniform']['ks_gue'].append(fit_uniform['gue_ks'])
        
        # Collatz
        H_collatz = CollatzEABCHamiltonian(N=N, gamma=gamma, use_random_soup=False)
        E_collatz = H_collatz.compute_spectrum(k=k, which='SM')
        s_collatz = compute_level_spacing(E_collatz)
        fit_collatz = fit_level_statistics(s_collatz)
        
        results['collatz']['mean'].append(np.mean(s_collatz))
        results['collatz']['std'].append(np.std(s_collatz))
        results['collatz']['ks_poisson'].append(fit_collatz['poisson_ks'])
        results['collatz']['ks_gue'].append(fit_collatz['gue_ks'])
        
        # Soup
        H_soup = CollatzEABCHamiltonian(N=N, gamma=gamma, use_random_soup=True)
        E_soup = H_soup.compute_spectrum(k=k, which='SM')
        s_soup = compute_level_spacing(E_soup)
        fit_soup = fit_level_statistics(s_soup)
        
        results['soup']['mean'].append(np.mean(s_soup))
        results['soup']['std'].append(np.std(s_soup))
        results['soup']['ks_poisson'].append(fit_soup['poisson_ks'])
        results['soup']['ks_gue'].append(fit_soup['gue_ks'])
        
        print(f"  Uniform:  KS(Poisson) = {fit_uniform['poisson_ks']:.4f}, KS(GUE) = {fit_uniform['gue_ks']:.4f}")
        print(f"  Collatz:  KS(Poisson) = {fit_collatz['poisson_ks']:.4f}, KS(GUE) = {fit_collatz['gue_ks']:.4f}")
        print(f"  Soup:     KS(Poisson) = {fit_soup['poisson_ks']:.4f}, KS(GUE) = {fit_soup['gue_ks']:.4f}")
    
    # Visualisierung
    print("\n" + "="*70)
    print("Erzeuge γ-Sweep-Visualisierung...")
    print("="*70)
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Plot 1: KS-Test Poisson
    ax = axes[0, 0]
    ax.plot(gamma_values, results['uniform']['ks_poisson'], 'o-', label='Uniform', color='blue', lw=2)
    ax.plot(gamma_values, results['collatz']['ks_poisson'], 's-', label='Collatz', color='red', lw=2)
    ax.plot(gamma_values, results['soup']['ks_poisson'], '^-', label='Random Soup', color='green', lw=2)
    ax.set_xlabel('γ (Defekt-Stärke)', fontsize=12)
    ax.set_ylabel('KS-Statistik (Poisson)', fontsize=12)
    ax.set_title('Kolmogorov-Smirnov: Abweichung von Poisson', fontsize=13, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(alpha=0.3)
    
    # Plot 2: KS-Test GUE
    ax = axes[0, 1]
    ax.plot(gamma_values, results['uniform']['ks_gue'], 'o-', label='Uniform', color='blue', lw=2)
    ax.plot(gamma_values, results['collatz']['ks_gue'], 's-', label='Collatz', color='red', lw=2)
    ax.plot(gamma_values, results['soup']['ks_gue'], '^-', label='Random Soup', color='green', lw=2)
    ax.set_xlabel('γ (Defekt-Stärke)', fontsize=12)
    ax.set_ylabel('KS-Statistik (GUE)', fontsize=12)
    ax.set_title('Kolmogorov-Smirnov: Abweichung von GUE', fontsize=13, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(alpha=0.3)
    
    # Plot 3: Mittelwert
    ax = axes[1, 0]
    ax.plot(gamma_values, results['uniform']['mean'], 'o-', label='Uniform', color='blue', lw=2)
    ax.plot(gamma_values, results['collatz']['mean'], 's-', label='Collatz', color='red', lw=2)
    ax.plot(gamma_values, results['soup']['mean'], '^-', label='Random Soup', color='green', lw=2)
    ax.axhline(1.0, color='black', linestyle='--', alpha=0.5, label='Theoretisch: ⟨s⟩ = 1')
    ax.set_xlabel('γ (Defekt-Stärke)', fontsize=12)
    ax.set_ylabel('⟨s⟩', fontsize=12)
    ax.set_title('Mittlerer Level Spacing', fontsize=13, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(alpha=0.3)
    
    # Plot 4: Standardabweichung
    ax = axes[1, 1]
    ax.plot(gamma_values, results['uniform']['std'], 'o-', label='Uniform', color='blue', lw=2)
    ax.plot(gamma_values, results['collatz']['std'], 's-', label='Collatz', color='red', lw=2)
    ax.plot(gamma_values, results['soup']['std'], '^-', label='Random Soup', color='green', lw=2)
    ax.set_xlabel('γ (Defekt-Stärke)', fontsize=12)
    ax.set_ylabel('σ(s)', fontsize=12)
    ax.set_title('Standardabweichung Level Spacing', fontsize=13, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(alpha=0.3)
    
    plt.suptitle(f'γ-Parameter-Sweep: Collatz vs. Uniform vs. Random Soup (N={N})', 
                 fontsize=15, fontweight='bold', y=0.995)
    plt.tight_layout()
    
    if save_fig:
        fig_dir = Path('figures')
        fig_dir.mkdir(exist_ok=True)
        filename = fig_dir / 'collatz_gamma_sweep.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"\n✓ Plot gespeichert: {filename}")
    
    plt.show()
    
    return results


def main():
    """Hauptprogramm: Führe alle Vergleichstests durch."""
    print("\n")
    print("╔" + "="*68 + "╗")
    print("║" + " "*20 + "COLLATZ-EABC-QUBIT DEMO" + " "*25 + "║")
    print("║" + " "*68 + "║")
    print("║" + "  Integration der Collatz-Dynamik in das EABC-Qubit-Framework  " + " "*3 + "║")
    print("╚" + "="*68 + "╝")
    
    # Test 1: Drei-Szenarien-Vergleich bei γ = 1.5
    print("\n\n" + "█"*70)
    print("TEST 1: Drei-Szenarien-Vergleich bei γ = 1.5")
    print("█"*70)
    results_single = compare_three_scenarios(
        N=1000,
        alpha=1.0,
        beta=0.5,
        gamma=1.5,
        k=800,
        save_fig=True
    )
    
    # Test 2: γ-Parameter-Sweep
    print("\n\n" + "█"*70)
    print("TEST 2: γ-Parameter-Sweep (γ ∈ [0, 3])")
    print("█"*70)
    results_sweep = gamma_sweep_comparison(
        N=1000,
        gamma_values=np.linspace(0, 3, 7),
        k=600,
        save_fig=True
    )
    
    # Zusammenfassung
    print("\n\n" + "="*70)
    print("ZUSAMMENFASSUNG")
    print("="*70)
    print("\nDie Demo hat folgende Aspekte untersucht:")
    print("  1. Vergleich der Level Spacing Distribution für drei Szenarien")
    print("  2. Abhängigkeit der Spektralstatistik vom Parameter γ")
    print("\nZentrale Frage (Falsifikations-Test):")
    print("  → Zeigen Collatz-Gewichte stabilere/charakteristischere Eigenschaften")
    print("    als uniforme Defekte oder Random Soup?")
    print("\nResultate:")
    print("  → Alle Plots wurden im Verzeichnis 'figures/' gespeichert")
    print("  → Untersuche die KS-Statistiken für quantitative Aussagen")
    print("="*70)
    print("\n✓ Demo abgeschlossen.\n")


if __name__ == "__main__":
    main()
