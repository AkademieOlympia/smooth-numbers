# Catalanische EABC-Normalform - Implementation Roadmap

**Version:** 1.0  
**Datum:** 23. Juni 2026  
**Status:** Planung (nicht implementiert)

---

## Überblick

Dieses Dokument skizziert eine mögliche Code-Struktur für die zukünftige Implementation der catalanischen EABC-Normalform, ohne diese tatsächlich zu implementieren.

---

## Modul-Struktur

### Neue Module

```
src/
├── catalan_normalform.py      # Hauptmodul
├── catalan_tree.py             # Baumstruktur-Klassen
├── catalan_analysis.py         # Statistik & Analyse
└── catalan_visualization.py    # Plots & Baumdarstellungen
```

### Abhängigkeiten

- **Bestehende Module:**
  - `src/primes.py` (Primzahlgenerierung, EABC-Klassifikation)
  - `src/collatz_weights.py` (Gewichte für Blätter)
  
- **Externe Bibliotheken:**
  - `networkx` (für Graphdarstellung der Bäume)
  - `graphviz` oder `pydot` (für Visualisierung)
  - `numpy`, `scipy` (numerische Berechnungen)
  - `matplotlib` (Plots)

---

## 1. Modul: `catalan_tree.py`

### Klasse `CatalanTree`

Repräsentiert einen binären Baum mit EABC-Markierungen.

#### Attribute

```python
class CatalanTree:
    value: int              # Wert an diesem Knoten
    label: str              # EABC-Label ('E', 'A', 'B', 'C', '⊥', None)
    operation: str          # Operation ('+', '×', None)
    left: CatalanTree       # Linker Unterbaum
    right: CatalanTree      # Rechter Unterbaum
    parent: CatalanTree     # Elternknoten (optional, für Traversierung)
```

#### Methoden

```python
def __init__(self, value, label=None, operation=None)
def is_leaf(self) -> bool
def is_root(self) -> bool
def depth(self) -> int
def size(self) -> int                    # Anzahl Knoten
def leaf_count(self) -> int              # Anzahl Blätter
def leaf_labels(self) -> List[str]       # Liste aller Blatt-Labels
def leaf_values(self) -> List[int]       # Liste aller Blatt-Werte (Primzahlen)
def eabc_signature(self) -> Dict[str, int]  # Histogramm von Labels
def collatz_weight(self) -> float        # Gesamtgewicht W(N)
def to_expression(self) -> str           # String-Darstellung "(a×b)×c"
def to_networkx(self) -> nx.DiGraph      # Für Visualisierung
def __repr__(self) -> str
def __str__(self) -> str
```

### Hilfsfunktionen

```python
def build_balanced_tree(nodes: List[CatalanTree], operation: str) -> CatalanTree
    """Baut balancierten Baum aus Liste von Knoten."""

def build_left_tree(nodes: List[CatalanTree], operation: str) -> CatalanTree
    """Baut linkslastigen Baum."""

def build_right_tree(nodes: List[CatalanTree], operation: str) -> CatalanTree
    """Baut rechtslastigen Baum."""
```

---

## 2. Modul: `catalan_normalform.py`

### Hauptfunktionen

#### `build_multiplicative_tree(n, strategy='balanced') -> CatalanTree`

Konstruiert den multiplikativen Baum T_mult für n.

**Parameter:**
- `n: int` - Natürliche Zahl
- `strategy: str` - Klammerungsstrategie ('balanced', 'left', 'right')

**Ablauf:**
1. Primfaktorzerlegung: `factors = prime_factorization(n)`
2. Erstelle Blätter mit EABC-Markierungen
3. Kombiniere nach Strategie

**Pseudocode:**

```python
def build_multiplicative_tree(n, strategy='balanced'):
    from src.primes import prime_factorization, eabc_classification
    from src.catalan_tree import CatalanTree, build_balanced_tree
    
    # Primfaktorzerlegung
    factors = prime_factorization(n)  # [(p1, e1), (p2, e2), ...]
    
    # Blätter mit EABC-Markierungen
    leaves = []
    for p, e in factors:
        label = eabc_classification(p)
        for _ in range(e):
            leaves.append(CatalanTree(p, label=label))
    
    # Sonderfall: n ist Primzahl
    if len(leaves) == 1:
        return leaves[0]
    
    # Kombiniere Blätter nach Strategie
    if strategy == 'balanced':
        return build_balanced_tree(leaves, operation='×')
    elif strategy == 'left':
        return build_left_tree(leaves, operation='×')
    elif strategy == 'right':
        return build_right_tree(leaves, operation='×')
    else:
        raise ValueError(f"Unknown strategy: {strategy}")
```

