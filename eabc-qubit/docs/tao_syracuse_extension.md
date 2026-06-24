# Tao-Syracuse-Erweiterung für EABC-Qubit

**Dynamische Syracuse-Trajektorien im Quantenrahmen**

---

## Übersicht

Die Tao-Syracuse-Erweiterung ersetzt die statischen Collatz-Gewichte durch **echte Syracuse-Trajektorien**, um die Collatz-Dynamik direkt im Quantensystem abzubilden.

### Motivation

Die ursprüngliche EABC-Qubit-Implementierung verwendet **statische Gewichte** log(r) für jede EABC-Klasse:
- **E** (n ≡ 1 mod 12): log(r) = -log(2) ≈ -0.693
- **A** (n ≡ 5 mod 12): log(r) = -log(2) + log(3)/2 ≈ -0.143
- **B** (n ≡ 7 mod 12): log(r) = +log(2) ≈ +0.693
- **C** (n ≡ 11 mod 12): log(r) = +log(3) - log(2) ≈ +0.405

Diese Gewichte sind **Mittelwerte** über die jeweilige EABC-Klasse. Die Syracuse-Erweiterung geht einen Schritt weiter und verwendet die **tatsächliche Dynamik** einer konkreten Syracuse-Trajektorie.

---

## Mathematischer Hintergrund

### Syracuse-Funktion

Die Syracuse-Funktion ist äquivalent zur Collatz-Abbildung, aber kompakter:

```
Syr(n) = (3n + 1) / 2^a
```

wobei **a = ν₂(3n+1)** die 2-adische Valuation ist (höchste Potenz von 2, die 3n+1 teilt).

#### Beispiele

- **n = 7**: 3·7+1 = 22 = 2·11 → ν₂(22) = 1 → Syr(7) = 11
- **n = 11**: 3·11+1 = 34 = 2·17 → ν₂(34) = 1 → Syr(11) = 17
- **n = 5**: 3·5+1 = 16 = 2⁴ → ν₂(16) = 4 → Syr(5) = 1

### Tao's Drift-Theorie (2019)

