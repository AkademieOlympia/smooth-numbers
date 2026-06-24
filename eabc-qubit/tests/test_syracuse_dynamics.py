"""
Tests für Syracuse-Dynamik

Testet die Korrektheit der Syracuse-Funktion, Trajektorien-Berechnung
und Tao's Drift-Statistiken.
"""

import pytest
import numpy as np
from src.syracuse_dynamics import (
    valuation_2,
    syracuse_step,
    syracuse_trajectory,
    compute_lambda_j,
    trajectory_statistics,
    geom2_expected_drift,
    compare_empirical_vs_geom2,
    random_coprime_6_odd
)


class TestValuation2:
    """Tests für die 2-adische Valuation ν₂(n)."""
    
    def test_powers_of_two(self):
        """Test: ν₂(2^k) = k."""
        assert valuation_2(2) == 1
        assert valuation_2(4) == 2
        assert valuation_2(8) == 3
        assert valuation_2(16) == 4
        assert valuation_2(1024) == 10
    
    def test_odd_numbers(self):
        """Test: ν₂(ungerade) = 0."""
        assert valuation_2(1) == 0
        assert valuation_2(3) == 0
        assert valuation_2(5) == 0
        assert valuation_2(7) == 0
        assert valuation_2(27) == 0
    
    def test_mixed_numbers(self):
        """Test: ν₂(2^k · m) = k für ungerade m."""
        assert valuation_2(12) == 2  # 12 = 2² · 3
        assert valuation_2(18) == 1  # 18 = 2 · 9
        assert valuation_2(20) == 2  # 20 = 2² · 5
        assert valuation_2(48) == 4  # 48 = 2⁴ · 3
    
    def test_zero_raises_error(self):
        """Test: ν₂(0) ist nicht definiert."""
        with pytest.raises(ValueError):
            valuation_2(0)


class TestSyracuseStep:
    """Tests für einen Schritt der Syracuse-Funktion."""
    
    def test_basic_examples(self):
        """Test: Bekannte Syracuse-Schritte."""
        # 7 → (3·7+1)/2 = 22/2 = 11 (ν₂(22) = 1)
        result, a = syracuse_step(7)
        assert result == 11
        assert a == 1
        
        # 11 → (3·11+1)/2 = 34/2 = 17 (ν₂(34) = 1)
        result, a = syracuse_step(11)
        assert result == 17
        assert a == 1
        
        # 5 → (3·5+1)/16 = 16/16 = 1 (ν₂(16) = 4)
        result, a = syracuse_step(5)
        assert result == 1
        assert a == 4
    
    def test_even_input_raises_error(self):
        """Test: Syracuse nur für ungerade Zahlen."""
        with pytest.raises(ValueError):
            syracuse_step(4)
        with pytest.raises(ValueError):
            syracuse_step(10)
    
    def test_valuation_property(self):
        """Test: Syr(n) = (3n+1) / 2^a mit a = ν₂(3n+1)."""
        for n in [7, 11, 13, 17, 19, 23]:
            result, a = syracuse_step(n)
            expected = (3 * n + 1) // (2**a)
            assert result == expected
            assert valuation_2(3 * n + 1) == a


class TestSyracuseTrajectory:
    """Tests für Syracuse-Trajektorien."""
    
    def test_trivial_case(self):
        """Test: Trajektorie von 1 ist [1] (bereits am Ziel)."""
        trajectory, valuations = syracuse_trajectory(1, max_steps=10)
        assert trajectory == [1]
        assert valuations == []
    
    def test_short_trajectory(self):
        """Test: Trajektorie von 5 → 1 in einem Schritt."""
        trajectory, valuations = syracuse_trajectory(5, max_steps=10)
        assert trajectory == [5, 1]
        assert valuations == [4]  # ν₂(3·5+1) = ν₂(16) = 4
    
    def test_longer_trajectory(self):
        """Test: Trajektorie von 7."""
        # 7 → 11 → 17 → 13 → 5 → 1
        trajectory, valuations = syracuse_trajectory(7, max_steps=10)
        assert trajectory[0] == 7
        assert trajectory[-1] == 1
        assert len(trajectory) == 6
        assert len(valuations) == 5
    
    def test_max_steps_limit(self):
        """Test: max_steps begrenzt die Trajektorie."""
        trajectory, valuations = syracuse_trajectory(27, max_steps=3)
        assert len(trajectory) <= 4  # Start + max_steps
        assert len(valuations) <= 3
    
    def test_even_start_raises_error(self):
        """Test: Startwert muss ungerade sein."""
        with pytest.raises(ValueError):
            syracuse_trajectory(4)


