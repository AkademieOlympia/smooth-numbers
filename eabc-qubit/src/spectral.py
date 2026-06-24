"""
Spektralanalyse und Unfolding

Dieses Modul implementiert Methoden zur Analyse des Energiespektrums,
insbesondere das spektrale Unfolding zur Normalisierung der lokalen
Zustandsdichte.
"""

import numpy as np
from scipy.interpolate import UnivariateSpline
from scipy.integrate import cumulative_trapezoid
from typing import Tuple, Optional


def compute_spectrum(H, k: int = 500, which: str = 'SM') -> np.ndarray:
    """
    Wrapper für Spektrumsberechnung.
    
    Parameters
    ----------
    H : EABCHamiltonian oder scipy.sparse Matrix
        Hamiltonoperator
    k : int
        Anzahl Eigenwerte
    which : str
        Welche Eigenwerte ('SM', 'LM', 'SA', 'LA')
    
    Returns
    -------
    np.ndarray
        Sortierte Eigenwerte
    """
    if hasattr(H, 'compute_spectrum'):
        return H.compute_spectrum(k=k, which=which, return_eigenvectors=False)
    else:
        from scipy.sparse.linalg import eigsh
        eigenvalues = eigsh(H, k=k, which=which, return_eigenvectors=False)
        return np.sort(eigenvalues)


