"""
Tests für den EABC-Hamiltonian
"""

import pytest
import numpy as np
import scipy.sparse as sp
from src.hamiltonian import EABCHamiltonian


def test_hamiltonian_dimensions():
    """Test: Dimensionen sind korrekt (4N × 4N)."""
    N = 50
    H = EABCHamiltonian(N, alpha=1.0, beta=0.5, gamma=1.0)
    
    assert H.N == N
    assert H.dim == 4 * N
    assert H.H.shape == (4 * N, 4 * N)


def test_hamiltonian_hermiticity():
    """Test: Hamiltonian ist hermitisch."""
    N = 30
    H = EABCHamiltonian(N, alpha=1.0, beta=0.5, gamma=1.0)
    
    # H sollte symmetrisch sein (reell und hermitisch)
    diff = H.H - H.H.T
    max_diff = np.abs(diff.data).max() if diff.nnz > 0 else 0
    
    assert max_diff < 1e-10


def test_hamiltonian_real():
    """Test: Hamiltonian ist reell."""
    N = 30
    H = EABCHamiltonian(N, alpha=1.0, beta=0.5, gamma=1.0)
    
    # Alle Einträge sollten reell sein
    assert np.all(np.isreal(H.H.data))


def test_tight_binding_term():
    """Test: Kinetischer Term hat korrekte Struktur."""
    N = 10
    H = EABCHamiltonian(N, alpha=1.0, beta=0.0, gamma=0.0)
    
    # Mit beta = gamma = 0 ist H = H_T
    # H_T sollte Nebendiagonalen haben (Hopping)
    
    # Prüfe Bandstruktur
    H_dense = H.H.toarray()
    
    # Diagonal sollte Nullen haben (kein On-Site-Term)
    diag = np.diag(H_dense)
    assert np.allclose(diag, 0)
    
    # Nebendiagonalen sollten nicht-Null sein
    # (aber mit 4×4 Blöcken wegen Kronecker-Produkt)
    assert np.any(np.abs(H_dense) > 0)


def test_chiral_term():
    """Test: Chiraler Term hat Z₄-Struktur."""
    N = 5
    H = EABCHamiltonian(N, alpha=0.0, beta=1.0, gamma=0.0)
    
    # Mit alpha = gamma = 0 ist H = H_χ
    H_dense = H.H.toarray()
    
    # H_χ sollte Block-Diagonal sein (Kronecker-Produkt mit I_N)
    # Jeder 4×4 Block sollte (χ + χ†) sein
    
    for i in range(N):
        block = H_dense[4*i:4*(i+1), 4*i:4*(i+1)]
        
        # χ + χ† hat Struktur:
        # [[0, 1, 0, 1],
        #  [1, 0, 1, 0],
        #  [0, 1, 0, 1],
        #  [1, 0, 1, 0]]
        
        expected = np.array([
            [0, 1, 0, 1],
            [1, 0, 1, 0],
            [0, 1, 0, 1],
            [1, 0, 1, 0]
        ], dtype=float)
        
        assert np.allclose(block, expected)


def test_prime_defects():
    """Test: Primzahl-Defekte sind an korrekten Positionen."""
    N = 50
    H = EABCHamiltonian(N, alpha=0.0, beta=0.0, gamma=1.0)
    
    # Mit alpha = beta = 0 ist H = H_p
    # H_p sollte nur auf Diagonale nicht-Null sein
    
    H_dense = H.H.toarray()
    diag = np.diag(H_dense)
    
    # Zähle Nicht-Null-Einträge
    non_zero_count = np.sum(diag > 0)
    
    # Sollte gleich Anzahl Primzahlen ≤ N sein
    from src.primes import generate_primes
    primes = generate_primes(N)
    
    assert non_zero_count == len(primes)


def test_spectrum_computation():
    """Test: Spektrumsberechnung läuft durch."""
    N = 50
    H = EABCHamiltonian(N, alpha=1.0, beta=0.5, gamma=1.0)
    
    eigenvalues = H.compute_spectrum(k=20, which='SM')
    
    assert len(eigenvalues) == 20
    assert np.all(np.isreal(eigenvalues))
    
    # Eigenwerte sollten sortiert sein
    assert np.all(np.diff(eigenvalues) >= 0)


def test_eigenvectors_orthogonality():
    """Test: Eigenvektoren sind orthonormal."""
    N = 20
    H = EABCHamiltonian(N, alpha=1.0, beta=0.5, gamma=1.0)
    
    eigenvalues, eigenvectors = H.compute_spectrum(k=10, return_eigenvectors=True)
    
    # Prüfe Orthonormalität: V^T V = I
    overlap = eigenvectors.T @ eigenvectors
    identity = np.eye(10)
    
    assert np.allclose(overlap, identity, atol=1e-8)


def test_parameter_scaling():
    """Test: Parameter skalieren korrekt."""
    N = 30
    
    H1 = EABCHamiltonian(N, alpha=1.0, beta=0.5, gamma=1.0)
    H2 = EABCHamiltonian(N, alpha=2.0, beta=0.5, gamma=1.0)
    
    # Bei Verdopplung von alpha sollten sich Eigenwerte ändern
    E1 = H1.compute_spectrum(k=10, which='SM')
    E2 = H2.compute_spectrum(k=10, which='SM')
    
    assert not np.allclose(E1, E2)


def test_periodic_boundary_conditions():
    """Test: Periodische Randbedingungen funktionieren."""
    N = 20
    
    H_open = EABCHamiltonian(N, alpha=1.0, beta=0.0, gamma=0.0, periodic=False)
    H_periodic = EABCHamiltonian(N, alpha=1.0, beta=0.0, gamma=0.0, periodic=True)
    
    # Spektren sollten sich unterscheiden
    E_open = H_open.compute_spectrum(k=10, which='SM')
    E_periodic = H_periodic.compute_spectrum(k=10, which='SM')
    
    assert not np.allclose(E_open, E_periodic)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
