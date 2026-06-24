"""
EABC-sensitive Catalan-Magic M_{C,EABC}(T)

Implementiert EABC-gewichtete Baummetriken, die die EABC-Verteilung
der Primfaktoren in Teilbäumen berücksichtigen.

Zwei Varianten:
1. M_{C,EABC}^{simple} = M_C(T) * E(n)  (Produkt)
2. M_{C,EABC}^{subtree} = Σ |E(T_L) - E(T_R)|  (Teilbaum-Differenzen)

Autor: H12-B Framework
Datum: 2026-06-24
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from catalan_trees import BinaryTree
from typing import Optional, List
import numpy as np


def compute_subtree_eabc_entropy(tree: BinaryTree, factor_eabc_classes: List[str]) -> float:
    """
    Berechnet EABC-Entropie eines Teilbaums.
    
    Args:
        tree: BinaryTree-Knoten
        factor_eabc_classes: Liste der EABC-Klassen ('E', 'A', 'B', 'C', 'shell')
                            für jeden Primfaktor (in Reihenfolge der Blätter)
    
    Returns:
        Shannon-Entropie der EABC-Verteilung im Teilbaum
    """
    if tree.is_leaf:
        # Einzelnes Blatt: Entropie = 0 (perfekte Konzentration)
        return 0.0
    
    # Sammle alle Blätter des Teilbaums (in Pre-order)
    def collect_leaves_indices(node: BinaryTree, start_idx: int = 0) -> List[int]:
        """Sammelt Indizes aller Blätter in einem Teilbaum."""
        if node.is_leaf:
            return [start_idx]
        
        # Linker Teilbaum
        left_indices = collect_leaves_indices(node.left, start_idx) if node.left else []
        # Rechter Teilbaum (Offset = Größe linker Teilbaum)
        left_size = len(left_indices)
        right_indices = collect_leaves_indices(node.right, start_idx + left_size) if node.right else []
        
        return left_indices + right_indices
    
    leaf_indices = collect_leaves_indices(tree)
    
    # Zähle EABC-Klassen in diesem Teilbaum
    counts = {'E': 0, 'A': 0, 'B': 0, 'C': 0}
    for idx in leaf_indices:
        if idx < len(factor_eabc_classes):
            cls = factor_eabc_classes[idx]
            if cls in counts:
                counts[cls] += 1
    
    total = sum(counts.values())
    
    if total == 0:
        # Keine EABC-Faktoren (nur 2, 3)
        return 0.0
    
    # Shannon-Entropie
    entropy = 0.0
    for count in counts.values():
        if count > 0:
            p = count / total
            entropy -= p * np.log(p)
    
    return entropy


def mc_eabc_simple(tree: BinaryTree, n: int, base_mc: float) -> float:
    """
    EABC-sensitive Catalan-Magic (einfache Variante).
    
    M_{C,EABC}^{simple}(T, n) = M_C(T) * E(n)
    
    Idee: Gewichte Baumasymmetrie mit globaler EABC-Entropie.
    
    Args:
        tree: Faktorisierungsbaum
        n: Die Zahl (für EABC-Berechnung)
        base_mc: Bereits berechnetes M_C(T)
    
    Returns:
        M_{C,EABC}^{simple}
    """
    from utils.eabc import prime_factors_with_multiplicity, eabc_class
    
    factors = prime_factors_with_multiplicity(n)
    
    # Berechne EABC-Entropie
    counts = {'E': 0, 'A': 0, 'B': 0, 'C': 0}
    for p in factors:
        if p > 3:
            cls = eabc_class(p)
            if cls in counts:
                counts[cls] += 1
    
    total = sum(counts.values())
    
    if total == 0:
        # Keine EABC-Faktoren
        return 0.0
    
    entropy = 0.0
    for count in counts.values():
        if count > 0:
            p_val = count / total
            entropy -= p_val * np.log(p_val)
    
    return base_mc * entropy


def mc_eabc_subtree(tree: BinaryTree, factor_eabc_classes: List[str]) -> float:
    """
    EABC-sensitive Catalan-Magic (Teilbaum-Variante).
    
    M_{C,EABC}^{subtree}(T) = Σ_{v∈T} |E(T_L(v)) - E(T_R(v))|
    
    wobei E(T_L) die EABC-Entropie des linken Teilbaums ist.
    
    Idee: Misst EABC-Ungleichgewicht in der Baumstruktur.
    
    Args:
        tree: Faktorisierungsbaum
        factor_eabc_classes: Liste der EABC-Klassen für jeden Primfaktor
    
    Returns:
        M_{C,EABC}^{subtree}
    """
    if tree.is_leaf:
        return 0.0
    
    # Entropien der Teilbäume
    left_entropy = 0.0
    right_entropy = 0.0
    
    if tree.left and not tree.left.is_leaf:
        # Bestimme, welche Faktoren im linken Teilbaum sind
        left_size = tree.left.num_leaves
        left_classes = factor_eabc_classes[:left_size]
        left_entropy = compute_subtree_eabc_entropy(tree.left, left_classes)
    
    if tree.right and not tree.right.is_leaf:
        # Bestimme, welche Faktoren im rechten Teilbaum sind
        left_size = tree.left.num_leaves if tree.left else 0
        right_classes = factor_eabc_classes[left_size:]
        right_entropy = compute_subtree_eabc_entropy(tree.right, right_classes)
    
    # Lokales Ungleichgewicht
    local_imbalance = abs(left_entropy - right_entropy)
    
    # Rekursive Beiträge
    left_imbalance = 0.0
    right_imbalance = 0.0
    
    if tree.left and not tree.left.is_leaf:
        left_size = tree.left.num_leaves
        left_classes = factor_eabc_classes[:left_size]
        left_imbalance = mc_eabc_subtree(tree.left, left_classes)
    
    if tree.right and not tree.right.is_leaf:
        left_size = tree.left.num_leaves if tree.left else 0
        right_classes = factor_eabc_classes[left_size:]
        right_imbalance = mc_eabc_subtree(tree.right, right_classes)
    
    return local_imbalance + left_imbalance + right_imbalance


def compute_mc_eabc(n: int, method: str = 'balanced', variant: str = 'simple') -> float:
    """
    Berechnet EABC-sensitive Catalan-Magic für Zahl n.
    
    Args:
        n: Natürliche Zahl ≥ 2
        method: Kanonisierungsmethode (siehe canonization.py)
        variant: Variante der EABC-Metrik
            - 'simple': M_C(T) * E(n)
            - 'subtree': Σ |E(T_L) - E(T_R)|
    
    Returns:
        M_{C,EABC}(n)
    """
    from utils.canonization import canonize_number
    from utils.catalan_magic import compute_catalan_magic
    from utils.eabc import prime_factors_with_multiplicity, eabc_class
    
    # Kanonisiere
    tree = canonize_number(n, method=method)
    
    # Berechne EABC-Klassen der Faktoren
    factors = prime_factors_with_multiplicity(n)
    factor_classes = [eabc_class(p) for p in factors]
    
    if variant == 'simple':
        # Einfache Variante: M_C * E(n)
        base_mc = compute_catalan_magic(n, method=method, metric='depth')
        return mc_eabc_simple(tree, n, base_mc)
    
    elif variant == 'subtree':
        # Teilbaum-Variante: Σ |E(T_L) - E(T_R)|
        return mc_eabc_subtree(tree, factor_classes)
    
    else:
        raise ValueError(f"Unbekannte Variante: {variant}")


# Beispieltest
if __name__ == "__main__":
    print("EABC-sensitive Catalan-Magic Tests:")
    print()
    
    test_numbers = [
        (60, [2, 2, 3, 5]),
        (210, [2, 3, 5, 7]),
        (2310, [2, 3, 5, 7, 11]),
        (30030, [2, 3, 5, 7, 11, 13])
    ]
    
    for n, factors in test_numbers:
        print(f"n = {n} = {' × '.join(map(str, factors))}")
        
        from utils.catalan_magic import compute_catalan_magic
        M_C = compute_catalan_magic(n, method='balanced', metric='depth')
        M_C_EABC_simple = compute_mc_eabc(n, method='balanced', variant='simple')
        M_C_EABC_subtree = compute_mc_eabc(n, method='balanced', variant='subtree')
        
        print(f"  M_C                 = {M_C:.4f}")
        print(f"  M_{{C,EABC}}^{{simple}} = {M_C_EABC_simple:.4f}")
        print(f"  M_{{C,EABC}}^{{subtree}} = {M_C_EABC_subtree:.4f}")
        print()
