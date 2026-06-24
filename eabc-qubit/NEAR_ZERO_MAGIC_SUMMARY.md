# Near-Zero-Magic M_EABC: Implementation Summary

**Datum:** 2026-06-23  
**Status:** ✓ Vollständig implementiert

---

## Konzeptionelle Verfeinerung

### WICHTIG: Kausalität umgekehrt!

**Arithmetische Magic ≠ Chiralität selbst**

Sondern:

**Arithmetische Magic = spektrale Nichtreduzierbarkeit des EABC-Dirac-Systems**

### Kausale Hierarchie

```
Near-Zero-Spektrum → chiraler Drift → sichtbare ABCE/CEAB-Asymmetrie
```

- **Near-Zero-Moden** = der "Ofen" (Ursache)
- **Chiraler Bias** = das "Thermometer" (Wirkung)

**Magic ist die Ursache, Bias ist die Wirkung!**

---

## Primäre Definition

### M_EABC(N): Near-Zero-basierte Magic

```
M_EABC(N) = Σ_{|λ_i|<ε} w_i · Asym(v_i) / Σ w_i
```

**Parameter:**
- **λ_i**: Eigenwerte im Near-Zero-Fenster |λ_i| < ε
- **v_i**: Zugehörige Eigenvektoren
- **Asym(v_i)**: ABCE/CEAB-Asymmetrie im Eigenmodus i
- **w_i**: Spektrale Gewichte, z.B. w_i = 1/(|λ_i| + δ)
- **ε**: Near-Zero-Schwelle (typisch 0.1)
- **δ**: Regularisierung (typisch 0.01)

### Asymmetrie-Maß

```
Asym(v_i) = |ρ_i^{ABCE} - ρ_i^{CEAB}|
```

wobei:
```
ρ_i^{ABCE} = Projektion von v_i auf ABCE-Orientierung
ρ_i^{CEAB} = Projektion von v_i auf CEAB-Orientierung
```

**ABCE-Orientierung:** (A=1, B=2, C=3, E=0)  
**CEAB-Orientierung:** (C=3, E=0, A=1, B=2)

---

## Implementation

### Neue Funktionen in `src/arithmetic_magic.py`

#### 1. `extract_near_zero_modes(epsilon, k, sigma)`

Extrahiert Eigenwerte und Eigenvektoren im Near-Zero-Fenster.

```python
nzm_eigenvalues, nzm_eigenvectors = magic.extract_near_zero_modes(
    epsilon=0.1,
    k=500,
    sigma=0.0
)
```

**Returns:**
- `nzm_eigenvalues`: Near-Zero-Eigenwerte (|λ_i| < ε)
- `nzm_eigenvectors`: Zugehörige Eigenvektoren

#### 2. `eigenvector_asymmetry(eigenvector, pattern)`

Berechnet ABCE/CEAB-Asymmetrie eines Eigenvektors.

```python
asymmetry = magic.eigenvector_asymmetry(
    eigenvector=v_i,
    pattern='ABCE_CEAB'
)
```

**Muster:**
- `'ABCE_CEAB'`: Standard (empfohlen)
- `'EABC_ECBA'`: Alternative

**Returns:**
- `asymmetry`: Asymmetrie-Wert ∈ [0, 1]

#### 3. `compute_near_zero_magic(epsilon, k, delta, mode, pattern)`

Hauptfunktion: Berechnet Near-Zero-Magic.

```python
M_nz = magic.compute_near_zero_magic(
    epsilon=0.1,
    k=500,
    delta=0.01,
    mode='spectral_weighted',
    pattern='ABCE_CEAB'
)
```

**Modi:**
- `'spectral_weighted'`: w_i = 1/(|λ_i| + δ) (empfohlen)
- `'asymmetry_based'`: w_i = 1/n_nzm (uniform)
- `'count'`: M = n_nzm / k (einfachste Variante)

**Returns (Dict):**
- `M_near_zero`: Near-Zero-Magic-Wert (PRIMÄR!)
- `n_nzm`: Anzahl Near-Zero-Moden
- `mean_asymmetry`: Mittlere Asymmetrie
- `max_asymmetry`: Maximale Asymmetrie
- `total_weight`: Gesamtgewicht

#### 4. `compute_all()` - Erweitert

```python
M_all = magic.compute_all(
    compute_near_zero=True,  # Near-Zero-Magic (primär)
    compute_nzm=True,        # Alte NZM-Definition (Vergleich)
    epsilon=0.1,
    k=500,
    nz_mode='spectral_weighted',
    nz_pattern='ABCE_CEAB'
)
```

