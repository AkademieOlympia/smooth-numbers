#!/usr/bin/env python3
"""
Ratio-Statistik Quick-Check (HÖCHSTE PRIORITÄT!)

Oganesyan-Huse Ratio-Statistik: Unempfindlich gegen Unfolding-Artefakte!

ZIEL: Prüfe ob ⟨r⟩ stabil im Bereich [0.52, 0.68] mit konsistenter P(r)

Theoriewerte:
- Poisson: ⟨r⟩ ≈ 0.386
- GOE: ⟨r⟩ ≈ 0.530
- GUE: ⟨r⟩ ≈ 0.603

KRITISCH: Speichere die GESAMTE Verteilung P(r), nicht nur Mittelwert!

Author: EABC Research Group
Date: 2026-06-23
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import pandas as pd
from pathlib import Path
import sys

# Füge src zum Path hinzu
sys.path.insert(0, str(Path(__file__).parent))

from src.hamiltonian import (
    EABCHamiltonian, 
    CollatzEABCHamiltonian, 
    TaoSyracuseHamiltonian
)
from src.level_spacing import compute_level_spacing
from src.spectral import spectral_unfolding
from src.statistical_validation import ratio_statistic
from src.syracuse_dynamics import random_coprime_6_odd

# Konfiguration (reduziert für Geschwindigkeit)
N = 500  # Systemgröße (reduziert von 1000)
K = 200   # Anzahl Eigenwerte (reduziert von 500)
N_ENSEMBLE = 20  # Ensemble für Fehlerbalken (reduziert von 30)

# Szenarien
SCENARIOS = ['Uniform', 'Collatz', 'Syracuse', 'Primes']

# Output
OUTPUT_DIR = Path(__file__).parent
FIGURES_DIR = OUTPUT_DIR / 'figures'
RESULTS_DIR = OUTPUT_DIR / 'results'
FIGURES_DIR.mkdir(exist_ok=True)
RESULTS_DIR.mkdir(exist_ok=True)


def compute_ratio_statistic_full(spacings):
    """
    Berechne Ratio-Statistik mit vollständiger P(r)-Verteilung.
    
    r_n = min(s_n, s_{n+1}) / max(s_n, s_{n+1})
    
    Returns
    -------
    dict
        'mean': ⟨r⟩
        'std': σ_r
        'values': Array aller r_n
        'hist': P(r) Histogram
        'bins': Bin-Kanten
    """
    r_values = []
    for i in range(len(spacings) - 1):
        s_min = min(spacings[i], spacings[i + 1])
        s_max = max(spacings[i], spacings[i + 1])
        
        if s_max > 0:
            r = s_min / s_max
            r_values.append(r)
    
    r_values = np.array(r_values)
    
    # Histogram für P(r)
    hist, bins = np.histogram(r_values, bins=50, range=(0, 1), density=True)
    
    return {
        'mean': np.mean(r_values),
        'std': np.std(r_values),
        'values': r_values,
        'hist': hist,
        'bins': bins
    }


def create_hamiltonian(scenario, N, seed=None):
    """Factory für Hamiltonian-Szenarien."""
    kwargs = {'alpha': 1.0, 'beta': 0.5, 'gamma': 1.5}
    
    if scenario == 'Uniform':
        return EABCHamiltonian(N=N, **kwargs)
    elif scenario == 'Collatz':
        return CollatzEABCHamiltonian(N=N, random_seed=seed, **kwargs)
    elif scenario == 'Syracuse':
        start_n = random_coprime_6_odd(N, seed=seed if seed else 42)
        return TaoSyracuseHamiltonian(
            N=N, start_n=start_n, trajectory_length=50, **kwargs
        )
    elif scenario == 'Primes':
        return EABCHamiltonian(N=N, **kwargs)
    else:
        raise ValueError(f"Unbekanntes Szenario: {scenario}")


def ratio_statistic_quick_check():
    """Hauptfunktion: Ratio-Statistik Quick-Check."""
    
    print("="*80)
    print(" "*20 + "RATIO-STATISTIK QUICK-CHECK")
    print("="*80)
    print("\nOganesyan-Huse Ratio-Statistik: r_n = min(s_n, s_{n+1}) / max(s_n, s_{n+1})")
    print("\nTheoriewerte:")
    print("  Poisson: ⟨r⟩ ≈ 0.386")
    print("  GOE:     ⟨r⟩ ≈ 0.530")
    print("  GUE:     ⟨r⟩ ≈ 0.603")
    print("\nSystem: N = {}, k = {}, Ensemble = {}".format(N, K, N_ENSEMBLE))
    print("Szenarien: {}".format(SCENARIOS))
    print("="*80 + "\n")
    
    # Ergebnis-Speicher
    results = {}
    
    for scenario in SCENARIOS:
        print(f"\n>>> Szenario: {scenario}")
        print("-" * 80)
        
        # Ensemble-Mittelung
        ensemble_r_means = []
        ensemble_r_stds = []
        all_r_values = []
        P_r_accumulated = None
        
        for i in range(N_ENSEMBLE):
            if (i + 1) % 5 == 0:
                print(f"  Fortschritt: {i+1}/{N_ENSEMBLE}")
            
            try:
                # Konstruiere Hamiltonian
                H = create_hamiltonian(scenario, N, seed=i)
                
                # Berechne Spektrum (SA = smallest algebraic - stabiler!)
                eigenvalues = H.compute_spectrum(k=K, which='SA')
                
                # Unfolding
                unfolded = spectral_unfolding(eigenvalues)
                
                # Level Spacings
                spacings = compute_level_spacing(unfolded)
                
                # Ratio-Statistik (vollständig)
                r_results = compute_ratio_statistic_full(spacings)
                
                ensemble_r_means.append(r_results['mean'])
                ensemble_r_stds.append(r_results['std'])
                all_r_values.extend(r_results['values'])
                
                # Akkumuliere P(r)
                if P_r_accumulated is None:
                    P_r_accumulated = r_results['hist']
                    bins = r_results['bins']
                else:
                    P_r_accumulated += r_results['hist']
            
            except Exception as e:
                print(f"  ✗ Ensemble {i} fehlgeschlagen: {e}")
                continue
        
        # Mittle P(r) über Ensemble
        P_r_accumulated /= N_ENSEMBLE
        
        # Bootstrap für Konfidenzintervalle
        ensemble_r_means = np.array(ensemble_r_means)
        mean_r = np.mean(ensemble_r_means)
        std_r = np.std(ensemble_r_means)
        
        # 95% CI via Perzentile
        ci_lower = np.percentile(ensemble_r_means, 2.5)
        ci_upper = np.percentile(ensemble_r_means, 97.5)
        
        # Speichere Ergebnisse
        results[scenario] = {
            'mean_r': mean_r,
            'std_r': std_r,
            'ci_lower': ci_lower,
            'ci_upper': ci_upper,
            'ensemble_means': ensemble_r_means,
            'all_r_values': np.array(all_r_values),
            'P_r': P_r_accumulated,
            'bins': bins
        }
        
        # Ausgabe
        print(f"\n  ERGEBNISSE:")
        print(f"    ⟨r⟩ = {mean_r:.4f} ± {std_r:.4f}")
        print(f"    95% CI: [{ci_lower:.4f}, {ci_upper:.4f}]")
        print(f"    n_ensemble = {len(ensemble_r_means)}")
        print("-" * 80)
    
    # Bewertung
    print("\n" + "="*80)
    print("BEWERTUNG: UNIVERSALITÄTSKLASSE")
    print("="*80)
    
    # Extrahiere ⟨r⟩-Werte
    r_means = {sc: results[sc]['mean_r'] for sc in SCENARIOS}
    
    print("\n⟨r⟩-Werte (mit 95% CI):")
    for sc in SCENARIOS:
        r = results[sc]
        print(f"  {sc:<12}: ⟨r⟩ = {r['mean_r']:.4f} ± {r['std_r']:.4f}  [{r['ci_lower']:.4f}, {r['ci_upper']:.4f}]")
    
    # Prüfe Stabilität
    r_min = min(r_means.values())
    r_max = max(r_means.values())
    r_range = r_max - r_min
    
    print(f"\n⟨r⟩-Bereich über alle Szenarien:")
    print(f"  Min: {r_min:.4f}")
    print(f"  Max: {r_max:.4f}")
    print(f"  Δr:  {r_range:.4f}")
    
    # Referenz
    print(f"\nReferenzwerte:")
    print(f"  Poisson: ⟨r⟩ ≈ 0.386")
    print(f"  GOE:     ⟨r⟩ ≈ 0.530")
    print(f"  GUE:     ⟨r⟩ ≈ 0.603")
    
    # Hypothese-Check
    print(f"\nHYPOTHESE-CHECK:")
    target_min, target_max = 0.52, 0.68
    
    if target_min <= r_min and r_max <= target_max:
        print(f"  ✓✓✓ ALLE ⟨r⟩-WERTE IM BEREICH [{target_min}, {target_max}]!")
        print(f"      → ARITHMETISCHE UNIVERSALITÄTSKLASSE BESTÄTIGT!")
        decision = 'confirmed'
    elif r_min >= target_min - 0.03 and r_max <= target_max + 0.03:
        print(f"  ✓✓ MEISTE ⟨r⟩-WERTE NAHE [{target_min}, {target_max}]")
        print(f"     → Hinweise auf arithmetische Universalitätsklasse")
        print(f"     → WEITERMACHEN mit Finite-Size-Scaling")
        decision = 'hints'
    else:
        print(f"  ✗ ⟨r⟩-WERTE AUSSERHALB DES ERWARTETEN BEREICHS")
        print(f"    → Hypothese NICHT bestätigt")
        print(f"    → STOPPEN hier, keine weitere Analyse nötig")
        decision = 'rejected'
    
    print("="*80 + "\n")
    
    # Speichere Ergebnisse
    save_results(results)
    
    # Erstelle Plots
    plot_ratio_statistic_results(results)
    
    return results, decision


def save_results(results):
    """Speichere Ergebnisse als CSV und NPZ."""
    
    # CSV: Mittelwerte und CIs
    df_data = []
    for scenario, r in results.items():
        df_data.append({
            'Scenario': scenario,
            'N': N,
            'mean_r': r['mean_r'],
            'std_r': r['std_r'],
            'ci_lower': r['ci_lower'],
            'ci_upper': r['ci_upper'],
            'n_ensemble': len(r['ensemble_means'])
        })
    
    df = pd.DataFrame(df_data)
    csv_path = RESULTS_DIR / 'ratio_statistic_quick_check.csv'
    df.to_csv(csv_path, index=False)
    print(f"✓ CSV gespeichert: {csv_path}")
    
    # NPZ: Komplette P(r)-Verteilungen
    npz_data = {}
    for scenario, r in results.items():
        npz_data[f'{scenario}_P_r'] = r['P_r']
        npz_data[f'{scenario}_bins'] = r['bins']
        npz_data[f'{scenario}_all_r_values'] = r['all_r_values']
    
    npz_path = RESULTS_DIR / 'P_r_distributions.npz'
    np.savez(npz_path, **npz_data)
    print(f"✓ NPZ gespeichert: {npz_path}")


def plot_ratio_statistic_results(results):
    """Erstelle publikationsreife Plots."""
    
    fig = plt.figure(figsize=(16, 5))
    gs = GridSpec(1, 3, figure=fig, wspace=0.3)
    
    scenarios = list(results.keys())
    colors = ['C0', 'C1', 'C2', 'C3']
    
    # Panel A: ⟨r⟩ mit Fehlerbalken
    ax1 = fig.add_subplot(gs[0])
    
    x_pos = np.arange(len(scenarios))
    means = [results[sc]['mean_r'] for sc in scenarios]
    stds = [results[sc]['std_r'] for sc in scenarios]
    ci_lowers = [results[sc]['ci_lower'] for sc in scenarios]
    ci_uppers = [results[sc]['ci_upper'] for sc in scenarios]
    
    ax1.errorbar(x_pos, means, yerr=stds, fmt='o', 
                 markersize=12, capsize=6, linewidth=2.5, label='⟨r⟩ ± σ')
    
    # 95% CI als Fehlerbalken
    for i, sc in enumerate(scenarios):
        ax1.plot([i, i], [ci_lowers[i], ci_uppers[i]], 
                linewidth=4, alpha=0.3, color=colors[i])
    
    # Referenzlinien
    ax1.axhline(y=0.386, color='gray', linestyle='--', linewidth=1.5, alpha=0.6, label='Poisson')
    ax1.axhline(y=0.530, color='blue', linestyle='--', linewidth=1.5, alpha=0.6, label='GOE')
    ax1.axhline(y=0.603, color='red', linestyle='--', linewidth=1.5, alpha=0.6, label='GUE')
    
    # Hypothesenbereich
    ax1.axhspan(0.52, 0.68, color='yellow', alpha=0.15, label='Arithmetische Klasse?')
    
    ax1.set_xticks(x_pos)
    ax1.set_xticklabels(scenarios, rotation=0, ha='center', fontsize=11)
    ax1.set_ylabel(r'Ratio-Statistik $\langle r \rangle$', fontsize=13)
    ax1.set_title('Panel A: Ratio-Statistik (N=1000)', fontsize=14, fontweight='bold')
    ax1.legend(fontsize=9, loc='upper right')
    ax1.grid(True, alpha=0.3, axis='y')
    ax1.set_ylim(0.35, 0.72)
    
    # Panel B: P(r) Verteilungen für N=1000
    ax2 = fig.add_subplot(gs[1])
    
    for i, sc in enumerate(scenarios):
        r = results[sc]
        bin_centers = (r['bins'][:-1] + r['bins'][1:]) / 2
        ax2.plot(bin_centers, r['P_r'], linewidth=2.5, alpha=0.8, 
                label=f"{sc} (⟨r⟩={r['mean_r']:.3f})", color=colors[i])
    
    ax2.set_xlabel(r'$r = \min(s_n, s_{n+1}) / \max(s_n, s_{n+1})$', fontsize=12)
    ax2.set_ylabel(r'$P(r)$', fontsize=13)
    ax2.set_title('Panel B: P(r)-Verteilungen', fontsize=14, fontweight='bold')
    ax2.legend(fontsize=9, loc='upper left')
    ax2.grid(True, alpha=0.3)
    ax2.set_xlim(0, 1)
    
    # Panel C: Violin-Plot der Ensemble-Verteilungen
    ax3 = fig.add_subplot(gs[2])
    
    ensemble_data = [results[sc]['ensemble_means'] for sc in scenarios]
    
    parts = ax3.violinplot(ensemble_data, positions=x_pos, widths=0.6,
                           showmeans=True, showextrema=True)
    
    # Farbige Violins
    for i, pc in enumerate(parts['bodies']):
        pc.set_facecolor(colors[i])
        pc.set_alpha(0.6)
    
    # Referenzlinien
    ax3.axhline(y=0.386, color='gray', linestyle='--', linewidth=1.5, alpha=0.6)
    ax3.axhline(y=0.530, color='blue', linestyle='--', linewidth=1.5, alpha=0.6)
    ax3.axhline(y=0.603, color='red', linestyle='--', linewidth=1.5, alpha=0.6)
    ax3.axhspan(0.52, 0.68, color='yellow', alpha=0.15)
    
    ax3.set_xticks(x_pos)
    ax3.set_xticklabels(scenarios, rotation=0, ha='center', fontsize=11)
    ax3.set_ylabel(r'Ensemble $\langle r \rangle$ Verteilung', fontsize=13)
    ax3.set_title('Panel C: Ensemble-Variabilität', fontsize=14, fontweight='bold')
    ax3.grid(True, alpha=0.3, axis='y')
    ax3.set_ylim(0.35, 0.72)
    
    # Suptitle
    fig.suptitle('Ratio-Statistik Quick-Check: Oganesyan-Huse Methode', 
                 fontsize=16, fontweight='bold', y=1.00)
    
    plt.tight_layout()
    
    output_path = FIGURES_DIR / 'ratio_statistic_quick_check.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Plot gespeichert: {output_path}")
    plt.close()


if __name__ == "__main__":
    results, decision = ratio_statistic_quick_check()
    
    print("\n" + "="*80)
    print("QUICK-CHECK ABGESCHLOSSEN!")
    print("="*80)
    print(f"\nEntscheidung: {decision.upper()}")
    
    if decision == 'confirmed' or decision == 'hints':
        print("\n→ WEITERMACHEN mit Finite-Size-Scaling empfohlen!")
        print("→ Führe 'finite_size_scaling.py' aus")
    else:
        print("\n→ STOPPEN hier. Hypothese nicht bestätigt.")
        print("→ Berichte Ergebnis an Nutzer.")
    
    print(f"\nErgebnisse:")
    print(f"  CSV:  {RESULTS_DIR / 'ratio_statistic_quick_check.csv'}")
    print(f"  NPZ:  {RESULTS_DIR / 'P_r_distributions.npz'}")
    print(f"  Plot: {FIGURES_DIR / 'ratio_statistic_quick_check.png'}")
    print("="*80 + "\n")
