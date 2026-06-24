# Catalan-Laplacian Design-Spezifikation

**Version:** 1.0  
**Datum:** 2026-06-24  
**Übergeordnetes Dokument:** `H14_SPECTRAL_THEORY.md`

---

## 🎯 DESIGN-ZIELE

1. **Modularität:** Jede Graph-Variante (A, B, C, D) ist unabhängig testbar
2. **Erweiterbarkeit:** Neue Graphen/Metriken einfach hinzufügbar
3. **Performance:** Effizient für n ≤ 10000
4. **Reproduzierbarkeit:** Deterministisch, gut dokumentiert
5. **Testbarkeit:** Unit-Tests für alle Komponenten

---

## 📐 ARCHITEKTUR

### Modul-Struktur

```
code/
├── utils/
│   ├── graph_laplacian.py       ← NEU: Graph-Konstruktion & Laplacian
│   ├── pde_solvers.py            ← NEU: PDE-Simulatoren
│   ├── tamari_graph.py           ← NEU: Tamari-spezifische Funktionen
│   ├── eabc.py                   ← EXISTIERT: EABC-Funktionen
│   ├── catalan_trees.py          ← EXISTIERT: Baum-Strukturen
│   └── catalan_magic.py          ← EXISTIERT: M_C-Metriken
├── experiments/
│   ├── h14_spectral_theory.py    ← NEU: Hauptexperiment
│   ├── h14_heat_flow.py          ← NEU: Heat-Flow-Simulationen
│   ├── h14_harmonicity.py        ← NEU: Harmonizitäts-Tests
│   └── h14_visualizations.py     ← NEU: Plots & Animationen
└── tests/
    ├── test_graph_laplacian.py   ← NEU: Unit-Tests
    └── test_pde_solvers.py       ← NEU: Unit-Tests
```

---

## 🔧 DETAILLIERTES DESIGN

### 1. `graph_laplacian.py`

#### Klassen-Hierarchie

```python
from abc import ABC, abstractmethod
import networkx as nx
import numpy as np
from typing import List, Tuple, Optional

class GraphLaplacian(ABC):
    """
    Abstrakte Basisklasse für Graph-Laplacians.
    """
    
    def __init__(self, numbers: List[int]):
        self.numbers = numbers
        self.graph = None
        self.laplacian = None
        self.eigenvalues = None
        self.eigenvectors = None
    
    @abstractmethod
    def construct_graph(self) -> nx.Graph:
        """Konstruiert Graph G."""
        pass
    
    def compute_laplacian(self, weight_key='weight') -> np.ndarray:
        """
        Berechnet Laplace-Matrix L = D - A.
        
        Returns:
            L: Scipy sparse matrix (CSR format)
        """
        if self.graph is None:
            self.construct_graph()
        
        self.laplacian = nx.laplacian_matrix(
            self.graph, 
            weight=weight_key
        )
        return self.laplacian
    
    def compute_spectrum(self, k: Optional[int] = None):
        """
        Berechnet Eigenwerte und -vektoren.
        
        Args:
            k: Anzahl kleinster Eigenwerte (None = alle)
        """
        import scipy.sparse.linalg as spla
        
        if self.laplacian is None:
            self.compute_laplacian()
        
        n = self.laplacian.shape[0]
        
        if k is None or k >= n:
            # Alle Eigenwerte (dichte Matrix)
            L_dense = self.laplacian.toarray()
            self.eigenvalues, self.eigenvectors = np.linalg.eigh(L_dense)
        else:
            # Erste k Eigenwerte (sparse)
            self.eigenvalues, self.eigenvectors = spla.eigsh(
                self.laplacian, 
                k=min(k, n-1), 
                which='SM'  # Smallest Magnitude
            )
        
        return self.eigenvalues, self.eigenvectors
    
    def rayleigh_quotient(self, f: np.ndarray) -> float:
        """
        R(f) = ⟨f, Lf⟩ / ⟨f, f⟩
        """
        if self.laplacian is None:
            self.compute_laplacian()
        
        numerator = f.T @ (self.laplacian @ f)
        denominator = f.T @ f
        
        if denominator == 0:
            return np.inf
        
        return numerator / denominator
    
    def fiedler_value(self) -> float:
        """
        Zweitkleinster Eigenwert (algebraische Konnektivität).
        """
        if self.eigenvalues is None:
            self.compute_spectrum(k=10)
        
        # Sortiere falls nötig
        sorted_eigs = np.sort(self.eigenvalues)
        
        return sorted_eigs[1]
    
    def spectral_gap(self) -> float:
        """
        λ₁ - λ₀
        """
        if self.eigenvalues is None:
            self.compute_spectrum(k=10)
        
        sorted_eigs = np.sort(self.eigenvalues)
        return sorted_eigs[1] - sorted_eigs[0]
```

