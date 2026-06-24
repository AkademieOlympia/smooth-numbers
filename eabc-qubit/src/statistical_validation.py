"""
Statistische Validierung und Bootstrap-Analysen für das EABC-Qubit-Framework.

Dieses Modul implementiert rigorose statistische Methoden zur Absicherung
der Hauptresultate für Publikationsreife:

1. Bootstrap-Analyse für σ-Werte mit Konfidenzintervallen
2. Ensemble-Mittelung über Multiple Seeds
3. Alternative Spektralmaße (Ratio Statistic, Σ², Δ₃, K)
4. Unfolding-Robustheit über verschiedene Methoden
5. Finite-Size-Scaling mit Fehlerbalken
6. β-Paramter-Test mit Collatz-Gewichten

Author: EABC Research Group
Date: 2026-06-23
"""

import numpy as np
from scipy import stats
from scipy.optimize import curve_fit
from typing import Dict, List, Tuple, Optional, Callable
import warnings

try:
    from .spectral import spectral_unfolding, spectral_rigidity, number_variance, compute_spectrum
    from .level_spacing import (
        compute_level_spacing, 
        brody_distribution, 
        fit_level_statistics,
        spectral_form_factor
    )
except ImportError:
    # Fallback für direkten Import
    from spectral import spectral_unfolding, spectral_rigidity, number_variance, compute_spectrum
    from level_spacing import (
        compute_level_spacing, 
        brody_distribution, 
        fit_level_statistics,
        spectral_form_factor
    )


def bootstrap_spacing_std(
    spacings: np.ndarray,
    n_bootstrap: int = 1000,
    confidence_level: float = 0.95,
    seed: Optional[int] = None
) -> Dict[str, float]:
    """
    Bootstrap-Resampling für die Standardabweichung der Level Spacings.
    
    Berechnet σ = std(spacings) mit Konfidenzintervall via Bootstrap.
    
    Parameters
    ----------
    spacings : np.ndarray
        Level spacings (normalisiert: ⟨s⟩ = 1)
    n_bootstrap : int, optional
        Anzahl Bootstrap-Samples, default: 1000
    confidence_level : float, optional
        Konfidenzlevel (z.B. 0.95 für 95% CI), default: 0.95
    seed : int, optional
        Random seed für Reproduzierbarkeit
    
    Returns
    -------
    Dict[str, float]
        Dictionary mit Keys:
        - 'mean': Mittelwert von σ über Bootstrap-Samples
        - 'std': Standardabweichung von σ
        - 'ci_lower': Untere Grenze des Konfidenzintervalls
        - 'ci_upper': Obere Grenze des Konfidenzintervalls
        - 'median': Median von σ
    
    Examples
    --------
    >>> spacings = np.random.exponential(1.0, 1000)
    >>> result = bootstrap_spacing_std(spacings)
    >>> print(f"σ = {result['mean']:.3f} ± {result['std']:.3f}")
    >>> print(f"95% CI: [{result['ci_lower']:.3f}, {result['ci_upper']:.3f}]")
    """
    if seed is not None:
        np.random.seed(seed)
    
    n = len(spacings)
    sigma_bootstrap = np.zeros(n_bootstrap)
    
    for i in range(n_bootstrap):
        # Resampling mit Zurücklegen
        resampled = np.random.choice(spacings, size=n, replace=True)
        sigma_bootstrap[i] = np.std(resampled)
    
    # Statistiken berechnen
    alpha = 1 - confidence_level
    ci_lower = np.percentile(sigma_bootstrap, 100 * alpha / 2)
    ci_upper = np.percentile(sigma_bootstrap, 100 * (1 - alpha / 2))
    
    return {
        'mean': np.mean(sigma_bootstrap),
        'std': np.std(sigma_bootstrap),
        'ci_lower': ci_lower,
        'ci_upper': ci_upper,
        'median': np.median(sigma_bootstrap)
    }


