"""
Vergleich: Statische Collatz-Gewichte vs. Dynamische Syracuse-Trajektorien

Dieses Skript vergleicht drei Hamiltonian-Varianten:

1. **Statisch (Collatz-EABC)**:
   Feste log(r)-Gewichte pro EABC-Klasse (Paper C)
   H_p^static = γ Σ_p log(r(p)) |p⟩⟨p| ⊗ |σ(p)⟩⟨σ(p)|

2. **Dynamisch (Tao-Syracuse)**:
   Echte Syracuse-Trajektorie von Startwert N₀
   H_p^dynamic = γ Σ_j λ_j(N₀) |S_j⟩⟨S_j| ⊗ |σ(S_j)⟩⟨σ(S_j)|

3. **Geom(2)-Ensemble**:
   Mittelung über viele Startwerte (Tao's statistische Vorhersage)

Zentrale Frage:
    Ist σ_dynamic ≈ σ_static ≈ 0.52 (GUE-Signatur)?
    → Falls JA: GUE-Chaos kommt direkt aus der Syracuse-Dynamik!
"""

import numpy as np
import matplotlib.pyplot as plt
from src.hamiltonian import EABCHamiltonian, CollatzEABCHamiltonian, TaoSyracuseHamiltonian
from src.level_spacing import compute_level_spacing
from src.spectral import spectral_unfolding, fit_wigner_surmise
from src.visualization import plot_level_spacing_comparison
import time


def analyze_single_hamiltonian(H, name: str, k: int = 500):
    """
    Analysiere ein einzelnes Hamiltonian-System.
    
    Parameters
    ----------
    H : Hamiltonian
        EABC-Hamiltonian-Instanz
    name : str
        Name für Plots
    k : int
        Anzahl Eigenwerte
    
    Returns
    -------
    dict
        Analyseergebnisse
    """
    print(f"\n{'='*70}")
    print(f"Analysiere: {name}")
    print(f"{'='*70}")
    
    # Spektrum berechnen
    start = time.time()
    E = H.compute_spectrum(k=k, which='SM')
    elapsed = time.time() - start
    print(f"✓ Spektrum berechnet in {elapsed:.2f}s")
    
    # Spectral Unfolding
    E_unfolded = spectral_unfolding(E)
    
    # Level Spacings
    spacings = compute_level_spacing(E_unfolded)
    
    # Statistik
    mean_s = np.mean(spacings)
    std_s = np.std(spacings)
    
    print(f"\nLevel-Spacing-Statistik:")
    print(f"  Anzahl Spacings: {len(spacings)}")
    print(f"  ⟨s⟩ = {mean_s:.6f}")
    print(f"  σ(s) = {std_s:.6f}")
    
    # Wigner-Surmise Fit
    try:
        beta_fit = fit_wigner_surmise(spacings)
        print(f"\nWigner-Surmise Fit:")
        print(f"  β ≈ {beta_fit:.3f}")
        
        if beta_fit < 0.5:
            regime = "Poisson (β=0, integrabel)"
        elif 0.5 <= beta_fit < 1.5:
            regime = "GOE (β=1, Zeit-Umkehr-Symmetrie)"
        elif 1.5 <= beta_fit < 3.0:
            regime = "GUE (β=2, broken TRS)"
        else:
            regime = "GSE (β=4, quaternionen)"
        
        print(f"  Regime: {regime}")
    except Exception as e:
        print(f"\nWigner-Surmise Fit fehlgeschlagen: {e}")
        beta_fit = None
        regime = "Unbekannt"
    
    return {
        'name': name,
        'eigenvalues': E,
        'eigenvalues_unfolded': E_unfolded,
        'spacings': spacings,
        'mean_spacing': mean_s,
        'std_spacing': std_s,
        'beta': beta_fit,
        'regime': regime,
        'computation_time': elapsed
    }


