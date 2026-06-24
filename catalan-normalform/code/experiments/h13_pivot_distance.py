"""
H13 Pivot-Distanz-Analyse
==========================

KERNFRAGE: Gibt es etwas Besonderes an Distanzen d(p) = |p - 40| für Primzahlen,
           wenn man sie durch EABC-Linse betrachtet?

MOTIVATION:
    Ein exploratives Primzahl-Diagramm (mit 40 als Pivot) zeigt interessante
    Muster. Statt geometrische Interpretationen zu spekulieren, behandeln wir
    die Pivot-Distanzen als testbare arithmetische Invarianten.

METHODIK:
    1. Datensatz-Generierung: Für alle Primzahlen p < 10^5 (später 10^7)
       berechne für jeden Pivot k ∈ {30, 36, 40, 42, 60}:
       - d_k(p) = |p - k|
       - EABC-Eigenschaften von p und d_k(p)
    
    2. Statistische Tests:
       A) Ist 40 besonders? (Vergleich verschiedener Pivots)
       B) EABC-Korrelationen (Zusammenhänge zwischen EABC(p) und EABC(d_k(p)))
       C) Strukturelle Eigenschaften (H, E, Ω)
    
    3. Verbindung zu H10/H12:
       - H10: M_C ist eigenständig, korreliert nicht mit S
       - H13: Könnte M_C mit Pivot-Distanz-Invarianten korrelieren?

ERWARTETE ERGEBNISSE:
    - 40 ist nicht besonders → Interessante Kunst, aber keine tiefe Mathematik
    - 40 zeigt Anomalien → Neue arithmetische Muster!
    - Pivot-Distanzen generell strukturiert → Neue Invarianten entdeckt

Autor: H13 Testing Framework
Datum: 2026-06-24
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from scipy import stats
from scipy.stats import chi2_contingency
from typing import Dict, List, Tuple
import json
from datetime import datetime
import pandas as pd
from pathlib import Path

from utils.eabc import eabc_class, compute_eabc_vector
from utils.eabc_test_data import EABCTestData
from utils.pivot_analysis import (
    generate_primes,
    compute_pivot_distance,
    compute_eabc_entropy,
    analyze_pivot_for_primes,
    compute_eabc_correlation,
    compare_pivot_distributions,
    create_contingency_table
)


# Konfiguration
PIVOTS = [30, 36, 40, 42, 48, 60, 72, 84]  # Erweitert: 8 Pivots statt 5
N_RANDOM_PIVOTS = 100  # Für Randomisierungs-Test
RANDOM_PIVOT_RANGE = (20, 100)  # Bereich für zufällige Pivots
PRIME_LIMIT = 10**5  # Start mit 10^5, später 10^7
OUTPUT_DIR = Path("experiments/results/h13")


# ============================================================================
# TEST A: IST 40 BESONDERS?
# ============================================================================

def test_A_pivot_comparison(
    results_all: Dict[int, Dict[str, np.ndarray]]
) -> Dict:
    """
    Test A: Vergleicht Eigenschaften der Distanz-Verteilungen über Pivots.
    
    Analysiert:
    - Varianz von d_k(p)
    - EABC-Signatur-Verteilung
    - Entropie-Verteilung
    - Konzentrations-Verteilung H
    
    Ziel: Feststellen, ob 40 statistisch besondere Eigenschaften zeigt.
    """
    print("\n" + "="*80)
    print("TEST A: IST 40 BESONDERS?")
    print("="*80)
    
    comparison = compare_pivot_distributions(results_all)
    
    # 1. Varianz-Vergleich
    print("\n1. VARIANZ DER DISTANZEN d_k(p):")
    print("   (Misst Streuung der Primzahlen um Pivot)")
    print()
    
    for pivot in PIVOTS:
        var = comparison['variance'][pivot]
        print(f"   Pivot k={pivot:2d}: Var(d_k) = {var:12,.2f}")
    
    # Normalisiere auf 40
    var_40 = comparison['variance'][40]
    print()
    print(f"   Normalisiert auf k=40:")
    for pivot in PIVOTS:
        ratio = comparison['variance'][pivot] / var_40
        marker = " ← PIVOT 40" if pivot == 40 else ""
        print(f"   Pivot k={pivot:2d}: {ratio:6.4f}x{marker}")
    
    # 2. Entropie-Vergleich
    print("\n2. MITTLERE ENTROPIE E(d_k(p)):")
    print("   (Misst Durchschnittliche Verteilung der EABC-Faktoren)")
    print()
    
    for pivot in PIVOTS:
        E_mean = comparison['entropy_mean'][pivot]
        E_std = comparison['entropy_std'][pivot]
        print(f"   Pivot k={pivot:2d}: E̅ = {E_mean:.4f} ± {E_std:.4f} bits")
    
    # 3. Konzentrations-Vergleich
    print("\n3. MITTLERE KONZENTRATION H(d_k(p)):")
    print("   (Misst durchschnittliche EABC-Faktor-Konzentration)")
    print()
    
    for pivot in PIVOTS:
        H_mean = comparison['H_mean'][pivot]
        H_std = comparison['H_std'][pivot]
        print(f"   Pivot k={pivot:2d}: H̅ = {H_mean:.4f} ± {H_std:.4f}")
    
    # 4. Omega-Vergleich
    print("\n4. MITTLERES Ω(d_k(p)):")
    print("   (Misst durchschnittliche Anzahl Primfaktoren)")
    print()
    
    for pivot in PIVOTS:
        omega_mean = comparison['omega_mean'][pivot]
        omega_std = comparison['omega_std'][pivot]
        print(f"   Pivot k={pivot:2d}: Ω̅ = {omega_mean:.4f} ± {omega_std:.4f}")
    
    # 5. Statistische Tests
    print("\n5. STATISTISCHE TESTS:")
    print()
    
    # Kruskal-Wallis Test für Entropie
    entropy_groups = [results_all[k]['E_d'][results_all[k]['d_k'] >= 2] for k in PIVOTS]
    H_stat_entropy, p_value_entropy = stats.kruskal(*entropy_groups)
    print(f"   Kruskal-Wallis Test (Entropie E):")
    print(f"   H = {H_stat_entropy:.4f}, p = {p_value_entropy:.4e}")
    print(f"   → {'Signifikanter Unterschied' if p_value_entropy < 0.05 else 'Kein signifikanter Unterschied'}")
    
    # Kruskal-Wallis Test für H
    H_groups = [
        results_all[k]['H_d'][(results_all[k]['d_k'] >= 2) & (~np.isnan(results_all[k]['H_d']))]
        for k in PIVOTS
    ]
    H_stat_H, p_value_H = stats.kruskal(*H_groups)
    print(f"\n   Kruskal-Wallis Test (Konzentration H):")
    print(f"   H = {H_stat_H:.4f}, p = {p_value_H:.4e}")
    print(f"   → {'Signifikanter Unterschied' if p_value_H < 0.05 else 'Kein signifikanter Unterschied'}")
    
    # INTERPRETATION
    print("\n" + "-"*80)
    print("INTERPRETATION:")
    print("-"*80)
    
    # Prüfe, ob 40 extreme Werte hat
    var_values = [comparison['variance'][k] for k in PIVOTS]
    var_40_rank = sorted(var_values).index(comparison['variance'][40]) + 1
    
    E_values = [comparison['entropy_mean'][k] for k in PIVOTS]
    E_40_rank = sorted(E_values).index(comparison['entropy_mean'][40]) + 1
    
    H_values = [comparison['H_mean'][k] for k in PIVOTS]
    H_40_rank = sorted(H_values).index(comparison['H_mean'][40]) + 1
    
    print(f"\nRang von k=40 (unter {len(PIVOTS)} Pivots):")
    print(f"  Varianz:      Rang {var_40_rank}/{len(PIVOTS)}")
    print(f"  Entropie E̅:   Rang {E_40_rank}/{len(PIVOTS)}")
    print(f"  Konzentration H̅: Rang {H_40_rank}/{len(PIVOTS)}")
    
    is_special = (
        (var_40_rank == 1 or var_40_rank == len(PIVOTS)) or
        (E_40_rank == 1 or E_40_rank == len(PIVOTS)) or
        (H_40_rank == 1 or H_40_rank == len(PIVOTS))
    )
    
    if is_special:
        print("\n→ 40 zeigt EXTREME Werte in mindestens einer Metrik!")
        print("  Dies könnte auf besondere arithmetische Eigenschaften hindeuten.")
    else:
        print("\n→ 40 ist NICHT besonders extrem in den getesteten Metriken.")
        print("  Die Werte liegen im mittleren Bereich der Pivots.")
    
    return {
        'comparison': comparison,
        'kruskal_entropy': {'H': H_stat_entropy, 'p': p_value_entropy},
        'kruskal_H': {'H': H_stat_H, 'p': p_value_H},
        'var_40_rank': var_40_rank,
        'E_40_rank': E_40_rank,
        'H_40_rank': H_40_rank,
        'is_special': is_special
    }


# ============================================================================
# TEST B: EABC-KORRELATIONEN
# ============================================================================

def test_B_eabc_correlations(
    results_all: Dict[int, Dict[str, np.ndarray]]
) -> Dict:
    """
    Test B: Analysiert Korrelationen zwischen EABC(p) und EABC(d_k(p)).
    
    Fragt:
    - Gibt es bevorzugte EABC-Kombinationen?
    - Wenn p ∈ E, ist d_k(p) häufiger in bestimmter Klasse?
    - Unterscheiden sich diese Muster zwischen Pivots?
    """
    print("\n" + "="*80)
    print("TEST B: EABC-KORRELATIONEN")
    print("="*80)
    
    correlations = {}
    
    for pivot in PIVOTS:
        print(f"\n{'─'*80}")
        print(f"PIVOT k={pivot}")
        print(f"{'─'*80}")
        
        results = results_all[pivot]
        
        # Erstelle Kontingenz-Tabelle
        matrix, row_labels, col_labels = create_contingency_table(
            results['eabc_p'],
            results['eabc_d']
        )
        
        # Chi²-Test
        chi2, p_value, dof, expected = chi2_contingency(matrix)
        
        print("\n1. KONTINGENZ-TABELLE: EABC(p) × dominante EABC-Klasse von d_k(p)")
        print()
        
        # Formatierte Ausgabe
        header = "EABC(p)".ljust(10) + "".join([c.rjust(8) for c in col_labels]) + "  TOTAL"
        print("   " + header)
        print("   " + "-" * len(header))
        
        for i, row_label in enumerate(row_labels):
            row_sum = np.sum(matrix[i])
            row_str = row_label.ljust(10) + "".join([f"{matrix[i,j]:8d}" for j in range(len(col_labels))])
            row_str += f"{row_sum:8d}"
            print("   " + row_str)
        
        # Total
        col_totals = np.sum(matrix, axis=0)
        total_str = "TOTAL".ljust(10) + "".join([f"{t:8d}" for t in col_totals])
        total_str += f"{np.sum(matrix):8d}"
        print("   " + "-" * len(header))
        print("   " + total_str)
        
        print(f"\n2. CHI²-TEST (Unabhängigkeit EABC(p) vs. EABC(d_k(p))):")
        print(f"   χ² = {chi2:.4f}, df = {dof}, p = {p_value:.4e}")
        print(f"   → {'Signifikante Abhängigkeit' if p_value < 0.05 else 'Keine signifikante Abhängigkeit'}")
        
        # Berechne normalisierte Residuen (für starke Abweichungen)
        residuals = (matrix - expected) / np.sqrt(expected + 1e-10)
        
        print("\n3. NORMALISIERTE RESIDUEN (|r| > 2 zeigt starke Abweichung):")
        print("   (Positive Werte: Überrepräsentation, Negative: Unterrepräsentation)")
        print()
        
        for i, row_label in enumerate(row_labels):
            for j, col_label in enumerate(col_labels):
                r = residuals[i, j]
                if abs(r) > 2:
                    direction = "↑" if r > 0 else "↓"
                    print(f"   {row_label} → {col_label}: r = {r:+6.2f} {direction}")
        
        correlations[pivot] = {
            'matrix': matrix,
            'row_labels': row_labels,
            'col_labels': col_labels,
            'chi2': chi2,
            'p_value': p_value,
            'dof': dof,
            'expected': expected,
            'residuals': residuals
        }
    
    # VERGLEICH ÜBER PIVOTS
    print("\n" + "="*80)
    print("PIVOT-VERGLEICH")
    print("="*80)
    
    print("\nChi²-Statistik für alle Pivots:")
    for pivot in PIVOTS:
        chi2 = correlations[pivot]['chi2']
        p = correlations[pivot]['p_value']
        marker = " ← PIVOT 40" if pivot == 40 else ""
        sig = " (***)" if p < 0.001 else " (**)" if p < 0.01 else " (*)" if p < 0.05 else ""
        print(f"   k={pivot:2d}: χ² = {chi2:8.2f}, p = {p:.4e}{sig}{marker}")
    
    # Ist 40 besonders?
    chi2_values = [correlations[k]['chi2'] for k in PIVOTS]
    chi2_40_rank = sorted(chi2_values).index(correlations[40]['chi2']) + 1
    
    print(f"\nRang von k=40: {chi2_40_rank}/{len(PIVOTS)} (nach χ²)")
    
    if chi2_40_rank == 1 or chi2_40_rank == len(PIVOTS):
        print("→ 40 zeigt EXTREMALE χ²-Statistik!")
    else:
        print("→ 40 ist NICHT extrem in der EABC-Korrelation.")
    
    return {
        'correlations': correlations,
        'chi2_40_rank': chi2_40_rank
    }


# ============================================================================
# TEST C: STRUKTURELLE EIGENSCHAFTEN
# ============================================================================

def test_C_structural_properties(
    results_all: Dict[int, Dict[str, np.ndarray]]
) -> Dict:
    """
    Test C: Analysiert strukturelle Eigenschaften der Distanzen.
    
    Betrachtet:
    - H(d_k(p)) - Konzentration der Faktorisierung
    - E(d_k(p)) - Entropie der EABC-Signatur
    - Korrelationen zwischen diesen Größen
    """
    print("\n" + "="*80)
    print("TEST C: STRUKTURELLE EIGENSCHAFTEN")
    print("="*80)
    
    structural = {}
    
    for pivot in PIVOTS:
        print(f"\n{'─'*80}")
        print(f"PIVOT k={pivot}")
        print(f"{'─'*80}")
        
        results = results_all[pivot]
        
        # Filtere gültige Werte (d_k >= 2)
        mask = results['d_k'] >= 2
        E_d = results['E_d'][mask]
        H_d = results['H_d'][mask]
        H_d = H_d[~np.isnan(H_d)]
        omega_d = results['omega_d'][mask]
        
        print(f"\n1. ENTROPIE E(d_k(p)):")
        print(f"   Mittelwert: {np.mean(E_d):.4f} bits")
        print(f"   Std.-Abw.: {np.std(E_d):.4f} bits")
        print(f"   Min/Max:   {np.min(E_d):.4f} / {np.max(E_d):.4f} bits")
        print(f"   Median:    {np.median(E_d):.4f} bits")
        
        print(f"\n2. KONZENTRATION H(d_k(p)):")
        print(f"   Mittelwert: {np.mean(H_d):.4f}")
        print(f"   Std.-Abw.: {np.std(H_d):.4f}")
        print(f"   Min/Max:   {np.min(H_d):.4f} / {np.max(H_d):.4f}")
        print(f"   Median:    {np.median(H_d):.4f}")
        
        print(f"\n3. ANZAHL PRIMFAKTOREN Ω(d_k(p)):")
        print(f"   Mittelwert: {np.mean(omega_d):.4f}")
        print(f"   Std.-Abw.: {np.std(omega_d):.4f}")
        print(f"   Min/Max:   {np.min(omega_d)} / {np.max(omega_d)}")
        print(f"   Median:    {np.median(omega_d):.1f}")
        
        # Korrelationen
        # Filtere für Korrelationen (beide gültig)
        mask_corr = (results['d_k'] >= 2) & (~np.isnan(results['H_d']))
        E_d_corr = results['E_d'][mask_corr]
        H_d_corr = results['H_d'][mask_corr]
        omega_d_corr = results['omega_d'][mask_corr]
        
        corr_E_H = np.corrcoef(E_d_corr, H_d_corr)[0, 1]
        corr_E_omega = np.corrcoef(E_d_corr, omega_d_corr)[0, 1]
        corr_H_omega = np.corrcoef(H_d_corr, omega_d_corr)[0, 1]
        
        print(f"\n4. KORRELATIONEN:")
        print(f"   corr(E, H):     {corr_E_H:+.4f}")
        print(f"   corr(E, Ω):     {corr_E_omega:+.4f}")
        print(f"   corr(H, Ω):     {corr_H_omega:+.4f}")
        
        structural[pivot] = {
            'E_mean': np.mean(E_d),
            'E_std': np.std(E_d),
            'H_mean': np.mean(H_d),
            'H_std': np.std(H_d),
            'omega_mean': np.mean(omega_d),
            'omega_std': np.std(omega_d),
            'corr_E_H': corr_E_H,
            'corr_E_omega': corr_E_omega,
            'corr_H_omega': corr_H_omega
        }
    
    return {'structural': structural}


# ============================================================================
# TEST D: RANDOMISIERUNGS-TEST
# ============================================================================

def test_D_randomization(
    primes: np.ndarray,
    get_coords,
    results_40: Dict[str, np.ndarray]
) -> Dict:
    """
    Test D: Randomisierungs-Test gegen zufällige Pivots.
    
    Generiert N zufällige Pivots aus dem Bereich [20, 100] und vergleicht
    die k=40-Metriken mit der zufälligen Verteilung.
    
    Ziel: Feststellen, ob k=40 auch im Vergleich zu zufälligen Zahlen
          besonders ist oder ob es ein allgemeines Muster stark
          zusammengesetzter Zahlen ist.
    """
    print("\n" + "="*80)
    print("TEST D: RANDOMISIERUNGS-TEST")
    print("="*80)
    
    print(f"\nGeneriere {N_RANDOM_PIVOTS} zufällige Pivots aus [{RANDOM_PIVOT_RANGE[0]}, {RANDOM_PIVOT_RANGE[1]}]...")
    
    np.random.seed(42)  # Reproduzierbarkeit
    random_pivots = np.random.randint(
        RANDOM_PIVOT_RANGE[0], 
        RANDOM_PIVOT_RANGE[1] + 1, 
        size=N_RANDOM_PIVOTS
    )
    
    # Sammle Metriken für alle zufälligen Pivots
    random_E_means = []
    random_H_means = []
    random_omega_means = []
    random_chi2_values = []
    
    print("Analysiere zufällige Pivots...", end=" ")
    for k_rand in random_pivots:
        results_rand = analyze_pivot_for_primes(primes, k_rand, get_coords)
        
        # Berechne Metriken
        mask = results_rand['d_k'] >= 2
        E_d = results_rand['E_d'][mask]
        H_d = results_rand['H_d'][mask]
        H_d = H_d[~np.isnan(H_d)]
        omega_d = results_rand['omega_d'][mask]
        
        random_E_means.append(np.mean(E_d))
        random_H_means.append(np.mean(H_d))
        random_omega_means.append(np.mean(omega_d))
        
        # Chi²-Statistik
        matrix, _, _ = create_contingency_table(results_rand['eabc_p'], results_rand['eabc_d'])
        chi2, _, _, _ = chi2_contingency(matrix)
        random_chi2_values.append(chi2)
    
    print("✓")
    
    # Konvertiere zu numpy arrays
    random_E_means = np.array(random_E_means)
    random_H_means = np.array(random_H_means)
    random_omega_means = np.array(random_omega_means)
    random_chi2_values = np.array(random_chi2_values)
    
    # Berechne k=40 Metriken (bereits vorhanden)
    mask_40 = results_40['d_k'] >= 2
    E_40 = np.mean(results_40['E_d'][mask_40])
    H_40 = np.mean(results_40['H_d'][mask_40 & ~np.isnan(results_40['H_d'])])
    omega_40 = np.mean(results_40['omega_d'][mask_40])
    
    matrix_40, _, _ = create_contingency_table(results_40['eabc_p'], results_40['eabc_d'])
    chi2_40, _, _, _ = chi2_contingency(matrix_40)
    
    # Berechne Perzentile
    E_percentile = (random_E_means < E_40).sum() / len(random_E_means) * 100
    H_percentile = (random_H_means < H_40).sum() / len(random_H_means) * 100
    omega_percentile = (random_omega_means < omega_40).sum() / len(random_omega_means) * 100
    chi2_percentile = (random_chi2_values < chi2_40).sum() / len(random_chi2_values) * 100
    
    # Ausgabe
    print("\n" + "="*80)
    print("ERGEBNISSE: k=40 vs. ZUFÄLLIGE PIVOTS")
    print("="*80)
    
    print(f"\n1. MITTLERE ENTROPIE E̅:")
    print(f"   k=40:              {E_40:.4f} bits")
    print(f"   Zufällige Pivots:  {np.mean(random_E_means):.4f} ± {np.std(random_E_means):.4f} bits")
    print(f"   Perzentil:         {E_percentile:.1f}%")
    print(f"   → k=40 ist {'extremer' if E_percentile < 10 or E_percentile > 90 else 'nicht extrem'} (< 10% oder > 90% ist extrem)")
    
    print(f"\n2. MITTLERE KONZENTRATION H̅:")
    print(f"   k=40:              {H_40:.4f}")
    print(f"   Zufällige Pivots:  {np.mean(random_H_means):.4f} ± {np.std(random_H_means):.4f}")
    print(f"   Perzentil:         {H_percentile:.1f}%")
    print(f"   → k=40 ist {'extremer' if H_percentile < 10 or H_percentile > 90 else 'nicht extrem'}")
    
    print(f"\n3. MITTLERES Ω̅:")
    print(f"   k=40:              {omega_40:.4f}")
    print(f"   Zufällige Pivots:  {np.mean(random_omega_means):.4f} ± {np.std(random_omega_means):.4f}")
    print(f"   Perzentil:         {omega_percentile:.1f}%")
    print(f"   → k=40 ist {'extremer' if omega_percentile < 10 or omega_percentile > 90 else 'nicht extrem'}")
    
    print(f"\n4. CHI²-STATISTIK:")
    print(f"   k=40:              {chi2_40:.2f}")
    print(f"   Zufällige Pivots:  {np.mean(random_chi2_values):.2f} ± {np.std(random_chi2_values):.2f}")
    print(f"   Perzentil:         {chi2_percentile:.1f}%")
    print(f"   → k=40 ist {'extremer' if chi2_percentile < 10 or chi2_percentile > 90 else 'nicht extrem'}")
    
    # Gesamtbewertung
    print("\n" + "-"*80)
    print("INTERPRETATION:")
    print("-"*80)
    
    n_extreme = sum([
        E_percentile < 10 or E_percentile > 90,
        H_percentile < 10 or H_percentile > 90,
        omega_percentile < 10 or omega_percentile > 90,
        chi2_percentile < 10 or chi2_percentile > 90
    ])
    
    print(f"\nAnzahl extremer Metriken (< 10% oder > 90%): {n_extreme}/4")
    
    if n_extreme >= 3:
        print("\n→ 🔴 k=40 ist ROBUST BESONDERS!")
        print("  Die Anomalien sind auch im Vergleich zu zufälligen Pivots signifikant.")
    elif n_extreme >= 2:
        print("\n→ 🟡 k=40 zeigt MODERATE Besonderheiten.")
        print("  Einige Metriken sind extrem, aber nicht alle.")
    else:
        print("\n→ 🟢 k=40 ist NICHT robust besonders.")
        print("  Die Werte liegen im Bereich zufälliger Pivots.")
    
    return {
        'random_pivots': random_pivots,
        'random_E_means': random_E_means,
        'random_H_means': random_H_means,
        'random_omega_means': random_omega_means,
        'random_chi2_values': random_chi2_values,
        'E_40': E_40,
        'H_40': H_40,
        'omega_40': omega_40,
        'chi2_40': chi2_40,
        'E_percentile': E_percentile,
        'H_percentile': H_percentile,
        'omega_percentile': omega_percentile,
        'chi2_percentile': chi2_percentile,
        'n_extreme': n_extreme
    }


# ============================================================================
# VISUALISIERUNG
# ============================================================================

def create_visualizations(
    results_all: Dict[int, Dict[str, np.ndarray]],
    test_A_results: Dict,
    test_B_results: Dict,
    test_D_results: Dict,
    output_path: Path
):
    """
    Erstellt umfassende Visualisierungen der Pivot-Distanz-Analyse.
    """
    print("\n" + "="*80)
    print("ERSTELLE VISUALISIERUNGEN")
    print("="*80)
    
    # Figure mit mehreren Panels
    fig = plt.figure(figsize=(24, 16))
    gs = GridSpec(4, 3, figure=fig, hspace=0.35, wspace=0.3)
    
    # Panel 1: Distanz-Histogramme (nur für ausgewählte Pivots - zu viele sonst)
    ax1 = fig.add_subplot(gs[0, :])
    selected_for_hist = [30, 40, 60, 84]  # Repräsentative Auswahl
    for pivot in selected_for_hist:
        d_k = results_all[pivot]['d_k']
        label = f"k={pivot}" + (" (FOKUS)" if pivot == 40 else "")
        alpha = 0.8 if pivot == 40 else 0.4
        linewidth = 2 if pivot == 40 else 1
        ax1.hist(d_k, bins=50, alpha=alpha, label=label, linewidth=linewidth, edgecolor='black')
    ax1.set_xlabel('Distanz d_k(p) = |p - k|', fontsize=12)
    ax1.set_ylabel('Häufigkeit', fontsize=12)
    ax1.set_title('A) Verteilung der Pivot-Distanzen (ausgewählte k)', fontsize=14, fontweight='bold')
    ax1.legend()
    ax1.grid(alpha=0.3)
    
    # Panel 2: Entropie-Vergleich
    ax2 = fig.add_subplot(gs[1, 0])
    comparison = test_A_results['comparison']
    pivots_list = list(PIVOTS)
    E_means = [comparison['entropy_mean'][k] for k in pivots_list]
    E_stds = [comparison['entropy_std'][k] for k in pivots_list]
    colors = ['red' if k == 40 else 'steelblue' for k in pivots_list]
    ax2.bar(range(len(pivots_list)), E_means, yerr=E_stds, color=colors, alpha=0.7, capsize=5)
    ax2.set_xticks(range(len(pivots_list)))
    ax2.set_xticklabels([f"{k}" for k in pivots_list], rotation=0, fontsize=10)
    ax2.set_xlabel('Pivot k', fontsize=11)
    ax2.set_ylabel('Mittlere Entropie E̅ (bits)', fontsize=11)
    ax2.set_title('B) Entropie E(d_k(p))', fontsize=12, fontweight='bold')
    ax2.grid(alpha=0.3, axis='y')
    ax2.axhline(y=test_D_results['E_40'], color='red', linestyle='--', alpha=0.5, linewidth=1)
    
    # Panel 3: H-Vergleich
    ax3 = fig.add_subplot(gs[1, 1])
    H_means = [comparison['H_mean'][k] for k in pivots_list]
    H_stds = [comparison['H_std'][k] for k in pivots_list]
    ax3.bar(range(len(pivots_list)), H_means, yerr=H_stds, color=colors, alpha=0.7, capsize=5)
    ax3.set_xticks(range(len(pivots_list)))
    ax3.set_xticklabels([f"{k}" for k in pivots_list], rotation=0, fontsize=10)
    ax3.set_xlabel('Pivot k', fontsize=11)
    ax3.set_ylabel('Mittlere Konzentration H̅', fontsize=11)
    ax3.set_title('C) Konzentration H(d_k(p))', fontsize=12, fontweight='bold')
    ax3.grid(alpha=0.3, axis='y')
    ax3.axhline(y=test_D_results['H_40'], color='red', linestyle='--', alpha=0.5, linewidth=1)
    
    # Panel 4: Omega-Vergleich
    ax4 = fig.add_subplot(gs[1, 2])
    omega_means = [comparison['omega_mean'][k] for k in pivots_list]
    omega_stds = [comparison['omega_std'][k] for k in pivots_list]
    ax4.bar(range(len(pivots_list)), omega_means, yerr=omega_stds, color=colors, alpha=0.7, capsize=5)
    ax4.set_xticks(range(len(pivots_list)))
    ax4.set_xticklabels([f"{k}" for k in pivots_list], rotation=0, fontsize=10)
    ax4.set_xlabel('Pivot k', fontsize=11)
    ax4.set_ylabel('Mittleres Ω̅(d_k(p))', fontsize=11)
    ax4.set_title('D) Anzahl Primfaktoren Ω(d_k(p))', fontsize=12, fontweight='bold')
    ax4.grid(alpha=0.3, axis='y')
    ax4.axhline(y=test_D_results['omega_40'], color='red', linestyle='--', alpha=0.5, linewidth=1)
    
    # Panel 5-7: EABC Heatmaps für ausgewählte Pivots (30, 40, 60)
    selected_pivots = [30, 40, 60]
    for idx, pivot in enumerate(selected_pivots):
        ax = fig.add_subplot(gs[2, idx])
        
        corr_data = test_B_results['correlations'][pivot]
        matrix = corr_data['matrix']
        row_labels = corr_data['row_labels']
        col_labels = corr_data['col_labels']
        
        # Normalisiere Zeilen (für bessere Visualisierung)
        matrix_norm = matrix.astype(float)
        row_sums = matrix_norm.sum(axis=1, keepdims=True)
        matrix_norm = matrix_norm / (row_sums + 1e-10)
        
        im = ax.imshow(matrix_norm, cmap='YlOrRd', aspect='auto', vmin=0, vmax=1)
        ax.set_xticks(range(len(col_labels)))
        ax.set_yticks(range(len(row_labels)))
        ax.set_xticklabels(col_labels, fontsize=10)
        ax.set_yticklabels(row_labels, fontsize=10)
        ax.set_xlabel('EABC(d_k(p))', fontsize=10)
        ax.set_ylabel('EABC(p)', fontsize=10)
        
        title_suffix = " ← FOKUS" if pivot == 40 else ""
        ax.set_title(f'E) k={pivot}: EABC-Korrelation{title_suffix}', fontsize=11, fontweight='bold')
        
        # Annotiere Zellen
        for i in range(len(row_labels)):
            for j in range(len(col_labels)):
                text = ax.text(j, i, f'{matrix_norm[i, j]:.2f}',
                              ha="center", va="center", color="black", fontsize=8)
        
        plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    
    # Panel 8-9: Randomisierungs-Test
    # Panel 8: Histogramme für zufällige Pivots
    ax8 = fig.add_subplot(gs[3, 0])
    ax8.hist(test_D_results['random_E_means'], bins=20, alpha=0.7, color='gray', edgecolor='black')
    ax8.axvline(test_D_results['E_40'], color='red', linewidth=2, label=f'k=40 ({test_D_results["E_percentile"]:.1f}%ile)')
    ax8.set_xlabel('Mittlere Entropie E̅', fontsize=10)
    ax8.set_ylabel('Häufigkeit', fontsize=10)
    ax8.set_title('F) Randomisierung: E̅ Verteilung', fontsize=11, fontweight='bold')
    ax8.legend(fontsize=9)
    ax8.grid(alpha=0.3)
    
    ax9 = fig.add_subplot(gs[3, 1])
    ax9.hist(test_D_results['random_H_means'], bins=20, alpha=0.7, color='gray', edgecolor='black')
    ax9.axvline(test_D_results['H_40'], color='red', linewidth=2, label=f'k=40 ({test_D_results["H_percentile"]:.1f}%ile)')
    ax9.set_xlabel('Mittlere Konzentration H̅', fontsize=10)
    ax9.set_ylabel('Häufigkeit', fontsize=10)
    ax9.set_title('G) Randomisierung: H̅ Verteilung', fontsize=11, fontweight='bold')
    ax9.legend(fontsize=9)
    ax9.grid(alpha=0.3)
    
    ax10 = fig.add_subplot(gs[3, 2])
    ax10.hist(test_D_results['random_chi2_values'], bins=20, alpha=0.7, color='gray', edgecolor='black')
    ax10.axvline(test_D_results['chi2_40'], color='red', linewidth=2, label=f'k=40 ({test_D_results["chi2_percentile"]:.1f}%ile)')
    ax10.set_xlabel('Chi²-Statistik', fontsize=10)
    ax10.set_ylabel('Häufigkeit', fontsize=10)
    ax10.set_title('H) Randomisierung: χ² Verteilung', fontsize=11, fontweight='bold')
    ax10.legend(fontsize=9)
    ax10.grid(alpha=0.3)
    
    # Haupttitel
    fig.suptitle(
        'H13 Pivot-Distanz-Analyse (Erweitert): Ist 40 besonders?\n'
        f'Primzahlen p < {PRIME_LIMIT:,} | Pivots k ∈ {{{", ".join(map(str, PIVOTS))}}} | {N_RANDOM_PIVOTS} zufällige Pivots',
        fontsize=16,
        fontweight='bold',
        y=0.99
    )
    
    # Speichere
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Visualisierung gespeichert: {output_path}")
    
    plt.close()


# ============================================================================
# HAUPTPROGRAMM
# ============================================================================

def main():
    """
    Hauptprogramm für H13 Pivot-Distanz-Analyse.
    """
    print("="*80)
    print("H13 PIVOT-DISTANZ-ANALYSE")
    print("="*80)
    print(f"\nKonfiguration:")
    print(f"  Primzahlen:  p < {PRIME_LIMIT:,}")
    print(f"  Pivots:      k ∈ {PIVOTS}")
    print(f"  Ausgabe:     {OUTPUT_DIR}")
    print()
    
    # Erstelle Ausgabe-Verzeichnis
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Lade EABC-Daten (wenn Cache vorhanden)
    cache_file = Path("data/eabc_cache.h5")
    
    if cache_file.exists():
        print(f"Lade EABC-Cache: {cache_file}")
        eabc_data = EABCTestData(cache_file=cache_file, readonly=True)
        get_coords = eabc_data.get_coordinates
    else:
        print("⚠ Warnung: Kein EABC-Cache gefunden, verwende direkte Berechnung")
        print("  (Dies ist langsamer! Erstelle Cache mit eabc_test_data.create_cache)")
        from utils.eabc import compute_svn_coordinates
        
        def get_coords(n):
            coords = compute_svn_coordinates(n)
            coords['shell'] = coords['v2'] + coords['v3']
            return coords
    
    # Generiere Primzahlen
    print(f"\nGeneriere Primzahlen < {PRIME_LIMIT:,}...")
    primes = generate_primes(PRIME_LIMIT)
    print(f"✓ {len(primes):,} Primzahlen gefunden")
    
    # Analysiere für alle Pivots
    print("\nAnalysiere Pivot-Distanzen...")
    results_all = {}
    
    for pivot in PIVOTS:
        print(f"  Analysiere k={pivot}...", end=" ")
        results = analyze_pivot_for_primes(primes, pivot, get_coords)
        results_all[pivot] = results
        print("✓")
    
    # TEST A: Ist 40 besonders?
    test_A_results = test_A_pivot_comparison(results_all)
    
    # TEST B: EABC-Korrelationen
    test_B_results = test_B_eabc_correlations(results_all)
    
    # TEST C: Strukturelle Eigenschaften
    test_C_results = test_C_structural_properties(results_all)
    
    # TEST D: Randomisierungs-Test
    test_D_results = test_D_randomization(primes, get_coords, results_all[40])
    
    # Erstelle Visualisierungen
    viz_path = OUTPUT_DIR / "pivot_analysis_plots.png"
    create_visualizations(results_all, test_A_results, test_B_results, test_D_results, viz_path)
    
    # Exportiere CSV-Daten für k=40
    print("\n" + "="*80)
    print("EXPORTIERE DATEN")
    print("="*80)
    
    csv_path = OUTPUT_DIR / "pivot_40_data.csv"
    results_40 = results_all[40]
    
    df = pd.DataFrame({
        'p': results_40['p'],
        'd_40': results_40['d_k'],
        'eabc_p': results_40['eabc_p'],
        'e_d': results_40['eabc_d'][:, 0],
        'a_d': results_40['eabc_d'][:, 1],
        'b_d': results_40['eabc_d'][:, 2],
        'c_d': results_40['eabc_d'][:, 3],
        'omega_d': results_40['omega_d'],
        'shell_d': results_40['shell_d'],
        'H_d': results_40['H_d'],
        'E_d': results_40['E_d']
    })
    
    df.to_csv(csv_path, index=False)
    print(f"✓ Daten exportiert: {csv_path}")
    print(f"  Zeilen: {len(df):,}")
    
    # Zusammenfassung speichern (konvertiere numpy-Typen zu Python-Typen)
    summary = {
        'timestamp': datetime.now().isoformat(),
        'config': {
            'prime_limit': int(PRIME_LIMIT),
            'pivots': [int(p) for p in PIVOTS],
            'n_primes': int(len(primes)),
            'n_random_pivots': int(N_RANDOM_PIVOTS)
        },
        'test_A': {
            'is_special': bool(test_A_results['is_special']),
            'var_40_rank': int(test_A_results['var_40_rank']),
            'E_40_rank': int(test_A_results['E_40_rank']),
            'H_40_rank': int(test_A_results['H_40_rank'])
        },
        'test_B': {
            'chi2_40_rank': int(test_B_results['chi2_40_rank'])
        },
        'test_D': {
            'E_percentile': float(test_D_results['E_percentile']),
            'H_percentile': float(test_D_results['H_percentile']),
            'omega_percentile': float(test_D_results['omega_percentile']),
            'chi2_percentile': float(test_D_results['chi2_percentile']),
            'n_extreme': int(test_D_results['n_extreme'])
        }
    }
    
    summary_path = OUTPUT_DIR / "summary.json"
    with open(summary_path, 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"✓ Zusammenfassung gespeichert: {summary_path}")
    
    # FINALE INTERPRETATION
    print("\n" + "="*80)
    print("FINALE INTERPRETATION")
    print("="*80)
    
    # Kombiniere Test A und Test D
    is_special_A = test_A_results['is_special']
    is_special_D = test_D_results['n_extreme'] >= 2
    
    if is_special_A and is_special_D:
        print("\n🔴 ERGEBNIS: Pivot k=40 ist ROBUST BESONDERS!")
        print(f"\nTest A: Extreme Ränge unter {len(PIVOTS)} Kontroll-Pivots")
        print(f"Test D: {test_D_results['n_extreme']}/4 Metriken extrem (< 10% oder > 90% Perzentil)")
        print(f"        unter {N_RANDOM_PIVOTS} zufälligen Pivots")
        print("\nDie Anomalien sind konsistent über verschiedene Vergleichsgruppen.")
        print("Dies deutet auf reale arithmetische Muster hin, die weitere")
        print("Untersuchung verdienen.")
    elif is_special_A:
        print("\n🟡 ERGEBNIS: Pivot k=40 zeigt MODERATE Besonderheiten.")
        print(f"\nTest A: Extreme Ränge unter {len(PIVOTS)} Kontroll-Pivots")
        print(f"Test D: {test_D_results['n_extreme']}/4 Metriken extrem unter zufälligen Pivots")
        print("\nk=40 ist unter den Kontroll-Pivots besonders, aber nicht robust")
        print("extrem im Vergleich zu zufälligen Zahlen. Dies könnte auf ein")
        print("Muster stark zusammengesetzter Zahlen hindeuten.")
    else:
        print("\n🟢 ERGEBNIS: Pivot k=40 ist NICHT statistisch besonders.")
        print("\nDie Werte für k=40 liegen im mittleren Bereich der getesteten Pivots")
        print("und der zufälligen Pivots. Das explorative Diagramm ist interessant,")
        print("aber die EABC-Analyse zeigt keine robusten Anomalien.")
        print("Dies ist ein wichtiges NEGATIVERGEBNIS.")
    
    print("\n" + "="*80)
    print("NÄCHSTE SCHRITTE")
    print("="*80)
    print("\n1. Skaliere auf p < 10^7 für robustere Statistik")
    print("2. Teste Verbindung zu M_C (falls M_C-Daten verfügbar)")
    print("3. Untersuche spezifische EABC-Kombinationen genauer")
    print("4. Erwäge alternative Pivot-Familien (Primorials, Fakultäten, etc.)")
    
    print("\n✓ Analyse abgeschlossen!")
    print(f"  Ergebnisse in: {OUTPUT_DIR.absolute()}")


if __name__ == "__main__":
    main()
