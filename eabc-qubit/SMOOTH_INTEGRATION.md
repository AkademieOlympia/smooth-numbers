# Smooth Numbers Integration - Quick Start

## Übersicht

Diese Erweiterung integriert **k-glatte Zahlen** als zusätzliche Potentiallandschaft in das EABC-Qubit-Framework.

```
H = α H_T + β H_χ + γ H_p + η H_smooth
```

## Schnellstart

### 1. Installation prüfen

```bash
cd /Users/thomashoffbauer/Projects/smooth-numbers/eabc-qubit
python -c "from src.smooth_integration import *; print('✓ Smooth-Integration verfügbar')"
```

### 2. Basis-Demo ausführen

```bash
python demo_smooth.py
```

Zeigt:
- Glattheitsdichten einzelner Zahlen
- Potentiallandschaft-Visualisierung
- MultiLayerHamiltonian-Beispiele
- Vergleich mit/ohne Smooth

### 3. Vollständiger Layer-Vergleich

```bash
python compare_layers.py
```

Führt systematische Analyse aller Szenarien durch:
1. Baseline (nur TB + χ)
2. Primes only
3. Smooth only
4. Primes + EABC
5. Primes + Collatz
6. Primes + Collatz + Smooth
7. All layers

**Output:**
- `results/layer_comparison.csv` - Metriken
- `results/layer_comparison.json` - JSON-Daten
- `figures/layer_comparison.png` - Visualisierung

### 4. Tests ausführen

```bash
pytest tests/test_smooth_integration.py -v
```

## Hauptfeatures

### 1. Glattheitsdichte berechnen

```python
from src.smooth_integration import smooth_density_fast, largest_prime_factor

n = 12  # 12 = 2² × 3
density = smooth_density_fast(n, max_k=20)
p_max = largest_prime_factor(n)

print(f"n = {n}: größter Primfaktor = {p_max}, Dichte = {density:.3f}")
# Output: n = 12: größter Primfaktor = 3, Dichte = 0.947
```

### 2. Potentiallandschaft generieren

```python
from src.smooth_integration import smooth_potential_landscape

# Generiere Landschaft für N Zahlen
landscape = smooth_potential_landscape(N=1000, max_k=20)

# landscape[n-1] = Glattheitsdichte von n ∈ [0, 1]
# 1.0 = sehr glatt (kleine Primfaktoren)
# 0.0 = rau (große Primfaktoren, Primzahlen)
```

### 3. MultiLayerHamiltonian verwenden

```python
from src.hamiltonian import MultiLayerHamiltonian

# Nur Glattheitspotential
H1 = MultiLayerHamiltonian(
    N=1000,
    eta=0.5,                # Glattheitspotential-Stärke
    use_primes=False,
    use_smooth=True,
    smooth_max_k=20
)

# Primzahlen + Glattheit
H2 = MultiLayerHamiltonian(
    N=1000,
    gamma=1.5,              # Primzahl-Defekte
    eta=0.5,                # Glattheitspotential
    use_primes=True,
    use_smooth=True
)

# Spektrum berechnen
eigenvalues = H2.compute_spectrum(k=500)
```

### 4. Systematischer Vergleich

```python
from src.hamiltonian import MultiLayerHamiltonian
from src.level_spacing import compute_level_spacings, estimate_brody_q

# Ohne Smooth
H_without = MultiLayerHamiltonian(N=1000, use_primes=True, use_smooth=False)
E_without = H_without.compute_spectrum(k=500)
q_without = estimate_brody_q(compute_level_spacings(E_without))

# Mit Smooth
H_with = MultiLayerHamiltonian(N=1000, use_primes=True, use_smooth=True, eta=0.5)
E_with = H_with.compute_spectrum(k=500)
q_with = estimate_brody_q(compute_level_spacings(E_with))

delta_q = q_with - q_without
print(f"Δq = {delta_q:+.3f}")

# Interpretation:
# Δq < 0 → Glattheit dämpft Chaos
# Δq > 0 → Glattheit verstärkt Chaos
# Δq ≈ 0 → Kein Effekt
```

## Forschungsfrage

**Wirkt Glattheit verstärkend oder dämpfend auf das Chaos im Spektrum?**

### Hypothesen

