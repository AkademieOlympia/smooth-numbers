"""
Visualisierung der spektralen Eigenschaften

Dieses Modul stellt Plotting-Funktionen für:
- Level Spacing Distribution
- Eigenspektrum
- Parameter-Sweeps
- Vergleiche mit theoretischen Verteilungen
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Optional, List, Tuple
from .level_spacing import (
    poisson_distribution,
    wigner_surmise_GOE,
    wigner_surmise_GUE,
    cumulative_distribution
)

# Stil
sns.set_style("whitegrid")
plt.rcParams['figure.dpi'] = 100
plt.rcParams['font.size'] = 11


def plot_level_statistics(
    spacings: np.ndarray,
    title: str = "Level Spacing Distribution",
    save_path: Optional[str] = None,
    show_theory: bool = True
):
    """
    Plotte Level Spacing Distribution mit theoretischen Vergleichen.
    
    Parameters
    ----------
    spacings : np.ndarray
        Level spacings (normalisiert)
    title : str, optional
        Titel des Plots
    save_path : str, optional
        Speicherpfad (falls None, nur anzeigen)
    show_theory : bool, optional
        Zeige theoretische Kurven (Poisson, GOE, GUE)
    """
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Histogram (PDF)
    ax = axes[0]
    bins = 50
    ax.hist(spacings, bins=bins, density=True, alpha=0.6, 
            color='steelblue', edgecolor='black', label='Daten')
    
    if show_theory:
        s_theory = np.linspace(0, np.max(spacings), 200)
        ax.plot(s_theory, poisson_distribution(s_theory), 
                'r--', lw=2, label='Poisson')
        ax.plot(s_theory, wigner_surmise_GOE(s_theory), 
                'g-', lw=2, label='GOE')
        ax.plot(s_theory, wigner_surmise_GUE(s_theory), 
                'b-', lw=2, label='GUE')
    
    ax.set_xlabel('Spacing s', fontsize=12)
    ax.set_ylabel('Probability Density P(s)', fontsize=12)
    ax.set_title('Probability Density Function', fontsize=13)
    ax.legend(fontsize=10)
    ax.grid(alpha=0.3)
    
    # Cumulative Distribution (CDF)
    ax = axes[1]
    s_sorted, cdf = cumulative_distribution(spacings)
    ax.plot(s_sorted, cdf, 'steelblue', lw=2, label='Daten')
    
    if show_theory:
        s_theory = np.linspace(0, np.max(spacings), 200)
        
        # Poisson CDF: I(s) = 1 - exp(-s)
        cdf_poisson = 1 - np.exp(-s_theory)
        ax.plot(s_theory, cdf_poisson, 'r--', lw=2, label='Poisson')
        
        # GOE CDF (numerisch integriert)
        from scipy.integrate import cumulative_trapezoid
        pdf_GOE = wigner_surmise_GOE(s_theory)
        cdf_GOE = cumulative_trapezoid(pdf_GOE, s_theory, initial=0)
        ax.plot(s_theory, cdf_GOE, 'g-', lw=2, label='GOE')
        
        # GUE CDF
        pdf_GUE = wigner_surmise_GUE(s_theory)
        cdf_GUE = cumulative_trapezoid(pdf_GUE, s_theory, initial=0)
        ax.plot(s_theory, cdf_GUE, 'b-', lw=2, label='GUE')
    
    ax.set_xlabel('Spacing s', fontsize=12)
    ax.set_ylabel('Cumulative Probability I(s)', fontsize=12)
    ax.set_title('Cumulative Distribution Function', fontsize=13)
    ax.legend(fontsize=10)
    ax.grid(alpha=0.3)
    
    fig.suptitle(title, fontsize=14, fontweight='bold')
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Plot gespeichert: {save_path}")
    else:
        plt.show()


def plot_eigenspectrum(
    eigenvalues: np.ndarray,
    unfolded: Optional[np.ndarray] = None,
    title: str = "Eigenspektrum",
    save_path: Optional[str] = None
):
    """
    Plotte Energiespektrum und Staircase Function.
    
    Parameters
    ----------
    eigenvalues : np.ndarray
        Ursprüngliches Spektrum
    unfolded : np.ndarray, optional
        Entfaltetes Spektrum
    title : str, optional
        Titel
    save_path : str, optional
        Speicherpfad
    """
    if unfolded is not None:
        fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    else:
        fig, axes = plt.subplots(1, 2, figsize=(12, 5))
        axes = list(axes) + [None]
    
    # Plot 1: Energiespektrum
    ax = axes[0]
    n = len(eigenvalues)
    ax.plot(range(n), eigenvalues, 'o', markersize=2, alpha=0.6)
    ax.set_xlabel('Index n', fontsize=12)
    ax.set_ylabel('Energie E_n', fontsize=12)
    ax.set_title('Eigenspektrum', fontsize=13)
    ax.grid(alpha=0.3)
    
    # Plot 2: Staircase Function
    ax = axes[1]
    staircase = np.arange(1, n + 1)
    ax.plot(eigenvalues, staircase, 'steelblue', lw=1.5, label='N(E)')
    
    # Smooth Fit (Polynom)
    degree = min(7, n // 10)
    coeffs = np.polyfit(eigenvalues, staircase, deg=degree)
    fit = np.polyval(coeffs, eigenvalues)
    ax.plot(eigenvalues, fit, 'r--', lw=2, label='Smooth Fit')
    
    ax.set_xlabel('Energie E', fontsize=12)
    ax.set_ylabel('Kumulative Zustände N(E)', fontsize=12)
    ax.set_title('Staircase Function', fontsize=13)
    ax.legend(fontsize=10)
    ax.grid(alpha=0.3)
    
    # Plot 3: Entfaltetes Spektrum (optional)
    if unfolded is not None:
        ax = axes[2]
        ax.plot(range(len(unfolded)), unfolded, 'o', markersize=2, alpha=0.6, color='green')
        ax.plot([0, len(unfolded)], [0, len(unfolded)], 'k--', lw=1, label='Linear (ideal)')
        ax.set_xlabel('Index n', fontsize=12)
        ax.set_ylabel('Entfaltetes ε_n', fontsize=12)
        ax.set_title('Entfaltetes Spektrum', fontsize=13)
        ax.legend(fontsize=10)
        ax.grid(alpha=0.3)
    
    fig.suptitle(title, fontsize=14, fontweight='bold')
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Plot gespeichert: {save_path}")
    else:
        plt.show()


def plot_parameter_sweep(
    parameter_values: np.ndarray,
    results: List[dict],
    parameter_name: str = "γ",
    save_path: Optional[str] = None
):
    """
    Plotte Ergebnisse eines Parameter-Sweeps.
    
    Parameters
    ----------
    parameter_values : np.ndarray
        Werte des variierten Parameters
    results : List[dict]
        Liste von Ergebnis-Dictionaries (χ²-Werte, etc.)
    parameter_name : str, optional
        Name des Parameters (für Labels)
    save_path : str, optional
        Speicherpfad
    """
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Plot 1: χ² Werte
    ax = axes[0]
    
    chi2_poisson = [r['poisson'] for r in results]
    chi2_GOE = [r['GOE'] for r in results]
    chi2_GUE = [r['GUE'] for r in results]
    
    ax.plot(parameter_values, chi2_poisson, 'o-', label='Poisson', lw=2)
    ax.plot(parameter_values, chi2_GOE, 's-', label='GOE', lw=2)
    ax.plot(parameter_values, chi2_GUE, '^-', label='GUE', lw=2)
    
    ax.set_xlabel(f'Parameter {parameter_name}', fontsize=12)
    ax.set_ylabel('χ² (Goodness of Fit)', fontsize=12)
    ax.set_title('Fit-Qualität vs. Parameter', fontsize=13)
    ax.legend(fontsize=10)
    ax.set_yscale('log')
    ax.grid(alpha=0.3)
    
    # Plot 2: Brody-Parameter
    ax = axes[1]
    
    brody_q = [r['brody_q'] for r in results]
    
    ax.plot(parameter_values, brody_q, 'o-', color='purple', lw=2, label='Brody q')
    ax.axhline(0, color='red', linestyle='--', lw=1, label='q=0 (Poisson)')
    ax.axhline(1, color='green', linestyle='--', lw=1, label='q=1 (Wigner-Dyson)')
    
    ax.set_xlabel(f'Parameter {parameter_name}', fontsize=12)
    ax.set_ylabel('Brody-Parameter q', fontsize=12)
    ax.set_title('Brody-Interpolation', fontsize=13)
    ax.legend(fontsize=10)
    ax.set_ylim(-0.1, 1.1)
    ax.grid(alpha=0.3)
    
    fig.suptitle(f'Parameter-Sweep: {parameter_name}', fontsize=14, fontweight='bold')
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Plot gespeichert: {save_path}")
    else:
        plt.show()


def plot_spectral_rigidity(
    L_values: np.ndarray,
    Delta3: np.ndarray,
    title: str = "Spektrale Rigidität Δ₃(L)",
    save_path: Optional[str] = None
):
    """
    Plotte spektrale Rigidität Δ₃(L).
    
    Parameters
    ----------
    L_values : np.ndarray
        Längenskalen
    Delta3 : np.ndarray
        Δ₃(L) Werte
    title : str, optional
        Titel
    save_path : str, optional
        Speicherpfad
    """
    fig, ax = plt.subplots(figsize=(8, 6))
    
    ax.plot(L_values, Delta3, 'o-', lw=2, label='Daten')
    
    # Theoretische Vorhersagen
    # Poisson: Δ₃(L) = L/15
    ax.plot(L_values, L_values / 15, 'r--', lw=2, label='Poisson (L/15)')
    
    # GUE: Δ₃(L) ≈ (1/π²) ln(L) + const
    ax.plot(L_values, (1 / np.pi**2) * np.log(L_values) + 0.5, 
            'g-', lw=2, label='GUE ((1/π²)ln L)')
    
    ax.set_xlabel('Längenskala L', fontsize=12)
    ax.set_ylabel('Δ₃(L)', fontsize=12)
    ax.set_title(title, fontsize=13)
    ax.legend(fontsize=10)
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.grid(alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Plot gespeichert: {save_path}")
    else:
        plt.show()


if __name__ == "__main__":
    # Demonstration
    print("=== Visualisierung Demo ===\n")
    
    np.random.seed(42)
    
    # Synthetisches Spektrum (GOE)
    n = 500
    H = np.random.randn(n, n)
    H = (H + H.T) / 2
    eigenvalues = np.linalg.eigvalsh(H)
    
    # Unfolding (einfach)
    unfolded = (eigenvalues - eigenvalues[0]) / np.mean(np.diff(eigenvalues))
    
    # Spacings
    spacings = np.diff(unfolded)
    spacings = spacings / np.mean(spacings)
    
    print("Plotte Level Statistics...")
    plot_level_statistics(spacings, title="Demo: GOE-Statistik")
    
    print("\nPlotte Eigenspektrum...")
    plot_eigenspectrum(eigenvalues, unfolded, title="Demo: GOE-Spektrum")