def compare_all_variants(N: int = 1000, k: int = 500, start_n: int = 27, trajectory_length: int = 50):
    """
    Vergleiche alle drei Hamiltonian-Varianten.
    
    Parameters
    ----------
    N : int
        Gittergröße
    k : int
        Anzahl Eigenwerte
    start_n : int
        Startwert für Syracuse-Trajektorie
    trajectory_length : int
        Länge der Syracuse-Trajektorie
    
    Returns
    -------
    dict
        Vergleichsresultate
    """
    print("="*70)
    print("VERGLEICH: Statisch vs. Dynamisch vs. Geom(2)")
    print("="*70)
    print(f"\nParameter:")
    print(f"  Gittergröße N:        {N}")
    print(f"  Eigenwerte k:         {k}")
    print(f"  Startwert N₀:         {start_n}")
    print(f"  Trajektorienlänge:    {trajectory_length}")
    
    # 1. Statisch (Collatz-EABC)
    H_static = CollatzEABCHamiltonian(N=N, alpha=1.0, beta=0.5, gamma=1.5)
    results_static = analyze_single_hamiltonian(H_static, "Statisch (Collatz-EABC)", k=k)
    
    # 2. Dynamisch (Tao-Syracuse)
    H_dynamic = TaoSyracuseHamiltonian(
        N=N, 
        start_n=start_n, 
        trajectory_length=trajectory_length,
        alpha=1.0, 
        beta=0.5, 
        gamma=1.5
    )
    results_dynamic = analyze_single_hamiltonian(H_dynamic, "Dynamisch (Tao-Syracuse)", k=k)
    
    # 3. Geom(2)-Synthetisch (Kontrolle)
    H_geom2 = TaoSyracuseHamiltonian(
        N=N,
        start_n=start_n,
        trajectory_length=trajectory_length,
        alpha=1.0,
        beta=0.5,
        gamma=1.5,
        use_geom2_synthetic=True
    )
    results_geom2 = analyze_single_hamiltonian(H_geom2, "Geom(2)-Synthetisch", k=k)
    
    # Zusammenfassung
    print("\n" + "="*70)
    print("ZUSAMMENFASSUNG")
    print("="*70)
    
    data = [
        ("Statisch (Collatz)", results_static),
        ("Dynamisch (Syracuse)", results_dynamic),
        ("Geom(2)-Synthetisch", results_geom2)
    ]
    
    print(f"\n{'Variante':<25} {'σ(s)':<12} {'β':<12} {'Regime':<20}")
    print("-"*70)
    for name, res in data:
        sigma = res['std_spacing']
        beta = res['beta'] if res['beta'] is not None else float('nan')
        regime = res['regime']
        print(f"{name:<25} {sigma:<12.4f} {beta:<12.3f} {regime:<20}")
    
    # Interpretation
    print("\n" + "="*70)
    print("INTERPRETATION")
    print("="*70)
    
    sigma_static = results_static['std_spacing']
    sigma_dynamic = results_dynamic['std_spacing']
    sigma_geom2 = results_geom2['std_spacing']
    
    # GUE-Referenzwert (theoretisch)
    sigma_gue = 0.52
    
    diff_static = abs(sigma_static - sigma_gue)
    diff_dynamic = abs(sigma_dynamic - sigma_gue)
    diff_geom2 = abs(sigma_geom2 - sigma_gue)
    
    print(f"\nAbweichung von σ_GUE ≈ 0.52:")
    print(f"  Statisch:   |{sigma_static:.4f} - 0.52| = {diff_static:.4f}")
    print(f"  Dynamisch:  |{sigma_dynamic:.4f} - 0.52| = {diff_dynamic:.4f}")
    print(f"  Geom(2):    |{sigma_geom2:.4f} - 0.52| = {diff_geom2:.4f}")
    
    print("\n" + "-"*70)
    
    # Hypothesentests
    threshold = 0.05  # 5% Toleranz
    
    if diff_dynamic < threshold:
        print("✓ HYPOTHESE A BESTÄTIGT:")
        print("  Die dynamische Syracuse-Trajektorie zeigt GUE-Chaos!")
        print("  → Die GUE-Signatur ist intrinsisch zur Collatz-Dynamik.")
    else:
        print("✗ HYPOTHESE A VERWORFEN:")
        print("  Die dynamische Syracuse-Trajektorie zeigt KEINE GUE-Signatur.")
        print("  → Die statischen EABC-Gewichte sind speziell.")
    
    print()
    
    if abs(sigma_static - sigma_dynamic) < threshold:
        print("✓ Statisch ≈ Dynamisch:")
        print("  Beide Varianten zeigen identische Spektralstatistik!")
        print("  → Die Mittelung über EABC-Klassen ist äquivalent zur Trajektorie.")
    else:
        print("✗ Statisch ≠ Dynamisch:")
        print("  Die beiden Varianten zeigen unterschiedliche Statistik.")
        print(f"  Differenz: |σ_static - σ_dynamic| = {abs(sigma_static - sigma_dynamic):.4f}")
    
    return {
        'static': results_static,
        'dynamic': results_dynamic,
        'geom2': results_geom2,
        'N': N,
        'k': k,
        'start_n': start_n,
        'trajectory_length': trajectory_length
    }


