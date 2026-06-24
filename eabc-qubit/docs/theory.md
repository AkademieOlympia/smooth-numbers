# Theoretische Grundlagen des EABC-Qubit-Frameworks

## 1. Das physikalische Modell

### 1.1 Hilbertraum-Struktur

Das EABC-Qubit-System operiert auf einem zusammengesetzten Hilbertraum:

```
ℋ = ℋ_Zahl ⊗ ℋ_EABC
```

- **ℋ_Zahl**: Eindimensionale Tight-Binding-Kette mit N Gitterplätzen  
  Basiszustände: {|1⟩, |2⟩, ..., |N⟩}

- **ℋ_EABC**: Interner Z₄-Freiheitsgrad (Chiralität)  
  Basiszustände: {|E⟩, |A⟩, |B⟩, |C⟩}

Gesamtdimension: **dim(ℋ) = 4N**

Ein allgemeiner Zustand hat die Form:

```
|ψ⟩ = Σ_{n=1}^N Σ_{σ∈{E,A,B,C}} c_{n,σ} |n⟩ ⊗ |σ⟩
```

### 1.2 Hamiltonian

```
H = α H_T + β H_χ + γ H_p
```

#### Kinetischer Term (Tight-Binding)

```
H_T = -Σ_{n=1}^{N-1} (|n⟩⟨n+1| + |n+1⟩⟨n|) ⊗ 𝟙_EABC
```

Matrix-Darstellung (als Kronecker-Produkt):

```
H_T = T ⊗ 𝟙₄
```

mit

```
T = ⎡ 0  1  0  0  ... ⎤
    ⎢ 1  0  1  0  ... ⎥
    ⎢ 0  1  0  1  ... ⎥
    ⎢ ...            ⎥
    ⎣ ...          0 ⎦
```

**Interpretation**: Ein Teilchen kann zwischen benachbarten Gitterplätzen hüpfen (Hopping-Amplitude α).

#### Chiraler Term

```
H_χ = 𝟙_Zahl ⊗ (χ + χ†)
```

mit der zyklischen Permutation:

```
χ = |E⟩⟨C| + |A⟩⟨E| + |B⟩⟨A| + |C⟩⟨B|
```

Matrix-Form:

```
χ = ⎡ 0  0  0  1 ⎤       χ + χ† = ⎡ 0  1  0  1 ⎤
    ⎢ 1  0  0  0 ⎥               ⎢ 1  0  1  0 ⎥
    ⎢ 0  1  0  0 ⎥               ⎢ 0  1  0  1 ⎥
    ⎣ 0  0  1  0 ⎦               ⎣ 1  0  1  0 ⎦
```

**Interpretation**: Der chirale Freiheitsgrad rotiert durch den Zyklus E → A → B → C → E mit Amplitude β.

#### Primzahl-Defekt

```
H_p = Σ_{p∈Primes, p≤N} |p⟩⟨p| ⊗ |σ(p)⟩⟨σ(p)|
```

wobei σ(p) die EABC-Klassifikation der Primzahl p ist:

```
σ(p) = E   falls p ≡ 1  (mod 12)
σ(p) = A   falls p ≡ 5  (mod 12)
σ(p) = B   falls p ≡ 7  (mod 12)
σ(p) = C   falls p ≡ 11 (mod 12)
```

**Interpretation**: An jeder Primzahlposition p gibt es ein lokalisiertes Potential, das nur an den entsprechenden chiralen Zustand σ(p) koppelt.

## 2. Physikalische Analogien

### 2.1 Festkörperphysik

Das EABC-Modell ist verwandt mit:

**a) Anderson-Lokalisierung**  
Primzahlen = zufällige magnetische Verunreinigungen in einem Kristall

**b) Tight-Binding-Modelle**  
Standard-Modell für Elektronen in Festkörpern

**c) Spin-Bahn-Kopplung**  
Der chirale Term mischt interne Freiheitsgrade (analog zu Spin)

