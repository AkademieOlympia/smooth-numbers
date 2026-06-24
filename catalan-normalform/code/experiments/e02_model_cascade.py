"""
Experiment E02: Modellkaskade M0-M4

Testet systematisch, wie viel der Varianz von Catalan-Magic M_C(n)
durch sukzessive reichere arithmetische Koordinaten erklärt wird.

Kernfrage: Erklärt H(n) zusätzliche Varianz über Ω, Ω², (v₂, v₃) hinaus?
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error
from scipy import stats
from typing import Dict, List, Tuple
import json
from datetime import datetime

from utils.eabc import compute_svn_coordinates, count_prime_factors
from utils.catalan_magic import compute_catalan_magic


def generate_dataset(n_min: int = 2, n_max: int = 1000, omega_min: int = 4) -> List[int]:
    """
    Generiert Datensatz von Zahlen für Experiment.
    
    Args:
        n_min: Minimale Zahl
        n_max: Maximale Zahl
        omega_min: Minimale Anzahl Primfaktoren
        
    Returns:
        Liste von Zahlen mit Ω(n) ≥ omega_min
    """
    numbers = []
    for n in range(n_min, n_max + 1):
        if count_prime_factors(n) >= omega_min:
            numbers.append(n)
    
    print(f"Datensatz generiert: {len(numbers)} Zahlen mit Ω ≥ {omega_min}")
    return numbers


def compute_features(numbers: List[int], canonization: str = 'balanced') -> Dict[str, np.ndarray]:
    """
    Berechnet Features für alle Zahlen.
    
    Returns:
        Dictionary mit numpy arrays für jedes Feature
    """
    print(f"Berechne Features für {len(numbers)} Zahlen...")
    
    # Sammle alle Koordinaten
    all_coords = [compute_svn_coordinates(n) for n in numbers]
    M_C = np.array([compute_catalan_magic(n, method=canonization) for n in numbers])
    
    # Extrahiere Features
    omega = np.array([c['omega'] for c in all_coords])
    omega_sq = omega ** 2
    sigma = np.array([c['sigma'] for c in all_coords])
    v2 = np.array([c['v2'] for c in all_coords])
    v3 = np.array([c['v3'] for c in all_coords])
    
    e = np.array([c['e'] for c in all_coords])
    a = np.array([c['a'] for c in all_coords])
    b = np.array([c['b'] for c in all_coords])
    c = np.array([c['c'] for c in all_coords])
    
    norm_sq = np.array([c['norm_sq'] for c in all_coords])
    H = np.array([c['H'] for c in all_coords])
    omega_eabc = np.array([c['omega_eabc'] for c in all_coords])
    
    print("Features berechnet.")
    
    return {
        'M_C': M_C,
        'omega': omega,
        'omega_sq': omega_sq,
        'sigma': sigma,
        'v2': v2,
        'v3': v3,
        'e': e,
        'a': a,
        'b': b,
        'c': c,
        'norm_sq': norm_sq,
        'H': H,
        'omega_eabc': omega_eabc,
        'numbers': np.array(numbers)
    }


def fit_model(X: np.ndarray, y: np.ndarray, name: str) -> Dict:
    """
    Fitte lineares Modell und berechne Statistiken.
    
    Returns:
        Dictionary mit R², RMSE, Residuen, Modell
    """
    # Entferne NaN-Werte (z.B. H für Zahlen ohne EABC-Faktoren)
    mask = ~np.isnan(X).any(axis=1) & ~np.isnan(y)
    X_clean = X[mask]
    y_clean = y[mask]
    
    if len(X_clean) == 0:
        return {
            'name': name,
            'R2': np.nan,
            'RMSE': np.nan,
            'n_samples': 0,
            'coefficients': None,
            'residuals': None,
            'predictions': None
        }
    
    model = LinearRegression()
    model.fit(X_clean, y_clean)
    
    y_pred = model.predict(X_clean)
    R2 = r2_score(y_clean, y_pred)
    RMSE = np.sqrt(mean_squared_error(y_clean, y_pred))
    residuals = y_clean - y_pred
    
    return {
        'name': name,
        'R2': R2,
        'RMSE': RMSE,
        'n_samples': len(X_clean),
        'coefficients': model.coef_,
        'intercept': model.intercept_,
        'residuals': residuals,
        'predictions': y_pred,
        'mask': mask,
        'model': model
    }


def run_model_cascade(features: Dict[str, np.ndarray]) -> Dict:
    """
    Führt Modellkaskade M0-M4 durch.
    
    Returns:
        Dictionary mit Ergebnissen für alle Modelle
    """
    M_C = features['M_C']
    omega = features['omega']
    omega_sq = features['omega_sq']
    sigma = features['sigma']
    v2 = features['v2']
    v3 = features['v3']
    e = features['e']
    a = features['a']
    b = features['b']
    c = features['c']
    norm_sq = features['norm_sq']
    H = features['H']
    
    print("\nFitting Modelle...")
    
    # M0: M_C ~ Ω
    print("  M0: M_C ~ Ω")
    X_M0 = omega.reshape(-1, 1)
    res_M0 = fit_model(X_M0, M_C, 'M0')
    
    # M0b: M_C ~ Ω + Ω² (kritisch für nichtlineare Effekte!)
    print("  M0b: M_C ~ Ω + Ω²")
    X_M0b = np.column_stack([omega, omega_sq])
    res_M0b = fit_model(X_M0b, M_C, 'M0b')
    
    # M1: M_C ~ Ω + Ω² + σ
    print("  M1: M_C ~ Ω + Ω² + σ")
    X_M1 = np.column_stack([omega, omega_sq, sigma])
    res_M1 = fit_model(X_M1, M_C, 'M1')
    
    # M2: M_C ~ Ω + Ω² + (v₂, v₃)
    print("  M2: M_C ~ Ω + Ω² + (v₂, v₃)")
    X_M2 = np.column_stack([omega, omega_sq, v2, v3])
    res_M2 = fit_model(X_M2, M_C, 'M2')
    
    # M3*: M_C ~ Ω + Ω² + (v₂, v₃) + H  (bevorzugt!)
    print("  M3*: M_C ~ Ω + Ω² + (v₂, v₃) + H")
    X_M3_star = np.column_stack([omega, omega_sq, v2, v3, H])
    res_M3_star = fit_model(X_M3_star, M_C, 'M3*')
    
    # M3: M_C ~ Ω + Ω² + (v₂, v₃) + ||v||² (alternative)
    print("  M3: M_C ~ Ω + Ω² + (v₂, v₃) + ||v||²")
    X_M3 = np.column_stack([omega, omega_sq, v2, v3, norm_sq])
    res_M3 = fit_model(X_M3, M_C, 'M3')
    
    # M4: M_C ~ Ω + Ω² + (v₂, v₃) + v (voller EABC-Vektor)
    print("  M4: M_C ~ Ω + Ω² + (v₂, v₃) + (e, a, b, c)")
    X_M4 = np.column_stack([omega, omega_sq, v2, v3, e, a, b, c])
    res_M4 = fit_model(X_M4, M_C, 'M4')
    
    print("Modelle gefittet.")
    
    # Sammle Ergebnisse
    results = {
        'M0': res_M0,
        'M0b': res_M0b,
        'M1': res_M1,
        'M2': res_M2,
        'M3*': res_M3_star,
        'M3': res_M3,
        'M4': res_M4
    }
    
    # Berechne Δ-Werte
    deltas = compute_deltas(results)
    results['deltas'] = deltas
    
    # Interpretiere Ergebnisse
    interpretation = interpret_results(results)
    results['interpretation'] = interpretation
    
    return results


def compute_deltas(results: Dict) -> Dict:
    """
    Berechnet Δ-Werte zwischen Modellstufen.
    
    Kritische Größe: ΔR²_H = R²(M3*) - R²(M2)
    """
    R2_M0 = results['M0']['R2']
    R2_M0b = results['M0b']['R2']
    R2_M1 = results['M1']['R2']
    R2_M2 = results['M2']['R2']
    R2_M3_star = results['M3*']['R2']
    R2_M3 = results['M3']['R2']
    R2_M4 = results['M4']['R2']
    
    deltas = {
        'Delta_quad': R2_M0b - R2_M0,  # Quadratischer Effekt
        'Delta_sigma': R2_M1 - R2_M0b,  # Teiler-Summe
        'Delta_shell': R2_M2 - R2_M0b,  # Schalen-Koordinaten
        'Delta_H': R2_M3_star - R2_M2,  # Konzentrationsmessung H(n) - KRITISCH!
        'Delta_norm': R2_M3 - R2_M2,    # Norm ||v||²
        'Delta_dir': R2_M4 - R2_M3      # Volle Richtung
    }
    
    return deltas


def interpret_results(results: Dict) -> Dict:
    """
    Interpretiert Ergebnisse nach wissenschaftlichen Kriterien.
    
    Kernfrage: Ist ΔR²_H > η signifikant?
    
    Kritische Klarstellung:
    Der Test entscheidet NICHT über die Gültigkeit der Gauß-Eisenstein-Interpretation
    des EABC-Vektors (die ist auf modularer Ebene bereits ein Satz, A-Niveau),
    sondern über deren zusätzliche Erklärungskraft für Catalan-Magic nach Kontrolle
    der einfacheren Kombinatorik (Ω, Ω², (v₂, v₃)).
    """
    R2_M0 = results['M0']['R2']
    R2_M0b = results['M0b']['R2']
    R2_M2 = results['M2']['R2']
    R2_M3_star = results['M3*']['R2']
    R2_M4 = results['M4']['R2']
    
    Delta_quad = results['deltas']['Delta_quad']
    Delta_H = results['deltas']['Delta_H']
    Delta_norm = results['deltas']['Delta_norm']
    Delta_dir = results['deltas']['Delta_dir']
    
    # Präzise Schwellenwerte für praktische Signifikanz
    eta_weak = 0.01
    eta_moderate = 0.05
    eta_strong = 0.10
    
    interpretation = {
        'H_is_significant': False,
        'H_strength': 'none',
        'hypothesis_supported': False,
        'fall': 0,
        'conclusion': '',
        'meaning': '',
        'consequence': '',
        'recommendations': [],
        'methodological_notes': []
    }
    
    # KRITISCH: Stabilitätsprüfung M0b
    if Delta_quad > 0.05:
        interpretation['methodological_notes'].append(
            f"⚠️ WICHTIG: ΔR²(Ω²) = {Delta_quad:.4f} > 0.05. "
            "Starker nichtlinearer Ω-Effekt! Ohne M0b-Kontrolle wären "
            "alle späteren ΔR² verdächtig."
        )
    else:
        interpretation['methodological_notes'].append(
            f"✓ ΔR²(Ω²) = {Delta_quad:.4f} ≤ 0.05. "
            "Nichtlinearer Ω-Effekt ist schwach, M0b-Kontrolle ist stabil."
        )
    
    # Bewerte ΔR²_H nach präzisen Schwellenwerten
    
    # Fall 1: ΔR²_H < 0.01
    if Delta_H < eta_weak:
        interpretation['fall'] = 1
        interpretation['H_strength'] = 'none'
        interpretation['conclusion'] = (
            f"ΔR²_H = {Delta_H:.4f} < {eta_weak}: "
            "H ist für M_C praktisch redundant."
        )
        interpretation['meaning'] = (
            "M_C ≈ F(Ω, Ω², v₂, v₃). "
            "Gauß-Eisenstein bleibt starke Interpretation des EABC-Vektors, "
            "ABER: Keine erkennbare Brücke zu Catalan. "
            "Catalan-Strukturen sind rein kombinatorisch (Ω-dominiert)."
        )
        interpretation['consequence'] = (
            "Projekt fokussiert auf EABC selbst, nicht Catalan-Verbindung."
        )
        interpretation['recommendations'].append(
            "Hypothese H(n) → M_C(n) zurückgewiesen."
        )
        interpretation['recommendations'].append(
            "EABC hat keine zusätzliche Erklärungskraft für Catalan-Magic."
        )
        interpretation['recommendations'].append(
            "Fokus auf rein kombinatorische Modelle M0-M2."
        )
    
    # Fall 2: 0.01 ≤ ΔR²_H ≤ 0.05
    elif Delta_H <= eta_moderate:
        interpretation['fall'] = 2
        interpretation['H_strength'] = 'weak'
        interpretation['H_is_significant'] = True
        interpretation['conclusion'] = (
            f"ΔR²_H = {Delta_H:.4f} ∈ [0.01, 0.05]: "
            "Schwaches Signal."
        )
        interpretation['meaning'] = (
            "Nicht ignorieren, aber auch nicht überinterpretieren. "
            "Signal könnte artefaktisch sein."
        )
        interpretation['consequence'] = (
            "Weitere Experimente nötig, keine klare Aussage möglich."
        )
        interpretation['recommendations'].append(
            "Hypothese schwach gestützt, aber nicht überzeugend."
        )
        interpretation['recommendations'].append(
            "ERFORDERLICH: Größere Stichprobe (n_max > 5000)."
        )
        interpretation['recommendations'].append(
            "ERFORDERLICH: Cross-Validation (k-fold)."
        )
        interpretation['recommendations'].append(
            "ERFORDERLICH: Permutationstest innerhalb fester Ω-Klassen."
        )
        interpretation['recommendations'].append(
            "ERFORDERLICH: Stratifizierte Analyse nach Ω-Bereichen."
        )
    
    # Fall 3: 0.05 < ΔR²_H ≤ 0.10
    elif Delta_H <= eta_strong:
        interpretation['fall'] = 3
        interpretation['H_strength'] = 'moderate'
        interpretation['H_is_significant'] = True
        interpretation['hypothesis_supported'] = True
        interpretation['conclusion'] = (
            f"ΔR²_H = {Delta_H:.4f} ∈ (0.05, 0.10]: "
            "Moderates Signal – wird interessant."
        )
        interpretation['meaning'] = (
            "Spaltungskonzentration (Gauß/Eisenstein) hat messbare zusätzliche "
            "Erklärungskraft. Nicht mehr rein kombinatorisch. "
            "Erste echte Brücke zwischen algebraischer Zahlentheorie und "
            "Catalan-Hierarchie."
        )
        interpretation['consequence'] = (
            "H0.6 ist empirisch gestützt, weitere Verfeinerungen sinnvoll."
        )
        interpretation['recommendations'].append(
            "Hypothese H(n) → M_C(n) empirisch gestützt!"
        )
        interpretation['recommendations'].append(
            "H(n) hat messbare Zusatzinformation über Baseline hinaus."
        )
        interpretation['recommendations'].append(
            "Weiter mit Experiment E03 (Residualisierung)."
        )
        
        # Interpretation hängt von ΔR²_dir ab
        if Delta_dir > Delta_H:
            interpretation['recommendations'].append(
                f"WICHTIG: ΔR²_dir = {Delta_dir:.4f} > ΔR²_H. "
                "Volle EABC-Richtung wichtiger als Konzentration allein."
            )
        else:
            interpretation['recommendations'].append(
                f"INTERESSANT: ΔR²_H ≈ ΔR²_dir. "
                "Konzentration erklärt fast so viel wie volle Richtung!"
            )
    
    # Fall 4: ΔR²_H > 0.10
    else:
        interpretation['fall'] = 4
        interpretation['H_strength'] = 'strong'
        interpretation['H_is_significant'] = True
        interpretation['hypothesis_supported'] = True
        interpretation['conclusion'] = (
            f"ΔR²_H = {Delta_H:.4f} > {eta_strong}: "
            "Starkes Signal!"
        )
        interpretation['meaning'] = (
            "Catalan-Magic ist NICHT NUR Ω-kombinatorisch. "
            "Reagiert auf algebraisch-zahlentheoretische Verteilung der Primfaktoren. "
            "Überraschende tiefe Verbindung zwischen Spaltungsverhalten und "
            "kombinatorischer Hierarchie. "
            "WISSENSCHAFTLICH HOCHINTERESSANT, weil keine offensichtliche Verbindung "
            "zwischen mod-4/mod-3-Spaltung und Baumstrukturen existiert."
        )
        interpretation['consequence'] = (
            "Publikationswürdig! Tamari/Spektraltheorie wird relevant. "
            "Könnte auf tiefere zahlentheoretisch-kombinatorische Prinzipien hinweisen."
        )
        interpretation['recommendations'].append(
            "🎯 Hypothese H(n) → M_C(n) STARK bestätigt!"
        )
        interpretation['recommendations'].append(
            "H(n) ist zentrale Größe für Catalan-Magic."
        )
        interpretation['recommendations'].append(
            "H(n) sollte in Haupttheorie integriert werden."
        )
        interpretation['recommendations'].append(
            "Teste Hurwitz-Erweiterung (H11)."
        )
        interpretation['recommendations'].append(
            "PUBLIKATION: Ergebnis würde Catalan-Projekt stark aufwerten."
        )
    
    # Vergleiche H vs. Norm vs. Richtung
    ratio_H_vs_dir = Delta_H / Delta_dir if Delta_dir > 0 else np.inf
    
    interpretation['comparison'] = {
        'Delta_H': Delta_H,
        'Delta_norm': Delta_norm,
        'Delta_dir': Delta_dir,
        'ratio_H_vs_dir': ratio_H_vs_dir
    }
    
    if Delta_dir > 0.01:
        if ratio_H_vs_dir > 0.8:
            interpretation['recommendations'].append(
                f"KONZENTRATION dominiert: ΔR²_H / ΔR²_dir = {ratio_H_vs_dir:.2f}. "
                "Hauptinformation ist Konzentration, nicht Richtung."
            )
        elif ratio_H_vs_dir > 0.5:
            interpretation['recommendations'].append(
                f"KONZENTRATION + RICHTUNG: ΔR²_H / ΔR²_dir = {ratio_H_vs_dir:.2f}. "
                "Sowohl Konzentration als auch Richtung sind relevant."
            )
        else:
            interpretation['recommendations'].append(
                f"RICHTUNG dominiert: ΔR²_H / ΔR²_dir = {ratio_H_vs_dir:.2f}. "
                "Nicht nur Konzentration, sondern Richtung im EABC-Raum ist wichtiger."
            )
    
    # Prüfe Catalan-Residuen
    if R2_M4 > 0.95:
        interpretation['recommendations'].append(
            f"⚠️ R²(M4) = {R2_M4:.4f} > 0.95. "
            "Catalan-Magic ist fast vollständig durch SVN erklärt. "
            "Keine eigenständigen Catalan-Residuen!"
        )
    elif R2_M4 < 0.80:
        interpretation['recommendations'].append(
            f"✓ R²(M4) = {R2_M4:.4f} < 0.80. "
            "Substantielle Catalan-Residuen bleiben. "
            "Echte Catalan-Arithmetik vorhanden!"
        )
    
    return interpretation


def bootstrap_confidence_interval(
    X_lower: np.ndarray,
    X_upper: np.ndarray,
    y: np.ndarray,
    n_bootstrap: int = 1000,
    confidence: float = 0.95
) -> Tuple[float, float, np.ndarray]:
    """
    Berechnet Bootstrap-Konfidenzintervall für ΔR².
    
    Returns:
        (mean_delta, std_delta, deltas_array)
    """
    deltas = []
    
    # Entferne NaN-Werte
    mask_lower = ~np.isnan(X_lower).any(axis=1) & ~np.isnan(y)
    mask_upper = ~np.isnan(X_upper).any(axis=1) & ~np.isnan(y)
    mask = mask_lower & mask_upper
    
    X_lower_clean = X_lower[mask]
    X_upper_clean = X_upper[mask]
    y_clean = y[mask]
    
    n = len(y_clean)
    
    for _ in range(n_bootstrap):
        # Resample
        idx = np.random.choice(n, n, replace=True)
        X_lower_boot = X_lower_clean[idx]
        X_upper_boot = X_upper_clean[idx]
        y_boot = y_clean[idx]
        
        # Fitte Modelle
        model_lower = LinearRegression().fit(X_lower_boot, y_boot)
        model_upper = LinearRegression().fit(X_upper_boot, y_boot)
        
        R2_lower = r2_score(y_boot, model_lower.predict(X_lower_boot))
        R2_upper = r2_score(y_boot, model_upper.predict(X_upper_boot))
        
        deltas.append(R2_upper - R2_lower)
    
    deltas = np.array(deltas)
    
    alpha = 1 - confidence
    lower_percentile = 100 * alpha / 2
    upper_percentile = 100 * (1 - alpha / 2)
    
    ci_lower = np.percentile(deltas, lower_percentile)
    ci_upper = np.percentile(deltas, upper_percentile)
    
    return np.mean(deltas), np.std(deltas), (ci_lower, ci_upper), deltas


def visualize_results(results: Dict, features: Dict, output_dir: str):
    """
    Erstellt Visualisierungen der Ergebnisse.
    """
    print("\nErstelle Visualisierungen...")
    
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. R²-Progression über Modelle
    fig, ax = plt.subplots(figsize=(10, 6))
    
    models = ['M0', 'M0b', 'M1', 'M2', 'M3*', 'M3', 'M4']
    R2_values = [results[m]['R2'] for m in models]
    
    ax.plot(models, R2_values, 'o-', linewidth=2, markersize=10)
    ax.set_xlabel('Modell', fontsize=12)
    ax.set_ylabel('R²', fontsize=12)
    ax.set_title('Modellkaskade: Erklärte Varianz', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.set_ylim([0, 1])
    
    # Markiere kritischen Übergang M2 → M3*
    ax.axvspan(3.5, 4.5, alpha=0.2, color='red', label='ΔR²_H (kritisch)')
    ax.legend()
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'r2_progression.png'), dpi=300)
    plt.close()
    
    # 2. Δ-Werte Barplot
    fig, ax = plt.subplots(figsize=(10, 6))
    
    deltas = results['deltas']
    delta_names = list(deltas.keys())
    delta_values = list(deltas.values())
    
    colors = ['gray', 'gray', 'gray', 'red', 'orange', 'blue']
    ax.bar(delta_names, delta_values, color=colors, alpha=0.7)
    ax.set_xlabel('Δ-Typ', fontsize=12)
    ax.set_ylabel('ΔR²', fontsize=12)
    ax.set_title('Inkrementelle Erklärungskraft', fontsize=14, fontweight='bold')
    ax.axhline(y=0.01, color='k', linestyle='--', alpha=0.5, label='η_weak = 0.01')
    ax.axhline(y=0.05, color='k', linestyle='--', alpha=0.5, label='η_moderate = 0.05')
    ax.grid(True, alpha=0.3, axis='y')
    ax.legend()
    
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'delta_values.png'), dpi=300)
    plt.close()
    
    # 3. Residuen von M2 vs. H(n)
    fig, ax = plt.subplots(figsize=(10, 6))
    
    mask_M2 = results['M2']['mask']
    residuals_M2 = results['M2']['residuals']
    H_values = features['H'][mask_M2]
    
    # Entferne NaN-Werte in H
    mask_H = ~np.isnan(H_values)
    H_clean = H_values[mask_H]
    res_clean = residuals_M2[mask_H]
    
    ax.scatter(H_clean, res_clean, alpha=0.5, s=20)
    ax.set_xlabel('H(n) [Konzentration]', fontsize=12)
    ax.set_ylabel('Residuen M2', fontsize=12)
    ax.set_title('Residuen von M2 vs. H(n)', fontsize=14, fontweight='bold')
    ax.axhline(y=0, color='r', linestyle='--', alpha=0.7)
    ax.grid(True, alpha=0.3)
    
    # Korrelation
    if len(H_clean) > 1:
        corr = np.corrcoef(H_clean, res_clean)[0, 1]
        ax.text(0.05, 0.95, f'ρ = {corr:.3f}', transform=ax.transAxes,
                fontsize=12, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'residuals_M2_vs_H.png'), dpi=300)
    plt.close()
    
    # 4. Residuen von M4 (finale Catalan-Residuen)
    fig, ax = plt.subplots(figsize=(10, 6))
    
    residuals_M4 = results['M4']['residuals']
    
    ax.hist(residuals_M4, bins=50, alpha=0.7, edgecolor='black')
    ax.set_xlabel('Residuen M4', fontsize=12)
    ax.set_ylabel('Häufigkeit', fontsize=12)
    ax.set_title('Verteilung der finalen Catalan-Residuen (M4)', fontsize=14, fontweight='bold')
    ax.axvline(x=0, color='r', linestyle='--', linewidth=2)
    ax.grid(True, alpha=0.3, axis='y')
    
    # Statistiken
    mean_res = np.mean(residuals_M4)
    std_res = np.std(residuals_M4)
    ax.text(0.65, 0.95, f'μ = {mean_res:.3f}\nσ = {std_res:.3f}',
            transform=ax.transAxes, fontsize=12, verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'residuals_M4_distribution.png'), dpi=300)
    plt.close()
    
    print(f"Visualisierungen gespeichert in: {output_dir}")


def save_report(results: Dict, features: Dict, output_path: str, config: Dict):
    """
    Erstellt Markdown-Bericht mit vollständigen Ergebnissen.
    """
    print(f"\nErstelle Bericht: {output_path}")
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# Experiment E02: Modellkaskade M0-M4\n\n")
        f.write(f"**Datum:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("---\n\n")
        
        # KRITISCHE METHODISCHE KLARSTELLUNG
        f.write("## Methodische Klarstellung\n\n")
        f.write("> **WICHTIG:**\n>\n")
        f.write("> Dieser Test entscheidet **nicht** über die Gültigkeit der ")
        f.write("Gauß-Eisenstein-Interpretation des EABC-Vektors ")
        f.write("(die ist auf modularer Ebene bereits ein Satz, A-Niveau), ")
        f.write("sondern über deren **zusätzliche Erklärungskraft** für ")
        f.write("Catalan-Magic nach Kontrolle der einfacheren Kombinatorik ")
        f.write("Ω, Ω², (v₂, v₃).\n\n")
        f.write("---\n\n")
        
        # Konfiguration
        f.write("## Konfiguration\n\n")
        f.write(f"- **Datensatz:** n ∈ [{config['n_min']}, {config['n_max']}]\n")
        f.write(f"- **Anzahl Zahlen:** {len(features['numbers'])}\n")
        f.write(f"- **Ω-Filter:** Ω(n) ≥ {config['omega_min']}\n")
        f.write(f"- **Kanonisierung:** {config['canonization']}\n")
        f.write("\n")
        
        # Datensatz-Statistiken
        f.write("## Datensatz-Statistiken\n\n")
        f.write(f"| Größe | Wert |\n")
        f.write(f"|-------|------|\n")
        f.write(f"| Anzahl n | {len(features['numbers'])} |\n")
        f.write(f"| Ω(n): Mittel | {np.mean(features['omega']):.2f} |\n")
        f.write(f"| Ω(n): Range | [{np.min(features['omega'])}, {np.max(features['omega'])}] |\n")
        f.write(f"| M_C(n): Mittel | {np.mean(features['M_C']):.2f} |\n")
        f.write(f"| M_C(n): Std | {np.std(features['M_C']):.2f} |\n")
        
        # H(n) Statistiken (ohne NaN)
        H_clean = features['H'][~np.isnan(features['H'])]
        if len(H_clean) > 0:
            f.write(f"| H(n): Mittel | {np.mean(H_clean):.4f} |\n")
            f.write(f"| H(n): Range | [{np.min(H_clean):.4f}, {np.max(H_clean):.4f}] |\n")
        f.write("\n")
        
        # Modell-Ergebnisse - TABELLE 1: Modell-Hierarchie
        f.write("## Tabelle 1: Modell-Hierarchie\n\n")
        f.write("| Modell | Features | R² | ΔR² (vs. vorheriges) | RMSE | #Samples |\n")
        f.write("|--------|----------|-----|----------------------|------|----------|\n")
        
        model_features = {
            'M0': 'Ω',
            'M0b': 'Ω + Ω²',
            'M1': 'Ω + Ω² + σ',
            'M2': 'Ω + Ω² + (v₂, v₃)',
            'M3*': 'Ω + Ω² + (v₂, v₃) + H',
            'M3': 'Ω + Ω² + (v₂, v₃) + ||v||²',
            'M4': 'Ω + Ω² + (v₂, v₃) + (e,a,b,c)'
        }
        
        # Berechne schrittweise ΔR²
        deltas = results['deltas']
        model_sequence = ['M0', 'M0b', 'M1', 'M2', 'M3*', 'M3', 'M4']
        prev_R2 = 0
        
        for i, model_name in enumerate(model_sequence):
            res = results[model_name]
            current_R2 = res['R2']
            
            if i == 0:
                delta_str = "−"
            elif model_name == 'M0b':
                delta_str = f"{deltas['Delta_quad']:.4f} ← Wie stark ist Ω²?"
            elif model_name == 'M2':
                delta_str = f"{deltas['Delta_shell']:.4f}"
            elif model_name == 'M3*':
                delta_str = f"{deltas['Delta_H']:.4f} ← **ΔR²_H**"
            elif model_name == 'M4':
                # M4 folgt auf M3*, nicht M3
                delta_vs_M3_star = current_R2 - results['M3*']['R2']
                delta_str = f"{delta_vs_M3_star:.4f} ← ΔR²_dir"
            elif model_name == 'M3':
                delta_str = f"{deltas['Delta_norm']:.4f}"
            elif model_name == 'M1':
                delta_str = f"{deltas['Delta_sigma']:.4f}"
            else:
                delta_str = f"{current_R2 - prev_R2:.4f}"
            
            f.write(f"| {model_name} | {model_features[model_name]} | "
                   f"{res['R2']:.4f} | {delta_str} | "
                   f"{res['RMSE']:.2f} | {res['n_samples']} |\n")
            
            prev_R2 = current_R2
        
        f.write("\n")
        
        # Δ-Werte
        f.write("## Inkrementelle Erklärungskraft (ΔR²)\n\n")
        f.write("| Übergang | ΔR² | Interpretation |\n")
        f.write("|----------|-----|----------------|\n")
        
        deltas = results['deltas']
        
        f.write(f"| M0 → M0b | {deltas['Delta_quad']:.4f} | ")
        f.write("Quadratischer Effekt (nichtlineare Ω-Abhängigkeit) |\n")
        
        f.write(f"| M0b → M1 | {deltas['Delta_sigma']:.4f} | ")
        f.write("Teiler-Summe σ(n) |\n")
        
        f.write(f"| M0b → M2 | {deltas['Delta_shell']:.4f} | ")
        f.write("Schalen-Koordinaten (v₂, v₃) |\n")
        
        f.write(f"| **M2 → M3*** | **{deltas['Delta_H']:.4f}** | ")
        f.write("**Konzentration H(n) - KRITISCH!** |\n")
        
        f.write(f"| M2 → M3 | {deltas['Delta_norm']:.4f} | ")
        f.write("Norm ||v||² |\n")
        
        f.write(f"| M3 → M4 | {deltas['Delta_dir']:.4f} | ")
        f.write("Volle EABC-Richtung |\n")
        
        f.write("\n")
        
        # TABELLE 2: Interpretation
        interp = results['interpretation']
        f.write("## Tabelle 2: Interpretation\n\n")
        f.write("| Test | Wert | Interpretation |\n")
        f.write("|------|------|----------------|\n")
        f.write(f"| ΔR²_H | {deltas['Delta_H']:.4f} | Fall {interp['fall']}: {interp['H_strength']} |\n")
        f.write(f"| ΔR²_dir | {deltas['Delta_dir']:.4f} | Richtung vs. Konzentration |\n")
        
        ratio = interp['comparison']['ratio_H_vs_dir']
        ratio_str = f"{ratio:.3f}" if ratio < 10 else "∞"
        f.write(f"| ΔR²_H / ΔR²_dir | {ratio_str} | Relative Wichtigkeit |\n")
        f.write("\n")
        
        # Ausführliche Interpretation nach Fällen
        f.write("## Detaillierte Interpretation\n\n")
        f.write(f"### Fall {interp['fall']}: {interp['H_strength'].upper()}\n\n")
        f.write(f"**ΔR²_H = {deltas['Delta_H']:.4f}**\n\n")
        f.write(f"**Signifikant:** {'Ja' if interp['H_is_significant'] else 'Nein'}\n\n")
        f.write(f"**Hypothese gestützt:** {'Ja' if interp['hypothesis_supported'] else 'Nein'}\n\n")
        
        f.write(f"#### Befund\n\n")
        f.write(f"{interp['conclusion']}\n\n")
        
        f.write(f"#### Bedeutung\n\n")
        f.write(f"{interp['meaning']}\n\n")
        
        f.write(f"#### Konsequenz\n\n")
        f.write(f"{interp['consequence']}\n\n")
        
        f.write("#### Empfehlungen\n\n")
        for rec in interp['recommendations']:
            f.write(f"- {rec}\n")
        f.write("\n")
        
        # Methodische Hinweise
        if interp['methodological_notes']:
            f.write("#### Methodische Hinweise\n\n")
            for note in interp['methodological_notes']:
                f.write(f"{note}\n\n")
        
        # Kritische Frage
        f.write("## Kritische Frage\n\n")
        f.write("**Nach Kontrolle von Ω, Ω², (v₂, v₃): ")
        f.write("Bleibt strukturierte Varianz, die H(n) erklärt?**\n\n")
        
        if deltas['Delta_H'] > 0.01:
            f.write(f"✓ JA: ΔR²_H = {deltas['Delta_H']:.4f} > 0.01\n\n")
            f.write("Die Konzentrationsgröße H(n) hat empirisch nachweisbare ")
            f.write("Erklärungskraft für Catalan-Magic über die Baseline-Koordinaten hinaus.\n\n")
        else:
            f.write(f"✗ NEIN: ΔR²_H = {deltas['Delta_H']:.4f} ≤ 0.01\n\n")
            f.write("Die Konzentrationsgröße H(n) hat KEINE praktische ")
            f.write("Erklärungskraft. EABC-Konzentration ist für Catalan-Magic irrelevant.\n\n")
        
        # Visualisierungen
        f.write("## Visualisierungen\n\n")
        f.write("Siehe Plots im Verzeichnis `results/e02/`:\n\n")
        f.write("1. `r2_progression.png`: R²-Werte über Modellhierarchie\n")
        f.write("2. `delta_values.png`: Inkrementelle ΔR²-Beiträge\n")
        f.write("3. `residuals_M2_vs_H.png`: Residuen von M2 vs. H(n)\n")
        f.write("4. `residuals_M4_distribution.png`: Verteilung finaler Catalan-Residuen\n")
        f.write("\n")
        
        # Methodische Hinweise
        f.write("## Methodische Hinweise\n\n")
        f.write("### M0b ist essentiell\n\n")
        f.write("Ohne Ω²-Kontrolle könnte scheinbare H-Korrelation ")
        f.write("nur nichtlinearer Ω-Effekt sein.\n\n")
        
        f.write("### Interpretation der Schwellenwerte\n\n")
        f.write("- ΔR²_H < 0.01: Keine praktische Erklärungskraft\n")
        f.write("- ΔR²_H ≈ 0.01-0.05: Schwaches Signal\n")
        f.write("- ΔR²_H ≈ 0.05-0.10: Moderates Signal\n")
        f.write("- ΔR²_H > 0.10: Starkes Signal\n")
        f.write("\n")
        
        f.write("---\n\n")
        f.write("*Generiert durch `e02_model_cascade.py`*\n")
    
    print(f"Bericht gespeichert: {output_path}")


def main():
    """
    Hauptfunktion: Führt vollständiges E02-Experiment durch.
    """
    print("=" * 70)
    print("EXPERIMENT E02: MODELLKASKADE M0-M4")
    print("Testet Hypothese H(n) → M_C(n)")
    print("=" * 70)
    print()
    
    # Konfiguration
    config = {
        'n_min': 2,
        'n_max': 1000,
        'omega_min': 4,
        'canonization': 'balanced'
    }
    
    # 1. Datensatz generieren
    print("SCHRITT 1: Datensatz generieren")
    numbers = generate_dataset(
        n_min=config['n_min'],
        n_max=config['n_max'],
        omega_min=config['omega_min']
    )
    print()
    
    # 2. Features berechnen
    print("SCHRITT 2: Features berechnen")
    features = compute_features(numbers, canonization=config['canonization'])
    print()
    
    # 3. Modellkaskade durchführen
    print("SCHRITT 3: Modellkaskade M0-M4")
    results = run_model_cascade(features)
    print()
    
    # 4. Visualisierungen erstellen
    print("SCHRITT 4: Visualisierungen")
    output_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
        'experiments', 'results', 'e02'
    )
    visualize_results(results, features, output_dir)
    print()
    
    # 5. Bericht erstellen
    print("SCHRITT 5: Bericht erstellen")
    report_path = os.path.join(output_dir, 'e02_results.md')
    save_report(results, features, report_path, config)
    print()
    
    # Zusammenfassung ausgeben
    print("=" * 70)
    print("ZUSAMMENFASSUNG")
    print("=" * 70)
    print()
    print(f"Kritische Größe: ΔR²_H = {results['deltas']['Delta_H']:.4f}")
    print(f"Stärke: {results['interpretation']['H_strength']}")
    print(f"Hypothese gestützt: {results['interpretation']['hypothesis_supported']}")
    print()
    print("SCHLUSSFOLGERUNG:")
    print(results['interpretation']['conclusion'])
    print()
    print("=" * 70)
    
    return results


if __name__ == "__main__":
    results = main()
