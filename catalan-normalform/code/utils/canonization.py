"""
Kanonisierungsmethoden n → T(n).

Implementiert verschiedene Heuristiken zur kanonischen Wahl
eines binären Faktorisierungsbaums aus der Primfaktorzerlegung.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from catalan_trees import BinaryTree, construct_left_tree, construct_right_tree, construct_balanced_tree
from utils.eabc import prime_factors_with_multiplicity, eabc_class
from typing import List


def canonize_number(n: int, method: str = 'balanced') -> BinaryTree:
    """
    Kanonisiert Zahl n zu einem binären Faktorisierungsbaum.
    
    Args:
        n: Natürliche Zahl ≥ 2
        method: Kanonisierungsmethode
            - 'left': Linksbaum (((a·b)·c)·d)
            - 'right': Rechtsbaum (a·(b·(c·d)))
            - 'balanced': Balancierter Baum (rekursive Halbierung)
            - 'lex': Lexikographisch (nach (v₂, v₃, p₁, p₂, ...))
            - 'smallest_first': Kleinste Primzahl zuerst, dann balanciert
            - 'largest_first': Größte Primzahl zuerst, dann balanciert
            - 'eabc_grouped': Gruppiert nach EABC-Klassen
            
    Returns:
        BinaryTree mit Primfaktoren als Blätter
    """
    factors = prime_factors_with_multiplicity(n)
    
    if len(factors) == 0:
        raise ValueError(f"Zahl {n} hat keine Primfaktoren")
    
    if len(factors) == 1:
        return BinaryTree(value=factors[0])
    
    # Wende Kanonisierungsmethode an
    if method == 'left':
        return construct_left_tree(factors)
    
    elif method == 'right':
        return construct_right_tree(factors)
    
    elif method == 'balanced':
        return construct_balanced_tree(factors)
    
    elif method == 'lex':
        # Lexikographische Ordnung: v₂, v₃, dann aufsteigende Primzahlen
        # Faktoren sind bereits in aufsteigender Reihenfolge (aus prime_factors_with_multiplicity)
        return construct_balanced_tree(factors)
    
    elif method == 'smallest_first':
        # Sortiere Faktoren aufsteigend
        sorted_factors = sorted(factors)
        return construct_balanced_tree(sorted_factors)
    
    elif method == 'largest_first':
        # Sortiere Faktoren absteigend
        sorted_factors = sorted(factors, reverse=True)
        return construct_balanced_tree(sorted_factors)
    
    elif method == 'eabc_grouped':
        # Gruppiere nach EABC-Klassen: Shell (2, 3), E, A, B, C
        shell_factors = [p for p in factors if p in [2, 3]]
        e_factors = [p for p in factors if eabc_class(p) == 'E']
        a_factors = [p for p in factors if eabc_class(p) == 'A']
        b_factors = [p for p in factors if eabc_class(p) == 'B']
        c_factors = [p for p in factors if eabc_class(p) == 'C']
        
        # Konkateniere in Reihenfolge
        grouped_factors = shell_factors + e_factors + a_factors + b_factors + c_factors
        return construct_balanced_tree(grouped_factors)
    
    else:
        raise ValueError(f"Unbekannte Kanonisierungsmethode: {method}")


def all_canonization_methods() -> List[str]:
    """Liste aller verfügbaren Kanonisierungsmethoden."""
    return [
        'left',
        'right',
        'balanced',
        'lex',
        'smallest_first',
        'largest_first',
        'eabc_grouped'
    ]


# Beispieltest
if __name__ == "__main__":
    print("Kanonisierungs-Tests:")
    print()
    
    n = 60  # 2² × 3 × 5
    
    for method in all_canonization_methods():
        tree = canonize_number(n, method=method)
        print(f"{method:20s}: {tree}")
    
    print()
    print("Vergleich für n = 210 (2 × 3 × 5 × 7):")
    n = 210
    
    for method in ['left', 'right', 'balanced']:
        tree = canonize_number(n, method=method)
        print(f"{method:20s}: height = {tree.height}, tree = {tree}")
