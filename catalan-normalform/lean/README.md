# Lean-Formalisierung: Catalan-Normalform

**Kombinatorische Grundstruktur der Spektralen Catalan-Geometrie**

---

## Philosophie

```
┌─────────────────────────────────────────────────────┐
│  Lean formalisiert die kombinatorische Architektur  │
│  Python testet die empirischen Hypothesen           │
└─────────────────────────────────────────────────────┘
```

Lean ist **nicht** für numerische Spektralanalyse gedacht, sondern für:

1. **Präzise Typdefinitionen** (CTree k)
2. **Strukturelle Beweise** (Rotation, Grapheigenschaften)
3. **Formale Hypothesen** (H10 als Prop)
4. **Objektstatus** (Was ist beweisbar, was ist axiomatisch)

---

## Projektstruktur

```
lean/
├── lakefile.lean                  # Lake-Konfiguration
├── CatalanNormalform.lean         # Hauptmodul
└── CatalanNormalform/
    ├── CTree.lean                 # Stufe 1: Binäre Bäume
    ├── Rotation.lean              # Stufe 2: Tamari-Rotation
    ├── TamariGraph.lean           # Stufe 3: SimpleGraph-Instanz
    ├── Magic.lean                 # Stufe 4: Observablen
    ├── Arithmetic.lean            # Stufe 5: Primfaktoren, EABC
    ├── ShellVectorNorm.lean       # Stufe 5b: SVN-Architektur
    ├── GaussEisenstein.lean       # Stufe 5c: Gauß-Eisenstein-Interpretation
    └── Hypotheses.lean            # Stufe 6: H10 Null-Modell
```

---

## Stufe 1: Binäre Bäume (`CTree.lean`)

```lean
inductive CTree : Nat → Type where
  | leaf : CTree 1
  | node : CTree m → CTree n → CTree (m + n)
```

**Was ist formalisiert:**

- ✅ Abhängiger Typ: Anzahl der Blätter im Typ kodiert
- ✅ Höhe, interne Knoten, strukturelle Funktionen
- ✅ Linksbaum, Rechtsbaum, balancierte Bäume
- ✅ Theorem: `internal_nodes = k - 1`
- ✅ Theorem: `height ≤ k - 1`
- ✅ DecidableEq-Instanz

**Beispiele:**

```lean
def four_balanced : CTree 4 := node (node leaf leaf) (node leaf leaf)
def four_left : CTree 4 := node (node (node leaf leaf) leaf) leaf
```

---

## Stufe 2: Tamari-Rotation (`Rotation.lean`)

```lean
inductive TamariStepRight : CTree k → CTree k → Prop where
  | assoc : TamariStepRight (node (node A B) C) (node A (node B C))
```

**Was ist formalisiert:**

- ✅ Gerichtete Rotationen (links/rechts)
- ✅ Ungerichtete Adjazenz `TamariAdj`
- ✅ Symmetrie der Adjazenz
- ✅ Irreflexivität (mit sorry)
- ✅ Tamari-Pfade (als induktiver Typ)
- ✅ Distanz-Definition (noncomputable)
- ✅ Durchmesser: `k(k-1)/2`

**Axiome:**

- Konnektivität des Tamari-Graphen (Sleator-Tarjan-Thurston)
- Distanz Linksbaum ↔ Rechtsbaum = Durchmesser

---

## Stufe 3: Tamari-Graph (`TamariGraph.lean`)

```lean
def TamariGraph (k : Nat) : SimpleGraph (CTree k) where
  Adj := TamariAdj
  symm := tamariAdj_symm
  loopless := tamariAdj_irrefl
```

**Was ist formalisiert:**

- ✅ SimpleGraph-Instanz für Mathlib
- ✅ Nachbarschaftsdefinitionen (Scaffold)
- ✅ Grad, Zusammenhang (axiomatisch)
- ✅ Laplace-Operator L = D - A (formal, nicht numerisch)
- ✅ Spektrale Eigenschaften (Axiome)

**Wichtig:** Numerische Eigenwerte bleiben in Python!

---

## Stufe 4: Catalan-Magic (`Magic.lean`)

```lean
noncomputable def catalan_magic (t : CTree k) : Nat :=
  Nat.find (...)  -- Minimale Distanz zu balancierten Bäumen
```

**Was ist formalisiert:**

