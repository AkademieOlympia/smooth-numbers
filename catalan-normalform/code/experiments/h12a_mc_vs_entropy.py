"""
H12-A: Test M_C gegen EABC-Shannon-Entropie
===========================================

ZENTRALE HYPOTHESE:
Falls M_C Baumasymmetrie misst, sollte es mit Entropie/Konzentration 
korrelieren (nicht mit S=v₂+v₃).

NEUE METRIK:
E(n) = -Σ_{x∈{E,A,B,C}} p_x log p_x

wobei p_x = Anteil der Primfaktoren in Klasse x.

ERWARTUNG:
corr(M_C, E(n)) ≫ corr(M_C, S)

Denn: Hohe Entropie = gleichverteilte Faktoren = balancierter Baum = niedriges M_C
      Niedrige Entropie = konzentrierte Faktoren = unbalancierter Baum = hohes M_C

Autor: H12 Testing Framework
Datum: 2026-06-24
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from scipy import stats
from typing import Dict, List, Tuple
import json
from datetime import datetime
import pandas as pd
from pathlib import Path

from utils.eabc_test_data import EABCTestData
from utils.catalan_magic import compute_catalan_magic
from utils.eabc import prime_factors_with_multiplicity, eabc_class


# ============================================================================
# ENTROPIE-BERECHNUNG
# ============================================================================

def compute_eabc_entropy(n: int) -> float:
    """
    Berechnet Shannon-Entropie der EABC-Verteilung.
    
    E(n) = -Σ_{x∈{E,A,B,C}} p_x log p_x
    
    wobei p_x = (Anzahl Faktoren in Klasse x) / (Gesamt-EABC-Faktoren)
    
    Args:
        n: Natürliche Zahl ≥ 2
        
    Returns:
        E(n) ∈ [0, log(4)] = [0, 1.386]
        - E = 0: Alle Faktoren in einer Klasse (maximale Konzentration)
        - E = log(4): Gleichverteilung (maximale Entropie)
        np.nan falls keine EABC-Faktoren vorhanden
    """
    factors = prime_factors_with_multiplicity(n)
    
    # Zähle Faktoren in jeder EABC-Klasse
    counts = {'E': 0, 'A': 0, 'B': 0, 'C': 0}
    for p in factors:
        if p > 3:
            cls = eabc_class(p)
            if cls in counts:
                counts[cls] += 1
    
    total = sum(counts.values())
    
    if total == 0:
        # Keine EABC-Faktoren (nur 2, 3)
        return np.nan
    
    # Shannon-Entropie
    entropy = 0.0
    for count in counts.values():
        if count > 0:
            p = count / total
            entropy -= p * np.log(p)
    
    return entropy


def compute_eabc_entropy_batch(data: EABCTestData, n_values: np.ndarray) -> np.ndarray:
    """
    Batch-Berechnung von E(n) unter Verwendung des Caches.
    
    Args:
        data: EABCTestData-Instanz
        n_values: Array von Zahlen
        
    Returns:
        Array von Entropien
    """
    entropies = np.zeros(len(n_values))
    
    for i, n in enumerate(n_values):
        coords = data.get_coordinates(n)
        e, a, b, c = coords['e'], coords['a'], coords['b'], coords['c']
        total = e + a + b + c
        
        if total == 0:
            entropies[i] = np.nan
        else:
            # Shannon-Entropie
            entropy = 0.0
            for count in [e, a, b, c]:
                if count > 0:
                    p = count / total
                    entropy -= p * np.log(p)
            entropies[i] = entropy
    
    return entropies


# ============================================================================
# H12-A MAIN TEST
# ============================================================================

def h12a_mc_vs_entropy(
    n_max: int = 10000,
    cache_file: str = None,
    output_dir: str = "../../experiments/results/h12"
) -> Dict:
    """
    H12-A: Teste M_C gegen EABC-Entropie E(n).
    
    Vergleiche:
    1. corr(M_C, E) vs. corr(M_C, S) [aus H10]
    2. R²(M_C, E) vs. R²(M_C, Ω) [aus H10]
    3. Residuen-Test: corr(M_C^⊥, E^⊥) nach Ω-Entfernung
    
    Args:
        n_max: Maximale Zahl für Test
        cache_file: Pfad zu EABC-Cache (optional, sonst direkte Berechnung)
        output_dir: Ausgabeverzeichnis für Ergebnisse
        
    Returns:
        Dictionary mit Ergebnissen
    """
    print("=" * 80)
    print("H12-A: M_C vs. EABC-SHANNON-ENTROPIE")
    print("=" * 80)
    print()
    print(f"Getestet: n ∈ [2, {n_max:,}]")
    print()
    
    # -------------------------------------------------------------------------
    # 1. DATEN LADEN
    # -------------------------------------------------------------------------
    
    print("1. Lade Daten...")
    
    if cache_file and Path(cache_file).exists():
        print(f"   Cache gefunden: {cache_file}")
        data = EABCTestData(cache_file=cache_file, readonly=True)
    else:
        print("   Kein Cache, berechne direkt (langsam!)")
        data = None
    
    # Generiere n-Werte (alle mit Ω ≥ 2 für sinnvolle M_C)
    n_values = []
    for n in range(2, n_max + 1):
        # Prüfe, ob n genug Primfaktoren hat
        # (M_C ist nur für Ω ≥ 2 interessant)
        factors = prime_factors_with_multiplicity(n)
        if len(factors) >= 2:
            n_values.append(n)
    
    n_values = np.array(n_values)
    n_samples = len(n_values)
    
    print(f"   {n_samples:,} Zahlen mit Ω(n) ≥ 2")
    print()
    
    # -------------------------------------------------------------------------
    # 2. BERECHNE FEATURES
    # -------------------------------------------------------------------------
    
    print("2. Berechne Features...")
    
    M_C = np.zeros(n_samples)
    E = np.zeros(n_samples)
    H = np.zeros(n_samples)
    S = np.zeros(n_samples)
    omega = np.zeros(n_samples)
    
    if data:
        print("   Verwende Cache für schnelle Berechnung...")
        E = compute_eabc_entropy_batch(data, n_values)
        
        for i, n in enumerate(n_values):
            M_C[i] = compute_catalan_magic(n, method='balanced', metric='depth')
            coords = data.get_coordinates(n)
            H[i] = coords['H']
            S[i] = coords['shell']
            omega[i] = coords['omega']
    else:
        print("   Direkte Berechnung (dauert länger)...")
        for i, n in enumerate(n_values):
            M_C[i] = compute_catalan_magic(n, method='balanced', metric='depth')
            E[i] = compute_eabc_entropy(n)
            
            # Berechne auch H, S, omega für Vergleich
            from utils.eabc import compute_svn_coordinates
            coords = compute_svn_coordinates(n)
            H[i] = coords['H']
            S[i] = coords['v2'] + coords['v3']
            omega[i] = coords['omega']
            
            if (i + 1) % 1000 == 0:
                print(f"   {i+1:,} / {n_samples:,} berechnet...")
    
    print(f"   ✓ Features berechnet")
    print()
    
    # -------------------------------------------------------------------------
    # 3. ENTFERNE NaN-WERTE
    # -------------------------------------------------------------------------
    
    valid_mask = ~np.isnan(M_C) & ~np.isnan(E) & ~np.isnan(H) & ~np.isnan(S) & ~np.isnan(omega)
    
    M_C_clean = M_C[valid_mask]
    E_clean = E[valid_mask]
    H_clean = H[valid_mask]
    S_clean = S[valid_mask]
    omega_clean = omega[valid_mask]
    n_valid = len(M_C_clean)
    
    print(f"3. Bereinigte Daten: {n_valid:,} gültige Samples (von {n_samples:,})")
    print()
    
    # -------------------------------------------------------------------------
    # 4. BASELINE: M_C VS Ω (REPRODUZIERE H10-A)
    # -------------------------------------------------------------------------
    
    print("4. Baseline: M_C vs Ω (Reproduktion von H10-A)")
    print("-" * 80)
    
    X_omega = omega_clean.reshape(-1, 1)
    y_MC = M_C_clean
    
    model_MC_Omega = LinearRegression().fit(X_omega, y_MC)
    y_MC_pred_Omega = model_MC_Omega.predict(X_omega)
    R2_MC_Omega = r2_score(y_MC, y_MC_pred_Omega)
    
    corr_MC_Omega = np.corrcoef(M_C_clean, omega_clean)[0, 1]
    
    print(f"   R²(M_C, Ω) = {R2_MC_Omega:.6f}")
    print(f"   corr(M_C, Ω) = {corr_MC_Omega:.6f}")
    print()
    print(f"   [Vergleich H10: R² ≈ 0.16]")
    print()
    
    # -------------------------------------------------------------------------
    # 5. NEUE TESTS: M_C VS E(n)
    # -------------------------------------------------------------------------
    
    print("5. NEUE TESTS: M_C vs. Entropie E(n)")
    print("-" * 80)
    
    # 5a. Direkte Korrelation
    corr_MC_E = np.corrcoef(M_C_clean, E_clean)[0, 1]
    print(f"   corr(M_C, E) = {corr_MC_E:.6f}")
    
    # 5b. Regression M_C ~ E
    X_E = E_clean.reshape(-1, 1)
    model_MC_E = LinearRegression().fit(X_E, y_MC)
    y_MC_pred_E = model_MC_E.predict(X_E)
    R2_MC_E = r2_score(y_MC, y_MC_pred_E)
    
    print(f"   R²(M_C, E) = {R2_MC_E:.6f}")
    print(f"   Koeffizienten: β = {model_MC_E.coef_[0]:.4f}, α = {model_MC_E.intercept_:.4f}")
    print()
    
    # -------------------------------------------------------------------------
    # 6. VERGLEICHSTESTS
    # -------------------------------------------------------------------------
    
    print("6. Vergleichstests")
    print("-" * 80)
    
    # 6a. M_C vs H(n) (Konzentration)
    valid_H = ~np.isnan(H_clean)
    if valid_H.sum() > 0:
        corr_MC_H = np.corrcoef(M_C_clean[valid_H], H_clean[valid_H])[0, 1]
        
        X_H = H_clean[valid_H].reshape(-1, 1)
        y_MC_H = M_C_clean[valid_H]
        model_MC_H = LinearRegression().fit(X_H, y_MC_H)
        y_MC_pred_H = model_MC_H.predict(X_H)
        R2_MC_H = r2_score(y_MC_H, y_MC_pred_H)
        
        print(f"   corr(M_C, H) = {corr_MC_H:.6f}")
        print(f"   R²(M_C, H) = {R2_MC_H:.6f}")
    else:
        corr_MC_H = np.nan
        R2_MC_H = np.nan
        print("   [H(n) hat keine gültigen Werte]")
    print()
    
    # 6b. M_C vs S (Schale) [Reproduktion H10-B]
    corr_MC_S = np.corrcoef(M_C_clean, S_clean)[0, 1]
    
    X_S = S_clean.reshape(-1, 1)
    model_MC_S = LinearRegression().fit(X_S, y_MC)
    y_MC_pred_S = model_MC_S.predict(X_S)
    R2_MC_S = r2_score(y_MC, y_MC_pred_S)
    
    print(f"   corr(M_C, S) = {corr_MC_S:.6f}")
    print(f"   R²(M_C, S) = {R2_MC_S:.6f}")
    print()
    print(f"   [Vergleich H10: corr(M_C^⊥, S^⊥) ≈ 0.03]")
    print()
    
    # -------------------------------------------------------------------------
    # 7. RESIDUEN-TEST: M_C^⊥ vs E^⊥ NACH Ω-ENTFERNUNG
    # -------------------------------------------------------------------------
    
    print("7. Residuen-Test: M_C^⊥ vs E^⊥ (nach Ω-Entfernung)")
    print("-" * 80)
    
    # Entferne Ω aus M_C
    MC_perp = M_C_clean - y_MC_pred_Omega
    
    # Entferne Ω aus E
    X_omega_E = omega_clean.reshape(-1, 1)
    y_E = E_clean
    model_E_Omega = LinearRegression().fit(X_omega_E, y_E)
    y_E_pred_Omega = model_E_Omega.predict(X_omega_E)
    E_perp = E_clean - y_E_pred_Omega
    
    corr_MC_perp_E_perp = np.corrcoef(MC_perp, E_perp)[0, 1]
    
    # p-Wert
    corr_test = stats.pearsonr(MC_perp, E_perp)
    p_value = corr_test[1]
    
    print(f"   corr(M_C^⊥, E^⊥) = {corr_MC_perp_E_perp:.6f}")
    print(f"   p-Wert = {p_value:.6f}")
    
    if p_value < 0.05:
        print(f"   → SIGNIFIKANT! (p < 0.05)")
    else:
        print(f"   → Nicht signifikant (p ≥ 0.05)")
    print()
    
    # -------------------------------------------------------------------------
    # 8. ZUSAMMENFASSUNG
    # -------------------------------------------------------------------------
    
    print("=" * 80)
    print("ZUSAMMENFASSUNG: H12-A")
    print("=" * 80)
    print()
    
    print("KORRELATIONEN:")
    print(f"  corr(M_C, Ω)  = {corr_MC_Omega:+.6f}  (Baseline aus H10)")
    print(f"  corr(M_C, E)  = {corr_MC_E:+.6f}  ⭐ NEU")
    print(f"  corr(M_C, H)  = {corr_MC_H:+.6f}  (Konzentration)")
    print(f"  corr(M_C, S)  = {corr_MC_S:+.6f}  (Schale aus H10)")
    print()
    
    print("R² WERTE:")
    print(f"  R²(M_C, Ω)    = {R2_MC_Omega:.6f}  (Baseline aus H10)")
    print(f"  R²(M_C, E)    = {R2_MC_E:.6f}  ⭐ NEU")
    print(f"  R²(M_C, H)    = {R2_MC_H:.6f}  (Konzentration)")
    print(f"  R²(M_C, S)    = {R2_MC_S:.6f}  (Schale)")
    print()
    
    print("RESIDUEN (nach Ω-Entfernung):")
    print(f"  corr(M_C^⊥, E^⊥) = {corr_MC_perp_E_perp:+.6f}")
    print(f"  p-Wert           = {p_value:.6f}")
    print()
    
    # Interpretation
    print("INTERPRETATION:")
    
    if abs(corr_MC_E) > abs(corr_MC_S):
        print("  ✓ M_C korreliert STÄRKER mit Entropie E als mit Schale S!")
        print("  → Baumasymmetrie misst tatsächlich Verteilungsstruktur!")
    else:
        print("  ✗ M_C korreliert NICHT stärker mit E als mit S")
        print("  → Hypothese nicht bestätigt")
    print()
    
    if R2_MC_E > R2_MC_Omega:
        print("  ✓ E(n) erklärt M_C BESSER als Ω(n)!")
        print("  → Entropie ist besserer Prädiktor als Faktorenanzahl!")
    else:
        print("  → E(n) erklärt M_C ähnlich wie Ω(n)")
    print()
    
    if abs(corr_MC_perp_E_perp) > 0.1 and p_value < 0.05:
        print("  ✓ SIGNIFIKANTE Residuen-Korrelation!")
        print("  → M_C und E teilen Information UNABHÄNGIG von Ω!")
    else:
        print("  → Keine starke Residuen-Korrelation")
    print()
    
    # -------------------------------------------------------------------------
    # 9. SPEICHERE ERGEBNISSE
    # -------------------------------------------------------------------------
    
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # CSV
    results_df = pd.DataFrame({
        'n': n_values[valid_mask],
        'M_C': M_C_clean,
        'E': E_clean,
        'H': H_clean,
        'S': S_clean,
        'omega': omega_clean
    })
    
    csv_file = output_path / "h12a_results.csv"
    results_df.to_csv(csv_file, index=False)
    print(f"✓ Ergebnisse gespeichert: {csv_file}")
    
    # JSON Zusammenfassung
    summary = {
        'test': 'H12-A',
        'timestamp': datetime.now().isoformat(),
        'n_max': n_max,
        'n_samples': n_valid,
        'correlations': {
            'MC_Omega': float(corr_MC_Omega),
            'MC_E': float(corr_MC_E),
            'MC_H': float(corr_MC_H) if not np.isnan(corr_MC_H) else None,
            'MC_S': float(corr_MC_S)
        },
        'r2_scores': {
            'MC_Omega': float(R2_MC_Omega),
            'MC_E': float(R2_MC_E),
            'MC_H': float(R2_MC_H) if not np.isnan(R2_MC_H) else None,
            'MC_S': float(R2_MC_S)
        },
        'residual_test': {
            'corr_MC_perp_E_perp': float(corr_MC_perp_E_perp),
            'p_value': float(p_value),
            'significant': bool(p_value < 0.05)
        }
    }
    
    json_file = output_path / "h12a_summary.json"
    with open(json_file, 'w') as f:
        json.dump(summary, f, indent=2)
    print(f"✓ Zusammenfassung gespeichert: {json_file}")
    
    # -------------------------------------------------------------------------
    # 10. VISUALISIERUNG
    # -------------------------------------------------------------------------
    
    print()
    print("10. Erstelle Visualisierungen...")
    
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    fig.suptitle('H12-A: M_C vs. EABC-Entropie', fontsize=16, fontweight='bold')
    
    # Plot 1: M_C vs Ω
    ax = axes[0, 0]
    ax.scatter(omega_clean, M_C_clean, alpha=0.3, s=10)
    ax.plot(omega_clean, y_MC_pred_Omega, 'r-', linewidth=2, label=f'R²={R2_MC_Omega:.3f}')
    ax.set_xlabel('Ω(n)')
    ax.set_ylabel('M_C(n)')
    ax.set_title(f'M_C vs Ω (Baseline H10)\ncorr={corr_MC_Omega:.3f}')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Plot 2: M_C vs E
    ax = axes[0, 1]
    ax.scatter(E_clean, M_C_clean, alpha=0.3, s=10, color='green')
    ax.plot(E_clean, y_MC_pred_E, 'r-', linewidth=2, label=f'R²={R2_MC_E:.3f}')
    ax.set_xlabel('E(n) [Entropie]')
    ax.set_ylabel('M_C(n)')
    ax.set_title(f'M_C vs E (NEU) ⭐\ncorr={corr_MC_E:.3f}')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Plot 3: M_C vs H
    ax = axes[0, 2]
    if valid_H.sum() > 0:
        ax.scatter(H_clean[valid_H], M_C_clean[valid_H], alpha=0.3, s=10, color='orange')
        ax.plot(H_clean[valid_H], y_MC_pred_H, 'r-', linewidth=2, label=f'R²={R2_MC_H:.3f}')
        ax.set_title(f'M_C vs H\ncorr={corr_MC_H:.3f}')
    else:
        ax.text(0.5, 0.5, 'Keine H-Daten', ha='center', va='center', transform=ax.transAxes)
        ax.set_title('M_C vs H (N/A)')
    ax.set_xlabel('H(n) [Konzentration]')
    ax.set_ylabel('M_C(n)')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Plot 4: M_C vs S
    ax = axes[1, 0]
    ax.scatter(S_clean, M_C_clean, alpha=0.3, s=10, color='purple')
    ax.plot(S_clean, y_MC_pred_S, 'r-', linewidth=2, label=f'R²={R2_MC_S:.3f}')
    ax.set_xlabel('S(n) = v₂ + v₃')
    ax.set_ylabel('M_C(n)')
    ax.set_title(f'M_C vs S (H10)\ncorr={corr_MC_S:.3f}')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Plot 5: Residuen M_C^⊥ vs E^⊥
    ax = axes[1, 1]
    ax.scatter(E_perp, MC_perp, alpha=0.3, s=10, color='red')
    ax.axhline(0, color='k', linestyle='--', linewidth=1, alpha=0.5)
    ax.axvline(0, color='k', linestyle='--', linewidth=1, alpha=0.5)
    ax.set_xlabel('E^⊥ (Residuen)')
    ax.set_ylabel('M_C^⊥ (Residuen)')
    ax.set_title(f'Residuen nach Ω-Entfernung\ncorr={corr_MC_perp_E_perp:.3f}, p={p_value:.3f}')
    ax.grid(True, alpha=0.3)
    
    # Plot 6: Korrelationsvergleich
    ax = axes[1, 2]
    correlations = {
        'Ω': corr_MC_Omega,
        'E': corr_MC_E,
        'H': corr_MC_H if not np.isnan(corr_MC_H) else 0,
        'S': corr_MC_S
    }
    colors = ['blue', 'green', 'orange', 'purple']
    bars = ax.bar(correlations.keys(), correlations.values(), color=colors, alpha=0.7)
    ax.axhline(0, color='k', linestyle='-', linewidth=1)
    ax.set_ylabel('Korrelation mit M_C')
    ax.set_title('Korrelationsvergleich')
    ax.grid(True, alpha=0.3, axis='y')
    
    # Markiere stärkste Korrelation
    max_idx = np.argmax([abs(v) for v in correlations.values()])
    bars[max_idx].set_edgecolor('red')
    bars[max_idx].set_linewidth(3)
    
    plt.tight_layout()
    
    plot_file = output_path / "h12a_plots.png"
    plt.savefig(plot_file, dpi=150, bbox_inches='tight')
    print(f"✓ Plots gespeichert: {plot_file}")
    
    plt.close()
    
    print()
    print("=" * 80)
    print("H12-A ABGESCHLOSSEN")
    print("=" * 80)
    
    return summary


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='H12-A: Test M_C gegen EABC-Entropie')
    parser.add_argument('--n_max', type=int, default=10000, help='Maximale Zahl')
    parser.add_argument('--cache', type=str, default=None, help='Pfad zu EABC-Cache')
    parser.add_argument('--output', type=str, default='../../experiments/results/h12', 
                       help='Ausgabeverzeichnis')
    
    args = parser.parse_args()
    
    # Standard-Cache-Pfad falls nicht angegeben
    if args.cache is None:
        default_cache = Path(__file__).parent.parent.parent / "data" / "eabc_cache_10M.h5"
        if default_cache.exists():
            args.cache = str(default_cache)
    
    results = h12a_mc_vs_entropy(
        n_max=args.n_max,
        cache_file=args.cache,
        output_dir=args.output
    )
