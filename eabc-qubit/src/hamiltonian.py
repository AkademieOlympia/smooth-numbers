"""
EABC-Hamiltonian: Konstruktion des Quantensystems

Dieses Modul implementiert die Konstruktion des Hamiltonoperators H = α H_T + β H_χ + γ H_p
für das eindimensionale Quantensystem mit internem EABC-Freiheitsgrad.
"""

import numpy as np
import scipy.sparse as sp
from scipy.sparse.linalg import eigsh
from typing import Optional, Tuple
from .primes import generate_primes, eabc_index
from .collatz_weights import collatz_log_rate_prime, random_soup_weights
from .syracuse_dynamics import (
    syracuse_trajectory, 
    trajectory_statistics,
    compute_lambda_j,
    random_coprime_6_odd
)
from .smooth_integration import smooth_density_fast, smooth_potential_landscape


class EABCHamiltonian:
    """
    EABC-Hamiltonoperator H = α H_T + β H_χ + γ H_p
    
    Konstruiert einen sparse Hamiltonoperator für ein eindimensionales
    Tight-Binding-System mit internem Z₄-Freiheitsgrad (EABC) und
    topologischen Defekten an Primzahlpositionen.
    
    Parameters
    ----------
    N : int
        Anzahl der Gitterplätze
    alpha : float, optional
        Hopping-Stärke (kinetischer Term), default: 1.0
    beta : float, optional
        Chirale Kopplung, default: 0.5
    gamma : float, optional
        Primzahl-Defekt-Stärke, default: 1.5
    periodic : bool, optional
        Periodische Randbedingungen, default: False
    
    Attributes
    ----------
    N : int
        Gittergröße
    dim : int
        Hilbertraum-Dimension (= 4N)
    alpha, beta, gamma : float
        Kopplungskonstanten
    H : scipy.sparse.csr_matrix
        Gesamthamiltonian (sparse)
    H_T, H_chi, H_p : scipy.sparse.csr_matrix
        Einzelterme
    """
    
    def __init__(
        self,
        N: int,
        alpha: float = 1.0,
        beta: float = 0.5,
        gamma: float = 1.5,
        periodic: bool = False
    ):
        self.N = N
        self.dim = 4 * N
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.periodic = periodic
        
        # Hamiltonoperator konstruieren
        self._build_hamiltonian()
    
    def _build_tight_binding(self) -> sp.csr_matrix:
        """
        Konstruiere den kinetischen Term H_T = T ⊗ 𝟙₄.
        
        T ist eine Nebendiagonal-Matrix (Hopping zwischen benachbarten Plätzen):
        
        T = ⎡ 0  1  0  0  ... ⎤
            ⎢ 1  0  1  0  ... ⎥
            ⎢ 0  1  0  1  ... ⎥
            ⎢ ...            ⎥
            ⎣ ...          0 ⎦
        
        Mit periodischen Randbedingungen: T[0, N-1] = T[N-1, 0] = 1
        
        Returns
        -------
        scipy.sparse.csr_matrix
            H_T mit Dimension 4N × 4N
        """
        # Tight-Binding-Matrix (Nebendiagonalen)
        diagonals = [np.ones(self.N - 1), np.ones(self.N - 1)]
        offsets = [-1, 1]
        
        T = sp.diags(diagonals, offsets, shape=(self.N, self.N), format='csr')
        
        # Periodische Randbedingungen (optional)
        if self.periodic:
            T[0, self.N - 1] = 1.0
            T[self.N - 1, 0] = 1.0
        
        # Kronecker-Produkt: T ⊗ 𝟙₄
        I_4 = sp.eye(4, format='csr')
        H_T = sp.kron(T, I_4, format='csr')
        
        return H_T
    
    def _build_chiral_term(self) -> sp.csr_matrix:
        """
        Konstruiere den chiralen Term H_χ = 𝟙_N ⊗ (χ + χ†).
        
        χ ist die zyklische Permutation E → C → B → A → E:
        
        χ = ⎡ 0  0  0  1 ⎤       χ† = ⎡ 0  1  0  0 ⎤
            ⎢ 1  0  0  0 ⎥            ⎢ 0  0  1  0 ⎥
            ⎢ 0  1  0  0 ⎥            ⎢ 0  0  0  1 ⎥
            ⎣ 0  0  1  0 ⎦            ⎣ 1  0  0  0 ⎦
        
        χ + χ† = ⎡ 0  1  0  1 ⎤
                 ⎢ 1  0  1  0 ⎥
                 ⎢ 0  1  0  1 ⎥
                 ⎣ 1  0  1  0 ⎦
        
        Returns
        -------
        scipy.sparse.csr_matrix
            H_χ mit Dimension 4N × 4N
        """
        # Zyklische Permutation χ (E=0, A=1, B=2, C=3)
        # χ: |0⟩→|3⟩, |1⟩→|0⟩, |2⟩→|1⟩, |3⟩→|2⟩
        chi = sp.csr_matrix([
            [0, 0, 0, 1],
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0]
        ], dtype=float)
        
        # χ + χ† (hermitisch)
        chi_herm = chi + chi.T
        
        # Kronecker-Produkt: 𝟙_N ⊗ (χ + χ†)
        I_N = sp.eye(self.N, format='csr')
        H_chi = sp.kron(I_N, chi_herm, format='csr')
        
        return H_chi
    
    def _build_prime_defects(self) -> sp.csr_matrix:
        """
        Konstruiere den Primzahl-Defekt-Term H_p.
        
        H_p = Σ_p |p⟩⟨p| ⊗ |σ(p)⟩⟨σ(p)|
        
        Diagonalterm an Position (4(p-1) + σ(p), 4(p-1) + σ(p)) für jede Primzahl p ≤ N,
        wobei σ(p) ∈ {0,1,2,3} der EABC-Index ist.
        
        Returns
        -------
        scipy.sparse.csr_matrix
            H_p mit Dimension 4N × 4N
        """
        primes = generate_primes(self.N)
        
        # Sparse Matrix im COO-Format (coordinate format)
        rows = []
        cols = []
        data = []
        
        for p in primes:
            sigma = eabc_index(p)  # EABC-Klassifikation
            idx = 4 * (p - 1) + sigma  # Globaler Index im 4N-dimensionalen Raum
            
            rows.append(idx)
            cols.append(idx)
            data.append(1.0)
        
        # In CSR-Format konvertieren
        H_p = sp.csr_matrix(
            (data, (rows, cols)),
            shape=(self.dim, self.dim)
        )
        
        return H_p
    
    def _build_hamiltonian(self):
        """
        Konstruiere den Gesamthamiltonian H = α H_T + β H_χ + γ H_p.
        
        Alle Terme werden als sparse CSR-Matrizen gespeichert.
        """
        print(f"Konstruiere EABC-Hamiltonian für N = {self.N} (Dimension {self.dim})...")
        
        # Einzelterme
        print("  [1/3] Kinetischer Term H_T...")
        self.H_T = self._build_tight_binding()
        
        print("  [2/3] Chiraler Term H_χ...")
        self.H_chi = self._build_chiral_term()
        
        print("  [3/3] Primzahl-Defekte H_p...")
        self.H_p = self._build_prime_defects()
        
        # Gesamthamiltonian
        print("  Summiere Terme...")
        self.H = self.alpha * self.H_T + self.beta * self.H_chi + self.gamma * self.H_p
        
        # Speicherstatistik
        nnz = self.H.nnz
        sparsity = 100 * nnz / (self.dim ** 2)
        print(f"✓ Hamiltonian konstruiert: {nnz} Nicht-Null-Einträge ({sparsity:.4f}% der Matrix)")
    
    def compute_spectrum(
        self,
        k: int = 500,
        which: str = 'SM',
        return_eigenvectors: bool = False,
        sigma: Optional[float] = None
    ) -> np.ndarray:
        """
        Berechne k Eigenwerte (und optional Eigenvektoren) des Hamiltonians.
        
        Verwendet den Lanczos-Algorithmus (scipy.sparse.linalg.eigsh) für
        effiziente partielle Diagonalisierung großer sparse Matrizen.
        
        Parameters
        ----------
        k : int, optional
            Anzahl der zu berechnenden Eigenwerte, default: 500
        which : str, optional
            Welche Eigenwerte: 'SM' (smallest magnitude), 'LM' (largest magnitude),
            'SA' (smallest algebraic), 'LA' (largest algebraic), default: 'SM'
        return_eigenvectors : bool, optional
            Falls True, gib auch Eigenvektoren zurück, default: False
        sigma : float, optional
            Shift für Spektrum-Targeting (z.B. sigma=0.0 für mittlere Eigenwerte)
        
        Returns
        -------
        eigenvalues : np.ndarray
            Sortierte Eigenwerte (1D-Array der Länge k)
        eigenvectors : np.ndarray, optional
            Eigenvektoren (Matrix der Größe dim × k), nur falls return_eigenvectors=True
        
        Examples
        --------
        >>> H = EABCHamiltonian(N=1000)
        >>> E = H.compute_spectrum(k=200)  # Mittlere 200 Eigenwerte
        >>> len(E)
        200
        """
        print(f"Berechne {k} Eigenwerte (Methode: {which})...")
        
        result = eigsh(
            self.H,
            k=k,
            which=which,
            sigma=sigma,
            return_eigenvectors=return_eigenvectors
        )
        
        if return_eigenvectors:
            eigenvalues, eigenvectors = result
            idx = np.argsort(eigenvalues)
            eigenvalues = eigenvalues[idx]
            eigenvectors = eigenvectors[:, idx]
            print(f"✓ Spektrum berechnet: E ∈ [{eigenvalues[0]:.4f}, {eigenvalues[-1]:.4f}]")
            return eigenvalues, eigenvectors
        else:
            eigenvalues = np.sort(result)
            print(f"✓ Spektrum berechnet: E ∈ [{eigenvalues[0]:.4f}, {eigenvalues[-1]:.4f}]")
            return eigenvalues
    
    def info(self):
        """Zeige System-Informationen."""
        print("\n" + "="*60)
        print("EABC-Hamiltonian System")
        print("="*60)
        print(f"Gittergröße N:         {self.N}")
        print(f"Hilbertraum-Dimension: {self.dim} (= 4N)")
        print(f"Periodische Randbedingungen: {self.periodic}")
        print("\nKopplungskonstanten:")
        print(f"  α (Hopping):         {self.alpha:.3f}")
        print(f"  β (Chiralität):      {self.beta:.3f}")
        print(f"  γ (Primzahl-Defekt): {self.gamma:.3f}")
        print("\nPrimzahl-Statistik:")
        primes = generate_primes(self.N)
        print(f"  Anzahl Primzahlen ≤ N: {len(primes)}")
        print(f"  Defekt-Dichte:         {len(primes)/self.N:.4f}")
        print("="*60 + "\n")


