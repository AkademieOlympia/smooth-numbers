"""
Debug Stage C: Verstehe, warum Z = 0.0
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import numpy as np
from utils.eabc import (
    prime_factors_with_multiplicity,
    eabc_class,
    compute_eabc_vector,
    compute_H
)

# Test mit einer einfachen Zahl
n = 210  # = 2 × 3 × 5 × 7

print(f"Original: n = {n}")
factors = prime_factors_with_multiplicity(n)
print(f"Faktoren: {factors}")

# EABC-Klassen
classes = [eabc_class(p) for p in factors]
print(f"EABC-Klassen: {classes}")

# EABC-Vektor
v = compute_eabc_vector(n)
print(f"EABC-Vektor (e, a, b, c): {v}")
print(f"H(n) = {compute_H(n):.6f}")

print("\n" + "="*60)
print("PERMUTATION TEST")
print("="*60)

# Permutation: E↔A, B↔C
perm_map = {'E': 'A', 'A': 'E', 'B': 'C', 'C': 'B'}

representatives = {
    'E': 13,
    'A': 5,
    'B': 7,
    'C': 11
}

permuted_factors = []
for p in factors:
    cls = eabc_class(p)
    if cls == 'shell':
        permuted_factors.append(p)
    else:
        new_cls = perm_map.get(cls, cls)
        permuted_factors.append(representatives[new_cls])

print(f"\nPermutierte Faktoren: {permuted_factors}")

n_perm = int(np.prod(permuted_factors))
print(f"Permutierte Zahl: n_perm = {n_perm}")

# EABC der permutierten Zahl
v_perm = compute_eabc_vector(n_perm)
print(f"EABC-Vektor (permutiert): {v_perm}")
print(f"H(n_perm) = {compute_H(n_perm):.6f}")

print("\n" + "="*60)
print("MULTIPLE PERMUTATIONS")
print("="*60)

H_vals_perm = []
for i in range(10):
    # Zufällige Permutation
    classes_list = ['E', 'A', 'B', 'C']
    perm_classes = np.random.permutation(classes_list)
    perm_map_rand = {orig: perm for orig, perm in zip(classes_list, perm_classes)}
    
    permuted_factors_rand = []
    for p in factors:
        cls = eabc_class(p)
        if cls == 'shell':
            permuted_factors_rand.append(p)
        else:
            new_cls = perm_map_rand.get(cls, cls)
            permuted_factors_rand.append(representatives[new_cls])
    
    n_perm_rand = int(np.prod(permuted_factors_rand))
    H_perm = compute_H(n_perm_rand)
    H_vals_perm.append(H_perm)
    
    print(f"Perm {i+1}: n_perm = {n_perm_rand}, H = {H_perm:.6f}")

print(f"\nH (original) = {compute_H(n):.6f}")
print(f"H (perm, mean) = {np.nanmean(H_vals_perm):.6f}")
print(f"H (perm, std) = {np.nanstd(H_vals_perm):.6f}")

print("\n" + "="*60)
print("PROBLEM ANALYSIS")
print("="*60)

# Prüfe ob Permutation überhaupt etwas ändert
unique_perms = len(set([x for x in H_vals_perm if not np.isnan(x)]))
print(f"\nAnzahl einzigartiger H-Werte: {unique_perms}")

if unique_perms == 1:
    print("\n⚠️ PROBLEM: Alle permutierten H-Werte sind GLEICH!")
    print("Das bedeutet: Die Permutation ändert H(n) nicht.")
    print("\nMÖGLICHE URSACHEN:")
    print("1. H(n) hängt nur von |v|, nicht von der Verteilung ab")
    print("2. Die Permutation ändert die Faktorstruktur nicht richtig")
    print("3. Der Test ist konzeptionell falsch")
