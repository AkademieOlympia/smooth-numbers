#!/usr/bin/env python3
"""
EABC-Qubit: Die Kritischen Tests

TEST 1: Finite-Size-Scaling (N → 5000)
  Frage: Erreichen wir q → 1.0 bei mehr Primzahlen?
  
TEST 2: Chiralitäts-Test (β-Sweep)
  Frage: Ist die Z₄-Kopplung entscheidend für Chaos?
  Erwartung: β = 0 → Kollaps des Chaos!

Dies sind die entscheidenden Experimente zur Validierung des EABC-Modells.
"""

import numpy as np
import matplotlib.pyplot as plt
from src.hamiltonian import EABCHamiltonian
from src.spectral import spectral_unfolding
from src.level_spacing import compute_level_spacing, fit_level_statistics
from src.primes import generate_primes


def trim_spectrum(eigenvalues, trim_fraction=0.4):
    """Schneide Bandkanten ab."""
    n = len(eigenvalues)
    cut = int(n * trim_fraction / 2)
    return eigenvalues[cut:-cut]


def analyze_system(N, alpha, beta, gamma, k=500, trim=True, verbose=True):
    """Vollständige Analyse eines EABC-Systems."""
    if verbose:
        print(f"  N={N}, α={alpha:.2f}, β={beta:.2f}, γ={gamma:.2f} ... ", 
              end="", flush=True)
    
    # Hamiltonian
    H = EABCHamiltonian(N, alpha, beta, gamma)
    
    # Spektrum
    eigenvalues = H.compute_spectrum(k=k, which='SM', return_eigenvectors=False)
    
    # Trimming
    if trim:
        eigenvalues = trim_spectrum(eigenvalues, trim_fraction=0.4)
    
    # Unfolding
    unfolded = spectral_unfolding(eigenvalues, method='polynomial')
    
    # Spacings
    spacings = compute_level_spacing(unfolded)
    
    # Fit
    results = fit_level_statistics(spacings)
    
    # Beste Fit
    chi2_dict = {k: v for k, v in results.items() if k != 'brody_q'}
    best = min(chi2_dict, key=chi2_dict.get)
    q = results['brody_q']
    
    if verbose:
        print(f"✓ {best.upper()} (q={q:.3f})" if not np.isnan(q) else f"✓ {best.upper()}")
    
    return results