#### Variante A: EABC-Graph

```python
class EABCGraphLaplacian(GraphLaplacian):
    """
    EABC-Nachbarschaftsgraph basierend auf EABC-Vektor-Distanz.
    """
    
    def __init__(self, numbers: List[int], threshold: float = 2.0):
        super().__init__(numbers)
        self.threshold = threshold
    
    def construct_graph(self) -> nx.Graph:
        """
        Konstruiert EABC-Graph.
        
        Knoten: numbers
        Kanten: d_EABC(n, m) < threshold
        Gewichte: exp(-d_EABC(n, m))
        """
        from utils.eabc import eabc_vector
        
        G = nx.Graph()
        G.add_nodes_from(self.numbers)
        
        # EABC-Vektoren berechnen
        eabc_vecs = {}
        for n in self.numbers:
            eabc_vecs[n] = eabc_vector(n)
        
        # Kanten hinzufügen
        for i, n in enumerate(self.numbers):
            for m in self.numbers[i+1:]:
                d = np.linalg.norm(
                    np.array(eabc_vecs[n]) - np.array(eabc_vecs[m])
                )
                
                if d < self.threshold:
                    w = np.exp(-d)
                    G.add_edge(n, m, weight=w)
        
        self.graph = G
        return G
```

#### Variante B: Tamari-Graph

```python
class TamariGraphLaplacian(GraphLaplacian):
    """
    Tamari-Graph für k Blätter.
    """
    
    def __init__(self, k: int):
        # numbers = indices der Catalan-Bäume
        super().__init__(list(range(catalan_number(k-1))))
        self.k = k
        self.trees = None
    
    def construct_graph(self) -> nx.Graph:
        """
        Konstruiert Tamari-Graph für k Blätter.
        
        Knoten: Catalan-Bäume (indiziert 0, 1, ..., C_{k-1}-1)
        Kanten: Tamari-Rotationen
        Gewichte: 1 (ungewichtet)
        """
        from catalan_trees import generate_all_trees
        from utils.tamari_graph import are_tamari_neighbors
        
        self.trees = generate_all_trees(self.k)
        
        G = nx.Graph()
        G.add_nodes_from(range(len(self.trees)))
        
        # Kanten: Tamari-Relationen
        for i, T1 in enumerate(self.trees):
            for j, T2 in enumerate(self.trees[i+1:], start=i+1):
                if are_tamari_neighbors(T1, T2):
                    G.add_edge(i, j, weight=1.0)
        
        self.graph = G
        return G
```

#### Variante C: Faktorisierungs-Graph

```python
class FactorizationGraphLaplacian(GraphLaplacian):
    """
    Faktorisierungs-Graph basierend auf gemeinsamen Primfaktoren.
    """
    
    def construct_graph(self) -> nx.Graph:
        """
        Konstruiert Faktorisierungs-Graph.
        
        Knoten: numbers
        Kanten: Gemeinsame Primfaktoren
        Gewichte: Anzahl gemeinsamer Faktoren
        """
        from sympy import factorint
        
        G = nx.Graph()
        G.add_nodes_from(self.numbers)
        
        # Primfaktoren berechnen
        factors = {}
        for n in self.numbers:
            factors[n] = set(factorint(n).keys())
        
        # Kanten hinzufügen
        for i, n in enumerate(self.numbers):
            for m in self.numbers[i+1:]:
                common = factors[n] & factors[m]
                
                if len(common) > 0:
                    G.add_edge(n, m, weight=len(common))
        
        self.graph = G
        return G
```

