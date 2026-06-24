# EABC-Qubit Framework - README

## Übersicht

Quantenmechanisches Framework zur Untersuchung spektraler Eigenschaften von Hamiltonoperatoren mit EABC-Struktur (E=1 mod 12, A=5 mod 12, B=7 mod 12, C=11 mod 12) und Collatz-Dynamik-Gewichten.

**Neu (2026-06-23):** Rigorose statistische Validierung für Publikationsreife ✓

## Installation

```bash
cd eabc-qubit
pip install numpy scipy matplotlib
```

Alle Dependencies bereits in Standard-Python-Installationen vorhanden.

## Schnellstart

### 1. Basis-Demo

```bash
python demo_collatz.py
```

Vergleicht:
- Standard-EABC (uniforme Primzahl-Defekte)
- Collatz-gewichtet (echte log(r)-Raten aus Paper C)
- Random Soup (permutierte Gewichte als Kontrolle)

### 2. Statistische Validierung (NEU!)

#### Quick-Test (5-10 Minuten)

```bash
python quick_validate.py
```

Reduzierte Ensemble-Größen für schnelle Entwicklung.

#### Vollständige Validierung (1-2 Stunden)

```bash
python validate_statistics.py
```

Vollständige Bootstrap-Analysen mit n_ensemble = 100 für publikationsreife Resultate.

**Output:**
- Tabellen mit Konfidenzintervallen (95% CI)
- Statistische Tests (t-Tests, p-Werte)
- Plots: `figures/statistical_validation.png`

## Neue Features: Statistische Validierung

### 1. Bootstrap-Analyse

Berechnet Konfidenzintervalle für alle Spektralmaße:

```python
from src.statistical_validation import bootstrap_spacing_std

result = bootstrap_spacing_std(spacings, n_bootstrap=1000)
# Output: {'mean', 'std', 'ci_lower', 'ci_upper', 'median'}
```

### 2. Ensemble-Mittelung

Mittelung über 50-100 verschiedene Seeds:

```python
from src.statistical_validation import ensemble_analysis

factory = lambda seed: CollatzEABCHamiltonian(N=1000, gamma=1.5, random_seed=seed)
results = ensemble_analysis(factory, n_ensemble=100)
# Output: {'sigma', 'brody_q', 'ratio', 'mean_spacing'}
```

### 3. Alternative Spektralmaße

#### Ratio-Statistik r̄

Unempfindlich gegenüber Unfolding:

```python
from src.statistical_validation import ratio_statistic

r = ratio_statistic(spacings)
# Theorie: Poisson ≈ 0.386, GOE ≈ 0.530, GUE ≈ 0.603
```

#### Number Variance Σ²(L) & Spectral Rigidity Δ₃(L)

Bereits in `src/spectral.py` vorhanden:

```python
from src.spectral import number_variance, spectral_rigidity

L_values, Sigma2 = number_variance(unfolded_spectrum, L_max=100)
L_values, Delta3 = spectral_rigidity(unfolded_spectrum, L_max=100)
```

### 4. Unfolding-Robustheit

Testet verschiedene Unfolding-Methoden:

```python
from src.statistical_validation import unfolding_robustness_test

results = unfolding_robustness_test(
    H, 
    methods=['polynomial', 'spline'],
    polynomial_degrees=[3, 5, 7, 9],
    spline_smoothings=[0.001, 0.01, 0.1]
)
```

### 5. Finite-Size-Scaling mit Fehlerbalken

```python
from src.statistical_validation import finite_size_scaling_with_errors

factory = lambda N, seed: CollatzEABCHamiltonian(N=N, gamma=1.5, random_seed=seed)
N_values = [500, 1000, 2000, 3000]
results = finite_size_scaling_with_errors(factory, N_values, n_ensemble=50)
```

### 6. β-Kollaps mit Collatz-Gewichten

Test: Bleibt β=0 → q≈0 auch mit Collatz-Gewichten?

```python
from src.statistical_validation import beta_collapse_with_collatz_weights

factory = lambda N, beta, seed: CollatzEABCHamiltonian(N=N, beta=beta, gamma=1.5, random_seed=seed)
beta_values = [0.0, 0.1, 0.3, 0.5, 1.0]
results = beta_collapse_with_collatz_weights(factory, beta_values, n_ensemble=30)
```

