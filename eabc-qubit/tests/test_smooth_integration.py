"""
Tests für Smooth Numbers Integration
"""

import pytest
import numpy as np
from src.smooth_integration import (
    is_k_smooth,
    count_k_smooth,
    smooth_density,
    smooth_density_fast,
    largest_prime_factor,
    compute_smooth_triangle,
    smooth_potential_landscape,
    analyze_smooth_statistics
)
from src.hamiltonian import MultiLayerHamiltonian


class TestSmoothNumbers:
    """Tests für grundlegende Smooth-Number-Funktionen."""
    
    def test_is_k_smooth_basic(self):
        """Test k-Glattheit für bekannte Beispiele."""
        # 1 ist für alle k glatt
        assert is_k_smooth(1, 2) == True
        assert is_k_smooth(1, 10) == True
        
        # 12 = 2² × 3 ist 3-glatt
        assert is_k_smooth(12, 3) == True
        assert is_k_smooth(12, 2) == False
        
        # 30 = 2 × 3 × 5 ist 5-glatt
        assert is_k_smooth(30, 5) == True
        assert is_k_smooth(30, 3) == False
        
        # 97 ist Primzahl, nur für k ≥ 97 glatt
        assert is_k_smooth(97, 97) == True
        assert is_k_smooth(97, 96) == False
    
    def test_count_k_smooth(self):
        """Test Zählung k-glatter Zahlen."""
        # 2-glatte Zahlen bis 10: {1, 2, 4, 8}
        assert count_k_smooth(10, 2) == 4
        
        # 3-glatte Zahlen bis 10: {1, 2, 3, 4, 6, 8, 9}
        assert count_k_smooth(10, 3) == 7
        
        # 5-glatte Zahlen bis 10: {1, 2, 3, 4, 5, 6, 8, 9, 10}
        assert count_k_smooth(10, 5) == 9
    
    def test_largest_prime_factor(self):
        """Test größter Primfaktor."""
        assert largest_prime_factor(1) == 1
        assert largest_prime_factor(2) == 2
        assert largest_prime_factor(12) == 3  # 12 = 2² × 3
        assert largest_prime_factor(14) == 7  # 14 = 2 × 7
        assert largest_prime_factor(97) == 97  # 97 ist Primzahl
    
    def test_smooth_density(self):
        """Test Glattheitsdichte."""
        # 1 ist für alle k glatt → Dichte = 1.0
        assert smooth_density(1, max_k=10) == 1.0
        
        # Primzahlen haben niedrige Dichte
        density_prime = smooth_density(97, max_k=10)
        assert density_prime < 0.2
        
        # Glatte Zahlen haben hohe Dichte
        density_smooth = smooth_density(12, max_k=10)
        assert density_smooth > 0.5
    
    def test_smooth_density_fast_matches_slow(self):
        """Test dass schnelle und langsame Variante übereinstimmen."""
        test_numbers = [1, 2, 12, 30, 97, 128, 210]
        max_k = 20
        
        for n in test_numbers:
            slow = smooth_density(n, max_k)
            fast = smooth_density_fast(n, max_k)
            assert abs(slow - fast) < 1e-10, f"Mismatch für n={n}: slow={slow}, fast={fast}"
    
    def test_compute_smooth_triangle(self):
        """Test Dreieck-Berechnung."""
        triangle = compute_smooth_triangle(n_max=10, k_max=5)
        
        # Form prüfen
        assert triangle.shape == (10, 5)
        
        # Monotonie: T(n, k) wächst mit n für festes k
        for k in range(5):
            for n in range(9):
                assert triangle[n+1, k] >= triangle[n, k]
        
        # Monotonie: T(n, k) wächst mit k für festes n
        for n in range(10):
            for k in range(4):
                assert triangle[n, k+1] >= triangle[n, k]
        
        # T(n, n) = n (alle Zahlen bis n sind n-glatt)
        for n in range(1, 6):
            assert triangle[n-1, n-1] == n
    
    def test_smooth_potential_landscape(self):
        """Test Potentiallandschaft."""
        landscape = smooth_potential_landscape(N=100, max_k=10)
        
        # Form prüfen
        assert len(landscape) == 100
        
        # Alle Werte im Bereich [0, 1]
        assert np.all(landscape >= 0.0)
        assert np.all(landscape <= 1.0)
        
        # Glatte Zahlen sollten hohe Dichte haben
        # z.B. n=1, n=2, n=4, n=8
        assert landscape[0] == 1.0  # n=1
        assert landscape[1] > 0.8   # n=2
        assert landscape[3] > 0.7   # n=4
    
    def test_analyze_smooth_statistics(self):
        """Test statistische Analyse."""
        stats = analyze_smooth_statistics(N=100, max_k=10)
        
        # Prüfe Schlüssel
        assert 'N' in stats
        assert 'max_k' in stats
        assert 'mean_density' in stats
        assert 'std_density' in stats
        assert 'smoothest_numbers' in stats
        assert 'roughest_numbers' in stats
        
        # Werte plausibel
        assert stats['mean_density'] > 0.0
        assert stats['mean_density'] < 1.0
        assert stats['std_density'] > 0.0
        
        # Glatteste Zahl sollte 1 sein
        smoothest = stats['smoothest_numbers'][0]
        assert smoothest[0] == 1  # n=1
        assert smoothest[1] == 1.0  # Dichte=1.0


