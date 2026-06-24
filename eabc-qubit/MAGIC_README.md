# Arithmetische Magic M_EABC

## KONZEPTIONELLE VERFEINERUNG (2026-06-23)

**WICHTIG:** Arithmetische Magic ≠ Chiralität selbst!

**Arithmetische Magic = spektrale Nichtreduzierbarkeit des EABC-Dirac-Systems**

Die Chiralität ist nicht die Quelle, sondern ein makroskopischer Ordnungsparameter.

### Kausale Hierarchie

```
Near-Zero-Spektrum → chiraler Drift → sichtbare ABCE/CEAB-Asymmetrie
```

Die Near-Zero-Moden sind der **Ofen**, die Orientierungszählung ist nur das **Thermometer**.

## Überblick

Dieses Modul implementiert **arithmetische Magic** für das EABC-Qubit-System, inspiriert von der holographischen Quantengravitation.

**Zentrale Idee:** Magic ist die spektrale Nichtreduzierbarkeit im Near-Zero-Sektor. Sie ist der primäre Steuerparameter!

**Zentrale Hypothese (verfeinert):**

```
M_EABC(N) hoch  ⟹  starker chiraler Bias  ⟹  q_Brody ↑  ⟹  σ(s) → σ_GUE
```

**Kausalität:** Magic ist die Ursache, Bias ist die Wirkung!

## Dateien

### Implementierung

- **`src/arithmetic_magic.py`**: Hauptmodul
  - `ArithmeticMagic`: Klasse zur Berechnung aller Magic-Maße
  - `compute_magic_vs_chaos_correlation()`: Korrelationsanalyse

### Tests & Demos

- **`test_magic_correlation.py`**: Vollständige Test-Suite
  - Test 1: β-Sweep (Chiralitäts-Stärke) → **Haupttest!**
  - Test 2: γ-Sweep (Primzahl-Defekt-Stärke)
  - Test 3: Collatz vs. Uniform (Kontrolle)

- **`demo_magic.py`**: Schnelle Demo ohne lange Berechnungen
  - Demo 1: Single-System-Analyse
  - Demo 2: β-Variation
  - Demo 3: Collatz-Effekt
  - Demo 4: Near-Zero-Mode-Analyse (optional)

### Dokumentation

- **`docs/magic_holography_analogy.md`**: Theoretischer Hintergrund
  - Holographische Quantengravitation
  - EABC-Analogie
  - Definition aller Magic-Maße
  - Testbare Vorhersagen

### Output

- **`figures/`**: Plots aus `test_magic_correlation.py`
  - `magic_vs_chaos_main.png` (Hauptresultat: M_chi vs. q)
  - `magic_correlations_all.png` (Alle Korrelationen)
  - `magic_landscape.png` (β vs. alle Magic-Maße)
  - `gamma_sweep.png` (γ-Variation)
  - `collatz_vs_uniform.png` (Collatz-Kontrolle)

## Schnellstart

### 1. Demo ausführen (5 Minuten)

```bash
cd eabc-qubit
python demo_magic.py
```

Dies zeigt die Berechnung aller Magic-Maße für verschiedene Systeme.

### 2. Vollständige Tests ausführen (30-60 Minuten)

```bash
python test_magic_correlation.py
```

Dies führt die vollständige Korrelationsanalyse durch:
- β-Sweep: 11 Werte × (Spektrum + Unfolding + LSD-Fit) ≈ 30 min
- γ-Sweep: 6 Werte ≈ 10 min
- Collatz vs. Uniform: 3 Systeme ≈ 5 min

**Ergebnis:** Plots in `figures/` + Korrelationswerte in der Konsole.

### 3. Eigene Analyse

```python
from src.hamiltonian import EABCHamiltonian
from src.arithmetic_magic import ArithmeticMagic

# System erstellen
H = EABCHamiltonian(N=1000, beta=0.5, gamma=1.5)

# Magic berechnen
magic = ArithmeticMagic(H)
M_all = magic.compute_all(compute_nzm=False)

# Ausgabe
print(magic.summary())
```

## Magic-Maße

### PRIMÄRE DEFINITION: M_near_zero (Near-Zero-Sektor)

Die theoretisch fundierteste Definition, basierend auf der Quanteninformations-Definition von Magic!

```python
M_near_zero = Σ_{|λ_i|<ε} (1/(|λ_i|+δ)) · Asym(v_i) / Σ w_i
```

wobei:
- **λ_i**: Eigenwerte im Near-Zero-Fenster |λ_i| < ε (typisch ε = 0.1)
- **v_i**: Eigenvektoren
- **Asym(v_i)**: ABCE/CEAB-Asymmetrie im Eigenmodus i
  ```
  Asym(v_i) = |ρ_i^{ABCE} - ρ_i^{CEAB}|
  ```
- **δ**: Regularisierung (typisch δ = 0.01)

**Verwendung:**

```python
from src.arithmetic_magic import ArithmeticMagic

magic = ArithmeticMagic(H)

# Berechne Near-Zero-Magic
M_nz = magic.compute_near_zero_magic(
    epsilon=0.1,
    k=500,
    mode='spectral_weighted',
    pattern='ABCE_CEAB'
)

print(f"M_near_zero = {M_nz['M_near_zero']:.4f}")
print(f"n_nzm = {M_nz['n_nzm']}")  # Anzahl Near-Zero-Moden
print(f"⟨Asym⟩ = {M_nz['mean_asymmetry']:.4f}")
```