**d) Topologische Isolatoren**  
Z₄-Symmetrie könnte topologische Invarianten ermöglichen

### 2.2 Quantenchaos und Random Matrix Theory

Das System kann zwei extreme Grenzen zeigen:

**Integrable Systeme** (γ = 0, keine Primzahlen)
- Translationssymmetrie
- Bloch-Wellen als exakte Eigenzustände
- Poisson-Statistik: P(s) = exp(-s)

**Quantenchaos** (γ ≠ 0, Primzahl-Defekte aktiv)
- Gebrochene Translationssymmetrie
- Mögliche Level-Repulsion
- Wigner-Dyson-Statistik: P(s) ∼ s^β exp(-const · s²)

## 3. Spektralstatistik

### 3.1 Level Spacing Distribution

Die zentrale Größe zur Charakterisierung des Systems ist die **Nearest-Neighbor Level Spacing Distribution**:

```
P(s) = Wahrscheinlichkeit, dass zwei benachbarte Eigenwerte den Abstand s haben
```

Nach spektralem Unfolding (Normalisierung auf mittlere Dichte ρ̄ = 1) gilt:

```
s_n = ε_{n+1} - ε_n
```

### 3.2 Theoretische Vorhersagen

**Poisson-Verteilung** (integrable Systeme)

```
P(s) = exp(-s)
⟨s⟩ = 1
P(s=0) = 1  → Keine Level-Repulsion
```

**Wigner-Dyson (GOE - Gaussian Orthogonal Ensemble)**

```
P(s) = (π/2) s exp(-πs²/4)
⟨s⟩ = 1
P(s→0) → 0  → Lineare Repulsion
```

GOE gilt für reelle symmetrische Matrizen (Zeitumkehr-invariant, kein Spin).

**Wigner-Dyson (GUE - Gaussian Unitary Ensemble)**

```
P(s) = (32/π²) s² exp(-4s²/π)
⟨s⟩ = 1
P(s→0) → 0  → Quadratische Repulsion
```

GUE gilt für komplexe hermitische Matrizen (gebrochene Zeitumkehr-Symmetrie).

**Verbindung zu Riemannschen Nullstellen**

Montgomery (1973) zeigte, dass die Paarkorrelation der Riemannschen ζ-Nullstellen **exakt GUE-Statistik** folgt. Falls das EABC-System ebenfalls GUE zeigt, wäre dies ein möglicher Hinweis auf eine tiefe Verbindung zwischen:

```
Primzahlen ↔ Spektrum von H_EABC ↔ Riemannsche Nullstellen
```

## 4. Numerische Methoden

### 4.1 Sparse Matrix Konstruktion

Für N = 10.000 ist die Hamiltonian-Matrix 40.000 × 40.000. **Aber**: Sie ist extrem dünnbesetzt.

**Anzahl Nicht-Null-Einträge pro Zeile**:
- 2 vom Hopping (T)
- 2 vom chiralen Term (χ + χ†)
- ≤ 1 vom Primzahl-Defekt

→ Maximal **6 Einträge pro Zeile** (bei 40.000 Zeilen)  
→ Speicherbedarf: **O(N)** statt O(N²)

**Format**: Compressed Sparse Row (CSR) in scipy.sparse

### 4.2 Partielle Diagonalisierung

Wir nutzen den **Lanczos-Algorithmus** (`scipy.sparse.linalg.eigsh`):

- Berechnet nur k << 4N Eigenwerte
- Komplexität: O(k · nnz(H)) ≈ O(k · N)
- Typisch: k = 500-2000 für Statistik

**Shift-Invert-Modus** für mittlere Eigenwerte:
```python
eigsh(H, k=500, sigma=0.0)  # Eigenwerte nahe E=0
```

### 4.3 Spektrales Unfolding

Ziel: Transformiere das Spektrum so, dass die mittlere Dichte konstant (= 1) ist.

