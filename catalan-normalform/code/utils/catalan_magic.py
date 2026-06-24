"""
Catalan-Magic M_C(T): Messung der Baum-Asymmetrie.

Implementiert verschiedene Metriken zur Quantifizierung
der Asymmetrie/Unbalanciertheit von Faktorisierungsbäumen.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from catalan_trees import BinaryTree
from typing import Optional
import numpy as np


def tree_depth_imbalance(tree: BinaryTree, node_weights: Optional[dict] = None) -> float:
    """
    Berechnet Tiefen-Ungleichgewicht des Baums.
    
    M_C(T) = Σ |depth(left) - depth(right)| über alle inneren Knoten
    
    Dies ist eine einfache Metrik für Asymmetrie:
    - M_C = 0: Perfekt balancierter Baum
    - M_C > 0: Unbalanciert (größer = asymmetrischer)
    
    Args:
        tree: BinaryTree
        node_weights: Optional, für gewichtete Variante
        
    Returns:
        Ungleichgewichts-Score (float ≥ 0)
    """
    if tree.is_leaf:
        return 0.0
    
    # Tiefen der Teilbäume
    left_depth = tree.left.height if tree.left else 0
    right_depth = tree.right.height if tree.right else 0
    
    # Lokales Ungleichgewicht
    local_imbalance = abs(left_depth - right_depth)
    
    # Rekursive Beiträge von Teilbäumen
    left_imbalance = tree_depth_imbalance(tree.left) if tree.left and not tree.left.is_leaf else 0.0
    right_imbalance = tree_depth_imbalance(tree.right) if tree.right and not tree.right.is_leaf else 0.0
    
    return local_imbalance + left_imbalance + right_imbalance


def tree_size_imbalance(tree: BinaryTree) -> float:
    """
    Größen-basiertes Ungleichgewicht.
    
    M_C(T) = Σ |size(left) - size(right)| über alle inneren Knoten
    
    wobei size = Anzahl Blätter im Teilbaum.
    """
    if tree.is_leaf:
        return 0.0
    
    left_size = tree.left.num_leaves if tree.left else 0
    right_size = tree.right.num_leaves if tree.right else 0
    
    local_imbalance = abs(left_size - right_size)
    
    left_imbalance = tree_size_imbalance(tree.left) if tree.left and not tree.left.is_leaf else 0.0
    right_imbalance = tree_size_imbalance(tree.right) if tree.right and not tree.right.is_leaf else 0.0
    
    return local_imbalance + left_imbalance + right_imbalance


def tree_total_depth(tree: BinaryTree, current_depth: int = 0) -> float:
    """
    Summe aller Blatttiefen (gewichtete Pfadlänge).
    
    Äquivalent zu "external path length" in der Informatik.
    Minimiert für balancierten Baum.
    """
    if tree.is_leaf:
        return current_depth
    
    left_depth = tree_total_depth(tree.left, current_depth + 1) if tree.left else 0
    right_depth = tree_total_depth(tree.right, current_depth + 1) if tree.right else 0
    
    return left_depth + right_depth


def tree_tamari_distance_to_balanced(tree: BinaryTree) -> int:
    """
    Approximierte Tamari-Distanz zu balanciertem Baum.
    
    Exakte Berechnung der Tamari-Distanz ist komplex.
    Diese Funktion gibt eine obere Schranke durch Rotation-Counting.
    
    Für kleine Bäume: Zähle minimale Rotationen zu perfekt balanciertem Baum.
    """
    # TODO: Implementiere exakte Tamari-Distanz für vollständige Version
    # Für E02: Verwende Tiefen-Ungleichgewicht als Proxy
    return tree_depth_imbalance(tree)


def tree_colless_index(tree: BinaryTree) -> float:
    """
    Colless-Index: Klassisches Maß für Baum-Ungleichgewicht.
    
    Colless(T) = Σ |n_L - n_R| über alle inneren Knoten
    wobei n_L, n_R = Anzahl Knoten in linkem/rechtem Teilbaum
    
    Normiert durch (k-1)(k-2)/2 für k Blätter.
    """
    if tree.is_leaf:
        return 0.0
    
    def count_nodes(t: BinaryTree) -> int:
        if t is None:
            return 0
        if t.is_leaf:
            return 1
        return 1 + count_nodes(t.left) + count_nodes(t.right)
    
    left_nodes = count_nodes(tree.left) if tree.left else 0
    right_nodes = count_nodes(tree.right) if tree.right else 0
    
    local_imbalance = abs(left_nodes - right_nodes)
    
    left_imbalance = tree_colless_index(tree.left) if tree.left and not tree.left.is_leaf else 0.0
    right_imbalance = tree_colless_index(tree.right) if tree.right and not tree.right.is_leaf else 0.0
    
    return local_imbalance + left_imbalance + right_imbalance


def compute_catalan_magic(n: int, method: str = 'balanced', metric: str = 'depth') -> float:
    """
    Berechnet Catalan-Magic für Zahl n.
    
    M_C(n) = M_C(κ(n))
    
    wobei κ: n → T(n) eine Kanonisierung ist.
    
    Args:
        n: Natürliche Zahl ≥ 2
        method: Kanonisierungsmethode (siehe canonization.py)
        metric: Metrik zur Messung der Asymmetrie
            - 'depth': Tiefen-Ungleichgewicht (Standard)
            - 'size': Größen-Ungleichgewicht
            - 'total_depth': Totale Pfadlänge
            - 'colless': Colless-Index
            - 'tamari': Tamari-Distanz zu balanciert (approximiert)
            
    Returns:
        M_C(n) ≥ 0
    """
    from utils.canonization import canonize_number
    
    tree = canonize_number(n, method=method)
    
    if metric == 'depth':
        return tree_depth_imbalance(tree)
    elif metric == 'size':
        return tree_size_imbalance(tree)
    elif metric == 'total_depth':
        return tree_total_depth(tree)
    elif metric == 'colless':
        return tree_colless_index(tree)
    elif metric == 'tamari':
        return tree_tamari_distance_to_balanced(tree)
    else:
        raise ValueError(f"Unbekannte Metrik: {metric}")


def normalized_catalan_magic(n: int, method: str = 'balanced', metric: str = 'depth') -> float:
    """
    Normierte Catalan-Magic M̃_C(n) ∈ [0, 1].
    
    Normiert durch maximales Ungleichgewicht bei k Blättern.
    """
    from utils.eabc import count_prime_factors
    
    k = count_prime_factors(n)
    M_C = compute_catalan_magic(n, method=method, metric=metric)
    
    # Maximales Ungleichgewicht: Linksbaum oder Rechtsbaum
    # Für depth-Metrik: ≈ (k-1)(k-2)/2
    max_imbalance = (k - 1) * (k - 2) / 2 if k > 2 else 1
    
    if max_imbalance == 0:
        return 0.0
    
    return M_C / max_imbalance


# Beispieltest
if __name__ == "__main__":
    print("Catalan-Magic Tests:")
    print()
    
    test_numbers = [
        (6, [2, 3]),
        (12, [2, 2, 3]),
        (30, [2, 3, 5]),
        (60, [2, 2, 3, 5]),
        (210, [2, 3, 5, 7])
    ]
    
    for n, factors in test_numbers:
        print(f"n = {n} = {' × '.join(map(str, factors))}")
        
        for method in ['left', 'balanced', 'right']:
            M_C = compute_catalan_magic(n, method=method, metric='depth')
            M_C_norm = normalized_catalan_magic(n, method=method, metric='depth')
            print(f"  {method:10s}: M_C = {M_C:6.2f}, M̃_C = {M_C_norm:.4f}")
        
        print()
