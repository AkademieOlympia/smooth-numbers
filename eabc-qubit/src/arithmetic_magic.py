"""
Arithmetische Magic M_EABC: Spektrale Nichtreduzierbarkeit des EABC-Dirac-Systems

KONZEPTIONELLE VERFEINERUNG (2026-06-23):

**Arithmetische Magic ≠ Chiralität selbst**

Sondern:

**Arithmetische Magic = spektrale Nichtreduzierbarkeit des EABC-Dirac-Systems**

Die Chiralität ist nicht die Quelle, sondern ein makroskopischer Ordnungsparameter.

## Kausale Hierarchie

```
Near-Zero-Spektrum → chiraler Drift → sichtbare ABCE/CEAB-Asymmetrie
```

Die Near-Zero-Moden sind der **Ofen**, die Orientierungszählung ist nur das **Thermometer**.

## Definition von M_EABC(N)

Fokus auf den **Near-Zero-Sektor des Dirac-Spektrums**:

**Option 1 (Asymmetrie-basiert):**
```
M_EABC(N) = Σ_{λ_i ≈ 0} w_i · |ρ_i^{ABCE} - ρ_i^{CEAB}|
```

**Option 2 (Spektral gewichtet):**
```
M_EABC(N) = Σ_{|λ_i|<ε} (1/(|λ_i|+δ)) · Asym(v_i)
```

Dabei:
- λ_i: Dirac-Eigenwerte
- v_i: Eigenvektoren
- Asym(v_i): ABCE/CEAB-Asymmetrie im Eigenmodus
- ε: Near-Zero-Fenster (z.B. ε=0.1)
- δ: Regularisierung (z.B. δ=0.01)

## Holographie-Analogie (verstärkt)

| Holographie | EABC |
|-------------|------|
| Entanglement | Vierlingspopulation Q_4(N) |
| Code-Subspace | mod-420 / Wigner-Zellen |
| **Magic** | **Near-Zero-Dirac-Sektor** |
| Gravitative Rückwirkung | chiraler Drift |
| Krümmung | ABCE/CEAB-Bias |

## Der entscheidende Test

```
M_EABC(N) hoch ⇒ starker chiraler Bias
```

**Nicht umgekehrt!** Magic ist die Ursache, Bias ist die Wirkung.

---

Dieses Modul implementiert sowohl die Near-Zero-basierten Magic-Maße (primär)
als auch globale Metriken (zum Vergleich).
"""

import numpy as np
from typing import Dict, Optional, Tuple
from .primes import generate_primes, eabc_index
from .collatz_weights import collatz_log_rate_prime


