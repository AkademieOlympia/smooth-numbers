"""
Systematischer Vergleich der arithmetischen Schichten im EABC-Qubit-Framework.

Dieses Skript untersucht die zentrale Forschungsfrage:
    Wirkt Glattheit verstärkend oder dämpfend auf das Chaos im Spektrum?

Es vergleicht verschiedene Szenarien:
1. Nur Primzahlen (Referenz)
2. Nur Glattheit
3. Primzahlen + EABC
4. Primzahlen + Collatz
5. Primzahlen + Collatz + Glattheit
6. Alle Schichten (vollständige Integration)

Metriken:
- Brody-Parameter q (q=0: Poisson, q=1: GOE/GUE)
- Spectral rigidity Σ²(L)
- Level spacing ratio ⟨r⟩
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import pandas as pd
from typing import Dict, List, Tuple

from src.hamiltonian import MultiLayerHamiltonian
from src.level_spacing import compute_level_spacings, brody_parameter, estimate_brody_q
from src.spectral import spectral_rigidity, level_spacing_ratio


def build_scenario(name: str, N: int, **kwargs) -> MultiLayerHamiltonian:
    """
    Baut einen Hamiltonian für ein bestimmtes Szenario.
    
    Parameters
    ----------
    name : str
        Szenario-Name
    N : int
        Gittergröße
    **kwargs : dict
        Zusätzliche Parameter für MultiLayerHamiltonian
    
    Returns
    -------
    MultiLayerHamiltonian
        Hamiltonian-Instanz
    """
    print(f"\n{'='*70}")
    print(f"Szenario: {name}")
    print(f"{'='*70}")
    
    H = MultiLayerHamiltonian(N, **kwargs)
    H.info()
    
    return H


def compute_spectral_metrics(H: MultiLayerHamiltonian, k: int = 500) -> Dict:
    """
    Berechnet spektrale Metriken für einen Hamiltonian.
    
    Parameters
    ----------
    H : MultiLayerHamiltonian
        Hamiltonian
    k : int, optional
        Anzahl der zu berechnenden Eigenwerte
    
    Returns
    -------
    dict
        Dictionary mit spektralen Metriken
    """
    print(f"\nBerechne Spektrum ({k} Eigenwerte)...")
    eigenvalues = H.compute_spectrum(k=k, which='SM')
    
    # Level spacings
    spacings = compute_level_spacings(eigenvalues)
    
    # Brody-Parameter
    print("Berechne Brody-Parameter q...")
    q = estimate_brody_q(spacings)
    
    # Level spacing ratio
    print("Berechne Level Spacing Ratio ⟨r⟩...")
    r_mean = level_spacing_ratio(eigenvalues)
    
    # Spectral rigidity (nur für große genug Spektren)
    if len(eigenvalues) > 50:
        print("Berechne Spectral Rigidity Σ²(L)...")
        L_values, sigma2 = spectral_rigidity(eigenvalues, max_L=20)
        sigma2_mean = np.mean(sigma2[5:15])  # Mittelwert für L ∈ [5, 15]
    else:
        L_values, sigma2 = None, None
        sigma2_mean = np.nan
    
    metrics = {
        'eigenvalues': eigenvalues,
        'spacings': spacings,
        'brody_q': q,
        'spacing_ratio_mean': r_mean,
        'sigma2_L': (L_values, sigma2),
        'sigma2_mean': sigma2_mean
    }
    
    print(f"\nMetriken:")
    print(f"  Brody q:     {q:.4f}")
    print(f"  ⟨r⟩:         {r_mean:.4f}")
    if not np.isnan(sigma2_mean):
        print(f"  ⟨Σ²⟩ (L=5-15): {sigma2_mean:.4f}")
    
    return metrics


def compare_all_scenarios(N: int = 1000, k: int = 500) -> pd.DataFrame:
    """
    Vergleicht alle Szenarien systematisch.
    
    Parameters
    ----------
    N : int, optional
        Gittergröße, default: 1000
    k : int, optional
        Anzahl Eigenwerte, default: 500
    
    Returns
    -------
    pd.DataFrame
        Vergleichstabelle mit allen Metriken
    """
    # Standard-Parameter
    alpha = 1.0
    beta = 0.5
    gamma = 1.5
    eta = 0.5
    smooth_max_k = 20
    
    # Definiere Szenarien
    scenarios = {
        "Baseline (nur TB+χ)": dict(
            alpha=alpha, beta=beta, gamma=0.0, eta=0.0,
            use_primes=False, use_collatz=False, use_smooth=False
        ),
        "Primes only": dict(
            alpha=alpha, beta=beta, gamma=gamma, eta=0.0,
            use_primes=True, use_collatz=False, use_smooth=False
        ),
        "Smooth only": dict(
            alpha=alpha, beta=beta, gamma=0.0, eta=eta,
            use_primes=False, use_collatz=False, use_smooth=True,
            smooth_max_k=smooth_max_k
        ),
        "Primes + EABC": dict(
            alpha=alpha, beta=beta, gamma=gamma, eta=0.0,
            use_primes=True, use_collatz=False, use_smooth=False
        ),
        "Primes + Collatz": dict(
            alpha=alpha, beta=beta, gamma=gamma, eta=0.0,
            use_primes=True, use_collatz=True, use_smooth=False
        ),
        "Primes + Collatz + Smooth": dict(
            alpha=alpha, beta=beta, gamma=gamma, eta=eta,
            use_primes=True, use_collatz=True, use_smooth=True,
            smooth_max_k=smooth_max_k
        ),
        "All layers": dict(
            alpha=alpha, beta=beta, gamma=gamma, eta=eta,
            use_primes=True, use_collatz=True, use_smooth=True,
            smooth_max_k=smooth_max_k
        )
    }
    
    # Sammle Ergebnisse
    results = []
    
    for name, config in scenarios.items():
        # Baue Hamiltonian
        H = build_scenario(name, N, **config)
        
        # Berechne Metriken
        metrics = compute_spectral_metrics(H, k=k)
        
        # Speichere Ergebnis
        results.append({
            'Scenario': name,
            'N': N,
            'alpha': config.get('alpha', alpha),
            'beta': config.get('beta', beta),
            'gamma': config.get('gamma', 0.0),
            'eta': config.get('eta', 0.0),
            'use_primes': config.get('use_primes', False),
            'use_collatz': config.get('use_collatz', False),
            'use_smooth': config.get('use_smooth', False),
            'brody_q': metrics['brody_q'],
            'spacing_ratio': metrics['spacing_ratio_mean'],
            'sigma2_mean': metrics['sigma2_mean']
        })
    
    # Konvertiere zu DataFrame
    df = pd.DataFrame(results)
    
    return df


def plot_comparison(df: pd.DataFrame, output_dir: str = "figures"):
    """
    Visualisiert den Layer-Vergleich.
    
    Parameters
    ----------
    df : pd.DataFrame
        Vergleichstabelle
    output_dir : str, optional
        Ausgabeverzeichnis für Plots
    """
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    
    scenarios = df['Scenario'].values
    x = np.arange(len(scenarios))
    
    # Plot 1: Brody q
    ax = axes[0]
    bars = ax.bar(x, df['brody_q'], color='steelblue', alpha=0.7, edgecolor='black')
    ax.axhline(y=0.0, color='red', linestyle='--', label='Poisson (q=0)')
    ax.axhline(y=1.0, color='green', linestyle='--', label='GUE (q=1)')
    ax.set_xlabel('Szenario', fontsize=12)
    ax.set_ylabel('Brody-Parameter q', fontsize=12)
    ax.set_title('Spektrale Statistik: Brody q', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(scenarios, rotation=45, ha='right', fontsize=9)
    ax.legend()
    ax.grid(axis='y', alpha=0.3)
    
    # Färbe Smooth-Szenarien
    for i, use_smooth in enumerate(df['use_smooth']):
        if use_smooth:
            bars[i].set_color('orange')
            bars[i].set_alpha(0.8)
    
    # Plot 2: Level Spacing Ratio
    ax = axes[1]
    bars = ax.bar(x, df['spacing_ratio'], color='coral', alpha=0.7, edgecolor='black')
    ax.axhline(y=0.386, color='red', linestyle='--', label='Poisson (0.386)')
    ax.axhline(y=0.530, color='green', linestyle='--', label='GOE (0.530)')
    ax.set_xlabel('Szenario', fontsize=12)
    ax.set_ylabel('⟨r⟩', fontsize=12)
    ax.set_title('Level Spacing Ratio ⟨r⟩', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(scenarios, rotation=45, ha='right', fontsize=9)
    ax.legend()
    ax.grid(axis='y', alpha=0.3)
    
    for i, use_smooth in enumerate(df['use_smooth']):
        if use_smooth:
            bars[i].set_color('orange')
            bars[i].set_alpha(0.8)
    
    # Plot 3: Δq (Effekt von Smooth)
    ax = axes[2]
    
    # Vergleiche Szenarien mit/ohne Smooth
    comparisons = [
        ("Primes only", "Primes + Collatz + Smooth"),
        ("Primes + Collatz", "Primes + Collatz + Smooth"),
    ]
    
    delta_q = []
    labels = []
    
    for without, with_smooth in comparisons:
        q_without = df[df['Scenario'] == without]['brody_q'].values[0]
        q_with = df[df['Scenario'] == with_smooth]['brody_q'].values[0]
        delta = q_with - q_without
        delta_q.append(delta)
        labels.append(f"{without.split()[0]}\n→ +Smooth")
    
    colors = ['green' if dq < 0 else 'red' for dq in delta_q]
    bars = ax.bar(range(len(delta_q)), delta_q, color=colors, alpha=0.7, edgecolor='black')
    ax.axhline(y=0, color='black', linestyle='-', linewidth=1)
    ax.set_xlabel('Vergleich', fontsize=12)
    ax.set_ylabel('Δq', fontsize=12)
    ax.set_title('Effekt von Glattheit auf Chaos', fontsize=14, fontweight='bold')
    ax.set_xticks(range(len(delta_q)))
    ax.set_xticklabels(labels, fontsize=10)
    ax.grid(axis='y', alpha=0.3)
    
    # Annotiere Werte
    for i, dq in enumerate(delta_q):
        ax.text(i, dq + 0.01 * np.sign(dq), f"{dq:+.3f}", 
                ha='center', va='bottom' if dq > 0 else 'top', fontsize=10, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(output_path / "layer_comparison.png", dpi=300, bbox_inches='tight')
    print(f"\n✓ Plot gespeichert: {output_path / 'layer_comparison.png'}")
    
    plt.show()


def print_comparison_table(df: pd.DataFrame):
    """
    Druckt die Vergleichstabelle formatiert.
    
    Parameters
    ----------
    df : pd.DataFrame
        Vergleichstabelle
    """
    print("\n" + "="*80)
    print("LAYER COMPARISON - Spektrale Metriken")
    print("="*80)
    
    print(f"\n{'Scenario':<30s} │ {'q':>6s} │ {'⟨r⟩':>6s} │ {'Σ²':>6s} │ P C S")
    print("─" * 30 + "┼" + "─" * 8 + "┼" + "─" * 8 + "┼" + "─" * 8 + "┼" + "─" * 6)
    
    for _, row in df.iterrows():
        name = row['Scenario'][:28]
        q = row['brody_q']
        r = row['spacing_ratio']
        sigma2 = row['sigma2_mean']
        
        p_flag = '✓' if row['use_primes'] else '✗'
        c_flag = '✓' if row['use_collatz'] else '✗'
        s_flag = '✓' if row['use_smooth'] else '✗'
        
        sigma2_str = f"{sigma2:6.3f}" if not np.isnan(sigma2) else "  N/A "
        
        print(f"{name:<30s} │ {q:6.3f} │ {r:6.3f} │ {sigma2_str} │ {p_flag} {c_flag} {s_flag}")
    
    print("="*80)
    print("Legende: P=Primzahlen, C=Collatz, S=Smooth")
    print("="*80 + "\n")


def export_results(df: pd.DataFrame, output_dir: str = "results"):
    """
    Exportiert Ergebnisse als CSV und JSON.
    
    Parameters
    ----------
    df : pd.DataFrame
        Vergleichstabelle
    output_dir : str, optional
        Ausgabeverzeichnis
    """
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    # CSV Export
    csv_path = output_path / "layer_comparison.csv"
    df.to_csv(csv_path, index=False)
    print(f"✓ CSV exportiert: {csv_path}")
    
    # JSON Export
    json_path = output_path / "layer_comparison.json"
    df.to_json(json_path, orient='records', indent=2)
    print(f"✓ JSON exportiert: {json_path}")


def main():
    """Hauptfunktion für vollständige Layer-Analyse."""
    print("╔═══════════════════════════════════════════════════════════════════╗")
    print("║  SMOOTH INTEGRATION - Systematischer Layer-Vergleich             ║")
    print("╚═══════════════════════════════════════════════════════════════════╝\n")
    
    # Parameter
    N = 1000
    k = 500
    
    print(f"Konfiguration:")
    print(f"  Gittergröße N:    {N}")
    print(f"  Eigenwerte k:     {k}")
    print(f"  Smooth max_k:     20")
    
    # Führe Vergleich durch
    print("\n" + "="*70)
    print("STARTE LAYER-VERGLEICH")
    print("="*70)
    
    df = compare_all_scenarios(N=N, k=k)
    
    # Zeige Ergebnisse
    print_comparison_table(df)
    
    # Export
    export_results(df, output_dir="results")
    
    # Visualisierung
    plot_comparison(df, output_dir="figures")
    
    # Zusammenfassung
    print("\n" + "="*70)
    print("ZUSAMMENFASSUNG")
    print("="*70)
    
    # Finde Szenarien mit/ohne Smooth
    q_primes_only = df[df['Scenario'] == 'Primes only']['brody_q'].values[0]
    q_primes_collatz_smooth = df[df['Scenario'] == 'Primes + Collatz + Smooth']['brody_q'].values[0]
    
    delta_q = q_primes_collatz_smooth - q_primes_only
    
    print(f"\nHauptfrage: Wirkt Glattheit verstärkend oder dämpfend auf Chaos?")
    print(f"\nErgebnis:")
    print(f"  Primes only:               q = {q_primes_only:.3f}")
    print(f"  Primes + Collatz + Smooth: q = {q_primes_collatz_smooth:.3f}")
    print(f"  Δq = {delta_q:+.3f}")
    
    if delta_q < -0.01:
        print("\n→ Hypothese A bestätigt: Glattheit GLÄTTET das Spektrum (q sinkt)")
    elif delta_q > 0.01:
        print("\n→ Hypothese B bestätigt: Glattheit VERSTÄRKT Chaos (q steigt)")
    else:
        print("\n→ Hypothese C bestätigt: Glattheit ist ORTHOGONAL (kein Effekt)")
    
    print("\n✓ Alle Analysen abgeschlossen!")
    print(f"✓ Ergebnisse: results/layer_comparison.csv")
    print(f"✓ Plots:      figures/layer_comparison.png")


if __name__ == "__main__":
    main()