class CollatzEABCHamiltonian(EABCHamiltonian):
    """
    Erweiterte EABC-Hamiltonian-Klasse mit Collatz-Dynamik-Gewichten.
    
    Statt uniformer Primzahl-Defekte (γ * 1.0) werden die Defekte nach den
    lokalen Collatz-Kontraktionsraten log(r) gewichtet:
    
    H_p^Collatz = Σ_p log(r(p)) · |p⟩⟨p| ⊗ |σ(p)⟩⟨σ(p)|
    
    wobei log(r(p)) die theoretische Expansions-/Kontraktionsrate für die
    EABC-Klasse von p ist (aus Paper C).
    
    Parameters
    ----------
    N : int
        Anzahl der Gitterplätze
    alpha : float, optional
        Hopping-Stärke (kinetischer Term), default: 1.0
    beta : float, optional
        Chirale Kopplung, default: 0.5
    gamma : float, optional
        Globaler Skalierungsfaktor für Collatz-Gewichte, default: 1.5
    periodic : bool, optional
        Periodische Randbedingungen, default: False
    use_random_soup : bool, optional
        Falls True, verwende zufällig permutierte Gewichte (Kontrolle), default: False
    random_seed : int, optional
        Random seed für random_soup, default: 42
    
    Attributes
    ----------
    collatz_weights : np.ndarray
        Array der Collatz log(r)-Gewichte für alle Primzahlen
    use_random_soup : bool
        Flag für Kontroll-Experiment
    
    Notes
    -----
    Der Parameter γ skaliert jetzt die physikalisch motivierten Collatz-Gewichte
    statt uniform alle Defekte zu setzen. Dies ermöglicht Studien der Stärke
    der Collatz-Kopplung bei gleichzeitiger Beibehaltung der relativen Struktur.
    
    Examples
    --------
    >>> H = CollatzEABCHamiltonian(N=1000, gamma=2.0)
    >>> H.info()
    >>> eigenvalues = H.compute_spectrum(k=500)
    
    References
    ----------
    Paper C: "Conditional Collatz via G2 Log-Drift Axiom"
    """
    
    def __init__(
        self,
        N: int,
        alpha: float = 1.0,
        beta: float = 0.5,
        gamma: float = 1.5,
        periodic: bool = False,
        use_random_soup: bool = False,
        random_seed: int = 42
    ):
        self.use_random_soup = use_random_soup
        self.random_seed = random_seed
        
        # Basisklassen-Initialisierung (ohne _build_hamiltonian)
        self.N = N
        self.dim = 4 * N
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.periodic = periodic
        
        # Collatz-Gewichte vorbereiten
        self._prepare_collatz_weights()
        
        # Jetzt Hamiltonian bauen
        self._build_hamiltonian()
    
    def _prepare_collatz_weights(self):
        """Berechne Collatz-Gewichte für alle Primzahlen."""
        primes = generate_primes(self.N)
        
        if self.use_random_soup:
            # Kontroll-Experiment: Zufällig permutierte Gewichte
            self.collatz_weights = random_soup_weights(len(primes), seed=self.random_seed)
        else:
            # Echte Collatz-Gewichte aus Paper C
            self.collatz_weights = np.array([collatz_log_rate_prime(p) for p in primes])
    
    def _build_prime_defects(self) -> sp.csr_matrix:
        """
        Überschreibe die Primzahl-Defekt-Konstruktion mit Collatz-Gewichten.
        
        H_p^Collatz = γ · Σ_p log(r(p)) · |p⟩⟨p| ⊗ |σ(p)⟩⟨σ(p)|
        
        Returns
        -------
        scipy.sparse.csr_matrix
            H_p mit Collatz-gewichteten Defekten
        """
        primes = generate_primes(self.N)
        
        # Sparse Matrix im COO-Format
        rows = []
        cols = []
        data = []
        
        for i, p in enumerate(primes):
            sigma = eabc_index(p)
            idx = 4 * (p - 1) + sigma
            
            # Verwende Collatz-Gewicht statt uniformem 1.0
            weight = self.collatz_weights[i]
            
            rows.append(idx)
            cols.append(idx)
            data.append(weight)  # Collatz log(r) statt 1.0
        
        # In CSR-Format konvertieren
        H_p = sp.csr_matrix(
            (data, (rows, cols)),
            shape=(self.dim, self.dim)
        )
        
        return H_p
    
    def info(self):
        """Zeige System-Informationen mit Collatz-Details."""
        print("\n" + "="*60)
        print("Collatz-EABC-Hamiltonian System")
        print("="*60)
        print(f"Gittergröße N:         {self.N}")
        print(f"Hilbertraum-Dimension: {self.dim} (= 4N)")
        print(f"Periodische Randbedingungen: {self.periodic}")
        print("\nKopplungskonstanten:")
        print(f"  α (Hopping):         {self.alpha:.3f}")
        print(f"  β (Chiralität):      {self.beta:.3f}")
        print(f"  γ (Collatz-Skala):   {self.gamma:.3f}")
        print("\nCollatz-Gewichte:")
        print(f"  Modus: {'Random Soup (Kontrolle)' if self.use_random_soup else 'Echte Collatz-Raten'}")
        print(f"  Mittelwert log(r):   {np.mean(self.collatz_weights):+.6f}")
        print(f"  Std.-Abweichung:     {np.std(self.collatz_weights):.6f}")
        print(f"  Min log(r):          {np.min(self.collatz_weights):+.6f}")
        print(f"  Max log(r):          {np.max(self.collatz_weights):+.6f}")
        print("\nPrimzahl-Statistik:")
        primes = generate_primes(self.N)
        print(f"  Anzahl Primzahlen ≤ N: {len(primes)}")
        print(f"  Defekt-Dichte:         {len(primes)/self.N:.4f}")
        print("="*60 + "\n")
    
    def compare_with_uniform(self, k: int = 500) -> dict:
        """
        Vergleiche Collatz-gewichtete mit uniform-gewichteter Spektralstatistik.
        
        Parameters
        ----------
        k : int, optional
            Anzahl der zu berechnenden Eigenwerte, default: 500
        
        Returns
        -------
        dict
            Dictionary mit beiden Spektren und Statistiken
        """
        print("Berechne Collatz-gewichtetes Spektrum...")
        E_collatz = self.compute_spectrum(k=k, which='SM')
        
        # Temporär uniform-gewichteten Hamiltonian bauen
        print("Berechne uniform-gewichtetes Spektrum (Referenz)...")
        H_uniform = EABCHamiltonian(
            N=self.N,
            alpha=self.alpha,
            beta=self.beta,
            gamma=self.gamma,
            periodic=self.periodic
        )
        E_uniform = H_uniform.compute_spectrum(k=k, which='SM')
        
        return {
            'collatz': E_collatz,
            'uniform': E_uniform,
            'collatz_weights': self.collatz_weights,
            'delta_spectrum': E_collatz - E_uniform
        }


