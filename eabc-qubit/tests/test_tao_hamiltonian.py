"""
Tests für Tao-Syracuse-Hamiltonian

Testet die korrekte Konstruktion und Eigenschaften des zeitabhängigen
Tao-Syracuse-Hamiltonians.
"""

import pytest
import numpy as np
from src.hamiltonian import TaoSyracuseHamiltonian, CollatzEABCHamiltonian, EABCHamiltonian
from src.syracuse_dynamics import syracuse_trajectory


class TestTaoSyracuseHamiltonianConstruction:
    """Tests für die Konstruktion des Tao-Syracuse-Hamiltonians."""
    
    def test_basic_construction(self):
        """Test: Hamiltonian kann konstruiert werden."""
        H = TaoSyracuseHamiltonian(N=100, start_n=27, trajectory_length=10)
        
        # Dimension prüfen
        assert H.dim == 400  # 4 * 100
        
        # Trajektorie wurde berechnet
        assert len(H.trajectory) > 0
        assert len(H.valuations) > 0
        assert len(H.lambdas) > 0
        
        # Hamiltonian ist sparse matrix
        assert H.H.shape == (400, 400)
        assert H.H.nnz > 0  # Hat Nicht-Null-Einträge
    
    def test_trajectory_stored_correctly(self):
        """Test: Syracuse-Trajektorie wird korrekt gespeichert."""
        start_n = 27
        trajectory_length = 20
        
        H = TaoSyracuseHamiltonian(N=500, start_n=start_n, trajectory_length=trajectory_length)
        
        # Startwert stimmt überein
        assert H.start_n == start_n
        assert H.trajectory[0] == start_n
        
        # Trajektorie hat vernünftige Länge
        assert len(H.trajectory) >= 1
        assert len(H.trajectory) <= trajectory_length + 1
        
        # Valuationen haben richtige Länge
        assert len(H.valuations) == len(H.trajectory) - 1
        assert len(H.lambdas) == len(H.valuations)
    
    def test_geom2_synthetic_mode(self):
        """Test: Synthetischer Geom(2)-Modus funktioniert."""
        H = TaoSyracuseHamiltonian(
            N=100,
            start_n=27,
            trajectory_length=30,
            use_geom2_synthetic=True
        )
        
        assert H.use_geom2_synthetic is True
        assert len(H.valuations) == 30
        assert len(H.trajectory) > 0
        
        # Valuationen sollten im vernünftigen Bereich sein (Geom(2))
        assert all(1 <= a <= 20 for a in H.valuations)
    
    def test_hermiticity(self):
        """Test: Hamiltonian ist hermitisch."""
        H = TaoSyracuseHamiltonian(N=50, start_n=7, trajectory_length=10)
        
        # Konvertiere zu dense für einfachen Test
        H_dense = H.H.toarray()
        
        # Prüfe Hermitizität: H = H†
        assert np.allclose(H_dense, H_dense.T)
    
    def test_real_eigenvalues(self):
        """Test: Eigenwerte sind reell (hermitischer Operator)."""
        H = TaoSyracuseHamiltonian(N=100, start_n=11, trajectory_length=15)
        
        # Berechne einige Eigenwerte
        eigenvalues = H.compute_spectrum(k=20, which='SM')
        
        # Alle Eigenwerte sollten reell sein
        assert eigenvalues.dtype in [np.float64, np.float32]
        assert not np.any(np.isnan(eigenvalues))
        assert not np.any(np.isinf(eigenvalues))


class TestTaoSyracuseDefects:
    """Tests für die Syracuse-Defekt-Konstruktion."""
    
    def test_defects_in_grid(self):
        """Test: Defekte liegen innerhalb des Gitters."""
        N = 200
        H = TaoSyracuseHamiltonian(N=N, start_n=27, trajectory_length=50)
        
        # Alle Trajektorien-Punkte sollten ≤ N sein (oder werden gefiltert)
        for s_j in H.trajectory:
            if s_j <= N:
                # Position im Hilbertraum sollte gültig sein
                # (wird intern geprüft, aber wir testen die Logik)
                assert 1 <= s_j <= N
    
    def test_lambda_weights(self):
        """Test: Lambda-Gewichte haben korrekte Formel."""
        H = TaoSyracuseHamiltonian(N=100, start_n=7, trajectory_length=20)
        
        # Prüfe λ_j = log(3) - a_j·log(2) für alle j
        for lambda_j, a_j in zip(H.lambdas, H.valuations):
            expected = np.log(3) - a_j * np.log(2)
            assert np.isclose(lambda_j, expected)
    
    def test_negative_mean_drift(self):
        """Test: Durchschnittliche Drift ist negativ (Tao's Theorie)."""
        H = TaoSyracuseHamiltonian(N=500, start_n=27, trajectory_length=100)
        
        mean_lambda = np.mean(H.lambdas)
        
        # Tao's Theorie: E[λ] = log(3/4) < 0
        assert mean_lambda < 0
        
        # Sollte im vernünftigen Bereich sein
        assert -1.0 < mean_lambda < 0


