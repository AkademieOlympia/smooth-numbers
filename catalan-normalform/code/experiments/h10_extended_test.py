"""
H10 Extended Test: n=1-1000

Erweiterte Version des H10-Tests mit größerer Stichprobe.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from h10_mc_information_test import *

print('\n' + '='*70)
print('H10 EXTENDED TEST: n=1-1000')
print('='*70)
print()

config = {
    'n_min': 2,
    'n_max': 1000,
    'omega_min': 3,
    'canonization': 'balanced',
    'n_permutations': 500,  # weniger Permutationen für Geschwindigkeit
    'k_folds': 5
}

output_dir = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    'experiments', 'results', 'h10_extended'
)

# 1. Datensatz
print('Datensatz generieren (n=1-1000)...')
numbers = generate_dataset(n_min=config['n_min'], n_max=config['n_max'], omega_min=config['omega_min'])

# 2. Features
print('Features berechnen...')
features = compute_features_h10(numbers, canonization=config['canonization'])

# 3. Modellkaskade
results = run_model_cascade_h10(features)

# 4. Robustheitstests (reduziert für Geschwindigkeit)
print('\nPermutationstest (500 Permutationen)...')
perm_results = permutation_test(features, results, n_permutations=config['n_permutations'])

print('\nCross-Validation...')
cv_results = cross_validation_test(features, k_folds=config['k_folds'])

print('\nResiduenanalyse...')
residual_results = residual_analysis(results, features)

# 5. Interpretation
interpretation = interpret_h10_results(results, perm_results, cv_results, residual_results)

# 6. Visualisierungen
visualize_h10_results(results, features, perm_results, cv_results, residual_results, output_dir)

# 7. Bericht
save_h10_report(results, features, perm_results, cv_results, residual_results, interpretation, output_dir, config)

# Zusammenfassung
print('\n' + '='*70)
print('EXTENDED TEST ZUSAMMENFASSUNG')
print('='*70)
print()
print(f'Datensatz: n ∈ [2, 1000], {len(numbers)} Zahlen')
print(f'ANTWORT: {interpretation["H10_answer"]}')
print(f'ΔR²₂ = {results["Delta_R2_2"]:.6f}')
print(f'p-Wert (Permutation) = {perm_results["p_value"]:.4f}')
print(f'p-Wert (CV) = {cv_results["t_pvalue"]:.4f}')
print()
print('='*70)