def spectral_unfolding(
    eigenvalues: np.ndarray,
    smoothing: float = 0.01,
    method: str = 'polynomial'
) -> np.ndarray:
    """
    Spektrales Unfolding: Transformiere Eigenwerte auf einheitliche mittlere Dichte.
    
    Das Unfolding entfernt glatte Trends in der Zustandsdichte ρ(E) und
    transformiert das Spektrum so, dass die mittlere Level-Spacing konstant ist.
    
    Methode:
    1. Berechne die kumulative Zustandsdichte N(E) (Staircase Function)
    2. Fitte N(E) mit einem glatten Polynom oder Spline
    3. Transformiere: ε_i = N_smooth(E_i)
    
    Das resultierende "entfaltete" Spektrum {ε_i} hat mittlere Dichte ρ̄ = 1.
    
    Parameters
    ----------
    eigenvalues : np.ndarray
        Ursprüngliches Spektrum (sortiert)
    smoothing : float, optional
        Glättungsparameter (nur für Spline-Methode), default: 0.01
    method : str, optional
        Unfolding-Methode: 'polynomial' oder 'spline', default: 'polynomial'
    
    Returns
    -------
    np.ndarray
        Entfaltetes Spektrum ε_i
    
    Notes
    -----
    Nach dem Unfolding gilt:
    - Mittlerer Spacing: ⟨s⟩ = 1
    - Lokale Dichte: ρ(ε) ≈ 1
    
    References
    ----------
    - Mehta (2004): "Random Matrices", Chapter 1
    - Haake (2010): "Quantum Signatures of Chaos", Section 2.3
    """
    n = len(eigenvalues)
    E = eigenvalues
    
    # Kumulative Zustandsdichte (Staircase Function)
    # N(E_i) = i (Anzahl der Eigenwerte ≤ E_i)
    staircase = np.arange(1, n + 1, dtype=float)
    
    if method == 'polynomial':
        # Fit mit Polynom (Grad 5-7 typisch)
        degree = min(7, n // 10)  # Adaptiv
        coeffs = np.polyfit(E, staircase, deg=degree)
        N_smooth = np.polyval(coeffs, E)
        
    elif method == 'spline':
        # Fit mit Spline (glatter)
        # Smoothing-Parameter s kontrolliert Glattheit
        s_param = smoothing * n
        spline = UnivariateSpline(E, staircase, s=s_param, k=3)
        N_smooth = spline(E)
        
    else:
        raise ValueError(f"Unbekannte Methode: {method}")
    
    # Entfaltetes Spektrum
    unfolded = N_smooth
    
    return unfolded


def local_density(
    eigenvalues: np.ndarray,
    window_size: Optional[int] = None
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Berechne die lokale Zustandsdichte ρ(E) mittels gleitendem Fenster.
    
    ρ(E_i) ≈ (Anzahl Zustände im Fenster) / (Fensterbreite)
    
    Parameters
    ----------
    eigenvalues : np.ndarray
        Sortiertes Spektrum
    window_size : int, optional
        Fenstergröße (Anzahl Eigenwerte), default: √n
    
    Returns
    -------
    E_centers : np.ndarray
        Zentren der Fenster
    rho : np.ndarray
        Lokale Dichte an jedem Zentrum
    """
    n = len(eigenvalues)
    
    if window_size is None:
        window_size = max(10, int(np.sqrt(n)))
    
    # Anzahl der Fenster
    n_windows = n - window_size + 1
    
    E_centers = np.zeros(n_windows)
    rho = np.zeros(n_windows)
    
    for i in range(n_windows):
        window = eigenvalues[i:i + window_size]
        E_centers[i] = np.mean(window)
        
        # Dichte = N / ΔE
        delta_E = window[-1] - window[0]
        if delta_E > 0:
            rho[i] = window_size / delta_E
        else:
            rho[i] = np.nan
    
    return E_centers, rho


def spectral_rigidity(
    unfolded_spectrum: np.ndarray,
    L_max: int = 100
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Berechne die spektrale Rigidität Δ₃(L).
    
    Die Δ₃-Statistik misst die Abweichung der Staircase Function
    von einer Geraden über eine Längenskala L.
    
    Δ₃(L) = ⟨ min_{A,B} (1/L) ∫₀ᴸ [N(ε) - Aε - B]² dε ⟩
    
    Für Poisson:  Δ₃(L) ∼ L/15
    Für GUE:      Δ₃(L) ∼ (1/π²) ln(L)
    
    Parameters
    ----------
    unfolded_spectrum : np.ndarray
        Entfaltetes Spektrum
    L_max : int, optional
        Maximale Längenskala, default: 100
    
    Returns
    -------
    L_values : np.ndarray
        Längenskalen
    Delta3_values : np.ndarray
        Δ₃(L) Werte
    
    References
    ----------
    - Mehta (2004): "Random Matrices", Chapter 15
    """
    n = len(unfolded_spectrum)
    epsilon = unfolded_spectrum
    
    L_values = np.arange(2, min(L_max, n // 2))
    Delta3_values = np.zeros(len(L_values))
    
    for idx, L in enumerate(L_values):
        # Anzahl der Intervalle
        n_intervals = n - L
        delta3_sum = 0.0
        
        for i in range(n_intervals):
            # Intervall [ε_i, ε_{i+L}]
            eps_interval = epsilon[i:i + L + 1]
            staircase = np.arange(len(eps_interval))
            
            # Best-fit-Gerade
            A, B = np.polyfit(eps_interval, staircase, deg=1)
            fit = A * eps_interval + B
            
            # Mittlere quadratische Abweichung
            deviation = np.mean((staircase - fit) ** 2)
            delta3_sum += deviation
        
        Delta3_values[idx] = delta3_sum / n_intervals
    
    return L_values, Delta3_values


def number_variance(
    unfolded_spectrum: np.ndarray,
    L_max: int = 100
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Berechne die Zahlenvarianz Σ²(L).
    
    Σ²(L) = ⟨n²⟩ - ⟨n⟩²
    
    wobei n die Anzahl der Eigenwerte in einem Intervall der Länge L ist.
    
    Für Poisson:  Σ²(L) = L
    Für GUE:      Σ²(L) ∼ (2/π²) ln(L)
    
    Parameters
    ----------
    unfolded_spectrum : np.ndarray
        Entfaltetes Spektrum
    L_max : int, optional
        Maximale Längenskala
    
    Returns
    -------
    L_values : np.ndarray
        Längenskalen
    Sigma2_values : np.ndarray
        Σ²(L) Werte
    """
    n = len(unfolded_spectrum)
    epsilon = unfolded_spectrum
    
    L_values = np.arange(1, min(L_max, n // 2))
    Sigma2_values = np.zeros(len(L_values))
    
    for idx, L in enumerate(L_values):
        n_intervals = n - int(L)
        counts = []
        
        for i in range(n_intervals):
            # Anzahl der Eigenwerte im Intervall [ε_i, ε_i + L]
            eps_start = epsilon[i]
            eps_end = eps_start + L
            count = np.sum((epsilon >= eps_start) & (epsilon <= eps_end))
            counts.append(count)
        
        # Varianz
        Sigma2_values[idx] = np.var(counts)
    
    return L_values, Sigma2_values


if __name__ == "__main__":
    # Demonstration mit synthetischem Spektrum
    print("=== Spektralanalyse Demo ===\n")
    
    # Synthetisches Spektrum (GUE-ähnlich)
    np.random.seed(42)
    n = 1000
    
    # Random Matrix (GOE)
    from scipy.stats import ortho_group
    H = np.random.randn(n, n)
    H = (H + H.T) / 2  # Symmetrisch
    eigenvalues = np.linalg.eigvalsh(H)
    
    print(f"Spektrum: {len(eigenvalues)} Eigenwerte")
    print(f"E ∈ [{eigenvalues[0]:.3f}, {eigenvalues[-1]:.3f}]")
    
    # Unfolding
    print("\nSpektrales Unfolding...")
    unfolded = spectral_unfolding(eigenvalues, method='polynomial')
    print(f"Entfaltet: ε ∈ [{unfolded[0]:.3f}, {unfolded[-1]:.3f}]")
    print(f"Mittlere Dichte: {len(unfolded) / (unfolded[-1] - unfolded[0]):.3f} (sollte ≈ 1)")
    
    # Lokale Dichte
    print("\nLokale Zustandsdichte...")
    E_centers, rho = local_density(eigenvalues)
    print(f"ρ(E): Mittelwert = {np.nanmean(rho):.3f}, Std = {np.nanstd(rho):.3f}")