**Globale Metriken (zum Vergleich):**
- `M_bias`, `M_collatz`, `M_chi`, `M_gap`, `M_symbreak`

**Near-Zero-Metriken (primär):**
- `M_near_zero`, `n_nzm`, `mean_asymmetry`, `max_asymmetry`

---

## Test-Suite

### 1. `test_near_zero_causality.py`

Haupttest: Validiert die Kausalitätshypothese.

**Tests:**
- **Test 1:** Near-Zero vs. Global (Korrelation mit q)
- **Test 2:** ε-Abhängigkeit (Optimale Schwelle)
- **Test 3:** Pattern-Vergleich (ABCE/CEAB vs. EABC/ECBA)

**Hypothese:**
```
M_near_zero korreliert STÄRKER mit q als M_chi (global)
```

**Ausführung:**
```bash
python test_near_zero_causality.py
```

**Output:**
- `figures/near_zero_causality.png` (Hauptresultat)
- `figures/epsilon_dependence.png`

### 2. `test_magic_correlation.py`

Vollständige Test-Suite (inkl. globaler Metriken zum Vergleich).

**Tests:**
- β-Sweep (Chiralitäts-Stärke)
- γ-Sweep (Primzahl-Defekt-Stärke)
- Collatz vs. Uniform

### 3. Unit-Tests

`tests/test_arithmetic_magic.py` - Grundlegende Validierung.

---

## Demos

### 1. `demo_near_zero_magic.py`

Schnelle Demo der Near-Zero-Magic (primäre Definition).

**Demos:**
- Demo 1: Basis-Berechnung
- Demo 2: Near-Zero vs. Global
- Demo 3: Pattern-Vergleich
- Demo 4: ε-Sensitivität

**Ausführung:**
```bash
python demo_near_zero_magic.py
```

### 2. `demo_magic.py`

Allgemeine Magic-Demo (inkl. globaler Metriken).

---

## Dokumentation

### 1. `docs/magic_holography_analogy.md`

Theoretischer Hintergrund - **AKTUALISIERT** mit:
- Near-Zero-Definition (primär)
- Kausale Hierarchie
- Hierarchie der Observablen
- Holographie-Analogie (verfeinert)

### 2. `MAGIC_README.md`

Übersicht - **AKTUALISIERT** mit:
- Near-Zero-Definition
- Verwendungsbeispiele
- Erwartete Ergebnisse

### 3. `NEAR_ZERO_MAGIC_SUMMARY.md` (dieses Dokument)

Vollständige Implementation-Zusammenfassung.

---

## Erwartete Ergebnisse

### Kausalitäts-Test

**Falls Hypothese korrekt:**

```
Korrelation M_near_zero vs. q:  > 0.9  (sehr stark!)
Korrelation M_chi vs. q:        > 0.8  (stark)

→ M_near_zero ist stärker korreliert als M_chi!
```

**Interpretation:**
```
Near-Zero-Sektor → primäre Quelle der Magic
Chiralität → makroskopischer Ordnungsparameter (Wirkung)
```

### β-Sweep

**Erwartung:**
- M_near_zero wächst mit β (wie M_chi)
- ABER: M_near_zero erfasst lokale Asymmetrie (kritischer Sektor)
- M_chi erfasst nur globale Chiralität

### ε-Abhängigkeit

**Optimale Schwelle:**
- Zu klein (ε < 0.05): Zu wenige Moden, hohe Varianz
- Zu groß (ε > 0.3): Zu viele Moden, Signal verdünnt
- **Optimal: ε ≈ 0.1 - 0.15**

---

## Hierarchie der Observablen

1. **Q_4(N)**: Vierlingspopulation (Entanglement-Struktur)
2. **D_r(N)**: lokale Wigner-Zellen-Differenzen
3. **M_EABC(N)**: arithmetische Magic (Near-Zero-Sektor) ← **PRIMÄR**
4. **κ_EABC(N)**: chirale Krümmung/Drift (makroskopisch)

**Kausalität:**
```
M_EABC(N) → κ_EABC(N) → Beobachtbarer Bias
```

---

## Holographie-Analogie (Verfeinert)

