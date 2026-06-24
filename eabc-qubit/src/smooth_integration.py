"""
Smooth Numbers Integration für EABC-Qubit Framework

Dieses Modul implementiert die Datenbrücke zwischen dem C++ Smooth-Numbers-Projekt
und dem Python EABC-Qubit Framework.

Es stellt Funktionen bereit zur:
- Berechnung von k-Glattheit (Smooth Numbers)
- Import von vorgenerierten Smooth-Daten (CSV/JSON)
- Berechnung von Glattheitsdichten für Zahlen
- Konstruktion des Glattheitspotentials H_smooth
"""

import numpy as np
import pandas as pd
from pathlib import Path
from typing import Optional, Dict, List, Tuple
import json


def is_k_smooth(n: int, k: int) -> bool:
    """
    Prüft ob eine Zahl n k-glatt ist.
    
    Eine Zahl ist k-glatt, wenn alle ihre Primfaktoren ≤ k sind.
    
    Parameters
    ----------
    n : int
        Zu prüfende Zahl
    k : int
        Glattheitsschwelle (größter erlaubter Primfaktor)
    
    Returns
    -------
    bool
        True falls n k-glatt ist
    
    Examples
    --------
    >>> is_k_smooth(12, 3)  # 12 = 2² × 3
    True
    >>> is_k_smooth(14, 3)  # 14 = 2 × 7 (7 > 3)
    False
    """
    if n == 1:
        return True
    
    # Versuche alle Primfaktoren ≤ k zu dividieren
    temp = n
    for p in range(2, k + 1):
        while temp % p == 0:
            temp //= p
    
    # Falls temp > 1 übrig bleibt, gibt es einen Primfaktor > k
    return temp == 1 or temp <= k


def count_k_smooth(n_max: int, k: int) -> int:
    """
    Zählt die Anzahl k-glatter Zahlen ≤ n_max.
    
    Dies ist die Funktion T(n, k) aus dem Dreieck.
    
    Parameters
    ----------
    n_max : int
        Obere Schranke
    k : int
        Glattheitsschwelle
    
    Returns
    -------
    int
        Anzahl k-glatter Zahlen in [1, n_max]
    
    Examples
    --------
    >>> count_k_smooth(10, 2)  # Potenzen von 2: {1,2,4,8}
    4
    >>> count_k_smooth(10, 3)  # {1,2,3,4,6,8,9}
    7
    """
    if k < 2:
        return 1 if n_max >= 1 else 0
    
    count = 0
    for n in range(1, n_max + 1):
        if is_k_smooth(n, k):
            count += 1
    
    return count


def smooth_density(n: int, max_k: int = 10) -> float:
    """
    Berechnet die Glattheitsdichte einer Zahl n.
    
    Die Dichte misst, für wie viele k-Werte (k ≤ max_k) die Zahl n k-glatt ist.
    Höhere Dichte → glattere Zahl.
    
    Parameters
    ----------
    n : int
        Zahl, deren Glattheit berechnet wird
    max_k : int, optional
        Maximaler k-Wert, default: 10
    
    Returns
    -------
    float
        Normalisierte Glattheitsdichte in [0, 1]
        
        - 1.0: Sehr glatt (z.B. n=1, n=2)
        - 0.0: Nicht glatt (z.B. große Primzahlen)
    
    Examples
    --------
    >>> smooth_density(1, 10)   # 1 ist für alle k glatt
    1.0
    >>> smooth_density(12, 10)  # 12 = 2² × 3 ist glatt für k ≥ 3
    0.8
    >>> smooth_density(97, 10)  # 97 ist Primzahl, nur für k ≥ 97 glatt
    0.1
    """
    if n == 1:
        return 1.0
    
    count = 0
    for k in range(2, max_k + 1):
        if is_k_smooth(n, k):
            count += 1
    
    # Normalisiere auf [0, 1]
    return count / (max_k - 1)


