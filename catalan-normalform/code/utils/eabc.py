"""
EABC-Vektor und Konzentrationsmessung H(n).

Implementiert die Berechnung des EABC-Vektors v = (e, a, b, c)
für die Gauß-Eisenstein-Klassifikation von Primfaktoren.
"""

import numpy as np
from typing import List, Tuple, Dict
from functools import cache


def prime_factors_with_multiplicity(n: int) -> List[int]:
    """
    Berechnet Primfaktorzerlegung mit Vielfachheit.
    
    Beispiel: 60 = 2² × 3 × 5 → [2, 2, 3, 5]
    """
    if n < 2:
        return []
    
    factors = []
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors.append(d)
            n //= d
        d += 1
    if n > 1:
        factors.append(n)
    return factors


def count_prime_factors(n: int) -> int:
    """Anzahl Primfaktoren mit Vielfachheit (Ω(n))."""
    return len(prime_factors_with_multiplicity(n))


def padicval(n: int, p: int) -> int:
    """p-adische Bewertung: Maximale Potenz von p, die n teilt."""
    if n == 0:
        return float('inf')
    
    val = 0
    while n % p == 0:
        val += 1
        n //= p
    return val


def sum_of_divisors(n: int) -> int:
    """Summe aller Teiler σ(n)."""
    if n < 1:
        return 0
    
    result = 0
    i = 1
    while i * i <= n:
        if n % i == 0:
            result += i
            if i != n // i:
                result += n // i
        i += 1
    return result


def eabc_class(p: int) -> str:
    """
    Klassifiziert Primzahl p nach Gauß-Eisenstein.
    
    Returns:
        'E' für p ≡ 1 (mod 12) - Eisenstein-Primzahlen
        'A' für p ≡ 5 (mod 12) - Typ A
        'B' für p ≡ 7 (mod 12) - Typ B
        'C' für p ≡ 11 (mod 12) - Typ C
        'shell' für p ∈ {2, 3} - Schalen-Primzahlen
        'invalid' für p < 2 oder zusammengesetzte Zahlen
    """
    if p == 2 or p == 3:
        return 'shell'
    if p < 2:
        return 'invalid'
    
    # Primzahltest (einfach)
    if p < 4:
        return 'shell' if p in [2, 3] else 'invalid'
    if any(p % i == 0 for i in range(2, int(p**0.5) + 1)):
        return 'invalid'
    
    mod12 = p % 12
    if mod12 == 1:
        return 'E'
    elif mod12 == 5:
        return 'A'
    elif mod12 == 7:
        return 'B'
    elif mod12 == 11:
        return 'C'
    else:
        return 'invalid'


def compute_eabc_vector(n: int) -> np.ndarray:
    """
    Berechnet EABC-Vektor v = (e, a, b, c) für Zahl n.
    
    Zählt Primfaktoren (mit Vielfachheit) p > 3 nach ihrer Restklasse mod 12:
    - e: Anzahl Faktoren ≡ 1 (mod 12)
    - a: Anzahl Faktoren ≡ 5 (mod 12)
    - b: Anzahl Faktoren ≡ 7 (mod 12)
    - c: Anzahl Faktoren ≡ 11 (mod 12)
    
    Args:
        n: Natürliche Zahl ≥ 2
        
    Returns:
        numpy array [e, a, b, c]
    """
    factors = prime_factors_with_multiplicity(n)
    
    e = sum(1 for p in factors if p > 3 and eabc_class(p) == 'E')
    a = sum(1 for p in factors if p > 3 and eabc_class(p) == 'A')
    b = sum(1 for p in factors if p > 3 and eabc_class(p) == 'B')
    c = sum(1 for p in factors if p > 3 and eabc_class(p) == 'C')
    
    return np.array([e, a, b, c], dtype=float)


def compute_H(n: int) -> float:
    """
    Berechnet dimensionslose Konzentrationsmessung H(n).
    
    H(n) = ||v||² / Ω_EABC² 
    
    wobei v = (e, a, b, c) und Ω_EABC = e + a + b + c.
    
    Wertebereich: H ∈ [1/4, 1]
    - H = 1: Maximale Konzentration (alle Faktoren in einer Klasse)
    - H = 1/4: Maximale Gleichverteilung
    
    Äquivalent zu:
    - Simpson-Index (Ökologie)
    - Herfindahl-Hirschman-Index (Ökonomie)
    - Rényi-Entropie Ordnung 2 (Informationstheorie)
    
    Args:
        n: Natürliche Zahl ≥ 2
        
    Returns:
        H(n) ∈ [1/4, 1], oder np.nan falls Ω_EABC = 0
    """
    v = compute_eabc_vector(n)
    norm_sq = np.dot(v, v)  # ||v||²
    omega_eabc = np.sum(v)   # Ω_EABC = e + a + b + c
    
    if omega_eabc == 0:
        # Keine EABC-Faktoren (nur 2, 3)
        return np.nan
    
    H = norm_sq / (omega_eabc ** 2)
    return H


def compute_svn_coordinates(n: int) -> Dict[str, float]:
    """
    Berechnet vollständige SVN-Koordinaten (Smooth-Variety-Number) für Zahl n.
    
    Returns:
        Dictionary mit Schlüsseln:
        - 'omega': Ω(n) - Anzahl Primfaktoren mit Vielfachheit
        - 'sigma': σ(n) - Summe der Teiler
        - 'v2': v₂(n) - 2-adische Bewertung
        - 'v3': v₃(n) - 3-adische Bewertung
        - 'e', 'a', 'b', 'c': EABC-Komponenten
        - 'v_fac': EABC-Vektor als numpy array
        - 'norm_sq': ||v||² - Quadrierte Norm
        - 'H': H(n) - Konzentrationsmessung
        - 'omega_eabc': Ω_EABC = e + a + b + c
    """
    omega = count_prime_factors(n)
    sigma = sum_of_divisors(n)
    v2 = padicval(n, 2)
    v3 = padicval(n, 3)
    
    v_fac = compute_eabc_vector(n)
    norm_sq = np.dot(v_fac, v_fac)
    H = compute_H(n)
    omega_eabc = np.sum(v_fac)
    
    return {
        'omega': omega,
        'sigma': sigma,
        'v2': v2,
        'v3': v3,
        'e': v_fac[0],
        'a': v_fac[1],
        'b': v_fac[2],
        'c': v_fac[3],
        'v_fac': v_fac,
        'norm_sq': norm_sq,
        'H': H,
        'omega_eabc': omega_eabc
    }


# Beispieltest
if __name__ == "__main__":
    print("EABC-Vektor Tests:")
    print()
    
    test_numbers = [60, 210, 2310, 30030]
    
    for n in test_numbers:
        factors = prime_factors_with_multiplicity(n)
        v = compute_eabc_vector(n)
        H = compute_H(n)
        coords = compute_svn_coordinates(n)
        
        print(f"n = {n}")
        print(f"  Faktoren: {factors}")
        print(f"  EABC-Vektor v = {v}")
        print(f"  ||v||² = {coords['norm_sq']}")
        print(f"  Ω_EABC = {coords['omega_eabc']}")
        print(f"  H(n) = {H:.4f}")
        print(f"  Ω(n) = {coords['omega']}")
        print(f"  (v₂, v₃) = ({coords['v2']}, {coords['v3']})")
        print()
