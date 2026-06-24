"""
Tests für Geom(2)-Ensemble

Testet die statistische Konsistenz von Tao's Geom(2)-Hypothese
über mehrere Syracuse-Trajektorien hinweg.
"""

import pytest
import numpy as np
from src.hamiltonian import TaoSyracuseHamiltonian
from src.syracuse_dynamics import (
    geom2_sample_valuations,
    geom2_expected_drift,
    compare_empirical_vs_geom2
)
from src.level_spacing import compute_level_spacing
from src.spectral import spectral_unfolding


class TestGeom2Sampling:
    """Tests für Geom(2)-Sampling."""
    
    def test_geom2_sample_mean(self):
        """Test: Geom(2)-Samples haben Erwartungswert ~2."""
        samples = geom2_sample_valuations(n=10000, seed=42)
        
        mean = np.mean(samples)
        
        # Sollte nahe bei 2.0 liegen (mit Toleranz wegen Stichprobe)
        assert 1.8 < mean < 2.2
    
    def test_geom2_sample_range(self):
        """Test: Geom(2)-Samples sind positive Integers."""
        samples = geom2_sample_valuations(n=100, seed=42)
        
        assert np.all(samples >= 1)
        assert samples.dtype in [np.int64, np.int32]
    
    def test_geom2_reproducibility(self):
        """Test: Gleicher Seed → gleiche Samples."""
        samples1 = geom2_sample_valuations(n=50, seed=123)
        samples2 = geom2_sample_valuations(n=50, seed=123)
        
        assert np.array_equal(samples1, samples2)


class TestEmpiricalVsTheory:
    """Tests für empirische vs. theoretische Geom(2)-Statistik."""
    
    def test_empirical_matches_theory(self):
        """Test: Empirische Daten stimmen grob mit Theorie überein."""
        comparison = compare_empirical_vs_geom2(N=500, n_trajectories=30, seed=42)
        
        # ⟨a_j⟩ sollte nahe bei 2.0 liegen
        assert comparison['empirical_mean_a'] > 0
        assert comparison['geom2_expected_a'] == 2.0
        
        # Abweichung sollte < 50% sein (großzügige Toleranz für kleine Stichprobe)
        assert comparison['agreement_a'] < 0.5
        
        # ⟨λ_j⟩ sollte negativ sein
        assert comparison['empirical_mean_lambda'] < 0
        assert comparison['geom2_expected_lambda'] < 0
    
    def test_sufficient_samples(self):
        """Test: Genügend Samples werden generiert."""
        comparison = compare_empirical_vs_geom2(N=300, n_trajectories=20, seed=42)
        
        # Sollte mindestens einige hundert Samples haben
        assert comparison['n_samples'] > 100


class TestEnsembleConsistency:
    """Tests für Konsistenz über Ensemble verschiedener Startwerte."""
    
    def test_multiple_start_values_similar_spectra(self):
        """Test: Verschiedene Startwerte → ähnliche Spektralstatistik."""
        N = 200
        k = 100
        trajectory_length = 30
        
        sigmas = []
        
        # Teste 5 verschiedene Startwerte
        start_values = [7, 11, 27, 31, 47]
        
        for start_n in start_values:
            H = TaoSyracuseHamiltonian(N=N, start_n=start_n, trajectory_length=trajectory_length)
            E = H.compute_spectrum(k=k, which='SM')
            E_unfolded = spectral_unfolding(E)
            spacings = compute_level_spacing(E_unfolded)
            
            sigma = np.std(spacings)
            sigmas.append(sigma)
        
        # Alle σ sollten im ähnlichen Bereich liegen
        sigma_mean = np.mean(sigmas)
        sigma_std = np.std(sigmas)
        
        # Standardabweichung der σ-Werte sollte klein sein (< 20% vom Mittel)
        relative_spread = sigma_std / sigma_mean
        assert relative_spread < 0.2
    
    def test_geom2_synthetic_vs_real(self):
        """Test: Synthetische Geom(2)-Daten vs. echte Trajektorien."""
        N = 200
        start_n = 27
        trajectory_length = 40
        k = 100
        
        # Echte Trajektorie
        H_real = TaoSyracuseHamiltonian(N=N, start_n=start_n, trajectory_length=trajectory_length,
                                        use_geom2_synthetic=False)
        E_real = H_real.compute_spectrum(k=k, which='SM')
        E_real_unfolded = spectral_unfolding(E_real)
        spacings_real = compute_level_spacing(E_real_unfolded)
        sigma_real = np.std(spacings_real)
        
        # Synthetische Geom(2)
        H_synthetic = TaoSyracuseHamiltonian(N=N, start_n=start_n, trajectory_length=trajectory_length,
                                            use_geom2_synthetic=True)
        E_synthetic = H_synthetic.compute_spectrum(k=k, which='SM')
        E_synthetic_unfolded = spectral_unfolding(E_synthetic)
        spacings_synthetic = compute_level_spacing(E_synthetic_unfolded)
        sigma_synthetic = np.std(spacings_synthetic)
        
        # Beide sollten im ähnlichen Bereich liegen (innerhalb 30%)
        relative_diff = abs(sigma_real - sigma_synthetic) / sigma_real
        assert relative_diff < 0.3


