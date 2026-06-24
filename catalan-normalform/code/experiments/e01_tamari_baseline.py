"""
E01: Tamari-Baseline - Nüchterner Grundatlas

Ziel: Den kombinatorischen Catalan-Raum ohne arithmetische Aspekte vermessen.

Lieferables:
1. Tabelle mit Grundstatistiken für k=2,...,12
2. Spektrum des Laplace-Operators L_C^(k)
3. Visualisierung von Γ_4, Γ_5
"""

import numpy as np
import networkx as nx
from typing import List, Tuple, Set
from dataclasses import dataclass
import pandas as pd

@dataclass
class CatalanAtlasEntry:
    """Eintrag im Grundatlas des Catalan-Raums."""
    k: int
    num_trees: int  # |T_k| = C_{k-1}
    num_edges: int
    diameter: int
    num_balanced: int  # |B_k|
    mean_dist_to_balanced: float
    lambda_1: float  # Spektrallücke
    spectral_gap: float


class BinaryTree:
    """Binärer Baum mit k Blättern."""
    
    def __init__(self, left=None, right=None):
        self.left = left
        self.right = right
    
    def is_leaf(self) -> bool:
        return self.left is None and self.right is None
    
    def num_leaves(self) -> int:
        if self.is_leaf():
            return 1
        return self.left.num_leaves() + self.right.num_leaves()
    
    def height(self) -> int:
        if self.is_leaf():
            return 0
        return 1 + max(self.left.height(), self.right.height())
    
    def is_balanced(self) -> bool:
        """Prüft, ob Baum minimale Höhe hat."""
        k = self.num_leaves()
        min_height = int(np.ceil(np.log2(k)))
        return self.height() == min_height
    
    def __hash__(self):
        if self.is_leaf():
            return hash("leaf")
        return hash(("node", self.left, self.right))
    
    def __eq__(self, other):
        if not isinstance(other, BinaryTree):
            return False
        if self.is_leaf() and other.is_leaf():
            return True
        if self.is_leaf() or other.is_leaf():
            return False
        return self.left == other.left and self.right == other.right
    
    def __repr__(self):
        if self.is_leaf():
            return "•"
        return f"({self.left}{self.right})"


def enumerate_all_trees(k: int) -> List[BinaryTree]:
    """
    Enumeriert alle binären Bäume mit k Blättern.
    Verwendet Catalan-Rekursion.
    """
    if k == 1:
        return [BinaryTree()]
    
    trees = []
    for m in range(1, k):
        n = k - m
        left_trees = enumerate_all_trees(m)
        right_trees = enumerate_all_trees(n)
        for left in left_trees:
            for right in right_trees:
                trees.append(BinaryTree(left, right))
    
    return trees


def is_tamari_rotation(t1: BinaryTree, t2: BinaryTree) -> bool:
    """
    Prüft, ob t1 und t2 durch eine Tamari-Rotation verbunden sind.
    
    Rotation: ((A B) C) ↔ (A (B C))
    """
    # Rotation nach rechts: ((AB)C) → (A(BC))
    if (not t1.is_leaf() and 
        not t1.left.is_leaf() and
        not t2.is_leaf() and
        not t2.right.is_leaf()):
        # Prüfe ((AB)C) → (A(BC))
        if (t1.left.left == t2.left and
            t1.left.right == t2.right.left and
            t1.right == t2.right.right):
            return True
        # Prüfe (A(BC)) → ((AB)C)
        if (t2.left.left == t1.left and
            t2.left.right == t1.right.left and
            t2.right == t1.right.right):
            return True
    
    return False


def construct_tamari_graph(k: int) -> nx.Graph:
    """Konstruiert den Tamari-Graphen Γ_k."""
    trees = enumerate_all_trees(k)
    G = nx.Graph()
    
    # Knoten hinzufügen
    for i, t in enumerate(trees):
        G.add_node(i, tree=t)
    
    # Kanten hinzufügen
    for i, t1 in enumerate(trees):
        for j, t2 in enumerate(trees):
            if i < j and is_tamari_rotation(t1, t2):
                G.add_edge(i, j)
    
    return G


def find_balanced_trees(k: int) -> List[int]:
    """Findet alle balancierten Bäume mit k Blättern."""
    trees = enumerate_all_trees(k)
    balanced = []
    for i, t in enumerate(trees):
        if t.is_balanced():
            balanced.append(i)
    return balanced