| Holographie | EABC-Qubit | Observabel |
|-------------|------------|------------|
| **Entanglement** | **EABC-Struktur** | Q_4(N) |
| **Code-Subspace** | **Wigner-Zellen** | D_r(N) |
| **Magic** | **Near-Zero-Dirac-Sektor** | M_EABC(N) |
| **Gravitative Rückwirkung** | **Chiraler Drift** | κ_EABC(N) |
| **Krümmung** | **ABCE/CEAB-Bias** | Beobachtbar |

---

## Workflow

### Quick Start

```bash
# 1. Demo ausführen (5 min)
python demo_near_zero_magic.py

# 2. Kausalitäts-Tests (30-60 min)
python test_near_zero_causality.py

# 3. Plots analysieren
open figures/near_zero_causality.png
```

### Vollständige Analyse

```bash
# 1. Near-Zero-Tests
python test_near_zero_causality.py

# 2. Globale Metriken (Vergleich)
python test_magic_correlation.py

# 3. Unit-Tests
pytest tests/test_arithmetic_magic.py -v
```

### Eigene Analyse

```python
from src.hamiltonian import EABCHamiltonian
from src.arithmetic_magic import ArithmeticMagic

# System erstellen
H = EABCHamiltonian(N=1000, beta=0.5, gamma=1.5)

# Magic berechnen
magic = ArithmeticMagic(H)

# Near-Zero-Magic (primär!)
M_nz = magic.compute_near_zero_magic(
    epsilon=0.1,
    k=500,
    mode='spectral_weighted'
)

print(f"M_near_zero = {M_nz['M_near_zero']:.4f}")

# Globale Metriken (Vergleich)
M_global = magic.compute_all(compute_near_zero=False)
print(f"M_chi = {M_global['M_chi']:.4f}")

# Vergleich
print(f"Δ = {M_nz['M_near_zero'] - M_global['M_chi']:+.4f}")
```

---

## Nächste Schritte

### 1. Validierung

- [ ] Kausalitäts-Tests ausführen
- [ ] Korrelation M_near_zero vs. q prüfen
- [ ] Vergleich mit globalen Metriken
- [ ] Dokumentation der Ergebnisse

### 2. Erweiterungen

- [ ] Andere Asymmetrie-Maße (nicht nur ABCE/CEAB)
- [ ] Zeitabhängige Magic (dynamisches System)
- [ ] Verbindung zum Primzahl-Projekt (echte κ_EABC-Daten)
- [ ] Größere Systeme (N > 1000)

### 3. Publikation

Falls M_near_zero stark mit q korreliert:

→ **"Near-Zero-Magic als Steuerparameter des Chaos-Übergangs in arithmetischen Quantensystemen"**

---

## Technische Details

### Performance

**Near-Zero-Magic:**
- Requires: Eigenvectors (rechenintensiv!)
- Time: ~1-2 min für N=500, k=500
- Memory: ~4N² für sparse Eigenvector-Matrix

**Globale Metriken:**
- No diagonalization required
- Time: <1 sec für N=1000
- Memory: Minimal

### Genauigkeit

**Near-Zero-Schwelle ε:**
- Trade-off: Genauigkeit vs. Statistik
- ε = 0.1: ~20-50 Moden (gut)
- ε = 0.05: ~5-15 Moden (wenig Statistik)
- ε = 0.2: ~50-100 Moden (viele Moden, aber Signal verdünnt)

**Regularisierung δ:**
- Vermeidet Division durch Null
- δ = 0.01: Standard
- Zu groß (δ > 0.1): Wäscht Spektralstruktur aus
- Zu klein (δ < 0.001): Numerische Instabilität

---

## Zusammenfassung

**Arithmetische Magic M_EABC(N)** ist jetzt vollständig implementiert mit:

1. **Primäre Definition:** Near-Zero-Sektor-basiert (theoretisch fundiert)
2. **Globale Metriken:** Zum Vergleich (schneller, weniger fundamental)
3. **Test-Suite:** Kausalitäts-Validierung
4. **Dokumentation:** Vollständig aktualisiert
5. **Demos:** Near-Zero-spezifisch und allgemein

**Kausale Hierarchie:**
```
Near-Zero-Spektrum → chiraler Drift → ABCE/CEAB-Asymmetrie → Beobachtbarer Bias
```

**Zentrale Hypothese:**
```
M_EABC(N) hoch  ⟹  starker chiraler Bias  ⟹  q_Brody ↑  ⟹  σ(s) → σ_GUE
```

**Magic ist die Ursache, Bias ist die Wirkung!**

---

*Implementation abgeschlossen: 2026-06-23*  
*Thomas Hoffbauer*
