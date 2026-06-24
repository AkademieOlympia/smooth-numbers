"""
Unit-Tests für Collatz-Gewichte-Modul

Testet die Korrektheit der Collatz log(r)-Raten und verwandter Funktionen.
"""

import pytest
import numpy as np
from src.collatz_weights import (
    collatz_log_rate,
    collatz_log_rate_prime,
    collatz_weights_array,
    random_soup_weights,
    analyze_collatz_distribution
)
from src.primes import generate_primes


class TestCollatzLogRate:
    """Tests für collatz_log_rate Funktion."""
    
    def test_class_E_kontraktor(self):
        """E-Klasse (n ≡ 1 mod 12) sollte Kontraktor sein."""
        assert collatz_log_rate(13) < 0  # 13 ≡ 1 (mod 12)
        assert collatz_log_rate(37) < 0  # 37 ≡ 1 (mod 12)
        assert np.isclose(collatz_log_rate(13), -np.log(2))
    
    def test_class_A_kontraktor(self):
        """A-Klasse (n ≡ 5 mod 12) sollte Kontraktor sein."""
        assert collatz_log_rate(5) < 0   # 5 ≡ 5 (mod 12)
        assert collatz_log_rate(17) < 0  # 17 ≡ 5 (mod 12)
    
    def test_class_B_expander(self):
        """B-Klasse (n ≡ 7 mod 12) sollte Expander sein."""
        assert collatz_log_rate(7) > 0   # 7 ≡ 7 (mod 12)
        assert collatz_log_rate(19) > 0  # 19 ≡ 7 (mod 12)
        assert np.isclose(collatz_log_rate(7), +np.log(2))
    
    def test_class_C_expander(self):
        """C-Klasse (n ≡ 11 mod 12) sollte Expander sein."""
        assert collatz_log_rate(11) > 0  # 11 ≡ 11 (mod 12)
        assert collatz_log_rate(23) > 0  # 23 ≡ 11 (mod 12)
    
    def test_special_primes(self):
        """Spezialfälle p = 2 und p = 3."""
        assert collatz_log_rate(2) < 0   # E (Kontraktor)
        assert collatz_log_rate(3) < 0   # A (Kontraktor)
    
    def test_consistency_with_prime_function(self):
        """collatz_log_rate und collatz_log_rate_prime sollten konsistent sein."""
        primes = generate_primes(100)
        for p in primes:
            assert np.isclose(
                collatz_log_rate(p),
                collatz_log_rate_prime(p)
            )


class TestCollatzWeightsArray:
    """Tests für collatz_weights_array Funktion."""
    
    def test_array_length(self):
        """Array sollte dieselbe Länge wie Primzahl-Liste haben."""
        primes = generate_primes(100)
        weights = collatz_weights_array(100, primes)
        assert len(weights) == len(primes)
    
    def test_array_values_range(self):
        """Alle Gewichte sollten im erwarteten Bereich liegen."""
        primes = generate_primes(100)
        weights = collatz_weights_array(100, primes)
        
        # E: -log(2) ≈ -0.693 (stärkster Kontraktor)
        # C: +log(3/2) ≈ +0.405 (stärkster Expander in dieser Parametrisierung)
        assert np.all(weights >= -np.log(2) - 0.01)  # Mit kleiner Toleranz
        assert np.all(weights <= +np.log(2) + 0.01)
    
    def test_nonzero_variance(self):
        """Gewichte sollten nicht alle gleich sein."""
        primes = generate_primes(100)
        weights = collatz_weights_array(100, primes)
        assert np.std(weights) > 0


class TestRandomSoupWeights:
    """Tests für random_soup_weights Funktion."""
    
    def test_reproducibility(self):
        """Mit festem seed sollten identische Gewichte erzeugt werden."""
        weights1 = random_soup_weights(100, seed=42)
        weights2 = random_soup_weights(100, seed=42)
        assert np.allclose(weights1, weights2)
    
    def test_different_seeds_different_results(self):
        """Verschiedene seeds sollten verschiedene Gewichte erzeugen."""
        weights1 = random_soup_weights(100, seed=42)
        weights2 = random_soup_weights(100, seed=123)
        assert not np.allclose(weights1, weights2)
    
    def test_correct_length(self):
        """Array sollte die angeforderte Länge haben."""
        n = 50
        weights = random_soup_weights(n)
        assert len(weights) == n
    
    def test_permutation_property(self):
        """Random Soup sollte aus denselben Basiswerten bestehen (permutiert)."""
        n = 100
        weights = random_soup_weights(n, seed=42)
        
        # Sollte nur die vier EABC-Werte enthalten
        base_values = {
            -np.log(2),
            -np.log(2) + np.log(3)/2,
            +np.log(2),
            +np.log(3) - np.log(2)
        }
        
        unique_weights = set(np.unique(np.round(weights, 6)))
        base_values_rounded = set(np.round(list(base_values), 6))
        
        assert unique_weights.issubset(base_values_rounded)


class TestAnalyzeCollatzDistribution:
    """Tests für analyze_collatz_distribution Funktion."""
    
    def test_all_classes_present(self):
        """Analyse sollte alle vier EABC-Klassen enthalten."""
        primes = generate_primes(100)
        stats = analyze_collatz_distribution(100, primes)
        
        assert 'E' in stats
        assert 'A' in stats
        assert 'B' in stats
        assert 'C' in stats
    
    def test_counts_sum_to_total(self):
        """Summe der Klassenzählungen sollte Gesamtzahl der Primzahlen sein."""
        primes = generate_primes(100)
        stats = analyze_collatz_distribution(100, primes)
        
        total_count = sum(stats[cls]['count'] for cls in ['E', 'A', 'B', 'C'])
        assert total_count == len(primes)
    
    def test_log_rates_correct(self):
        """log_rate-Werte sollten korrekt zugeordnet sein."""
        primes = generate_primes(100)
        stats = analyze_collatz_distribution(100, primes)
        
        assert np.isclose(stats['E']['log_rate'], -np.log(2))
        assert np.isclose(stats['B']['log_rate'], +np.log(2))
        assert stats['A']['log_rate'] < 0  # Kontraktor
        assert stats['C']['log_rate'] > 0  # Expander


class TestPhysicalProperties:
    """Tests für physikalische Eigenschaften der Collatz-Gewichte."""
    
    def test_net_drift_approximately_zero(self):
        """
        G2-Axiom: Der Netto-Drift sollte näherungsweise null sein.
        
        Dies ist eine fundamentale Eigenschaft der Collatz-Vermutung:
        Die Summe aller log(r)-Raten sollte im Mittel gegen null gehen.
        """
        primes = generate_primes(10000)
        weights = collatz_weights_array(10000, primes)
        
        mean_drift = np.mean(weights)
        
        # Toleranz: Der mittlere Drift sollte klein sein (nicht exakt null)
        assert np.abs(mean_drift) < 0.1
    
    def test_kontraktoren_vs_expanders(self):
        """Sollte sowohl Kontraktoren als auch Expander enthalten."""
        primes = generate_primes(1000)
        weights = collatz_weights_array(1000, primes)
        
        kontraktoren = np.sum(weights < 0)
        expanders = np.sum(weights > 0)
        
        assert kontraktoren > 0
        assert expanders > 0
        
        # Sollte näherungsweise balanciert sein
        ratio = kontraktoren / expanders
        assert 0.5 < ratio < 2.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
