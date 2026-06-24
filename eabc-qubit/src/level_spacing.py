"""
Level Spacing Distribution (LSD)

Analyse der Nearest-Neighbor-Abstände im entfalteten Spektrum.
Dies ist die zentrale Größe zur Unterscheidung zwischen Poisson-Statistik
(integrable Systeme) und Wigner-Dyson-Statistik (Quantenchaos).
"""

import numpy as np
from scipy.optimize import curve_fit
from scipy.stats import chi2
from typing import Tuple, Dict, Optional


def compute_level_spacing(unfolded_spectrum: np.ndarray) -> np.ndarray:
    """
    Berechne Nearest-Neighbor Level Spacings.
    
    s_i = ε_{i+1} - ε_i
    
    Für entfaltetes Spektrum (mittlere Dichte = 1) gilt: ⟨s⟩ = 1
    
    Parameters
    ----------
    unfolded_spectrum : np.ndarray
        Entfaltetes Spektrum (sortiert)
    
    Returns
    -------
    np.ndarray
        Level spacings s_i
    
    Examples
    --------
    >>> eps = np.array([0.0, 1.2, 2.5, 3.1])
    >>> compute_level_spacing(eps)
    array([1.2, 1.3, 0.6])
    """
    spacings = np.diff(unfolded_spectrum)
    
    # Normalisierung (falls ⟨s⟩ ≠ 1 aufgrund numerischer Fehler)
    mean_spacing = np.mean(spacings)
    spacings_normalized = spacings / mean_spacing
    
    return spacings_normalized


def poisson_distribution(s: np.ndarray) -> np.ndarray:
    """
    Poisson-Verteilung: P(s) = exp(-s)
    
    Charakteristisch für integrable Systeme oder zufällige Störungen.
    
    Parameters
    ----------
    s : np.ndarray
        Level spacings
    
    Returns
    -------
    np.ndarray
        P_Poisson(s)
    """
    return np.exp(-s)


def wigner_surmise_GOE(s: np.ndarray) -> np.ndarray:
    """
    Wigner-Surmise für GOE (Gaussian Orthogonal Ensemble).
    
    P(s) = (π/2) s exp(-πs²/4)
    
    GOE: Reelle symmetrische Matrizen (Zeitumkehr-invariant, kein Spin)
    
    Parameters
    ----------
    s : np.ndarray
        Level spacings
    
    Returns
    -------
    np.ndarray
        P_GOE(s)
    """
    return (np.pi / 2) * s * np.exp(-np.pi * s**2 / 4)


def wigner_surmise_GUE(s: np.ndarray) -> np.ndarray:
    """
    Wigner-Surmise für GUE (Gaussian Unitary Ensemble).
    
    P(s) = (32/π²) s² exp(-4s²/π)
    
    GUE: Komplexe hermitische Matrizen (gebrochene Zeitumkehr-Symmetrie)
    
    Parameters
    ----------
    s : np.ndarray
        Level spacings
    
    Returns
    -------
    np.ndarray
        P_GUE(s)
    """
    return (32 / np.pi**2) * s**2 * np.exp(-4 * s**2 / np.pi)


def wigner_surmise_GSE(s: np.ndarray) -> np.ndarray:
    """
    Wigner-Surmise für GSE (Gaussian Symplectic Ensemble).
    
    P(s) ≈ C s⁴ exp(-A s²)  mit passenden Konstanten
    
    GSE: Quaternionische Matrizen (Spin-1/2 mit Zeitumkehr)
    
    Parameters
    ----------
    s : np.ndarray
        Level spacings
    
    Returns
    -------
    np.ndarray
        P_GSE(s)
    """
    # Approximate Wigner-Surmise für GSE
    C = 2**18 / (3**6 * np.pi**3)
    A = 64 / (9 * np.pi)
    return C * s**4 * np.exp(-A * s**2)


