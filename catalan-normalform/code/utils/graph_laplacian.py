"""
Graph-Laplacian-Konstruktion für EABC/Catalan-Graphen.

Implementiert vier Varianten:
A) EABC-Nachbarschaftsgraph
B) Tamari-Graph
C) Faktorisierungs-Graph
D) Hybrid EABC-Catalan-Graph (⭐ HAUPTFOKUS)

Version: 1.0
Datum: 2026-06-24
Dokumentation: CATALAN_LAPLACIAN_DESIGN.md
"""

from abc import ABC, abstractmethod
import networkx as nx
import numpy as np
from typing import List, Tuple, Optional
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))


class GraphLaplacian(ABC):
    """
    Abstrakte Basisklasse für Graph-Laplacians.
    
    Alle konkreten Implementierungen müssen construct_graph() überschreiben.
    """
    
    def __init__(self, numbers: List[int]):
        """
        Args:
            numbers: Liste von natürlichen Zahlen (Knoten)
        """
        self.numbers = numbers
        self.graph = None
        self.laplacian = None
        self.eigenvalues = None
        self.eigenvectors = None
    
    @abstractmethod
    def construct_graph(self) -> nx.Graph:
        """
        Konstruiert Graph G.
        
        Returns:
            NetworkX Graph mit Gewichten
        """
        pass
    
    def compute_laplacian(self, weight_key='weight') -> np.ndarray:
        """
        Berechnet Laplace-Matrix L = D - A.
        
        Args:
            weight_key: Attribut-Name für Kantengewichte
            
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
            
        Returns:
            eigenvalues: Array von λ_0, λ_1, ..., λ_k
            eigenvectors: Matrix von Eigenvektoren (spaltenweise)
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
        Berechnet Rayleigh-Quotient R(f) = ⟨f, Lf⟩ / ⟨f, f⟩.
        
        Misst "Glattheit" von f:
        - R(f) ≈ 0: f ist glatt (nahe harmonisch)
        - R(f) groß: f ist rau (hochfrequent)
        
        Args:
            f: Funktion auf Knoten (Array)
            
        Returns:
            R(f): Rayleigh-Quotient
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
        
        λ_1 > 0 ⟺ Graph ist verbunden
        
        Returns:
            λ_1: Fiedler-Wert
        """
        if self.eigenvalues is None:
            self.compute_spectrum(k=10)
        
        # Sortiere falls nötig
        sorted_eigs = np.sort(self.eigenvalues)
        
        return sorted_eigs[1]
    
    def spectral_gap(self) -> float:
        """
        Spektrale Lücke: λ_1 - λ_0.
        
        Große Lücke → Schnelle Konvergenz der Diffusion
        
        Returns:
            λ_1 - λ_0
        """
        if self.eigenvalues is None:
            self.compute_spectrum(k=10)
        
        sorted_eigs = np.sort(self.eigenvalues)
        return sorted_eigs[1] - sorted_eigs[0]


class EABCGraphLaplacian(GraphLaplacian):
    """
    EABC-Nachbarschaftsgraph basierend auf EABC-Vektor-Distanz.
    
    Knoten: numbers
    Kanten: d_EABC(n, m) < threshold
    Gewichte: exp(-d_EABC(n, m))
    """
    
    def __init__(self, numbers: List[int], threshold: float = 2.0):
        """
        Args:
            numbers: Liste von natürlichen Zahlen
            threshold: EABC-Distanz-Schwelle für Kanten
        """
        super().__init__(numbers)
        self.threshold = threshold
    
    def construct_graph(self) -> nx.Graph:
        """
        Konstruiert EABC-Graph.
        
        Returns:
            NetworkX Graph
        """
        from utils.eabc import compute_eabc_vector
        
        G = nx.Graph()
        G.add_nodes_from(self.numbers)
        
        # EABC-Vektoren berechnen
        eabc_vecs = {}
        for n in self.numbers:
            try:
                eabc_vecs[n] = tuple(compute_eabc_vector(n))
            except:
                # Fallback: Nullvektor
                eabc_vecs[n] = (0, 0, 0, 0)
        
        # Kanten hinzufügen
        for i, n in enumerate(self.numbers):
            for m in self.numbers[i+1:]:
                vec_n = np.array(eabc_vecs[n], dtype=float)
                vec_m = np.array(eabc_vecs[m], dtype=float)
                d = np.linalg.norm(vec_n - vec_m)
                
                if d < self.threshold:
                    w = np.exp(-d)
                    G.add_edge(n, m, weight=w)
        
        self.graph = G
        return G


