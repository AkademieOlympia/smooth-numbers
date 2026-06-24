"""
Collatz-Dynamik-Gewichte für EABC-Klassifikation

Dieses Modul implementiert die lokalen Expansions-/Kontraktionsraten log(r)
für die Collatz-Dynamik basierend auf der EABC-Klassifikation (n mod 12).

Basierend auf "Conditional Collatz via G2 Log-Drift Axiom" (Paper C):
- B und C: Expander (log r > 0)
- E und A: Kontraktoren (log r < 0)

Die log-Raten quantifizieren die lokale Kontraktions-/Expansionsdynamik
der Collatz-Abbildung in Abhängigkeit von der Restklasse mod 12.
"""

import numpy as np
from typing import Dict, List
from .primes import eabc_classification, eabc_index


def collatz_log_rate(n: int) -> float:
    """
    Berechne die theoretische log-Kontraktionsrate log(r) für Zahl n.
    
    Die Collatz-Dynamik definiert lokale Raten basierend auf EABC-Klasse:
    
    - E (n ≡ 1  mod 12): Kontraktor, log r = -log(2)       ≈ -0.693
    - A (n ≡ 5  mod 12): Kontraktor, log r = -log(2/3)     ≈ -0.405
    - B (n ≡ 7  mod 12): Expander,   log r = +log(2)       ≈ +0.693
    - C (n ≡ 11 mod 12): Expander,   log r = +log(3/2)     ≈ +0.405
    
    Diese Raten spiegeln die durchschnittliche Wachstums-/Schrumpfungsrate
    der Collatz-Trajektorie wider, wenn sie durch die jeweilige Restklasse läuft.
    
    Parameters
    ----------
    n : int
        Natürliche Zahl (typischerweise Primzahl)
    
    Returns
    -------
    float
        log(r): Negativ für Kontraktion, positiv für Expansion
    
    References
    ----------
    Paper C: "Conditional Collatz via G2 Log-Drift Axiom"
    
    Examples
    --------
    >>> collatz_log_rate(13)  # E: Kontraktor
    -0.6931471805599453
    >>> collatz_log_rate(7)   # B: Expander
    0.6931471805599453
    """
    # EABC-Klassifikation bestimmen
    if n == 2:
        cls = 'E'
    elif n == 3:
        cls = 'A'
    else:
        r = n % 12
        cls_map = {1: 'E', 5: 'A', 7: 'B', 11: 'C'}
        cls = cls_map.get(r, 'E')  # Fallback zu E
    
    # log(r)-Raten nach Paper C
    log_rates = {
        'E': -np.log(2),        # ≈ -0.693 (starker Kontraktor)
        'A': -np.log(2) + np.log(3)/2,  # ≈ -0.143 (schwacher Kontraktor)
        'B': +np.log(2),        # ≈ +0.693 (starker Expander)
        'C': +np.log(3) - np.log(2)     # ≈ +0.405 (mittlerer Expander)
    }
    
    return log_rates[cls]


def collatz_log_rate_prime(p: int) -> float:
    """
    Spezialisierte Funktion für Primzahlen (nutzt eabc_classification).
    
    Parameters
    ----------
    p : int
        Primzahl
    
    Returns
    -------
    float
        log(r) für diese Primzahl
    """
    cls = eabc_classification(p)
    
    log_rates = {
        'E': -np.log(2),
        'A': -np.log(2) + np.log(3)/2,
        'B': +np.log(2),
        'C': +np.log(3) - np.log(2)
    }
    
    return log_rates[cls]


def collatz_weights_array(n_max: int, primes: List[int]) -> np.ndarray:
    """
    Erstelle ein Array von Collatz-Gewichten für alle Primzahlen bis n_max.
    
    Parameters
    ----------
    n_max : int
        Maximale Gittergröße
    primes : List[int]
        Liste von Primzahlen
    
    Returns
    -------
    np.ndarray
        Array der Länge len(primes) mit log(r)-Werten
    """
    return np.array([collatz_log_rate_prime(p) for p in primes])


def random_soup_weights(n_primes: int, seed: int = 42) -> np.ndarray:
    """
    Erzeuge zufällig permutierte Collatz-Gewichte als Kontroll-Experiment.
    
    Diese Funktion erzeugt dieselbe Verteilung von Gewichten wie die echten
    Collatz-Raten, aber permutiert sie zufällig. Dies dient als Falsifikations-Test:
    Wenn die physikalisch motivierten Collatz-Gewichte keine besseren Eigenschaften
    zeigen als eine zufällige Permutation, ist die Theorie nicht haltbar.
    
    Parameters
    ----------
    n_primes : int
        Anzahl der Primzahlen (und damit der Gewichte)
    seed : int, optional
        Random seed für Reproduzierbarkeit, default: 42
    
    Returns
    -------
    np.ndarray
        Permutiertes Array von log(r)-Werten
    """
    # Echte EABC-Verteilung approximieren (gleichverteilt über E, A, B, C)
    rng = np.random.RandomState(seed)
    
    # Vier Basisgewichte (E, A, B, C)
    base_weights = [
        -np.log(2),                    # E
        -np.log(2) + np.log(3)/2,      # A
        +np.log(2),                    # B
        +np.log(3) - np.log(2)         # C
    ]
    
    # Gleichverteilt über die Klassen samplen
    weights = rng.choice(base_weights, size=n_primes)
    
    # Zufällig permutieren
    rng.shuffle(weights)
    
    return weights


