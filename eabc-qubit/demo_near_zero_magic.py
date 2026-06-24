#!/usr/bin/env python3
"""
Demo: Near-Zero-Magic M_EABC (Primäre Definition)

Diese Demo zeigt die Near-Zero-basierte Magic-Definition, die direkt zur
Quanteninformations-Definition von Magic passt.

**Kausale Hierarchie:**
```
Near-Zero-Spektrum → chiraler Drift → ABCE/CEAB-Asymmetrie
```

Magic ist die Ursache (im Near-Zero-Sektor), Bias ist die Wirkung!
"""

import numpy as np
from src.hamiltonian import EABCHamiltonian
from src.arithmetic_magic import ArithmeticMagic


def demo_near_zero_basic():
    """
    Demo 1: Basis-Berechnung der Near-Zero-Magic.
    """
    print("\n" + "="*80)
    print("DEMO 1: NEAR-ZERO-MAGIC - BASIS")
    print("="*80 + "\n")
    
    print("Erstelle EABC-Hamiltonian...")
    H = EABCHamiltonian(N=300, beta=0.5, gamma=1.5)
    H.info()
    
    print("\nBerechne Near-Zero-Magic (Primäre Definition)...")
    magic = ArithmeticMagic(H)
    
    # Near-Zero-Magic berechnen
    M_nz = magic.compute_near_zero_magic(
        epsilon=0.1,
        k=200,  # Kleines k für schnelle Demo
        mode='spectral_weighted',
        pattern='ABCE_CEAB'
    )
    
    # Ausgabe
    print("\n" + "="*80)
    print("NEAR-ZERO-MAGIC ERGEBNISSE:")
    print("="*80)
    print(f"\nM_near_zero:     {M_nz['M_near_zero']:.6f}  ← PRIMÄRER WERT")
    print(f"Anzahl NZM:      {M_nz['n_nzm']}")
    print(f"⟨Asymmetrie⟩:    {M_nz['mean_asymmetry']:.6f}")
    print(f"max(Asymmetrie): {M_nz['max_asymmetry']:.6f}")
    print(f"Gesamtgewicht:   {M_nz['total_weight']:.6f}")
    
    print("\nInterpretation:")
    if M_nz['M_near_zero'] > 0.1:
        print("  → M_near_zero ist HOCH")
        print("  → Starke Asymmetrie im Near-Zero-Sektor")
        print("  → Dies treibt chiralen Drift und führt zu beobachtbarem Bias!")
    elif M_nz['M_near_zero'] > 0.05:
        print("  → M_near_zero ist MODERAT")
        print("  → Moderate Asymmetrie im Near-Zero-Sektor")
    else:
        print("  → M_near_zero ist NIEDRIG")
        print("  → Geringe Asymmetrie, System ist nahe an Symmetrie")
    
    print("="*80 + "\n")


def demo_near_zero_vs_global():
    """
    Demo 2: Near-Zero-Magic vs. Globale Metriken.
    """
    print("\n" + "="*80)
    print("DEMO 2: NEAR-ZERO-MAGIC vs. GLOBALE METRIKEN")
    print("="*80 + "\n")
    
    beta_values = [0.0, 0.3, 0.6, 1.0]
    
    print(f"{'β':^10s} | {'M_near_zero':^15s} | {'n_nzm':^10s} | "
          f"{'M_chi':^15s} | {'Δ':^15s}")
    print("-" * 80)
    
    for beta in beta_values:
        H = EABCHamiltonian(N=200, beta=beta, gamma=1.5)
        magic = ArithmeticMagic(H)
        
        # Globale Metrik (schnell)
        M_global = magic.compute_all(compute_near_zero=False, compute_nzm=False)
        
        # Near-Zero-Magic (langsam)
        M_nz = magic.compute_near_zero_magic(epsilon=0.1, k=150, mode='spectral_weighted')
        
        delta = M_nz['M_near_zero'] - M_global['M_chi']
        
        print(f"{beta:^10.2f} | {M_nz['M_near_zero']:^15.6f} | {M_nz['n_nzm']:^10.0f} | "
              f"{M_global['M_chi']:^15.6f} | {delta:^+15.6f}")
    
    print("\nBeobachtung:")
    print("  → Near-Zero-Magic erfasst die lokale Asymmetrie im kritischen Sektor")
    print("  → Globale M_chi misst nur die makroskopische Chiralität")
    print("  → Near-Zero ist der 'Ofen', M_chi ist das 'Thermometer'!")
    print("\n")