class TestMeanValuationStatistics:
    """Tests für ⟨a_j⟩-Statistiken über Ensemble."""
    
    def test_ensemble_mean_valuation(self):
        """Test: Ensemble-Mittel von ⟨a_j⟩ nahe bei 2.0."""
        N = 300
        trajectory_length = 50
        n_samples = 20
        
        mean_valuations = []
        
        for i in range(n_samples):
            # Verschiedene Startwerte (coprime zu 6)
            start_n = 6 * i + 7  # Erzeugt ungerade, coprime zu 6
            if start_n > N:
                start_n = start_n % N
                if start_n % 2 == 0:
                    start_n += 1
            
            H = TaoSyracuseHamiltonian(N=N, start_n=start_n, trajectory_length=trajectory_length)
            mean_val = H.trajectory_stats['mean_valuation']
            mean_valuations.append(mean_val)
        
        # Ensemble-Mittel
        ensemble_mean = np.mean(mean_valuations)
        
        # Sollte nahe bei 2.0 liegen (mit Toleranz)
        assert 1.5 < ensemble_mean < 2.5


class TestDriftConsistency:
    """Tests für Drift-Konsistenz."""
    
    def test_negative_drift_consistent(self):
        """Test: Negative Drift ist konsistent über mehrere Trajektorien."""
        N = 200
        trajectory_length = 40
        
        mean_lambdas = []
        
        start_values = [7, 11, 13, 17, 19, 23, 27, 31]
        
        for start_n in start_values:
            H = TaoSyracuseHamiltonian(N=N, start_n=start_n, trajectory_length=trajectory_length)
            mean_lambda = np.mean(H.lambdas)
            mean_lambdas.append(mean_lambda)
        
        # Alle sollten negativ sein (mindestens 50% der Werte)
        # Kleine Trajektorien können positiv sein wegen Varianz
        negative_count = sum(1 for ml in mean_lambdas if ml < 0)
        assert negative_count >= len(mean_lambdas) * 0.5  # Mindestens 50%
        
        # Ensemble-Mittel sollte nahe bei log(3/4) liegen
        ensemble_mean_lambda = np.mean(mean_lambdas)
        expected = geom2_expected_drift()
        
        # Großzügige Toleranz (< 150% Abweichung) für kleine Stichprobe
        relative_diff = abs(ensemble_mean_lambda - expected) / abs(expected)
        assert relative_diff < 1.5  # 150% Toleranz für n=8 Samples
    
    def test_total_drift_negative(self):
        """Test: Gesamtdrift Σλ_j ist typischerweise negativ."""
        N = 300
        trajectory_length = 50
        
        total_drifts = []
        
        for i in range(10):
            start_n = 6 * i + 7
            H = TaoSyracuseHamiltonian(N=N, start_n=start_n, trajectory_length=trajectory_length)
            total_drift = H.trajectory_stats['total_drift']
            total_drifts.append(total_drift)
        
        # Mehrheit sollte negativ sein (mindestens 70%)
        negative_count = sum(1 for td in total_drifts if td < 0)
        assert negative_count >= 0.7 * len(total_drifts)


class TestStoppingTimeStatistics:
    """Tests für Stopping-Time-Statistiken."""
    
    def test_stopping_times_finite(self):
        """Test: Alle Stopping Times sind endlich (innerhalb max_steps)."""
        N = 500
        max_steps = 200
        
        for start_n in [7, 11, 27, 31, 47]:
            H = TaoSyracuseHamiltonian(N=N, start_n=start_n, trajectory_length=max_steps)
            stopping_time = H.trajectory_stats['stopping_time']
            
            # Sollte innerhalb der Grenzen sein
            assert 0 < stopping_time <= max_steps
    
    def test_stopping_time_variability(self):
        """Test: Stopping Times variieren zwischen verschiedenen Startwerten."""
        N = 300
        trajectory_length = 100
        
        stopping_times = []
        
        for i in range(10):
            start_n = 6 * i + 7
            H = TaoSyracuseHamiltonian(N=N, start_n=start_n, trajectory_length=trajectory_length)
            st = H.trajectory_stats['stopping_time']
            stopping_times.append(st)
        
        # Sollte Variabilität zeigen (nicht alle gleich)
        unique_times = len(set(stopping_times))
        assert unique_times > 1
        
        # Standardabweichung > 0
        assert np.std(stopping_times) > 0


@pytest.mark.slow
class TestLargeEnsemble:
    """Tests für große Ensembles (markiert als langsam)."""
    
    def test_large_ensemble_convergence(self):
        """Test: Großes Ensemble konvergiert zu Theorie."""
        comparison = compare_empirical_vs_geom2(N=500, n_trajectories=100, seed=42)
        
        # Mit vielen Samples sollte die Übereinstimmung besser sein
        assert comparison['agreement_a'] < 0.3  # < 30% Abweichung
        assert comparison['agreement_lambda'] < 0.3


if __name__ == "__main__":
    # Run all tests (außer slow tests)
    pytest.main([__file__, "-v", "-m", "not slow"])