class TaoSyracuseHamiltonian(EABCHamiltonian):
    """
    Zeitabhängiger Hamiltonian mit echter Syracuse-Dynamik (Tao 2019).
    
    Statt statischer Collatz-Gewichte log(r) pro EABC-Klasse verwendet dieser
    Hamiltonian die echte Syracuse-Trajektorie S₀, S₁, S₂, ... eines Startwerts N₀:
    
    H^{Tao-EABC}(t) = H_T + H_χ + γ Σ_{j=0}^t λ_j(N₀) |S_j⟩⟨S_j| ⊗ |σ(S_j)⟩⟨σ(S_j)|
    
    wobei:
    - S_j(N₀) = Syr^j(N₀) ist die j-te Iteration der Syracuse-Funktion
    - a_j = ν₂(3·S_j + 1) ist die 2-adische Valuation
    - λ_j = log(3) - a_j·log(2) ist Tao's lokale Drift
    
    Tao's Hauptresultat (2019):
        Für typische N₀ sind die a_j wie unabhängige Geom(2)-Zufallsvariablen verteilt
        mit E[a_j] = 2, sodass E[λ_j] = log(3/4) < 0 (negative Drift!).
    
    Diese Klasse ermöglicht den direkten Vergleich:
    1. Statisch (CollatzEABCHamiltonian): Feste log(r)-Gewichte pro EABC-Klasse
    2. Dynamisch (TaoSyracuseHamiltonian): Echte Trajektorie von N₀
    3. Geom(2)-Ensemble: Mittelung über viele Startwerte
    
    Parameters
    ----------
    N : int
        Gittergröße (Anzahl der Gitterplätze)
    start_n : int
        Startwert N₀ für Syracuse-Iteration (ungerade, coprime zu 6)
    trajectory_length : int
        Anzahl der Syracuse-Schritte (Trajektorienlänge)
    alpha : float, optional
        Hopping-Stärke (kinetischer Term), default: 1.0
    beta : float, optional
        Chirale Kopplung, default: 0.5
    gamma : float, optional
        Skalierungsfaktor für Syracuse-Defekte, default: 1.5
    periodic : bool, optional
        Periodische Randbedingungen, default: False
    use_geom2_synthetic : bool, optional
        Falls True, verwende synthetische Geom(2)-Valuationen statt echter Trajektorie, default: False
    
    Attributes
    ----------
    start_n : int
        Startwert der Syracuse-Trajektorie
    trajectory : List[int]
        Syracuse-Trajektorie [N₀, S₁, S₂, ...]
    valuations : List[int]
        2-adische Valuationen [a₁, a₂, ...]
    lambdas : List[float]
        Lokale Drifts [λ₁, λ₂, ...]
    trajectory_stats : dict
        Statistische Kenngrößen der Trajektorie
    H_syracuse : scipy.sparse.csr_matrix
        Syracuse-Defekt-Term
    use_geom2_synthetic : bool
        Flag für synthetische Geom(2)-Valuationen
    
    Examples
    --------
    >>> # Dynamischer Hamiltonian mit echter Trajektorie
    >>> H_dyn = TaoSyracuseHamiltonian(N=1000, start_n=27, trajectory_length=50)
    >>> H_dyn.info()
    >>> E_dyn = H_dyn.compute_spectrum(k=500)
    
    >>> # Geom(2)-synthetische Kontrolle
    >>> H_geom = TaoSyracuseHamiltonian(N=1000, start_n=27, trajectory_length=50, use_geom2_synthetic=True)
    
    References
    ----------
    T. Tao, "Almost all Collatz orbits attain almost bounded values" (2019)
    https://arxiv.org/abs/1909.03562
    """
    
    def __init__(
        self,
        N: int,
        start_n: int,
        trajectory_length: int,
        alpha: float = 1.0,
        beta: float = 0.5,
        gamma: float = 1.5,
        periodic: bool = False,
        use_geom2_synthetic: bool = False
    ):
        self.start_n = start_n
        self.trajectory_length = trajectory_length
        self.use_geom2_synthetic = use_geom2_synthetic
        
        # Basisklassen-Attribute (ohne _build_hamiltonian)
        self.N = N
        self.dim = 4 * N
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.periodic = periodic
        
        # Berechne Syracuse-Trajektorie oder synthetische Geom(2)-Daten
        self._prepare_syracuse_trajectory()
        
        # Hamiltonian bauen
        self._build_hamiltonian()
    
    def _prepare_syracuse_trajectory(self):
        """Berechne Syracuse-Trajektorie und Statistiken."""
        if self.use_geom2_synthetic:
            # Synthetische Geom(2)-Valuationen (Kontrolle)
            print(f"Generiere synthetische Geom(2)-Valuationen (n={self.trajectory_length})...")
            from .syracuse_dynamics import geom2_sample_valuations
            self.valuations = list(geom2_sample_valuations(self.trajectory_length, seed=42))
            
            # Konstruiere fiktive Trajektorie (für Konsistenz)
            # Wir samplen zufällige ungerade Zahlen ≤ N
            import random
            random.seed(42)
            self.trajectory = [random_coprime_6_odd(self.N, seed=i) for i in range(self.trajectory_length + 1)]
        else:
            # Echte Syracuse-Trajektorie
            print(f"Berechne Syracuse-Trajektorie für N₀ = {self.start_n}...")
            self.trajectory, self.valuations = syracuse_trajectory(
                self.start_n, 
                max_steps=self.trajectory_length
            )
        
        # Statistiken berechnen
        self.trajectory_stats = trajectory_statistics(self.trajectory, self.valuations)
        
        # Lokale Drifts λ_j
        self.lambdas = [np.log(3) - a * np.log(2) for a in self.valuations]
        
        print(f"✓ Trajektorienlänge: {len(self.trajectory)}")
        print(f"✓ ⟨a_j⟩ = {self.trajectory_stats['mean_valuation']:.3f} (Theorie: 2.0)")
        print(f"✓ ⟨λ_j⟩ = {self.trajectory_stats['mean_lambda']:.4f} (Theorie: log(3/4) ≈ -0.288)")
    
    def _build_prime_defects(self) -> sp.csr_matrix:
        """
        Überschreibe die Primzahl-Defekt-Konstruktion mit Syracuse-Dynamik.
        
        H_syracuse = γ · Σ_j λ_j |S_j⟩⟨S_j| ⊗ |σ(S_j)⟩⟨σ(S_j)|
        
        Jeder Term in der Summe entspricht einem Defekt an der Position S_j(N₀)
        mit Gewicht λ_j = log(3) - a_j·log(2).
        
        Returns
        -------
        scipy.sparse.csr_matrix
            H_syracuse mit zeitabhängigen Syracuse-Defekten
        """
        # Sparse Matrix im COO-Format
        rows = []
        cols = []
        data = []
        
        for j, (s_j, lambda_j) in enumerate(zip(self.trajectory[:-1], self.lambdas)):
            # S_j muss im Gitter [1, N] liegen
            if s_j > self.N:
                continue
            
            # EABC-Klassifikation (funktioniert auch für zusammengesetzte Zahlen)
            # Wir verwenden die mod-12-Klassifikation direkt
            if s_j == 2:
                sigma = 0  # E
            elif s_j == 3:
                sigma = 1  # A
            else:
                r = s_j % 12
                sigma_map = {1: 0, 5: 1, 7: 2, 11: 3}  # E, A, B, C
                sigma = sigma_map.get(r, 0)  # Fallback zu E
            
            idx = 4 * (s_j - 1) + sigma
            
            # Prüfe ob Index im gültigen Bereich
            if idx >= self.dim:
                continue
            
            rows.append(idx)
            cols.append(idx)
            data.append(lambda_j)  # Verwende λ_j statt uniformem 1.0
        
        # In CSR-Format konvertieren
        H_syracuse = sp.csr_matrix(
            (data, (rows, cols)),
            shape=(self.dim, self.dim)
        )
        
        return H_syracuse
    
    def info(self):
        """Zeige System-Informationen mit Syracuse-Details."""
        print("\n" + "="*70)
        print("Tao-Syracuse-EABC-Hamiltonian System")
        print("="*70)
        print(f"Gittergröße N:         {self.N}")
        print(f"Hilbertraum-Dimension: {self.dim} (= 4N)")
        print(f"Periodische Randbedingungen: {self.periodic}")
        print("\nKopplungskonstanten:")
        print(f"  α (Hopping):         {self.alpha:.3f}")
        print(f"  β (Chiralität):      {self.beta:.3f}")
        print(f"  γ (Syracuse-Skala):  {self.gamma:.3f}")
        print("\nSyracuse-Trajektorie:")
        if self.use_geom2_synthetic:
            print(f"  Modus: Synthetische Geom(2)-Valuationen (Kontrolle)")
        else:
            print(f"  Startwert N₀:        {self.start_n}")
        print(f"  Trajektorienlänge:   {len(self.trajectory)}")
        print(f"  Max. Wert:           {self.trajectory_stats['max_value']}")
        print("\nTao's Drift-Statistiken:")
        print(f"  ⟨a_j⟩:               {self.trajectory_stats['mean_valuation']:.4f} (Theorie: 2.0)")
        print(f"  ⟨λ_j⟩:               {self.trajectory_stats['mean_lambda']:.4f} (Theorie: -0.288)")
        print(f"  Σλ_j (Gesamtdrift):  {self.trajectory_stats['total_drift']:.4f}")
        print(f"  Min λ_j:             {min(self.lambdas):.4f}")
        print(f"  Max λ_j:             {max(self.lambdas):.4f}")
        print("\nDefekt-Statistik:")
        nnz_syracuse = self.H_p.nnz if hasattr(self, 'H_p') else 0
        print(f"  Anzahl Defekte:      {nnz_syracuse}")
        print(f"  Defekt-Dichte:       {nnz_syracuse/self.N:.4f}")
        print("="*70 + "\n")
    
    def compare_with_static(self, k: int = 500) -> dict:
        """
        Vergleiche dynamischen Syracuse-Hamiltonian mit statischem Collatz-Hamiltonian.
        
        Dieser Vergleich ist der Kern der Tao-Syracuse-Erweiterung:
        Zeigt die dynamische Syracuse-Trajektorie dieselbe GUE-Signatur wie
        die statischen EABC-Collatz-Gewichte?
        
        Parameters
        ----------
        k : int, optional
            Anzahl der zu berechnenden Eigenwerte, default: 500
        
        Returns
        -------
        dict
            Vergleichsstatistiken beider Spektren
        """
        print("Berechne dynamisches Syracuse-Spektrum...")
        E_dynamic = self.compute_spectrum(k=k, which='SM')
        
        print("Berechne statisches Collatz-Spektrum (Referenz)...")
        H_static = CollatzEABCHamiltonian(
            N=self.N,
            alpha=self.alpha,
            beta=self.beta,
            gamma=self.gamma,
            periodic=self.periodic
        )
        E_static = H_static.compute_spectrum(k=k, which='SM')
        
        return {
            'dynamic': E_dynamic,
            'static': E_static,
            'delta_spectrum': E_dynamic - E_static,
            'dynamic_lambdas': self.lambdas,
            'static_weights': H_static.collatz_weights,
            'trajectory_stats': self.trajectory_stats
        }