**Methode**: Fitte die kumulative Zustandsdichte N(E) mit einem Polynom:

```
N(E) = Anzahl der Eigenwerte ≤ E
```

Dann definiere das entfaltete Spektrum:

```
ε_n = N_smooth(E_n)
```

Dies entfernt glatte Trends in der Zustandsdichte.

## 5. Erwartete Szenarien

### Szenario A: Poisson-Statistik

**Falls χ²_Poisson << χ²_GOE, χ²_GUE**:

→ Die Primzahlen wirken wie **unkorrelierte zufällige Störungen**  
→ Das EABC-Modell besitzt **keine kohärente Quantenstruktur**  
→ Die chirale Modulation ist physikalisch irrelevant

**Interpretation**: Die Primzahlen verhalten sich wie ein statistisches Rauschen auf dem Gitter.

### Szenario B: Wigner-Dyson (GOE/GUE)

**Falls χ²_GUE << χ²_Poisson** oder **χ²_GOE << χ²_Poisson**:

→ Starke **Level-Repulsion** → Korrelationen im Spektrum  
→ Die Primzahlen bilden eine **kohärente Quantenstruktur**  
→ Mögliche Verbindung zu **Riemannschen Nullstellen** (Montgomery, Berry-Keating)

**Interpretation**: Das EABC-Modell zeigt Quantenchaos. Die Primzahl-Defekte sind **nicht zufällig**, sondern erzeugen globale spektrale Korrelationen.

Falls speziell **GUE**: Dies wäre besonders bemerkenswert, da GUE mit gebrochener Zeitumkehr-Symmetrie assoziiert ist (wie bei Riemannschen Nullstellen).

### Szenario C: Intermediär (Brody-Distribution)

**Falls Brody-Parameter 0 < q < 1**:

→ **Crossover-Regime** zwischen Poisson und Wigner-Dyson  
→ Abhängig von γ/α (Defekt-Stärke vs. Hopping)  
→ Möglicher **Metal-Insulator-Übergang**

**Interpretation**: Das System zeigt partielles Chaos. Die Primzahlen induzieren Korrelationen, aber nicht stark genug für vollständiges Quantenchaos.

## 6. Testbare Vorhersagen

### Test 1: Variation von γ (Defekt-Stärke)

```
γ → 0:  Sollte Poisson zeigen (keine Defekte)
γ → ∞:  Starke Lokalisierung → Poisson oder Zwischenregime
γ ≈ α:  Kritischer Bereich → mögliches Wigner-Dyson
```

### Test 2: Vergleich mit H₀ (ohne Primzahlen)

```
H₀ = α H_T + β H_χ  (γ = 0)
```

H₀ ist translationssymmetrisch → exakt diagonalisierbar → Poisson-Statistik

Falls H (mit Primzahlen) **nicht** Poisson zeigt → Die Primzahlen sind entscheidend!

### Test 3: Größenskalierung

```
N = 1.000   → Level Statistics
N = 5.000   → Level Statistics
N = 10.000  → Level Statistics
```

Falls Wigner-Dyson: Sollte mit N **stabiler** werden (universell)  
Falls Poisson bleibt: Artefakte oder vorasymptotisches Regime

## 7. Referenzen

**Quantenchaos und RMT:**
- Haake (2010): "Quantum Signatures of Chaos"
- Mehta (2004): "Random Matrices"
- Bohigas, Giannoni, Schmit (1984): "Characterization of Chaotic Quantum Spectra"

**Primzahlen und Quantenmechanik:**
- Montgomery (1973): Pair Correlation Conjecture
- Berry, Keating (1999): "The Riemann Zeros and Eigenvalue Asymptotics"
- Connes (1999): "Trace Formula in Noncommutative Geometry"

**Anderson-Lokalisierung:**
- Anderson (1958): "Absence of Diffusion in Certain Random Lattices"
- Evers, Mirlin (2008): "Anderson Transitions"