class ArithmeticMagic:
    """
    Arithmetische Magic M_EABC: Maß für Abweichung von perfekter EABC-Symmetrie.
    
    Implementiert verschiedene Magic-Maße:
    1. M_bias: EABC vs ECBA Ungleichgewicht (aus Primzahl-Projekt)
    2. M_collatz: Anisotropie der Collatz-Gewichte
    3. M_chi: Relative Stärke des chiralen Terms
    4. M_nzm: Near-Zero-Mode-Konzentration
    5. M_gap: Gap-Asymmetrie (aus Primzahl-Projekt)
    6. M_symbreak: Symmetriebrechungs-Index
    
    Parameters
    ----------
    hamiltonian : EABCHamiltonian oder abgeleitete Klasse
        Der zu analysierende Hamiltonian
    
    Attributes
    ----------
    H : EABCHamiltonian
        Referenz zum Hamiltonian
    magic_values : Dict[str, float]
        Berechnete Magic-Werte
    
    Examples
    --------
    >>> from .hamiltonian import EABCHamiltonian
    >>> H = EABCHamiltonian(N=1000, beta=0.5, gamma=1.5)
    >>> magic = ArithmeticMagic(H)
    >>> M_all = magic.compute_all()
    >>> print(f"M_chi = {M_all['M_chi']:.4f}")
    """
    
    def __init__(self, hamiltonian):
        """
        Initialisiere ArithmeticMagic-Objekt.
        
        Parameters
        ----------
        hamiltonian : EABCHamiltonian
            Der zu analysierende Hamiltonian
        """
        self.H = hamiltonian
        self.magic_values = {}
        
        # Vorbereitung: EABC-Klassen der Primzahlen
        self.primes = generate_primes(self.H.N)
        self.eabc_classes = [eabc_index(p) for p in self.primes]
    
    def compute_bias_magic(self) -> float:
        """
        M_bias: EABC vs ECBA Ungleichgewicht.
        
        Aus dem Primzahl-Projekt bekannt: Es gibt einen Bias zugunsten von
        EABC-Übergängen gegenüber ECBA-Übergängen. Der Bias-Parameter R(X)
        misst dieses Ungleichgewicht.
        
        M_bias = |P(EABC) - P(ECBA)|
        
        Approximation: Wir nutzen die EABC-Verteilung der Primzahlen als Proxy:
        M_bias ≈ Standardabweichung der EABC-Klassenhäufigkeiten
        
        Returns
        -------
        float
            M_bias Wert (0 = perfekte Symmetrie, >0 = Bias)
        
        Notes
        -----
        Eine hohe Standardabweichung der Klassenhäufigkeiten deutet auf
        ein Ungleichgewicht hin, das die Symmetrie bricht.
        """
        # Zähle Häufigkeiten der EABC-Klassen
        class_counts = np.zeros(4)
        for eabc_class in self.eabc_classes:
            class_counts[eabc_class] += 1
        
        # Normalisiere
        class_frequencies = class_counts / len(self.primes)
        
        # Bias = Abweichung von Gleichverteilung (1/4 für jede Klasse)
        uniform = 0.25
        deviations = class_frequencies - uniform
        
        # M_bias = RMS-Abweichung
        M_bias = np.sqrt(np.mean(deviations**2))
        
        return M_bias
    
    def compute_collatz_magic(self) -> float:
        """
        M_collatz: Anisotropie der Collatz-Gewichte.
        
        Die Collatz-Gewichte λ_E, λ_A, λ_B, λ_C sind nicht uniform verteilt.
        Diese Anisotropie bricht die Z₄-Symmetrie des EABC-Systems.
        
        M_collatz = Σ_classes |λ_i - ⟨λ⟩|² / ⟨λ⟩²
        
        wobei:
        - λ_E ≈ -0.693 (E-Klasse: p ≡ 1 mod 12)
        - λ_A ≈ -0.143 (A-Klasse: p ≡ 5 mod 12)
        - λ_B ≈ +0.693 (B-Klasse: p ≡ 7 mod 12)
        - λ_C ≈ +0.405 (C-Klasse: p ≡ 11 mod 12)
        
        Returns
        -------
        float
            M_collatz Wert (0 = uniform, >0 = anisotrop)
        
        Notes
        -----
        Diese Magic misst die intrinsische Asymmetrie der Collatz-Dynamik
        im EABC-Raum. Sie ist unabhängig vom β-Parameter.
        """
        # Theoretische Collatz-Gewichte für EABC-Klassen
        # Aus Paper C: "Conditional Collatz via G2 Log-Drift Axiom"
        lambda_weights = np.array([
            -0.693147,  # λ_E (E = 0)
            -0.143841,  # λ_A (A = 1)
            +0.693147,  # λ_B (B = 2)
            +0.405465   # λ_C (C = 3)
        ])
        
        # Wenn Collatz-Hamiltonian, verwende tatsächliche Gewichte
        if hasattr(self.H, 'collatz_weights'):
            # Mittlere Gewichte pro EABC-Klasse
            class_weights = np.zeros(4)
            class_counts = np.zeros(4)
            
            for i, p in enumerate(self.primes):
                eabc_class = eabc_index(p)
                class_weights[eabc_class] += self.H.collatz_weights[i]
                class_counts[eabc_class] += 1
            
            # Mittelwerte
            mask = class_counts > 0
            lambda_weights = np.where(mask, class_weights / class_counts, 0)
        
        # Berechne Anisotropie
        mean_lambda = np.mean(lambda_weights)
        
        # Schutz vor Division durch Null
        if abs(mean_lambda) < 1e-10:
            mean_lambda = 1.0
        
        M_collatz = np.sum((lambda_weights - mean_lambda)**2) / mean_lambda**2
        
        return M_collatz
    
    def compute_chirality_magic(self) -> float:
        """
        M_chi: Relative Stärke des chiralen Terms.
        
        Der chirale Term H_χ bricht die Z₄-Symmetrie durch zyklische Kopplung:
        E → C → B → A → E
        
        M_chi = β · ||H_χ|| / ||H_total||
        
        Dies ist der direkteste Magic-Parameter, da β explizit die Stärke
        der Symmetriebrechung kontrolliert.
        
        Returns
        -------
        float
            M_chi Wert (0 = keine Chiralität, >0 = chirale Kopplung)
        
        Notes
        -----
        Dies sollte der dominante Magic-Parameter sein, da β direkt
        die Deviation von der Z₄-Symmetrie steuert.
        """
        # Normen berechnen
        norm_chi = np.linalg.norm(self.H.H_chi.data)
        norm_total = np.linalg.norm(self.H.H.data)
        
        # Schutz vor Division durch Null
        if norm_total < 1e-10:
            return 0.0
        
        M_chi = self.H.beta * norm_chi / norm_total
        
        return M_chi
    
    def compute_nzm_magic(
        self, 
        epsilon: float = 0.1,
        k: Optional[int] = None
    ) -> float:
        """
        M_nzm: Near-Zero-Mode-Konzentration.
        
        Misst, wie stark das Spektrum in Near-Zero-Moden kondensiert.
        Dies ist analog zum POP (Participation Ratio) in Anderson-Lokalisierung.
        
        M_nzm = Σ_{|E_i| < ε} 1 / N_total
        
        wobei ε die Schwelle für "nahe Null" ist.
        
        Parameters
        ----------
        epsilon : float, optional
            Schwelle für Near-Zero-Moden, default: 0.1
        k : int, optional
            Anzahl der zu berechnenden Eigenwerte, default: min(500, dim//2)
        
        Returns
        -------
        float
            M_nzm Wert (0 = keine NZM, 1 = alle Moden bei Null)
        
        Notes
        -----
        Hohe M_nzm deutet auf Kondensation nahe der Fermi-Energie hin,
        was typisch für kritische Systeme ist.
        """
        if k is None:
            k = min(500, self.H.dim // 2)
        
        # Berechne Spektrum (mittlere Eigenwerte)
        print(f"  Berechne {k} Eigenwerte für NZM-Analyse...")
        eigenvalues = self.H.compute_spectrum(k=k, which='SM', sigma=0.0)
        
        # Zähle Near-Zero-Moden
        near_zero = np.sum(np.abs(eigenvalues) < epsilon)
        
        M_nzm = near_zero / len(eigenvalues)
        
        return M_nzm
    
    def compute_gap_magic(self) -> float:
        """
        M_gap: Gap-Asymmetrie (aus Primzahl-Projekt).
        
        Im Primzahl-Projekt wurde beobachtet, dass Primzahllücken eine
        mod-12-Struktur zeigen. Diese Asymmetrie bricht die Translationsinvarianz.
        
        M_gap = |P(g≡2,4 mod 12) - P(g≡8,10 mod 12)|
        
        Approximation: Wir nutzen die Verteilung der Primzahllücken als Proxy.
        
        Returns
        -------
        float
            M_gap Wert (0 = symmetrisch, >0 = asymmetrisch)
        
        Notes
        -----
        Dies ist eine indirekte Magic, die die arithmetische Struktur
        der Primzahlverteilung reflektiert.
        """
        if len(self.primes) < 2:
            return 0.0
        
        # Berechne Primzahllücken
        gaps = np.diff(self.primes)
        
        # Klassifiziere nach mod 12
        gaps_mod12 = gaps % 12
        
        # Zähle g ≡ 2,4 mod 12 vs. g ≡ 8,10 mod 12
        count_low = np.sum((gaps_mod12 == 2) | (gaps_mod12 == 4))
        count_high = np.sum((gaps_mod12 == 8) | (gaps_mod12 == 10))
        
        # Normalisiere
        total = count_low + count_high
        if total == 0:
            return 0.0
        
        P_low = count_low / total
        P_high = count_high / total
        
        M_gap = abs(P_low - P_high)
        
        return M_gap
    
    def compute_symbreak_magic(self) -> float:
        """
        M_symbreak: Symmetriebrechungs-Index.
        
        Misst die Invarianz unter Permutationen von {E,A,B,C}.
        Perfekte S₄-Symmetrie würde M_symbreak = 0 ergeben.
        
        M_symbreak = 1 - S₄_invariance
        
        wobei S₄_invariance die relative Invarianz unter allen 24 Permutationen ist.
        
        Returns
        -------
        float
            M_symbreak Wert (0 = perfekte S₄-Symmetrie, 1 = maximale Brechung)
        
        Notes
        -----
        Dies ist das abstrakteste Magic-Maß, da es die globale Symmetrie
        des Systems bewertet.
        """
        # Berechne Häufigkeiten der EABC-Klassen
        class_counts = np.zeros(4)
        for eabc_class in self.eabc_classes:
            class_counts[eabc_class] += 1
        
        # Normalisiere
        class_frequencies = class_counts / len(self.primes)
        
        # S₄-Invarianz = Wie gleichverteilt sind die Klassen?
        # Perfekte Symmetrie: alle Frequenzen = 1/4
        # Berechne Gini-Koeffizient als Invarianz-Maß
        sorted_freq = np.sort(class_frequencies)
        n = len(sorted_freq)
        index = np.arange(1, n + 1)
        gini = (2 * np.sum(index * sorted_freq)) / (n * np.sum(sorted_freq)) - (n + 1) / n
        
        # M_symbreak = Gini-Koeffizient (0 = perfekte Gleichheit, 1 = maximale Ungleichheit)
        M_symbreak = gini
        
        return M_symbreak
    
    # =========================================================================
    # NEAR-ZERO-SEKTOR-BASIERTE MAGIC (PRIMÄRE DEFINITION)
    # =========================================================================
    
    def extract_near_zero_modes(
        self,
        epsilon: float = 0.1,
        k: Optional[int] = None,
        sigma: float = 0.0
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Extrahiere Near-Zero-Eigenmoden aus dem Spektrum.
        
        Dies ist die Grundlage für die Near-Zero-basierte Magic-Definition.
        Die Near-Zero-Moden sind der "Ofen" der arithmetischen Magic!
        
        Parameters
        ----------
        epsilon : float, optional
            Schwelle für Near-Zero: |λ_i| < ε, default: 0.1
        k : int, optional
            Anzahl der zu berechnenden Eigenwerte, default: min(500, dim//2)
        sigma : float, optional
            Shift für Spektrum-Targeting (0.0 für mittlere Eigenwerte), default: 0.0
        
        Returns
        -------
        eigenvalues : np.ndarray
            Near-Zero-Eigenwerte (|λ_i| < ε)
        eigenvectors : np.ndarray
            Zugehörige Eigenvektoren (Matrix, Spalten sind Eigenvektoren)
        
        Notes
        -----
        Diese Funktion ist rechenintensiv, da sie eine partielle Diagonalisierung
        des Hamiltonians erfordert!
        """
        if k is None:
            k = min(500, self.H.dim // 2)
        
        print(f"  Extrahiere Near-Zero-Moden (ε={epsilon}, k={k})...")
        
        # Berechne Eigenwerte und Eigenvektoren
        eigenvalues, eigenvectors = self.H.compute_spectrum(
            k=k,
            which='SM',
            sigma=sigma,
            return_eigenvectors=True
        )
        
        # Filtere Near-Zero-Moden
        near_zero_mask = np.abs(eigenvalues) < epsilon
        nzm_eigenvalues = eigenvalues[near_zero_mask]
        nzm_eigenvectors = eigenvectors[:, near_zero_mask]
        
        n_nzm = len(nzm_eigenvalues)
        print(f"  ✓ Gefunden: {n_nzm}/{k} Near-Zero-Moden (|λ| < {epsilon})")
        
        return nzm_eigenvalues, nzm_eigenvectors
    
    def eigenvector_asymmetry(
        self,
        eigenvector: np.ndarray,
        pattern: str = 'ABCE_CEAB'
    ) -> float:
        """
        Berechne ABCE/CEAB-Asymmetrie eines Eigenvektors.
        
        Der Eigenvektor hat Dimension 4N (N Gitterplätze × 4 EABC-Zustände).
        Wir projizieren auf ABCE- und CEAB-Orientierungen und messen die Differenz.
        
        Parameters
        ----------
        eigenvector : np.ndarray
            Eigenvektor (Länge 4N)
        pattern : str, optional
            Asymmetrie-Muster, default: 'ABCE_CEAB'
            - 'ABCE_CEAB': |ρ^{ABCE} - ρ^{CEAB}|
            - 'EABC_ECBA': |ρ^{EABC} - ρ^{ECBA}|
        
        Returns
        -------
        float
            Asymmetrie-Maß (0 = perfekte Symmetrie, >0 = Asymmetrie)
        
        Notes
        -----
        Interpretation der EABC-Indizes:
        - E = 0 (p ≡ 1 mod 12)
        - A = 1 (p ≡ 5 mod 12)
        - B = 2 (p ≡ 7 mod 12)
        - C = 3 (p ≡ 11 mod 12)
        
        ABCE-Orientierung: (A, B, C, E) = (1, 2, 3, 0)
        CEAB-Orientierung: (C, E, A, B) = (3, 0, 1, 2)
        """
        N = self.H.N
        v = eigenvector.reshape(N, 4)  # Reshape: (4N,) → (N, 4)
        
        if pattern == 'ABCE_CEAB':
            # ABCE: (A=1, B=2, C=3, E=0) → Indizes [1, 2, 3, 0]
            # CEAB: (C=3, E=0, A=1, B=2) → Indizes [3, 0, 1, 2]
            ABCE_indices = [1, 2, 3, 0]
            CEAB_indices = [3, 0, 1, 2]
            
        elif pattern == 'EABC_ECBA':
            # EABC: (E=0, A=1, B=2, C=3) → Indizes [0, 1, 2, 3]
            # ECBA: (E=0, C=3, B=2, A=1) → Indizes [0, 3, 2, 1]
            ABCE_indices = [0, 1, 2, 3]
            CEAB_indices = [0, 3, 2, 1]
            
        else:
            raise ValueError(f"Unbekanntes Muster: {pattern}")
        
        # Berechne Wahrscheinlichkeitsdichten
        # ρ^{ABCE} = Σ_n |v_n^A|² |v_n^B|² |v_n^C|² |v_n^E|²
        # (vereinfacht: Summe der Amplituden in ABCE-Reihenfolge)
        
        rho_ABCE = 0.0
        rho_CEAB = 0.0
        
        for n in range(N):
            # ABCE-Projektion (zyklische Produkte)
            amp_ABCE = np.prod([np.abs(v[n, idx])**2 for idx in ABCE_indices])
            rho_ABCE += amp_ABCE
            
            # CEAB-Projektion
            amp_CEAB = np.prod([np.abs(v[n, idx])**2 for idx in CEAB_indices])
            rho_CEAB += amp_CEAB
        
        # Normalisierung (optional, für Vergleichbarkeit)
        total = rho_ABCE + rho_CEAB
        if total > 1e-10:
            rho_ABCE /= total
            rho_CEAB /= total
        
        # Asymmetrie
        asymmetry = np.abs(rho_ABCE - rho_CEAB)
        
        return asymmetry
    
    def compute_near_zero_magic(
        self,
        epsilon: float = 0.1,
        k: Optional[int] = None,
        delta: float = 0.01,
        mode: str = 'spectral_weighted',
        pattern: str = 'ABCE_CEAB'
    ) -> Dict[str, float]:
        """
        Berechne Near-Zero-basierte arithmetische Magic M_EABC(N).
        
        **PRIMÄRE DEFINITION**: Dies ist die theoretisch fundierteste Definition,
        die direkt zur Quanteninformations-Definition von Magic passt!
        
        Kausale Hierarchie:
        ```
        Near-Zero-Spektrum → chiraler Drift → ABCE/CEAB-Asymmetrie
        ```
        
        Parameters
        ----------
        epsilon : float, optional
            Near-Zero-Schwelle: |λ_i| < ε, default: 0.1
        k : int, optional
            Anzahl Eigenwerte, default: min(500, dim//2)
        delta : float, optional
            Regularisierung für spektrale Gewichtung, default: 0.01
        mode : str, optional
            Berechnungsmodus, default: 'spectral_weighted'
            - 'asymmetry_based': M = Σ_i w_i · Asym(v_i)
            - 'spectral_weighted': M = Σ_i (1/(|λ_i|+δ)) · Asym(v_i)
            - 'count': M = Anzahl Near-Zero-Moden / k
        pattern : str, optional
            Asymmetrie-Muster, default: 'ABCE_CEAB'
        
        Returns
        -------
        Dict[str, float]
            Dictionary mit:
            - 'M_near_zero': Near-Zero-Magic-Wert
            - 'n_nzm': Anzahl Near-Zero-Moden
            - 'mean_asymmetry': Mittlere Asymmetrie
            - 'max_asymmetry': Maximale Asymmetrie
            - 'total_weight': Gesamtgewicht (für spektrale Gewichtung)
        
        Examples
        --------
        >>> magic = ArithmeticMagic(H)
        >>> M_nz = magic.compute_near_zero_magic(epsilon=0.1, mode='spectral_weighted')
        >>> print(f"M_near_zero = {M_nz['M_near_zero']:.4f}")
        
        Notes
        -----
        **WICHTIG**: Dies ist rechenintensiv, da Eigenvektoren berechnet werden müssen!
        Für große Systeme (N > 1000) kann dies mehrere Minuten dauern.
        
        Die Near-Zero-Magic ist der "Ofen", chiraler Bias ist das "Thermometer"!
        """
        print(f"\n  Berechne Near-Zero-basierte Magic (Primäre Definition)...")
        
        # Extrahiere Near-Zero-Moden
        nzm_eigenvalues, nzm_eigenvectors = self.extract_near_zero_modes(
            epsilon=epsilon,
            k=k,
            sigma=0.0
        )
        
        n_nzm = len(nzm_eigenvalues)
        
        if n_nzm == 0:
            print(f"  ✗ Keine Near-Zero-Moden gefunden (ε={epsilon})!")
            return {
                'M_near_zero': 0.0,
                'n_nzm': 0,
                'mean_asymmetry': 0.0,
                'max_asymmetry': 0.0,
                'total_weight': 0.0
            }
        
        # Berechne Asymmetrien für alle Near-Zero-Moden
        print(f"  Berechne Asymmetrien für {n_nzm} Near-Zero-Moden...")
        asymmetries = np.zeros(n_nzm)
        
        for i in range(n_nzm):
            eigenvector = nzm_eigenvectors[:, i]
            asymmetries[i] = self.eigenvector_asymmetry(eigenvector, pattern=pattern)
        
        # Berechne Magic je nach Modus
        if mode == 'asymmetry_based':
            # M = Σ_i w_i · Asym(v_i) mit uniform Gewichten w_i = 1/n_nzm
            weights = np.ones(n_nzm) / n_nzm
            M_near_zero = np.sum(weights * asymmetries)
            total_weight = 1.0
            
        elif mode == 'spectral_weighted':
            # M = Σ_i (1/(|λ_i|+δ)) · Asym(v_i)
            weights = 1.0 / (np.abs(nzm_eigenvalues) + delta)
            M_near_zero = np.sum(weights * asymmetries)
            total_weight = np.sum(weights)
            
            # Normalisiere (optional)
            M_near_zero /= total_weight
            
        elif mode == 'count':
            # M = Anzahl Near-Zero-Moden / k (einfachstes Maß)
            M_near_zero = n_nzm / (k if k is not None else self.H.dim // 2)
            total_weight = 1.0
            
        else:
            raise ValueError(f"Unbekannter Modus: {mode}")
        
        # Statistiken
        mean_asymmetry = np.mean(asymmetries)
        max_asymmetry = np.max(asymmetries)
        
        print(f"  ✓ Near-Zero-Magic berechnet:")
        print(f"    M_near_zero = {M_near_zero:.6f}")
        print(f"    n_nzm = {n_nzm}")
        print(f"    ⟨Asym⟩ = {mean_asymmetry:.6f}")
        print(f"    max(Asym) = {max_asymmetry:.6f}")
        
        return {
            'M_near_zero': M_near_zero,
            'n_nzm': n_nzm,
            'mean_asymmetry': mean_asymmetry,
            'max_asymmetry': max_asymmetry,
            'total_weight': total_weight
        }
    
    def compute_all(
        self,
        compute_nzm: bool = False,
        compute_near_zero: bool = False,
        epsilon: float = 0.1,
        k: Optional[int] = None,
        nz_mode: str = 'spectral_weighted',
        nz_pattern: str = 'ABCE_CEAB'
    ) -> Dict[str, float]:
        """
        Berechne alle Magic-Maße.
        
        Parameters
        ----------
        compute_nzm : bool, optional
            Falls True, berechne auch M_nzm (alte Definition, rechenintensiv!), default: False
        compute_near_zero : bool, optional
            Falls True, berechne Near-Zero-basierte Magic (PRIMÄR, sehr rechenintensiv!), default: False
        epsilon : float, optional
            Schwelle für Near-Zero-Moden, default: 0.1
        k : int, optional
            Anzahl Eigenwerte für NZM-Analyse, default: min(500, dim//2)
        nz_mode : str, optional
            Modus für Near-Zero-Magic, default: 'spectral_weighted'
        nz_pattern : str, optional
            Asymmetrie-Muster für Near-Zero-Magic, default: 'ABCE_CEAB'
        
        Returns
        -------
        Dict[str, float]
            Dictionary mit allen Magic-Werten
        
        Examples
        --------
        >>> magic = ArithmeticMagic(H)
        >>> # Schnelle Metriken (globale, zum Vergleich)
        >>> M = magic.compute_all(compute_near_zero=False)
        >>> 
        >>> # Vollständige Analyse mit Near-Zero-Magic (primär!)
        >>> M_full = magic.compute_all(compute_near_zero=True, compute_nzm=True)
        """
        print("Berechne arithmetische Magic M_EABC...")
        print("\n[GLOBALE METRIKEN - Zum Vergleich]")
        
        # Schnelle Maße (keine Diagonalisierung)
        self.magic_values['M_bias'] = self.compute_bias_magic()
        print(f"  M_bias:     {self.magic_values['M_bias']:.6f}")
        
        self.magic_values['M_collatz'] = self.compute_collatz_magic()
        print(f"  M_collatz:  {self.magic_values['M_collatz']:.6f}")
        
        self.magic_values['M_chi'] = self.compute_chirality_magic()
        print(f"  M_chi:      {self.magic_values['M_chi']:.6f}")
        
        self.magic_values['M_gap'] = self.compute_gap_magic()
        print(f"  M_gap:      {self.magic_values['M_gap']:.6f}")
        
        self.magic_values['M_symbreak'] = self.compute_symbreak_magic()
        print(f"  M_symbreak: {self.magic_values['M_symbreak']:.6f}")
        
        # Langsames Maß (Diagonalisierung erforderlich, alte Definition)
        if compute_nzm:
            print("\n[NZM-KONZENTRATION - Alte Definition]")
            self.magic_values['M_nzm'] = self.compute_nzm_magic(epsilon=epsilon, k=k)
            print(f"  M_nzm:      {self.magic_values['M_nzm']:.6f}")
        
        # PRIMÄRE DEFINITION: Near-Zero-basierte Magic
        if compute_near_zero:
            print("\n[NEAR-ZERO-MAGIC - PRIMÄRE DEFINITION]")
            nz_results = self.compute_near_zero_magic(
                epsilon=epsilon,
                k=k,
                mode=nz_mode,
                pattern=nz_pattern
            )
            
            # Füge alle Near-Zero-Ergebnisse hinzu
            self.magic_values['M_near_zero'] = nz_results['M_near_zero']
            self.magic_values['n_nzm'] = nz_results['n_nzm']
            self.magic_values['mean_asymmetry'] = nz_results['mean_asymmetry']
            self.magic_values['max_asymmetry'] = nz_results['max_asymmetry']
        
        print("\n✓ Magic-Berechnung abgeschlossen\n")
        
        return self.magic_values
    
    def summary(self) -> str:
        """
        Erstelle einen lesbaren Summary-String aller Magic-Werte.
        
        Returns
        -------
        str
            Formatierter Summary
        """
        if not self.magic_values:
            return "Keine Magic-Werte berechnet. Rufe compute_all() auf."
        
        summary = "\n" + "="*60 + "\n"
        summary += "Arithmetische Magic M_EABC: Summary\n"
        summary += "="*60 + "\n"
        summary += f"System: N = {self.H.N}, β = {self.H.beta:.3f}, γ = {self.H.gamma:.3f}\n"
        summary += "\nMagic-Maße:\n"
        
        for key, val in sorted(self.magic_values.items()):
            description = {
                'M_bias': 'EABC/ECBA Bias',
                'M_collatz': 'Collatz-Anisotropie',
                'M_chi': 'Chiralitäts-Stärke',
                'M_nzm': 'Near-Zero-Mode-Konzentration',
                'M_gap': 'Gap-Asymmetrie',
                'M_symbreak': 'Symmetriebrechung'
            }.get(key, key)
            
            summary += f"  {key:15s} ({description:30s}): {val:.6f}\n"
        
        summary += "="*60 + "\n"
        
        return summary


def compute_magic_vs_chaos_correlation(
    N: int = 1000,
    beta_values: np.ndarray = None,
    gamma: float = 1.5,
    k: int = 500
) -> Tuple[np.ndarray, Dict[str, np.ndarray]]:
    """
    Zentrale Korrelationsanalyse: M_EABC vs. q-Parameter.
    
    Variiere β (Chiralitäts-Stärke) und messe Korrelation zwischen
    Magic-Maßen (insbesondere M_chi) und dem Brody-Parameter q.
    
    Hypothese: M_EABC ↑ ⟹ q ↑ ⟹ σ(s) → σ_GUE
    
    Parameters
    ----------
    N : int, optional
        Gittergröße, default: 1000
    beta_values : np.ndarray, optional
        Array von β-Werten zum Testen, default: [0.0, 0.1, 0.3, 0.5, 0.7, 1.0]
    gamma : float, optional
        Primzahl-Defekt-Stärke, default: 1.5
    k : int, optional
        Anzahl Eigenwerte für Spektralanalyse, default: 500
    
    Returns
    -------
    beta_values : np.ndarray
        Getestete β-Werte
    results : Dict[str, np.ndarray]
        Dictionary mit Arrays für jedes Magic-Maß und q-Parameter
    
    Notes
    -----
    Diese Funktion ist das Herzstück der Magic-Hypothese!
    Falls M_chi stark mit q korreliert, ist die Hypothese bestätigt.
    """
    from .hamiltonian import EABCHamiltonian
    from .level_spacing import compute_level_spacing, fit_level_statistics
    from .spectral import spectral_unfolding
    
    if beta_values is None:
        beta_values = np.array([0.0, 0.1, 0.3, 0.5, 0.7, 1.0])
    
    n_beta = len(beta_values)
    
    # Ergebnis-Arrays
    results = {
        'M_bias': np.zeros(n_beta),
        'M_collatz': np.zeros(n_beta),
        'M_chi': np.zeros(n_beta),
        'M_gap': np.zeros(n_beta),
        'M_symbreak': np.zeros(n_beta),
        'q_brody': np.zeros(n_beta)
    }
    
    print("\n" + "="*70)
    print("MAGIC vs. CHAOS KORRELATIONSANALYSE")
    print("="*70)
    print(f"Parameter-Sweep: β ∈ {beta_values}")
    print(f"System: N = {N}, γ = {gamma}, k = {k}")
    print("="*70 + "\n")
    
    for i, beta in enumerate(beta_values):
        print(f"\n[{i+1}/{n_beta}] β = {beta:.2f}")
        print("-" * 70)
        
        # Konstruiere Hamiltonian
        H = EABCHamiltonian(N=N, beta=beta, gamma=gamma)
        
        # Berechne Magic
        magic = ArithmeticMagic(H)
        M_all = magic.compute_all(compute_nzm=False)
        
        # Speichere Magic-Werte
        for key in ['M_bias', 'M_collatz', 'M_chi', 'M_gap', 'M_symbreak']:
            results[key][i] = M_all[key]
        
        # Berechne Spektrum und Chaos-Parameter
        print(f"\n  Berechne Spektrum...")
        eigenvalues = H.compute_spectrum(k=k, which='SM', sigma=0.0)
        
        # Unfolding
        print(f"  Spektrales Unfolding...")
        unfolded = spectral_unfolding(eigenvalues)
        
        # Level Spacing
        spacings = compute_level_spacing(unfolded)
        
        # Brody-Fit
        print(f"  Fitte Level Spacing Distribution...")
        lsd_results = fit_level_statistics(spacings, bins=50)
        q_brody = lsd_results['brody_q']
        
        results['q_brody'][i] = q_brody
        
        print(f"\n  → M_chi = {M_all['M_chi']:.4f}, q = {q_brody:.4f}")
        print("-" * 70)
    
    print("\n" + "="*70)
    print("KORRELATIONSANALYSE ABGESCHLOSSEN")
    print("="*70)
    
    # Berechne Korrelationen
    print("\nKorrelationen (Pearson) zwischen Magic-Maßen und q:")
    for key in ['M_bias', 'M_collatz', 'M_chi', 'M_gap', 'M_symbreak']:
        corr = np.corrcoef(results[key], results['q_brody'])[0, 1]
        print(f"  {key:15s} vs. q: {corr:+.4f}")
    
    print("\n")
    
    return beta_values, results


if __name__ == "__main__":
    # Demonstration
    from .hamiltonian import EABCHamiltonian
    
    print("=== Arithmetische Magic Demo ===\n")
    
    # Test-System
    H = EABCHamiltonian(N=500, beta=0.5, gamma=1.5)
    H.info()
    
    # Magic berechnen
    magic = ArithmeticMagic(H)
    M_all = magic.compute_all(compute_nzm=True, epsilon=0.1, k=200)
    
    # Summary
    print(magic.summary())