- **A: Glättung** - Smooth-Potential unterdrückt Chaos (q sinkt)
- **B: Verstärkung** - Interferenz verstärkt Chaos (q steigt)
- **C: Orthogonalität** - Kein Effekt auf Spektralstatistik (q konstant)

### Metriken

- **Brody q**: q=0 (Poisson/integrabel) → q=1 (GUE/chaotisch)
- **⟨r⟩**: 0.386 (Poisson) → 0.530 (GOE) → 0.603 (GUE)
- **Σ²(L)**: Spectral rigidity

## Dateistruktur

```
eabc-qubit/
├── src/
│   ├── smooth_integration.py      # Neu: Smooth-Numbers-Funktionen
│   └── hamiltonian.py              # Erweitert: MultiLayerHamiltonian
├── tests/
│   └── test_smooth_integration.py  # Neu: Tests
├── docs/
│   └── smooth_integration.md       # Neu: Vollständige Dokumentation
├── demo_smooth.py                  # Neu: Quick Demo
├── compare_layers.py               # Neu: Systematischer Vergleich
├── results/                        # Generiert
│   ├── layer_comparison.csv
│   └── layer_comparison.json
└── figures/                        # Generiert
    ├── smooth_landscape_demo.png
    ├── smooth_effect_demo.png
    └── layer_comparison.png
```

## Beispielausgabe

### Glattheitsdichte

```
     n │  p_max │   Dichte │ Interpretation
──────┼────────┼──────────┼──────────────────────────────
     1 │      1 │    1.000 │ sehr glatt
    12 │      3 │    0.947 │ sehr glatt
    30 │      5 │    0.842 │ sehr glatt
    97 │     97 │    0.000 │ rau (Primzahl-artig)
   128 │      2 │    1.000 │ sehr glatt
   210 │      7 │    0.737 │ glatt
```

### Layer-Vergleich

```
Scenario                       │      q │    ⟨r⟩ │ P C S
──────────────────────────────┼────────┼────────┼──────
Baseline (nur TB+χ)            │  0.215 │  0.412 │ ✗ ✗ ✗
Primes only                    │  0.653 │  0.502 │ ✓ ✗ ✗
Smooth only                    │  0.318 │  0.445 │ ✗ ✗ ✓
Primes + Collatz               │  0.712 │  0.521 │ ✓ ✓ ✗
Primes + Collatz + Smooth      │  0.678 │  0.508 │ ✓ ✓ ✓

Δq (Primes → +Smooth) = -0.034  ← Glattheit DÄMPFT Chaos!
```

## Wissenschaftliche Bedeutung

Falls Glattheit messbare Effekte zeigt:

→ **Arithmetische Struktur (nicht nur Primzahlen) ist spektral relevant!**

Dies bedeutet, dass nicht nur Primzahl-Defekte, sondern auch die **Faktorisierungsstruktur** (Glattheit) einen direkten Einfluss auf die Quantendynamik hat.

## Weiterführende Dokumentation

- **Vollständige Dokumentation**: `docs/smooth_integration.md`
- **Tests**: `tests/test_smooth_integration.py`
- **C++ Smooth Numbers**: `../smooth_numbers.cpp`
- **EABC-Modell**: `../EABC_MODEL.md`

## Nächste Schritte

1. **Parameter-Sweep**: Variiere `eta` und `smooth_max_k`
2. **Größen-Skalierung**: Teste verschiedene N (100, 500, 1000, 2000)
3. **Eigenzustands-Analyse**: Lokalisierung in glatten vs. rauen Bereichen
4. **Zeitentwicklung**: Dynamik unter H_smooth
5. **Paper-Generation**: Ergebnisse dokumentieren

## Status

✅ **IMPLEMENTIERT** (Jun 2026)

- [x] Smooth-Integration-Modul (`src/smooth_integration.py`)
- [x] MultiLayerHamiltonian-Klasse (`src/hamiltonian.py`)
- [x] Systematischer Vergleich (`compare_layers.py`)
- [x] Tests (`tests/test_smooth_integration.py`)
- [x] Dokumentation (`docs/smooth_integration.md`)
- [x] Demo (`demo_smooth.py`)

**Bereit für wissenschaftliche Analyse!**