def plot_comparison(results: dict, save_path: str = None):
    """
    Erstelle Vergleichsplot aller drei Varianten.
    
    Parameters
    ----------
    results : dict
        Resultate von compare_all_variants()
    save_path : str, optional
        Pfad zum Speichern der Abbildung
    """
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    
    variants = [
        ('static', 'Statisch (Collatz-EABC)', 'blue'),
        ('dynamic', 'Dynamisch (Tao-Syracuse)', 'red'),
        ('geom2', 'Geom(2)-Synthetisch', 'green')
    ]
    
    for ax, (key, title, color) in zip(axes, variants):
        spacings = results[key]['spacings']
        
        # Histogram
        ax.hist(spacings, bins=50, density=True, alpha=0.6, color=color, edgecolor='black')
        
        # Wigner-Surmise (GUE)
        s = np.linspace(0, 4, 200)
        p_gue = (32 / np.pi**2) * s**2 * np.exp(-4 * s**2 / np.pi)
        ax.plot(s, p_gue, 'k--', linewidth=2, label='GUE (β=2)')
        
        # Statistik
        sigma = results[key]['std_spacing']
        beta = results[key]['beta']
        
        ax.set_title(f"{title}\nσ={sigma:.4f}, β≈{beta:.2f}" if beta is not None else f"{title}\nσ={sigma:.4f}")
        ax.set_xlabel('Level Spacing s')
        ax.set_ylabel('P(s)')
        ax.legend()
        ax.grid(alpha=0.3)
    
    plt.suptitle(f"Level-Spacing-Vergleich (N={results['N']}, k={results['k']})", fontsize=14, fontweight='bold')
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"\n✓ Plot gespeichert: {save_path}")
    
    plt.show()