#### Variante D: Hybrid-Graph (⭐ HAUPTFOKUS)

```python
class HybridGraphLaplacian(GraphLaplacian):
    """
    Hybrid EABC-Catalan-Graph.
    
    Kombiniert:
    - EABC-Vektor-Ähnlichkeit (lokal)
    - Tamari-Distanz (global)
    
    Gewichte: w = α · w_EABC + β · w_Tamari
    """
    
    def __init__(
        self, 
        numbers: List[int], 
        alpha: float = 1.0, 
        beta: float = 1.0,
        eabc_threshold: float = 3.0,
        tamari_max_distance: int = 5
    ):
        super().__init__(numbers)
        self.alpha = alpha
        self.beta = beta
        self.eabc_threshold = eabc_threshold
        self.tamari_max_distance = tamari_max_distance
        self.trees = {}  # n -> Catalan-Baum
    
    def construct_graph(self) -> nx.Graph:
        """
        Konstruiert Hybrid-Graph.
        """
        from utils.eabc import eabc_vector
        from utils.canonization import canonize_number
        from utils.tamari_graph import tamari_distance_bfs
        
        G = nx.Graph()
        G.add_nodes_from(self.numbers)
        
        # 1. Kanonische Bäume und EABC-Vektoren berechnen
        eabc_vecs = {}
        for n in self.numbers:
            self.trees[n] = canonize_number(n, method='balanced')
            eabc_vecs[n] = eabc_vector(n)
        
        # 2. Kanten hinzufügen (kombiniert EABC + Tamari)
        for i, n in enumerate(self.numbers):
            for m in self.numbers[i+1:]:
                # EABC-Komponente
                d_eabc = np.linalg.norm(
                    np.array(eabc_vecs[n]) - np.array(eabc_vecs[m])
                )
                
                if d_eabc < self.eabc_threshold:
                    w_eabc = np.exp(-d_eabc)
                else:
                    w_eabc = 0
                
                # Tamari-Komponente (nur falls gleiche Anzahl Blätter)
                T_n = self.trees[n]
                T_m = self.trees[m]
                
                if T_n.num_leaves == T_m.num_leaves:
                    d_tamari = tamari_distance_bfs(
                        T_n, T_m, 
                        max_distance=self.tamari_max_distance
                    )
                    
                    if d_tamari is not None and d_tamari <= self.tamari_max_distance:
                        w_tamari = np.exp(-d_tamari)
                    else:
                        w_tamari = 0
                else:
                    w_tamari = 0
                
                # Kombiniertes Gewicht
                w = self.alpha * w_eabc + self.beta * w_tamari
                
                if w > 0.01:  # Minimum-Threshold
                    G.add_edge(n, m, weight=w)
        
        self.graph = G
        return G
    
    def spectral_catalan_magic(
        self, 
        n: int, 
        epsilon: float = 0.1
    ) -> float:
        """
        M_catalan^(spectral)(n) = Σ_{λ_k < ε·λ_max} |⟨φ_k | δ_n⟩|²
        
        Projektion auf Near-Zero-Sektor.
        """
        if self.eigenvalues is None or self.eigenvectors is None:
            self.compute_spectrum()
        
        # Node-Index von n
        try:
            idx_n = self.numbers.index(n)
        except ValueError:
            raise ValueError(f"Zahl {n} nicht im Graph")
        
        # Delta-Funktion
        delta_n = np.zeros(len(self.numbers))
        delta_n[idx_n] = 1.0
        
        # Near-Zero-Schwelle
        threshold = epsilon * self.eigenvalues[-1]
        
        # Projektion
        M = 0.0
        for k, (lam, phi) in enumerate(zip(self.eigenvalues, self.eigenvectors.T)):
            if lam < threshold:
                projection = np.dot(phi, delta_n)
                M += projection**2
        
        return M
```

---

### 2. `tamari_graph.py`