def brody_distribution(s: np.ndarray, q: float) -> np.ndarray:
    """
    Brody-Verteilung: Interpoliert zwischen Poisson (q=0) und Wigner-Dyson (q=1).
    
    P(s; q) = α s^q exp(-β s^(q+1))
    
    mit α = (q+1)β, β = [Γ((q+2)/(q+1))]^(q+1)
    
    Parameters
    ----------
    s : np.ndarray
        Level spacings
    q : float
        Brody-Parameter (0 ≤ q ≤ 1)
    
    Returns
    -------
    np.ndarray
        P_Brody(s; q)
    
    References
    ----------
    - Brody (1973): "A statistical measure for the repulsion of energy levels"
    """
    from scipy.special import gamma
    
    beta = gamma((q + 2) / (q + 1)) ** (q + 1)
    alpha = (q + 1) * beta
    
    return alpha * s**q * np.exp(-beta * s**(q + 1))


def fit_level_statistics(
    spacings: np.ndarray,
    bins: int = 50
) -> Dict[str, float]:
    """
    Fitte Level Spacing Distribution gegen theoretische Verteilungen.
    
    Berechnet χ²-Goodness-of-Fit für:
    - Poisson
    - GOE (Wigner-Dyson)
    - GUE (Wigner-Dyson)
    - Brody (mit optimalem q)
    
    Parameters
    ----------
    spacings : np.ndarray
        Level spacings (normalisiert: ⟨s⟩ = 1)
    bins : int, optional
        Anzahl Bins für Histogramm, default: 50
    
    Returns
    -------
    Dict[str, float]
        Chi-Squared Werte für jede Verteilung
    
    Examples
    --------
    >>> spacings = np.random.exponential(1.0, 1000)  # Poisson
    >>> results = fit_level_statistics(spacings)
    >>> results['poisson']  # sollte klein sein
    """
    # Histogramm
    hist, bin_edges = np.histogram(spacings, bins=bins, density=True)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
    
    # Nur Bins mit genug Statistik
    mask = hist > 0
    hist = hist[mask]
    s = bin_centers[mask]
    
    # Theoretische Verteilungen
    p_poisson = poisson_distribution(s)
    p_GOE = wigner_surmise_GOE(s)
    p_GUE = wigner_surmise_GUE(s)
    
    # Chi-Squared
    def chi_squared(observed, expected):
        # Normalisiere erwartete Verteilung
        from scipy.integrate import trapezoid
        expected = expected / trapezoid(expected, s) * trapezoid(observed, s)
        return np.sum((observed - expected)**2 / (expected + 1e-10))
    
    chi2_poisson = chi_squared(hist, p_poisson)
    chi2_GOE = chi_squared(hist, p_GOE)
    chi2_GUE = chi_squared(hist, p_GUE)
    
    # Brody-Fit (optimiere q)
    def brody_fit(s_data, q):
        return brody_distribution(s_data, q)
    
    try:
        popt, _ = curve_fit(brody_fit, s, hist, p0=[0.5], bounds=(0, 1))
        q_optimal = popt[0]
        p_brody = brody_distribution(s, q_optimal)
        chi2_brody = chi_squared(hist, p_brody)
    except:
        q_optimal = np.nan
        chi2_brody = np.inf
    
    return {
        'poisson': chi2_poisson,
        'GOE': chi2_GOE,
        'GUE': chi2_GUE,
        'brody': chi2_brody,
        'brody_q': q_optimal
    }


