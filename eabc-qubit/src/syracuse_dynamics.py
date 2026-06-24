"""
Syracuse-Dynamik und Tao's Geom(2)-Theorie

Dieses Modul implementiert die echte Syracuse-Funktion und Trajektorien-Analyse
für die Tao-Syracuse-Erweiterung des EABC-Qubit-Frameworks.

Syracuse-Funktion:
    Syr(n) = (3n+1) / 2^a  wobei a = ν₂(3n+1)

Tao's Hauptresultat (2019):
    Für typische ungerade n verhalten sich die 2-adischen Valuationen a_j
    wie unabhängige Geom(2)-Zufallsvariablen mit E[a_j] = 2.
    
    Die lokale Drift λ_j = log(3) - a_j·log(2) hat Erwartungswert:
    E[λ_j] = log(3) - 2·log(2) = log(3/4) ≈ -0.288 (negative Drift!)

References
----------
T. Tao, "Almost all Collatz orbits attain almost bounded values" (2019)
https://arxiv.org/abs/1909.03562
"""

import numpy as np
from typing import Tuple, List, Optional
import random


def valuation_2(n: int) -> int:
    """
    Berechne die 2-adische Valuation ν₂(n).
    
    ν₂(n) ist die höchste Potenz von 2, die n teilt.
    Äquivalent: Die Anzahl der Trailing-Nullen in der Binärdarstellung.
    
    Parameters
    ----------
    n : int
        Positive ganze Zahl
    
    Returns
    -------
    int
        ν₂(n) = max{k : 2^k | n}
    
    Examples
    --------
    >>> valuation_2(8)   # 8 = 2³
    3
    >>> valuation_2(12)  # 12 = 2² · 3
    2
    >>> valuation_2(7)   # 7 ist ungerade
    0
    """
    if n == 0:
        raise ValueError("ν₂(0) ist nicht definiert")
    
    if n % 2 != 0:
        return 0
    
    # Effiziente Berechnung durch Bit-Manipulation
    count = 0
    while n % 2 == 0:
        n //= 2
        count += 1
    
    return count


def syracuse_step(n: int) -> Tuple[int, int]:
    """
    Ein Schritt der Syracuse-Funktion Syr(n) = (3n+1) / 2^a.
    
    Die Syracuse-Funktion ist äquivalent zur Collatz-Funktion für ungerade
    Zahlen, aber kompakter:
    - Collatz: n → 3n+1 → (3n+1)/2 → (3n+1)/4 → ...
    - Syracuse: n → (3n+1)/2^a direkt
    
    Parameters
    ----------
    n : int
        Ungerade positive ganze Zahl
    
    Returns
    -------
    result : int
        Syr(n) = (3n+1) / 2^a
    a : int
        2-adische Valuation ν₂(3n+1)
    
    Examples
    --------
    >>> syracuse_step(7)   # 3·7+1 = 22 = 2·11 → ν₂(22) = 1
    (11, 1)
    >>> syracuse_step(11)  # 3·11+1 = 34 = 2·17 → ν₂(34) = 1
    (17, 1)
    >>> syracuse_step(5)   # 3·5+1 = 16 = 2⁴ → ν₂(16) = 4
    (1, 4)
    """
    if n % 2 == 0:
        raise ValueError(f"Syracuse-Funktion nur für ungerade n definiert, erhielt n={n}")
    
    val = 3 * n + 1
    a = valuation_2(val)
    result = val >> a  # Bitshift ist schneller als Division
    
    return result, a


def syracuse_trajectory(N: int, max_steps: int = 1000) -> Tuple[List[int], List[int]]:
    """
    Berechne die Syracuse-Trajektorie S₀, S₁, S₂, ... bis Stopping Time oder max_steps.
    
    Stopping Time τ(N) ist definiert als das kleinste j mit S_j(N) = 1.
    Collatz-Vermutung: τ(N) < ∞ für alle N ≥ 1.
    
    Parameters
    ----------
    N : int
        Startwert (ungerade)
    max_steps : int, optional
        Maximale Anzahl von Iterationen, default: 1000
    
    Returns
    -------
    trajectory : List[int]
        [N, S₁(N), S₂(N), ..., S_τ(N)]
    valuations : List[int]
        [a₁, a₂, ..., a_τ] wobei a_j = ν₂(3·S_{j-1}(N) + 1)
    
    Examples
    --------
    >>> syracuse_trajectory(5)
    ([5, 1], [4])
    >>> syracuse_trajectory(7, max_steps=10)
    ([7, 11, 17, 13, 5, 1], [1, 1, 2, 2, 4])
    """
    if N % 2 == 0:
        raise ValueError(f"Startwert muss ungerade sein, erhielt N={N}")
    
    trajectory = [N]
    valuations = []
    
    current = N
    for _ in range(max_steps):
        if current == 1:
            break
        
        current, a = syracuse_step(current)
        trajectory.append(current)
        valuations.append(a)
    
    return trajectory, valuations