def test_finite_size_scaling():
    """
    TEST 1: Finite-Size-Scaling
    
    Vergrößere das System von N = 1000 → 5000
    Fixiere γ = 1.0 (Resonanz)
    
    Erwartung: q sollte näher an 1.0 kommen
    """
    print("="*70)
    print(" TEST 1: Finite-Size-Scaling")
    print("="*70)
    print()
    print("Frage: Erreichen wir vollständiges GOE (q → 1.0) bei mehr Primzahlen?")
    print()
    print("Methode:")
    print("  - Fixiere γ = 1.0 (Resonanz-Punkt)")
    print("  - Variiere N: 500 → 1000 → 2000 → 3000 → 5000")
    print("  - Erwartung: q(N) → 1.0 für N → ∞")
    print()
    print("-" * 70)
    print()
    
    # Parameter
    alpha = 1.0
    beta = 0.5
    gamma = 1.0  # Resonanz!
    
    N_values = [500, 1000, 2000, 3000, 5000]
    k_values = [300, 500, 800, 1000, 1500]  # Skaliere k mit N
    
    results_list = []
    
    for N, k in zip(N_values, k_values):
        # Zähle Primzahlen
        primes = generate_primes(N)
        n_primes = len(primes)
        
        print(f"N = {N:5d}  ({n_primes:3d} Primzahlen, k={k:4d} Eigenwerte)")
        
        try:
            results = analyze_system(N, alpha, beta, gamma, k=k, trim=True, verbose=True)
            results['N'] = N
            results['n_primes'] = n_primes
            results_list.append(results)
        except Exception as e:
            print(f"    ✗ Fehler: {e}")
            results_list.append(None)
        
        print()
    
    print("="*70)
    print(" ERGEBNISSE: Finite-Size-Scaling")
    print("="*70)
    print()
    print("N       #Primes   χ²_Poisson  χ²_GOE    Brody-q   Trend")
    print("-" * 70)
    
    valid_results = [r for r in results_list if r is not None]
    
    for res in valid_results:
        N = res['N']
        np_val = res['n_primes']
        chi2_p = res['poisson']
        chi2_g = res['GOE']
        q = res['brody_q']
        
        # Trend
        if q < 0.3:
            trend = "Poisson-like"
        elif q < 0.7:
            trend = "Crossover"
        elif q < 0.9:
            trend = "Fast GOE"
        else:
            trend = "GOE!"
        
        q_str = f"{q:.3f}" if not np.isnan(q) else "N/A"
        print(f"{N:5d}   {np_val:5d}     {chi2_p:8.3f}  {chi2_g:8.3f}  {q_str:>7s}   {trend}")
    
    print()
    print("INTERPRETATION:")
    print("-" * 70)
    
    if len(valid_results) >= 3:
        # Extraktion q(N)
        q_values = [r['brody_q'] for r in valid_results if not np.isnan(r['brody_q'])]
        N_vals = [r['N'] for r in valid_results if not np.isnan(r['brody_q'])]
        
        if len(q_values) >= 3:
            q_trend = np.polyfit(np.log(N_vals), q_values, deg=1)
            slope = q_trend[0]
            
            print(f"q(N) Trend: {'steigend' if slope > 0 else 'fallend'}")
            print(f"Slope: {slope:.4f} pro log(N)")
            print()
            
            if slope > 0.01:
                print("✓ FINITE-SIZE-EFFEKT BESTÄTIGT!")
                print("  → q steigt mit N")
                print("  → Bei größeren Systemen nähert sich das System GOE")
                
                # Extrapolation
                if slope > 0:
                    N_extrap = np.exp((1.0 - q_trend[1]) / q_trend[0])
                    if N_extrap < 1e6:
                        print(f"  → Extrapolation: q = 1.0 bei N ≈ {N_extrap:.0f}")
            else:
                print("⚠ q saturiert")
                print("  → Mögliche systematische Barriere bei q ≈ {:.2f}".format(q_values[-1]))
                print("  → Das System erreicht nicht vollständiges GOE")
    
    print()
    
    return results_list