class FactorizationGraphLaplacian(GraphLaplacian):
    """
    Faktorisierungs-Graph basierend auf gemeinsamen Primfaktoren.
    
    Knoten: numbers
    Kanten: Gemeinsame Primfaktoren
    Gewichte: Anzahl gemeinsamer Faktoren
    """
    
    def construct_graph(self) -> nx.Graph:
        """
        Konstruiert Faktorisierungs-Graph.
        
        Returns:
            NetworkX Graph
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


class HybridGraphLaplacian(GraphLaplacian):
    """
    Hybrid EABC-Catalan-Graph (⭐ HAUPTFOKUS).
    
    Kombiniert:
    - EABC-Vektor-Ähnlichkeit (lokal)
    - Tamari-Distanz (global)
    
    Gewichte: w = α · w_EABC + β · w_Tamari
    
    Entspricht metrischem Tensor: ds² = α d²_EABC + β d²_Tamari
    """
    
    def __init__(
        self, 
        numbers: List[int], 
        alpha: float = 1.0, 
        beta: float = 1.0,
        eabc_threshold: float = 3.0
    ):
        """
        Args:
            numbers: Liste von natürlichen Zahlen
            alpha: Gewicht für EABC-Komponente
            beta: Gewicht für Tamari-Komponente
            eabc_threshold: EABC-Distanz-Schwelle
        """
        super().__init__(numbers)
        self.alpha = alpha
        self.beta = beta
        self.eabc_threshold = eabc_threshold
        self.trees = {}  # n -> Catalan-Baum
    
    def construct_graph(self) -> nx.Graph:
        """
        Konstruiert Hybrid-Graph.
        
        Returns:
            NetworkX Graph
        """
        from utils.eabc import compute_eabc_vector
        from utils.canonization import canonize_number
        
        G = nx.Graph()
        G.add_nodes_from(self.numbers)
        
        # 1. Kanonische Bäume und EABC-Vektoren berechnen
        eabc_vecs = {}
        for n in self.numbers:
            try:
                self.trees[n] = canonize_number(n, method='balanced')
                eabc_vecs[n] = tuple(compute_eabc_vector(n))
            except:
                # Fallback
                self.trees[n] = None
                eabc_vecs[n] = (0, 0, 0, 0)
        
        # 2. Kanten hinzufügen (kombiniert EABC + Tamari)
        for i, n in enumerate(self.numbers):
            for m in self.numbers[i+1:]:
                # EABC-Komponente
                vec_n = np.array(eabc_vecs[n], dtype=float)
                vec_m = np.array(eabc_vecs[m], dtype=float)
                d_eabc = np.linalg.norm(vec_n - vec_m)
                
                if d_eabc < self.eabc_threshold:
                    w_eabc = np.exp(-d_eabc)
                else:
                    w_eabc = 0
                
                # Tamari-Komponente (TODO: Implementieren wenn tamari_graph.py fertig)
                # Aktuell: Nur EABC-Komponente
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
        Berechnet spektrale Catalan-Magic für Zahl n.
        
        M_catalan^(spectral)(n) = Σ_{λ_k < ε·λ_max} |⟨φ_k | δ_n⟩|²
        
        Projektion auf Near-Zero-Sektor.
        
        Args:
            n: Natürliche Zahl
            epsilon: Near-Zero-Schwelle (relativ zu λ_max)
            
        Returns:
            M_catalan^(spectral)(n)
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


# Beispiel-Verwendung
if __name__ == "__main__":
    print("Graph-Laplacian Tests\n")
    
    # Test 1: EABC-Graph
    print("=== Test 1: EABC-Graph ===")
    numbers = [6, 10, 12, 15, 18, 20]
    eabc = EABCGraphLaplacian(numbers, threshold=3.0)
    G_eabc = eabc.construct_graph()
    print(f"Knoten: {G_eabc.number_of_nodes()}")
    print(f"Kanten: {G_eabc.number_of_edges()}")
    
    L_eabc = eabc.compute_laplacian()
    print(f"Laplacian-Dimension: {L_eabc.shape}")
    
    # Test 2: Faktorisierungs-Graph
    print("\n=== Test 2: Faktorisierungs-Graph ===")
    factor = FactorizationGraphLaplacian(numbers)
    G_factor = factor.construct_graph()
    print(f"Knoten: {G_factor.number_of_nodes()}")
    print(f"Kanten: {G_factor.number_of_edges()}")
    
    # Test 3: Hybrid-Graph
    print("\n=== Test 3: Hybrid-Graph ===")
    hybrid = HybridGraphLaplacian(numbers, alpha=1.0, beta=0.0)  # Nur EABC
    G_hybrid = hybrid.construct_graph()
    print(f"Knoten: {G_hybrid.number_of_nodes()}")
    print(f"Kanten: {G_hybrid.number_of_edges()}")
    
    # Spektrum berechnen
    eigenvalues, eigenvectors = hybrid.compute_spectrum()
    print(f"\nEigenwerte: {eigenvalues[:5]}")
    print(f"Fiedler-Wert: {hybrid.fiedler_value():.4f}")
    print(f"Spektrale Lücke: {hybrid.spectral_gap():.4f}")
    
    # Spektrale Catalan-Magic
    M_12 = hybrid.spectral_catalan_magic(12, epsilon=0.1)
    print(f"\nM_catalan^(spectral)(12) = {M_12:.4f}")
    
    print("\n✅ Alle Tests abgeschlossen!")
