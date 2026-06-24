"""
E02 Zusatztest: Kanonisierungs-Stabilität

Testet, ob das ΔR²_H-Signal robust über verschiedene Kanonisierungen ist.
Dies adressiert H0 (Existenz kanonischer Abbildung).
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from typing import Dict, List

from utils.eabc import compute_svn_coordinates, count_prime_factors
from utils.catalan_magic import compute_catalan_magic
from utils.canonization import all_canonization_methods


def test_canonization_stability(numbers: List[int]) -> Dict:
    """
    Testet ΔR²_H für verschiedene Kanonisierungen.
    
    Wenn H(n) robust ist, sollte ΔR²_H für alle Kanonisierungen ähnlich sein.
    """
    print("Teste Kanonisierungs-Stabilität...")
    print()
    
    methods = ['left', 'right', 'balanced']
    results = {}
    
    for method in methods:
        print(f"Kanonisierung: {method}")
        
        # Features berechnen
        all_coords = [compute_svn_coordinates(n) for n in numbers]
        M_C = np.array([compute_catalan_magic(n, method=method) for n in numbers])
        
        omega = np.array([c['omega'] for c in all_coords])
        omega_sq = omega ** 2
        v2 = np.array([c['v2'] for c in all_coords])
        v3 = np.array([c['v3'] for c in all_coords])
        H = np.array([c['H'] for c in all_coords])
        
        # M2: Baseline
        X_M2 = np.column_stack([omega, omega_sq, v2, v3])
        mask_M2 = ~np.isnan(X_M2).any(axis=1) & ~np.isnan(M_C)
        model_M2 = LinearRegression().fit(X_M2[mask_M2], M_C[mask_M2])
        R2_M2 = r2_score(M_C[mask_M2], model_M2.predict(X_M2[mask_M2]))
        
        # M3*: Mit H(n)
        X_M3_star = np.column_stack([omega, omega_sq, v2, v3, H])
        mask_M3 = ~np.isnan(X_M3_star).any(axis=1) & ~np.isnan(M_C)
        model_M3 = LinearRegression().fit(X_M3_star[mask_M3], M_C[mask_M3])
        R2_M3 = r2_score(M_C[mask_M3], model_M3.predict(X_M3_star[mask_M3]))
        
        Delta_H = R2_M3 - R2_M2
        
        print(f"  R²(M2)  = {R2_M2:.4f}")
        print(f"  R²(M3*) = {R2_M3:.4f}")
        print(f"  ΔR²_H   = {Delta_H:.4f}")
        print()
        
        results[method] = {
            'R2_M2': R2_M2,
            'R2_M3_star': R2_M3,
            'Delta_H': Delta_H,
            'M_C': M_C,
            'n_samples': len(M_C[mask_M3])
        }
    
    # Korrelation zwischen Kanonisierungen
    print("Korrelationen zwischen M_C für verschiedene Kanonisierungen:")
    M_C_left = results['left']['M_C']
    M_C_right = results['right']['M_C']
    M_C_balanced = results['balanced']['M_C']
    
    corr_LR = np.corrcoef(M_C_left, M_C_right)[0, 1]
    corr_LB = np.corrcoef(M_C_left, M_C_balanced)[0, 1]
    corr_RB = np.corrcoef(M_C_right, M_C_balanced)[0, 1]
    
    print(f"  ρ(left, right)     = {corr_LR:.4f}")
    print(f"  ρ(left, balanced)  = {corr_LB:.4f}")
    print(f"  ρ(right, balanced) = {corr_RB:.4f}")
    print()
    
    # Stabilitäts-Bewertung
    Delta_H_values = [results[m]['Delta_H'] for m in methods]
    Delta_H_mean = np.mean(Delta_H_values)
    Delta_H_std = np.std(Delta_H_values)
    Delta_H_cv = Delta_H_std / Delta_H_mean if Delta_H_mean > 0 else np.inf
    
    print("Stabilität von ΔR²_H:")
    print(f"  Mittelwert: {Delta_H_mean:.4f}")
    print(f"  Std:        {Delta_H_std:.4f}")
    print(f"  CV:         {Delta_H_cv:.2f}")
    print()
    
    if Delta_H_cv < 0.2:
        print("✓ STABIL: ΔR²_H ist robust über Kanonisierungen (CV < 0.2)")
        stable = True
    elif Delta_H_cv < 0.5:
        print("~ MODERAT: ΔR²_H variiert moderat (0.2 ≤ CV < 0.5)")
        stable = True
    else:
        print("✗ INSTABIL: ΔR²_H ist stark kanonisierungs-abhängig (CV ≥ 0.5)")
        stable = False
    
    return {
        'results_by_method': results,
        'correlations': {
            'left_right': corr_LR,
            'left_balanced': corr_LB,
            'right_balanced': corr_RB
        },
        'Delta_H_mean': Delta_H_mean,
        'Delta_H_std': Delta_H_std,
        'Delta_H_cv': Delta_H_cv,
        'stable': stable
    }


def main():
    print("=" * 70)
    print("E02 ZUSATZTEST: KANONISIERUNGS-STABILITÄT")
    print("=" * 70)
    print()
    
    # Generiere denselben Datensatz
    numbers = [n for n in range(2, 1001) if count_prime_factors(n) >= 4]
    print(f"Datensatz: {len(numbers)} Zahlen mit Ω ≥ 4")
    print()
    
    # Teste Stabilität
    stability_results = test_canonization_stability(numbers)
    
    # Speichere Ergebnisse
    output_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
        'experiments', 'results', 'e02'
    )
    
    report_path = os.path.join(output_dir, 'canonization_stability.md')
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("# E02 Zusatztest: Kanonisierungs-Stabilität\n\n")
        f.write("## Zielsetzung\n\n")
        f.write("Teste, ob das ΔR²_H-Signal robust über verschiedene ")
        f.write("Kanonisierungen n → T(n) ist.\n\n")
        f.write("Falls ΔR²_H stark variiert, wäre das Signal ein Kanonisierungs-Artefakt.\n\n")
        f.write("---\n\n")
        
        f.write("## Ergebnisse\n\n")
        f.write("| Kanonisierung | R²(M2) | R²(M3*) | ΔR²_H |\n")
        f.write("|---------------|--------|---------|-------|\n")
        
        for method in ['left', 'right', 'balanced']:
            res = stability_results['results_by_method'][method]
            f.write(f"| {method:13s} | {res['R2_M2']:.4f} | ")
            f.write(f"{res['R2_M3_star']:.4f} | {res['Delta_H']:.4f} |\n")
        
        f.write("\n")
        f.write(f"**Mittelwert ΔR²_H:** {stability_results['Delta_H_mean']:.4f}\n\n")
        f.write(f"**Standardabweichung:** {stability_results['Delta_H_std']:.4f}\n\n")
        f.write(f"**Variationskoeffizient:** {stability_results['Delta_H_cv']:.2f}\n\n")
        
        f.write("---\n\n")
        f.write("## Korrelationen zwischen M_C\n\n")
        f.write("| Vergleich | Korrelation |\n")
        f.write("|-----------|-------------|\n")
        corr = stability_results['correlations']
        f.write(f"| Left ↔ Right | {corr['left_right']:.4f} |\n")
        f.write(f"| Left ↔ Balanced | {corr['left_balanced']:.4f} |\n")
        f.write(f"| Right ↔ Balanced | {corr['right_balanced']:.4f} |\n")
        f.write("\n")
        
        f.write("---\n\n")
        f.write("## Interpretation\n\n")
        
        if stability_results['stable']:
            f.write("✅ **STABIL**: Das ΔR²_H-Signal ist robust über verschiedene ")
            f.write("Kanonisierungen.\n\n")
            f.write("**Konsequenz:** Die Erklärungskraft von H(n) ist KEIN ")
            f.write("Kanonisierungs-Artefakt, sondern eine echte arithmetische Eigenschaft.\n\n")
            f.write("**H0 (Existenz kanonischer Abbildung):** Erfüllt - die Wahl der ")
            f.write("Kanonisierung ändert das qualitative Ergebnis nicht.\n\n")
        else:
            f.write("⚠️ **INSTABIL**: Das ΔR²_H-Signal variiert stark zwischen ")
            f.write("Kanonisierungen.\n\n")
            f.write("**Konsequenz:** Die Erklärungskraft von H(n) könnte ein ")
            f.write("Kanonisierungs-Artefakt sein.\n\n")
            f.write("**H0 (Existenz kanonischer Abbildung):** Verletzt - weitere ")
            f.write("Tests erforderlich.\n\n")
        
        f.write("---\n\n")
        f.write("*Generiert durch `e02_canonization_stability.py`*\n")
    
    print(f"Bericht gespeichert: {report_path}")
    print()
    print("=" * 70)
    print("ZUSAMMENFASSUNG")
    print("=" * 70)
    print(f"ΔR²_H (Mittelwert): {stability_results['Delta_H_mean']:.4f}")
    print(f"Variationskoeffizient: {stability_results['Delta_H_cv']:.2f}")
    print(f"Stabil: {'Ja' if stability_results['stable'] else 'Nein'}")
    print("=" * 70)


if __name__ == "__main__":
    main()