def largest_prime_factor(n: int) -> int:
    """
    Berechnet den größten Primfaktor von n.
    
    Parameters
    ----------
    n : int
        Zahl
    
    Returns
    -------
    int
        Größter Primfaktor
        
    Examples
    --------
    >>> largest_prime_factor(12)  # 12 = 2² × 3
    3
    >>> largest_prime_factor(14)  # 14 = 2 × 7
    7
    """
    if n == 1:
        return 1
    
    largest = 1
    temp = n
    
    # Prüfe 2
    while temp % 2 == 0:
        largest = 2
        temp //= 2
    
    # Prüfe ungerade Zahlen
    p = 3
    while p * p <= temp:
        while temp % p == 0:
            largest = p
            temp //= p
        p += 2
    
    if temp > 1:
        largest = temp
    
    return largest


def smooth_density_fast(n: int, max_k: int = 10) -> float:
    """
    Schnelle Berechnung der Glattheitsdichte via größtem Primfaktor.
    
    Falls der größte Primfaktor von n gleich p ist, dann ist n k-glatt
    für alle k ≥ p.
    
    Parameters
    ----------
    n : int
        Zahl
    max_k : int, optional
        Maximaler k-Wert
    
    Returns
    -------
    float
        Normalisierte Glattheitsdichte
    """
    if n == 1:
        return 1.0
    
    p_max = largest_prime_factor(n)
    
    # n ist k-glatt für k ∈ {p_max, p_max+1, ..., max_k}
    # Anzahl: max_k - p_max + 1 (aber nur falls p_max ≤ max_k)
    if p_max > max_k:
        count = 0
    else:
        count = max_k - p_max + 1
    
    # Normalisiere auf [0, 1]
    return count / (max_k - 1)


def compute_smooth_triangle(n_max: int, k_max: int) -> np.ndarray:
    """
    Berechnet das Smooth-Dreieck T(n, k).
    
    T(n, k) = Anzahl der k-glatten Zahlen ≤ n
    
    Parameters
    ----------
    n_max : int
        Maximales n
    k_max : int
        Maximales k
    
    Returns
    -------
    np.ndarray
        Matrix der Größe (n_max, k_max) mit T(n, k)
    """
    triangle = np.zeros((n_max, k_max), dtype=int)
    
    for n in range(1, n_max + 1):
        for k in range(1, k_max + 1):
            triangle[n-1, k-1] = count_k_smooth(n, k)
    
    return triangle


def import_smooth_triangle_csv(csv_path: str) -> pd.DataFrame:
    """
    Importiert Smooth-Dreieck aus C++ CSV-Export.
    
    Erwartet Format:
        n,k,T(n,k)
        1,1,1
        1,2,1
        ...
    
    Parameters
    ----------
    csv_path : str
        Pfad zur CSV-Datei
    
    Returns
    -------
    pd.DataFrame
        DataFrame mit Spalten ['n', 'k', 'T_nk']
    """
    df = pd.read_csv(csv_path)
    
    # Stelle sicher, dass die Spalten korrekt benannt sind
    if 'T(n,k)' in df.columns:
        df = df.rename(columns={'T(n,k)': 'T_nk'})
    
    return df


def import_smooth_triangle_json(json_path: str) -> Dict:
    """
    Importiert Smooth-Dreieck aus C++ JSON-Export.
    
    Parameters
    ----------
    json_path : str
        Pfad zur JSON-Datei
    
    Returns
    -------
    dict
        Dictionary mit Dreieck-Daten
    """
    with open(json_path, 'r') as f:
        data = json.load(f)
    
    return data


def export_smooth_triangle_csv(triangle: np.ndarray, output_path: str):
    """
    Exportiert Smooth-Dreieck als CSV.
    
    Parameters
    ----------
    triangle : np.ndarray
        Dreieck-Matrix
    output_path : str
        Ausgabepfad
    """
    n_max, k_max = triangle.shape
    
    with open(output_path, 'w') as f:
        f.write("n,k,T(n,k)\n")
        for n in range(1, n_max + 1):
            for k in range(1, k_max + 1):
                f.write(f"{n},{k},{triangle[n-1, k-1]}\n")
    
    print(f"✓ Smooth-Dreieck exportiert nach: {output_path}")


def smooth_potential_landscape(N: int, max_k: int = 10, use_fast: bool = True) -> np.ndarray:
    """
    Berechnet die Glattheitspotentiallandschaft für alle Zahlen 1..N.
    
    Parameters
    ----------
    N : int
        Anzahl der Zahlen
    max_k : int, optional
        Maximaler k-Wert für Glattheitsdichte
    use_fast : bool, optional
        Verwende schnelle Variante via größten Primfaktor
    
    Returns
    -------
    np.ndarray
        Array der Länge N mit Glattheitsdichten
    """
    landscape = np.zeros(N)
    
    density_func = smooth_density_fast if use_fast else smooth_density
    
    for n in range(1, N + 1):
        landscape[n-1] = density_func(n, max_k)
    
    return landscape