def demo_pattern_comparison():
    """
    Demo 3: ABCE/CEAB vs. EABC/ECBA Muster.
    """
    print("\n" + "="*80)
    print("DEMO 3: PATTERN-VERGLEICH")
    print("="*80 + "\n")
    
    H = EABCHamiltonian(N=200, beta=0.5, gamma=1.5)
    magic = ArithmeticMagic(H)
    
    # Pattern 1: ABCE/CEAB
    print("[1/2] Berechne ABCE/CEAB-Magic...")
    M_nz_1 = magic.compute_near_zero_magic(
        epsilon=0.1, k=150, mode='spectral_weighted', pattern='ABCE_CEAB'
    )
    
    # Pattern 2: EABC/ECBA
    print("\n[2/2] Berechne EABC/ECBA-Magic...")
    M_nz_2 = magic.compute_near_zero_magic(
        epsilon=0.1, k=150, mode='spectral_weighted', pattern='EABC_ECBA'
    )
    
    print("\n" + "="*80)
    print("VERGLEICH:")
    print("="*80)
    
    print(f"\n{'Pattern':^20s} | {'M_near_zero':^15s} | {'⟨Asymmetrie⟩':^15s}")
    print("-" * 60)
    print(f"{'ABCE/CEAB':^20s} | {M_nz_1['M_near_zero']:^15.6f} | {M_nz_1['mean_asymmetry']:^15.6f}")
    print(f"{'EABC/ECBA':^20s} | {M_nz_2['M_near_zero']:^15.6f} | {M_nz_2['mean_asymmetry']:^15.6f}")
    
    diff = abs(M_nz_1['M_near_zero'] - M_nz_2['M_near_zero'])
    print(f"\nAbsolute Differenz: {diff:.6f}")
    
    if diff < 0.01:
        print("  ✓ Beide Muster sind konsistent (Differenz < 0.01)")
    else:
        print("  ∼ Muster zeigen unterschiedliche Signaturen")
    
    print("="*80 + "\n")


def demo_epsilon_sensitivity():
    """
    Demo 4: Sensitivität bezüglich ε (Near-Zero-Schwelle).
    """
    print("\n" + "="*80)
    print("DEMO 4: ε-SENSITIVITÄT")
    print("="*80 + "\n")
    
    H = EABCHamiltonian(N=200, beta=0.5, gamma=1.5)
    magic = ArithmeticMagic(H)
    
    epsilon_values = [0.05, 0.1, 0.15, 0.2]
    
    print(f"{'ε':^10s} | {'M_near_zero':^15s} | {'n_nzm':^10s} | {'⟨Asym⟩':^15s}")
    print("-" * 60)
    
    for epsilon in epsilon_values:
        M_nz = magic.compute_near_zero_magic(epsilon=epsilon, k=150, mode='spectral_weighted')
        
        print(f"{epsilon:^10.2f} | {M_nz['M_near_zero']:^15.6f} | "
              f"{M_nz['n_nzm']:^10.0f} | {M_nz['mean_asymmetry']:^15.6f}")
    
    print("\nBeobachtung:")
    print("  → Bei kleinerem ε: weniger Moden, aber höhere Gewichte")
    print("  → Bei größerem ε: mehr Moden, aber niedrigere Gewichte")
    print("  → Optimaler Kompromiss: ε ≈ 0.1 - 0.15")
    print("="*80 + "\n")


def main():
    """Hauptfunktion: Führe alle Demos aus."""
    print("\n" + "="*80)
    print("NEAR-ZERO-MAGIC M_EABC: DEMO-SUITE (PRIMÄRE DEFINITION)")
    print("="*80)
    print("\nKausale Hierarchie:")
    print("  Near-Zero-Spektrum → chiraler Drift → ABCE/CEAB-Asymmetrie")
    print("\nMagic ist die Ursache (im Near-Zero-Sektor), Bias ist die Wirkung!")
    print("="*80)
    
    try:
        # Demo 1: Basis
        demo_near_zero_basic()
        
        # Demo 2: Near-Zero vs. Global
        demo_near_zero_vs_global()
        
        # Demo 3: Pattern-Vergleich
        demo_pattern_comparison()
        
        # Demo 4: ε-Sensitivität
        demo_epsilon_sensitivity()
        
        print("="*80)
        print("ALLE DEMOS ABGESCHLOSSEN!")
        print("="*80)
        print("\nNächste Schritte:")
        print("  1. test_near_zero_causality.py ausführen (Kausalitäts-Tests)")
        print("  2. Korrelation M_near_zero vs. q analysieren")
        print("  3. Vergleiche mit test_magic_correlation.py (globale Metriken)")
        print("\n→ Ist M_near_zero stärker korreliert mit q als M_chi?")
        print("="*80 + "\n")
        
    except KeyboardInterrupt:
        print("\n\n✗ Demo abgebrochen durch Benutzer.\n")
    except Exception as e:
        print(f"\n\n✗ Fehler während Demo: {e}\n")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