- ✅ Definition der balancierten Bäume
- ✅ Catalan-Magic als minimale Distanz
- ✅ Ensemble-Magic (Mittelung über alle Bäume)
- ✅ Residuale Magic (Abweichung vom Mittelwert)
- ✅ Normierte Magic ∈ [0,1]
- ✅ Theoreme: balanciert ⇒ Magic=0, Linksbaum hat hohe Magic

**Catalan-Zahl:**

- Axiom: `Fintype.card (CTree k) = C_{k-1}`

---

## Stufe 5: Arithmetik (`Arithmetic.lean`)

```lean
structure CatalanNormalform (n : Nat) where
  value : Nat
  omega : Nat
  signature : List EABC
  tree : CTree omega
  magic : ℚ
  residual : ℚ
```

**Was ist formalisiert:**

- ✅ `omega(n)`: Anzahl Primfaktoren mit Vielfachheit
- ✅ EABC-Klassifikation (E, A, B, C für p mod 12)
- ✅ EABC-Signatur einer Zahl
- ✅ Vollständige Normalform-Struktur
- ✅ Kanonisierungen (left, right, balanced)

---

## Stufe 5b: Schale-Vektor-Norm (`ShellVectorNorm.lean`)

```lean
structure FactorEABCVector where
  e : Nat  -- Anzahl Faktoren in E (p ≡ 1 mod 12)
  a : Nat  -- Anzahl Faktoren in A (p ≡ 5 mod 12)
  b : Nat  -- Anzahl Faktoren in B (p ≡ 7 mod 12)
  c : Nat  -- Anzahl Faktoren in C (p ≡ 11 mod 12)
```

**Was ist formalisiert:**

- ✅ Schalenhöhe σ(n) = v₂ + v₃
- ✅ Reduzierter Kern m(n) (ohne 2- und 3-Faktoren)
- ✅ Faktor-EABC-Vektor V_fac(n)
- ✅ Vektornorm ||V||² = e² + a² + b² + c²
- ✅ SVN-Koordinatensystem (Omega, Schale, Vektor, Norm)
- ✅ H0.5–H0.7 Hypothesen (Schalen-, Faser-, Norm-Kopplung)

---

## Stufe 5c: Gauß-Eisenstein-Interpretation (`GaussEisenstein.lean`)

```lean
inductive SplittingBehavior where
  | Split : SplittingBehavior    -- p spaltet
  | Inert : SplittingBehavior    -- p bleibt prim
  | Ramified : SplittingBehavior -- p ramifiziert
```

**Was ist formalisiert:**

- ✅ **Modulare** Spaltungskriterien (p mod 4, p mod 3)
- ✅ `gaussSplitting`: p mod 4 → Split (1) oder Inert (3)
- ✅ `eisensteinSplitting`: p mod 3 → Split (1) oder Inert (2)
- ✅ `SplittingPair`: Kombiniertes modulares Verhalten
- ✅ `eabcFromSplittingPair`: EABC ↔ (mod 4, mod 3) Paare
- ✅ Die vier zentralen Äquivalenzen (E, A, B, C ↔ Spaltungspaare)
- ✅ Alternative Definition von `factorEABCVector` über modulare Kriterien
- ✅ Konzentrationsverhältnis H(n) = ||v||² / Ω²
- ✅ Interpretation: e = (S,S), a = (S,I), b = (I,S), c = (I,I)

**Methodische Klarstellung:**

Diese Formalisierung behandelt nur die **modularen Spaltungskriterien** auf
ℚ-Ebene (p mod 4, p mod 3), **nicht** die volle Idealtheorie von ℤ[i] oder
ℤ[ω]. Die klassischen Kriterien sind ausreichend, um die EABC-Verfeinerung
zu verstehen.

**Mathematische Fundierung:**

Dies basiert auf **klassischen Spaltungskriterien** der algebraischen Zahlentheorie
und erklärt, warum 12 = 4 · 3 die natürliche Modulo-Basis für EABC ist:

| EABC | mod 12 | Gauß (mod 4) | Eisenstein (mod 3) |
|------|--------|--------------|---------------------|
| E    | 1      | Spaltet (1)  | Spaltet (1)         |
| A    | 5      | Spaltet (1)  | Inert (2)           |
| B    | 7      | Inert (3)    | Spaltet (1)         |
| C    | 11     | Inert (3)    | Inert (2)           |

Falls H0.7 (Norm-Kopplung) bestätigt wird, bedeutet dies:

> **Catalan-Strukturen sind sensitiv auf modulare Spaltungs-Konzentration.**

