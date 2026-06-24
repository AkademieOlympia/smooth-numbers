"""
H10 Four-Stage Testing Program V2 - CORRECTED
==============================================

KORREKTUR VON STAGE C:

Das ursprüngliche Problem:
- M_C hängt NICHT von EABC ab (es misst nur Baum-Asymmetrie)
- S = v₂ + v₃ hängt NICHT von EABC ab (nur 2- und 3-adische Bewertung)
- Daher kann die Beziehung M_C ↔ S nicht von EABC abhängen!

KORRIGIERTE STAGE C:

Teste stattdessen, ob M_C mit **EABC-abhängigen Features** korreliert:
1. H(n) = Konzentrationsmessung der EABC-Verteilung
2. Ω_EABC = e + a + b + c (Anzahl der EABC-Faktoren)
3. EABC-Vektor-Normen

Dann permutiere die EABC-Labels und teste, ob diese Korrelationen
von der spezifischen EABC-Arithmetik abhängen.
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
    eabc_class,
    compute_H,
    compute_eabc_vector
)
from utils.catalan_magic import compute_catalan_magic

# Import Stage A und B vom Original
import h10_four_stage_complete as h10_original


# ============================================================================
# STAGE H10-C V2: KORRIGIERTER EABC-PERMUTATIONS-TEST
# ============================================================================

def compute_eabc_features(n: int) -> Dict:
    """
    Berechnet EABC-abhängige Features für Zahl n.
    
    Returns:
        - H: Konzentrationsmessung
        - omega_eabc: Anzahl EABC-Faktoren
        - eabc_norm: ||EABC-Vektor||
        - eabc_balance: Entropie-ähnliches Maß
    """
    coords = compute_svn_coordinates(n)
    v_eabc = coords['v_fac']  # [e, a, b, c]
    omega_eabc = np.sum(v_eabc)
    
    H_val = coords['H']
    eabc_norm = np.linalg.norm(v_eabc)
    
    # Balance: Wie gleichmäßig sind die EABC-Faktoren verteilt?
    if omega_eabc > 0:
        p = v_eabc / omega_eabc  # Wahrscheinlichkeiten
        p = p[p > 0]  # Entferne Nullen
        eabc_balance = -np.sum(p * np.log(p + 1e-10))  # Shannon-Entropie
    else:
        eabc_balance = np.nan
    
    return {
        'H': H_val,
        'omega_eabc': omega_eabc,
        'eabc_norm': eabc_norm,
        'eabc_balance': eabc_balance,
        'e': coords['e'],
        'a': coords['a'],
        'b': coords['b'],
        'c': coords['c']
    }


def permute_eabc_assignment(factors: List[int], perm_map: Dict[str, str]) -> List[int]:
    """
    Permutiert EABC-Zuordnung von Primfaktoren.
    
    WICHTIG: Behält die EXAKTE Faktorstruktur, ändert nur die EABC-Klassen.
    
    Args:
        factors: Liste von Primfaktoren
        perm_map: Permutations-Mapping (z.B. {'E': 'A', 'A': 'E', ...})
    
    Returns:
        Liste von permutierten Faktoren (mit neuen EABC-Klassen)
    """
    # Repräsentanten für jede Klasse (kleinste Primzahl)
    representatives = {
        'E': 13,   # 13 ≡ 1 (mod 12)
        'A': 5,    # 5 ≡ 5 (mod 12)
        'B': 7,    # 7 ≡ 7 (mod 12)
        'C': 11    # 11 ≡ 11 (mod 12)
    }
    
    permuted = []
    for p in factors:
        cls = eabc_class(p)
        if cls == 'shell':
            # 2 und 3 bleiben unverändert
            permuted.append(p)
        else:
            # Permutiere EABC-Klasse
            new_cls = perm_map.get(cls, cls)
            permuted.append(representatives[new_cls])
    
    return permuted


def stage_C_v2_eabc_permutation(features: Dict[str, np.ndarray],
                                n_permutations: int = 1000) -> Dict:
    """
    Stage H10-C V2: Korrigierter EABC-Permutations-Test.
    
    TESTE OB M_C MIT EABC-FEATURES KORRELIERT UND OB DIESE KORRELATION
    VON DER SPEZIFISCHEN EABC-ZUORDNUNG ABHÄNGT.
    
    Vorgehen:
    1. Berechne EABC-Features (H, Ω_EABC, etc.)
    2. Berechne Korrelationen: corr(M_C, H), corr(M_C, Ω_EABC), etc.
    3. Permutiere EABC-Labels
    4. Berechne permutierte EABC-Features
    5. Berechne permutierte Korrelationen
    6. Teste Signifikanz mit Z-Score
    
    Interpretation:
        Z ≈ 0: Korrelationen sind unabhängig von EABC-Zuordnung
        Z ≫ 2: Korrelationen hängen von spezifischer EABC-Arithmetik ab
    """
    print("\n" + "="*80)
    print("STAGE H10-C V2: KORRIGIERTER EABC-PERMUTATIONS-TEST")
    print("="*80)
    print(f"\nFühre {n_permutations} EABC-Permutationen durch...")
    
    numbers = features['numbers']
    M_C_observed = features['M_C']
    
    # 1. Berechne EABC-Features für alle Zahlen
    print("\n1. Berechne EABC-Features...")
    H_vals = []
    omega_eabc_vals = []
    eabc_norm_vals = []
    eabc_balance_vals = []
    
    for n in numbers:
        eabc_feats = compute_eabc_features(int(n))
        H_vals.append(eabc_feats['H'])
        omega_eabc_vals.append(eabc_feats['omega_eabc'])
        eabc_norm_vals.append(eabc_feats['eabc_norm'])
        eabc_balance_vals.append(eabc_feats['eabc_balance'])
    
    H_vals = np.array(H_vals)
    omega_eabc_vals = np.array(omega_eabc_vals)
    eabc_norm_vals = np.array(eabc_norm_vals)
    eabc_balance_vals = np.array(eabc_balance_vals)
    
    # 2. Berechne beobachtete Korrelationen
    print("\n2. Berechne beobachtete Korrelationen...")
    
    # Entferne NaN-Werte für Korrelationen
    mask_H = ~np.isnan(M_C_observed) & ~np.isnan(H_vals)
    mask_omega = ~np.isnan(M_C_observed) & ~np.isnan(omega_eabc_vals)
    mask_norm = ~np.isnan(M_C_observed) & ~np.isnan(eabc_norm_vals)
    mask_balance = ~np.isnan(M_C_observed) & ~np.isnan(eabc_balance_vals)
    
    corr_MC_H_obs = np.corrcoef(M_C_observed[mask_H], H_vals[mask_H])[0, 1] if np.sum(mask_H) > 0 else np.nan
    corr_MC_omega_obs = np.corrcoef(M_C_observed[mask_omega], omega_eabc_vals[mask_omega])[0, 1] if np.sum(mask_omega) > 0 else np.nan
    corr_MC_norm_obs = np.corrcoef(M_C_observed[mask_norm], eabc_norm_vals[mask_norm])[0, 1] if np.sum(mask_norm) > 0 else np.nan
    corr_MC_balance_obs = np.corrcoef(M_C_observed[mask_balance], eabc_balance_vals[mask_balance])[0, 1] if np.sum(mask_balance) > 0 else np.nan
    
    print(f"   corr(M_C, H) = {corr_MC_H_obs:.6f}")
    print(f"   corr(M_C, Ω_EABC) = {corr_MC_omega_obs:.6f}")
    print(f"   corr(M_C, ||EABC||) = {corr_MC_norm_obs:.6f}")
    print(f"   corr(M_C, Balance) = {corr_MC_balance_obs:.6f}")
    
    # 3. Permutations-Test
    print(f"\n3. Permutations-Test ({n_permutations} Permutationen)...")
    
    corr_MC_H_perm = []
    corr_MC_omega_perm = []
    corr_MC_norm_perm = []
    corr_MC_balance_perm = []
    
    for i in range(n_permutations):
        if (i + 1) % 100 == 0:
            print(f"   Permutation {i+1}/{n_permutations}...")
        
        # Zufällige Permutation der EABC-Labels
        classes = ['E', 'A', 'B', 'C']
        perm_classes = np.random.permutation(classes)
        perm_map = {orig: perm for orig, perm in zip(classes, perm_classes)}
        
        # Berechne permutierte EABC-Features
        H_perm = []
        omega_eabc_perm = []
        eabc_norm_perm = []
        eabc_balance_perm = []
        
        for n in numbers:
            # Permutiere EABC-Zuordnung
            factors = prime_factors_with_multiplicity(int(n))
            perm_factors = permute_eabc_assignment(factors, perm_map)
            
            # Rekonstruiere "Zahl" mit permutierten Faktoren
            n_perm = int(np.prod(perm_factors))
            
            # Berechne EABC-Features für permutierte Zahl
            try:
                eabc_feats = compute_eabc_features(n_perm)
                H_perm.append(eabc_feats['H'])
                omega_eabc_perm.append(eabc_feats['omega_eabc'])
                eabc_norm_perm.append(eabc_feats['eabc_norm'])
                eabc_balance_perm.append(eabc_feats['eabc_balance'])
            except:
                H_perm.append(np.nan)
                omega_eabc_perm.append(np.nan)
                eabc_norm_perm.append(np.nan)
                eabc_balance_perm.append(np.nan)
        
        H_perm = np.array(H_perm)
        omega_eabc_perm = np.array(omega_eabc_perm)
        eabc_norm_perm = np.array(eabc_norm_perm)
        eabc_balance_perm = np.array(eabc_balance_perm)
        
        # Berechne permutierte Korrelationen
        mask_H_p = ~np.isnan(M_C_observed) & ~np.isnan(H_perm)
        mask_omega_p = ~np.isnan(M_C_observed) & ~np.isnan(omega_eabc_perm)
        mask_norm_p = ~np.isnan(M_C_observed) & ~np.isnan(eabc_norm_perm)
        mask_balance_p = ~np.isnan(M_C_observed) & ~np.isnan(eabc_balance_perm)
        
        if np.sum(mask_H_p) > 1:
            corr_MC_H_perm.append(np.corrcoef(M_C_observed[mask_H_p], H_perm[mask_H_p])[0, 1])
        else:
            corr_MC_H_perm.append(np.nan)
        
        if np.sum(mask_omega_p) > 1:
            corr_MC_omega_perm.append(np.corrcoef(M_C_observed[mask_omega_p], omega_eabc_perm[mask_omega_p])[0, 1])
        else:
            corr_MC_omega_perm.append(np.nan)
        
        if np.sum(mask_norm_p) > 1:
            corr_MC_norm_perm.append(np.corrcoef(M_C_observed[mask_norm_p], eabc_norm_perm[mask_norm_p])[0, 1])
        else:
            corr_MC_norm_perm.append(np.nan)
        
        if np.sum(mask_balance_p) > 1:
            corr_MC_balance_perm.append(np.corrcoef(M_C_observed[mask_balance_p], eabc_balance_perm[mask_balance_p])[0, 1])
        else:
            corr_MC_balance_perm.append(np.nan)
    
    # 4. Z-Score-Analyse
    print("\n4. Z-Score-Analyse...")
    
    corr_MC_H_perm = np.array(corr_MC_H_perm)
    corr_MC_omega_perm = np.array(corr_MC_omega_perm)
    corr_MC_norm_perm = np.array(corr_MC_norm_perm)
    corr_MC_balance_perm = np.array(corr_MC_balance_perm)
    
    # Entferne NaNs
    corr_MC_H_perm = corr_MC_H_perm[~np.isnan(corr_MC_H_perm)]
    corr_MC_omega_perm = corr_MC_omega_perm[~np.isnan(corr_MC_omega_perm)]
    corr_MC_norm_perm = corr_MC_norm_perm[~np.isnan(corr_MC_norm_perm)]
    corr_MC_balance_perm = corr_MC_balance_perm[~np.isnan(corr_MC_balance_perm)]
    
    # Z-Scores
    Z_H = (corr_MC_H_obs - np.mean(corr_MC_H_perm)) / (np.std(corr_MC_H_perm) + 1e-10) if len(corr_MC_H_perm) > 0 else np.nan
    Z_omega = (corr_MC_omega_obs - np.mean(corr_MC_omega_perm)) / (np.std(corr_MC_omega_perm) + 1e-10) if len(corr_MC_omega_perm) > 0 else np.nan
    Z_norm = (corr_MC_norm_obs - np.mean(corr_MC_norm_perm)) / (np.std(corr_MC_norm_perm) + 1e-10) if len(corr_MC_norm_perm) > 0 else np.nan
    Z_balance = (corr_MC_balance_obs - np.mean(corr_MC_balance_perm)) / (np.std(corr_MC_balance_perm) + 1e-10) if len(corr_MC_balance_perm) > 0 else np.nan
    
    print(f"\n   Z(M_C, H) = {Z_H:.4f}")
    print(f"   Z(M_C, Ω_EABC) = {Z_omega:.4f}")
    print(f"   Z(M_C, ||EABC||) = {Z_norm:.4f}")
    print(f"   Z(M_C, Balance) = {Z_balance:.4f}")
    
    # Globaler Z-Score (Maximum der absoluten Z-Werte)
    Z_scores = np.array([Z_H, Z_omega, Z_norm, Z_balance])
    Z_scores = Z_scores[~np.isnan(Z_scores)]
    Z_global = np.max(np.abs(Z_scores)) if len(Z_scores) > 0 else 0.0
    
    print(f"\n   Z (global, max|Z|) = {Z_global:.4f}")
    
    # 5. Interpretation
    print(f"\n5. Interpretation:")
    if Z_global < 0.5:
        print(f"   Z ≈ 0: Korrelationen sind UNABHÄNGIG von EABC-Zuordnung")
        print(f"   → M_C korreliert nicht spezifisch mit EABC-Arithmetik")
        verdict = "EABC_INDEPENDENT"
    elif Z_global < 2.0:
        print(f"   0.5 < |Z| < 2: Schwaches EABC-Signal")
        print(f"   → Grenzfall, mehr Daten benötigt")
        verdict = "UNCLEAR"
    else:
        print(f"   |Z| ≫ 2: STARKES EABC-Signal!")
        print(f"   → M_C korreliert SPEZIFISCH mit EABC-Arithmetik!")
        print(f"   → 🎯 JACKPOT: M_C hängt von EABC-Zuordnung ab!")
        verdict = "EABC_DEPENDENT"
    
    return {
        'corr_MC_H_obs': corr_MC_H_obs,
        'corr_MC_omega_obs': corr_MC_omega_obs,
        'corr_MC_norm_obs': corr_MC_norm_obs,
        'corr_MC_balance_obs': corr_MC_balance_obs,
        'corr_MC_H_perm': corr_MC_H_perm,
        'corr_MC_omega_perm': corr_MC_omega_perm,
        'corr_MC_norm_perm': corr_MC_norm_perm,
        'corr_MC_balance_perm': corr_MC_balance_perm,
        'Z_H': Z_H,
        'Z_omega': Z_omega,
        'Z_norm': Z_norm,
        'Z_balance': Z_balance,
        'Z_global': Z_global,
        'verdict': verdict,
        'n_permutations': n_permutations,
        'H_vals': H_vals,
        'omega_eabc_vals': omega_eabc_vals,
        'eabc_norm_vals': eabc_norm_vals,
        'eabc_balance_vals': eabc_balance_vals
    }


# ============================================================================
# HAUPTFUNKTION V2
# ============================================================================

def main_v2(n_min: int = 2, n_max: int = 1000, omega_min: int = 3,
            canonization: str = 'balanced', n_permutations: int = 1000,
            sample_size: int = None):
    """
    Führt das korrigierte H10 Four-Stage Testing Program durch.
    """
    print("\n" + "="*80)
    print("H10 FOUR-STAGE TESTING PROGRAM V2 (CORRECTED)")
    print("="*80)
    print()
    print("ZENTRALE FRAGE: \"Welche Information bleibt übrig, nachdem Ω(n) entfernt wurde?\"")
    print()
    print("KORREKTUR: Stage C testet jetzt EABC-abhängige Korrelationen.")
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
        'experiments', 'results', 'h10_four_stage_v2'
    )
    os.makedirs(output_dir, exist_ok=True)
    
    # Sammle Daten (gleich wie V1)
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
    
    # STAGE A (wiederverwendbar)
    print(f"\nSCHRITT 3: Stage H10-A")
    stage_A = h10_original.stage_A_omega_baseline(features)
    
    # STAGE B (wiederverwendbar)
    print(f"\nSCHRITT 4: Stage H10-B")
    stage_B = h10_original.stage_B_residual_test(features, stage_A)
    
    # STAGE C V2 (NEU)
    print(f"\nSCHRITT 5: Stage H10-C V2 (KORRIGIERT)")
    stage_C = stage_C_v2_eabc_permutation(features, n_permutations=n_permutations)
    
    # Bericht (vereinfacht)
    print(f"\nSCHRITT 6: Bericht generieren...")
    report_path = os.path.join(output_dir, 'H10_V2_REPORT.md')
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("# H10 FOUR-STAGE TESTING V2 - CORRECTED\n\n")
        f.write(f"**Datum:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("---\n\n")
        
        f.write("## KORREKTUR VON STAGE C\n\n")
        f.write("Das ursprüngliche Problem: M_C und S hängen beide NICHT von EABC ab.\n\n")
        f.write("**Neuer Ansatz:** Teste ob M_C mit **EABC-abhängigen Features** korreliert:\n")
        f.write("- H(n): Konzentrationsmessung\n")
        f.write("- Ω_EABC: Anzahl EABC-Faktoren\n")
        f.write("- ||EABC||: Norm des EABC-Vektors\n")
        f.write("- Balance: Shannon-Entropie der EABC-Verteilung\n\n")
        f.write("---\n\n")
        
        f.write("## ERGEBNISSE\n\n")
        
        f.write("### STAGE A: Ω-Baseline\n\n")
        f.write(f"- R²(M_C, Ω) = {stage_A['R2_MC_Omega']:.6f}\n")
        f.write(f"- R²(S, Ω) = {stage_A['R2_S_Omega']:.6f}\n\n")
        
        f.write("### STAGE B: Residuen\n\n")
        f.write(f"- corr(M_C^⊥, S^⊥) = {stage_B['corr_residuals']:.6f}\n")
        f.write(f"- p-Wert = {stage_B['p_value_residuals']:.6f}\n\n")
        
        f.write("### STAGE C V2: EABC-Permutationen\n\n")
        f.write("**Beobachtete Korrelationen:**\n\n")
        f.write(f"- corr(M_C, H) = {stage_C['corr_MC_H_obs']:.6f}\n")
        f.write(f"- corr(M_C, Ω_EABC) = {stage_C['corr_MC_omega_obs']:.6f}\n")
        f.write(f"- corr(M_C, ||EABC||) = {stage_C['corr_MC_norm_obs']:.6f}\n")
        f.write(f"- corr(M_C, Balance) = {stage_C['corr_MC_balance_obs']:.6f}\n\n")
        
        f.write("**Z-Scores:**\n\n")
        f.write(f"- Z(M_C, H) = {stage_C['Z_H']:.4f}\n")
        f.write(f"- Z(M_C, Ω_EABC) = {stage_C['Z_omega']:.4f}\n")
        f.write(f"- Z(M_C, ||EABC||) = {stage_C['Z_norm']:.4f}\n")
        f.write(f"- Z(M_C, Balance) = {stage_C['Z_balance']:.4f}\n\n")
        f.write(f"**Z (global) = {stage_C['Z_global']:.4f}**\n\n")
        f.write(f"**Verdict:** {stage_C['verdict']}\n\n")
        
        f.write("---\n\n")
        f.write("## 🎯 FINALE ANTWORT\n\n")
        
        if stage_C['verdict'] == 'EABC_DEPENDENT':
            f.write("### **JA - EABC-ABHÄNGIG!**\n\n")
            f.write("M_C korreliert spezifisch mit EABC-Arithmetik. Die Catalan-Struktur ")
            f.write("hängt von der spezifischen EABC-Zuordnung ab!\n\n")
            f.write("**Dies ist publikationswürdig!**\n")
        elif stage_C['verdict'] == 'UNCLEAR':
            f.write("### **UNKLAR**\n\n")
            f.write("Schwaches Signal. Mehr Daten benötigt.\n")
        else:
            f.write("### **NEIN - EABC-UNABHÄNGIG**\n\n")
            f.write("M_C korreliert nicht spezifisch mit EABC-Arithmetik. Die Catalan-Struktur ")
            f.write("ist unabhängig von der spezifischen EABC-Zuordnung.\n\n")
            f.write("**M_C ist eine rein geometrische Eigenschaft.**\n")
    
    print(f"✓ Bericht gespeichert: {report_path}")
    
    # CSV
    csv_path = os.path.join(output_dir, 'h10_v2_results.csv')
    results_df = pd.DataFrame({
        'metric': ['R2_MC_Omega', 'R2_S_Omega', 'corr_residuals', 
                   'corr_MC_H', 'Z_H', 'Z_omega', 'Z_norm', 'Z_balance', 'Z_global'],
        'value': [
            stage_A['R2_MC_Omega'],
            stage_A['R2_S_Omega'],
            stage_B['corr_residuals'],
            stage_C['corr_MC_H_obs'],
            stage_C['Z_H'],
            stage_C['Z_omega'],
            stage_C['Z_norm'],
            stage_C['Z_balance'],
            stage_C['Z_global']
        ]
    })
    results_df.to_csv(csv_path, index=False)
    print(f"✓ CSV gespeichert: {csv_path}")
    
    # Finale Zusammenfassung
    print("\n" + "="*80)
    print("FINALE ZUSAMMENFASSUNG V2")
    print("="*80)
    print()
    print(f"Datensatz: {len(numbers)} Zahlen")
    print()
    print("ERGEBNISSE:")
    print(f"  Stage A: R²(M_C, Ω) = {stage_A['R2_MC_Omega']:.4f}")
    print(f"  Stage B: corr(M_C^⊥, S^⊥) = {stage_B['corr_residuals']:.4f}")
    print(f"  Stage C V2: Z (global) = {stage_C['Z_global']:.4f} → {stage_C['verdict']}")
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
    
    parser = argparse.ArgumentParser(description='H10 Four-Stage Testing V2 (Corrected)')
    parser.add_argument('--n_min', type=int, default=2)
    parser.add_argument('--n_max', type=int, default=1000)
    parser.add_argument('--omega_min', type=int, default=3)
    parser.add_argument('--canonization', type=str, default='balanced')
    parser.add_argument('--n_permutations', type=int, default=1000)
    parser.add_argument('--sample_size', type=int, default=None)
    
    args = parser.parse_args()
    
    results = main_v2(
        n_min=args.n_min,
        n_max=args.n_max,
        omega_min=args.omega_min,
        canonization=args.canonization,
        n_permutations=args.n_permutations,
        sample_size=args.sample_size
    )
