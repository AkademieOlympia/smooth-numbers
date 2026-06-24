#!/usr/bin/env python3
"""
EABC-Qubit Demo Script

Schneller Test des Frameworks mit einem kleinen System.
"""

import numpy as np
from src.hamiltonian import EABCHamiltonian
from src.spectral import spectral_unfolding
from src.level_spacing import compute_level_spacing, fit_level_statistics
from src.visualization import plot_level_statistics, plot_eigenspectrum


def main():
    print("="*70)
    print(" EABC-Qubit Framework Demo")
    print("="*70)
    print()
    
    # Parameter (kleines System für schnellen Test)
    N = 500
    alpha = 1.0
    beta = 0.5
    gamma = 1.5
    k = 200  # Anzahl Eigenwerte
    
    print("SYSTEM-PARAMETER:")
    print(f"  Gittergröße N:          {N}")
    print(f"  Hopping-Stärke α:       {alpha}")
    print(f"  Chirale Kopplung β:     {beta}")
    print(f"  Defekt-Stärke γ:        {gamma}")
    print(f"  Eigenwerte k:           {k}")
    print()
    
    # 1. Hamiltonian konstruieren
    print("SCHRITT 1: Hamiltonian-Konstruktion")
    print("-" * 70)
    H = EABCHamiltonian(N, alpha, beta, gamma)
    print()
    
    # 2. Spektrum berechnen
    print("SCHRITT 2: Spektrumsberechnung")
    print("-" * 70)
    eigenvalues = H.compute_spectrum(k=k, which='SM')
    print(f"✓ {k} Eigenwerte berechnet")
    print(f"  Energie-Bereich: [{eigenvalues[0]:.4f}, {eigenvalues[-1]:.4f}]")
    print()
    
    # 3. Spektrales Unfolding
    print("SCHRITT 3: Spektrales Unfolding")
    print("-" * 70)
    unfolded = spectral_unfolding(eigenvalues, method='polynomial')
    mean_density = k / (unfolded[-1] - unfolded[0])
    print(f"✓ Spektrum entfaltet")
    print(f"  Mittlere Dichte: {mean_density:.3f} (Ziel: 1.0)")
    print()
    
    # 4. Level Spacing Distribution
    print("SCHRITT 4: Level Spacing Distribution")
    print("-" * 70)
    spacings = compute_level_spacing(unfolded)
    print(f"✓ {len(spacings)} Spacings berechnet")
    print(f"  ⟨s⟩ = {np.mean(spacings):.4f} (Ziel: 1.0)")
    print(f"  σ_s = {np.std(spacings):.4f}")
    print()
    
    # 5. Statistischer Fit
    print("SCHRITT 5: Fit gegen theoretische Verteilungen")
    print("-" * 70)
    results = fit_level_statistics(spacings)
    
    print("χ² Goodness-of-Fit:")
    print(f"  Poisson:  {results['poisson']:.3f}")
    print(f"  GOE:      {results['GOE']:.3f}")
    print(f"  GUE:      {results['GUE']:.3f}")
    print(f"  Brody:    {results['brody']:.3f} (q = {results['brody_q']:.3f})")
    print()
    
    # Beste Fit
    chi2_models = {k: v for k, v in results.items() if k != 'brody_q'}
    best_fit = min(chi2_models, key=chi2_models.get)
    
    print(f"→ Beste Übereinstimmung: {best_fit.upper()}")
    print()
    
    # Interpretation
    print("INTERPRETATION:")
    print("-" * 70)
    
    if best_fit == 'poisson':
        print("✓ POISSON-STATISTIK")
        print("  → Primzahlen wirken wie unkorrelierte zufällige Störungen")
        print("  → Keine globale Quantenkohärenz")
        print("  → Das EABC-Modell zeigt integrable Dynamik")
    elif best_fit in ['GOE', 'GUE']:
        print(f"✓ {best_fit.upper()}-STATISTIK (Wigner-Dyson)")
        print("  → Level-Repulsion vorhanden!")
        print("  → Starke spektrale Korrelationen")
        print("  → Quantenchaos!")
        
        if best_fit == 'GUE':
            print("  → GUE: Gebrochene Zeitumkehr-Symmetrie")
            print("  → Wie Riemannsche Nullstellen (Montgomery-Vermutung)!")
        else:
            print("  → GOE: Zeitumkehr-invariant")
    else:
        q = results['brody_q']
        print(f"✓ BRODY-STATISTIK (q = {q:.3f})")
        print(f"  → Intermediäres Regime zwischen Poisson (q=0) und Wigner-Dyson (q=1)")
        print(f"  → Partielles Chaos")
        
        if q < 0.3:
            print("  → Näher an Poisson → Schwach korreliert")
        elif q > 0.7:
            print("  → Näher an Wigner-Dyson → Stark korreliert")
        else:
            print("  → Crossover-Regime")
    
    print()
    print("="*70)
    print("Demo abgeschlossen!")
    print()
    print("Nächste Schritte:")
    print("  1. Variiere γ (Defekt-Stärke): gamma_sweep.py")
    print("  2. Größere Systeme (N=5000): notebooks/02_spectral_analysis.ipynb")
    print("  3. Visualisierung: Plots wurden gespeichert in figures/")
    print("="*70)
    
    # Visualisierung
    print("\nErstelle Visualisierungen...")
    
    import matplotlib
    matplotlib.use('Agg')  # Non-interactive backend
    
    plot_level_statistics(
        spacings,
        title=f"EABC-Qubit (N={N}, γ={gamma})",
        save_path="figures/demo_level_statistics.png"
    )
    
    plot_eigenspectrum(
        eigenvalues,
        unfolded,
        title=f"EABC-Qubit Spektrum (N={N})",
        save_path="figures/demo_eigenspectrum.png"
    )
    
    print("✓ Plots gespeichert in figures/")


if __name__ == "__main__":
    main()