def analyze_collatz_distribution(n_max: int, primes: List[int]) -> Dict[str, Dict]:
    """
    Analysiere die Verteilung der Collatz-Gewichte für gegebene Primzahlen.
    
    Parameters
    ----------
    n_max : int
        Gittergröße
    primes : List[int]
        Liste von Primzahlen
    
    Returns
    -------
    Dict[str, Dict]
        Statistiken für jede EABC-Klasse:
        - count: Anzahl der Primzahlen
        - log_rate: Zugeordneter log(r)-Wert
        - contribution: Gesamt-Beitrag zum Hamiltonian
    """
    stats = {
        'E': {'count': 0, 'log_rate': -np.log(2), 'contribution': 0.0},
        'A': {'count': 0, 'log_rate': -np.log(2) + np.log(3)/2, 'contribution': 0.0},
        'B': {'count': 0, 'log_rate': +np.log(2), 'contribution': 0.0},
        'C': {'count': 0, 'log_rate': +np.log(3) - np.log(2), 'contribution': 0.0}
    }
    
    for p in primes:
        cls = eabc_classification(p)
        stats[cls]['count'] += 1
        stats[cls]['contribution'] += stats[cls]['log_rate']
    
    return stats


def visualize_collatz_rates():
    """
    Erzeuge eine einfache Visualisierung der Collatz-Raten.
    
    Gibt eine formattierte Tabelle mit den vier EABC-Klassen und ihren
    zugeordneten log(r)-Werten aus.
    """
    print("="*60)
    print("Collatz log(r)-Raten nach EABC-Klassifikation")
    print("="*60)
    print(f"{'Klasse':<10} {'n mod 12':<12} {'log(r)':<15} {'Typ':<20}")
    print("-"*60)
    
    rates = [
        ('E', '≡ 1', -np.log(2), 'Starker Kontraktor'),
        ('A', '≡ 5', -np.log(2) + np.log(3)/2, 'Schwacher Kontraktor'),
        ('B', '≡ 7', +np.log(2), 'Starker Expander'),
        ('C', '≡ 11', +np.log(3) - np.log(2), 'Mittlerer Expander')
    ]
    
    for cls, mod, rate, typ in rates:
        print(f"{cls:<10} {mod:<12} {rate:+.6f}     {typ:<20}")
    
    print("="*60)
    print("\nInterpretation:")
    print("  • log(r) < 0: Kontraktoren (Collatz-Trajektorie schrumpft)")
    print("  • log(r) > 0: Expander (Collatz-Trajektorie wächst)")
    print("  • G2-Axiom: Globaler Drift ≈ 0 (bedingte Konvergenz)")
    print("="*60)


if __name__ == "__main__":
    # Demonstration
    print("\n=== Collatz-Gewichte für EABC-Qubit ===\n")
    
    # Visualisiere die theoretischen Raten
    visualize_collatz_rates()
    
    # Test: Berechne Gewichte für erste Primzahlen
    from .primes import generate_primes
    
    print("\n\nBeispiele: log(r) für erste 15 Primzahlen:")
    print("-"*50)
    primes = generate_primes(50)[:15]
    
    for p in primes:
        cls = eabc_classification(p)
        log_r = collatz_log_rate_prime(p)
        print(f"p = {p:3d}  →  {cls}  →  log(r) = {log_r:+.4f}")
    
    # Verteilungsanalyse
    print("\n\nCollatz-Gewichtsverteilung bis N = 1000:")
    print("-"*50)
    primes_1000 = generate_primes(1000)
    stats = analyze_collatz_distribution(1000, primes_1000)
    
    for cls in ['E', 'A', 'B', 'C']:
        count = stats[cls]['count']
        rate = stats[cls]['log_rate']
        contrib = stats[cls]['contribution']
        print(f"{cls}: {count:3d} Primzahlen, log(r) = {rate:+.4f}, Σ = {contrib:+.2f}")
    
    # Falsifikations-Test: Random Soup
    print("\n\nFalsifikations-Test: Random Soup Kontrolle")
    print("-"*50)
    soup = random_soup_weights(len(primes_1000), seed=42)
    print(f"Original Mittelwert:  {np.mean(collatz_weights_array(1000, primes_1000)):+.6f}")
    print(f"Random Soup Mittel:   {np.mean(soup):+.6f}")
    print(f"Original Std.-Abw.:   {np.std(collatz_weights_array(1000, primes_1000)):.6f}")
    print(f"Random Soup Std.-Abw: {np.std(soup):.6f}")