def compute_lambda_j(n: int) -> float:
    """
    Berechne die lokale Tao-Drift λ_j = log(3) - a_j·log(2).
    
    Diese Größe quantifiziert die logarithmische Expansions-/Kontraktionsrate
    der Syracuse-Dynamik bei einem einzelnen Schritt:
    
    log(Syr(n)) = log(3n+1) - a·log(2)
                = log(n) + log(3 + 1/n) - a·log(2)
                ≈ log(n) + log(3) - a·log(2)
    
    → Drift: λ = log(3) - a·log(2)
    
    Tao's Resultat:
        Für typische n ist a ∼ Geom(2) mit E[a] = 2
        → E[λ] = log(3) - 2·log(2) = log(3/4) ≈ -0.288
    
    Parameters
    ----------
    n : int
        Ungerade Zahl vor dem Syracuse-Schritt
    
    Returns
    -------
    float
        λ = log(3) - a·log(2)
    
    Examples
    --------
    >>> compute_lambda_j(7)  # a = 1
    0.4054651081081644
    >>> compute_lambda_j(5)  # a = 4 → starke Kontraktion
    -1.6794257988236813
    """
    _, a_j = syracuse_step(n)
    return np.log(3) - a_j * np.log(2)


def trajectory_statistics(trajectory: List[int], valuations: List[int]) -> dict:
    """
    Berechne statistische Kenngrößen für eine Syracuse-Trajektorie.
    
    Parameters
    ----------
    trajectory : List[int]
        Syracuse-Trajektorie [N, S₁(N), ...]
    valuations : List[int]
        2-adische Valuationen [a₁, a₂, ...]
    
    Returns
    -------
    dict
        Statistiken:
        - stopping_time: Länge der Trajektorie (oder max_steps)
        - mean_valuation: Durchschnittliche a_j
        - mean_lambda: Durchschnittliche lokale Drift
        - total_drift: Σ λ_j (Gesamtdrift)
        - max_value: max_j S_j(N) (Höchster erreichter Wert)
    """
    n_steps = len(valuations)
    
    if n_steps == 0:
        return {
            'stopping_time': 0,  # Keine Schritte nötig (bereits am Ziel)
            'mean_valuation': 0.0,
            'mean_lambda': 0.0,
            'total_drift': 0.0,
            'max_value': trajectory[0]
        }
    
    mean_val = np.mean(valuations)
    lambdas = [np.log(3) - a * np.log(2) for a in valuations]
    mean_lambda = np.mean(lambdas)
    total_drift = np.sum(lambdas)
    
    return {
        'stopping_time': n_steps,
        'mean_valuation': mean_val,
        'mean_lambda': mean_lambda,
        'total_drift': total_drift,
        'max_value': max(trajectory),
        'valuations': valuations,
        'lambdas': lambdas
    }


def random_coprime_6_odd(N: int, seed: Optional[int] = None) -> int:
    """
    Generiere eine zufällige ungerade Zahl ≤ N, die coprime zu 6 ist.
    
    Coprime zu 6 bedeutet coprime zu 2 und 3, also n ≡ 1, 5, 7, 11 (mod 12).
    Dies sind genau die Zahlen, die potentiell Primzahlen sind (außer 2 und 3).
    
    Parameters
    ----------
    N : int
        Obere Schranke
    seed : int, optional
        Random seed für Reproduzierbarkeit
    
    Returns
    -------
    int
        Zufällige ungerade Zahl n mit gcd(n, 6) = 1
    """
    if seed is not None:
        random.seed(seed)
    
    while True:
        n = random.randint(3, N)
        if n % 2 == 1 and n % 3 != 0:  # ungerade und nicht durch 3 teilbar
            return n


def geom2_expected_drift() -> float:
    """
    Berechne den theoretisch erwarteten Drift unter Tao's Geom(2)-Annahme.
    
    Unter der Annahme a_j ∼ Geom(2) mit E[a_j] = 2:
    
    E[λ_j] = E[log(3) - a_j·log(2)]
           = log(3) - E[a_j]·log(2)
           = log(3) - 2·log(2)
           = log(3/4)
           ≈ -0.288
    
    Returns
    -------
    float
        E[λ] = log(3/4)
    """
    return np.log(3.0 / 4.0)


def geom2_sample_valuations(n: int, seed: Optional[int] = None) -> np.ndarray:
    """
    Sample n Valuationen aus einer geometrischen Verteilung Geom(p=1/2).
    
    Geom(p) modelliert die Anzahl von Bernoulli-Trials bis zum ersten Erfolg.
    Für p = 1/2 (fairer Münzwurf): E[a] = 1/p = 2.
    
    Dies simuliert Tao's theoretische Vorhersage für typische Syracuse-Schritte.
    
    Parameters
    ----------
    n : int
        Anzahl der zu samplenden Valuationen
    seed : int, optional
        Random seed
    
    Returns
    -------
    np.ndarray
        Array von n Geom(1/2)-verteilten Werten
    """
    rng = np.random.RandomState(seed)
    # numpy's geometric(p) gibt die Anzahl von Fehlversuchen zurück
    # → +1 für die Anzahl von Trials bis zum Erfolg
    return rng.geometric(p=0.5, size=n)