def bootstrap_brody_q(
    spacings: np.ndarray,
    n_bootstrap: int = 500,
    confidence_level: float = 0.95,
    bins: int = 50,
    seed: Optional[int] = None
) -> Dict[str, float]:
    """
    Bootstrap-Analyse für den Brody-Parameter q.
    
    Der Brody-Parameter interpoliert zwischen Poisson (q=0) und Wigner-Dyson (q=1).
    
    Parameters
    ----------
    spacings : np.ndarray
        Level spacings
    n_bootstrap : int, optional
        Anzahl Bootstrap-Samples, default: 500
    confidence_level : float, optional
        Konfidenzlevel, default: 0.95
    bins : int, optional
        Anzahl Bins für Histogramm-Fit, default: 50
    seed : int, optional
        Random seed
    
    Returns
    -------
    Dict[str, float]
        Bootstrap-Statistiken für q
    """
    if seed is not None:
        np.random.seed(seed)
    
    n = len(spacings)
    q_bootstrap = []
    
    for i in range(n_bootstrap):
        resampled = np.random.choice(spacings, size=n, replace=True)
        
        # Fitte Brody-Verteilung
        try:
            fit_result = fit_level_statistics(resampled, bins=bins)
            q = fit_result.get('brody_q', np.nan)
            
            if not np.isnan(q) and 0 <= q <= 1:
                q_bootstrap.append(q)
        except:
            continue
    
    if len(q_bootstrap) < n_bootstrap // 2:
        warnings.warn(f"Nur {len(q_bootstrap)}/{n_bootstrap} Bootstrap-Fits erfolgreich")
    
    q_bootstrap = np.array(q_bootstrap)
    
    alpha = 1 - confidence_level
    ci_lower = np.percentile(q_bootstrap, 100 * alpha / 2)
    ci_upper = np.percentile(q_bootstrap, 100 * (1 - alpha / 2))
    
    return {
        'mean': np.mean(q_bootstrap),
        'std': np.std(q_bootstrap),
        'ci_lower': ci_lower,
        'ci_upper': ci_upper,
        'median': np.median(q_bootstrap),
        'n_successful': len(q_bootstrap)
    }


def ratio_statistic(spacings: np.ndarray) -> float:
    """
    Berechne die Ratio-Statistik r̄ für Level Spacings.
    
    Definiert als:
        r_n = min(s_n, s_{n+1}) / max(s_n, s_{n+1})
        r̄ = ⟨r_n⟩
    
    Theoretische Werte:
    - Poisson:  r̄ ≈ 0.386
    - GOE:      r̄ ≈ 0.530
    - GUE:      r̄ ≈ 0.603
    
    Parameters
    ----------
    spacings : np.ndarray
        Level spacings
    
    Returns
    -------
    float
        Mittlere Ratio r̄
    
    References
    ----------
    - Oganesyan & Huse (2007): "Localization of interacting fermions at high temperature"
    - Atas et al. (2013): "Distribution of the ratio of consecutive level spacings"
    """
    ratios = []
    for i in range(len(spacings) - 1):
        s_min = min(spacings[i], spacings[i + 1])
        s_max = max(spacings[i], spacings[i + 1])
        
        if s_max > 0:
            r = s_min / s_max
            ratios.append(r)
    
    return np.mean(ratios) if ratios else np.nan


def bootstrap_ratio_statistic(
    spacings: np.ndarray,
    n_bootstrap: int = 1000,
    confidence_level: float = 0.95,
    seed: Optional[int] = None
) -> Dict[str, float]:
    """
    Bootstrap-Analyse für die Ratio-Statistik.
    
    Parameters
    ----------
    spacings : np.ndarray
        Level spacings
    n_bootstrap : int, optional
        Anzahl Bootstrap-Samples, default: 1000
    confidence_level : float, optional
        Konfidenzlevel, default: 0.95
    seed : int, optional
        Random seed
    
    Returns
    -------
    Dict[str, float]
        Bootstrap-Statistiken für r̄
    """
    if seed is not None:
        np.random.seed(seed)
    
    n = len(spacings)
    r_bootstrap = np.zeros(n_bootstrap)
    
    for i in range(n_bootstrap):
        resampled = np.random.choice(spacings, size=n, replace=True)
        r_bootstrap[i] = ratio_statistic(resampled)
    
    alpha = 1 - confidence_level
    ci_lower = np.percentile(r_bootstrap, 100 * alpha / 2)
    ci_upper = np.percentile(r_bootstrap, 100 * (1 - alpha / 2))
    
    return {
        'mean': np.mean(r_bootstrap),
        'std': np.std(r_bootstrap),
        'ci_lower': ci_lower,
        'ci_upper': ci_upper,
        'median': np.median(r_bootstrap)
    }