def compute_atlas_entry(k: int) -> CatalanAtlasEntry:
    """
    Berechnet alle Statistiken für k Blätter.
    
    Dies ist die Kernfunktion von E01.
    """
    print(f"Computing atlas for k={k}...")
    
    # Graph konstruieren
    G = construct_tamari_graph(k)
    trees = enumerate_all_trees(k)
    
    # Grundstatistik
    num_trees = len(trees)
    num_edges = G.number_of_edges()
    
    # Durchmesser
    diameter = nx.diameter(G)
    
    # Balancierte Bäume
    balanced = find_balanced_trees(k)
    num_balanced = len(balanced)
    
    # Mittlere Distanz zu balancierten Bäumen
    distances = []
    for i in G.nodes():
        dist_to_balanced = min(
            nx.shortest_path_length(G, i, b)
            for b in balanced
        )
        distances.append(dist_to_balanced)
    mean_dist_to_balanced = np.mean(distances)
    
    # Laplace-Spektrum
    L = nx.laplacian_matrix(G).toarray()
    eigenvalues = np.linalg.eigvalsh(L)
    eigenvalues = np.sort(eigenvalues)
    
    lambda_0 = eigenvalues[0]  # Sollte ≈0 sein
    lambda_1 = eigenvalues[1]  # Spektrallücke
    spectral_gap = lambda_1 - lambda_0
    
    return CatalanAtlasEntry(
        k=k,
        num_trees=num_trees,
        num_edges=num_edges,
        diameter=diameter,
        num_balanced=num_balanced,
        mean_dist_to_balanced=mean_dist_to_balanced,
        lambda_1=lambda_1,
        spectral_gap=spectral_gap
    )


def create_catalan_atlas(k_max: int = 12) -> pd.DataFrame:
    """
    Erstellt den vollständigen Grundatlas für k=2,...,k_max.
    
    Dies ist die Hauptfunktion von E01.
    """
    entries = []
    
    for k in range(2, k_max + 1):
        entry = compute_atlas_entry(k)
        entries.append({
            'k': entry.k,
            'C_{k-1}': entry.num_trees,
            'edges': entry.num_edges,
            'diameter': entry.diameter,
            '|B_k|': entry.num_balanced,
            'mean_dist_to_balanced': f"{entry.mean_dist_to_balanced:.3f}",
            'λ_1(L_C)': f"{entry.lambda_1:.4f}",
            'spectral_gap': f"{entry.spectral_gap:.4f}"
        })
    
    return pd.DataFrame(entries)


def verify_catalan_numbers(k_max: int = 12):
    """Verifiziert, dass |T_k| = C_{k-1}."""
    print("Verifying Catalan numbers...")
    
    def catalan(n):
        if n <= 1:
            return 1
        c = [0] * (n + 1)
        c[0], c[1] = 1, 1
        for i in range(2, n + 1):
            for j in range(i):
                c[i] += c[j] * c[i-1-j]
        return c[n]
    
    for k in range(2, k_max + 1):
        trees = enumerate_all_trees(k)
        expected = catalan(k - 1)
        actual = len(trees)
        status = "✓" if actual == expected else "✗"
        print(f"k={k}: |T_k|={actual}, C_{k-1}={expected} {status}")


if __name__ == "__main__":
    print("=" * 60)
    print("E01: Tamari-Baseline - Grundatlas des Catalan-Raums")
    print("=" * 60)
    print()
    
    # Schritt 1: Verifikation
    verify_catalan_numbers(k_max=8)
    print()
    
    # Schritt 2: Atlas erstellen
    print("Creating Catalan atlas...")
    atlas = create_catalan_atlas(k_max=8)  # Start mit k≤8, dann erweitern
    print()
    print(atlas.to_string(index=False))
    print()
    
    # Schritt 3: Atlas speichern
    output_path = "../../data/tamari/catalan_atlas.csv"
    atlas.to_csv(output_path, index=False)
    print(f"Atlas saved to: {output_path}")
    print()
    
    print("=" * 60)
    print("E01 completed: Grundatlas ist vermessen.")
    print("Nächster Schritt: Visualisierung (optional)")
    print("Dann: E02 Kanonisierungstest")
    print("=" * 60)