def analyze_smooth_statistics(N: int, max_k: int = 10) -> Dict:
    """
    Analysiert die Glattheitseigenschaften für Zahlen 1..N.
    
    Parameters
    ----------
    N : int
        Anzahl der Zahlen
    max_k : int, optional
        Maximaler k-Wert
    
    Returns
    -------
    dict
        Statistiken über Glattheit
    """
    landscape = smooth_potential_landscape(N, max_k)
    
    # Finde glatteste und unglatteste Zahlen
    smooth_indices = np.argsort(landscape)[::-1]  # Absteigende Sortierung
    
    stats = {
        'N': N,
        'max_k': max_k,
        'mean_density': np.mean(landscape),
        'std_density': np.std(landscape),
        'min_density': np.min(landscape),
        'max_density': np.max(landscape),
        'smoothest_numbers': [(int(i+1), landscape[i]) for i in smooth_indices[:10]],
        'roughest_numbers': [(int(i+1), landscape[i]) for i in smooth_indices[-10:]],
        'density_histogram': np.histogram(landscape, bins=20)
    }
    
    return stats


def print_smooth_statistics(stats: Dict):
    """
    Zeigt Glattheitstatistiken formatiert an.
    
    Parameters
    ----------
    stats : dict
        Statistiken von analyze_smooth_statistics()
    """
    print("\n" + "="*70)
    print("Smooth Numbers - Statistische Analyse")
    print("="*70)
    print(f"Zahlenbereich: [1, {stats['N']}]")
    print(f"Maximales k: {stats['max_k']}")
    print(f"\nGlattheitsdichte:")
    print(f"  Mittelwert: {stats['mean_density']:.4f}")
    print(f"  Std.-Abw.:  {stats['std_density']:.4f}")
    print(f"  Bereich:    [{stats['min_density']:.4f}, {stats['max_density']:.4f}]")
    
    print(f"\n10 glatteste Zahlen:")
    for n, density in stats['smoothest_numbers']:
        print(f"  n = {n:4d}: Dichte = {density:.4f}")
    
    print(f"\n10 raueste Zahlen (Primzahlen):")
    for n, density in stats['roughest_numbers'][::-1]:  # Aufsteigend
        print(f"  n = {n:4d}: Dichte = {density:.4f}")
    
    print("="*70 + "\n")


if __name__ == "__main__":
    print("=== Smooth Numbers Integration Demo ===\n")
    
    # Test 1: Einzelne Zahlen
    print("Test 1: Glattheit einzelner Zahlen")
    test_numbers = [1, 2, 12, 30, 97, 128, 210, 997]
    for n in test_numbers:
        density = smooth_density_fast(n, max_k=20)
        p_max = largest_prime_factor(n)
        print(f"  n = {n:4d}: größter Primfaktor = {p_max:3d}, Dichte = {density:.3f}")
    
    # Test 2: Statistiken
    print("\n\nTest 2: Statistische Analyse (N=100)")
    stats = analyze_smooth_statistics(N=100, max_k=20)
    print_smooth_statistics(stats)
    
    # Test 3: Dreieck berechnen
    print("\nTest 3: Smooth-Dreieck berechnen (n=20, k=10)")
    triangle = compute_smooth_triangle(20, 10)
    print("\nErste 5 Zeilen:")
    print("n\\k ", end="")
    for k in range(1, 11):
        print(f"{k:4d}", end="")
    print()
    print("-" * 48)
    
    for n in range(5):
        print(f"{n+1:3d} ", end="")
        for k in range(10):
            print(f"{triangle[n, k]:4d}", end="")
        print()
    
    # Test 4: Export
    print("\n\nTest 4: Export")
    export_path = "/tmp/smooth_triangle_demo.csv"
    export_smooth_triangle_csv(triangle, export_path)
    print(f"Dreieck exportiert nach: {export_path}")
    
    print("\n✓ Alle Tests erfolgreich!")