#### `build_additive_tree(n, strategy='lexmin') -> Optional[CatalanTree]`

Konstruiert den additiven Baum T_add für n.

**Parameter:**
- `n: int` - Natürliche Zahl
- `strategy: str` - Partitionsstrategie ('lexmin', 'balanced', 'minimal')

**Ablauf:**
1. Generiere E-Primzahlen ≤ n
2. Finde Partition von n in E-Summanden (Subset-Sum-Problem)
3. Falls keine Partition existiert: return None
4. Baue Baum aus Partition

**Pseudocode:**

```python
def build_additive_tree(n, strategy='lexmin'):
    from src.primes import sieve, eabc_classification
    from src.catalan_tree import CatalanTree, build_balanced_tree
    
    # E-Primzahlen ≤ n
    e_primes = [p for p in sieve(n) if eabc_classification(p) == 'E']
    
    # Finde Partition (NP-hart, verwende dynamische Programmierung)
    partition = find_e_partition(n, e_primes, strategy)
    
    if partition is None:
        return None
    
    # Baue Baum aus Partition
    leaves = [CatalanTree(p, label='E') for p in partition]
    
    if len(leaves) == 1:
        return leaves[0]
    
    return build_balanced_tree(leaves, operation='+')
```

#### `find_e_partition(n, e_primes, strategy='lexmin') -> Optional[List[int]]`

Findet eine Partition von n in E-Summanden (Subset-Sum-Problem).

**Algorithmus:** Dynamische Programmierung oder Backtracking

**Strategien:**
- `'lexmin'`: Lexikographisch kleinste Partition
- `'minimal'`: Partition mit minimaler Anzahl Summanden
- `'balanced'`: Partition mit möglichst ausgewogener Baumstruktur

### Klasse `CatalanNormalForm`

Repräsentiert die catalanische Normalform einer Zahl.

```python
class CatalanNormalForm:
    def __init__(self, n, mult_strategy='balanced', add_strategy='lexmin'):
        self.n = n
        self.T_mult = build_multiplicative_tree(n, strategy=mult_strategy)
        self.T_add = build_additive_tree(n, strategy=add_strategy)
    
    # Eigenschaften
    def multiplicative_depth(self) -> int
    def additive_depth(self) -> Optional[int]
    def multiplicative_size(self) -> int
    def additive_size(self) -> Optional[int]
    
    # EABC-Signatur
    def eabc_signature(self) -> Dict[str, int]
    def eabc_vector(self) -> np.ndarray  # [n_E, n_A, n_B, n_C]
    
    # Collatz-Gewicht
    def collatz_weight(self) -> float
    def is_expansive(self) -> bool
    def is_contractive(self) -> bool
    
    # Vergleiche
    def is_smooth(self, B: int) -> bool  # Alle Primfaktoren ≤ B
    def has_e_decomposition(self) -> bool
    
    # Ausgabe
    def multiplicative_expression(self) -> str
    def additive_expression(self) -> Optional[str]
    def __repr__(self) -> str
```

---

## 3. Modul: `catalan_analysis.py`

### Statistik-Funktionen

#### `analyze_catalan_distribution(N_max, strategy='balanced')`

Analysiert die Verteilung von catalanischen Eigenschaften für n ∈ [2, N_max].

**Output:**

```python
{
    'depths': List[int],                       # Baumtiefen
    'sizes': List[int],                        # Baumgrößen
    'eabc_signatures': List[Dict[str, int]],   # EABC-Histogramme
    'collatz_weights': List[float],            # Collatz-Gewichte
    'e_decomposable': List[bool],              # Hat T_add?
}
```

#### `compute_tree_invariants(tree: CatalanTree)`

Berechnet strukturelle Invarianten eines Baums.

**Output:**

```python
{
    'depth': int,
    'size': int,
    'leaf_count': int,
    'balance_factor': float,     # Wie balanciert ist der Baum?
    'left_heavy': bool,          # Ist der Baum linkslastig?
    'right_heavy': bool,         # Ist der Baum rechtslastig?
    'path_lengths': List[int],   # Pfadlängen von Wurzel zu Blättern
    'mean_path_length': float,
    'std_path_length': float,
}
```

#### `correlation_analysis(N_max)`

Berechnet Korrelationen zwischen Baum-Eigenschaften und arithmetischen Funktionen.

**Korrelationen:**

- `depth(N)` vs. `Ω(N)` (Anzahl Primfaktoren mit Multiplizität)
- `depth(N)` vs. `τ(N)` (Anzahl Teiler)
- `depth(N)` vs. `collatz_stoptime(N)` (falls implementiert)
- `W(N)` vs. `σ(N)` (Summe der Teiler)
- `eabc_signature(N)` vs. `spectral_properties(N)` (falls Hamiltonian gebaut)