```python
"""
Tamari-spezifische Funktionen.

- Rotation-Erkennung
- Tamari-Distanz-Berechnung (BFS)
- Tamari-Relation (partielle Ordnung)
"""

from catalan_trees import BinaryTree
import networkx as nx
from typing import Optional

def are_tamari_neighbors(T1: BinaryTree, T2: BinaryTree) -> bool:
    """
    Prüft, ob T1 und T2 durch eine Rotation verbunden sind.
    
    Rotation = Eine der beiden:
    1. Rechts-Rotation:  ((AB)C) → (A(BC))
    2. Links-Rotation:   (A(BC)) → ((AB)C)
    """
    # TODO: Implementiere präzise Rotations-Erkennung
    # Aktuell: Platzhalter (immer False)
    return can_rotate_right(T1, T2) or can_rotate_right(T2, T1)

def can_rotate_right(T1: BinaryTree, T2: BinaryTree) -> bool:
    """
    Prüft Rechts-Rotation:
    
    T1:  (·)              T2:  (·)
        /   \                 /   \
       (·)   C               A    (·)
      /   \                      /   \
     A     B                    B     C
    """
    if T1.is_leaf or T2.is_leaf:
        return False
    
    # T1 muss linkes Kind haben, das innerer Knoten ist
    if T1.left is None or T1.left.is_leaf:
        return False
    
    # T2 muss rechtes Kind haben, das innerer Knoten ist
    if T2.right is None or T2.right.is_leaf:
        return False
    
    # Prüfe Struktur:
    # T1.left = (A, B), T1.right = C
    # T2.left = A, T2.right = (B, C)
    
    A1 = T1.left.left
    B1 = T1.left.right
    C1 = T1.right
    
    A2 = T2.left
    B2 = T2.right.left
    C2 = T2.right.right
    
    # Strukturelle Gleichheit (ohne Label)
    return (
        trees_structurally_equal(A1, A2) and
        trees_structurally_equal(B1, B2) and
        trees_structurally_equal(C1, C2)
    )

def trees_structurally_equal(T1: BinaryTree, T2: BinaryTree) -> bool:
    """
    Prüft strukturelle Gleichheit (ignoriert Werte).
    """
    if T1 is None and T2 is None:
        return True
    if T1 is None or T2 is None:
        return False
    
    if T1.is_leaf and T2.is_leaf:
        return True  # Ignoriere Werte
    
    if T1.is_leaf != T2.is_leaf:
        return False
    
    return (
        trees_structurally_equal(T1.left, T2.left) and
        trees_structurally_equal(T1.right, T2.right)
    )

def tamari_distance_bfs(
    T1: BinaryTree, 
    T2: BinaryTree, 
    max_distance: int = 10
) -> Optional[int]:
    """
    Berechnet Tamari-Distanz via BFS über Rotationen.
    
    Args:
        T1, T2: Catalan-Bäume
        max_distance: Abbruch-Kriterium
        
    Returns:
        Distanz (int) oder None (falls > max_distance)
    """
    if trees_structurally_equal(T1, T2):
        return 0
    
    # BFS-Queue
    from collections import deque
    queue = deque([(T1, 0)])
    visited = {tree_to_string(T1)}
    
    while queue:
        current, dist = queue.popleft()
        
        if dist >= max_distance:
            continue
        
        # Generiere alle Nachbarn (Rotationen)
        neighbors = generate_rotations(current)
        
        for neighbor in neighbors:
            neighbor_str = tree_to_string(neighbor)
            
            if neighbor_str in visited:
                continue
            
            if trees_structurally_equal(neighbor, T2):
                return dist + 1
            
            visited.add(neighbor_str)
            queue.append((neighbor, dist + 1))
    
    return None  # Nicht gefunden

def generate_rotations(T: BinaryTree) -> list:
    """
    Generiert alle möglichen Rotationen von T.
    
    Returns:
        Liste von Bäumen (nach 1 Rotation erreichbar)
    """
    rotations = []
    
    # TODO: Implementiere vollständige Rotation-Generierung
    # Aktuell: Platzhalter (leere Liste)
    
    return rotations

def tree_to_string(T: BinaryTree) -> str:
    """
    Serialisiert Baum zu String (für Hashing).
    """
    if T.is_leaf:
        return "L"  # Leaf (ohne Wert)
    return f"({tree_to_string(T.left)},{tree_to_string(T.right)})"
```