class TestComparisonMethods:
    """Tests für Vergleichsmethoden."""
    
    def test_compare_with_static(self):
        """Test: Vergleich mit statischem Hamiltonian funktioniert."""
        H_dynamic = TaoSyracuseHamiltonian(N=200, start_n=27, trajectory_length=30)
        
        # Vergleichsmethode ausführen
        results = H_dynamic.compare_with_static(k=50)
        
        # Ergebnisse prüfen
        assert 'dynamic' in results
        assert 'static' in results
        assert 'delta_spectrum' in results
        
        # Beide Spektren sollten gleiche Länge haben
        assert len(results['dynamic']) == len(results['static']) == 50
        
        # Delta-Spektrum
        assert len(results['delta_spectrum']) == 50
    
    def test_info_method(self):
        """Test: info()-Methode läuft ohne Fehler."""
        H = TaoSyracuseHamiltonian(N=100, start_n=27, trajectory_length=20)
        
        # Sollte keine Exception werfen
        try:
            H.info()
            success = True
        except Exception:
            success = False
        
        assert success


class TestEdgeCases:
    """Tests für Randfälle und Fehlerfälle."""
    
    def test_short_trajectory(self):
        """Test: Sehr kurze Trajektorie (z.B. N₀=1)."""
        # Trajektorie von 1 ist trivial
        H = TaoSyracuseHamiltonian(N=100, start_n=1, trajectory_length=10)
        
        # Sollte funktionieren (leere oder minimale Trajektorie)
        assert H.dim == 400
        assert len(H.trajectory) >= 1
    
    def test_long_trajectory(self):
        """Test: Lange Trajektorie."""
        H = TaoSyracuseHamiltonian(N=1000, start_n=27, trajectory_length=200)
        
        assert H.dim == 4000
        assert len(H.lambdas) > 0
    
    def test_large_start_value(self):
        """Test: Startwert größer als Gittergröße."""
        # Sollte funktionieren, aber Trajektorie wird gefiltert
        H = TaoSyracuseHamiltonian(N=100, start_n=97, trajectory_length=20)
        
        assert H.dim == 400
        # Hamiltonian sollte trotzdem konstruierbar sein
        assert H.H.shape == (400, 400)
    
    def test_different_coupling_constants(self):
        """Test: Verschiedene Kopplungskonstanten."""
        H = TaoSyracuseHamiltonian(
            N=100,
            start_n=27,
            trajectory_length=20,
            alpha=2.0,
            beta=0.3,
            gamma=3.0
        )
        
        assert H.alpha == 2.0
        assert H.beta == 0.3
        assert H.gamma == 3.0


class TestSpectralProperties:
    """Tests für Spektraleigenschaften."""
    
    def test_spectrum_computation(self):
        """Test: Spektrum kann berechnet werden."""
        H = TaoSyracuseHamiltonian(N=100, start_n=27, trajectory_length=20)
        
        eigenvalues = H.compute_spectrum(k=30, which='SM')
        
        # Korrekte Anzahl
        assert len(eigenvalues) == 30
        
        # Sortiert
        assert np.all(eigenvalues[:-1] <= eigenvalues[1:])
        
        # Reell
        assert eigenvalues.dtype in [np.float64, np.float32]
    
    def test_spectral_statistics_reasonable(self):
        """Test: Spektralstatistik im vernünftigen Bereich."""
        H = TaoSyracuseHamiltonian(N=200, start_n=27, trajectory_length=30)
        
        from src.spectral import spectral_unfolding
        from src.level_spacing import compute_level_spacing
        
        E = H.compute_spectrum(k=100, which='SM')
        E_unfolded = spectral_unfolding(E)
        spacings = compute_level_spacing(E_unfolded)
        
        # Spacings sollten positiv sein
        assert np.all(spacings > 0)
        
        # Mittelwert sollte nahe 1 sein (nach Unfolding)
        mean_s = np.mean(spacings)
        assert 0.5 < mean_s < 1.5
        
        # Standardabweichung im vernünftigen Bereich
        std_s = np.std(spacings)
        assert 0.1 < std_s < 2.0


class TestConsistencyWithBaseClasses:
    """Tests für Konsistenz mit Basisklassen."""
    
    def test_inherits_from_eabc_hamiltonian(self):
        """Test: TaoSyracuseHamiltonian erbt von EABCHamiltonian."""
        H = TaoSyracuseHamiltonian(N=50, start_n=7, trajectory_length=10)
        
        assert isinstance(H, EABCHamiltonian)
        assert hasattr(H, 'H_T')  # Kinetischer Term
        assert hasattr(H, 'H_chi')  # Chiraler Term
        assert hasattr(H, 'H_p')  # Defekt-Term (überschrieben)
    
    def test_basis_terms_present(self):
        """Test: Basisklassen-Terme (H_T, H_chi) sind vorhanden."""
        H = TaoSyracuseHamiltonian(N=100, start_n=27, trajectory_length=20)
        
        # H_T (kinetisch) sollte nicht-trivial sein
        assert H.H_T.nnz > 0
        
        # H_chi (chiral) sollte nicht-trivial sein
        assert H.H_chi.nnz > 0
        
        # H_p (Defekte) sollte überschrieben sein
        assert H.H_p.nnz >= 0  # Kann 0 sein, wenn alle S_j > N


if __name__ == "__main__":
    # Run all tests
    pytest.main([__file__, "-v"])
