"""
Pivot-Distanz-Analyse Helper-Funktionen
========================================

Berechnet Distanzen d_k(p) = |p - k| für Primzahlen p und analysiert
diese durch die EABC-Linse.

Autor: H13 Pivot Distance Analysis
Datum: 2026-06-24
"""

import numpy as np
from typing import List, Dict, Tuple
from functools import cache
import sympy


def generate_primes(limit: int) -> np.ndarray:
    """
    Generiert alle Primzahlen p < limit.
    
    Args:
        limit: Obere Grenze (exklusiv)
        
    Returns:
        numpy array mit Primzahlen
    """
    return np.array(list(sympy.primerange(2, limit)))


def compute_pivot_distance(p: int, pivot: int) -> int:
    """
    Berechnet Pivot-Distanz d_k(p) = |p - k|.
    
    Args:
        p: Primzahl
        pivot: Pivot-Punkt k
        
    Returns:
        Absolute Distanz |p - k|
    """
    return abs(p - pivot)


def compute_eabc_entropy(eabc_vector: np.ndarray) -> float:
    """
    Berechnet Shannon-Entropie E(v) des EABC-Vektors.
    
    E(v) = -Σ p_i log₂(p_i)
    
    wobei p_i = v_i / Ω_EABC (normalisierte Häufigkeiten).
    
    Args:
        eabc_vector: EABC-Vektor [e, a, b, c]
        
    Returns:
        Shannon-Entropie (bits), oder 0.0 falls alle Komponenten 0
    """
    omega_eabc = np.sum(eabc_vector)
    
    if omega_eabc == 0:
        return 0.0
    
    # Normalisierte Wahrscheinlichkeiten
    p = eabc_vector / omega_eabc
    
    # Entferne Nullen (log(0) ist undefiniert)
    p_nonzero = p[p > 0]
    
    if len(p_nonzero) == 0:
        return 0.0
    
    # Shannon-Entropie
    entropy = -np.sum(p_nonzero * np.log2(p_nonzero))
    
    return entropy


def analyze_pivot_for_primes(
    primes: np.ndarray,
    pivot: int,
    eabc_data_getter,
    include_factorization: bool = True
) -> Dict[str, np.ndarray]:
    """
    Analysiert Pivot-Distanzen für alle gegebenen Primzahlen.
    
    Args:
        primes: Array von Primzahlen
        pivot: Pivot-Punkt k
        eabc_data_getter: Funktion n -> EABC-Koordinaten (z.B. EABCTestData.get_coordinates)
        include_factorization: Berechne auch Faktorisierungs-Eigenschaften
        
    Returns:
        Dictionary mit Arrays:
        - 'p': Primzahlen
        - 'd_k': Distanzen d_k(p)
        - 'eabc_p': EABC-Klasse von p
        - 'eabc_d': EABC-Vektor von d_k(p)
        - 'omega_d': Ω(d_k(p))
        - 'shell_d': S(d_k(p))
        - 'H_d': H(d_k(p))
        - 'E_d': E(d_k(p)) - Entropie
    """
    from utils.eabc import eabc_class
    
    n_primes = len(primes)
    
    # Ausgabe-Arrays
    results = {
        'p': primes,
        'd_k': np.zeros(n_primes, dtype=int),
        'eabc_p': np.empty(n_primes, dtype='U10'),
        'eabc_d': np.zeros((n_primes, 4), dtype=int),
        'omega_d': np.zeros(n_primes, dtype=int),
        'shell_d': np.zeros(n_primes, dtype=int),
        'H_d': np.zeros(n_primes, dtype=float),
        'E_d': np.zeros(n_primes, dtype=float)
    }
    
    for i, p in enumerate(primes):
        # Distanz
        d_k = compute_pivot_distance(p, pivot)
        results['d_k'][i] = d_k
        
        # EABC-Klasse von p
        results['eabc_p'][i] = eabc_class(p)
        
        # EABC-Eigenschaften von d_k(p)
        if d_k >= 2:
            coords = eabc_data_getter(d_k)
            results['eabc_d'][i] = [coords['e'], coords['a'], coords['b'], coords['c']]
            results['omega_d'][i] = coords['omega']
            results['shell_d'][i] = coords['shell']
            results['H_d'][i] = coords['H'] if not np.isnan(coords['H']) else 0.0
            results['E_d'][i] = compute_eabc_entropy(results['eabc_d'][i])
        else:
            # d_k < 2: Keine sinnvolle EABC-Analyse
            results['eabc_d'][i] = [0, 0, 0, 0]
            results['omega_d'][i] = 0
            results['shell_d'][i] = 0
            results['H_d'][i] = 0.0
            results['E_d'][i] = 0.0
    
    return results