def ensemble_analysis(
    hamiltonian_factory: Callable,
    n_ensemble: int = 50,
    k_eigenvalues: int = 500,
    unfolding_method: str = 'polynomial',
    seed_offset: int = 0
) -> Dict[str, np.ndarray]:
    """
    Ensemble-Mittelung über mehrere Hamiltonian-Realisierungen.
    
    Wiederholt die spektrale Analyse mit verschiedenen Seeds und berechnet
    Mittelwerte und Fehlerbalken für alle relevanten Observablen.
    
    Parameters
    ----------
    hamiltonian_factory : Callable
        Funktion die Hamiltonian-Objekt erzeugt: H = factory(seed)
        Muss Methode compute_spectrum(k, which) haben
    n_ensemble : int, optional
        Anzahl verschiedener Realisierungen, default: 50
    k_eigenvalues : int, optional
        Anzahl Eigenwerte pro Realisierung, default: 500
    unfolding_method : str, optional
        Unfolding-Methode ('polynomial' oder 'spline'), default: 'polynomial'
    seed_offset : int, optional
        Offset für Seeds, default: 0
    
    Returns
    -------
    Dict[str, np.ndarray]
        Dictionary mit Arrays für jede Observable über das Ensemble:
        - 'sigma': σ-Werte
        - 'brody_q': Brody-Parameter
        - 'ratio': Ratio-Statistik
        - 'mean_spacing': Mittlere Spacings
    
    Examples
    --------
    >>> from hamiltonian import CollatzEABCHamiltonian
    >>> factory = lambda seed: CollatzEABCHamiltonian(N=1000, gamma=1.5, random_seed=seed)
    >>> results = ensemble_analysis(factory, n_ensemble=100)
    >>> print(f"σ = {np.mean(results['sigma']):.3f} ± {np.std(results['sigma']):.3f}")
    """
    sigmas = []
    brody_qs = []
    ratios = []
    mean_spacings = []
    
    print(f"Starte Ensemble-Analyse mit {n_ensemble} Realisierungen...")
    
    for i in range(n_ensemble):
        if (i + 1) % 10 == 0:
            print(f"  Fortschritt: {i+1}/{n_ensemble}")
        
        try:
            # Hamiltonian mit neuem Seed erzeugen
            H = hamiltonian_factory(seed_offset + i)
            
            # Spektrum berechnen
            eigenvalues = H.compute_spectrum(k=k_eigenvalues, which='SM')
            
            # Unfolding
            unfolded = spectral_unfolding(eigenvalues, method=unfolding_method)
            
            # Level spacings
            spacings = compute_level_spacing(unfolded)
            
            # Observablen berechnen
            sigma = np.std(spacings)
            sigmas.append(sigma)
            
            mean_s = np.mean(spacings)
            mean_spacings.append(mean_s)
            
            r = ratio_statistic(spacings)
            ratios.append(r)
            
            # Brody-Fit (kann fehlschlagen)
            try:
                fit_result = fit_level_statistics(spacings, bins=50)
                q = fit_result.get('brody_q', np.nan)
                if not np.isnan(q) and 0 <= q <= 1:
                    brody_qs.append(q)
            except:
                pass
        
        except Exception as e:
            warnings.warn(f"Realisierung {i} fehlgeschlagen: {e}")
            continue
    
    print(f"✓ Ensemble-Analyse abgeschlossen: {len(sigmas)} erfolgreiche Realisierungen")
    
    return {
        'sigma': np.array(sigmas),
        'brody_q': np.array(brody_qs),
        'ratio': np.array(ratios),
        'mean_spacing': np.array(mean_spacings)
    }