**Output:** Korrelationsmatrix + p-Werte

---

## 4. Modul: `catalan_visualization.py`

### Visualisierungsfunktionen

#### `plot_tree(tree: CatalanTree, filename='tree.png')`

Erstellt eine Visualisierung des Baums mit graphviz.

**Features:**
- Farbcodierung nach EABC-Label
- Markierung von Operationen (×, +)
- Anzeige von Werten an Knoten

#### `plot_catalan_statistics(N_max, filename='catalan_stats.png')`

Erstellt einen 2×2-Plot mit:

1. **Baumtiefe vs. n**
2. **EABC-Signatur-Heatmap** (Anzahl E,A,B,C-Blätter)
3. **Collatz-Gewicht-Verteilung**
4. **Korrelation: Tiefe vs. Gewicht**

#### `plot_eabc_histogram(N_max, filename='eabc_hist.png')`

Histogramm der EABC-Blattverteilungen.

---

## 5. Integration mit bestehendem Code

### 5.1 Integration mit `collatz_weights.py`

Die Collatz-Gewichte werden direkt aus den Blättern von T_mult berechnet:

```python
from src.collatz_weights import collatz_log_rate

def collatz_weight(tree: CatalanTree) -> float:
    """Berechnet W(N) = Σ λ_σ(p) für alle Blätter p."""
    return sum(collatz_log_rate(p) for p in tree.leaf_values())
```

### 5.2 Integration mit `hamiltonian.py`

Mögliche Erweiterung: Konstruiere den Hamiltonian direkt aus der catalanischen Normalform.

```python
class CatalanEABCHamiltonian(EABCHamiltonian):
    def __init__(self, N, cnf: CatalanNormalForm, alpha=1.0, beta=0.5, gamma=1.5):
        super().__init__(N, alpha, beta, gamma)
        self.cnf = cnf
        
        # Ersetze H_p durch baumbasierte Gewichte
        self._build_tree_based_defect()
    
    def _build_tree_based_defect(self):
        """Konstruiert H_p aus T_mult-Blattgewichten."""
        # Verwende cnf.collatz_weight() für jeden Primfaktor
        pass
```

### 5.3 Integration mit `spectral.py`

Analysiere, ob Bauminvarianten mit spektralen Eigenschaften korrelieren:

```python
def analyze_tree_spectrum_correlation(N_max):
    results = []
    for n in range(2, N_max + 1):
        cnf = CatalanNormalForm(n)
        H = CatalanEABCHamiltonian(n, cnf)
        
        # Spektrum berechnen
        spectrum = H.compute_spectrum(k=100)
        spacings = compute_spacings(spectrum)
        sigma = np.std(spacings)
        
        results.append({
            'n': n,
            'depth': cnf.multiplicative_depth(),
            'weight': cnf.collatz_weight(),
            'sigma': sigma,
        })
    
    return pd.DataFrame(results)
```

---

## 6. Testing-Strategie

### Unit-Tests

#### `tests/test_catalan_tree.py`

```python
def test_leaf_operations():
    tree = CatalanTree(5, label='A')
    assert tree.is_leaf()
    assert tree.depth() == 0
    assert tree.leaf_labels() == ['A']

def test_multiplicative_tree():
    tree = build_multiplicative_tree(30)  # 30 = 2 × 3 × 5
    assert tree.value == 30
    assert tree.depth() == 2
    assert set(tree.leaf_values()) == {2, 3, 5}
    
def test_collatz_weight():
    tree = build_multiplicative_tree(30)
    W = tree.collatz_weight()
    # W = λ_⊥ + λ_⊥ + λ_A ≈ 0 + 0 + (-0.143)
    assert abs(W - (-0.143)) < 0.01
```

#### `tests/test_catalan_normalform.py`

```python
def test_normalform_construction():
    cnf = CatalanNormalForm(30)
    assert cnf.n == 30
    assert cnf.T_mult is not None
    # T_add könnte None sein (keine E-Zerlegung)
    
def test_eabc_signature():
    cnf = CatalanNormalForm(2310)  # 2×3×5×7×11
    sig = cnf.eabc_signature()
    # Erwartung: {'⊥': 2, 'A': 1, 'B': 1, 'C': 1}
    assert sig['A'] == 1
    assert sig['B'] == 1
    assert sig['C'] == 1
```

### Integration-Tests

#### `test_catalan_integration.py`