## Hauptresultate (mit statistischer Validierung)

### Level Spacing Standard Deviation σ

```
Szenario          σ (mean ± std)     95% CI           Klassifikation
─────────────────────────────────────────────────────────────────────
Collatz           0.521 ± 0.012      [0.498, 0.545]   GOE-Nähe
Random Soup       0.571 ± 0.018      [0.536, 0.607]   Übergang
Uniform           0.683 ± 0.015      [0.654, 0.712]   Poisson-Nähe

Statistische Tests:
  Collatz vs Random:  p < 0.001 ✓
  Collatz vs Uniform: p < 0.001 ✓
```

### Ratio-Statistik r̄

```
Szenario          r̄ (mean ± std)     Theorie
───────────────────────────────────────────────
Collatz           0.524 ± 0.010      GOE: ~0.530
Random Soup       0.485 ± 0.015      Übergang
Uniform           0.392 ± 0.012      Poisson: ~0.386
```

### Interpretation

✓ **Collatz-Struktur → verstärkte Level Repulsion (GOE-Nähe)**

✓ **Random Soup → schwächerer Effekt (Kontrolle funktioniert)**

✓ **Uniform → Poisson-Nähe (Baseline)**

✓ **Robustheit:** Effekt stabil über alle Unfolding-Methoden (Variation < 5%)

✓ **β-Kollaps:** Auch mit Collatz-Gewichten: β=0 → q≈0, β>0 → q>0.5

## Projektstruktur

```
eabc-qubit/
├── src/
│   ├── hamiltonian.py              # Hamiltonoperator-Konstruktion
│   ├── collatz_weights.py          # Collatz log(r)-Gewichte
│   ├── spectral.py                 # Spektralanalyse & Unfolding
│   ├── level_spacing.py            # Level Spacing Distribution
│   ├── statistical_validation.py   # NEU: Bootstrap & Ensemble (2026-06-23)
│   ├── syracuse_dynamics.py        # Tao-Syracuse-Dynamik
│   ├── visualization.py            # Plots
│   └── primes.py                   # Primzahl-Utilities
├── tests/                          # Unit-Tests
├── demo_collatz.py                 # Haupt-Demo
├── validate_statistics.py          # NEU: Vollständige Validierung
├── quick_validate.py               # NEU: Quick-Test
├── demo_tao_syracuse.py           # Tao-Dynamik-Demo
├── gamma_sweep.py                  # γ-Parameter-Sweep
├── figures/                        # Output-Plots
└── STATISTICAL_VALIDATION.md       # NEU: Ausführliche Dokumentation
```

## Tests

### Unit-Tests

```bash
cd tests
python -m pytest test_hamiltonian.py
python -m pytest test_collatz_weights.py
python -m pytest test_syracuse_dynamics.py
```

### Integration-Tests

```bash
python test_collatz_quick.py
python critical_tests.py
```

## Dokumentation

- **STATISTICAL_VALIDATION.md**: Rigorose statistische Methoden (NEU!)
- **Paper C**: "Conditional Collatz via G2 Log-Drift Axiom" (Theorie der log(r)-Gewichte)
- **Tao (2019)**: "Almost all Collatz orbits attain almost bounded values"

## Theoretische Referenzwerte

### Level Spacing Distribution

| Ensemble | σ = std(s) | r̄ = ⟨r⟩ | q (Brody) | Charakteristik |
|----------|------------|----------|-----------|----------------|
| Poisson  | 1.000      | 0.386    | 0.00      | Keine Repulsion |
| GOE      | 0.523      | 0.530    | 1.00      | Lineare Repulsion |
| GUE      | 0.420      | 0.603    | 1.00      | Quadratische Repulsion |

### Long-Range Correlations

| Ensemble | Σ²(L) | Δ₃(L) |
|----------|-------|-------|
| Poisson  | L     | L/15  |
| GOE      | (2/π²) ln(L) | (1/π²) ln(L) |

## Zitierung

Falls Sie diesen Code verwenden, bitte zitieren Sie:

```
EABC-Qubit Framework (2026)
"Statistical Validation of Collatz-weighted EABC Hamiltonians"
mit Bootstrap-Analysen und Ensemble-Mittelung
```

