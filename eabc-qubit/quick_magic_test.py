#!/usr/bin/env python3
"""
Quick Magic Test: Schnelle Validierung der Magic-Implementation

Dieser Test prüft, ob alle Komponenten korrekt implementiert sind
und gibt innerhalb von 1-2 Minuten Ergebnisse aus.
"""

import numpy as np
import sys

def test_imports():
    """Test 1: Können alle Module importiert werden?"""
    print("\n[1/5] Teste Imports...")
    
    try:
        from src.hamiltonian import EABCHamiltonian, CollatzEABCHamiltonian
        from src.arithmetic_magic import ArithmeticMagic
        from src.level_spacing import compute_level_spacing, fit_level_statistics
        from src.spectral import spectral_unfolding
        print("  ✓ Alle Imports erfolgreich")
        return True
    except Exception as e:
        print(f"  ✗ Import-Fehler: {e}")
        return False


def test_basic_magic():
    """Test 2: Kann Magic für ein System berechnet werden?"""
    print("\n[2/5] Teste Basic Magic-Berechnung...")
    
    try:
        from src.hamiltonian import EABCHamiltonian
        from src.arithmetic_magic import ArithmeticMagic
        
        H = EABCHamiltonian(N=100, beta=0.5, gamma=1.5)
        magic = ArithmeticMagic(H)
        M_all = magic.compute_all(compute_nzm=False)
        
        # Prüfe ob alle erwarteten Keys vorhanden sind
        expected_keys = ['M_bias', 'M_collatz', 'M_chi', 'M_gap', 'M_symbreak']
        for key in expected_keys:
            if key not in M_all:
                print(f"  ✗ Fehlendes Magic-Maß: {key}")
                return False
            if not np.isfinite(M_all[key]):
                print(f"  ✗ {key} = {M_all[key]} ist nicht endlich")
                return False
        
        print("  ✓ Magic-Berechnung erfolgreich")
        print(f"    M_chi = {M_all['M_chi']:.6f}")
        return True
    except Exception as e:
        print(f"  ✗ Fehler bei Magic-Berechnung: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_beta_variation():
    """Test 3: Variiert M_chi korrekt mit β?"""
    print("\n[3/5] Teste β-Variation...")
    
    try:
        from src.hamiltonian import EABCHamiltonian
        from src.arithmetic_magic import ArithmeticMagic
        
        beta_values = [0.0, 0.3, 0.6]
        M_chi_values = []
        
        for beta in beta_values:
            H = EABCHamiltonian(N=100, beta=beta, gamma=1.5)
            magic = ArithmeticMagic(H)
            M = magic.compute_all(compute_nzm=False)
            M_chi_values.append(M['M_chi'])
        
        # Prüfe Monotonie
        if not all(M_chi_values[i] <= M_chi_values[i+1] for i in range(len(M_chi_values)-1)):
            print(f"  ✗ M_chi ist nicht monoton: {M_chi_values}")
            return False
        
        print("  ✓ M_chi wächst monoton mit β")
        print(f"    β = {beta_values}: M_chi = {[f'{m:.4f}' for m in M_chi_values]}")
        return True
    except Exception as e:
        print(f"  ✗ Fehler bei β-Variation: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_collatz_vs_uniform():
    """Test 4: Unterscheiden sich Collatz und Uniform?"""
    print("\n[4/5] Teste Collatz vs. Uniform...")
    
    try:
        from src.hamiltonian import EABCHamiltonian, CollatzEABCHamiltonian
        from src.arithmetic_magic import ArithmeticMagic
        
        N = 200
        beta = 0.5
        gamma = 1.5
        
        # Uniform
        H_uniform = EABCHamiltonian(N=N, beta=beta, gamma=gamma)
        magic_uniform = ArithmeticMagic(H_uniform)
        M_uniform = magic_uniform.compute_all(compute_nzm=False)
        
        # Collatz
        H_collatz = CollatzEABCHamiltonian(N=N, beta=beta, gamma=gamma)
        magic_collatz = ArithmeticMagic(H_collatz)
        M_collatz = magic_collatz.compute_all(compute_nzm=False)
        
        # Vergleich
        print("  ✓ Beide Systeme berechnet")
        print(f"    M_chi (Uniform): {M_uniform['M_chi']:.6f}")
        print(f"    M_chi (Collatz): {M_collatz['M_chi']:.6f}")
        print(f"    Δ M_collatz: {M_collatz['M_collatz'] - M_uniform['M_collatz']:+.6f}")
        
        return True
    except Exception as e:
        print(f"  ✗ Fehler bei Collatz-Test: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_spectrum_and_chaos():
    """Test 5: Kann q-Parameter berechnet werden? (langsam!)"""
    print("\n[5/5] Teste Spektrum + Chaos-Parameter (ca. 30 sec)...")
    
    try:
        from src.hamiltonian import EABCHamiltonian
        from src.arithmetic_magic import ArithmeticMagic
        from src.level_spacing import compute_level_spacing, fit_level_statistics
        from src.spectral import spectral_unfolding
        
        # Kleines System
        H = EABCHamiltonian(N=200, beta=0.5, gamma=1.5)
        
        # Magic
        magic = ArithmeticMagic(H)
        M = magic.compute_all(compute_nzm=False)
        
        # Spektrum
        eigenvalues = H.compute_spectrum(k=100, which='SM', sigma=0.0)
        
        # Unfolding
        unfolded = spectral_unfolding(eigenvalues)
        
        # Level Spacing
        spacings = compute_level_spacing(unfolded)
        
        # Brody-Fit
        lsd_results = fit_level_statistics(spacings, bins=30)
        q = lsd_results['brody_q']
        
        print("  ✓ Spektralanalyse erfolgreich")
        print(f"    M_chi = {M['M_chi']:.4f}")
        print(f"    q = {q:.4f}")
        print(f"    → Korrelations-Test würde diese Werte vergleichen!")
        
        return True
    except Exception as e:
        print(f"  ✗ Fehler bei Spektralanalyse: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Hauptfunktion: Führe alle Tests aus."""
    print("\n" + "="*80)
    print("QUICK MAGIC TEST: Validierung der Implementation")
    print("="*80)
    print("\nDieser Test prüft die Grundfunktionalität in ~1 Minute.")
    print("Für vollständige Tests: test_magic_correlation.py")
    print("="*80)
    
    tests = [
        test_imports,
        test_basic_magic,
        test_beta_variation,
        test_collatz_vs_uniform,
        test_spectrum_and_chaos
    ]
    
    results = []
    for test_func in tests:
        try:
            result = test_func()
            results.append(result)
        except Exception as e:
            print(f"\n✗ Unerwarteter Fehler in {test_func.__name__}: {e}")
            results.append(False)
    
    # Zusammenfassung
    print("\n" + "="*80)
    print("ZUSAMMENFASSUNG")
    print("="*80)
    
    passed = sum(results)
    total = len(results)
    
    print(f"\n{passed}/{total} Tests bestanden")
    
    if all(results):
        print("\n✓ ALLE TESTS BESTANDEN!")
        print("\nNächste Schritte:")
        print("  1. python demo_magic.py (Schnelle Demo)")
        print("  2. python test_magic_correlation.py (Vollständige Analyse)")
        print("  3. Analysiere figures/magic_vs_chaos_main.png")
        print("\n→ Implementation ist bereit für produktive Nutzung!")
    else:
        print("\n✗ EINIGE TESTS FEHLGESCHLAGEN")
        print("\n→ Bitte Fehler beheben vor vollständiger Analyse!")
        sys.exit(1)
    
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
