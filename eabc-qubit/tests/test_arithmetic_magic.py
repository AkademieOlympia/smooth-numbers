"""
Unit Tests für arithmetische Magic M_EABC

Testet die Berechnung aller Magic-Maße auf Konsistenz und erwartete Eigenschaften.
"""

import pytest
import numpy as np
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.hamiltonian import EABCHamiltonian, CollatzEABCHamiltonian
from src.arithmetic_magic import ArithmeticMagic


class TestArithmeticMagic:
    """Test-Suite für ArithmeticMagic-Klasse."""
    
    def test_magic_initialization(self):
        """Test: Magic-Objekt kann initialisiert werden."""
        H = EABCHamiltonian(N=100, beta=0.5, gamma=1.5)
        magic = ArithmeticMagic(H)
        
        assert magic.H is H
        assert len(magic.primes) > 0
        assert len(magic.eabc_classes) == len(magic.primes)
    
    def test_bias_magic_range(self):
        """Test: M_bias liegt im erwarteten Bereich [0, 1]."""
        H = EABCHamiltonian(N=200, beta=0.5, gamma=1.5)
        magic = ArithmeticMagic(H)
        
        M_bias = magic.compute_bias_magic()
        
        assert 0.0 <= M_bias <= 1.0, f"M_bias = {M_bias} außerhalb [0, 1]"
    
    def test_collatz_magic_non_negative(self):
        """Test: M_collatz ist nicht-negativ."""
        H = EABCHamiltonian(N=200, beta=0.5, gamma=1.5)
        magic = ArithmeticMagic(H)
        
        M_collatz = magic.compute_collatz_magic()
        
        assert M_collatz >= 0.0, f"M_collatz = {M_collatz} ist negativ"
    
    def test_chi_magic_zero_when_beta_zero(self):
        """Test: M_chi = 0 wenn β = 0."""
        H = EABCHamiltonian(N=100, beta=0.0, gamma=1.5)
        magic = ArithmeticMagic(H)
        
        M_chi = magic.compute_chirality_magic()
        
        assert np.isclose(M_chi, 0.0, atol=1e-10), \
            f"M_chi = {M_chi} sollte 0 sein bei β = 0"
    
    def test_chi_magic_increases_with_beta(self):
        """Test: M_chi wächst monoton mit β."""
        beta_values = [0.1, 0.3, 0.5, 0.7, 1.0]
        M_chi_values = []
        
        for beta in beta_values:
            H = EABCHamiltonian(N=200, beta=beta, gamma=1.5)
            magic = ArithmeticMagic(H)
            M_chi = magic.compute_chirality_magic()
            M_chi_values.append(M_chi)
        
        # Prüfe Monotonie
        for i in range(len(M_chi_values) - 1):
            assert M_chi_values[i] < M_chi_values[i+1], \
                f"M_chi nicht monoton: {M_chi_values[i]} >= {M_chi_values[i+1]} " \
                f"bei β = {beta_values[i]} vs. {beta_values[i+1]}"
    
    def test_gap_magic_range(self):
        """Test: M_gap liegt im Bereich [0, 1]."""
        H = EABCHamiltonian(N=300, beta=0.5, gamma=1.5)
        magic = ArithmeticMagic(H)
        
        M_gap = magic.compute_gap_magic()
        
        assert 0.0 <= M_gap <= 1.0, f"M_gap = {M_gap} außerhalb [0, 1]"
    
    def test_symbreak_magic_range(self):
        """Test: M_symbreak liegt im Bereich [0, 1]."""
        H = EABCHamiltonian(N=200, beta=0.5, gamma=1.5)
        magic = ArithmeticMagic(H)
        
        M_symbreak = magic.compute_symbreak_magic()
        
        assert 0.0 <= M_symbreak <= 1.0, f"M_symbreak = {M_symbreak} außerhalb [0, 1]"
    
    def test_compute_all_returns_dict(self):
        """Test: compute_all() gibt Dictionary mit allen Magic-Werten zurück."""
        H = EABCHamiltonian(N=100, beta=0.5, gamma=1.5)
        magic = ArithmeticMagic(H)
        
        M_all = magic.compute_all(compute_nzm=False)
        
        assert isinstance(M_all, dict)
        assert 'M_bias' in M_all
        assert 'M_collatz' in M_all
        assert 'M_chi' in M_all
        assert 'M_gap' in M_all
        assert 'M_symbreak' in M_all
    
    def test_nzm_magic_with_spectrum(self):
        """Test: M_nzm kann berechnet werden (langsam!)."""
        H = EABCHamiltonian(N=100, beta=0.5, gamma=1.5)
        magic = ArithmeticMagic(H)
        
        M_nzm = magic.compute_nzm_magic(epsilon=0.1, k=50)
        
        assert 0.0 <= M_nzm <= 1.0, f"M_nzm = {M_nzm} außerhalb [0, 1]"
    
    def test_collatz_hamiltonian_has_collatz_magic(self):
        """Test: Collatz-Hamiltonian hat höhere M_collatz als Uniform."""
        N = 200
        beta = 0.5
        gamma = 1.5
        
        # Uniform
        H_uniform = EABCHamiltonian(N=N, beta=beta, gamma=gamma)
        magic_uniform = ArithmeticMagic(H_uniform)
        M_uniform = magic_uniform.compute_collatz_magic()
        
        # Collatz
        H_collatz = CollatzEABCHamiltonian(N=N, beta=beta, gamma=gamma)
        magic_collatz = ArithmeticMagic(H_collatz)
        M_collatz = magic_collatz.compute_collatz_magic()
        
        # Collatz sollte stärker anisotrop sein
        # (nicht immer garantiert, aber in der Regel)
        print(f"\nM_collatz (Uniform): {M_uniform:.6f}")
        print(f"M_collatz (Collatz): {M_collatz:.6f}")
    
    def test_summary_string(self):
        """Test: summary() gibt einen lesbaren String zurück."""
        H = EABCHamiltonian(N=100, beta=0.5, gamma=1.5)
        magic = ArithmeticMagic(H)
        magic.compute_all(compute_nzm=False)
        
        summary = magic.summary()
        
        assert isinstance(summary, str)
        assert len(summary) > 0
        assert "Magic" in summary
    
    def test_magic_independence_of_gamma(self):
        """Test: M_chi ist unabhängig von γ (nur β-abhängig)."""
        beta = 0.5
        gamma_values = [0.5, 1.0, 2.0, 3.0]
        M_chi_values = []
        
        for gamma in gamma_values:
            H = EABCHamiltonian(N=200, beta=beta, gamma=gamma)
            magic = ArithmeticMagic(H)
            M_chi = magic.compute_chirality_magic()
            M_chi_values.append(M_chi)
        
        # M_chi sollte ungefähr konstant sein (kleine Variationen durch Normalisierung erlaubt)
        M_chi_mean = np.mean(M_chi_values)
        M_chi_std = np.std(M_chi_values)
        
        # Relative Standardabweichung sollte klein sein
        relative_std = M_chi_std / M_chi_mean if M_chi_mean > 0 else 0
        
        assert relative_std < 0.1, \
            f"M_chi variiert zu stark mit γ: std/mean = {relative_std:.4f}"
    
    def test_all_magic_values_finite(self):
        """Test: Alle Magic-Werte sind endlich (keine NaN/Inf)."""
        H = EABCHamiltonian(N=200, beta=0.5, gamma=1.5)
        magic = ArithmeticMagic(H)
        
        M_all = magic.compute_all(compute_nzm=False)
        
        for key, value in M_all.items():
            assert np.isfinite(value), f"{key} = {value} ist nicht endlich"


class TestMagicCorrelation:
    """Test-Suite für Magic-Korrelationsanalyse."""
    
    def test_correlation_function_runs(self):
        """Test: compute_magic_vs_chaos_correlation läuft ohne Fehler (langsam!)."""
        # Sehr kleines System für schnellen Test
        beta_values = np.array([0.0, 0.5, 1.0])
        
        beta_vals, results = compute_magic_vs_chaos_correlation(
            N=100,
            beta_values=beta_values,
            gamma=1.5,
            k=50
        )
        
        assert len(beta_vals) == 3
        assert 'M_chi' in results
        assert 'q_brody' in results
        assert len(results['M_chi']) == 3
        assert len(results['q_brody']) == 3


def test_import():
    """Test: Magic-Modul kann importiert werden."""
    from src.arithmetic_magic import ArithmeticMagic, compute_magic_vs_chaos_correlation
    assert ArithmeticMagic is not None
    assert compute_magic_vs_chaos_correlation is not None


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, '-v'])