class MultiLayerHamiltonian(EABCHamiltonian):
    """
    Arithmetischer Mehrschichten-Hamiltonian mit Glattheitspotential.
    
    H = α H_T + β H_χ + γ H_p + η H_smooth
    
    Dieser Hamiltonian kombiniert vier arithmetische Strukturen:
    1. H_T: Tight-Binding (kinetisch)
    2. H_χ: Chirale EABC-Kopplung
    3. H_p: Primzahl-Defekte (optional mit Collatz-Gewichten)
    4. H_smooth: Glattheitspotential (k-smooth numbers)
    
    Die zentrale Forschungsfrage: Wirkt Glattheit verstärkend oder dämpfend
    auf das Chaos im Spektrum?
    
    Parameters
    ----------
    N : int
        Anzahl der Gitterplätze
    alpha : float, optional
        Hopping-Stärke (kinetischer Term), default: 1.0
    beta : float, optional
        Chirale Kopplung, default: 0.5
    gamma : float, optional
        Primzahl-Defekt-Stärke, default: 1.5
    eta : float, optional
        Glattheitspotential-Stärke, default: 0.5
    periodic : bool, optional
        Periodische Randbedingungen, default: False
    use_primes : bool, optional
        Primzahl-Defekte aktivieren, default: True
    use_collatz : bool, optional
        Collatz-Gewichte für Primzahl-Defekte nutzen, default: False
    use_smooth : bool, optional
        Glattheitspotential aktivieren, default: False
    smooth_max_k : int, optional
        Maximaler k-Wert für Glattheitsdichte, default: 20
    
    Attributes
    ----------
    eta : float
        Glattheitspotential-Stärke
    use_primes, use_collatz, use_smooth : bool
        Flags für aktive Terme
    smooth_max_k : int
        Maximaler k-Wert für Glattheit
    H_smooth : scipy.sparse.csr_matrix, optional
        Glattheitspotential-Term
    smooth_landscape : np.ndarray, optional
        Glattheitsdichten für alle Zahlen
    
    Examples
    --------
    >>> # Nur Glattheitspotential (ohne Primzahlen)
    >>> H1 = MultiLayerHamiltonian(N=1000, use_primes=False, use_smooth=True)
    >>> 
    >>> # Primzahlen + Glattheit
    >>> H2 = MultiLayerHamiltonian(N=1000, use_primes=True, use_smooth=True)
    >>> 
    >>> # Alle Schichten (Primzahlen + Collatz + Glattheit)
    >>> H3 = MultiLayerHamiltonian(N=1000, use_primes=True, use_collatz=True, use_smooth=True)
    
    Notes
    -----
    Das Glattheitspotential H_smooth ordnet glatten Zahlen niedrige Energie zu
    (Potentialsenken) und rauen Zahlen (Primzahlen) hohe Energie (Barrieren):
    
    H_smooth = η Σ_n [-density(n)] |n⟩⟨n| ⊗ 𝟙_EABC
    
    wobei density(n) ∈ [0, 1] die normalisierte Glattheitsdichte ist.
    """
    
    def __init__(
        self,
        N: int,
        alpha: float = 1.0,
        beta: float = 0.5,
        gamma: float = 1.5,
        eta: float = 0.5,
        periodic: bool = False,
        use_primes: bool = True,
        use_collatz: bool = False,
        use_smooth: bool = False,
        smooth_max_k: int = 20
    ):
        # Parameter speichern
        self.eta = eta
        self.use_primes = use_primes
        self.use_collatz = use_collatz
        self.use_smooth = use_smooth
        self.smooth_max_k = smooth_max_k
        
        # Basisklassen-Attribute (ohne _build_hamiltonian)
        self.N = N
        self.dim = 4 * N
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.periodic = periodic
        
        # Hamiltonian bauen
        self._build_hamiltonian()
    
    def _build_smooth_potential(self) -> sp.csr_matrix:
        """
        Konstruiere das Glattheitspotential H_smooth.
        
        Konzept:
        - Glatte Zahlen (hohe Dichte) = niedrige Energie (Senken)
        - Primzahlen (niedrige Dichte) = hohe Energie (Barrieren)
        
        H_smooth = η Σ_n [-density(n)] |n⟩⟨n| ⊗ 𝟙_EABC
        
        Das negative Vorzeichen sorgt dafür, dass hohe Glattheit zu niedriger
        Energie führt (Potentialsenken bei glatten Zahlen).
        
        Returns
        -------
        scipy.sparse.csr_matrix
            H_smooth mit Dimension 4N × 4N
        """
        print(f"  Berechne Glattheitspotential (max_k={self.smooth_max_k})...")
        
        # Berechne Glattheitsdichten für alle Zahlen 1..N
        self.smooth_landscape = smooth_potential_landscape(self.N, self.smooth_max_k)
        
        # Sparse Matrix im COO-Format
        rows = []
        cols = []
        data = []
        
        for n in range(1, self.N + 1):
            density = self.smooth_landscape[n-1]
            
            # Potential = -density (glatt = niedrig)
            # Skaliere so, dass Potential ∈ [-1, 0] (da density ∈ [0, 1])
            potential = -density
            
            # Diagonalterm für alle 4 EABC-Zustände
            for sigma in range(4):
                idx = 4 * (n - 1) + sigma
                rows.append(idx)
                cols.append(idx)
                data.append(self.eta * potential)
        
        # In CSR-Format konvertieren
        H_smooth = sp.csr_matrix(
            (data, (rows, cols)),
            shape=(self.dim, self.dim)
        )
        
        print(f"  ✓ Glattheitspotential: ⟨density⟩ = {np.mean(self.smooth_landscape):.3f}")
        
        return H_smooth
    
    def _build_hamiltonian(self):
        """
        Konstruiere den Multi-Layer-Hamiltonian.
        
        H = α H_T + β H_χ + [γ H_p] + [η H_smooth]
        
        wobei [...] optional je nach Flags sind.
        """
        print(f"Konstruiere Multi-Layer-Hamiltonian für N = {self.N}...")
        
        # Basis-Terme (immer vorhanden)
        print("  [1/4] Kinetischer Term H_T...")
        self.H_T = self._build_tight_binding()
        
        print("  [2/4] Chiraler Term H_χ...")
        self.H_chi = self._build_chiral_term()
        
        # Summiere Basis
        self.H = self.alpha * self.H_T + self.beta * self.H_chi
        
        # Optional: Primzahl-Defekte
        if self.use_primes:
            print("  [3/4] Primzahl-Defekte H_p...")
            if self.use_collatz:
                print("        (mit Collatz-Gewichten)")
                # Verwende Collatz-gewichtete Defekte
                from .collatz_weights import collatz_log_rate_prime
                primes = generate_primes(self.N)
                
                rows, cols, data = [], [], []
                for p in primes:
                    sigma = eabc_index(p)
                    idx = 4 * (p - 1) + sigma
                    weight = collatz_log_rate_prime(p)
                    
                    rows.append(idx)
                    cols.append(idx)
                    data.append(weight)
                
                self.H_p = sp.csr_matrix(
                    (data, (rows, cols)),
                    shape=(self.dim, self.dim)
                )
            else:
                print("        (uniform)")
                self.H_p = self._build_prime_defects()
            
            self.H = self.H + self.gamma * self.H_p
        else:
            print("  [3/4] Primzahl-Defekte H_p... (deaktiviert)")
            self.H_p = sp.csr_matrix((self.dim, self.dim))
        
        # Optional: Glattheitspotential
        if self.use_smooth:
            print("  [4/4] Glattheitspotential H_smooth...")
            self.H_smooth = self._build_smooth_potential()
            self.H = self.H + self.H_smooth
        else:
            print("  [4/4] Glattheitspotential H_smooth... (deaktiviert)")
            self.H_smooth = sp.csr_matrix((self.dim, self.dim))
        
        # Speicherstatistik
        nnz = self.H.nnz
        sparsity = 100 * nnz / (self.dim ** 2)
        print(f"✓ Multi-Layer-Hamiltonian: {nnz} Nicht-Null-Einträge ({sparsity:.4f}%)")
    
    def info(self):
        """Zeige System-Informationen mit allen Schichten."""
        print("\n" + "="*70)
        print("Multi-Layer-Arithmetischer Hamiltonian")
        print("="*70)
        print(f"Gittergröße N:         {self.N}")
        print(f"Hilbertraum-Dimension: {self.dim} (= 4N)")
        print(f"Periodische Randbedingungen: {self.periodic}")
        
        print("\nKopplungskonstanten:")
        print(f"  α (Hopping):            {self.alpha:.3f}")
        print(f"  β (Chiralität):         {self.beta:.3f}")
        print(f"  γ (Primzahl-Defekt):    {self.gamma:.3f} {'✓' if self.use_primes else '✗'}")
        print(f"  η (Glattheitspotential):{self.eta:.3f} {'✓' if self.use_smooth else '✗'}")
        
        print("\nAktive Schichten:")
        print(f"  Tight-Binding (H_T):    ✓ (immer aktiv)")
        print(f"  Chiralität (H_χ):       ✓ (immer aktiv)")
        print(f"  Primzahl-Defekte (H_p): {'✓' if self.use_primes else '✗'}")
        if self.use_primes:
            print(f"    → Collatz-Gewichte:   {'✓' if self.use_collatz else '✗'}")
        print(f"  Glattheitspotential:    {'✓' if self.use_smooth else '✗'}")
        if self.use_smooth:
            print(f"    → max_k:              {self.smooth_max_k}")
            print(f"    → ⟨density⟩:          {np.mean(self.smooth_landscape):.3f}")
            print(f"    → σ(density):         {np.std(self.smooth_landscape):.3f}")
        
        if self.use_primes:
            print("\nPrimzahl-Statistik:")
            primes = generate_primes(self.N)
            print(f"  Anzahl Primzahlen ≤ N: {len(primes)}")
            print(f"  Defekt-Dichte:         {len(primes)/self.N:.4f}")
        
        print("="*70 + "\n")


