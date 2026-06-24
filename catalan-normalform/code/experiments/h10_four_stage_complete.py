"""
H10 Four-Stage Testing Program
================================

ZENTRALE FRAGE: "Welche Information bleibt übrig, nachdem Ω(n) entfernt wurde?"

Dies ist KEINE Regressionsfrage, sondern eine INFORMATIONSFRAGE.
Der ΔR²-Test ist nur das erste Messinstrument.

Stages:
    H10-A: Wie stark erklärt Ω bereits alles?
    H10-B: Residuen-Test (KRITISCH)
    H10-C: Permutations-Test der EABC-Arithmetik (MÖGLICHERWEISE WICHTIGER ALS ΔR²)
    H10-D: Skalierungstest (n → 10^6)

Autor: H10 Testing Framework
Datum: 2026-06-24
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from scipy import stats
from typing import Dict, List, Tuple
import json
from datetime import datetime
import pandas as pd

from utils.eabc import (
    compute_svn_coordinates, 
    count_prime_factors,
    prime_factors_with_multiplicity,
    eabc_class
)
from utils.catalan_magic import compute_catalan_magic


# ============================================================================
# STAGE H10-A: WIE STARK ERKLÄRT Ω BEREITS ALLES?
# ============================================================================

def stage_A_omega_baseline(features: Dict[str, np.ndarray]) -> Dict:
    """
    Stage H10-A: Bestimme, wie viel von M_C und S bereits durch Ω erklärt wird.
    
    Fitte:
        M_C(n) ~ Ω(n)
        S(n) ~ Ω(n)
    
    Berechne:
        R²(M_C, Ω)
        R²(S, Ω)
    
    Interpretation:
        R² > 0.95: Fast reine Ω-Codierung
        0.7 < R² < 0.95: Teilweise neue Struktur
        R² < 0.7: Deutlich eigenständige Struktur
    """
    print("\n" + "="*80)
    print("STAGE H10-A: WIE STARK ERKLÄRT Ω BEREITS ALLES?")
    print("="*80)
    
    S = features['S']
    omega = features['omega']
    M_C = features['M_C']
    
    # Entferne NaN-Werte
    mask_S = ~np.isnan(omega) & ~np.isnan(S)
    mask_MC = ~np.isnan(omega) & ~np.isnan(M_C)
    
    # Modell 1: M_C ~ Ω
    X_omega_MC = omega[mask_MC].reshape(-1, 1)
    y_MC = M_C[mask_MC]
    
    model_MC_Omega = LinearRegression().fit(X_omega_MC, y_MC)
    y_MC_pred = model_MC_Omega.predict(X_omega_MC)
    R2_MC_Omega = r2_score(y_MC, y_MC_pred)
    
    # Modell 2: S ~ Ω
    X_omega_S = omega[mask_S].reshape(-1, 1)
    y_S = S[mask_S]
    
    model_S_Omega = LinearRegression().fit(X_omega_S, y_S)
    y_S_pred = model_S_Omega.predict(X_omega_S)
    R2_S_Omega = r2_score(y_S, y_S_pred)
    
    print(f"\n1. M_C(n) ~ Ω(n):")
    print(f"   R²(M_C, Ω) = {R2_MC_Omega:.6f}")
    print(f"   Koeffizienten: β = {model_MC_Omega.coef_[0]:.4f}, α = {model_MC_Omega.intercept_:.4f}")
    
    print(f"\n2. S(n) ~ Ω(n):")
    print(f"   R²(S, Ω) = {R2_S_Omega:.6f}")
    print(f"   Koeffizienten: β = {model_S_Omega.coef_[0]:.4f}, α = {model_S_Omega.intercept_:.4f}")
    
    # Interpretation
    print(f"\n3. Interpretation:")
    if R2_MC_Omega > 0.95:
        print(f"   M_C: FAST REINE Ω-CODIERUNG (R² > 0.95)")
    elif R2_MC_Omega > 0.7:
        print(f"   M_C: Teilweise neue Struktur (0.7 < R² < 0.95)")
    else:
        print(f"   M_C: DEUTLICH EIGENSTÄNDIGE STRUKTUR (R² < 0.7)")
    
    if R2_S_Omega > 0.95:
        print(f"   S: Fast reine Ω-Codierung (R² > 0.95)")
    elif R2_S_Omega > 0.7:
        print(f"   S: Teilweise neue Struktur (0.7 < R² < 0.95)")
    else:
        print(f"   S: Deutlich eigenständige Struktur (R² < 0.7)")
    
    return {
        'R2_MC_Omega': R2_MC_Omega,
        'R2_S_Omega': R2_S_Omega,
        'model_MC_Omega': model_MC_Omega,
        'model_S_Omega': model_S_Omega,
        'MC_pred': y_MC_pred,
        'S_pred': y_S_pred,
        'mask_MC': mask_MC,
        'mask_S': mask_S
    }


# ============================================================================
# STAGE H10-B: RESIDUEN-TEST (THE MOST IMPORTANT STEP)
# ============================================================================

def stage_B_residual_test(features: Dict[str, np.ndarray], stage_A_results: Dict) -> Dict:
    """
    Stage H10-B: Residuen-Test nach Entfernung von Ω.
    
    Berechne:
        M_C^⊥ = M_C - M̂_C(Ω)
        S^⊥ = S - Ŝ(Ω)
    
    Teste:
        corr(M_C^⊥, S^⊥)
    
    WARUM DIES WICHTIG IST:
        Ω ist jetzt komplett entfernt. Wenn Struktur übrig bleibt,
        wird es interessant.
    """
    print("\n" + "="*80)
    print("STAGE H10-B: RESIDUEN-TEST (KRITISCH)")
    print("="*80)
    
    S = features['S']
    M_C = features['M_C']
    omega = features['omega']
    
    # Berechne Residuen
    mask = ~np.isnan(omega) & ~np.isnan(M_C) & ~np.isnan(S)
    
    omega_clean = omega[mask].reshape(-1, 1)
    M_C_clean = M_C[mask]
    S_clean = S[mask]
    
    # M_C^⊥ = M_C - M̂_C(Ω)
    model_MC_Omega = LinearRegression().fit(omega_clean, M_C_clean)
    MC_pred = model_MC_Omega.predict(omega_clean)
    MC_residuals = M_C_clean - MC_pred
    
    # S^⊥ = S - Ŝ(Ω)
    model_S_Omega = LinearRegression().fit(omega_clean, S_clean)
    S_pred = model_S_Omega.predict(omega_clean)
    S_residuals = S_clean - S_pred
    
    # Korrelation der Residuen
    corr_residuals, p_value_residuals = stats.pearsonr(MC_residuals, S_residuals)
    
    print(f"\n1. Residuen berechnet:")
    print(f"   M_C^⊥ (Std): {np.std(MC_residuals):.4f}")
    print(f"   S^⊥ (Std): {np.std(S_residuals):.4f}")
    
    print(f"\n2. Korrelation nach Ω-Entfernung:")
    print(f"   corr(M_C^⊥, S^⊥) = {corr_residuals:.6f}")
    print(f"   p-Wert = {p_value_residuals:.6f}")
    
    print(f"\n3. Interpretation:")
    if abs(corr_residuals) > 0.1 and p_value_residuals < 0.05:
        print(f"   ✓ SIGNIFIKANTE RESIDUEN-KORRELATION")
        print(f"   → Nach Ω-Entfernung bleibt Struktur übrig!")
    elif abs(corr_residuals) > 0.05:
        print(f"   ~ Schwache Residuen-Korrelation")
    else:
        print(f"   ✗ Keine Residuen-Korrelation")
        print(f"   → M_C und S sind konditionell unabhängig gegeben Ω")
    
    return {
        'MC_residuals': MC_residuals,
        'S_residuals': S_residuals,
        'corr_residuals': corr_residuals,
        'p_value_residuals': p_value_residuals,
        'mask': mask
    }


# ============================================================================
# STAGE H10-C: PERMUTATIONS-TEST (POSSIBLY MORE IMPORTANT THAN ΔR²)
# ============================================================================

def permute_eabc_labels(n: int, permutation_type: str = 'random') -> int:
    """
    Permutiert EABC-Labels einer Zahl.
    
    Args:
        n: Zahl
        permutation_type: 
            'random': Vollständige zufällige Permutation
            'pairwise': Paarweise Vertauschung (E↔A, A↔B, B↔C)
            'cyclic': Zyklische Permutation (E→A→B→C→E)
    
    Returns:
        Neue "Zahl" mit permutierten EABC-Labels
        (technisch: Abbildung der Primfaktoren)
    """
    factors = prime_factors_with_multiplicity(n)
    
    # Definiere Permutation
    if permutation_type == 'random':
        # Vollständige zufällige Permutation
        perm_map = {
            'E': np.random.choice(['E', 'A', 'B', 'C']),
            'A': np.random.choice(['E', 'A', 'B', 'C']),
            'B': np.random.choice(['E', 'A', 'B', 'C']),
            'C': np.random.choice(['E', 'A', 'B', 'C'])
        }
    elif permutation_type == 'pairwise':
        # E↔A, B↔C
        perm_map = {'E': 'A', 'A': 'E', 'B': 'C', 'C': 'B'}
    elif permutation_type == 'cyclic':
        # E→A→B→C→E
        perm_map = {'E': 'A', 'A': 'B', 'B': 'C', 'C': 'E'}
    else:
        raise ValueError(f"Unbekannter Permutationstyp: {permutation_type}")
    
    # Definiere Repräsentanten für jede Klasse
    # (kleinste Primzahl in jeder Klasse)
    class_representatives = {
        'E': 13,   # 13 ≡ 1 (mod 12)
        'A': 5,    # 5 ≡ 5 (mod 12)
        'B': 7,    # 7 ≡ 7 (mod 12)
        'C': 11,   # 11 ≡ 11 (mod 12)
        'shell': [2, 3]
    }
    
    # Permutiere Faktoren
    permuted_factors = []
    for p in factors:
        cls = eabc_class(p)
        if cls == 'shell':
            # 2 und 3 bleiben unverändert
            permuted_factors.append(p)
        else:
            # Permutiere EABC-Klasse
            new_cls = perm_map.get(cls, cls)
            permuted_factors.append(class_representatives[new_cls])
    
    # Berechne neue "Zahl" (Produkt der permutierten Faktoren)
    n_perm = np.prod(permuted_factors)
    return n_perm


def stage_C_permutation_test(features: Dict[str, np.ndarray], 
                             n_permutations: int = 1000,
                             canonization: str = 'balanced') -> Dict:
    """
    Stage H10-C: Permutations-Test der EABC-Arithmetik.
    
    TEST OB DIE STRUKTUR VON DER SPEZIFISCHEN EABC-ZUORDNUNG ABHÄNGT:
    
    1. Nimm dieselben Zahlen
    2. Permutiere EABC-Labels (E↔A, A↔B, etc.)
    3. Wiederhole n_permutations Mal
    4. Berechne M_C^perm für jede Permutation
    5. Berechne Z-Score: Z = (M_C - M_C^perm) / σ(M_C^perm)
    
    Interpretation:
        Z ≈ 0: Catalan-Struktur kommt hauptsächlich von Baum-Architektur
        Z ≫ 2: Catalan-Struktur hängt TATSÄCHLICH von EABC-Arithmetik ab
    
    DAS IST DER JACKPOT-TEST!
    """
    print("\n" + "="*80)
    print("STAGE H10-C: PERMUTATIONS-TEST DER EABC-ARITHMETIK")
    print("="*80)
    print(f"\nFühre {n_permutations} EABC-Permutationen durch...")
    
    numbers = features['numbers']
    M_C_observed = features['M_C']
    
    # Sammle M_C-Werte für permutierte EABC-Labels
    M_C_permuted_all = []
    
    for i in range(n_permutations):
        if (i + 1) % 100 == 0:
            print(f"  Permutation {i+1}/{n_permutations}...")
        
        M_C_perm = []
        for n in numbers:
            # Permutiere EABC-Labels
            n_perm = permute_eabc_labels(int(n), permutation_type='random')
            
            # Berechne M_C für permutierte Zahl
            try:
                mc_val = compute_catalan_magic(int(n_perm), method=canonization)
                M_C_perm.append(mc_val)
            except:
                M_C_perm.append(np.nan)
        
        M_C_permuted_all.append(M_C_perm)
    
    M_C_permuted_all = np.array(M_C_permuted_all)
    
    # Berechne Statistiken
    M_C_perm_mean = np.nanmean(M_C_permuted_all, axis=0)
    M_C_perm_std = np.nanstd(M_C_permuted_all, axis=0)
    
    # Z-Scores für jede Zahl
    Z_scores = (M_C_observed - M_C_perm_mean) / (M_C_perm_std + 1e-10)
    Z_scores = Z_scores[~np.isnan(Z_scores)]
    
    # Globaler Z-Score
    Z_global = np.mean(Z_scores)
    Z_std = np.std(Z_scores)
    
    print(f"\n1. Permutations-Statistiken:")
    print(f"   M_C (beobachtet, Mittel): {np.nanmean(M_C_observed):.4f}")
    print(f"   M_C (permutiert, Mittel): {np.nanmean(M_C_perm_mean):.4f}")
    print(f"   M_C (permutiert, Std): {np.nanmean(M_C_perm_std):.4f}")
    
    print(f"\n2. Z-Score-Analyse:")
    print(f"   Z (global) = {Z_global:.4f} ± {Z_std:.4f}")
    print(f"   Z (Median) = {np.median(Z_scores):.4f}")
    print(f"   Z (Max) = {np.max(Z_scores):.4f}")
    print(f"   Z (Min) = {np.min(Z_scores):.4f}")
    
    print(f"\n3. Interpretation:")
    if abs(Z_global) < 0.5:
        print(f"   Z ≈ 0: Catalan-Struktur kommt HAUPTSÄCHLICH von Baum-Architektur")
        print(f"   → EABC-Arithmetik spielt KEINE wesentliche Rolle")
        verdict = "GEOMETRIC_ONLY"
    elif abs(Z_global) < 2.0:
        print(f"   0.5 < |Z| < 2: Schwaches EABC-Signal")
        print(f"   → Grenzfall, mehr Daten benötigt")
        verdict = "UNCLEAR"
    else:
        print(f"   |Z| ≫ 2: STARKES EABC-Signal!")
        print(f"   → Catalan-Struktur hängt TATSÄCHLICH von EABC-Arithmetik ab!")
        print(f"   → 🎯 JACKPOT: Erste starke Evidenz für EABC-Catalan-Verbindung!")
        verdict = "EABC_DEPENDENT"
    
    return {
        'M_C_permuted_all': M_C_permuted_all,
        'M_C_perm_mean': M_C_perm_mean,
        'M_C_perm_std': M_C_perm_std,
        'Z_scores': Z_scores,
        'Z_global': Z_global,
        'Z_std': Z_std,
        'verdict': verdict,
        'n_permutations': n_permutations
    }


# ============================================================================
# STAGE H10-D: SKALIERUNGSTEST
# ============================================================================

def stage_D_scaling_test(n_min: int, n_max: int, omega_min: int = 3,
                         canonization: str = 'balanced',
                         sample_size: int = None) -> Dict:
    """
    Stage H10-D: Skalierungstest.
    
    NICHT BEI n ≤ 100 STOPPEN!
    
    Minimum: 10^4
    Besser: 10^5
    Ideal: 10^6
    
    WARUM?
        Aktuelle H(n)-Plots werden von p^k und sehr kurzen Faktorisierungen dominiert.
        Nur für große n: Ω(n) ≈ log log n und Klassen-Mischung wird viel interessanter.
    """
    print("\n" + "="*80)
    print("STAGE H10-D: SKALIERUNGSTEST")
    print("="*80)
    print(f"\nBereich: n ∈ [{n_min}, {n_max}]")
    print(f"Ω-Filter: Ω(n) ≥ {omega_min}")
    
    # Sammle Zahlen
    print(f"\nSammle Zahlen...")
    numbers = []
    for n in range(n_min, min(n_max + 1, 100000)):  # Limitiere für erste Tests
        omega = count_prime_factors(n)
        if omega >= omega_min:
            numbers.append(n)
            if sample_size and len(numbers) >= sample_size:
                break
    
    print(f"✓ {len(numbers)} Zahlen gesammelt")
    
    # Berechne Features
    print(f"\nBerechne Features...")
    S = []
    omega_vals = []
    M_C = []
    
    for i, n in enumerate(numbers):
        if (i + 1) % 1000 == 0:
            print(f"  {i+1}/{len(numbers)}...")
        
        coords = compute_svn_coordinates(n)
        S.append(coords['v2'] + coords['v3'])
        omega_vals.append(coords['omega'])
        M_C.append(compute_catalan_magic(n, method=canonization))
    
    features = {
        'S': np.array(S),
        'omega': np.array(omega_vals),
        'M_C': np.array(M_C),
        'numbers': np.array(numbers)
    }
    
    print(f"✓ Features berechnet")
    
    # Führe Stage A und B durch (schnell)
    stage_A = stage_A_omega_baseline(features)
    stage_B = stage_B_residual_test(features, stage_A)
    
    return {
        'n_min': n_min,
        'n_max': n_max,
        'n_samples': len(numbers),
        'features': features,
        'stage_A': stage_A,
        'stage_B': stage_B
    }


# ============================================================================
# VISUALISIERUNGEN
# ============================================================================

def visualize_four_stage_results(stage_A: Dict, stage_B: Dict, 
                                 stage_C: Dict, features: Dict,
                                 output_dir: str):
    """
    Erstellt umfassende Visualisierungen für alle vier Stages.
    """
    print("\n" + "="*80)
    print("VISUALISIERUNGEN")
    print("="*80)
    
    os.makedirs(output_dir, exist_ok=True)
    
    fig = plt.figure(figsize=(20, 15))
    
    # ========== STAGE A: Ω-Baseline ==========
    
    # Plot 1: M_C vs Ω
    ax1 = plt.subplot(3, 4, 1)
    mask_MC = stage_A['mask_MC']
    omega = features['omega'][mask_MC]
    M_C = features['M_C'][mask_MC]
    MC_pred = stage_A['MC_pred']
    
    ax1.scatter(omega, M_C, alpha=0.3, s=10, color='steelblue', label='Daten')
    ax1.plot(omega, MC_pred, 'r-', linewidth=2, label=f'Fit (R² = {stage_A["R2_MC_Omega"]:.3f})')
    ax1.set_xlabel('Ω(n)', fontsize=11, fontweight='bold')
    ax1.set_ylabel('M_C(n)', fontsize=11, fontweight='bold')
    ax1.set_title('STAGE A: M_C ~ Ω', fontsize=12, fontweight='bold')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: S vs Ω
    ax2 = plt.subplot(3, 4, 2)
    mask_S = stage_A['mask_S']
    omega_S = features['omega'][mask_S]
    S = features['S'][mask_S]
    S_pred = stage_A['S_pred']
    
    ax2.scatter(omega_S, S, alpha=0.3, s=10, color='green', label='Daten')
    ax2.plot(omega_S, S_pred, 'r-', linewidth=2, label=f'Fit (R² = {stage_A["R2_S_Omega"]:.3f})')
    ax2.set_xlabel('Ω(n)', fontsize=11, fontweight='bold')
    ax2.set_ylabel('S(n) = v₂ + v₃', fontsize=11, fontweight='bold')
    ax2.set_title('STAGE A: S ~ Ω', fontsize=12, fontweight='bold')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # ========== STAGE B: Residuen ==========
    
    # Plot 3: Residuen-Korrelation
    ax3 = plt.subplot(3, 4, 3)
    MC_res = stage_B['MC_residuals']
    S_res = stage_B['S_residuals']
    corr = stage_B['corr_residuals']
    
    ax3.scatter(MC_res, S_res, alpha=0.4, s=15, color='purple')
    ax3.axhline(y=0, color='k', linestyle='--', linewidth=1, alpha=0.5)
    ax3.axvline(x=0, color='k', linestyle='--', linewidth=1, alpha=0.5)
    
    # Regressionslinie
    z = np.polyfit(MC_res, S_res, 1)
    p = np.poly1d(z)
    x_line = np.linspace(MC_res.min(), MC_res.max(), 100)
    ax3.plot(x_line, p(x_line), 'r-', linewidth=2, alpha=0.7)
    
    ax3.set_xlabel('M_C^⊥ (Residuen)', fontsize=11, fontweight='bold')
    ax3.set_ylabel('S^⊥ (Residuen)', fontsize=11, fontweight='bold')
    ax3.set_title(f'STAGE B: Residuen-Korrelation (ρ = {corr:.4f})', fontsize=12, fontweight='bold')
    ax3.grid(True, alpha=0.3)
    
    # Plot 4: Residuen-Verteilungen
    ax4 = plt.subplot(3, 4, 4)
    ax4.hist(MC_res, bins=50, alpha=0.5, color='blue', label='M_C^⊥', density=True)
    ax4.hist(S_res, bins=50, alpha=0.5, color='green', label='S^⊥', density=True)
    ax4.set_xlabel('Residuum', fontsize=11)
    ax4.set_ylabel('Dichte', fontsize=11)
    ax4.set_title('Residuen-Verteilungen', fontsize=12, fontweight='bold')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    
    # ========== STAGE C: EABC-Permutationen ==========
    
    # Plot 5: Z-Score-Verteilung
    ax5 = plt.subplot(3, 4, 5)
    Z_scores = stage_C['Z_scores']
    Z_global = stage_C['Z_global']
    
    ax5.hist(Z_scores, bins=50, alpha=0.7, color='orange', edgecolor='black')
    ax5.axvline(x=Z_global, color='red', linestyle='--', linewidth=2.5, 
                label=f'Mittel: {Z_global:.3f}')
    ax5.axvline(x=0, color='black', linestyle='-', linewidth=1, alpha=0.5)
    ax5.axvline(x=2, color='green', linestyle='--', linewidth=1.5, alpha=0.7, label='Z = 2')
    ax5.axvline(x=-2, color='green', linestyle='--', linewidth=1.5, alpha=0.7)
    ax5.set_xlabel('Z-Score', fontsize=11, fontweight='bold')
    ax5.set_ylabel('Häufigkeit', fontsize=11)
    ax5.set_title(f'STAGE C: Z-Score-Verteilung ({stage_C["n_permutations"]} perm.)', 
                  fontsize=12, fontweight='bold')
    ax5.legend()
    ax5.grid(True, alpha=0.3)
    
    # Plot 6: M_C beobachtet vs. permutiert
    ax6 = plt.subplot(3, 4, 6)
    M_C_obs = features['M_C']
    M_C_perm_mean = stage_C['M_C_perm_mean']
    
    valid_mask = ~np.isnan(M_C_obs) & ~np.isnan(M_C_perm_mean)
    ax6.scatter(M_C_obs[valid_mask], M_C_perm_mean[valid_mask], 
                alpha=0.4, s=15, color='darkorange')
    
    # Diagonale
    min_val = min(M_C_obs[valid_mask].min(), M_C_perm_mean[valid_mask].min())
    max_val = max(M_C_obs[valid_mask].max(), M_C_perm_mean[valid_mask].max())
    ax6.plot([min_val, max_val], [min_val, max_val], 'k--', linewidth=2, alpha=0.7, label='Diagonale')
    
    ax6.set_xlabel('M_C (beobachtet)', fontsize=11, fontweight='bold')
    ax6.set_ylabel('M_C (permutiert, Mittel)', fontsize=11, fontweight='bold')
    ax6.set_title('STAGE C: M_C beobachtet vs. permutiert', fontsize=12, fontweight='bold')
    ax6.legend()
    ax6.grid(True, alpha=0.3)
    
    # Plot 7: M_C^⊥ vs S^⊥ (detailliert)
    ax7 = plt.subplot(3, 4, 7)
    ax7.hexbin(MC_res, S_res, gridsize=30, cmap='YlOrRd', mincnt=1)
    ax7.axhline(y=0, color='white', linestyle='--', linewidth=2, alpha=0.8)
    ax7.axvline(x=0, color='white', linestyle='--', linewidth=2, alpha=0.8)
    ax7.set_xlabel('M_C^⊥', fontsize=11, fontweight='bold')
    ax7.set_ylabel('S^⊥', fontsize=11, fontweight='bold')
    ax7.set_title(f'Residuen-Hexbin (ρ = {corr:.4f})', fontsize=12, fontweight='bold')
    
    # Plot 8: Z-Score vs Ω
    ax8 = plt.subplot(3, 4, 8)
    omega_all = features['omega']
    Z_expanded = np.full_like(omega_all, np.nan)
    Z_expanded[~np.isnan(M_C_obs)] = Z_scores[:len(omega_all[~np.isnan(M_C_obs)])]
    
    valid_z = ~np.isnan(Z_expanded) & ~np.isnan(omega_all)
    ax8.scatter(omega_all[valid_z], Z_expanded[valid_z], alpha=0.4, s=15, color='teal')
    ax8.axhline(y=0, color='black', linestyle='-', linewidth=1, alpha=0.5)
    ax8.axhline(y=2, color='green', linestyle='--', linewidth=1.5, alpha=0.7)
    ax8.axhline(y=-2, color='green', linestyle='--', linewidth=1.5, alpha=0.7)
    ax8.set_xlabel('Ω(n)', fontsize=11, fontweight='bold')
    ax8.set_ylabel('Z-Score', fontsize=11, fontweight='bold')
    ax8.set_title('Z-Score vs. Ω(n)', fontsize=12, fontweight='bold')
    ax8.grid(True, alpha=0.3)
    
    # ========== ZUSAMMENFASSUNG ==========
    
    # Plot 9-12: Zusammenfassungs-Panels
    ax9 = plt.subplot(3, 4, 9)
    ax9.axis('off')
    summary_text = f"""