def test_chirality_sweep():
    """
    TEST 2: Chiralitäts-Test (β-Sweep)
    
    Variiere die chirale Kopplung β bei festem γ = 1.0
    
    Entscheidende Frage:
    Falls β = 0 → Kein Chaos
    dann ist die EABC-Klassifikation PHYSIKALISCH ENTSCHEIDEND!
    """
    print("="*70)
    print(" TEST 2: Chiralitäts-Test (β-Sweep)")
    print("="*70)
    print()
    print("DIE ENTSCHEIDENDE FRAGE:")
    print("  Ist die Z₄-Chiralität (EABC-Klassifikation) entscheidend für Chaos?")
    print()
    print("Methode:")
    print("  - Fixiere γ = 1.0 (Resonanz), N = 1000")
    print("  - Variiere β: 0.0 → 0.1 → 0.3 → 0.5 → 1.0")
    print("  - β = 0: Keine chirale Kopplung → nur Primzahl-Positionen zählen")
    print("  - β > 0: Chirale Modulation aktiv")
    print()
    print("ERWARTUNG:")
    print("  Falls β = 0 → q fällt drastisch (kein Chaos)")
    print("  → Dann ist EABC physikalisch ENTSCHEIDEND!")
    print()
    print("-" * 70)
    print()
    
    # Parameter
    N = 1000
    alpha = 1.0
    gamma = 1.0  # Resonanz!
    
    beta_values = [0.0, 0.1, 0.2, 0.3, 0.5, 0.7, 1.0]
    
    results_list = []
    
    for beta in beta_values:
        print(f"β = {beta:.2f}  ", end="", flush=True)
        
        try:
            results = analyze_system(N, alpha, beta, gamma, k=500, trim=True, verbose=True)
            results['beta'] = beta
            results_list.append(results)
        except Exception as e:
            print(f"✗ Fehler: {e}")
            results_list.append(None)
    
    print()
    print("="*70)
    print(" ERGEBNISSE: Chiralitäts-Sweep")
    print("="*70)
    print()
    print("β       χ²_Poisson  χ²_GOE    χ²_GUE    Brody-q   Interpretation")
    print("-" * 70)
    
    valid_results = [r for r in results_list if r is not None]
    
    for res in valid_results:
        beta = res['beta']
        chi2_p = res['poisson']
        chi2_g = res['GOE']
        chi2_u = res['GUE']
        q = res['brody_q']
        
        # Interpretation
        if beta == 0.0:
            if q < 0.3:
                interp = "Kein Chaos → EABC kritisch!"
            else:
                interp = "Noch Chaos → EABC nicht allein"
        else:
            if q < 0.3:
                interp = "Poisson-like"
            elif q < 0.7:
                interp = "Crossover"
            else:
                interp = "Fast GOE"
        
        q_str = f"{q:.3f}" if not np.isnan(q) else "N/A"
        print(f"{beta:4.2f}    {chi2_p:8.3f}  {chi2_g:8.3f}  {chi2_u:8.3f}  {q_str:>7s}   {interp}")
    
    print()
    print("INTERPRETATION:")
    print("-" * 70)
    
    # Kritischer Vergleich: β = 0 vs. β > 0
    beta_zero = [r for r in valid_results if r['beta'] == 0.0]
    beta_nonzero = [r for r in valid_results if r['beta'] > 0.3]
    
    if beta_zero and beta_nonzero:
        q_zero = beta_zero[0]['brody_q']
        q_large = np.mean([r['brody_q'] for r in beta_nonzero if not np.isnan(r['brody_q'])])
        
        print(f"β = 0.0:     q = {q_zero:.3f}")
        print(f"β ≥ 0.3:     q = {q_large:.3f} (Mittelwert)")
        print()
        
        delta_q = q_large - q_zero
        
        if delta_q > 0.2:
            print("✓✓✓ DRAMATISCHER EFFEKT!")
            print(f"  Δq = {delta_q:.3f}")
            print()
            print("SCHLUSSFOLGERUNG:")
            print("  Die Z₄-Chiralität (EABC-Klassifikation) ist ENTSCHEIDEND!")
            print("  Ohne chirale Kopplung kollabiert das Chaos.")
            print()
            print("  → Die Primzahlen allein (ohne EABC) reichen NICHT!")
            print("  → Die arithmetische Modulo-12-Struktur ist PHYSIKALISCH RELEVANT!")
        elif delta_q > 0.1:
            print("✓ MESSBARER EFFEKT")
            print(f"  Δq = {delta_q:.3f}")
            print("  Die Chiralität verstärkt das Chaos, aber ist nicht allein verantwortlich")
        else:
            print("⚠ SCHWACHER EFFEKT")
            print(f"  Δq = {delta_q:.3f}")
            print("  Die Chiralität scheint weniger wichtig zu sein")
            print("  → Primzahl-Positionen dominieren über EABC-Klassifikation")
    
    print()
    
    return results_list