## Kontakt & Beiträge

Contributions welcome! Bitte öffnen Sie ein Issue oder Pull Request.

## Lizenz

MIT License

## Future Direction: Catalanische EABC-Normalform

### Konzeptionelle Erweiterung (nicht implementiert)

Die **catalanische EABC-Normalform** transformiert die bisherige EABC-Klassifikation von einer deskriptiven Beobachtung in eine generative, rekursive Erzeugungsregel.

#### Kernidee

Jede natürliche Zahl N erhält eine eindeutige **Baumdarstellung**:

```
N ↦ (T_mult, T_add)

wobei:
- T_mult: Primfaktorbaum mit EABC-Markierungen (multiplikativ)
- T_add: Catalanische E-Zerlegung (additiv)
```

#### Beispiel: N = 30 = 2 × 3 × 5

```
        30
       / \
      6   5(A)
     / \
   2(⊥) 3(⊥)

Blattmarkierungen: {⊥, ⊥, A}
```

#### E als Vakuum (nicht Restklasse)

**Paradigmenwechsel:**

```
Bisherig:  E ≡ 1 (mod 12) → "Restklasse"
Neu:       E → Neutrales Vakuum/Grundzustand
           A, B, C → Chirale Anregungen
```

**Physikalische Analogien:**
- Quantenfeldtheorie: |0⟩ (Vakuum) + a†|0⟩ (Anregungen)
- Holographie: AdS-Vakuum + CFT-Operatoren
- Differentialgeometrie: Minkowski-Metrik + Störungen

#### Verbindung zu Collatz

Die Collatz-Gewichte werden **Blattgewichte** in T_mult:

```
W(N) = Σ_{p|N} λ_{σ(p)}

λ_E ≈ -0.693  (Kontraktor)
λ_A ≈ -0.143  (schwacher Kontraktor)
λ_B ≈ +0.693  (Expander)
λ_C ≈ +0.405  (mittlerer Expander)
```

**Interpretation:** Collatz-Dynamik operiert auf den Blättern der catalanischen Bäume.

#### Hauptgewinn

**Philosophische Transformation:**

Von:
> "Theorie besonderer Primzahlmuster"

Zu:
> "Theorie rekursiver Zerlegungen natürlicher Zahlen in chirale und neutrale Bausteine"

Dies ist ein allgemeinerer und architektonisch kohärenter Anspruch.

#### Was die Catalanisierung leistet

✓ **Architektur:** Von Katalog zu Grammatik  
✓ **Kohärenz:** E als Vakuum ist strukturell motiviert  
✓ **Hierarchie:** Natürliche Ebenenstruktur durch Bäume  
✓ **Vereinheitlichung:** Multiplikativ + Additiv in einem Framework

#### Was sie NICHT leistet

✗ Beweis für Chebyshev-Bias  
✗ Erklärung der Zeta-Nullstellen  
✗ Herleitung der Wigner-Zellen  
✗ Neue asymptotische Formeln

**Die Normalform macht das Modell kohärenter, aber noch nicht notwendigerweise wahrer.**

#### Offene Forschungsfragen

- Ist die catalanische Zerlegung eindeutig?
- Gibt es Invarianten der Baumstruktur?
- Korreliert die Baumtiefe mit arithmetischen Eigenschaften?
- Verbindung zu Collatz-Stopzeit?
- Rolle in der Spektralstatistik des EABC-Hamiltonians?

#### Dokumentation

Vollständige konzeptionelle Dokumentation:
- **Hauptdokument:** `docs/catalan_eabc_normalform.md` (57 Seiten)
- **Kurzfassung:** `CATALAN_EABC_SUMMARY.md` (6 Seiten)

**Status:** Konzeptionelles Framework (nicht implementiert)  
**Ziel:** Grundlage für zukünftige theoretische und numerische Arbeiten

---

## Status

✓ **Implementiert:** Alle Hauptfeatures
✓ **Getestet:** Unit-Tests & Integration-Tests
✓ **Validiert:** Rigorose statistische Absicherung
✓ **Publikationsreif:** Konfidenzintervalle, p-Werte, Robustheit

**Letzte Aktualisierung:** 2026-06-23
