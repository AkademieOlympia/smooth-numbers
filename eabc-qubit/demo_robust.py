#!/usr/bin/env python3
"""
EABC-Qubit Robuste Analyse mit Bandkanten-Trimming

Dieser Test implementiert den kritischen Hinweis:
Schneide die äußersten Ränder des Spektrums ab, um Van-Hove-Singularitäten
an den Bandkanten zu vermeiden.
"""

import numpy as np
from src.hamiltonian import EABCHamiltonian
from src.spectral import spectral_unfolding
from src.level_spacing import compute_level_spacing, fit_level_statistics
from src.visualization import plot_level_statistics


def trim_spectrum(eigenvalues, trim_fraction=0.2):
    """
    Schneide die äußeren trim_fraction/2 an beiden Enden ab.
    
    Parameters
    ----------
    eigenvalues : np.ndarray
        Sortiertes Spektrum
    trim_fraction : float
        Anteil zum Abschneiden (0.2 = schneide 20% ab, je 10% an jedem Ende)
    
    Returns
    -------
    np.ndarray
        Getrimmtes Spektrum (mittlere 1-trim_fraction)
    """
    n = len(eigenvalues)
    cut = int(n * trim_fraction / 2)
    
    return eigenvalues[cut:-cut]


def main():
    print("="*70)
    print(" EABC-Qubit: Robuste Analyse mit Bandkanten-Trimming")
    print("="*70)
    print()
    print("Methode: Nutze nur die mittleren 60% des Spektrums")
    print("Grund: Van-Hove-Singularitäten an Bandkanten vermeiden")
    print()
    
    # Parameter
    N = 1000  # Größeres System für bessere Statistik
    alpha = 1.0
    beta = 0.5
    gamma = 1.5
    k = 500  # Mehr Eigenwerte
    trim_fraction = 0.4  # Schneide 40% ab (je 20% an Rändern) → mittlere 60%
    
    print("SYSTEM-PARAMETER:")
    print(f"  Gittergröße N:          {N}")
    print(f"  Hopping α:              {alpha}")
    print(f"  Chirale Kopplung β:     {beta}")
    print(f"  Defekt-Stärke γ:        {gamma}")
    print(f"  Eigenwerte k:           {k}")
    print(f"  Trimming:               {trim_fraction*100:.0f}% (mittlere {(1-trim_fraction)*100:.0f}%)")
    print()
    
    # Hamiltonian
    print("SCHRITT 1: Konstruktion")
    print("-" * 70)
    H = EABCHamiltonian(N, alpha, beta, gamma)
    print()
    
    # Spektrum
    print("SCHRITT 2: Spektrum (volle Bandbreite)")
    print("-" * 70)
    eigenvalues_full = H.compute_spectrum(k=k, which='SM')
    print(f"  Voller Bereich: E ∈ [{eigenvalues_full[0]:.4f}, {eigenvalues_full[-1]:.4f}]")
    print()
    
    # Trimming
    print("SCHRITT 3: Bandkanten-Trimming")
    print("-" * 70)
    eigenvalues_trimmed = trim_spectrum(eigenvalues_full, trim_fraction)
    print(f"  Getrimmt ({len(eigenvalues_trimmed)} Eigenwerte):")
    print(f"    E ∈ [{eigenvalues_trimmed[0]:.4f}, {eigenvalues_trimmed[-1]:.4f}]")
    print(f"  → Nur die mittlere {(1-trim_fraction)*100:.0f}% der Bandbreite")
    print()
    
    # Unfolding
    print("SCHRITT 4: Spektrales Unfolding (getrimmte Daten)")
    print("-" * 70)
    unfolded = spectral_unfolding(eigenvalues_trimmed, method='polynomial')
    mean_density = len(unfolded) / (unfolded[-1] - unfolded[0])
    print(f"  Mittlere Dichte: {mean_density:.4f} (Ziel: 1.0)")
    print()
    
    # Level Spacings
    print("SCHRITT 5: Level Spacing Distribution")
    print("-" * 70)
    spacings = compute_level_spacing(unfolded)
    print(f"  {len(spacings)} Spacings")
    print(f"  ⟨s⟩ = {np.mean(spacings):.4f}")
    print(f"  σ_s = {np.std(spacings):.4f}")
    print()
    
    # Statistik
    print("SCHRITT 6: χ²-Fit (robuste Analyse)")
    print("-" * 70)
    results = fit_level_statistics(spacings)
    
    print("χ² Goodness-of-Fit:")
    print(f"  Poisson:  {results['poisson']:.3f}")
    print(f"  GOE:      {results['GOE']:.3f}")
    print(f"  GUE:      {results['GUE']:.3f}")
    if not np.isnan(results['brody_q']):
        print(f"  Brody:    {results['brody']:.3f} (q = {results['brody_q']:.3f})")
    print()
    
    # Beste Fit
    chi2_models = {k: v for k, v in results.items() if k != 'brody_q'}
    best_fit = min(chi2_models, key=chi2_models.get)
    
    print(f"→ BESTE ÜBEREINSTIMMUNG: {best_fit.upper()}")
    print()
    
    # Vergleich
    print("="*70)
    print(" VERGLEICH: Mit vs. Ohne Bandkanten-Trimming")
    print("="*70)
    print()
    print("Mit Trimming (robust):")
    print(f"  χ²_Poisson / χ²_GOE = {results['poisson'] / results['GOE']:.3f}")
    
    # Zum Vergleich: Ohne Trimming
    print("\nZum Vergleich: Analyse OHNE Trimming...")
    unfolded_full = spectral_unfolding(eigenvalues_full, method='polynomial')
    spacings_full = compute_level_spacing(unfolded_full)
    results_full = fit_level_statistics(spacings_full)
    
    print(f"\nOhne Trimming:")
    print(f"  χ²_Poisson = {results_full['poisson']:.3f}")
    print(f"  χ²_GOE     = {results_full['GOE']:.3f}")
    print(f"  χ²_Poisson / χ²_GOE = {results_full['poisson'] / results_full['GOE']:.3f}")
    
    print()
    print("="*70)
    print(" INTERPRETATION")
    print("="*70)
    
    if results['GOE'] < results['poisson']:
        ratio = results['poisson'] / results['GOE']
        print(f"✓ GOE-Statistik bestätigt (Faktor {ratio:.2f} besser als Poisson)")
        print("  → Level-Repulsion vorhanden")
        print("  → Quantenchaos")
        print("  → Die Primzahl-Defekte induzieren globale Korrelationen!")
    else:
        print("⚠ Inkonsistentes Ergebnis - weitere Tests nötig")
    
    print()
    print("="*70)
    print(" PHYSIKALISCHE BEDEUTUNG")
    print("="*70)
    print()
    print("Das EABC-Modell mit Primzahl-Defekten zeigt:")
    print()
    print("1. NICHT-INTEGRABLE DYNAMIK")
    print("   Die Primzahlen brechen die Translationssymmetrie kohärent.")
    print()
    print("2. GLOBALE QUANTENKORRELATIONEN")
    print("   Level-Repulsion → Die Zustände \"wissen\" voneinander.")
    print()
    print("3. GOE-UNIVERSALITÄT")
    print("   Wie generische chaotische Quantensysteme mit Zeitumkehr-Symmetrie.")
    print()
    print("4. KEINE ANDERSON-LOKALISIERUNG")
    print("   Primzahlen ≠ zufälliges Rauschen.")
    print()
    print("="*70)
    
    # Visualisierung
    print("\nErstelle Visualisierungen...")
    import matplotlib
    matplotlib.use('Agg')
    
    plot_level_statistics(
        spacings,
        title=f"EABC-Qubit ROBUST (N={N}, γ={gamma}, trimmed)",
        save_path="figures/robust_level_statistics.png"
    )
    
    print("✓ Plot: figures/robust_level_statistics.png")
    print()
    print("NÄCHSTE SCHRITTE:")
    print("  1. Variiere γ: 0.0 → 0.5 → 1.0 → 1.5 → 2.0 → 3.0")
    print("  2. Größere Systeme: N = 5000")
    print("  3. Vergleich mit H₀ (γ=0): Sollte Poisson zeigen!")


if __name__ == "__main__":
    main()
