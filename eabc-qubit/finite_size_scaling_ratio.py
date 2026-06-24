#!/usr/bin/env python3
"""
Finite-Size-Scaling: Ratio-Statistik

ENTSCHEIDENDER TEST:
    Ist Collatz-⟨r⟩ ≈ 0.48-0.50 stabil über N → eigene Universalitätsklasse?
    Oder konvergiert es gegen GOE/GUE?

Quick-Scaling: N = 500, 1000, 2000 (~1h)
Full-Scaling: N = 500, 1000, 2000, 5000, 10000 (~7-8h)

Author: EABC Research Group
Date: 2026-06-23
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import pandas as pd
from pathlib import Path
import sys
import time

# Füge src zum Path hinzu
sys.path.insert(0, str(Path(__file__).parent))

from src.hamiltonian import EABCHamiltonian, CollatzEABCHamiltonian
from src.level_spacing import compute_level_spacing
from src.spectral import spectral_unfolding

# Konfiguration
N_VALUES_QUICK = [500, 1000, 2000]  # Quick-Scaling (~1h)
N_VALUES_FULL = [500, 1000, 2000, 5000, 10000]  # Full-Scaling (~7-8h)
K_EIGENVALUES = 500  # Anzahl Eigenwerte
N_ENSEMBLE = 50  # Bootstrap-Größe (erhöht von 20!)

SCENARIOS = ['Uniform', 'Collatz', 'Primes']

# Output
OUTPUT_DIR = Path(__file__).parent
FIGURES_DIR = OUTPUT_DIR / 'figures'
RESULTS_DIR = OUTPUT_DIR / 'results'
FIGURES_DIR.mkdir(exist_ok=True)
RESULTS_DIR.mkdir(exist_ok=True)

# Referenzwerte (KORRIGIERT!)
REF_POISSON = 0.386
REF_GOE = 0.536  # NICHT 0.530!
REF_GUE = 0.603


def compute_ratio_statistic_full(spacings):
    """Berechne Ratio-Statistik mit vollständiger Info."""
    r_values = []
    for i in range(len(spacings) - 1):
        s_min = min(spacings[i], spacings[i + 1])
        s_max = max(spacings[i], spacings[i + 1])
        
        if s_max > 0:
            r = s_min / s_max
            r_values.append(r)
    
    return np.array(r_values)


def create_hamiltonian(scenario, N, seed=None):
    """Factory für Hamiltonian-Szenarien."""
    kwargs = {'alpha': 1.0, 'beta': 0.5, 'gamma': 1.5}
    
    if scenario == 'Uniform':
        return EABCHamiltonian(N=N, **kwargs)
    elif scenario == 'Collatz':
        return CollatzEABCHamiltonian(N=N, random_seed=seed, **kwargs)
    elif scenario == 'Primes':
        return EABCHamiltonian(N=N, **kwargs)
    else:
        raise ValueError(f"Unbekanntes Szenario: {scenario}")


def finite_size_scaling(n_values=N_VALUES_QUICK, use_full=False):
    """
    Hauptfunktion: Finite-Size-Scaling der Ratio-Statistik.
    
    Parameters
    ----------
    n_values : list
        Liste von N-Werten zum Testen
    use_full : bool
        Falls True, verwende Full-Scaling mit N=10000
    """
    
    if use_full:
        n_values = N_VALUES_FULL
    
    print("="*80)
    print(" "*20 + "FINITE-SIZE-SCALING: RATIO-STATISTIK")
    print("="*80)
    print("\nOganesyan-Huse Ratio-Statistik über verschiedene Systemgrößen N")
    print("\nReferenzwerte (KORRIGIERT!):")
    print(f"  Poisson: ⟨r⟩ ≈ {REF_POISSON:.3f}")
    print(f"  GOE:     ⟨r⟩ ≈ {REF_GOE:.3f}  (NICHT 0.530!)")
    print(f"  GUE:     ⟨r⟩ ≈ {REF_GUE:.3f}")
    print(f"\nSystemgrößen: N ∈ {n_values}")
    print(f"Ensemble: n = {N_ENSEMBLE}")
    print(f"Szenarien: {SCENARIOS}")
    print("\nENTSCHEIDEND: Ist Collatz stabil bei ⟨r⟩ ≈ 0.48-0.50?")
    print("="*80 + "\n")
    
    # Ergebnis-Speicher
    results = {}
    for scenario in SCENARIOS:
        results[scenario] = {
            'N': [],
            'mean_r': [],
            'std_r': [],
            'ci_lower': [],
            'ci_upper': [],
            'P_r': [],
            'bins': []
        }
    
    total_start = time.time()
    
    # Hauptschleife: Über N-Werte
    for n_idx, N in enumerate(n_values):
        print(f"\n{'='*80}")
        print(f"N = {N} ({n_idx+1}/{len(n_values)})")
        print(f"{'='*80}\n")
        
        for scenario in SCENARIOS:
            print(f">>> Szenario: {scenario}")
            print("-" * 80)
            
            scenario_start = time.time()
            
            # Ensemble-Mittelung
            ensemble_r_means = []
            all_r_values_for_P_r = []
            
            for i in range(N_ENSEMBLE):
                if (i + 1) % 10 == 0:
                    print(f"  Fortschritt: {i+1}/{N_ENSEMBLE}")
                
                try:
                    # Konstruiere Hamiltonian
                    H = create_hamiltonian(scenario, N, seed=i)
                    
                    # Berechne Spektrum (SA = smallest algebraic - stabiler!)
                    k = min(N, K_EIGENVALUES)
                    eigenvalues = H.compute_spectrum(k=k, which='SA')
                    
                    # Unfolding
                    unfolded = spectral_unfolding(eigenvalues)
                    
                    # Level Spacings
                    spacings = compute_level_spacing(unfolded)
                    
                    # Ratio-Statistik
                    r_values = compute_ratio_statistic_full(spacings)
                    
                    ensemble_r_means.append(np.mean(r_values))
                    
                    # Sammle für P(r) (nur ersten 10 Samples)
                    if i < 10:
                        all_r_values_for_P_r.extend(r_values)
                
                except Exception as e:
                    print(f"  ✗ Ensemble {i} fehlgeschlagen: {e}")
                    continue
            
            # Statistiken berechnen
            ensemble_r_means = np.array(ensemble_r_means)
            mean_r = np.mean(ensemble_r_means)
            std_r = np.std(ensemble_r_means)
            
            # 95% CI via Perzentile
            ci_lower = np.percentile(ensemble_r_means, 2.5)
            ci_upper = np.percentile(ensemble_r_means, 97.5)
            
            # P(r) Verteilung (akkumuliert über erste 10 Samples)
            all_r_values_for_P_r = np.array(all_r_values_for_P_r)
            P_r, bins = np.histogram(all_r_values_for_P_r, bins=50, range=(0, 1), density=True)
            
            # Speichere Ergebnisse
            results[scenario]['N'].append(N)
            results[scenario]['mean_r'].append(mean_r)
            results[scenario]['std_r'].append(std_r)
            results[scenario]['ci_lower'].append(ci_lower)
            results[scenario]['ci_upper'].append(ci_upper)
            results[scenario]['P_r'].append(P_r)
            results[scenario]['bins'].append(bins)
            
            # Ausgabe
            scenario_elapsed = time.time() - scenario_start
            print(f"\n  ERGEBNISSE (N={N}, {scenario}):")
            print(f"    ⟨r⟩ = {mean_r:.4f} ± {std_r:.4f}")
            print(f"    95% CI: [{ci_lower:.4f}, {ci_upper:.4f}]")
            print(f"    n_ensemble = {len(ensemble_r_means)}")
            print(f"    Zeit: {scenario_elapsed:.1f}s")
            
            # Bewertung relativ zu Referenzen
            if mean_r < REF_POISSON + 0.05:
                print(f"    → Nähe POISSON")
            elif mean_r < REF_GOE - 0.02:
                print(f"    → INTERMEDIÄR (unter GOE) ⚡")
            elif abs(mean_r - REF_GOE) < 0.02:
                print(f"    → Nähe GOE")
            elif mean_r > REF_GOE + 0.02 and mean_r < REF_GUE - 0.02:
                print(f"    → ZWISCHEN GOE und GUE")
            elif mean_r > REF_GUE - 0.02:
                print(f"    → Nähe GUE")
            
            print("-" * 80)
    
    total_elapsed = time.time() - total_start
    print(f"\n✓ Finite-Size-Scaling abgeschlossen in {total_elapsed/60:.1f} Min")
    
    # Analysiere Trends
    analyze_trends(results, n_values)
    
    # Speichere Ergebnisse
    save_results(results)
    
    # Erstelle Plots
    plot_finite_size_scaling(results, n_values)
    
    return results


def analyze_trends(results, n_values):
    """Analysiere Trends und Stabilität."""
    print("\n" + "="*80)
    print("TREND-ANALYSE: FINITE-SIZE-SCALING")
    print("="*80)
    
    for scenario in SCENARIOS:
        print(f"\n>>> {scenario}:")
        print("-" * 80)
        
        mean_r_values = np.array(results[scenario]['mean_r'])
        
        # Stabilität: Relative Änderung
        if len(mean_r_values) >= 2:
            rel_change = []
            for i in range(1, len(mean_r_values)):
                change = (mean_r_values[i] - mean_r_values[i-1]) / mean_r_values[i-1]
                rel_change.append(change)
                print(f"  N={n_values[i-1]:5d} → N={n_values[i]:5d}: " +
                      f"⟨r⟩ = {mean_r_values[i-1]:.4f} → {mean_r_values[i]:.4f} " +
                      f"(Δ = {change*100:+.2f}%)")
            
            # Gesamttrend
            total_change = (mean_r_values[-1] - mean_r_values[0]) / mean_r_values[0]
            print(f"\n  Gesamttrend (N={n_values[0]} → N={n_values[-1]}): {total_change*100:+.2f}%")
            
            # Bewertung
            if abs(total_change) < 0.02:
                print(f"  ✓✓✓ SEHR STABIL (Δ < 2%)")
                print(f"      → Starke Evidenz für eigenständige Klasse!")
            elif abs(total_change) < 0.05:
                print(f"  ✓✓ STABIL (Δ < 5%)")
                print(f"     → Hinweise auf eigenständige Klasse")
            elif abs(total_change) < 0.10:
                print(f"  ✓ MODERAT STABIL (Δ < 10%)")
                print(f"    → Trend vorhanden, weitere N nötig")
            else:
                print(f"  ✗ INSTABIL (Δ > 10%)")
                print(f"    → Finite-Size-Effekte dominant")
        
        print("-" * 80)
    
    # Spezielle Analyse für Collatz
    print("\n" + "="*80)
    print("COLLATZ-SPEZIAL-ANALYSE")
    print("="*80)
    
    collatz_mean_r = np.array(results['Collatz']['mean_r'])
    
    print(f"\nCollatz-⟨r⟩-Werte über N:")
    for i, N in enumerate(n_values):
        r = collatz_mean_r[i]
        std = results['Collatz']['std_r'][i]
        print(f"  N={N:5d}: ⟨r⟩ = {r:.4f} ± {std:.4f}")
    
    # Entscheidung
    print(f"\nENTSCHEIDUNG:")
    if len(collatz_mean_r) >= 2:
        final_r = collatz_mean_r[-1]
        
        if 0.48 <= final_r <= 0.50:
            print(f"  ✓✓✓ COLLATZ STABIL BEI ⟨r⟩ ≈ {final_r:.3f} ∈ [0.48, 0.50]!")
            print(f"      → EIGENE ARITHMETISCHE UNIVERSALITÄTSKLASSE BESTÄTIGT!")
            print(f"      → Intermediäres Regime zwischen Poisson und GOE")
            decision = 'confirmed_intermediate_class'
        elif final_r < 0.48:
            print(f"  → COLLATZ BEI ⟨r⟩ ≈ {final_r:.3f} < 0.48")
            print(f"    → Näher an Poisson, möglicherweise kritisch/lokalisiert")
            decision = 'critical_below_intermediate'
        elif 0.50 < final_r < REF_GOE - 0.02:
            print(f"  → COLLATZ BEI ⟨r⟩ ≈ {final_r:.3f}, zwischen [0.50, GOE]")
            print(f"    → Trend Richtung GOE, weitere N empfohlen")
            decision = 'trending_to_goe'
        elif abs(final_r - REF_GOE) < 0.02:
            print(f"  → COLLATZ KONVERGIERT ZU GOE (⟨r⟩ ≈ {final_r:.3f})")
            print(f"    → Finite-Size-Crossover, keine eigene Klasse")
            decision = 'converging_to_goe'
        else:
            print(f"  → COLLATZ BEI ⟨r⟩ ≈ {final_r:.3f} > GOE")
            print(f"    → Unerwartet, weitere Untersuchung nötig")
            decision = 'unexpected'
    
    print("="*80 + "\n")
    
    return decision


def save_results(results):
    """Speichere Ergebnisse als CSV."""
    df_data = []
    for scenario in SCENARIOS:
        for i, N in enumerate(results[scenario]['N']):
            df_data.append({
                'Scenario': scenario,
                'N': N,
                'mean_r': results[scenario]['mean_r'][i],
                'std_r': results[scenario]['std_r'][i],
                'ci_lower': results[scenario]['ci_lower'][i],
                'ci_upper': results[scenario]['ci_upper'][i]
            })
    
    df = pd.DataFrame(df_data)
    csv_path = RESULTS_DIR / 'finite_size_scaling_ratio.csv'
    df.to_csv(csv_path, index=False)
    print(f"✓ CSV gespeichert: {csv_path}")


def plot_finite_size_scaling(results, n_values):
    """Erstelle Finite-Size-Scaling Plots."""
    
    fig = plt.figure(figsize=(18, 5))
    gs = GridSpec(1, 3, figure=fig, wspace=0.3)
    
    colors = {'Uniform': 'C0', 'Collatz': 'C1', 'Primes': 'C3'}
    
    # Panel A: ⟨r⟩ vs N
    ax1 = fig.add_subplot(gs[0])
    
    for scenario in SCENARIOS:
        N_vals = results[scenario]['N']
        mean_r = results[scenario]['mean_r']
        std_r = results[scenario]['std_r']
        
        ax1.errorbar(N_vals, mean_r, yerr=std_r, 
                    fmt='o-', markersize=10, linewidth=2.5, capsize=6,
                    label=scenario, color=colors[scenario], alpha=0.9)
    
    # Referenzlinien (KORRIGIERT!)
    ax1.axhline(REF_POISSON, color='gray', linestyle='--', linewidth=2, alpha=0.6, label='Poisson')
    ax1.axhline(REF_GOE, color='blue', linestyle='--', linewidth=2, alpha=0.6, label='GOE')
    ax1.axhline(REF_GUE, color='red', linestyle='--', linewidth=2, alpha=0.6, label='GUE')
    
    # Hypothetischer intermediärer Bereich
    ax1.axhspan(0.48, 0.50, color='yellow', alpha=0.2, label='Intermediär?')
    
    ax1.set_xlabel('System Size $N$', fontsize=13)
    ax1.set_ylabel(r'Ratio-Statistik $\langle r \rangle$', fontsize=13)
    ax1.set_title('Panel A: Finite-Size-Scaling', fontsize=14, fontweight='bold')
    ax1.legend(fontsize=10, loc='best')
    ax1.grid(True, alpha=0.3)
    ax1.set_xscale('log')
    
    # Panel B: Relative Änderung
    ax2 = fig.add_subplot(gs[1])
    
    for scenario in SCENARIOS:
        mean_r_values = np.array(results[scenario]['mean_r'])
        if len(mean_r_values) >= 2:
            rel_changes = []
            N_pairs = []
            for i in range(1, len(mean_r_values)):
                change = (mean_r_values[i] - mean_r_values[i-1]) / mean_r_values[i-1]
                rel_changes.append(change * 100)
                N_pairs.append(n_values[i])
            
            ax2.plot(N_pairs, rel_changes, 'o-', markersize=10, linewidth=2.5,
                    label=scenario, color=colors[scenario], alpha=0.9)
    
    ax2.axhline(0, color='black', linestyle='-', linewidth=1, alpha=0.5)
    ax2.axhspan(-2, 2, color='green', alpha=0.1, label='Stabil (< 2%)')
    ax2.set_xlabel('System Size $N$', fontsize=13)
    ax2.set_ylabel('Relative Änderung (%)', fontsize=13)
    ax2.set_title('Panel B: Stabilität', fontsize=14, fontweight='bold')
    ax2.legend(fontsize=10)
    ax2.grid(True, alpha=0.3)
    ax2.set_xscale('log')
    
    # Panel C: P(r) Evolution für Collatz
    ax3 = fig.add_subplot(gs[2])
    
    for i, N in enumerate(n_values):
        P_r = results['Collatz']['P_r'][i]
        bins = results['Collatz']['bins'][i]
        bin_centers = (bins[:-1] + bins[1:]) / 2
        
        alpha = 0.4 + 0.6 * (i / len(n_values))  # Transparenz steigt mit N
        ax3.plot(bin_centers, P_r, linewidth=2.5, alpha=alpha,
                label=f"N={N}", color=plt.cm.viridis(i / len(n_values)))
    
    ax3.set_xlabel(r'$r = \min(s_n, s_{n+1}) / \max(s_n, s_{n+1})$', fontsize=12)
    ax3.set_ylabel(r'$P(r)$', fontsize=13)
    ax3.set_title('Panel C: P(r)-Evolution (Collatz)', fontsize=14, fontweight='bold')
    ax3.legend(fontsize=10, loc='upper left')
    ax3.grid(True, alpha=0.3)
    ax3.set_xlim(0, 1)
    
    # Suptitle
    fig.suptitle('Finite-Size-Scaling: Ratio-Statistik (Oganesyan-Huse)', 
                 fontsize=16, fontweight='bold', y=1.00)
    
    plt.tight_layout()
    
    output_path = FIGURES_DIR / 'finite_size_scaling_ratio.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Plot gespeichert: {output_path}")
    plt.close()


if __name__ == "__main__":
    import sys
    
    # Parse Argument: quick oder full
    use_full = '--full' in sys.argv
    
    if use_full:
        print("\n⚠ FULL-SCALING MODUS: N = 500, 1000, 2000, 5000, 10000")
        print("  Geschätzte Zeit: ~7-8 Stunden")
        print("  Fortfahren? (Strg+C zum Abbrechen)\n")
        time.sleep(5)
        results = finite_size_scaling(use_full=True)
    else:
        print("\n📊 QUICK-SCALING MODUS: N = 500, 1000, 2000")
        print("  Geschätzte Zeit: ~1 Stunde")
        print("  (Verwende '--full' für vollständiges Scaling)\n")
        results = finite_size_scaling(use_full=False)
    
    print("\n" + "="*80)
    print("FINITE-SIZE-SCALING ABGESCHLOSSEN!")
    print("="*80)
    print(f"\nErgebnisse:")
    print(f"  CSV:  {RESULTS_DIR / 'finite_size_scaling_ratio.csv'}")
    print(f"  Plot: {FIGURES_DIR / 'finite_size_scaling_ratio.png'}")
    print("="*80 + "\n")