Die Formalisierung nutzt ausschließlich die klassischen modularen Kriterien
(p mod 4, p mod 3), ohne die volle Idealtheorie zu benötigen.

---

## Stufe 6: Hypothesen (`Hypotheses.lean`)

```lean
def H10_NullModel (canon : Canonization) : Prop :=
  ∃ f : Nat → ℚ, ∀ n ≥ 2, catalan_magic(n) = f(omega(n))
```

**Was ist formalisiert:**

- ✅ H10 als formales Prädikat
- ✅ Schwache und starke Versionen
- ✅ `GoNoGoCriterion`: Entscheidungsstruktur
- ✅ `should_continue`: Formale Abbruchkriterien
- ✅ Dokumentation der Konsequenzen

**Go/No-Go-Regel:**

```lean
def should_continue (criterion : GoNoGoCriterion) : Prop :=
  criterion.r_squared < 0.95 ∨
  criterion.variance_ratio > 0.05 ∨
  criterion.normality_pvalue < 0.05 ∨
  abs criterion.eabc_correlation > 0.15
```

Falls `should_continue = false`, ist H10 bestätigt → Projekt stoppen.

---

## Verwendete Mathlib-Module

```lean
import Mathlib.Combinatorics.Enumerative.Catalan
import Mathlib.Combinatorics.SimpleGraph.Basic
import Mathlib.Combinatorics.SimpleGraph.Acyclic
import Mathlib.Data.Nat.Prime.Basic
import Mathlib.Data.Nat.Factorization.Basic
import Mathlib.Data.Finset.Basic
import Mathlib.Algebra.BigOperators.Basic
import Mathlib.Data.Matrix.Basic
```

---

## Kompilieren

```bash
cd catalan-normalform/lean
lake build
```

Falls Mathlib noch nicht vorhanden:

```bash
lake update
lake build
```

---

## Was in Lean formalisiert ist

✅ **Kombinatorische Struktur:**
- Binäre Bäume mit k Blättern
- Tamari-Rotation
- Tamari-Graph als SimpleGraph
- Distanz, Durchmesser

✅ **Observablen:**
- Catalan-Magic
- Ensemble-Magic
- Residuale Magic

✅ **Arithmetik:**
- Primfaktorzerlegung
- EABC-Signatur
- Normalform-Struktur

✅ **Hypothesen:**
- H10 als formales Nullmodell
- Go/No-Go-Kriterium

---

## Was NICHT in Lean ist

❌ Numerische Spektralanalyse (Eigenwerte, IPR)  
❌ Statistische Tests (Korrelationen, p-Werte)  
❌ Große Experimente (10⁶ Zahlen)  
❌ Brody-Parameter, Collatz-Stopzeiten  
❌ Visualisierungen

→ Das gehört nach **Python/C++**!

---

## Nächste Schritte (Lean)

1. Vollständige Enumeration von `CTree k` für kleine k
2. Beweis von `tamariAdj_irrefl` (derzeit sorry)
3. Konstruktion aller Tamari-Kanten explizit
4. Berechnung von `tamari_dist` für kleine Beispiele
5. Integration mit `Mathlib.Combinatorics.Enumerative.Catalan`

---

## Nächste Schritte (Python)

Nach der Lean-Formalisierung sollte die **empirische Testphase** beginnen:

**Woche 1-2:** E01 Tamari-Baseline  
**Woche 3:** E02 Kanonisierungstest  
**Woche 4:** E03 Residualisierung + **H10-Test** (Go/No-Go!)  
**Woche 5-6:** E04 EABC-Information (falls H10 falsifiziert)  
**Woche 7-8:** E05 Spektralvergleich  

---

## Qualitätssicherung

**Lean garantiert:**

- Typsicherheit (keine falschen Blattanzahlen)
- Strukturelle Konsistenz (Rotationen sind wohldefiniert)
- Formale Klarheit (H10 ist präzise formuliert)

**Python liefert:**

- Numerische Werte (Eigenwerte, Korrelationen)
- Statistische Signifikanz (p-Werte)
- Große Ensembles (10⁶ Zahlen)

→ **Komplementäre Stärken**

---

## Literatur

- Mathlib4 Dokumentation: https://leanprover-community.github.io/mathlib4_docs/
- Loogle (Theorem-Suche): https://loogle.lean-lang.org/
- Tamari-Gitter: Huang & Tamari (1972)
- Catalan-Zahlen: Stanley (2015)