class TestMultiLayerHamiltonian:
    """Tests für MultiLayerHamiltonian."""
    
    def test_initialization_no_layers(self):
        """Test Initialisierung ohne zusätzliche Schichten."""
        H = MultiLayerHamiltonian(
            N=50,
            use_primes=False,
            use_collatz=False,
            use_smooth=False
        )
        
        assert H.N == 50
        assert H.dim == 200  # 4N
        assert not H.use_primes
        assert not H.use_collatz
        assert not H.use_smooth
    
    def test_initialization_primes_only(self):
        """Test mit nur Primzahl-Defekten."""
        H = MultiLayerHamiltonian(
            N=50,
            gamma=1.5,
            use_primes=True,
            use_collatz=False,
            use_smooth=False
        )
        
        assert H.use_primes
        assert not H.use_collatz
        assert not H.use_smooth
        assert H.H_p.nnz > 0  # Primzahl-Defekte vorhanden
    
    def test_initialization_smooth_only(self):
        """Test mit nur Glattheitspotential."""
        H = MultiLayerHamiltonian(
            N=50,
            eta=0.5,
            use_primes=False,
            use_collatz=False,
            use_smooth=True,
            smooth_max_k=10
        )
        
        assert not H.use_primes
        assert not H.use_collatz
        assert H.use_smooth
        assert H.H_smooth.nnz > 0  # Smooth-Potential vorhanden
        assert len(H.smooth_landscape) == 50
    
    def test_initialization_all_layers(self):
        """Test mit allen Schichten."""
        H = MultiLayerHamiltonian(
            N=50,
            gamma=1.5,
            eta=0.5,
            use_primes=True,
            use_collatz=True,
            use_smooth=True,
            smooth_max_k=10
        )
        
        assert H.use_primes
        assert H.use_collatz
        assert H.use_smooth
        assert H.H_p.nnz > 0
        assert H.H_smooth.nnz > 0
    
    def test_spectrum_computation(self):
        """Test Spektrum-Berechnung."""
        H = MultiLayerHamiltonian(
            N=50,
            use_primes=True,
            use_smooth=True
        )
        
        # Berechne 20 Eigenwerte
        eigenvalues = H.compute_spectrum(k=20, which='SM')
        
        assert len(eigenvalues) == 20
        assert np.all(np.isfinite(eigenvalues))
        assert np.all(eigenvalues[1:] >= eigenvalues[:-1])  # Sortierung
    
    def test_hamiltonian_hermiticity(self):
        """Test dass Hamiltonian hermitesch ist."""
        H = MultiLayerHamiltonian(
            N=20,
            use_primes=True,
            use_smooth=True
        )
        
        # Konvertiere zu dense für Test (nur für kleine N!)
        H_dense = H.H.toarray()
        
        # Prüfe Hermitizität: H = H†
        assert np.allclose(H_dense, H_dense.T.conj())
    
    def test_smooth_potential_diagonal(self):
        """Test dass Smooth-Potential diagonal ist."""
        H = MultiLayerHamiltonian(
            N=20,
            use_primes=False,
            use_smooth=True
        )
        
        H_smooth_dense = H.H_smooth.toarray()
        
        # Prüfe dass nur Diagonale nicht-Null ist
        off_diagonal = H_smooth_dense - np.diag(np.diag(H_smooth_dense))
        assert np.allclose(off_diagonal, 0.0)
    
    def test_smooth_potential_negative(self):
        """Test dass Smooth-Potential negative Werte hat (Senken)."""
        H = MultiLayerHamiltonian(
            N=50,
            eta=0.5,
            use_primes=False,
            use_smooth=True
        )
        
        # Extrahiere Diagonalelemente
        diagonal = H.H_smooth.diagonal()
        
        # Alle Werte sollten ≤ 0 sein (negative Potentiale = Senken)
        assert np.all(diagonal <= 0.0)
        
        # Mindestens einige sollte stark negativ sein
        assert np.any(diagonal < -0.1)
    
    def test_parameter_scaling(self):
        """Test Skalierung mit eta."""
        H1 = MultiLayerHamiltonian(N=30, eta=0.5, use_smooth=True, use_primes=False)
        H2 = MultiLayerHamiltonian(N=30, eta=1.0, use_smooth=True, use_primes=False)
        
        # H2.H_smooth sollte doppelt so stark sein wie H1.H_smooth
        # Vergleiche Diagonalelemente direkt (keine sparse Division)
        diag1 = H1.H_smooth.diagonal()
        diag2 = H2.H_smooth.diagonal()
        ratio = diag2 / diag1
        
        # Alle Ratios sollten 2.0 sein (außer wo beide 0 sind)
        non_zero_mask = np.abs(diag1) > 1e-10
        assert np.allclose(ratio[non_zero_mask], 2.0)