if __name__ == "__main__":
    # Demonstration
    print("=== EABC-Hamiltonian Demo ===\n")
    
    # Kleines System für Test
    H = EABCHamiltonian(N=100, alpha=1.0, beta=0.3, gamma=2.0)
    H.info()
    
    # Spektrum berechnen
    eigenvalues = H.compute_spectrum(k=50, which='SM')
    
    print("\nErste 10 Eigenwerte:")
    for i, E in enumerate(eigenvalues[:10]):
        print(f"  E_{i+1} = {E:.6f}")
    
    # Collatz-Version testen
    print("\n\n=== Collatz-EABC-Hamiltonian Demo ===\n")
    H_collatz = CollatzEABCHamiltonian(N=100, alpha=1.0, beta=0.3, gamma=2.0)
    H_collatz.info()
    
    eigenvalues_collatz = H_collatz.compute_spectrum(k=50, which='SM')
    
    print("\nErste 10 Eigenwerte (Collatz-gewichtet):")
    for i, E in enumerate(eigenvalues_collatz[:10]):
        print(f"  E_{i+1} = {E:.6f}")
    
    # Tao-Syracuse-Version testen
    print("\n\n=== Tao-Syracuse-EABC-Hamiltonian Demo ===\n")
    H_tao = TaoSyracuseHamiltonian(N=100, start_n=27, trajectory_length=30, alpha=1.0, beta=0.3, gamma=2.0)
    H_tao.info()
    
    eigenvalues_tao = H_tao.compute_spectrum(k=50, which='SM')
    
    print("\nErste 10 Eigenwerte (Tao-Syracuse):")
    for i, E in enumerate(eigenvalues_tao[:10]):
        print(f"  E_{i+1} = {E:.6f}")
    
    # Multi-Layer-Version testen
    print("\n\n=== Multi-Layer-Hamiltonian Demo ===\n")
    H_multi = MultiLayerHamiltonian(
        N=100, 
        alpha=1.0, 
        beta=0.3, 
        gamma=2.0, 
        eta=0.5,
        use_primes=True,
        use_collatz=False,
        use_smooth=True,
        smooth_max_k=20
    )
    H_multi.info()
    
    eigenvalues_multi = H_multi.compute_spectrum(k=50, which='SM')
    
    print("\nErste 10 Eigenwerte (Multi-Layer):")
    for i, E in enumerate(eigenvalues_multi[:10]):
        print(f"  E_{i+1} = {E:.6f}")