def compute_eabc_correlation(
    eabc_p: np.ndarray,
    eabc_d: np.ndarray
) -> Dict[str, float]:
    """
    Berechnet Korrelationen zwischen EABC(p) und EABC(d_k(p)).
    
    Args:
        eabc_p: Array von EABC-Klassen für Primzahlen p ['E', 'A', 'B', 'C', ...]
        eabc_d: Array von EABC-Vektoren für d_k(p), Shape (n, 4)
        
    Returns:
        Dictionary mit Statistiken:
        - Kontingenz-Tabelle (EABC(p) × dominante EABC-Klasse von d_k(p))
        - Chi²-Test-Ergebnisse
    """
    from scipy.stats import chi2_contingency
    
    # Dominante EABC-Klasse von d_k(p)
    class_names = ['E', 'A', 'B', 'C']
    dominant_class_d = np.array([
        class_names[np.argmax(vec)] if np.sum(vec) > 0 else 'none'
        for vec in eabc_d
    ])
    
    # Filtere nur gültige Primzahlen (E, A, B, C)
    valid_mask = np.isin(eabc_p, ['E', 'A', 'B', 'C'])
    eabc_p_valid = eabc_p[valid_mask]
    dominant_class_d_valid = dominant_class_d[valid_mask]
    
    # Kontingenz-Tabelle
    contingency = {}
    for p_class in ['E', 'A', 'B', 'C']:
        contingency[p_class] = {}
        mask_p = eabc_p_valid == p_class
        for d_class in ['E', 'A', 'B', 'C', 'none']:
            count = np.sum((eabc_p_valid == p_class) & (dominant_class_d_valid == d_class))
            contingency[p_class][d_class] = count
    
    # Chi²-Test
    # Erstelle numerische Kontingenz-Matrix
    matrix = np.zeros((4, 5), dtype=int)
    for i, p_class in enumerate(['E', 'A', 'B', 'C']):
        for j, d_class in enumerate(['E', 'A', 'B', 'C', 'none']):
            matrix[i, j] = contingency[p_class][d_class]
    
    chi2, p_value, dof, expected = chi2_contingency(matrix)
    
    return {
        'contingency': contingency,
        'chi2': chi2,
        'p_value': p_value,
        'dof': dof,
        'expected': expected
    }