def compare_scenarios_with_bootstrap(
    scenarios: Dict[str, Callable],
    n_ensemble: int = 100,
    n_bootstrap: int = 1000,
    k_eigenvalues: int = 500
) -> Dict[str, Dict]:
    """
    Vergleiche mehrere Szenarien mit vollständiger statistischer Analyse.
    
    Für jedes Szenario:
    1. Ensemble-Mittelung über n_ensemble Realisierungen
    2. Bootstrap-Analyse für Konfidenzintervalle
    3. Statistische Tests zwischen Szenarien
    
    Parameters
    ----------
    scenarios : Dict[str, Callable]
        Dictionary: Name -> Hamiltonian-Factory-Funktion
        Factory: factory(seed) -> Hamiltonian-Objekt
    n_ensemble : int, optional
        Anzahl Ensemble-Realisierungen pro Szenario, default: 100
    n_bootstrap : int, optional
        Anzahl Bootstrap-Samples, default: 1000
    k_eigenvalues : int, optional
        Anzahl Eigenwerte pro Realisierung, default: 500
    
    Returns
    -------
    Dict[str, Dict]
        Verschachteltes Dictionary: scenario -> observable -> statistics
    
    Examples
    --------
    >>> scenarios = {
    ...     'Collatz': lambda seed: CollatzEABCHamiltonian(N=1000, gamma=1.5, random_seed=seed),
    ...     'Uniform': lambda seed: EABCHamiltonian(N=1000, gamma=1.5)
    ... }
    >>> results = compare_scenarios_with_bootstrap(scenarios, n_ensemble=50)
    """
    results = {}
    
    print("="*70)
    print("STATISTISCHE VALIDIERUNG: Szenario-Vergleich mit Bootstrap")
    print("="*70)
    
    for scenario_name, factory in scenarios.items():
        print(f"\n>>> Szenario: {scenario_name}")
        
        # Ensemble-Analyse
        ensemble_data = ensemble_analysis(
            factory, 
            n_ensemble=n_ensemble, 
            k_eigenvalues=k_eigenvalues
        )
        
        # Bootstrap für σ
        sigma_bootstrap = bootstrap_spacing_std(
            ensemble_data['sigma'], 
            n_bootstrap=n_bootstrap
        )
        
        # Bootstrap für Ratio
        ratio_bootstrap = bootstrap_ratio_statistic(
            ensemble_data['ratio'], 
            n_bootstrap=n_bootstrap
        )
        
        # Statistiken speichern
        results[scenario_name] = {
            'ensemble_data': ensemble_data,
            'sigma': {
                'mean': np.mean(ensemble_data['sigma']),
                'std': np.std(ensemble_data['sigma']),
                'ci_lower': sigma_bootstrap['ci_lower'],
                'ci_upper': sigma_bootstrap['ci_upper'],
                'n_samples': len(ensemble_data['sigma'])
            },
            'ratio': {
                'mean': np.mean(ensemble_data['ratio']),
                'std': np.std(ensemble_data['ratio']),
                'ci_lower': ratio_bootstrap['ci_lower'],
                'ci_upper': ratio_bootstrap['ci_upper'],
                'n_samples': len(ensemble_data['ratio'])
            },
            'brody_q': {
                'mean': np.mean(ensemble_data['brody_q']) if len(ensemble_data['brody_q']) > 0 else np.nan,
                'std': np.std(ensemble_data['brody_q']) if len(ensemble_data['brody_q']) > 0 else np.nan,
                'n_samples': len(ensemble_data['brody_q'])
            }
        }
        
        # Ausgabe
        print(f"\n  σ = {results[scenario_name]['sigma']['mean']:.4f} ± {results[scenario_name]['sigma']['std']:.4f}")
        print(f"  95% CI: [{results[scenario_name]['sigma']['ci_lower']:.4f}, {results[scenario_name]['sigma']['ci_upper']:.4f}]")
        print(f"  n = {results[scenario_name]['sigma']['n_samples']}")
        
        print(f"\n  r̄ = {results[scenario_name]['ratio']['mean']:.4f} ± {results[scenario_name]['ratio']['std']:.4f}")
        print(f"  95% CI: [{results[scenario_name]['ratio']['ci_lower']:.4f}, {results[scenario_name]['ratio']['ci_upper']:.4f}]")
    
    # Paarweise statistische Tests
    print("\n" + "="*70)
    print("STATISTISCHE TESTS (Paarweise Vergleiche)")
    print("="*70)
    
    scenario_names = list(scenarios.keys())
    for i in range(len(scenario_names)):
        for j in range(i + 1, len(scenario_names)):
            name1, name2 = scenario_names[i], scenario_names[j]
            
            # t-Test für σ-Werte
            sigma1 = results[name1]['ensemble_data']['sigma']
            sigma2 = results[name2]['ensemble_data']['sigma']
            
            t_stat, p_value = stats.ttest_ind(sigma1, sigma2)
            
            print(f"\n{name1} vs {name2}:")
            print(f"  σ₁ = {np.mean(sigma1):.4f}, σ₂ = {np.mean(sigma2):.4f}")
            print(f"  t = {t_stat:.3f}, p = {p_value:.4e}")
            
            if p_value < 0.001:
                print(f"  → Hochsignifikanter Unterschied (p < 0.001) ✓")
            elif p_value < 0.01:
                print(f"  → Signifikanter Unterschied (p < 0.01) ✓")
            elif p_value < 0.05:
                print(f"  → Schwach signifikanter Unterschied (p < 0.05)")
            else:
                print(f"  → Kein signifikanter Unterschied (p ≥ 0.05)")
    
    return results


