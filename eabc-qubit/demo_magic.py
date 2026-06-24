#!/usr/bin/env python3
"""
Demo: Arithmetische Magic M_EABC

Einfache Demonstration der Magic-Berechnung für verschiedene Hamiltonians.
Dies ist ein schneller Einstieg ohne die zeitintensive Korrelationsanalyse.

Verwendung:
    python demo_magic.py
"""

import numpy as np
from src.hamiltonian import EABCHamiltonian, CollatzEABCHamiltonian
from src.arithmetic_magic import ArithmeticMagic


def demo_basic():
    """
    Basis-Demo: Ein einzelnes System analysieren.
    """
    print("\n" + "="*80)
    print("DEMO 1: SINGLE-SYSTEM MAGIC-ANALYSE")
    print("="*80 + "\n")
    
    # System erstellen
    print("Erstelle EABC-Hamiltonian...")
    H = EABCHamiltonian(N=500, beta=0.5, gamma=1.5)
    H.info()
    
    # Magic berechnen
    print("\nBerechne arithmetische Magic...")
    magic = ArithmeticMagic(H)
    
    # Alle Maße (ohne NZM, da rechenintensiv)
    M_all = magic.compute_all(compute_nzm=False)
    
    # Summary
    print(magic.summary())
    
    return magic


def demo_comparison():
    """
    Vergleichs-Demo: Verschiedene β-Werte.
    """
    print("\n" + "="*80)
    print("DEMO 2: VERGLEICH VERSCHIEDENER β-WERTE")
    print("="*80 + "\n")
    
    beta_values = [0.0, 0.3, 0.6, 1.0]
    
    print(f"{'β':^10s} | {'M_bias':^12s} | {'M_collatz':^12s} | {'M_chi':^12s} | {'M_symbreak':^12s}")
    print("-" * 80)
    
    for beta in beta_values:
        H = EABCHamiltonian(N=300, beta=beta, gamma=1.5)
        magic = ArithmeticMagic(H)
        M = magic.compute_all(compute_nzm=False)
        
        print(f"{beta:^10.2f} | {M['M_bias']:^12.6f} | {M['M_collatz']:^12.6f} | "
              f"{M['M_chi']:^12.6f} | {M['M_symbreak']:^12.6f}")
    
    print("\nBeobachtung:")
    print("  → M_chi wächst linear mit β (wie erwartet!)")
    print("  → M_collatz und M_bias sind unabhängig von β")
    print("  → M_symbreak variiert aufgrund statistischer Fluktuationen\n")


def demo_collatz_effect():
    """
    Collatz-Demo: Effekt der Collatz-Gewichte auf Magic.
    """
    print("\n" + "="*80)
    print("DEMO 3: COLLATZ-GEWICHTE vs. UNIFORM")
    print("="*80 + "\n")
    
    N = 500
    beta = 0.5
    gamma = 1.5
    
    # Uniform
    print("[1/2] Uniform-Hamiltonian...")
    H_uniform = EABCHamiltonian(N=N, beta=beta, gamma=gamma)
    magic_uniform = ArithmeticMagic(H_uniform)
    M_uniform = magic_uniform.compute_all(compute_nzm=False)
    
    # Collatz
    print("\n[2/2] Collatz-Hamiltonian...")
    H_collatz = CollatzEABCHamiltonian(N=N, beta=beta, gamma=gamma)
    magic_collatz = ArithmeticMagic(H_collatz)
    M_collatz = magic_collatz.compute_all(compute_nzm=False)
    
    # Vergleich
    print("\n" + "="*80)
    print("VERGLEICH:")
    print("="*80)
    
    print(f"\n{'Magic-Maß':^20s} | {'Uniform':^15s} | {'Collatz':^15s} | {'Δ (Collatz-Uniform)':^20s}")
    print("-" * 80)
    
    for key in ['M_bias', 'M_collatz', 'M_chi', 'M_gap', 'M_symbreak']:
        delta = M_collatz[key] - M_uniform[key]
        sign = "✓" if abs(delta) > 0.01 else "~"
        print(f"{key:^20s} | {M_uniform[key]:^15.6f} | {M_collatz[key]:^15.6f} | "
              f"{delta:^+20.6f} {sign}")
    
    print("\nInterpretation:")
    if M_collatz['M_collatz'] > M_uniform['M_collatz']:
        print("  ✓ Collatz-Gewichte ERHÖHEN M_collatz (Anisotropie verstärkt!)")
    else:
        print("  ∼ Collatz-Gewichte haben keinen starken Effekt auf M_collatz")
    
    print()


def demo_with_nzm():
    """
    NZM-Demo: Near-Zero-Mode-Analyse (langsam!).
    """
    print("\n" + "="*80)
    print("DEMO 4: NEAR-ZERO-MODE-ANALYSE (rechenintensiv!)")
    print("="*80 + "\n")
    
    print("Warnung: Diese Analyse erfordert Spektrumsberechnung!")
    print("Für N=500 dauert dies ca. 1-2 Minuten...\n")
    
    # Kleines System
    H = EABCHamiltonian(N=500, beta=0.5, gamma=1.5)
    
    # Magic mit NZM
    magic = ArithmeticMagic(H)
    M_all = magic.compute_all(compute_nzm=True, epsilon=0.1, k=300)
    
    print(magic.summary())
    
    # Interpretation
    print("\nInterpretation von M_nzm:")
    nzm = M_all['M_nzm']
    if nzm > 0.3:
        print(f"  → M_nzm = {nzm:.4f} ist HOCH")
        print("  → Starke Kondensation nahe Fermi-Energie")
        print("  → System ist nahe am kritischen Punkt!")
    elif nzm > 0.1:
        print(f"  → M_nzm = {nzm:.4f} ist MODERAT")
        print("  → Moderate Kondensation nahe Fermi-Energie")
    else:
        print(f"  → M_nzm = {nzm:.4f} ist NIEDRIG")
        print("  → Keine signifikante Near-Zero-Mode-Kondensation")
    
    print()


def main():
    """Hauptfunktion: Führe alle Demos aus."""
    print("\n" + "="*80)
    print("ARITHMETISCHE MAGIC M_EABC: DEMO-SUITE")
    print("="*80)
    print("\nDiese Demo zeigt die Berechnung verschiedener Magic-Maße.")
    print("Für die vollständige Korrelationsanalyse: test_magic_correlation.py\n")
    
    try:
        # Demo 1: Einzelsystem
        demo_basic()
        
        # Demo 2: β-Variation
        demo_comparison()
        
        # Demo 3: Collatz vs. Uniform
        demo_collatz_effect()
        
        # Demo 4: NZM (optional, langsam)
        print("\n" + "="*80)
        print("Optional: Near-Zero-Mode-Analyse durchführen? (dauert ~2 min)")
        print("="*80)
        response = input("Eingabe [j/N]: ").strip().lower()
        
        if response in ['j', 'ja', 'y', 'yes']:
            demo_with_nzm()
        else:
            print("\n→ NZM-Analyse übersprungen.\n")
        
        print("="*80)
        print("ALLE DEMOS ABGESCHLOSSEN!")
        print("="*80)
        print("\nNächste Schritte:")
        print("  1. test_magic_correlation.py ausführen (β-Sweep, γ-Sweep)")
        print("  2. docs/magic_holography_analogy.md lesen")
        print("  3. Korrelation M_chi vs. q analysieren!")
        print("="*80 + "\n")
        
    except KeyboardInterrupt:
        print("\n\n✗ Demo abgebrochen durch Benutzer.\n")
    except Exception as e:
        print(f"\n\n✗ Fehler während Demo: {e}\n")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