def create_combined_plot(size_results, beta_results):
    """Erstelle kombinierte Visualisierung."""
    import matplotlib
    matplotlib.use('Agg')
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Plot 1: Finite-Size-Scaling
    ax = axes[0]
    
    valid_size = [r for r in size_results if r is not None and not np.isnan(r.get('brody_q', np.nan))]
    
    if valid_size:
        N_vals = [r['N'] for r in valid_size]
        q_vals = [r['brody_q'] for r in valid_size]
        n_primes = [r['n_primes'] for r in valid_size]
        
        # Plot gegen N
        ax.plot(N_vals, q_vals, 'o-', color='purple', lw=2, markersize=10, label='q(N)')
        
        # Fit
        if len(N_vals) >= 3:
            fit = np.polyfit(np.log(N_vals), q_vals, deg=1)
            N_fit = np.linspace(min(N_vals), max(N_vals), 100)
            q_fit = fit[0] * np.log(N_fit) + fit[1]
            ax.plot(N_fit, q_fit, 'r--', lw=1, alpha=0.5, label=f'Fit: q ∝ {fit[0]:.3f}·ln(N)')
        
        ax.axhline(1, color='green', linestyle='--', lw=2, label='q=1 (GOE)')
        ax.axhline(0, color='red', linestyle='--', lw=1, label='q=0 (Poisson)')
        
        ax.set_xlabel('Systemgröße N', fontsize=12)
        ax.set_ylabel('Brody-Parameter q', fontsize=12)
        ax.set_title('Finite-Size-Scaling: q(N) bei γ=1.0', fontsize=13, fontweight='bold')
        ax.legend(fontsize=10)
        ax.set_xscale('log')
        ax.set_ylim(-0.1, 1.1)
        ax.grid(alpha=0.3)
        
        # Sekundäre Achse: Anzahl Primzahlen
        ax2 = ax.twiny()
        ax2.set_xlim(ax.get_xlim())
        ax2.set_xscale('log')
        # Primzahl-Ticks
        prime_ticks = [r['n_primes'] for r in valid_size]
        ax2.set_xticks(N_vals)
        ax2.set_xticklabels([f"{p}" for p in prime_ticks], fontsize=9)
        ax2.set_xlabel('Anzahl Primzahlen', fontsize=10, color='gray')
    
    # Plot 2: β-Sweep
    ax = axes[1]
    
    valid_beta = [r for r in beta_results if r is not None and not np.isnan(r.get('brody_q', np.nan))]
    
    if valid_beta:
        beta_vals = [r['beta'] for r in valid_beta]
        q_vals = [r['brody_q'] for r in valid_beta]
        
        ax.plot(beta_vals, q_vals, 'o-', color='blue', lw=2, markersize=10, label='q(β)')
        
        ax.axhline(1, color='green', linestyle='--', lw=1, label='q=1 (GOE)')
        ax.axhline(0, color='red', linestyle='--', lw=1, label='q=0 (Poisson)')
        
        # Markiere β=0
        if any(b == 0.0 for b in beta_vals):
            idx = beta_vals.index(0.0)
            ax.plot(0.0, q_vals[idx], 'ro', markersize=15, alpha=0.5, 
                   label=f'β=0: q={q_vals[idx]:.3f}')
        
        ax.set_xlabel('Chirale Kopplung β', fontsize=12)
        ax.set_ylabel('Brody-Parameter q', fontsize=12)
        ax.set_title('Chiralitäts-Test: q(β) bei γ=1.0', fontsize=13, fontweight='bold')
        ax.legend(fontsize=10)
        ax.set_ylim(-0.1, 1.1)
        ax.grid(alpha=0.3)
        
        # Färbe Bereiche
        ax.axhspan(0, 0.3, alpha=0.1, color='red')
        ax.axhspan(0.7, 1.0, alpha=0.1, color='green')
    
    fig.suptitle('EABC-Qubit: Kritische Tests', fontsize=15, fontweight='bold')
    plt.tight_layout()
    
    plt.savefig('figures/critical_tests.png', dpi=300, bbox_inches='tight')
    print("\n✓ Plot gespeichert: figures/critical_tests.png")


def main():
    print("\n")
    print("╔" + "="*68 + "╗")
    print("║" + " "*68 + "║")
    print("║" + "  EABC-QUBIT: DIE KRITISCHEN TESTS".center(68) + "║")
    print("║" + " "*68 + "║")
    print("║" + "  Finite-Size-Scaling + Chiralitäts-Validierung".center(68) + "║")
    print("║" + " "*68 + "║")
    print("╚" + "="*68 + "╝")
    print()
    
    # Test 1: Finite-Size-Scaling
    print("\n" + "▶"*35)
    size_results = test_finite_size_scaling()
    
    # Test 2: Chiralitäts-Sweep
    print("\n" + "▶"*35)
    beta_results = test_chirality_sweep()
    
    # Visualisierung
    print()
    print("="*70)
    print(" VISUALISIERUNG")
    print("="*70)
    create_combined_plot(size_results, beta_results)
    
    # Finale Zusammenfassung
    print()
    print("="*70)
    print(" FINALE ZUSAMMENFASSUNG")
    print("="*70)
    print()
    print("Diese beiden Tests entscheiden über die Validität des EABC-Modells:")
    print()
    print("1. FINITE-SIZE-SCALING:")
    print("   Falls q(N) → 1.0 für N → ∞")
    print("   → Das System erreicht vollständiges GOE")
    print("   → Die Primzahlen erzeugen universelles Quantenchaos")
    print()
    print("2. CHIRALITÄTS-TEST:")
    print("   Falls q(β=0) << q(β>0)")
    print("   → Die EABC-Klassifikation ist PHYSIKALISCH ENTSCHEIDEND")
    print("   → Primzahl-Positionen allein reichen nicht")
    print("   → Die Modulo-12-Arithmetik ist fundamental")
    print()
    print("="*70)


if __name__ == "__main__":
    main()