---

### 3. `pde_solvers.py`

```python
"""
PDE-Löser für Graphen.

- Laplace-Gleichung: Lf = 0
- Wärmegleichung: f_t = -Lf
- Wellengleichung: f_tt = -Lf
"""

import numpy as np
from scipy.linalg import expm
from scipy.sparse import issparse
from typing import Tuple, List

def solve_laplace_equation(
    L: np.ndarray, 
    boundary_indices: List[int], 
    boundary_values: List[float]
) -> np.ndarray:
    """
    Löst Lf = 0 mit Randbedingungen.
    
    Args:
        L: Laplace-Matrix
        boundary_indices: Indizes mit festen Werten
        boundary_values: Werte an Randknoten
        
    Returns:
        f: Lösung (harmonische Funktion)
    """
    n = L.shape[0]
    
    # Freie Knoten
    free = [i for i in range(n) if i not in boundary_indices]
    
    # Untermatrix für freie Knoten
    L_free = L[np.ix_(free, free)]
    
    # Rechte Seite (Einfluss der Randwerte)
    b = np.zeros(len(free))
    for i, idx_free in enumerate(free):
        for j, idx_boundary in enumerate(boundary_indices):
            b[i] -= L[idx_free, idx_boundary] * boundary_values[j]
    
    # Löse L_free f_free = b
    if issparse(L_free):
        from scipy.sparse.linalg import spsolve
        f_free = spsolve(L_free, b)
    else:
        f_free = np.linalg.solve(L_free, b)
    
    # Setze Lösung zusammen
    f = np.zeros(n)
    for i, idx_free in enumerate(free):
        f[idx_free] = f_free[i]
    for i, idx_boundary in enumerate(boundary_indices):
        f[idx_boundary] = boundary_values[i]
    
    return f

def simulate_heat_flow(
    L: np.ndarray, 
    f0: np.ndarray, 
    t_max: float, 
    dt: float = 0.01
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Simuliert f_t = -Lf mit Anfangsbedingung f(0) = f0.
    
    Lösung: f(t) = exp(-tL) f0
    
    Args:
        L: Laplace-Matrix
        f0: Anfangsbedingung
        t_max: Maximale Zeit
        dt: Zeitschritt
        
    Returns:
        t_steps: Zeitpunkte
        solutions: f(t) für jedes t
    """
    t_steps = np.arange(0, t_max + dt, dt)
    solutions = []
    
    # Konvertiere zu dicht (falls sparse)
    if issparse(L):
        L_dense = L.toarray()
    else:
        L_dense = L
    
    for t in t_steps:
        # Matrix-Exponential
        f_t = expm(-t * L_dense) @ f0
        solutions.append(f_t)
    
    return t_steps, np.array(solutions)

def compute_entropy(f: np.ndarray) -> float:
    """
    Berechnet Shannon-Entropie von Verteilung f.
    
    S(f) = -Σ p_i log(p_i)
    """
    # Normiere zu Wahrscheinlichkeitsverteilung
    p = np.abs(f) / np.sum(np.abs(f))
    
    # Entfernen von Nullen
    p = p[p > 0]
    
    return -np.sum(p * np.log(p))

def simulate_wave_propagation(
    L: np.ndarray, 
    f0: np.ndarray, 
    g0: np.ndarray, 
    t_max: float, 
    dt: float = 0.01
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Simuliert f_tt = -Lf mit Anfangsbedingungen f(0) = f0, f'(0) = g0.
    
    Lösung: f(t) = cos(√L t)f0 + (√L)^{-1} sin(√L t)g0
    
    Args:
        L: Laplace-Matrix
        f0: Anfangsposition
        g0: Anfangsgeschwindigkeit
        t_max: Maximale Zeit
        dt: Zeitschritt
        
    Returns:
        t_steps: Zeitpunkte
        solutions: f(t) für jedes t
    """
    # Konvertiere zu dicht
    if issparse(L):
        L_dense = L.toarray()
    else:
        L_dense = L
    
    # Eigenwert-Zerlegung
    eigenvalues, eigenvectors = np.linalg.eigh(L_dense)
    
    # √L
    sqrt_L = eigenvectors @ np.diag(np.sqrt(np.abs(eigenvalues))) @ eigenvectors.T
    
    # Inverse von √L (mit Regularisierung)
    eigenvalues_inv = np.where(
        np.abs(eigenvalues) > 1e-10, 
        1.0 / np.sqrt(np.abs(eigenvalues)), 
        0
    )
    inv_sqrt_L = eigenvectors @ np.diag(eigenvalues_inv) @ eigenvectors.T
    
    t_steps = np.arange(0, t_max + dt, dt)
    solutions = []
    
    for t in t_steps:
        # cos(√L t) f0
        cos_term = (
            eigenvectors @ 
            np.diag(np.cos(np.sqrt(np.abs(eigenvalues)) * t)) @ 
            eigenvectors.T @ 
            f0
        )
        
        # (√L)^{-1} sin(√L t) g0
        sin_term = inv_sqrt_L @ (
            eigenvectors @ 
            np.diag(np.sin(np.sqrt(np.abs(eigenvalues)) * t)) @ 
            eigenvectors.T @ 
            g0
        )
        
        f_t = cos_term + sin_term
        solutions.append(f_t)
    
    return t_steps, np.array(solutions)
```

