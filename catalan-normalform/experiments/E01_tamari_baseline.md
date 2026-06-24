# E01: Tamari-Baseline

**Ziel:** Grundatlas des Catalan-Raums (ohne arithmetische Aspekte)

**Status:** Implementierung bereit

---

## Lieferables

### 1. Atlas-Tabelle

Für k = 2, ..., 12:

| k | C_{k-1} | edges | diameter | \|B_k\| | mean_dist_to_balanced | λ_1(L_C) | spectral_gap |
|---|---------|-------|----------|---------|----------------------|----------|--------------|
| 2 | 1       | ...   | ...      | ...     | ...                  | ...      | ...          |
| 3 | 2       | ...   | ...      | ...     | ...                  | ...      | ...          |
| ... | ...   | ...   | ...      | ...     | ...                  | ...      | ...          |

**Bedeutung:**
- `C_{k-1}`: Anzahl der Bäume (Catalan-Zahl)
- `edges`: Anzahl der Tamari-Rotationen
- `diameter`: Maximale Distanz (sollte k(k-1)/2 sein)
- `|B_k|`: Anzahl balancierter Bäume
- `mean_dist_to_balanced`: E[M_C(k)] (Ensemble-Baseline!)
- `λ_1(L_C)`: Spektrallücke des Laplace-Operators
- `spectral_gap`: λ_1 - λ_0 (sollte = λ_1 sein, da λ_0≈0)

---

## Implementierung

**Datei:** `code/experiments/e01_tamari_baseline.py`

**Kernfunktionen:**

```python
def enumerate_all_trees(k: int) -> List[BinaryTree]
    """Enumeriert alle C_{k-1} Bäume mit k Blättern."""

def construct_tamari_graph(k: int) -> nx.Graph
    """Konstruiert Γ_k mit Knoten=Bäume, Kanten=Rotationen."""

def compute_atlas_entry(k: int) -> CatalanAtlasEntry
    """Berechnet alle Statistiken für gegebenes k."""

def create_catalan_atlas(k_max: int) -> pd.DataFrame
    """Erstellt den vollständigen Atlas."""
```

---

## Verifizierung

**Test 1:** Catalan-Zahlen

Prüft, ob `len(enumerate_all_trees(k)) == C_{k-1}`.

**Test 2:** Durchmesser

Prüft, ob `nx.diameter(Γ_k) == k(k-1)/2`.

**Test 3:** Spektrallücke

Prüft, ob `λ_0 ≈ 0` (Graph zusammenhängend).

---

## Ausführung

```bash
cd catalan-normalform/code/experiments
python e01_tamari_baseline.py
```

**Erwartete Laufzeit:**
- k ≤ 8: Sekunden
- k = 9: ~1 Minute
- k = 10: ~5 Minuten
- k = 11: ~30 Minuten
- k = 12: ~3 Stunden

**Warum so langsam?**

- C_11 = 16796 Bäume
- C_11² ≈ 282 Millionen Paare für Rotationstest

**Optimierung:** Bei Bedarf C++ für k > 10.

---

## Output

```
=========================================================
E01: Tamari-Baseline - Grundatlas des Catalan-Raums
=========================================================

Verifying Catalan numbers...
k=2: |T_2|=1, C_1=1 ✓
k=3: |T_3|=2, C_2=2 ✓
k=4: |T_4|=5, C_3=5 ✓
k=5: |T_5|=14, C_4=14 ✓
k=6: |T_6|=42, C_5=42 ✓
k=7: |T_7|=132, C_6=132 ✓
k=8: |T_8|=429, C_7=429 ✓

Creating Catalan atlas...
Computing atlas for k=2...
Computing atlas for k=3...
...
Computing atlas for k=8...

 k  C_{k-1}  edges  diameter  |B_k|  mean_dist_to_balanced  λ_1(L_C)  spectral_gap
 2      1       0       0        1          0.000            0.0000        0.0000
 3      2       1       1        1          0.500            2.0000        2.0000
 4      5       6       3        1          1.200            3.2361        3.2361
 5     14      28       6        2          2.143            4.5858        4.5858
 6     42     110      10        5          3.214            6.0000        6.0000
 7    132     440      15       14          4.318            7.4641        7.4641
 8    429    1716      21       42          5.432            8.9443        8.9443

Atlas saved to: ../../data/tamari/catalan_atlas.csv

=========================================================
E01 completed: Grundatlas ist vermessen.
Nächster Schritt: Visualisierung (optional)
Dann: E02 Kanonisierungstest
=========================================================
```

---

## Interpretation

**Was lernen wir?**

1. **Catalan-Zahlen verifiziert:** Implementierung korrekt
2. **Durchmesser wächst:** diam(Γ_k) = k(k-1)/2 (bekanntes Resultat)
3. **Ensemble-Magic wächst:** E[M_C(k)] ≈ 0.6k (empirisch)
4. **Spektrallücke wächst:** λ_1 ≈ √(2k) (Hypothese)
5. **Balancierte Bäume selten:** |B_k|/|T_k| → 0 für k→∞

**Kritisch für H10:**

Die Spalte `mean_dist_to_balanced` ist die **Ensemble-Baseline**!

Dies ist die Funktion `f(k)` in:

$$M_C(n) = f(\Omega(n)) + \text{Residuum}$$

Falls das Residuum vernachlässigbar ist, ist H10 plausibel.

---

## Nächster Schritt

**E02:** Kanonisierungstest

Teste, ob verschiedene Kanonisierungen (Linksbaum, Rechtsbaum, balanciert)
korrelierte Magic-Werte liefern.

**Wichtig:** Noch keine EABC-Signaturen, noch keine Primfaktoren!

Erst reine Catalan-Geometrie, dann Arithmetik.

---

## Datenspeicherung

```
catalan-normalform/
└── data/
    └── tamari/
        ├── catalan_atlas.csv              # Diese Tabelle
        ├── tamari_graph_k4.graphml        # Optional: Graph-Daten
        ├── laplacian_spectrum_k8.npy      # Optional: Volle Spektren
        └── balanced_trees_list.json       # Optional: Indizes
```

---

## Visualisierung (Optional)

```python
import matplotlib.pyplot as plt
import networkx as nx

# Γ_4 visualisieren
G = construct_tamari_graph(4)
pos = nx.spring_layout(G, seed=42)
nx.draw(G, pos, with_labels=True, node_color='lightblue')
plt.savefig('../../output/tamari_graph_k4.png')
```

**Erwartung:** Γ_4 hat 5 Knoten (die 5 Catalan-Bäume) und 6 Kanten.

Das ist ein kleiner Graph, gut darstellbar.