STAGE A: Ω-BASELINE
━━━━━━━━━━━━━━━━━━━━
R²(M_C, Ω) = {stage_A['R2_MC_Omega']:.4f}
R²(S, Ω) = {stage_A['R2_S_Omega']:.4f}

Interpretation:
"""
    if stage_A['R2_MC_Omega'] > 0.95:
        summary_text += "M_C ≈ reine Ω-Codierung"
    elif stage_A['R2_MC_Omega'] > 0.7:
        summary_text += "M_C: teilweise neue Struktur"
    else:
        summary_text += "M_C: eigenständige Struktur"
    
    ax9.text(0.1, 0.5, summary_text, fontsize=10, family='monospace',
             verticalalignment='center')
    
    ax10 = plt.subplot(3, 4, 10)
    ax10.axis('off')
    summary_text_B = f"""
STAGE B: RESIDUEN
━━━━━━━━━━━━━━━━━━━━
corr(M_C^⊥, S^⊥) = {stage_B['corr_residuals']:.4f}
p-Wert = {stage_B['p_value_residuals']:.6f}

Interpretation:
"""
    if abs(stage_B['corr_residuals']) > 0.1 and stage_B['p_value_residuals'] < 0.05:
        summary_text_B += "✓ SIGNIFIKANTE Struktur\nnach Ω-Entfernung!"
    else:
        summary_text_B += "✗ Keine signifikante\nResiduenstruktur"
    
    ax10.text(0.1, 0.5, summary_text_B, fontsize=10, family='monospace',
              verticalalignment='center')
    
    ax11 = plt.subplot(3, 4, 11)
    ax11.axis('off')
    summary_text_C = f"""