---

## 🧪 BEISPIEL-VERWENDUNG

### Hybrid-Graph für kleine Zahlen

```python
from utils.graph_laplacian import HybridGraphLaplacian
import matplotlib.pyplot as plt

# 1. Konstruiere Hybrid-Graph
numbers = list(range(10, 101, 10))  # [10, 20, ..., 100]
hybrid = HybridGraphLaplacian(
    numbers, 
    alpha=1.0,  # EABC-Gewicht
    beta=1.0    # Tamari-Gewicht
)

# 2. Berechne Spektrum
hybrid.compute_laplacian()
eigenvalues, eigenvectors = hybrid.compute_spectrum(k=20)

# 3. Fiedler-Wert
print(f"Fiedler-Wert: {hybrid.fiedler_value():.4f}")
print(f"Spektrale Lücke: {hybrid.spectral_gap():.4f}")

# 4. Spektrale Catalan-Magic für n=60
M_60 = hybrid.spectral_catalan_magic(60, epsilon=0.1)
print(f"M_catalan^(spectral)(60) = {M_60:.4f}")

# 5. Plot Spektrum
plt.figure(figsize=(10, 5))
plt.plot(eigenvalues, 'o-')
plt.axhline(0.1 * eigenvalues[-1], color='red', linestyle='--', 
            label='Near-Zero-Schwelle')
plt.xlabel('Index k')
plt.ylabel('Eigenwert λ_k')
plt.title('Spektrum des Hybrid-Graphen')
plt.legend()
plt.grid(True)
plt.show()
```

---

## 🔬 UNIT-TESTS

### `tests/test_graph_laplacian.py`