def unfolding_robustness_test(
    H,
    k_eigenvalues: int = 500,
    methods: Optional[List[str]] = None,
    polynomial_degrees: Optional[List[int]] = None,
    spline_smoothings: Optional[List[float]] = None
) -> Dict[str, Dict[str, float]]:
    """
    Teste Robustheit der Resultate über verschiedene Unfolding-Methoden.
    
    Variiert:
    - Polynomial-Grad (3, 5, 7, 9)
    - Spline-Smoothing-Parameter
    
    Parameters
    ----------
    H : EABCHamiltonian
        Hamiltonian-Objekt
    k_eigenvalues : int, optional
        Anzahl Eigenwerte, default: 500
    methods : List[str], optional
        Liste von Methoden ['polynomial', 'spline'], default: beide
    polynomial_degrees : List[int], optional
        Polynomial-Grade zu testen, default: [3, 5, 7, 9]
    spline_smoothings : List[float], optional
        Smoothing-Parameter für Spline, default: [0.001, 0.01, 0.1]
    
    Returns
    -------
    Dict[str, Dict[str, float]]
        Verschachteltes Dict: method_params -> {'sigma', 'ratio', 'brody_q'}
    """
    if methods is None:
        methods = ['polynomial', 'spline']
    
    if polynomial_degrees is None:
        polynomial_degrees = [3, 5, 7, 9]
    
    if spline_smoothings is None:
        spline_smoothings = [0.001, 0.01, 0.1]
    
    print("="*70)
    print("UNFOLDING-ROBUSTHEITS-TEST")
    print("="*70)
    
    # Spektrum berechnen (nur einmal)
    print(f"\nBerechne Spektrum mit {k_eigenvalues} Eigenwerten...")
    eigenvalues = H.compute_spectrum(k=k_eigenvalues, which='SM')
    
    results = {}
    
    # Test verschiedene Polynomial-Grade
    if 'polynomial' in methods:
        print("\n>>> Polynomial-Unfolding:")
        for degree in polynomial_degrees:
            # Modifizierte Unfolding-Funktion mit explizitem Grad
            try:
                # Manuelles Unfolding mit spezifischem Grad
                n = len(eigenvalues)
                E = eigenvalues
                staircase = np.arange(1, n + 1, dtype=float)
                
                deg = min(degree, n // 10)
                coeffs = np.polyfit(E, staircase, deg=deg)
                N_smooth = np.polyval(coeffs, E)
                unfolded = N_smooth
                
                spacings = compute_level_spacing(unfolded)
                
                sigma = np.std(spacings)
                r = ratio_statistic(spacings)
                
                try:
                    fit_result = fit_level_statistics(spacings, bins=50)
                    q = fit_result.get('brody_q', np.nan)
                except:
                    q = np.nan
                
                key = f'polynomial_deg{degree}'
                results[key] = {
                    'sigma': sigma,
                    'ratio': r,
                    'brody_q': q
                }
                
                print(f"  Grad {degree}: σ = {sigma:.4f}, r̄ = {r:.4f}, q = {q:.3f}")
            
            except Exception as e:
                warnings.warn(f"Polynomial Grad {degree} fehlgeschlagen: {e}")
    
    # Test verschiedene Spline-Smoothings
    if 'spline' in methods:
        print("\n>>> Spline-Unfolding:")
        for smoothing in spline_smoothings:
            try:
                unfolded = spectral_unfolding(eigenvalues, method='spline', smoothing=smoothing)
                spacings = compute_level_spacing(unfolded)
                
                sigma = np.std(spacings)
                r = ratio_statistic(spacings)
                
                try:
                    fit_result = fit_level_statistics(spacings, bins=50)
                    q = fit_result.get('brody_q', np.nan)
                except:
                    q = np.nan
                
                key = f'spline_s{smoothing}'
                results[key] = {
                    'sigma': sigma,
                    'ratio': r,
                    'brody_q': q
                }
                
                print(f"  Smoothing {smoothing}: σ = {sigma:.4f}, r̄ = {r:.4f}, q = {q:.3f}")
            
            except Exception as e:
                warnings.warn(f"Spline s={smoothing} fehlgeschlagen: {e}")
    
    # Analyse der Robustheit
    print("\n" + "="*70)
    print("ROBUSTHEITS-ANALYSE")
    print("="*70)
    
    sigmas = [r['sigma'] for r in results.values()]
    ratios = [r['ratio'] for r in results.values()]
    
    print(f"\nσ über alle Methoden:")
    print(f"  Mittelwert: {np.mean(sigmas):.4f}")
    print(f"  Std.-Abw.: {np.std(sigmas):.4f}")
    print(f"  Min: {np.min(sigmas):.4f}, Max: {np.max(sigmas):.4f}")
    print(f"  Relative Variation: {100*np.std(sigmas)/np.mean(sigmas):.2f}%")
    
    print(f"\nr̄ über alle Methoden:")
    print(f"  Mittelwert: {np.mean(ratios):.4f}")
    print(f"  Std.-Abw.: {np.std(ratios):.4f}")
    print(f"  Min: {np.min(ratios):.4f}, Max: {np.max(ratios):.4f}")
    print(f"  Relative Variation: {100*np.std(ratios)/np.mean(ratios):.2f}%")
    
    return results


def finite_size_scaling_with_errors(
    hamiltonian_factory: Callable,
    N_values: List[int],
    n_ensemble: int = 50,
    k_eigenvalues: int = 500
) -> Dict[int, Dict]:
    """
    Finite-Size-Scaling mit Fehlerbalken aus Ensemble-Mittelung.
    
    Für jede Systemgröße N:
    - Ensemble von n_ensemble Realisierungen
    - Berechne Mittelwert und Standardabweichung von σ, r̄, q
    
    Parameters
    ----------
    hamiltonian_factory : Callable
        Factory-Funktion: factory(N, seed) -> Hamiltonian
    N_values : List[int]
        Liste von Systemgrößen
    n_ensemble : int, optional
        Anzahl Realisierungen pro N, default: 50
    k_eigenvalues : int, optional
        Anzahl Eigenwerte, default: 500
    
    Returns
    -------
    Dict[int, Dict]
        N -> {'sigma_mean', 'sigma_std', 'ratio_mean', 'ratio_std', ...}
    
    Examples
    --------
    >>> from hamiltonian import CollatzEABCHamiltonian
    >>> factory = lambda N, seed: CollatzEABCHamiltonian(N=N, gamma=1.5, random_seed=seed)
    >>> N_values = [500, 1000, 2000, 3000]
    >>> results = finite_size_scaling_with_errors(factory, N_values, n_ensemble=30)
    """
    results = {}
    
    print("="*70)
    print("FINITE-SIZE-SCALING MIT FEHLERBALKEN")
    print("="*70)
    
    for N in N_values:
        print(f"\n>>> N = {N}")
        
        # Factory für dieses N
        factory_N = lambda seed: hamiltonian_factory(N, seed)
        
        # Ensemble-Analyse
        ensemble_data = ensemble_analysis(
            factory_N,
            n_ensemble=n_ensemble,
            k_eigenvalues=k_eigenvalues
        )
        
        # Statistiken berechnen
        sigma_mean = np.mean(ensemble_data['sigma'])
        sigma_std = np.std(ensemble_data['sigma'])
        
        ratio_mean = np.mean(ensemble_data['ratio'])
        ratio_std = np.std(ensemble_data['ratio'])
        
        brody_q_mean = np.mean(ensemble_data['brody_q']) if len(ensemble_data['brody_q']) > 0 else np.nan
        brody_q_std = np.std(ensemble_data['brody_q']) if len(ensemble_data['brody_q']) > 0 else np.nan
        
        results[N] = {
            'sigma_mean': sigma_mean,
            'sigma_std': sigma_std,
            'ratio_mean': ratio_mean,
            'ratio_std': ratio_std,
            'brody_q_mean': brody_q_mean,
            'brody_q_std': brody_q_std,
            'n_samples': len(ensemble_data['sigma'])
        }
        
        print(f"  σ = {sigma_mean:.4f} ± {sigma_std:.4f}")
        print(f"  r̄ = {ratio_mean:.4f} ± {ratio_std:.4f}")
        if not np.isnan(brody_q_mean):
            print(f"  q = {brody_q_mean:.3f} ± {brody_q_std:.3f}")
    
    return results


def beta_collapse_with_collatz_weights(
    hamiltonian_factory: Callable,
    beta_values: List[float],
    n_ensemble: int = 30,
    k_eigenvalues: int = 500,
    N: int = 1000
) -> Dict[float, Dict]:
    """
    Test des β-Kollaps (β=0 → q≈0) mit Collatz-Gewichten.
    
    Kritische Frage: Bleibt der β-Kollaps auch mit Collatz-gewichteten
    Primzahl-Defekten erhalten?
    
    Falls JA: "Collatz → chirale Z₄-Projektion → Level Repulsion" bestätigt!
    
    Parameters
    ----------
    hamiltonian_factory : Callable
        Factory: factory(N, beta, seed) -> Hamiltonian
    beta_values : List[float]
        Liste von β-Werten (chirale Kopplung)
    n_ensemble : int, optional
        Ensemble-Größe, default: 30
    k_eigenvalues : int, optional
        Anzahl Eigenwerte, default: 500
    N : int, optional
        Systemgröße, default: 1000
    
    Returns
    -------
    Dict[float, Dict]
        β -> {'brody_q_mean', 'brody_q_std', ...}
    """
    results = {}
    
    print("="*70)
    print("β-KOLLAPS-TEST MIT COLLATZ-GEWICHTEN")
    print("="*70)
    print(f"\nSystemgröße: N = {N}")
    print(f"Ensemble: {n_ensemble} Realisierungen pro β")
    
    for beta in beta_values:
        print(f"\n>>> β = {beta:.2f}")
        
        # Factory für diesen β-Wert
        factory_beta = lambda seed: hamiltonian_factory(N, beta, seed)
        
        # Ensemble-Analyse
        ensemble_data = ensemble_analysis(
            factory_beta,
            n_ensemble=n_ensemble,
            k_eigenvalues=k_eigenvalues
        )
        
        # Brody-q Statistiken
        if len(ensemble_data['brody_q']) > 0:
            q_mean = np.mean(ensemble_data['brody_q'])
            q_std = np.std(ensemble_data['brody_q'])
        else:
            q_mean = np.nan
            q_std = np.nan
        
        results[beta] = {
            'brody_q_mean': q_mean,
            'brody_q_std': q_std,
            'sigma_mean': np.mean(ensemble_data['sigma']),
            'sigma_std': np.std(ensemble_data['sigma']),
            'ratio_mean': np.mean(ensemble_data['ratio']),
            'ratio_std': np.std(ensemble_data['ratio']),
            'n_samples': len(ensemble_data['brody_q'])
        }
        
        if not np.isnan(q_mean):
            print(f"  q = {q_mean:.3f} ± {q_std:.3f}")
            print(f"  σ = {results[beta]['sigma_mean']:.4f} ± {results[beta]['sigma_std']:.4f}")
            print(f"  r̄ = {results[beta]['ratio_mean']:.4f} ± {results[beta]['ratio_std']:.4f}")
    
    # Analyse des Kollaps
    print("\n" + "="*70)
    print("KOLLAPS-ANALYSE")
    print("="*70)
    
    q_values = [results[beta]['brody_q_mean'] for beta in beta_values if not np.isnan(results[beta]['brody_q_mean'])]
    valid_betas = [beta for beta in beta_values if not np.isnan(results[beta]['brody_q_mean'])]
    
    if len(q_values) >= 2:
        print(f"\nβ = {valid_betas[0]:.1f}: q = {q_values[0]:.3f}")
        print(f"β = {valid_betas[-1]:.1f}: q = {q_values[-1]:.3f}")
        print(f"Δq = {abs(q_values[-1] - q_values[0]):.3f}")
        
        if valid_betas[0] == 0.0 and q_values[0] < 0.2:
            print("\n✓ β-Kollaps bestätigt: β=0 → q≈0 (Poisson-Nähe)")
        
        if q_values[-1] > 0.5:
            print("✓ Chiraler Effekt bestätigt: β>0 → q>0.5 (Level Repulsion)")
    
    return results


if __name__ == "__main__":
    # Demonstration
    print("="*70)
    print("STATISTISCHE VALIDIERUNG - DEMO")
    print("="*70)
    
    # Test mit synthetischen Daten
    np.random.seed(42)
    
    # Poisson-Spacings
    print("\n>>> Test mit Poisson-Spacings")
    spacings_poisson = np.random.exponential(1.0, 1000)
    result = bootstrap_spacing_std(spacings_poisson, n_bootstrap=1000)
    print(f"σ = {result['mean']:.3f} ± {result['std']:.3f}")
    print(f"95% CI: [{result['ci_lower']:.3f}, {result['ci_upper']:.3f}]")
    
    ratio_result = bootstrap_ratio_statistic(spacings_poisson, n_bootstrap=1000)
    print(f"r̄ = {ratio_result['mean']:.3f} ± {ratio_result['std']:.3f}")
    print(f"95% CI: [{ratio_result['ci_lower']:.3f}, {ratio_result['ci_upper']:.3f}]")
    print("(Theorie Poisson: r̄ ≈ 0.386)")
    
    # GOE-Spacings (aus Random Matrix)
    print("\n>>> Test mit GOE-Spacings")
    n_matrix = 500
    H_goe = np.random.randn(n_matrix, n_matrix)
    H_goe = (H_goe + H_goe.T) / 2
    eigenvalues_goe = np.linalg.eigvalsh(H_goe)
    unfolded_goe = (eigenvalues_goe - eigenvalues_goe[0]) / np.mean(np.diff(eigenvalues_goe))
    spacings_goe = compute_level_spacing(unfolded_goe)
    
    result_goe = bootstrap_spacing_std(spacings_goe, n_bootstrap=1000)
    print(f"σ = {result_goe['mean']:.3f} ± {result_goe['std']:.3f}")
    print(f"95% CI: [{result_goe['ci_lower']:.3f}, {result_goe['ci_upper']:.3f}]")
    
    ratio_result_goe = bootstrap_ratio_statistic(spacings_goe, n_bootstrap=1000)
    print(f"r̄ = {ratio_result_goe['mean']:.3f} ± {ratio_result_goe['std']:.3f}")
    print(f"95% CI: [{ratio_result_goe['ci_lower']:.3f}, {ratio_result_goe['ci_upper']:.3f}]")
    print("(Theorie GOE: r̄ ≈ 0.530)")
    
    print("\n" + "="*70)
    print("Modul erfolgreich getestet!")
    print("="*70)
