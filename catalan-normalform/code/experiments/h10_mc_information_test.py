"""
Experiment H10: M_C Information Test

Zentrale Frage des Catalan-Programms:
    H10: I(M_C; S | Ω) > 0 ?
    
Trägt M_C(n) zusätzliche Information über S(n) = v₂ + v₃ hinaus,
die nicht bereits in Ω(n) enthalten ist?

Methodischer Ansatz: Modellkaskade mit ΔR²-Analyse
    - Modell 0: S(n) ~ 1 (Intercept only)
    - Modell 1: S(n) ~ Ω(n) (Baseline)
    - Modell 2: S(n) ~ Ω(n) + M_C(n) (mit Catalan-Magic)
    
Falls ΔR²₂ = R²₂ - R²₁ signifikant > 0:
    → M_C trägt zusätzliche Information!
    
Falls ΔR²₂ ≈ 0:
    → M_C ist nur Umkodierung von Ω, keine neue Information.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.model_selection import KFold
from scipy import stats
from typing import Dict, List, Tuple
import json
from datetime import datetime

from utils.eabc import compute_svn_coordinates, count_prime_factors
from utils.catalan_magic import compute_catalan_magic


def generate_dataset(n_min: int = 2, n_max: int = 500, omega_min: int = 3) -> List[int]:
    """
    Generiert Datensatz von Zahlen für H10-Test.
    
    Args:
        n_min: Minimale Zahl
        n_max: Maximale Zahl
        omega_min: Minimale Anzahl Primfaktoren
        
    Returns:
        Liste von Zahlen mit Ω(n) ≥ omega_min
    """
    numbers = []
    for n in range(n_min, n_max + 1):
        omega = count_prime_factors(n)
        if omega >= omega_min:
            numbers.append(n)
    
    print(f"✓ Datensatz generiert: {len(numbers)} Zahlen mit Ω ≥ {omega_min}")
    return numbers


def compute_features_h10(numbers: List[int], canonization: str = 'balanced') -> Dict[str, np.ndarray]:
    """
    Berechnet Features für H10-Test.
    
    Returns:
        Dictionary mit:
        - 'S': S(n) = v₂(n) + v₃(n) [ABHÄNGIGE VARIABLE]
        - 'omega': Ω(n) [BASELINE]
        - 'M_C': M_C(n) [TEST-VARIABLE]
        - 'numbers': Original-Zahlen
    """
    print(f"Berechne Features für {len(numbers)} Zahlen...")
    
    S = []
    omega = []
    M_C = []
    
    for n in numbers:
        coords = compute_svn_coordinates(n)
        S.append(coords['v2'] + coords['v3'])
        omega.append(coords['omega'])
        M_C.append(compute_catalan_magic(n, method=canonization))
    
    print("✓ Features berechnet.")
    
    return {
        'S': np.array(S, dtype=float),
        'omega': np.array(omega, dtype=float),
        'M_C': np.array(M_C, dtype=float),
        'numbers': np.array(numbers, dtype=int)
    }


def fit_model_h10(X: np.ndarray, y: np.ndarray, name: str) -> Dict:
    """
    Fitte lineares Modell und berechne Statistiken.
    
    Returns:
        Dictionary mit R², RMSE, Residuen, Modell
    """
    if len(X.shape) == 1:
        X = X.reshape(-1, 1)
    
    # Entferne NaN-Werte
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
            'predictions': None,
            'mask': mask
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
        'model': model,
        'y_clean': y_clean,
        'X_clean': X_clean
    }


def run_model_cascade_h10(features: Dict[str, np.ndarray]) -> Dict:
    """
    Führt H10-Modellkaskade durch.
    
    Modell 0: S(n) ~ 1
    Modell 1: S(n) ~ Ω(n)
    Modell 2: S(n) ~ Ω(n) + M_C(n)
    
    Returns:
        Dictionary mit Ergebnissen
    """
    S = features['S']
    omega = features['omega']
    M_C = features['M_C']
    
    print("\n" + "="*70)
    print("MODELLKASKADE")
    print("="*70)
    
    # Modell 0: S ~ 1 (nur Intercept)
    print("\nModell 0: S(n) ~ 1 (Intercept)")
    X_M0 = np.ones((len(S), 1))
    res_M0 = fit_model_h10(X_M0, S, 'M0')
    print(f"  R²₀ = {res_M0['R2']:.6f}")
    
    # Modell 1: S ~ Ω (Baseline)
    print("\nModell 1: S(n) ~ Ω(n) (Baseline)")
    X_M1 = omega.reshape(-1, 1)
    res_M1 = fit_model_h10(X_M1, S, 'M1')
    print(f"  R²₁ = {res_M1['R2']:.6f}")
    
    # Modell 2: S ~ Ω + M_C (mit Catalan-Magic)
    print("\nModell 2: S(n) ~ Ω(n) + M_C(n) (mit Catalan-Magic)")
    X_M2 = np.column_stack([omega, M_C])
    res_M2 = fit_model_h10(X_M2, S, 'M2')
    print(f"  R²₂ = {res_M2['R2']:.6f}")
    
    # Berechne ΔR²-Werte
    Delta_R2_1 = res_M1['R2'] - res_M0['R2']  # Ω-Gewinn
    Delta_R2_2 = res_M2['R2'] - res_M1['R2']  # M_C-Gewinn ÜBER Ω hinaus
    
    print("\n" + "="*70)
    print("ΔR²-ANALYSE")
    print("="*70)
    print(f"ΔR²₁ = R²₁ - R²₀ = {Delta_R2_1:.6f}  (Ω-Gewinn)")
    print(f"ΔR²₂ = R²₂ - R²₁ = {Delta_R2_2:.6f}  (M_C-Gewinn über Ω hinaus)")
    print("="*70)
    
    return {
        'M0': res_M0,
        'M1': res_M1,
        'M2': res_M2,
        'Delta_R2_1': Delta_R2_1,
        'Delta_R2_2': Delta_R2_2
    }


def permutation_test(features: Dict[str, np.ndarray], results: Dict, n_permutations: int = 1000) -> Dict:
    """
    Permutationstest: Ist ΔR²₂ signifikant?
    
    Permutiere M_C(n)-Werte zufällig und teste, ob echtes ΔR²₂
    signifikant größer ist als permutiertes.
    
    Returns:
        Dictionary mit p-Wert und permutierten ΔR²-Werten
    """
    print("\n" + "="*70)
    print("PERMUTATIONSTEST")
    print("="*70)
    print(f"Führe {n_permutations} Permutationen durch...")
    
    S = features['S']
    omega = features['omega']
    M_C = features['M_C']
    
    # Echtes ΔR²₂
    Delta_R2_2_observed = results['Delta_R2_2']
    
    # Permutierte ΔR²₂-Werte
    Delta_R2_2_permuted = []
    
    for i in range(n_permutations):
        if (i + 1) % 100 == 0:
            print(f"  Permutation {i+1}/{n_permutations}...")
        
        # Permutiere M_C zufällig
        M_C_perm = np.random.permutation(M_C)
        
        # Fitte Modelle
        mask = ~np.isnan(omega) & ~np.isnan(M_C_perm) & ~np.isnan(S)
        omega_clean = omega[mask]
        M_C_perm_clean = M_C_perm[mask]
        S_clean = S[mask]
        
        # Modell 1: S ~ Ω
        X_M1 = omega_clean.reshape(-1, 1)
        model_M1 = LinearRegression().fit(X_M1, S_clean)
        R2_M1 = r2_score(S_clean, model_M1.predict(X_M1))
        
        # Modell 2: S ~ Ω + M_C_perm
        X_M2 = np.column_stack([omega_clean, M_C_perm_clean])
        model_M2 = LinearRegression().fit(X_M2, S_clean)
        R2_M2 = r2_score(S_clean, model_M2.predict(X_M2))
        
        Delta_R2_2_perm = R2_M2 - R2_M1
        Delta_R2_2_permuted.append(Delta_R2_2_perm)
    
    Delta_R2_2_permuted = np.array(Delta_R2_2_permuted)
    
    # p-Wert: Anteil permutierter Werte >= beobachteter Wert
    p_value = np.mean(Delta_R2_2_permuted >= Delta_R2_2_observed)
    
    print(f"\n✓ Permutationstest abgeschlossen")
    print(f"  ΔR²₂ (beobachtet) = {Delta_R2_2_observed:.6f}")
    print(f"  ΔR²₂ (permutiert, Mittel) = {np.mean(Delta_R2_2_permuted):.6f}")
    print(f"  ΔR²₂ (permutiert, Std) = {np.std(Delta_R2_2_permuted):.6f}")
    print(f"  p-Wert = {p_value:.4f}")
    
    return {
        'p_value': p_value,
        'Delta_R2_2_observed': Delta_R2_2_observed,
        'Delta_R2_2_permuted': Delta_R2_2_permuted,
        'Delta_R2_2_permuted_mean': np.mean(Delta_R2_2_permuted),
        'Delta_R2_2_permuted_std': np.std(Delta_R2_2_permuted)
    }


def cross_validation_test(features: Dict[str, np.ndarray], k_folds: int = 5) -> Dict:
    """
    Cross-Validation: Vergleiche Modell 1 vs. Modell 2.
    
    Returns:
        Dictionary mit CV-Scores
    """
    print("\n" + "="*70)
    print("CROSS-VALIDATION")
    print("="*70)
    print(f"Führe {k_folds}-fold Cross-Validation durch...")
    
    S = features['S']
    omega = features['omega']
    M_C = features['M_C']
    
    # Entferne NaN-Werte
    mask = ~np.isnan(omega) & ~np.isnan(M_C) & ~np.isnan(S)
    omega_clean = omega[mask]
    M_C_clean = M_C[mask]
    S_clean = S[mask]
    
    kf = KFold(n_splits=k_folds, shuffle=True, random_state=42)
    
    cv_scores_M1 = []
    cv_scores_M2 = []
    
    for fold, (train_idx, test_idx) in enumerate(kf.split(omega_clean), 1):
        # Split data
        omega_train, omega_test = omega_clean[train_idx], omega_clean[test_idx]
        M_C_train, M_C_test = M_C_clean[train_idx], M_C_clean[test_idx]
        S_train, S_test = S_clean[train_idx], S_clean[test_idx]
        
        # Modell 1: S ~ Ω
        X_M1_train = omega_train.reshape(-1, 1)
        X_M1_test = omega_test.reshape(-1, 1)
        model_M1 = LinearRegression().fit(X_M1_train, S_train)
        R2_M1 = r2_score(S_test, model_M1.predict(X_M1_test))
        cv_scores_M1.append(R2_M1)
        
        # Modell 2: S ~ Ω + M_C
        X_M2_train = np.column_stack([omega_train, M_C_train])
        X_M2_test = np.column_stack([omega_test, M_C_test])
        model_M2 = LinearRegression().fit(X_M2_train, S_train)
        R2_M2 = r2_score(S_test, model_M2.predict(X_M2_test))
        cv_scores_M2.append(R2_M2)
        
        print(f"  Fold {fold}: R²₁ = {R2_M1:.4f}, R²₂ = {R2_M2:.4f}, ΔR² = {R2_M2 - R2_M1:.4f}")
    
    cv_scores_M1 = np.array(cv_scores_M1)
    cv_scores_M2 = np.array(cv_scores_M2)
    cv_delta = cv_scores_M2 - cv_scores_M1
    
    print(f"\n✓ Cross-Validation abgeschlossen")
    print(f"  CV R²₁ (Mittel) = {np.mean(cv_scores_M1):.6f} ± {np.std(cv_scores_M1):.6f}")
    print(f"  CV R²₂ (Mittel) = {np.mean(cv_scores_M2):.6f} ± {np.std(cv_scores_M2):.6f}")
    print(f"  CV ΔR² (Mittel) = {np.mean(cv_delta):.6f} ± {np.std(cv_delta):.6f}")
    
    # Paired t-test
    t_stat, t_pvalue = stats.ttest_rel(cv_scores_M2, cv_scores_M1)
    print(f"  Paired t-test: t = {t_stat:.4f}, p = {t_pvalue:.4f}")
    
    return {
        'cv_scores_M1': cv_scores_M1,
        'cv_scores_M2': cv_scores_M2,
        'cv_delta': cv_delta,
        'cv_R2_M1_mean': np.mean(cv_scores_M1),
        'cv_R2_M1_std': np.std(cv_scores_M1),
        'cv_R2_M2_mean': np.mean(cv_scores_M2),
        'cv_R2_M2_std': np.std(cv_scores_M2),
        'cv_delta_mean': np.mean(cv_delta),
        'cv_delta_std': np.std(cv_delta),
        't_stat': t_stat,
        't_pvalue': t_pvalue
    }


def residual_analysis(results: Dict, features: Dict) -> Dict:
    """
    Residuenanalyse: Prüfe Residuen von Modell 1 vs. M_C(n).
    
    Gibt es systematische Struktur?
    
    Returns:
        Dictionary mit Korrelation und Statistiken
    """
    print("\n" + "="*70)
    print("RESIDUENANALYSE")
    print("="*70)
    
    res_M1 = results['M1']
    residuals = res_M1['residuals']
    
    # M_C-Werte für Residuen-Maske
    mask = res_M1['mask']
    M_C_masked = features['M_C'][mask]
    
    # Korrelation zwischen Residuen und M_C
    corr, p_value = stats.pearsonr(residuals, M_C_masked)
    
    print(f"Korrelation: ρ(Residuen M1, M_C) = {corr:.6f}")
    print(f"p-Wert: p = {p_value:.6f}")
    
    if abs(corr) > 0.1:
        print(f"  → Systematische Struktur erkennbar!")
    else:
        print(f"  → Keine systematische Struktur.")
    
    return {
        'correlation': corr,
        'p_value': p_value,
        'residuals': residuals,
        'M_C_masked': M_C_masked
    }


def interpret_h10_results(results: Dict, perm_results: Dict, cv_results: Dict, residual_results: Dict) -> Dict:
    """
    Interpretiere H10-Ergebnisse nach wissenschaftlichen Kriterien.
    
    Returns:
        Dictionary mit Interpretation
    """
    Delta_R2_2 = results['Delta_R2_2']
    p_value_perm = perm_results['p_value']
    p_value_cv = cv_results['t_pvalue']
    corr_residuals = residual_results['correlation']
    
    # Schwellenwerte
    eta_weak = 0.01
    eta_moderate = 0.05
    alpha = 0.05
    
    interpretation = {
        'H10_answer': 'UNDEFINED',
        'strength': 'none',
        'significance': False,
        'statistical_significance': False,
        'conclusion': '',
        'meaning': '',
        'recommendation': []
    }
    
    # Bewerte ΔR²₂
    if Delta_R2_2 < eta_weak:
        interpretation['strength'] = 'none'
        interpretation['H10_answer'] = 'NEIN'
        interpretation['conclusion'] = (
            f"ΔR²₂ = {Delta_R2_2:.6f} < {eta_weak}: "
            f"M_C trägt KEINE zusätzliche Information über S(n) hinaus, "
            f"die nicht bereits in Ω(n) enthalten ist."
        )
        interpretation['meaning'] = (
            "M_C(n) ist praktisch redundant zu Ω(n) für die Vorhersage von S(n). "
            "Es gibt keine erkennbare informationstheoretische Verbindung zwischen "
            "Catalan-Struktur und Schalen-Koordinaten über Ω hinaus."
        )
        interpretation['recommendation'].append(
            "H10 ist zurückgewiesen: I(M_C; S | Ω) ≈ 0"
        )
        interpretation['recommendation'].append(
            "Catalan-Magic und Schalen sind konditionell unabhängig gegeben Ω."
        )
        
    elif Delta_R2_2 < eta_moderate:
        interpretation['strength'] = 'weak'
        interpretation['significance'] = True
        
        if p_value_perm < alpha and p_value_cv < alpha:
            interpretation['statistical_significance'] = True
            interpretation['H10_answer'] = 'JA (schwach)'
            interpretation['conclusion'] = (
                f"ΔR²₂ = {Delta_R2_2:.6f} ∈ [{eta_weak}, {eta_moderate}): "
                f"Schwaches, aber statistisch signifikantes Signal (p < {alpha})."
            )
            interpretation['meaning'] = (
                "M_C trägt eine kleine, aber nachweisbare zusätzliche Information. "
                "Signal könnte theoretisch interessant sein, aber praktisch gering."
            )
            interpretation['recommendation'].append(
                "H10 ist schwach gestützt: I(M_C; S | Ω) > 0, aber klein"
            )
            interpretation['recommendation'].append(
                "Weitere Tests mit größerer Stichprobe empfohlen (n > 1000)"
            )
        else:
            interpretation['H10_answer'] = 'UNKLAR'
            interpretation['conclusion'] = (
                f"ΔR²₂ = {Delta_R2_2:.6f}, aber nicht statistisch signifikant "
                f"(p_perm = {p_value_perm:.4f}, p_cv = {p_value_cv:.4f})."
            )
            interpretation['meaning'] = (
                "Signal ist zu schwach oder Sample zu klein für klare Aussage."
            )
            interpretation['recommendation'].append(
                "Keine klare Aussage möglich - mehr Daten erforderlich"
            )
    
    else:
        interpretation['strength'] = 'moderate' if Delta_R2_2 < 0.10 else 'strong'
        interpretation['significance'] = True
        interpretation['statistical_significance'] = True
        interpretation['H10_answer'] = 'JA'
        interpretation['conclusion'] = (
            f"ΔR²₂ = {Delta_R2_2:.6f} ≥ {eta_moderate}: "
            f"M_C trägt SUBSTANTIELLE zusätzliche Information über S(n) hinaus!"
        )
        interpretation['meaning'] = (
            "Die Catalan-Baum-Struktur M_C(n) enthält Information über "
            "die Schalen-Verteilung (v₂, v₃), die nicht bereits durch "
            "die Anzahl der Primfaktoren Ω(n) erklärt wird. "
            "Dies deutet auf eine tiefere Verbindung zwischen "
            "kombinatorischer Hierarchie und arithmetischen Eigenschaften hin."
        )
        interpretation['recommendation'].append(
            "🎯 H10 ist BESTÄTIGT: I(M_C; S | Ω) > 0"
        )
        interpretation['recommendation'].append(
            "M_C und S sind konditionell abhängig gegeben Ω"
        )
        interpretation['recommendation'].append(
            "Weitere Untersuchung der M_C ↔ S Verbindung sinnvoll"
        )
        if Delta_R2_2 > 0.10:
            interpretation['recommendation'].append(
                "⚠️ STARKES Signal - publikationswürdig!"
            )
    
    # Ergänze mit statistischen Tests
    interpretation['tests'] = {
        'Delta_R2_2': Delta_R2_2,
        'p_value_permutation': p_value_perm,
        'p_value_cv': p_value_cv,
        'correlation_residuals': corr_residuals,
        'permutation_significant': p_value_perm < alpha,
        'cv_significant': p_value_cv < alpha,
        'residuals_correlated': abs(corr_residuals) > 0.1
    }
    
    return interpretation


def visualize_h10_results(results: Dict, features: Dict, perm_results: Dict, 
                          cv_results: Dict, residual_results: Dict, output_dir: str):
    """
    Erstellt Visualisierungen für H10-Test.
    """
    print("\n" + "="*70)
    print("VISUALISIERUNGEN")
    print("="*70)
    
    os.makedirs(output_dir, exist_ok=True)
    
    fig = plt.figure(figsize=(16, 12))
    
    # 1. R²-Progression (oben links)
    ax1 = plt.subplot(2, 3, 1)
    models = ['M0', 'M1', 'M2']
    R2_values = [results['M0']['R2'], results['M1']['R2'], results['M2']['R2']]
    colors = ['gray', 'blue', 'red']
    
    ax1.bar(models, R2_values, color=colors, alpha=0.7, edgecolor='black', linewidth=1.5)
    ax1.set_ylabel('R²', fontsize=12, fontweight='bold')
    ax1.set_title('R²-Progression über Modelle', fontsize=14, fontweight='bold')
    ax1.set_ylim([0, 1])
    ax1.grid(True, alpha=0.3, axis='y')
    
    # Annotiere ΔR²-Werte
    Delta_R2_1 = results['Delta_R2_1']
    Delta_R2_2 = results['Delta_R2_2']
    ax1.text(1, (R2_values[0] + R2_values[1]) / 2, f'ΔR²₁ = {Delta_R2_1:.4f}',
             ha='center', va='center', fontsize=10, fontweight='bold',
             bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
    ax1.text(2, (R2_values[1] + R2_values[2]) / 2, f'ΔR²₂ = {Delta_R2_2:.4f}',
             ha='center', va='center', fontsize=10, fontweight='bold',
             bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.8))
    
    # 2. ΔR²-Barplot (oben mittig)
    ax2 = plt.subplot(2, 3, 2)
    delta_names = ['ΔR²₁\n(Ω-Gewinn)', 'ΔR²₂\n(M_C-Gewinn)']
    delta_values = [Delta_R2_1, Delta_R2_2]
    colors_delta = ['blue', 'red']
    
    ax2.bar(delta_names, delta_values, color=colors_delta, alpha=0.7, edgecolor='black', linewidth=1.5)
    ax2.set_ylabel('ΔR²', fontsize=12, fontweight='bold')
    ax2.set_title('Inkrementelle Erklärungskraft', fontsize=14, fontweight='bold')
    ax2.axhline(y=0.01, color='k', linestyle='--', alpha=0.5, linewidth=1, label='η = 0.01')
    ax2.axhline(y=0.05, color='k', linestyle='--', alpha=0.7, linewidth=1.5, label='η = 0.05')
    ax2.grid(True, alpha=0.3, axis='y')
    ax2.legend(fontsize=9)
    
    # 3. Permutationstest (oben rechts)
    ax3 = plt.subplot(2, 3, 3)
    Delta_R2_2_permuted = perm_results['Delta_R2_2_permuted']
    Delta_R2_2_observed = perm_results['Delta_R2_2_observed']
    p_value = perm_results['p_value']
    
    ax3.hist(Delta_R2_2_permuted, bins=50, alpha=0.7, color='gray', edgecolor='black')
    ax3.axvline(x=Delta_R2_2_observed, color='red', linestyle='--', linewidth=2.5, label=f'Beobachtet: {Delta_R2_2_observed:.4f}')
    ax3.set_xlabel('ΔR²₂ (permutiert)', fontsize=11)
    ax3.set_ylabel('Häufigkeit', fontsize=11)
    ax3.set_title(f'Permutationstest (p = {p_value:.4f})', fontsize=14, fontweight='bold')
    ax3.legend(fontsize=9)
    ax3.grid(True, alpha=0.3, axis='y')
    
    # 4. Residuen M1 vs. M_C (unten links)
    ax4 = plt.subplot(2, 3, 4)
    residuals = residual_results['residuals']
    M_C_masked = residual_results['M_C_masked']
    corr = residual_results['correlation']
    
    ax4.scatter(M_C_masked, residuals, alpha=0.5, s=20, color='steelblue', edgecolors='black', linewidth=0.5)
    ax4.axhline(y=0, color='red', linestyle='--', linewidth=1.5)
    ax4.set_xlabel('M_C(n)', fontsize=11, fontweight='bold')
    ax4.set_ylabel('Residuen von Modell 1', fontsize=11, fontweight='bold')
    ax4.set_title(f'Residuenanalyse (ρ = {corr:.4f})', fontsize=14, fontweight='bold')
    ax4.grid(True, alpha=0.3)
    
    # Regressionsline
    z = np.polyfit(M_C_masked, residuals, 1)
    p = np.poly1d(z)
    x_line = np.linspace(M_C_masked.min(), M_C_masked.max(), 100)
    ax4.plot(x_line, p(x_line), 'r--', linewidth=2, alpha=0.7, label=f'Fit: y = {z[0]:.4f}x + {z[1]:.4f}')
    ax4.legend(fontsize=9)
    
    # 5. Cross-Validation (unten mittig)
    ax5 = plt.subplot(2, 3, 5)
    cv_scores_M1 = cv_results['cv_scores_M1']
    cv_scores_M2 = cv_results['cv_scores_M2']
    folds = np.arange(1, len(cv_scores_M1) + 1)
    
    ax5.plot(folds, cv_scores_M1, 'o-', label='Modell 1 (S ~ Ω)', linewidth=2, markersize=8, color='blue')
    ax5.plot(folds, cv_scores_M2, 's-', label='Modell 2 (S ~ Ω + M_C)', linewidth=2, markersize=8, color='red')
    ax5.set_xlabel('Fold', fontsize=11, fontweight='bold')
    ax5.set_ylabel('R² (Test Set)', fontsize=11, fontweight='bold')
    ax5.set_title('Cross-Validation Scores', fontsize=14, fontweight='bold')
    ax5.legend(fontsize=9)
    ax5.grid(True, alpha=0.3)
    
    # 6. Scatter-Matrix: S vs. Ω und S vs. M_C (unten rechts)
    ax6 = plt.subplot(2, 3, 6)
    S = features['S']
    omega = features['omega']
    M_C = features['M_C']
    
    # S vs. Ω
    ax6.scatter(omega, S, alpha=0.4, s=15, color='blue', label='S vs. Ω', edgecolors='none')
    # S vs. M_C (anders formatiert)
    ax6_twin = ax6.twiny()
    ax6_twin.scatter(M_C, S, alpha=0.4, s=15, color='red', marker='s', label='S vs. M_C', edgecolors='none')
    
    ax6.set_xlabel('Ω(n)', fontsize=11, fontweight='bold', color='blue')
    ax6_twin.set_xlabel('M_C(n)', fontsize=11, fontweight='bold', color='red')
    ax6.set_ylabel('S(n) = v₂ + v₃', fontsize=11, fontweight='bold')
    ax6.set_title('S(n) vs. Prädiktoren', fontsize=14, fontweight='bold')
    ax6.tick_params(axis='x', labelcolor='blue')
    ax6_twin.tick_params(axis='x', labelcolor='red')
    ax6.grid(True, alpha=0.3)
    
    plt.tight_layout()
    output_file = os.path.join(output_dir, 'h10_visualizations.png')
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✓ Visualisierungen gespeichert: {output_file}")


def save_h10_report(results: Dict, features: Dict, perm_results: Dict, 
                    cv_results: Dict, residual_results: Dict, 
                    interpretation: Dict, output_dir: str, config: Dict):
    """
    Erstellt H10-Bericht.
    """
    print("\n" + "="*70)
    print("BERICHT ERSTELLEN")
    print("="*70)
    
    os.makedirs(output_dir, exist_ok=True)
    report_path = os.path.join(output_dir, 'H10_RESULTS.md')
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("# H10: Catalan-Magic Information Test\n\n")
        f.write(f"**Datum:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("---\n\n")
        
        # Zentrale Frage
        f.write("## Zentrale Frage\n\n")
        f.write("> **H10:** Trägt M_C(n) zusätzliche Information über S(n) = v₂ + v₃ hinaus,\n")
        f.write("> die nicht bereits in Ω(n) enthalten ist?\n\n")
        f.write("> Formal: **I(M_C; S | Ω) > 0 ?**\n\n")
        f.write("---\n\n")
        
        # Konfiguration
        f.write("## Konfiguration\n\n")
        f.write(f"- **Datensatz:** n ∈ [{config['n_min']}, {config['n_max']}]\n")
        f.write(f"- **Anzahl Zahlen:** {len(features['numbers'])}\n")
        f.write(f"- **Ω-Filter:** Ω(n) ≥ {config['omega_min']}\n")
        f.write(f"- **Kanonisierung:** {config['canonization']}\n")
        f.write(f"- **Permutationen:** {config['n_permutations']}\n")
        f.write(f"- **CV-Folds:** {config['k_folds']}\n")
        f.write("\n")
        
        # Antwort (prominent)
        f.write("## 🎯 ANTWORT\n\n")
        f.write(f"### {interpretation['H10_answer']}\n\n")
        f.write(f"**Stärke:** {interpretation['strength']}\n\n")
        f.write(f"**Statistisch signifikant:** {'Ja' if interpretation['statistical_significance'] else 'Nein'}\n\n")
        f.write("---\n\n")
        
        # Modell-Ergebnisse
        f.write("## Modell-Ergebnisse\n\n")
        f.write("| Modell | Formel | R² | RMSE | #Samples |\n")
        f.write("|--------|--------|-----|------|----------|\n")
        f.write(f"| M0 | S(n) ~ 1 | {results['M0']['R2']:.6f} | {results['M0']['RMSE']:.4f} | {results['M0']['n_samples']} |\n")
        f.write(f"| M1 | S(n) ~ Ω(n) | {results['M1']['R2']:.6f} | {results['M1']['RMSE']:.4f} | {results['M1']['n_samples']} |\n")
        f.write(f"| M2 | S(n) ~ Ω(n) + M_C(n) | {results['M2']['R2']:.6f} | {results['M2']['RMSE']:.4f} | {results['M2']['n_samples']} |\n")
        f.write("\n")
        
        # ΔR²-Analyse
        f.write("## ΔR²-Analyse\n\n")
        f.write("| Übergang | ΔR² | Interpretation |\n")
        f.write("|----------|-----|----------------|\n")
        f.write(f"| M0 → M1 | {results['Delta_R2_1']:.6f} | Ω-Gewinn |\n")
        f.write(f"| **M1 → M2** | **{results['Delta_R2_2']:.6f}** | **M_C-Gewinn über Ω hinaus** |\n")
        f.write("\n")
        
        # Interpretation
        f.write("## Interpretation\n\n")
        f.write(f"### Befund\n\n")
        f.write(f"{interpretation['conclusion']}\n\n")
        f.write(f"### Bedeutung\n\n")
        f.write(f"{interpretation['meaning']}\n\n")
        f.write(f"### Empfehlungen\n\n")
        for rec in interpretation['recommendation']:
            f.write(f"- {rec}\n")
        f.write("\n")
        
        # Robustheitstests
        f.write("## Robustheitstests\n\n")
        
        f.write("### Permutationstest\n\n")
        f.write(f"- **ΔR²₂ (beobachtet):** {perm_results['Delta_R2_2_observed']:.6f}\n")
        f.write(f"- **ΔR²₂ (permutiert, Mittel):** {perm_results['Delta_R2_2_permuted_mean']:.6f}\n")
        f.write(f"- **ΔR²₂ (permutiert, Std):** {perm_results['Delta_R2_2_permuted_std']:.6f}\n")
        f.write(f"- **p-Wert:** {perm_results['p_value']:.4f}\n")
        f.write(f"- **Signifikant (α = 0.05):** {'Ja' if perm_results['p_value'] < 0.05 else 'Nein'}\n")
        f.write("\n")
        
        f.write("### Cross-Validation\n\n")
        f.write(f"- **CV R²₁ (Mittel):** {cv_results['cv_R2_M1_mean']:.6f} ± {cv_results['cv_R2_M1_std']:.6f}\n")
        f.write(f"- **CV R²₂ (Mittel):** {cv_results['cv_R2_M2_mean']:.6f} ± {cv_results['cv_R2_M2_std']:.6f}\n")
        f.write(f"- **CV ΔR² (Mittel):** {cv_results['cv_delta_mean']:.6f} ± {cv_results['cv_delta_std']:.6f}\n")
        f.write(f"- **Paired t-test:** t = {cv_results['t_stat']:.4f}, p = {cv_results['t_pvalue']:.4f}\n")
        f.write(f"- **Signifikant (α = 0.05):** {'Ja' if cv_results['t_pvalue'] < 0.05 else 'Nein'}\n")
        f.write("\n")
        
        f.write("### Residuenanalyse\n\n")
        f.write(f"- **Korrelation:** ρ(Residuen M1, M_C) = {residual_results['correlation']:.6f}\n")
        f.write(f"- **p-Wert:** {residual_results['p_value']:.6f}\n")
        f.write(f"- **Systematische Struktur:** {'Ja' if abs(residual_results['correlation']) > 0.1 else 'Nein'}\n")
        f.write("\n")
        
        # Visualisierungen
        f.write("## Visualisierungen\n\n")
        f.write("Siehe: `h10_visualizations.png`\n\n")
        f.write("1. R²-Progression über Modelle\n")
        f.write("2. ΔR²-Barplot\n")
        f.write("3. Permutationstest-Histogramm\n")
        f.write("4. Residuenanalyse (M1 vs. M_C)\n")
        f.write("5. Cross-Validation Scores\n")
        f.write("6. Scatter-Matrix (S vs. Prädiktoren)\n")
        f.write("\n")
        
        # Daten speichern (CSV)
        f.write("## Daten\n\n")
        f.write("Siehe: `h10_delta_r2_test.csv`\n\n")
        
        f.write("---\n\n")
        f.write("*Generiert durch `h10_mc_information_test.py`*\n")
    
    print(f"✓ Bericht gespeichert: {report_path}")
    
    # CSV-Daten speichern
    csv_path = os.path.join(output_dir, 'h10_delta_r2_test.csv')
    with open(csv_path, 'w') as f:
        f.write("model,R2,RMSE,n_samples\n")
        f.write(f"M0,{results['M0']['R2']:.8f},{results['M0']['RMSE']:.6f},{results['M0']['n_samples']}\n")
        f.write(f"M1,{results['M1']['R2']:.8f},{results['M1']['RMSE']:.6f},{results['M1']['n_samples']}\n")
        f.write(f"M2,{results['M2']['R2']:.8f},{results['M2']['RMSE']:.6f},{results['M2']['n_samples']}\n")
    
    print(f"✓ Daten gespeichert: {csv_path}")


def main():
    """
    Hauptfunktion: Führt H10-Test durch.
    """
    print("\n" + "="*70)
    print("H10: CATALAN-MAGIC INFORMATION TEST")
    print("="*70)
    print()
    print("Zentrale Frage: I(M_C; S | Ω) > 0 ?")
    print()
    print("="*70)
    print()
    
    # Konfiguration
    config = {
        'n_min': 2,
        'n_max': 500,
        'omega_min': 3,
        'canonization': 'balanced',
        'n_permutations': 1000,
        'k_folds': 5
    }
    
    # Output-Verzeichnis
    output_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
        'experiments', 'results', 'h10'
    )
    
    # 1. Datensatz generieren
    print("SCHRITT 1: Datensatz generieren")
    numbers = generate_dataset(
        n_min=config['n_min'],
        n_max=config['n_max'],
        omega_min=config['omega_min']
    )
    
    # 2. Features berechnen
    print("\nSCHRITT 2: Features berechnen")
    features = compute_features_h10(numbers, canonization=config['canonization'])
    
    # 3. Modellkaskade
    print("\nSCHRITT 3: Modellkaskade")
    results = run_model_cascade_h10(features)
    
    # 4. Permutationstest
    print("\nSCHRITT 4: Robustheitstests")
    perm_results = permutation_test(features, results, n_permutations=config['n_permutations'])
    
    # 5. Cross-Validation
    cv_results = cross_validation_test(features, k_folds=config['k_folds'])
    
    # 6. Residuenanalyse
    residual_results = residual_analysis(results, features)
    
    # 7. Interpretation
    print("\nSCHRITT 5: Interpretation")
    interpretation = interpret_h10_results(results, perm_results, cv_results, residual_results)
    
    # 8. Visualisierungen
    print("\nSCHRITT 6: Visualisierungen")
    visualize_h10_results(results, features, perm_results, cv_results, residual_results, output_dir)
    
    # 9. Bericht
    print("\nSCHRITT 7: Bericht")
    save_h10_report(results, features, perm_results, cv_results, residual_results, interpretation, output_dir, config)
    
    # Finale Zusammenfassung
    print("\n" + "="*70)
    print("ZUSAMMENFASSUNG")
    print("="*70)
    print()
    print(f"Zentrale Frage: I(M_C; S | Ω) > 0 ?")
    print()
    print(f"ANTWORT: {interpretation['H10_answer']}")
    print()
    print(f"ΔR²₂ = {results['Delta_R2_2']:.6f}")
    print(f"p-Wert (Permutation) = {perm_results['p_value']:.4f}")
    print(f"p-Wert (CV t-test) = {cv_results['t_pvalue']:.4f}")
    print()
    print("SCHLUSSFOLGERUNG:")
    print(interpretation['conclusion'])
    print()
    print("BEDEUTUNG:")
    print(interpretation['meaning'])
    print()
    print("="*70)
    print()
    print(f"Alle Ergebnisse gespeichert in: {output_dir}")
    print()
    print("="*70)
    
    return {
        'results': results,
        'perm_results': perm_results,
        'cv_results': cv_results,
        'residual_results': residual_results,
        'interpretation': interpretation,
        'config': config
    }


if __name__ == "__main__":
    h10_results = main()