class TestSmoothPrimeInteraction:
    """Tests für Interaktion zwischen Smooth und Primes."""
    
    def test_primes_are_rough(self):
        """Test dass Primzahlen niedrige Glattheitsdichte haben."""
        landscape = smooth_potential_landscape(N=100, max_k=20)
        
        # Bekannte Primzahlen
        # WICHTIG: Kleine Primzahlen wie 2, 3, 5, 7 sind für max_k=20 
        # eigentlich relativ glatt (sie sind k-glatt für k ≥ p).
        # Nur größere Primzahlen (p > max_k) haben Dichte ≈ 0.
        
        # Teste nur Primzahlen > max_k/2 (d.h. > 10)
        primes = [11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
        
        for p in primes:
            if p <= 100:
                # Diese größeren Primzahlen sollten niedrigere Dichte haben
                # (aber nicht notwendigerweise < 0.5, da p < max_k für p ≤ 20)
                if p > 20:
                    # Primzahlen > max_k sollten Dichte = 0 haben
                    assert landscape[p-1] < 0.1, f"Primzahl {p} hat zu hohe Dichte: {landscape[p-1]}"
    
    def test_smooth_primes_conflict(self):
        """Test dass Smooth und Primes gegenläufige Effekte haben."""
        N = 100
        
        # Hamiltonian nur mit Primzahl-Defekten
        H_primes = MultiLayerHamiltonian(
            N=N,
            gamma=1.0,
            eta=0.0,
            use_primes=True,
            use_smooth=False
        )
        
        # Hamiltonian nur mit Smooth-Potential
        H_smooth = MultiLayerHamiltonian(
            N=N,
            gamma=0.0,
            eta=1.0,
            use_primes=False,
            use_smooth=True
        )
        
        # An Primzahlpositionen:
        # - H_primes hat positive Energie (Defekte)
        # - H_smooth hat negative Energie (Primzahlen sind rau)
        
        # Prüfe Position einer Primzahl (z.B. p=7)
        p = 7
        sigma = 2  # EABC-Index von 7 (7 ≡ 7 mod 12 → B)
        idx = 4 * (p - 1) + sigma
        
        # H_primes sollte positiv sein
        E_prime = H_primes.H_p.toarray()[idx, idx]
        assert E_prime > 0
        
        # H_smooth sollte weniger negativ sein (Primzahl = rau)
        E_smooth = H_smooth.H_smooth.toarray()[idx, idx]
        assert E_smooth < 0
        
        # Bei glatten Zahlen (z.B. n=12) sollte H_smooth stärker negativ sein
        n_smooth = 12
        sigma_smooth = 0  # EABC-Index von 12 (12 ≡ 0 mod 12 → E)
        idx_smooth = 4 * (n_smooth - 1) + sigma_smooth
        E_smooth_at_smooth = H_smooth.H_smooth.toarray()[idx_smooth, idx_smooth]
        
        # Glatte Zahl sollte stärker negatives Potential haben
        assert E_smooth_at_smooth < E_smooth


def test_integration_example():
    """Integrationstest: Vollständiges Beispiel."""
    print("\n=== Integrationstest: Smooth Integration ===")
    
    # Baue Multi-Layer-Hamiltonian
    H = MultiLayerHamiltonian(
        N=100,
        alpha=1.0,
        beta=0.5,
        gamma=1.5,
        eta=0.5,
        use_primes=True,
        use_collatz=True,
        use_smooth=True,
        smooth_max_k=20
    )
    
    # Zeige Info
    H.info()
    
    # Berechne Spektrum
    eigenvalues = H.compute_spectrum(k=50, which='SM')
    
    print(f"\nErste 10 Eigenwerte:")
    for i, E in enumerate(eigenvalues[:10]):
        print(f"  E_{i+1} = {E:.6f}")
    
    # Prüfungen
    assert len(eigenvalues) == 50
    assert np.all(np.isfinite(eigenvalues))
    
    print("\n✓ Integrationstest erfolgreich!")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