def geom2_ensemble_test(N: int = 1000, n_samples: int = 50, k: int = 500, trajectory_length: int = 50):
    """
    Geom(2)-Ensemble-Test: Mittelung über viele Startwerte.
    
    Tao's Theorie sagt voraus: Für typische Startwerte N₀ sind die Spektren ähnlich.
    Dieser Test prüft, ob die Varianz über verschiedene Startwerte klein ist.
    
    Parameters
    ----------
    N : int
        Gittergröße
    n_samples : int
        Anzahl verschiedener Startwerte
    k : int
        Anzahl Eigenwerte
    trajectory_length : int
        Trajektorienlänge
    
    Returns
    -------
    dict
        Ensemble-Statistiken
    """
    print("\n" + "="*70)
    print(f"GEOM(2)-ENSEMBLE-TEST (n_samples={n_samples})")
    print("="*70)
    
    from src.syracuse_dynamics import random_coprime_6_odd
    
    sigmas = []
    betas = []
    
    for i in range(n_samples):
        # Zufälliger Startwert
        start_n = random_coprime_6_odd(N, seed=i)
        
        # Hamiltonian
        H = TaoSyracuseHamiltonian(
            N=N,
            start_n=start_n,
            trajectory_length=trajectory_length,
            alpha=1.0,
            beta=0.5,
            gamma=1.5
        )
        
        # Spektrum
        E = H.compute_spectrum(k=k, which='SM')
        E_unfolded = spectral_unfolding(E)
        spacings = compute_level_spacing(E_unfolded)
        
        sigma = np.std(spacings)
        sigmas.append(sigma)
        
        try:
            beta = fit_wigner_surmise(spacings)
            betas.append(beta)
        except:
            pass
        
        if (i + 1) % 10 == 0:
            print(f"  [{i+1}/{n_samples}] ⟨σ⟩ = {np.mean(sigmas):.4f} ± {np.std(sigmas):.4f}")
    
    mean_sigma = np.mean(sigmas)
    std_sigma = np.std(sigmas)
    mean_beta = np.mean(betas) if len(betas) > 0 else None
    
    print("\n" + "="*70)
    print("ENSEMBLE-RESULTATE")
    print("="*70)
    print(f"\nσ(s) über {n_samples} Startwerte:")
    print(f"  Mittelwert: {mean_sigma:.4f}")
    print(f"  Std.-Abw.:  {std_sigma:.4f}")
    print(f"  Min:        {min(sigmas):.4f}")
    print(f"  Max:        {max(sigmas):.4f}")
    
    if mean_beta is not None:
        print(f"\nβ (Wigner-Surmise) über {len(betas)} erfolgreiche Fits:")
        print(f"  Mittelwert: {mean_beta:.3f}")
        print(f"  Std.-Abw.:  {np.std(betas):.3f}")
    
    # Vergleich mit GUE
    sigma_gue = 0.52
    diff = abs(mean_sigma - sigma_gue)
    
    print(f"\nVergleich mit GUE (σ_GUE ≈ 0.52):")
    print(f"  Abweichung: {diff:.4f}")
    
    if diff < 0.05:
        print("  ✓ Ensemble-Mittel stimmt mit GUE überein!")
    else:
        print("  ✗ Ensemble-Mittel weicht von GUE ab.")
    
    return {
        'sigmas': sigmas,
        'betas': betas,
        'mean_sigma': mean_sigma,
        'std_sigma': std_sigma,
        'mean_beta': mean_beta,
        'n_samples': n_samples
    }


if __name__ == "__main__":
    import sys
    
    # Standardparameter
    N = 1000
    k = 500
    start_n = 27
    trajectory_length = 50
    
    # Kommandozeilenargumente
    if len(sys.argv) > 1:
        N = int(sys.argv[1])
    if len(sys.argv) > 2:
        k = int(sys.argv[2])
    
    print("\n" + "="*70)
    print("TAO-SYRACUSE-ERWEITERUNG: Statisch vs. Dynamisch")
    print("="*70)
    
    # Hauptvergleich
    results = compare_all_variants(N=N, k=k, start_n=start_n, trajectory_length=trajectory_length)
    
    # Plot
    plot_comparison(results, save_path='figures/static_vs_dynamic_comparison.png')
    
    # Optional: Geom(2)-Ensemble-Test
    print("\n\n")
    response = input("Geom(2)-Ensemble-Test durchführen? (dauert länger) [j/N]: ")
    if response.lower() == 'j':
        ensemble_results = geom2_ensemble_test(N=N, n_samples=50, k=k, trajectory_length=trajectory_length)
        
        # Ensemble-Plot
        plt.figure(figsize=(10, 6))
        plt.hist(ensemble_results['sigmas'], bins=20, density=True, alpha=0.7, color='purple', edgecolor='black')
        plt.axvline(x=0.52, color='red', linestyle='--', linewidth=2, label='σ_GUE = 0.52')
        plt.axvline(x=ensemble_results['mean_sigma'], color='green', linestyle='-', linewidth=2, 
                   label=f"⟨σ⟩_ensemble = {ensemble_results['mean_sigma']:.4f}")
        plt.xlabel('σ(s)')
        plt.ylabel('Häufigkeit')
        plt.title(f"Geom(2)-Ensemble-Verteilung (n={ensemble_results['n_samples']} Startwerte)")
        plt.legend()
        plt.grid(alpha=0.3)
        plt.tight_layout()
        plt.savefig('figures/geom2_ensemble_distribution.png', dpi=300, bbox_inches='tight')
        print("\n✓ Ensemble-Plot gespeichert: figures/geom2_ensemble_distribution.png")
        plt.show()
    
    print("\n" + "="*70)
    print("ANALYSE ABGESCHLOSSEN")
    print("="*70)