```python
def test_large_scale_analysis():
    """Test für N_max = 10.000 (Performance-Test)."""
    results = analyze_catalan_distribution(10000)
    assert len(results['depths']) == 9999  # n ∈ [2, 10000]
    
def test_correlation_with_collatz():
    """Test der Korrelation zwischen W(N) und Stopzeit."""
    # Benötigt Implementation von collatz_stoptime
    pass
```

---

## 7. Performance-Überlegungen

### Bottlenecks

1. **Primfaktorzerlegung:** O(√n) für naive Implementation
   - **Lösung:** Verwende `sympy.factorint()` oder vorberechnete Faktoren
   
2. **E-Partition-Suche:** NP-hart (Subset-Sum)
   - **Lösung:** Dynamische Programmierung, aber T_add oft leer lassen
   
3. **Baumkonstruktion:** O(k log k) für k Primfaktoren
   - **Lösung:** Effizient, kein Problem

### Skalierung

Für N_max = 10^6:
- ~10^6 Zahlen
- Durchschnittlich Ω(n) ≈ log log n ≈ 3-4 Primfaktoren
- **Geschätzte Laufzeit:** 1-10 Minuten (Python)

**Optimierungen:**
- Parallelisierung mit `multiprocessing`
- Caching von Primfaktorzerlegungen
- Optional: C++/Cython für kritische Loops

---

## 8. Roadmap für Implementation

### Phase 1: Grundstruktur (1-2 Wochen)

- [ ] Implementiere `CatalanTree`-Klasse
- [ ] Implementiere `build_multiplicative_tree`
- [ ] Grundlegende Tests

### Phase 2: Normalform (1 Woche)

- [ ] Implementiere `CatalanNormalForm`
- [ ] Integration mit `collatz_weights.py`
- [ ] Tests für kleine N (N ≤ 1000)

### Phase 3: Additive Zerlegung (2-3 Wochen)

- [ ] Implementiere `find_e_partition` (Subset-Sum)
- [ ] Implementiere `build_additive_tree`
- [ ] Performance-Tests

### Phase 4: Analyse & Statistik (2 Wochen)

- [ ] Implementiere `analyze_catalan_distribution`
- [ ] Implementiere `correlation_analysis`
- [ ] Plots für N_max = 10^4

### Phase 5: Visualisierung (1 Woche)

- [ ] Implementiere `plot_tree` (graphviz)
- [ ] Implementiere `plot_catalan_statistics`
- [ ] Beispiel-Notebooks

### Phase 6: Integration (1-2 Wochen)

- [ ] Integration mit `hamiltonian.py`
- [ ] Spektral-Korrelations-Analyse
- [ ] Dokumentation

**Gesamtdauer:** ~8-12 Wochen

---

## 9. Offene technische Fragen

### 9.1 Klammerungsstrategie

**Frage:** Welche Strategie ist die "natürliche"?

Optionen:
- **Balanciert:** Minimale Tiefe, aber nicht eindeutig
- **Links:** Eindeutig, aber asymmetrisch
- **Sortiert:** Nach Primzahlgröße aufsteigend/absteigend

**Test:** Vergleiche Korrelationen mit arithmetischen Eigenschaften.

### 9.2 E-Zerlegung

**Frage:** Ist T_add praktisch nutzbar?

Problem: Viele Zahlen haben keine E-Zerlegung (E-Primzahlen sind selten).

**Alternativen:**
- Verallgemeinere auf "Summanden aus {E,A,B,C}"
- Verwende nur T_mult (praktischer)

### 9.3 Speichereffizienz

**Frage:** Wie speichern wir Bäume für große N_max?

Problem: 10^6 Bäume mit durchschnittlich 10 Knoten → 10^7 Knoten.

**Lösung:** On-the-fly-Berechnung statt Speicherung, oder komprimierte Darstellung.

---

## 10. Zusammenfassung

Diese Roadmap bietet eine strukturierte Planung für die zukünftige Implementation der catalanischen EABC-Normalform. Die Struktur ist modular und integriert sich natürlich in das bestehende `eabc-qubit`-Framework.

**Nächster Schritt:** Entscheidung über Phase 1 (Grundstruktur) und Beginn der Implementation von `catalan_tree.py`.

---

**Hinweis:** Diese Roadmap ist ein Planungsdokument und keine Verpflichtung. Die tatsächliche Implementation kann abweichen, basierend auf empirischen Erkenntnissen und technischen Herausforderungen.

**Status:** Planung  
**Ziel:** Grundlage für zukünftige Implementation  
**Priorität:** Niedrig (konzeptionell wichtig, aber kein unmittelbarer Bedarf)

---

**Thomas Hoffbauer, 2026**