def compare_pivot_distributions(
    results_dict: Dict[int, Dict[str, np.ndarray]]
) -> Dict[str, Dict]:
    """
    Vergleicht Verteilungen über verschiedene Pivots.
    
    Args:
        results_dict: Dictionary {pivot: results_for_pivot}
        
    Returns:
        Dictionary mit Vergleichsstatistiken:
        - 'variance': Varianz von d_k(p) für jeden Pivot
        - 'entropy_mean': Mittlere Entropie E(d_k(p))
        - 'H_mean': Mittlere Konzentration H(d_k(p))
        - 'omega_mean': Mittleres Ω(d_k(p))
    """
    comparison = {
        'variance': {},
        'entropy_mean': {},
        'entropy_std': {},
        'H_mean': {},
        'H_std': {},
        'omega_mean': {},
        'omega_std': {}
    }
    
    for pivot, results in results_dict.items():
        # Varianz der Distanzen
        comparison['variance'][pivot] = np.var(results['d_k'])
        
        # Entropie-Statistiken (nur für d_k >= 2)
        valid_mask = results['d_k'] >= 2
        E_d_valid = results['E_d'][valid_mask]
        comparison['entropy_mean'][pivot] = np.mean(E_d_valid) if len(E_d_valid) > 0 else 0.0
        comparison['entropy_std'][pivot] = np.std(E_d_valid) if len(E_d_valid) > 0 else 0.0
        
        # H-Statistiken
        H_d_valid = results['H_d'][valid_mask]
        H_d_valid = H_d_valid[~np.isnan(H_d_valid)]
        comparison['H_mean'][pivot] = np.mean(H_d_valid) if len(H_d_valid) > 0 else 0.0
        comparison['H_std'][pivot] = np.std(H_d_valid) if len(H_d_valid) > 0 else 0.0
        
        # Omega-Statistiken
        omega_d_valid = results['omega_d'][valid_mask]
        comparison['omega_mean'][pivot] = np.mean(omega_d_valid) if len(omega_d_valid) > 0 else 0.0
        comparison['omega_std'][pivot] = np.std(omega_d_valid) if len(omega_d_valid) > 0 else 0.0
    
    return comparison


def create_contingency_table(
    eabc_p: np.ndarray,
    eabc_d: np.ndarray
) -> Tuple[np.ndarray, List[str], List[str]]:
    """
    Erstellt Kontingenz-Tabelle für EABC(p) × EABC(d_k(p)).
    
    Args:
        eabc_p: EABC-Klassen der Primzahlen
        eabc_d: EABC-Vektoren von d_k(p)
        
    Returns:
        (matrix, row_labels, col_labels)
        - matrix: Häufigkeitsmatrix
        - row_labels: EABC-Klassen von p
        - col_labels: Dominante EABC-Klassen von d_k(p)
    """
    class_names = ['E', 'A', 'B', 'C']
    
    # Dominante EABC-Klasse von d_k(p)
    dominant_class_d = np.array([
        class_names[np.argmax(vec)] if np.sum(vec) > 0 else 'none'
        for vec in eabc_d
    ])
    
    # Erstelle Matrix
    row_labels = ['E', 'A', 'B', 'C']
    col_labels = ['E', 'A', 'B', 'C', 'none']
    
    matrix = np.zeros((len(row_labels), len(col_labels)), dtype=int)
    
    for i, p_class in enumerate(row_labels):
        for j, d_class in enumerate(col_labels):
            count = np.sum((eabc_p == p_class) & (dominant_class_d == d_class))
            matrix[i, j] = count
    
    return matrix, row_labels, col_labels


# Beispieltest
if __name__ == "__main__":
    print("Pivot-Analyse Helper-Funktionen Tests:")
    print()
    
    # Test 1: Entropie-Berechnung
    test_vectors = [
        np.array([4, 0, 0, 0]),  # Maximale Konzentration
        np.array([1, 1, 1, 1]),  # Maximale Gleichverteilung
        np.array([2, 1, 1, 0]),  # Gemischt
        np.array([0, 0, 0, 0])   # Keine EABC-Faktoren
    ]
    
    print("Test 1: EABC-Entropie E(v):")
    for v in test_vectors:
        E = compute_eabc_entropy(v)
        print(f"  v = {v} → E(v) = {E:.4f} bits")
    
    print()
    
    # Test 2: Primzahl-Generierung
    print("Test 2: Primzahl-Generierung:")
    primes_small = generate_primes(100)
    print(f"  Primzahlen < 100: {len(primes_small)} Stück")
    print(f"  Erste 10: {primes_small[:10]}")
    
    print()
    
    # Test 3: Pivot-Distanzen
    print("Test 3: Pivot-Distanzen für p ∈ {37, 41, 43, 47} mit k=40:")
    test_primes = [37, 41, 43, 47]
    pivot = 40
    for p in test_primes:
        d = compute_pivot_distance(p, pivot)
        print(f"  d_{pivot}({p}) = {d}")