Terence Tao zeigte 2019 in seiner Arbeit ["Almost all Collatz orbits attain almost bounded values"](https://arxiv.org/abs/1909.03562):

> **Für typische ungerade Startwerte N₀ verhalten sich die 2-adischen Valuationen a_j wie unabhängige geometrisch verteilte Zufallsvariablen mit Parameter p = 1/2 (Geom(2)).**

#### Konsequenzen

1. **Erwartungswert der Valuation**: E[a_j] = 2

2. **Lokale Drift**:
   ```
   λ_j = log(3) - a_j·log(2)
   ```
   
   Mit E[a_j] = 2:
   ```
   E[λ_j] = log(3) - 2·log(2) = log(3/4) ≈ -0.288
   ```
   
   → **Negative Drift!** Dies ist Tao's zentrales Resultat für bedingte Konvergenz.

3. **Gesamtdrift**:
   ```
   Σ λ_j = Σ (log(3) - a_j·log(2)) → -∞  (mit hoher Wahrscheinlichkeit)
   ```

---

## Zeitabhängiger Hamiltonian

### Statisch (Collatz-EABC)

```
H^{static} = H_T + H_χ + γ Σ_p log(r(p)) |p⟩⟨p| ⊗ |σ(p)⟩⟨σ(p)|
```

- Summe über **Primzahlen** p
- Gewicht log(r(p)) hängt nur von der EABC-Klasse ab
- **Zeitunabhängig**

### Dynamisch (Tao-Syracuse)

```
H^{Tao}(N₀, t) = H_T + H_χ + γ Σ_{j=0}^t λ_j(N₀) |S_j(N₀)⟩⟨S_j(N₀)| ⊗ |σ(S_j)⟩⟨σ(S_j)|
```

wobei:
- **S_j(N₀)** = Syr^j(N₀) ist die j-te Iteration der Syracuse-Funktion
- **a_j** = ν₂(3·S_j + 1) ist die 2-adische Valuation im j-ten Schritt
- **λ_j** = log(3) - a_j·log(2) ist Tao's lokale Drift
- **t** ist die "Zeit" (Anzahl der Syracuse-Schritte)

**Unterschied**: 
- Statisch: Gewichte sind **klassenweise Mittelwerte**
- Dynamisch: Gewichte folgen der **konkreten Trajektorie** von N₀

---

## Implementation

### Kernmodul: `syracuse_dynamics.py`

#### Funktionen

**`valuation_2(n)`**
- Berechnet die 2-adische Valuation ν₂(n)
- Beispiel: `valuation_2(12) = 2` (da 12 = 2² · 3)

**`syracuse_step(n)`**
- Ein Schritt der Syracuse-Funktion
- Rückgabe: (Syr(n), a) wobei a = ν₂(3n+1)

**`syracuse_trajectory(N, max_steps)`**
- Berechnet die vollständige Trajektorie S₀, S₁, S₂, ... bis zur Stopping Time τ(N)
- Rückgabe: (trajectory, valuations)

**`compute_lambda_j(n)`**
- Berechnet die lokale Drift λ = log(3) - a·log(2)

**`trajectory_statistics(trajectory, valuations)`**
- Statistiken: ⟨a_j⟩, ⟨λ_j⟩, Σλ_j, max(S_j), ...

**`compare_empirical_vs_geom2(N, n_trajectories, seed)`**
- Vergleicht empirische Syracuse-Daten mit Tao's Geom(2)-Vorhersage

**`random_coprime_6_odd(N, seed)`**
- Generiert zufällige ungerade Zahl ≤ N, coprime zu 6 (möglicher Primzahl-Kandidat)

### Hamiltonian-Klasse: `TaoSyracuseHamiltonian`

Erbt von `EABCHamiltonian` und überschreibt `_build_prime_defects()`.

#### Parameter

- **N**: Gittergröße
- **start_n**: Startwert N₀ für Syracuse-Trajektorie (ungerade)
- **trajectory_length**: Anzahl der Syracuse-Schritte
- **alpha, beta, gamma**: Kopplungskonstanten
- **periodic**: Periodische Randbedingungen (default: False)
- **use_geom2_synthetic**: Falls True, verwende synthetische Geom(2)-Valuationen statt echter Trajektorie (Kontrolle)

#### Methoden

**`info()`**
- Zeigt System- und Trajektorien-Informationen

**`compare_with_static(k)`**
- Direkter Vergleich mit `CollatzEABCHamiltonian`
- Berechnet beide Spektren und gibt Differenzen zurück

#### Beispiel

```python
from src.hamiltonian import TaoSyracuseHamiltonian

# Konstruiere Hamiltonian mit Syracuse-Trajektorie von N₀=27
H = TaoSyracuseHamiltonian(
    N=1000,          # Gittergröße
    start_n=27,      # Startwert
    trajectory_length=50,
    alpha=1.0,
    beta=0.5,
    gamma=1.5
)

# Informationen anzeigen
H.info()

# Spektrum berechnen
eigenvalues = H.compute_spectrum(k=500, which='SM')

# Vergleich mit statischem Hamiltonian
results = H.compare_with_static(k=500)
```

---

## Vergleichsstudien

### Drei Varianten

1. **Statisch (Collatz-EABC)**:
   - `CollatzEABCHamiltonian`
   - Feste log(r)-Gewichte pro EABC-Klasse
   - Mittelung über alle Primzahlen einer Klasse

2. **Dynamisch (Tao-Syracuse)**:
   - `TaoSyracuseHamiltonian(use_geom2_synthetic=False)`
   - Echte Syracuse-Trajektorie von Startwert N₀
   - Zeitabhängige Gewichte λ_j

3. **Geom(2)-Synthetisch**:
   - `TaoSyracuseHamiltonian(use_geom2_synthetic=True)`
   - Synthetische Geom(2)-verteilte Valuationen a_j
   - Kontrolle: Testet, ob die Verteilung allein (ohne konkrete Trajektorie) die Eigenschaften erklärt

### Zentrale Frage

> **Zeigen alle drei Varianten dieselbe GUE-Signatur (σ ≈ 0.52)?**

- Falls **JA**: Die GUE-Signatur ist intrinsisch zur Collatz/Syracuse-Dynamik!
- Falls **NEIN**: Die statischen EABC-Gewichte haben spezielle Eigenschaften.

### Skripte

**`compare_static_vs_dynamic.py`**
- Vollständiger Vergleich aller drei Varianten
- Berechnet Level-Spacing-Statistiken (σ, β)
- Erstellt Side-by-Side-Plots
- Interpretiert Hypothesen

**`demo_tao_syracuse.py`**
- Interaktive Demo in drei Teilen:
  1. Syracuse-Trajektorien visualisieren
  2. Tao-Hamiltonian analysieren
  3. Statisch vs. Dynamisch vergleichen

---

## Spektralanalyse

### Level-Spacing-Statistik

Nach Spectral Unfolding berechnen wir:

```
s_n = E_{n+1} - E_n  (normierte Abstände)
```

Zentrale Größen:
- **⟨s⟩**: Mittelwert (sollte ≈ 1 nach Unfolding sein)
- **σ(s)**: Standardabweichung
  - **Poisson (integrabel)**: σ ≈ 1.0
  - **GOE (Zeit-Umkehr-Symmetrie)**: σ ≈ 0.52
  - **GUE (broken TRS)**: σ ≈ 0.52
  - **GSE (Quaternionen)**: σ ≈ 0.37

### Wigner-Surmise

Fit der Level-Spacing-Verteilung P(s) an:

```
P_β(s) ∝ s^β exp(-c_β s²)
```

wobei β der Repulsion-Parameter ist:
- **β = 0**: Poisson (integrabel)
- **β = 1**: GOE
- **β = 2**: GUE
- **β = 4**: GSE

### Erwartete Resultate

Für das EABC-System mit gebrochener Zeit-Umkehr-Symmetrie (durch chiralen Term H_χ):

```
σ ≈ 0.52   (GUE)
β ≈ 2
```

**Hypothese**: Diese Signatur sollte für **alle drei Varianten** ähnlich sein, wenn Tao's Theorie die Physik korrekt beschreibt.

---

## Tests

### `test_syracuse_dynamics.py`

Testet die Korrektheit der Syracuse-Funktion:
- `TestValuation2`: ν₂(n) für verschiedene n
- `TestSyracuseStep`: Einzelne Schritte Syr(n)
- `TestSyracuseTrajectory`: Vollständige Trajektorien
- `TestComputeLambdaJ`: Drift-Berechnung
- `TestGeom2Theory`: Vergleich mit Tao's Vorhersagen

### `test_tao_hamiltonian.py`

Testet die Hamiltonian-Konstruktion:
- `TestTaoSyracuseHamiltonianConstruction`: Basis-Konstruktion
- `TestTaoSyracuseDefects`: Defekt-Term korrekt
- `TestComparisonMethods`: Vergleichsmethoden funktionieren
- `TestEdgeCases`: Randfälle (kurze/lange Trajektorien, etc.)
- `TestSpectralProperties`: Spektrum ist reell, hermitisch

### `test_geom2_ensemble.py`

Testet Ensemble-Statistiken:
- `TestGeom2Sampling`: Geom(2)-Sampling korrekt
- `TestEmpiricalVsTheory`: Empirische Daten vs. Theorie
- `TestEnsembleConsistency`: Verschiedene Startwerte → ähnliche Resultate
- `TestDriftConsistency`: Negative Drift konsistent

#### Ausführung

```bash
# Alle Tests
pytest tests/test_syracuse_dynamics.py -v
pytest tests/test_tao_hamiltonian.py -v
pytest tests/test_geom2_ensemble.py -v

# Nur schnelle Tests (ohne slow marker)
pytest tests/test_geom2_ensemble.py -v -m "not slow"
```

---

## Verwendung

### Schnellstart

```python
from src.hamiltonian import TaoSyracuseHamiltonian
from src.level_spacing import compute_level_spacing, spectral_unfolding
import numpy as np

# 1. Hamiltonian konstruieren
H = TaoSyracuseHamiltonian(N=1000, start_n=27, trajectory_length=50)

# 2. Spektrum berechnen
E = H.compute_spectrum(k=500)

# 3. Level-Spacing-Statistik
E_unfolded = spectral_unfolding(E)
spacings = compute_level_spacing(E_unfolded)

# 4. Statistik
sigma = np.std(spacings)
print(f"σ(s) = {sigma:.4f}  (GUE: ~0.52)")
```

### Vergleich statisch vs. dynamisch

```python
from src.hamiltonian import TaoSyracuseHamiltonian, CollatzEABCHamiltonian

# Statisch
H_static = CollatzEABCHamiltonian(N=1000, gamma=1.5)
E_static = H_static.compute_spectrum(k=500)

# Dynamisch
H_dynamic = TaoSyracuseHamiltonian(N=1000, start_n=27, trajectory_length=50, gamma=1.5)
E_dynamic = H_dynamic.compute_spectrum(k=500)

# Differenz
delta_E = E_dynamic - E_static
print(f"⟨ΔE⟩ = {np.mean(delta_E):.6f}")
print(f"σ(ΔE) = {np.std(delta_E):.6f}")
```

### Geom(2)-Ensemble

```python
from src.syracuse_dynamics import random_coprime_6_odd
import numpy as np

sigmas = []

for i in range(50):
    start_n = random_coprime_6_odd(1000, seed=i)
    H = TaoSyracuseHamiltonian(N=1000, start_n=start_n, trajectory_length=50)
    E = H.compute_spectrum(k=500)
    # ... (Unfolding, Spacings)
    sigmas.append(sigma)

print(f"⟨σ⟩_ensemble = {np.mean(sigmas):.4f} ± {np.std(sigmas):.4f}")
```

---

## Interpretation der Resultate

### Szenario A: σ_dynamisch ≈ σ_statisch ≈ 0.52

**Interpretation**:
- Die GUE-Signatur ist **intrinsisch zur Syracuse-Dynamik**
- Die statischen EABC-Gewichte sind eine gute **Mittelung** über typische Trajektorien
- Tao's Geom(2)-Mischung erzeugt Quantenchaos
- **Starke Evidenz** für die Robustheit der Collatz-Quantenkopplung

### Szenario B: σ_dynamisch ≠ σ_statisch

**Interpretation**:
- Die statischen EABC-Gewichte haben **spezielle Eigenschaften**
- Die echte Trajektorie zeigt anderes Verhalten als der Klassenmittelwert
- Möglicherweise sind die Trajektorien **kohärenter** oder **inkohärenter** als der Mittelwert
- Weitere Untersuchung der Trajektorien-Struktur nötig

### Rolle des Geom(2)-Ensembles

Falls σ_geom2 ≈ σ_dynamisch:
- Tao's **statistische Vorhersage** ist korrekt
- Die Verteilung der a_j (nicht die konkrete Sequenz) bestimmt die Spektralstatistik

Falls σ_geom2 ≠ σ_dynamisch:
- Die **Korrelationen** in der echten Trajektorie sind wichtig
- Die Geom(2)-Unabhängigkeitsannahme ist zu grob

---

## Literatur

### Primärquellen

1. **T. Tao** (2019): ["Almost all Collatz orbits attain almost bounded values"](https://arxiv.org/abs/1909.03562)
   - Geom(2)-Hypothese für a_j
   - Negative Drift E[λ_j] = log(3/4)
   - Bedingte Konvergenz

2. **T. Tao** (Blog): [Collatz Conjecture Research](https://terrytao.wordpress.com/tag/collatz-conjecture/)
   - Informelle Erklärungen
   - Heuristische Argumente

### Spektraltheorie

3. **M. Mehta** (2004): *Random Matrices*
   - GUE, GOE, GSE Ensembles
   - Wigner-Surmise
   - Level-Spacing-Statistiken

4. **F. Haake** (2010): *Quantum Signatures of Chaos*
   - Quantenchaos-Kriterien
   - Spectral Unfolding
   - Berry-Tabor vs. Bohigas-Giannoni-Schmit

### Verwandte Arbeiten

5. **Paper C** (eigenes Projekt): "Conditional Collatz via G2 Log-Drift Axiom"
   - EABC-Klassifikation
   - Statische log(r)-Gewichte
   - G2-Axiom

6. **EABC-Qubit Framework** (dieses Projekt):
   - Quantenmechanische Formulierung
   - Chiraler Term H_χ
   - Primzahl-Defekte

---

## Ausblick

### Zukünftige Erweiterungen

1. **Zeitabhängige Spektralanalyse**:
   - H(t) für verschiedene Trajektorienlängen t
   - Relaxation zur GUE-Statistik

2. **Trajektorien-Clustering**:
   - Gruppiere Startwerte nach ähnlichen Trajektorien
   - Untersuche Ensemble-Substrukturen

3. **Höhere Momente**:
   - Nicht nur σ(s), sondern auch Schiefe, Kurtosis
   - Feinere GUE-Tests (z.B. number variance Σ²(L))

4. **Lokale Defekt-Korrelationen**:
   - Räumliche Korrelationen der Syracuse-Defekte
   - Vergleich mit Primzahl-Korrelationen

5. **Dynamische Observablen**:
   - Zeitentwicklung unter H(t)
   - Quantenphasen-Übergänge?

6. **Experimentelle Realisierung**:
   - Könnte man H^{Tao} in einem Quantensimulator implementieren?
   - Ultrakalte Atome in optischen Gittern mit programmierbaren Defekten

---

## FAQ

### Warum Syracuse statt Collatz?

Die Syracuse-Funktion Syr(n) = (3n+1)/2^a fasst mehrere Collatz-Schritte zusammen:
- Collatz: n → 3n+1 → (3n+1)/2 → (3n+1)/4 → ...
- Syracuse: n → (3n+1)/2^a direkt

Dies ist **effizienter** und zeigt die Rolle der 2-adischen Valuation a deutlicher.

### Warum ist die Drift negativ?

Tao zeigt: Für typische n ist a_j ≈ Geom(2) mit E[a_j] = 2. Daher:

```
E[λ_j] = E[log(3) - a_j·log(2)]
       = log(3) - 2·log(2)
       = log(3/4) < 0
```

Die Multiplikation mit 3 wird **im Durchschnitt** durch die Division durch 4 (= 2²) überkompensiert.

### Was ist der Unterschied zu den statischen Gewichten?

**Statisch**: log(r) ist ein **Klassenmittelwert**
- Alle Primzahlen p ≡ 1 (mod 12) erhalten log(r) = -log(2)
- Unabhängig von der konkreten Trajektorie

**Dynamisch**: λ_j folgt der **echten Trajektorie**
- Jeder Schritt hat ein individuelles λ_j basierend auf a_j
- Berücksichtigt Korrelationen in der Trajektorie

### Wie wähle ich den Startwert N₀?

Empfehlungen:
- **Ungerade** (Syracuse ist nur für ungerade Zahlen definiert)
- **Coprime zu 6** (d.h. nicht durch 2 oder 3 teilbar)
- **Typisch**: Zahlen wie 7, 11, 27, 31, 47 haben interessante Trajektorien
- **Ensemble**: Für Ensemble-Studien, verwende `random_coprime_6_odd(N, seed)`

### Was bedeutet "Geom(2)"?

Geom(p) ist die geometrische Verteilung:
- Anzahl von Bernoulli-Trials (Münzwürfe) bis zum ersten Erfolg
- Für p = 1/2 (fairer Münzwurf): E[X] = 1/p = 2

Tao's Hypothese: a_j verhält sich wie Geom(1/2), d.h. die Valuation ist wie "Anzahl von Bits bis zur ersten 0".

### Wie lange sollte die Trajektorie sein?

Faustregel:
- **Kurz** (10-20 Schritte): Schnell, aber wenig Statistik
- **Mittel** (30-50 Schritte): Guter Kompromiss
- **Lang** (100+ Schritte): Mehr Statistik, aber rechenintensiv

Die meisten Trajektorien konvergieren zu 1 innerhalb von 50-100 Schritten.

---

## Kontakt und Beiträge

Für Fragen, Bugs oder Feature-Requests:
- Öffne ein Issue im Repository
- Oder kontaktiere die Entwickler direkt

Beiträge (Pull Requests) sind willkommen!

---

**Letzte Aktualisierung**: 2026-06-23

**Version**: 1.0

**Status**: Experimentell (Forschungscode)