STAGE C: EABC-PERMUTATION
━━━━━━━━━━━━━━━━━━━━━━━━━━
Z (global) = {stage_C['Z_global']:.4f}
Verdict: {stage_C['verdict']}

Interpretation:
"""
    if stage_C['verdict'] == 'EABC_DEPENDENT':
        summary_text_C += "🎯 JACKPOT!\nCatalan hängt von\nEABC-Arithmetik ab!"
    elif stage_C['verdict'] == 'UNCLEAR':
        summary_text_C += "~ Grenzfall\nMehr Daten benötigt"
    else:
        summary_text_C += "✗ Nur geometrische\nStruktur"
    
    ax11.text(0.1, 0.5, summary_text_C, fontsize=10, family='monospace',
              verticalalignment='center')
    
    ax12 = plt.subplot(3, 4, 12)
    ax12.axis('off')
    ax12.text(0.5, 0.5, f"n = {len(features['numbers'])}\nSamples", 
              fontsize=20, fontweight='bold',
              ha='center', va='center')
    ax12.text(0.5, 0.2, datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
              fontsize=10, ha='center', va='center', style='italic')
    
    plt.tight_layout()
    output_file = os.path.join(output_dir, 'h10_four_stage_complete.png')
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✓ Visualisierung gespeichert: {output_file}")


# ============================================================================
# BERICHT
# ============================================================================

def generate_comprehensive_report(stage_A: Dict, stage_B: Dict, stage_C: Dict,
                                  features: Dict, config: Dict, output_dir: str):
    """
    Generiert umfassenden H10-Bericht für alle vier Stages.
    """
    print("\n" + "="*80)
    print("GENERIERE UMFASSENDEN BERICHT")
    print("="*80)
    
    os.makedirs(output_dir, exist_ok=True)
    report_path = os.path.join(output_dir, 'H10_FOUR_STAGE_REPORT.md')
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("# H10 FOUR-STAGE TESTING PROGRAM\n\n")
        f.write(f"**Datum:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("---\n\n")
        
        # Zentrale Frage
        f.write("## ZENTRALE FRAGE\n\n")
        f.write("> **\"Welche Information bleibt übrig, nachdem Ω(n) entfernt wurde?\"**\n\n")
        f.write("> H10 ist KEINE Regressionsfrage. Es ist eine INFORMATIONSFRAGE.\n")
        f.write("> Der ΔR²-Test ist nur das erste Messinstrument.\n\n")
        f.write("---\n\n")
        
        # Konfiguration
        f.write("## KONFIGURATION\n\n")
        f.write(f"- **Datensatz:** n ∈ [{config['n_min']}, {config['n_max']}]\n")
        f.write(f"- **Anzahl Zahlen:** {len(features['numbers'])}\n")
        f.write(f"- **Ω-Filter:** Ω(n) ≥ {config['omega_min']}\n")
        f.write(f"- **Kanonisierung:** {config['canonization']}\n")
        f.write(f"- **Permutationen:** {config['n_permutations']}\n\n")
        f.write("---\n\n")
        
        # STAGE A
        f.write("## STAGE H10-A: WIE STARK ERKLÄRT Ω BEREITS ALLES?\n\n")
        f.write("### Ergebnisse\n\n")
        f.write("| Modell | R² | Interpretation |\n")
        f.write("|--------|----|----------------|\n")
        f.write(f"| M_C ~ Ω | {stage_A['R2_MC_Omega']:.6f} | ")
        if stage_A['R2_MC_Omega'] > 0.95:
            f.write("Fast reine Ω-Codierung |\n")
        elif stage_A['R2_MC_Omega'] > 0.7:
            f.write("Teilweise neue Struktur |\n")
        else:
            f.write("Deutlich eigenständige Struktur |\n")
        
        f.write(f"| S ~ Ω | {stage_A['R2_S_Omega']:.6f} | ")
        if stage_A['R2_S_Omega'] > 0.95:
            f.write("Fast reine Ω-Codierung |\n")
        elif stage_A['R2_S_Omega'] > 0.7:
            f.write("Teilweise neue Struktur |\n")
        else:
            f.write("Deutlich eigenständige Struktur |\n")
        
        f.write("\n### Interpretation\n\n")
        f.write(f"- R²(M_C, Ω) = {stage_A['R2_MC_Omega']:.4f}: ")
        if stage_A['R2_MC_Omega'] > 0.95:
            f.write("M_C ist fast vollständig durch Ω determiniert. **Wenig Hoffnung für neue Information.**\n")
        elif stage_A['R2_MC_Omega'] > 0.7:
            f.write("M_C wird teilweise durch Ω erklärt, aber es bleibt Raum für eigenständige Struktur.\n")
        else:
            f.write("M_C hat deutlich eigenständige Struktur über Ω hinaus. **Vielversprechend!**\n")
        
        f.write(f"- R²(S, Ω) = {stage_A['R2_S_Omega']:.4f}: Schalen sind stark an Ω gekoppelt.\n")
        f.write("\n---\n\n")
        
        # STAGE B
        f.write("## STAGE H10-B: RESIDUEN-TEST (KRITISCH)\n\n")
        f.write("### Ergebnisse\n\n")
        f.write(f"- **corr(M_C^⊥, S^⊥) = {stage_B['corr_residuals']:.6f}**\n")
        f.write(f"- **p-Wert = {stage_B['p_value_residuals']:.6f}**\n\n")
        
        f.write("### Interpretation\n\n")
        if abs(stage_B['corr_residuals']) > 0.1 and stage_B['p_value_residuals'] < 0.05:
            f.write("✓ **SIGNIFIKANTE RESIDUEN-KORRELATION**\n\n")
            f.write("Nach Ω-Entfernung bleibt **systematische Struktur** zwischen M_C und S übrig!\n\n")
            f.write("Dies ist das erste starke Signal, dass M_C zusätzliche Information trägt.\n")
        elif abs(stage_B['corr_residuals']) > 0.05:
            f.write("~ **Schwache Residuen-Korrelation**\n\n")
            f.write("Ein schwaches Signal ist vorhanden, aber nicht statistisch robust.\n")
        else:
            f.write("✗ **Keine Residuen-Korrelation**\n\n")
            f.write("M_C und S sind **konditionell unabhängig gegeben Ω**.\n\n")
            f.write("M_C trägt keine zusätzliche Information über S hinaus.\n")
        
        f.write("\n---\n\n")
        
        # STAGE C
        f.write("## STAGE H10-C: EABC-PERMUTATIONS-TEST (DER JACKPOT-TEST)\n\n")
        f.write("### Ergebnisse\n\n")
        f.write(f"- **Z (global) = {stage_C['Z_global']:.4f} ± {stage_C['Z_std']:.4f}**\n")
        f.write(f"- **Z (Median) = {np.median(stage_C['Z_scores']):.4f}**\n")
        f.write(f"- **Permutationen:** {stage_C['n_permutations']}\n")
        f.write(f"- **Verdict:** {stage_C['verdict']}\n\n")
        
        f.write("### Interpretation\n\n")
        if stage_C['verdict'] == 'EABC_DEPENDENT':
            f.write("🎯 **JACKPOT!**\n\n")
            f.write("**Die Catalan-Struktur hängt TATSÄCHLICH von der EABC-Arithmetik ab!**\n\n")
            f.write(f"Mit Z = {stage_C['Z_global']:.2f} ≫ 2 ist das Signal statistisch robust.\n\n")
            f.write("**Dies ist die erste starke Evidenz, dass die Catalan-Verzweigung mehr ist ")
            f.write("als eine sophistizierte Reparametrisierung von Ω(n).**\n\n")
            f.write("**EMPFEHLUNG:** Publikationswürdig! Weitere Untersuchung der EABC-Catalan-Verbindung dringend empfohlen.\n")
        elif stage_C['verdict'] == 'UNCLEAR':
            f.write("~ **Grenzfall**\n\n")
            f.write(f"Mit Z = {stage_C['Z_global']:.2f} liegt das Signal im Grenzbereich.\n\n")
            f.write("**EMPFEHLUNG:** Mehr Daten sammeln (n > 10^5) für klarere Aussage.\n")
        else:
            f.write("✗ **Nur geometrische Struktur**\n\n")
            f.write(f"Mit Z ≈ {stage_C['Z_global']:.2f} zeigt sich kein EABC-Effekt.\n\n")
            f.write("Die Catalan-Struktur kommt hauptsächlich von der **Baum-Architektur**, ")
            f.write("nicht von der spezifischen EABC-Arithmetik.\n\n")
            f.write("**EMPFEHLUNG:** M_C ist wahrscheinlich nur eine komplexe Umkodierung von Ω.\n")
        
        f.write("\n---\n\n")
        
        # STAGE D
        f.write("## STAGE H10-D: SKALIERUNGSTEST\n\n")
        f.write(f"- **Aktueller Bereich:** n ∈ [{config['n_min']}, {config['n_max']}]\n")
        f.write(f"- **Samples:** {len(features['numbers'])}\n\n")
        
        if config['n_max'] < 10000:
            f.write("⚠️ **WARNUNG:** Sample-Größe noch zu klein!\n\n")
            f.write("**EMPFEHLUNG:**\n")
            f.write("- Minimum: n_max = 10^4\n")
            f.write("- Besser: n_max = 10^5\n")
            f.write("- Ideal: n_max = 10^6\n\n")
            f.write("Nur für große n wird Ω(n) ≈ log log n und Klassen-Mischung interessant.\n")
        else:
            f.write("✓ Sample-Größe ist ausreichend für robuste Aussagen.\n")
        
        f.write("\n---\n\n")
        
        # FINALE ANTWORT
        f.write("## 🎯 FINALE ANTWORT AUF H10\n\n")
        f.write("> **\"Welche Information bleibt übrig, nachdem Ω(n) entfernt wurde?\"**\n\n")
        
        # Entscheidungsbaum
        if stage_C['verdict'] == 'EABC_DEPENDENT':
            if abs(stage_B['corr_residuals']) > 0.1:
                grade = "A"
                answer = "**JA - STARKE EVIDENZ**"
                explanation = (
                    "M_C trägt **signifikante zusätzliche Information** über S, die nicht in Ω enthalten ist. "
                    "Zudem hängt diese Information **nachweislich von der EABC-Arithmetik** ab. "
                    "Dies ist ein **publikationswürdiges Ergebnis**!"
                )
            else:
                grade = "B+"
                answer = "**JA - EABC-ABHÄNGIG, ABER SCHWACH**"
                explanation = (
                    "Die EABC-Arithmetik zeigt einen starken Einfluss auf M_C, aber die Residuen-Korrelation "
                    "ist schwach. Möglicherweise ist die Verbindung M_C ↔ S weniger direkt als erwartet."
                )
        elif abs(stage_B['corr_residuals']) > 0.1 and stage_B['p_value_residuals'] < 0.05:
            if stage_C['verdict'] == 'UNCLEAR':
                grade = "B"
                answer = "**JA - ABER HERKUNFT UNKLAR**"
                explanation = (
                    "M_C trägt zusätzliche Information nach Ω-Entfernung, aber es ist unklar, "
                    "ob diese von EABC-Arithmetik oder nur von der Baum-Geometrie stammt. "
                    "Mehr Daten benötigt."
                )
            else:
                grade = "C"
                answer = "**SCHWACH - NUR GEOMETRISCH**"
                explanation = (
                    "M_C trägt etwas Information, aber diese stammt hauptsächlich von der Baum-Geometrie, "
                    "nicht von der EABC-Arithmetik. Praktisch eine Umkodierung von Ω."
                )
        else:
            grade = "D"
            answer = "**NEIN - KEINE ZUSÄTZLICHE INFORMATION**"
            explanation = (
                "M_C ist praktisch redundant zu Ω für die Vorhersage von S. "
                "Es gibt keine erkennbare informationstheoretische Verbindung zwischen "
                "Catalan-Struktur und Schalen-Koordinaten über Ω hinaus."
            )
        
        f.write(f"### EVIDENZ-GRAD: **{grade}**\n\n")
        f.write(f"### ANTWORT: {answer}\n\n")
        f.write(f"{explanation}\n\n")
        
        f.write("---\n\n")
        f.write("## ZUSAMMENFASSUNG DER EVIDENZ\n\n")
        f.write("| Stage | Metrik | Wert | Status |\n")
        f.write("|-------|--------|------|--------|\n")
        f.write(f"| A: Ω-Baseline | R²(M_C, Ω) | {stage_A['R2_MC_Omega']:.4f} | ")
        f.write("✓\n" if stage_A['R2_MC_Omega'] < 0.95 else "○\n")
        f.write(f"| B: Residuen | corr(M_C^⊥, S^⊥) | {stage_B['corr_residuals']:.4f} | ")
        f.write("✓\n" if abs(stage_B['corr_residuals']) > 0.1 else "✗\n")
        f.write(f"| C: EABC-Perm | Z (global) | {stage_C['Z_global']:.4f} | ")
        f.write("🎯\n" if stage_C['verdict'] == 'EABC_DEPENDENT' else ("○\n" if stage_C['verdict'] == 'UNCLEAR' else "✗\n"))
        f.write(f"| D: Skalierung | n_samples | {len(features['numbers'])} | ")
        f.write("✓\n" if len(features['numbers']) > 10000 else "⚠️\n")
        f.write("\n")
        
        f.write("**Legende:**\n")
        f.write("- 🎯 = Jackpot-Ergebnis\n")
        f.write("- ✓ = Positives Signal\n")
        f.write("- ○ = Grenzfall\n")
        f.write("- ✗ = Negatives Signal\n")
        f.write("- ⚠️ = Warnung\n")
        f.write("\n---\n\n")
        
        f.write("*Generiert durch h10_four_stage_complete.py*\n")
    
    print(f"✓ Bericht gespeichert: {report_path}")
    
    # CSV-Export
    csv_path = os.path.join(output_dir, 'h10_four_stage_results.csv')
    results_df = pd.DataFrame({
        'stage': ['A', 'A', 'B', 'C'],
        'metric': ['R2_MC_Omega', 'R2_S_Omega', 'corr_residuals', 'Z_global'],
        'value': [
            stage_A['R2_MC_Omega'],
            stage_A['R2_S_Omega'],
            stage_B['corr_residuals'],
            stage_C['Z_global']
        ]
    })
    results_df.to_csv(csv_path, index=False)
    print(f"✓ CSV gespeichert: {csv_path}")


# ============================================================================
# HAUPTFUNKTION
# ============================================================================

def main(n_min: int = 2, n_max: int = 1000, omega_min: int = 3,
         canonization: str = 'balanced', n_permutations: int = 1000,
         sample_size: int = None):
    """
    Führt das vollständige H10 Four-Stage Testing Program durch.
    """
    print("\n" + "="*80)
    print("H10 FOUR-STAGE TESTING PROGRAM")
    print("="*80)
    print()
    print("ZENTRALE FRAGE: \"Welche Information bleibt übrig, nachdem Ω(n) entfernt wurde?\"")
    print()
    print("="*80)
    print()
    
    config = {
        'n_min': n_min,
        'n_max': n_max,
        'omega_min': omega_min,
        'canonization': canonization,
        'n_permutations': n_permutations
    }
    
    output_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
        'experiments', 'results', 'h10_four_stage'
    )
    os.makedirs(output_dir, exist_ok=True)
    
    # Sammle Daten
    print(f"SCHRITT 1: Datensatz generieren (n ∈ [{n_min}, {n_max}], Ω ≥ {omega_min})...")
    numbers = []
    for n in range(n_min, n_max + 1):
        omega = count_prime_factors(n)
        if omega >= omega_min:
            numbers.append(n)
            if sample_size and len(numbers) >= sample_size:
                break
    
    print(f"✓ {len(numbers)} Zahlen gesammelt")
    
    # Berechne Features
    print(f"\nSCHRITT 2: Features berechnen...")
    S = []
    omega_vals = []
    M_C = []
    
    for i, n in enumerate(numbers):
        if (i + 1) % 500 == 0:
            print(f"  {i+1}/{len(numbers)}...")
        
        coords = compute_svn_coordinates(n)
        S.append(coords['v2'] + coords['v3'])
        omega_vals.append(coords['omega'])
        M_C.append(compute_catalan_magic(n, method=canonization))
    
    features = {
        'S': np.array(S),
        'omega': np.array(omega_vals),
        'M_C': np.array(M_C),
        'numbers': np.array(numbers)
    }
    
    print(f"✓ Features berechnet")
    
    # STAGE A
    print(f"\nSCHRITT 3: Stage H10-A")
    stage_A = stage_A_omega_baseline(features)
    
    # STAGE B
    print(f"\nSCHRITT 4: Stage H10-B")
    stage_B = stage_B_residual_test(features, stage_A)
    
    # STAGE C
    print(f"\nSCHRITT 5: Stage H10-C")
    stage_C = stage_C_permutation_test(features, n_permutations=n_permutations,
                                       canonization=canonization)
    
    # Visualisierungen
    print(f"\nSCHRITT 6: Visualisierungen")
    visualize_four_stage_results(stage_A, stage_B, stage_C, features, output_dir)
    
    # Bericht
    print(f"\nSCHRITT 7: Umfassender Bericht")
    generate_comprehensive_report(stage_A, stage_B, stage_C, features, config, output_dir)
    
    # Finale Zusammenfassung
    print("\n" + "="*80)
    print("FINALE ZUSAMMENFASSUNG")
    print("="*80)
    print()
    print("ZENTRALE FRAGE: \"Welche Information bleibt übrig, nachdem Ω(n) entfernt wurde?\"")
    print()
    print(f"Datensatz: {len(numbers)} Zahlen, n ∈ [{n_min}, {n_max}]")
    print()
    print("ERGEBNISSE:")
    print(f"  Stage A: R²(M_C, Ω) = {stage_A['R2_MC_Omega']:.4f}")
    print(f"  Stage B: corr(M_C^⊥, S^⊥) = {stage_B['corr_residuals']:.4f}")
    print(f"  Stage C: Z = {stage_C['Z_global']:.4f} → {stage_C['verdict']}")
    print()
    print("="*80)
    print(f"\nAlle Ergebnisse gespeichert in: {output_dir}")
    print()
    
    return {
        'stage_A': stage_A,
        'stage_B': stage_B,
        'stage_C': stage_C,
        'features': features,
        'config': config
    }


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='H10 Four-Stage Testing Program')
    parser.add_argument('--n_min', type=int, default=2, help='Minimale Zahl')
    parser.add_argument('--n_max', type=int, default=1000, help='Maximale Zahl')
    parser.add_argument('--omega_min', type=int, default=3, help='Minimale Anzahl Primfaktoren')
    parser.add_argument('--canonization', type=str, default='balanced', help='Kanonisierung')
    parser.add_argument('--n_permutations', type=int, default=1000, help='Anzahl Permutationen')
    parser.add_argument('--sample_size', type=int, default=None, help='Sample-Größe (optional)')
    
    args = parser.parse_args()
    
    results = main(
        n_min=args.n_min,
        n_max=args.n_max,
        omega_min=args.omega_min,
        canonization=args.canonization,
        n_permutations=args.n_permutations,
        sample_size=args.sample_size
    )