class TestComputeLambdaJ:
    """Tests für Tao's lokale Drift λ_j."""
    
    def test_formula(self):
        """Test: λ_j = log(3) - a_j·log(2)."""
        # Für n=7: a=1 → λ = log(3) - log(2) = log(3/2)
        lambda_7 = compute_lambda_j(7)
        expected = np.log(3) - 1 * np.log(2)
        assert np.isclose(lambda_7, expected)
        
        # Für n=5: a=4 → λ = log(3) - 4·log(2) = log(3/16)
        lambda_5 = compute_lambda_j(5)
        expected = np.log(3) - 4 * np.log(2)
        assert np.isclose(lambda_5, expected)
    
    def test_expected_drift_range(self):
        """Test: Tao's Theorie sagt E[λ] = log(3/4) < 0 voraus."""
        # Für typische n sollte λ im Bereich [-2, +1] liegen
        test_values = [7, 11, 13, 17, 19, 23, 27, 31]
        lambdas = [compute_lambda_j(n) for n in test_values]
        
        # Alle Werte sollten endlich und im vernünftigen Bereich sein
        assert all(-5 < l < 2 for l in lambdas)
        
        # Die meisten Werte sollten negativ sein (für große Samples)
        # Für kleine Samples können wir nicht garantieren, dass der Mittelwert negativ ist
        # Stattdessen prüfen wir, dass mindestens einige negative Werte existieren
        negative_count = sum(1 for l in lambdas if l < 0)
        assert negative_count >= 1  # Mindestens einer sollte negativ sein


class TestTrajectoryStatistics:
    """Tests für Trajektorien-Statistiken."""
    
    def test_empty_trajectory(self):
        """Test: Statistiken für Trajektorie [1] (keine Valuationen)."""
        stats = trajectory_statistics([1], [])
        assert stats['stopping_time'] == 0  # Keine Schritte nötig
        assert stats['mean_valuation'] == 0.0
        assert stats['max_value'] == 1
    
    def test_simple_trajectory(self):
        """Test: Statistiken für Trajektorie von 5."""
        trajectory, valuations = syracuse_trajectory(5)
        stats = trajectory_statistics(trajectory, valuations)
        
        assert stats['stopping_time'] == 1
        assert stats['mean_valuation'] == 4.0
        assert stats['max_value'] == 5
        assert np.isclose(stats['mean_lambda'], np.log(3) - 4 * np.log(2))
    
    def test_longer_trajectory(self):
        """Test: Statistiken für Trajektorie von 27."""
        trajectory, valuations = syracuse_trajectory(27, max_steps=50)
        stats = trajectory_statistics(trajectory, valuations)
        
        assert stats['stopping_time'] > 0
        assert 0 < stats['mean_valuation'] < 10  # Vernünftiger Bereich
        assert stats['max_value'] >= 27
        assert 'lambdas' in stats


class TestGeom2Theory:
    """Tests für Tao's Geom(2)-Theorie."""
    
    def test_expected_drift_value(self):
        """Test: E[λ] = log(3/4) ≈ -0.288."""
        expected = geom2_expected_drift()
        assert np.isclose(expected, np.log(3.0 / 4.0))
        assert expected < 0  # Negative Drift
        assert -0.3 < expected < -0.28
    
    def test_empirical_vs_theory(self):
        """Test: Empirische Daten stimmen mit Geom(2) überein."""
        comparison = compare_empirical_vs_geom2(N=500, n_trajectories=50, seed=42)
        
        # ⟨a_j⟩ sollte nahe bei 2.0 liegen (innerhalb 20%)
        assert 1.5 < comparison['empirical_mean_a'] < 2.5
        
        # ⟨λ_j⟩ sollte negativ sein und nahe bei log(3/4)
        assert comparison['empirical_mean_lambda'] < 0
        assert -0.5 < comparison['empirical_mean_lambda'] < 0
        
        # Agreement-Score sollte vernünftig sein (< 50% Abweichung)
        assert comparison['agreement_a'] < 0.5
        assert comparison['agreement_lambda'] < 0.5


class TestRandomCoprimeSelection:
    """Tests für Hilfsfunktionen."""
    
    def test_random_coprime_6_odd(self):
        """Test: Generierte Zahlen sind ungerade und coprime zu 6."""
        for seed in range(10):
            n = random_coprime_6_odd(100, seed=seed)
            
            # Ungerade
            assert n % 2 == 1
            
            # Coprime zu 6 (d.h. coprime zu 2 und 3)
            assert n % 3 != 0
            
            # Im richtigen Bereich
            assert 3 <= n <= 100
    
    def test_random_coprime_reproducibility(self):
        """Test: Gleicher Seed → gleiche Zahl."""
        n1 = random_coprime_6_odd(1000, seed=42)
        n2 = random_coprime_6_odd(1000, seed=42)
        assert n1 == n2


if __name__ == "__main__":
    # Run all tests
    pytest.main([__file__, "-v"])