def cumulative_distribution(spacings: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """
    Berechne kumulative Verteilungsfunktion (CDF).
    
    I(s) = P(s' < s) = ∫₀ˢ P(s') ds'
    
    Parameters
    ----------
    spacings : np.ndarray
        Level spacings (sortiert)
    
    Returns
    -------
    s_sorted : np.ndarray
        Sortierte spacings
    cdf : np.ndarray
        Kumulative Wahrscheinlichkeit
    """
    s_sorted = np.sort(spacings)
    cdf = np.arange(1, len(s_sorted) + 1) / len(s_sorted)
    
    return s_sorted, cdf


def level_repulsion_parameter(spacings: np.ndarray) -> float:
    """
    Berechne Level-Repulsion-Parameter β.
    
    β ≈ ⟨s²⟩ / ⟨s⟩² - 1
    
    β = 0: Poisson (keine Repulsion)
    β = 1: GOE (lineare Repulsion)
    β = 4: GUE (quadratische Repulsion)
    
    Parameters
    ----------
    spacings : np.ndarray
        Level spacings
    
    Returns
    -------
    float
        Repulsion-Parameter β
    """
    mean_s = np.mean(spacings)
    mean_s2 = np.mean(spacings**2)
    
    beta = mean_s2 / mean_s**2 - 1
    
    return beta


def spectral_form_factor(
    eigenvalues: np.ndarray,
    tau_max: float = 10.0,
    n_points: int = 100
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Berechne Spectral Form Factor (SFF).
    
    K(τ) = |⟨Tr[U(τ)]⟩|² / N
    
    mit U(τ) = exp(-iHτ) als Zeitevolutionsoperator.
    
    Für große Systeme:
    - Poisson:  K(τ) = konstant
    - RMT:      K(τ) ∼ τ (linear ramp), dann Plateau
    
    Parameters
    ----------
    eigenvalues : np.ndarray
        Energieeigenwerte
    tau_max : float, optional
        Maximale Zeit, default: 10.0
    n_points : int, optional
        Anzahl Zeitpunkte, default: 100
    
    Returns
    -------
    tau : np.ndarray
        Zeitpunkte
    K : np.ndarray
        Spectral Form Factor
    
    References
    ----------
    - Haake (2010): "Quantum Signatures of Chaos", Chapter 9
    """
    N = len(eigenvalues)
    tau = np.linspace(0, tau_max, n_points)
    K = np.zeros(n_points)
    
    for i, t in enumerate(tau):
        # Summe über alle Paare
        phase_sum = np.sum(np.exp(1j * eigenvalues * t))
        K[i] = np.abs(phase_sum)**2 / N
    
    return tau, K


if __name__ == "__main__":
    # Demonstration
    print("=== Level Spacing Distribution Demo ===\n")
    
    np.random.seed(42)
    
    # Test 1: Poisson-Statistik
    print("TEST 1: Poisson-Verteilung (zufällige Energien)")
    spacings_poisson = np.random.exponential(1.0, 5000)
    results_poisson = fit_level_statistics(spacings_poisson)
    
    print("χ² Werte:")
    for key, val in results_poisson.items():
        if key != 'brody_q':
            print(f"  {key:10s}: {val:.3f}")
    print(f"  Brody q:    {results_poisson['brody_q']:.3f}")
    print(f"  → Beste Fit: {min(results_poisson, key=lambda k: results_poisson[k] if k != 'brody_q' else np.inf)}")
    
    beta = level_repulsion_parameter(spacings_poisson)
    print(f"  Level Repulsion β: {beta:.3f} (erwartet ≈ 0)\n")
    
    # Test 2: GOE-Statistik
    print("TEST 2: GOE-Verteilung (Random Matrix)")
    n = 500
    H = np.random.randn(n, n)
    H = (H + H.T) / 2  # Symmetrisch
    eigenvalues = np.linalg.eigvalsh(H)
    
    # Unfolding (einfach: lineares Rescaling)
    unfolded = (eigenvalues - eigenvalues[0]) / np.mean(np.diff(eigenvalues))
    spacings_GOE = compute_level_spacing(unfolded)
    
    results_GOE = fit_level_statistics(spacings_GOE)
    
    print("χ² Werte:")
    for key, val in results_GOE.items():
        if key != 'brody_q':
            print(f"  {key:10s}: {val:.3f}")
    print(f"  Brody q:    {results_GOE['brody_q']:.3f}")
    print(f"  → Beste Fit: {min(results_GOE, key=lambda k: results_GOE[k] if k != 'brody_q' else np.inf)}")
    
    beta = level_repulsion_parameter(spacings_GOE)
    print(f"  Level Repulsion β: {beta:.3f} (erwartet ≈ 1)")