```python
import pytest
import numpy as np
from utils.graph_laplacian import (
    EABCGraphLaplacian, 
    TamariGraphLaplacian,
    FactorizationGraphLaplacian,
    HybridGraphLaplacian
)

def test_eabc_graph_construction():
    """Test: EABC-Graph wird korrekt konstruiert."""
    numbers = [6, 10, 12, 15]
    eabc = EABCGraphLaplacian(numbers, threshold=3.0)
    G = eabc.construct_graph()
    
    assert G.number_of_nodes() == len(numbers)
    assert G.number_of_edges() > 0  # Mindestens eine Kante

def test_laplacian_properties():
    """Test: Laplacian ist symmetrisch und positiv semi-definit."""
    numbers = list(range(10, 21))
    hybrid = HybridGraphLaplacian(numbers, alpha=1.0, beta=0.5)
    L = hybrid.compute_laplacian()
    
    L_dense = L.toarray()
    
    # Symmetrie
    assert np.allclose(L_dense, L_dense.T)
    
    # Positiv semi-definit (alle Eigenwerte ≥ 0)
    eigenvalues = np.linalg.eigvalsh(L_dense)
    assert np.all(eigenvalues >= -1e-10)  # Numerische Toleranz

def test_fiedler_value_positive():
    """Test: Fiedler-Wert > 0 für verbundene Graphen."""
    numbers = [12, 18, 24, 30]  # Alle teilen Faktor 2
    factorization = FactorizationGraphLaplacian(numbers)
    factorization.construct_graph()
    factorization.compute_spectrum(k=10)
    
    fiedler = factorization.fiedler_value()
    assert fiedler > 0  # Graph sollte verbunden sein

def test_spectral_catalan_magic_bounds():
    """Test: M_catalan^(spectral) ∈ [0, 1]."""
    numbers = list(range(20, 31))
    hybrid = HybridGraphLaplacian(numbers)
    hybrid.compute_laplacian()
    hybrid.compute_spectrum()
    
    for n in numbers:
        M = hybrid.spectral_catalan_magic(n, epsilon=0.1)
        assert 0 <= M <= 1, f"M({n}) = {M} außerhalb [0, 1]"

def test_rayleigh_quotient_constant():
    """Test: R(const) = 0 (Konstante ist harmonisch)."""
    numbers = list(range(10, 21))
    hybrid = HybridGraphLaplacian(numbers)
    L = hybrid.compute_laplacian()
    
    # Konstante Funktion
    f_const = np.ones(len(numbers))
    R = hybrid.rayleigh_quotient(f_const)
    
    assert np.abs(R) < 1e-10, f"R(const) = {R} ≠ 0"
```

---

## ⚙️ PERFORMANCE-OPTIMIERUNGEN

### 1. Sparse-Matrizen

```python
# IMMER sparse verwenden für große Graphen
L_sparse = nx.laplacian_matrix(G, weight='weight')  # Bereits sparse

# NUR für kleine Matrizen (n < 1000) zu dicht konvertieren
if n < 1000:
    L_dense = L_sparse.toarray()
```

### 2. Eigenwert-Berechnung

```python
# FÜR GROSSE MATRIZEN: Nur erste k Eigenwerte
eigenvalues, eigenvectors = spla.eigsh(L, k=50, which='SM')

# FÜR KLEINE MATRIZEN: Alle Eigenwerte (schneller)
if n < 200:
    eigenvalues, eigenvectors = np.linalg.eigh(L.toarray())
```

### 3. Caching

```python
# Cache EABC-Vektoren (wiederverwendbar)
eabc_cache = {}

def eabc_vector_cached(n):
    if n not in eabc_cache:
        eabc_cache[n] = eabc_vector(n)
    return eabc_cache[n]
```

### 4. Parallelisierung

```python
# Für große Ensembles: Parallele Verarbeitung
from joblib import Parallel, delayed

def compute_M_for_number(n, hybrid):
    return hybrid.spectral_catalan_magic(n)

M_values = Parallel(n_jobs=-1)(
    delayed(compute_M_for_number)(n, hybrid) 
    for n in numbers
)
```

---

## 📋 CHECKLISTE FÜR IMPLEMENTIERUNG

### Phase 1: Minimal Working Example ✅

- [ ] `graph_laplacian.py` mit `HybridGraphLaplacian`
- [ ] `tamari_graph.py` mit Platzhalter-Rotationen
- [ ] Test für n=10..100
- [ ] Spektrum berechnen
- [ ] Plot erstellen

### Phase 2: PDE-Simulator ✅

- [ ] `pde_solvers.py` mit `simulate_heat_flow`
- [ ] Entropie-Berechnung
- [ ] Test für Monotonie: S(t+dt) ≥ S(t)

### Phase 3: H10-Verbindung ✅

- [ ] M_catalan^(spectral) vs. E(n)
- [ ] Korrelationstest
- [ ] Scatter-Plot

### Phase 4: Vollständige Tests ✅

- [ ] Unit-Tests (pytest)
- [ ] Integration-Tests
- [ ] Performance-Benchmarks

---

**Ende CATALAN_LAPLACIAN_DESIGN.md**

*Für theoretische Hintergründe siehe: `H14_SPECTRAL_THEORY.md`*