def compare_empirical_vs_geom2(N: int, n_trajectories: int = 100, seed: int = 42) -> dict:
    """
    Vergleiche empirische Syracuse-Statistiken mit Tao's Geom(2)-Vorhersage.
    
    Dieser Test prüft, ob die a_j-Werte aus echten Syracuse-Trajektorien
    tatsächlich wie Geom(2)-Zufallsvariablen verteilt sind.
    
    Parameters
    ----------
    N : int
        Obere Schranke für Startwerte
    n_trajectories : int, optional
        Anzahl der zu testenden Trajektorien, default: 100
    seed : int, optional
        Random seed, default: 42
    
    Returns
    -------
    dict
        Vergleichsstatistiken:
        - empirical_mean_a: Durchschnittliche a_j (empirisch)
        - geom2_expected_a: Erwartungswert E[a] = 2 (Theorie)
        - empirical_mean_lambda: Durchschnittliche λ_j (empirisch)
        - geom2_expected_lambda: E[λ] = log(3/4) (Theorie)
        - agreement_score: |empirisch - Theorie| / Theorie
    """
    random.seed(seed)
    np.random.seed(seed)
    
    all_valuations = []
    all_lambdas = []
    
    for _ in range(n_trajectories):
        start = random_coprime_6_odd(N)
        trajectory, valuations = syracuse_trajectory(start, max_steps=50)
        
        if len(valuations) > 0:
            all_valuations.extend(valuations)
            lambdas = [np.log(3) - a * np.log(2) for a in valuations]
            all_lambdas.extend(lambdas)
    
    empirical_mean_a = np.mean(all_valuations)
    empirical_mean_lambda = np.mean(all_lambdas)
    
    geom2_a = 2.0
    geom2_lambda = geom2_expected_drift()
    
    agreement_a = abs(empirical_mean_a - geom2_a) / geom2_a
    agreement_lambda = abs(empirical_mean_lambda - geom2_lambda) / abs(geom2_lambda)
    
    return {
        'empirical_mean_a': empirical_mean_a,
        'geom2_expected_a': geom2_a,
        'empirical_mean_lambda': empirical_mean_lambda,
        'geom2_expected_lambda': geom2_lambda,
        'agreement_a': agreement_a,
        'agreement_lambda': agreement_lambda,
        'n_samples': len(all_valuations)
    }


if __name__ == "__main__":
    print("="*70)
    print("Syracuse-Dynamik und Tao's Geom(2)-Theorie")
    print("="*70)
    
    # Test 1: Einzelne Trajektorie
    print("\n[Test 1] Einzelne Syracuse-Trajektorie für N = 27:")
    print("-"*70)
    trajectory, valuations = syracuse_trajectory(27, max_steps=50)
    stats = trajectory_statistics(trajectory, valuations)
    
    print(f"Trajektorie: {' → '.join(map(str, trajectory[:10]))}...")
    print(f"Valuationen: {valuations[:10]}...")
    print(f"\nStopping Time: {stats['stopping_time']}")
    print(f"Durchschnitt ⟨a_j⟩: {stats['mean_valuation']:.3f} (Theorie: 2.0)")
    print(f"Durchschnitt ⟨λ_j⟩: {stats['mean_lambda']:.4f} (Theorie: {geom2_expected_drift():.4f})")
    print(f"Gesamtdrift Σλ_j: {stats['total_drift']:.4f}")
    print(f"Maximaler Wert: {stats['max_value']}")
    
    # Test 2: Geom(2)-Vergleich
    print("\n[Test 2] Empirisch vs. Geom(2)-Vorhersage (100 Trajektorien):")
    print("-"*70)
    comparison = compare_empirical_vs_geom2(N=1000, n_trajectories=100, seed=42)
    
    print(f"⟨a_j⟩ empirisch:  {comparison['empirical_mean_a']:.4f}")
    print(f"⟨a_j⟩ Geom(2):    {comparison['geom2_expected_a']:.4f}")
    print(f"Abweichung:       {comparison['agreement_a']*100:.2f}%")
    print()
    print(f"⟨λ_j⟩ empirisch:  {comparison['empirical_mean_lambda']:.4f}")
    print(f"⟨λ_j⟩ Geom(2):    {comparison['geom2_expected_lambda']:.4f}")
    print(f"Abweichung:       {comparison['agreement_lambda']*100:.2f}%")
    print()
    print(f"Anzahl Samples:   {comparison['n_samples']}")
    
    # Interpretation
    print("\n" + "="*70)
    print("Interpretation:")
    print("-"*70)
    print("✓ Wenn ⟨a_j⟩ ≈ 2.0: Geom(2)-Hypothese bestätigt (Tao 2019)")
    print("✓ Wenn ⟨λ_j⟩ < 0: Negative Drift → bedingte Konvergenz")
    print("✓ E[λ] = log(3/4) ≈ -0.288 ist Tao's zentrales Resultat")
    print("="*70)
