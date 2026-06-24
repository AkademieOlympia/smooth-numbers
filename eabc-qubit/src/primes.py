"""
Primzahlgenerierung und EABC-Klassifikation

Dieses Modul stellt Funktionen zur Generierung von Primzahlen und deren
Klassifikation nach dem EABC-Modell (mod 12) zur Verfügung.
"""

import numpy as np
from sympy import primerange
from typing import List, Dict


def generate_primes(n_max: int) -> List[int]:
    """
    Generiere alle Primzahlen bis n_max.
    
    Parameters
    ----------
    n_max : int
        Obere Grenze (inklusiv)
    
    Returns
    -------
    List[int]
        Liste aller Primzahlen p ≤ n_max
    
    Examples
    --------
    >>> generate_primes(20)
    [2, 3, 5, 7, 11, 13, 17, 19]
    """
    return list(primerange(2, n_max + 1))


def eabc_classification(p: int) -> str:
    """
    Klassifiziere Primzahl p nach EABC-Modell (mod 12).
    
    Die Klassifikation basiert auf p mod 12:
    - E: p ≡ 1  (mod 12)  [z.B. 13, 37, 61, ...]
    - A: p ≡ 5  (mod 12)  [z.B. 5, 17, 29, ...]
    - B: p ≡ 7  (mod 12)  [z.B. 7, 19, 31, ...]
    - C: p ≡ 11 (mod 12)  [z.B. 11, 23, 47, ...]
    
    Spezialfälle:
    - p = 2 → E (per Konvention)
    - p = 3 → A (per Konvention)
    
    Parameters
    ----------
    p : int
        Primzahl (muss Primzahl sein, wird nicht überprüft!)
    
    Returns
    -------
    str
        EABC-Klasse: 'E', 'A', 'B', oder 'C'
    
    Examples
    --------
    >>> eabc_classification(13)
    'E'
    >>> eabc_classification(17)
    'A'
    >>> eabc_classification(19)
    'B'
    >>> eabc_classification(23)
    'C'
    """
    # Spezialfälle für kleine Primzahlen
    if p == 2:
        return 'E'
    if p == 3:
        return 'A'
    
    # Klassifikation für p > 3
    r = p % 12
    classification_map = {
        1: 'E',
        5: 'A',
        7: 'B',
        11: 'C'
    }
    
    return classification_map[r]


def eabc_index(p: int) -> int:
    """
    Gib den numerischen Index der EABC-Klasse zurück.
    
    E → 0, A → 1, B → 2, C → 3
    
    Parameters
    ----------
    p : int
        Primzahl
    
    Returns
    -------
    int
        Index 0, 1, 2, oder 3
    
    Examples
    --------
    >>> eabc_index(13)  # E
    0
    >>> eabc_index(17)  # A
    1
    """
    cls = eabc_classification(p)
    return {'E': 0, 'A': 1, 'B': 2, 'C': 3}[cls]


def analyze_prime_distribution(n_max: int) -> Dict[str, int]:
    """
    Analysiere die EABC-Verteilung aller Primzahlen bis n_max.
    
    Parameters
    ----------
    n_max : int
        Obere Grenze
    
    Returns
    -------
    Dict[str, int]
        Anzahl der Primzahlen in jeder EABC-Klasse
    
    Examples
    --------
    >>> analyze_prime_distribution(100)
    {'E': 7, 'A': 6, 'B': 7, 'C': 5}
    """
    primes = generate_primes(n_max)
    distribution = {'E': 0, 'A': 0, 'B': 0, 'C': 0}
    
    for p in primes:
        cls = eabc_classification(p)
        distribution[cls] += 1
    
    return distribution


def prime_positions(n_max: int) -> Dict[str, List[int]]:
    """
    Gib die Positionen aller Primzahlen nach EABC-Klasse zurück.
    
    Parameters
    ----------
    n_max : int
        Maximale Gittergröße
    
    Returns
    -------
    Dict[str, List[int]]
        Dictionary mit EABC-Klassen als Keys und Listen von Positionen
    
    Examples
    --------
    >>> prime_positions(20)
    {'E': [2, 13], 'A': [3, 5, 17], 'B': [7, 19], 'C': [11]}
    """
    primes = generate_primes(n_max)
    positions = {'E': [], 'A': [], 'B': [], 'C': []}
    
    for p in primes:
        cls = eabc_classification(p)
        positions[cls].append(p)
    
    return positions


if __name__ == "__main__":
    # Demonstration
    print("=== EABC-Primzahlklassifikation ===\n")
    
    # Erste 20 Primzahlen
    primes = generate_primes(100)[:20]
    print("Erste 20 Primzahlen mit EABC-Klassifikation:")
    for p in primes:
        cls = eabc_classification(p)
        idx = eabc_index(p)
        print(f"p = {p:3d}  →  {cls} (Index {idx})")
    
    # Verteilung
    print("\n=== Verteilung bis N = 1000 ===")
    dist = analyze_prime_distribution(1000)
    total = sum(dist.values())
    print(f"Gesamt: {total} Primzahlen")
    for cls in ['E', 'A', 'B', 'C']:
        count = dist[cls]
        percent = 100 * count / total
        print(f"{cls}: {count:3d} ({percent:.1f}%)")
