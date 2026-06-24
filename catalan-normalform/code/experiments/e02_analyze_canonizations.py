"""
Detaillierte Analyse: Warum haben Links/Rechts perfektes R²?
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import numpy as np
import matplotlib.pyplot as plt

from utils.eabc import count_prime_factors
from utils.catalan_magic import compute_catalan_magic


def analyze_magic_by_canonization():
    """
    Untersucht M_C(n) für verschiedene Kanonisierungen.
    """
    print("Analysiere M_C für verschiedene Kanonisierungen...")
    print()
    
    numbers = [n for n in range(2, 200) if count_prime_factors(n) >= 4][:50]
    
    results = []
    
    for n in numbers:
        omega = count_prime_factors(n)
        M_C_left = compute_catalan_magic(n, method='left')
        M_C_right = compute_catalan_magic(n, method='right')
        M_C_balanced = compute_catalan_magic(n, method='balanced')
        
        results.append({
            'n': n,
            'omega': omega,
            'M_C_left': M_C_left,
            'M_C_right': M_C_right,
            'M_C_balanced': M_C_balanced
        })
    
    # Analysiere Abhängigkeit von Ω
    print("Erste 20 Beispiele:")
    print()
    print("n     | Ω | M_C(left) | M_C(right) | M_C(balanced)")
    print("------|---|-----------|------------|-------------")
    
    for i, res in enumerate(results[:20]):
        print(f"{res['n']:5d} | {res['omega']} | "
              f"{res['M_C_left']:9.1f} | {res['M_C_right']:10.1f} | {res['M_C_balanced']:12.1f}")
    
    print()
    
    # Berechne Korrelationen mit Ω
    omegas = np.array([r['omega'] for r in results])
    M_C_left_arr = np.array([r['M_C_left'] for r in results])
    M_C_right_arr = np.array([r['M_C_right'] for r in results])
    M_C_balanced_arr = np.array([r['M_C_balanced'] for r in results])
    
    corr_left = np.corrcoef(omegas, M_C_left_arr)[0, 1]
    corr_right = np.corrcoef(omegas, M_C_right_arr)[0, 1]
    corr_balanced = np.corrcoef(omegas, M_C_balanced_arr)[0, 1]
    
    print("Korrelation M_C mit Ω:")
    print(f"  Left:     {corr_left:.4f}")
    print(f"  Right:    {corr_right:.4f}")
    print(f"  Balanced: {corr_balanced:.4f}")
    print()
    
    # Theoretische Formel für Links/Rechts
    print("Theoretische Analyse:")
    print()
    print("Für Linksbaum (((a·b)·c)·...·z):")
    print("  Höhe = Ω - 1")
    print("  M_C ≈ Σ(Ω-1-i) für i=0...Ω-2")
    print("  M_C = (Ω-1)·(Ω-2)/2")
    print()
    
    # Teste theoretische Formel
    print("Validierung der theoretischen Formel:")
    print()
    print("Ω | M_C(left beobachtet) | M_C(theoretisch) | Differenz")
    print("--|----------------------|------------------|----------")
    
    for omega in range(4, 10):
        examples = [r for r in results if r['omega'] == omega]
        if examples:
            M_C_obs = examples[0]['M_C_left']
            M_C_theory = (omega - 1) * (omega - 2) / 2
            diff = abs(M_C_obs - M_C_theory)
            print(f"{omega} | {M_C_obs:20.1f} | {M_C_theory:16.1f} | {diff:8.1f}")
    
    print()
    print("ERKLÄRUNG:")
    print()
    print("Links- und Rechtsbäume sind DETERMINISTISCH:")
    print("  - Für gegebenes Ω ist M_C vollständig determiniert")
    print("  - M_C = (Ω-1)(Ω-2)/2 für Linksbaum")
    print("  - M_C = (Ω-1)(Ω-2)/2 für Rechtsbaum (symmetrisch)")
    print()
    print("Balancierte Bäume sind VARIABEL:")
    print("  - Für gegebenes Ω gibt es verschiedene mögliche Strukturen")
    print("  - M_C hängt von der konkreten Faktorzerlegung ab")
    print("  - HIER kann H(n) wirken!")
    print()
    
    return results


if __name__ == "__main__":
    print("=" * 70)
    print("DETAILANALYSE: WARUM HABEN LINKS/RECHTS PERFEKTES R²?")
    print("=" * 70)
    print()
    
    results = analyze_magic_by_canonization()