**Interpretation:**
- M_near_zero hoch → Starke Asymmetrie im Near-Zero-Sektor
- → Treibt chiralen Drift κ_EABC
- → Führt zu beobachtbarem ABCE/CEAB-Bias
- → Erzeugt Quantenchaos (q ↑)

**Erwartung:** M_near_zero korreliert STÄRKER mit q als globale Metriken!

---

### GLOBALE METRIKEN (zum Vergleich)

Diese Metriken sind schneller zu berechnen, aber weniger fundamental:

### 1. M_bias: EABC vs ECBA Ungleichgewicht

Aus dem Primzahl-Projekt bekannt: Bias zugunsten von EABC-Übergängen.

```python
M_bias = RMS(P(E) - 1/4, P(A) - 1/4, P(B) - 1/4, P(C) - 1/4)
```

**Interpretation:** Misst die Abweichung der EABC-Klassenverteilung von Gleichverteilung.

### 2. M_collatz: Anisotropie der Collatz-Gewichte

Collatz-Gewichte sind asymmetrisch verteilt:

```
λ_E ≈ -0.693  (stark kontraktiv)
λ_A ≈ -0.143  (schwach kontraktiv)
λ_B ≈ +0.693  (expansiv!)
λ_C ≈ +0.405  (moderat expansiv)
```

```python
M_collatz = Σ_i |λ_i - ⟨λ⟩|² / ⟨λ⟩²
```

**Interpretation:** Diese Asymmetrie bricht die Z₄-Symmetrie.

### 3. M_chi: Chiralitäts-Stärke ★

Der direkte Steuerparameter!

```python
M_chi = β · ||H_χ|| / ||H_total||
```

**Interpretation:** β kontrolliert die Stärke der zyklischen Kopplung E → C → B → A → E.

**Erwartung:** M_chi korreliert stark mit q (r > 0.9)!

### 4. M_nzm: Near-Zero-Mode-Konzentration

Analog zum Participation Ratio:

```python
M_nzm = (Anzahl Eigenwerte mit |E_i| < ε) / N_total
```

**Interpretation:** Misst Kondensation nahe Fermi-Energie (kritische Systeme).

### 5. M_gap: Gap-Asymmetrie

Primzahllücken zeigen mod-12-Struktur:

```python
M_gap = |P(g≡2,4 mod 12) - P(g≡8,10 mod 12)|
```

**Interpretation:** Reflektiert arithmetische Struktur der Primzahlverteilung.

### 6. M_symbreak: Symmetriebrechungs-Index

Globales Maß für S₄-Invarianz:

```python
M_symbreak = Gini-Koeffizient der EABC-Klassenverteilung
```

**Interpretation:** 0 = perfekte Symmetrie, 1 = maximale Brechung.

## Erwartete Ergebnisse

### β-Sweep (Haupttest!)

**Falls Hypothese korrekt:**

```
Korrelation M_chi vs. q:      > 0.9  (sehr stark!)
Korrelation M_collatz vs. q:  > 0.6  (moderat)
Korrelation M_nzm vs. q:      > 0.5  (schwach-moderat)
```

**Plot:** `figures/magic_vs_chaos_main.png` sollte eine klare lineare Korrelation zeigen!

### γ-Sweep

**Erwartung:** γ sollte WENIG Einfluss auf Magic haben, da γ nur die Amplitude skaliert, nicht die Symmetriebrechung.

```
Korrelation M_chi vs. q (bei γ-Variation): < 0.3
```

### Collatz vs. Uniform

**Erwartung:** Collatz-Gewichte VERSTÄRKEN M_collatz im Vergleich zu Uniform.

```
M_collatz(Collatz) > M_collatz(Uniform)
```

## Holographische Analogie

| Holographie | EABC-Qubit |
|-------------|------------|
| **Entanglement** | **EABC-Struktur** |
| **Magic** | **M_EABC** |
| **Statische Geometrie** | **q ≈ 0 (Poisson)** |
| **Dynamische Geometrie** | **q ≈ 0.7 (GUE)** |

**Mechanismus:**

```
Holographie:  Entanglement + Magic → Dynamische Geometrie (Gravitation)
EABC:         Diskrete Struktur + M_EABC → Spektrales Chaos
```

## Physikalische Interpretation

Falls M_chi stark mit q korreliert:

→ **Die chirale Kopplung β ist nicht nur ein Parameter, sondern DIE "arithmetische Magic" des Systems - der Mechanismus, der statische EABC-Geometrie in dynamisches Quantenchaos transformiert.**

Dies wäre ein **eigenständiges Organisationsprinzip** für das gesamte Projekt!

## Literatur

- **Maldacena (1997):** AdS/CFT Korrespondenz
- **Ryu & Takayanagi (2006):** Entanglement = Geometrie
- **Bao et al. (2023):** Magic in Holographie
- **Brody (1973):** Brody-Verteilung (Chaos-Übergang)
- **Tao (2019):** Collatz-Vermutung (G2 Log-Drift Axiom)

## Nächste Schritte

1. **Tests ausführen:** `python test_magic_correlation.py`
2. **Plots analysieren:** `figures/magic_vs_chaos_main.png`
3. **Hypothese prüfen:** Ist r(M_chi, q) > 0.9?
4. **Falls ja:** Paper schreiben! "Arithmetische Magic als Steuerparameter des Chaos-Übergangs"
5. **Falls nein:** Alternative Magic-Maße entwickeln

## Kontakt

Thomas Hoffbauer, 2026  
Inspiriert von holographischer Quantengravitation und arithmetischer Geometrie
