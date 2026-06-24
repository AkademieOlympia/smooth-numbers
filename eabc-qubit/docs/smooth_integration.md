# Smooth Numbers Integration - Dokumentation

## Überblick

Diese Erweiterung integriert die **Smooth Numbers** (k-glatte Zahlen) aus dem C++ Projekt als zusätzliche Potentiallandschaft in das EABC-Qubit-Framework.

### Erweiterte Hamiltonian-Gleichung

```
H = α H_T + β H_χ + γ H_p + η H_smooth
```

wobei:
- `H_T`: Tight-Binding (kinetischer Term)
- `H_χ`: Chirale EABC-Kopplung
- `H_p`: Primzahl-Defekte (optional mit Collatz-Gewichten)
- `H_smooth`: **Neues Glattheitspotential**

## Kernkonzept: Glattheitspotential

### Definition k-Glattheit

Eine positive ganze Zahl `n` ist **k-glatt**, wenn alle ihre Primfaktoren ≤ k sind.

**Beispiele:**
- `12 = 2² × 3` ist 3-glatt (größter Primfaktor: 3)
- `30 = 2 × 3 × 5` ist 5-glatt (größter Primfaktor: 5)
- `97` (Primzahl) ist nur 97-glatt

### Glattheitsdichte

Für eine Zahl `n` definieren wir die **Glattheitsdichte**:

```python
density(n) = (Anzahl der k ≤ max_k, für die n k-glatt ist) / (max_k - 1)
```

Diese Metrik liegt in `[0, 1]`:
- **density = 1.0**: Sehr glatt (z.B. n=1, n=2)
- **density ≈ 0.0**: Rau, d.h. große Primfaktoren (z.B. große Primzahlen)

### Potentiallandschaft H_smooth

Das Glattheitspotential ordnet glatten Zahlen **niedrige Energie** zu (Potentialsenken):

```
H_smooth = η Σ_n [-density(n)] |n⟩⟨n| ⊗ 𝟙_EABC
```

**Physikalische Interpretation:**
- **Glatte Zahlen** (hohe density): Negative Energie → Potentialsenken
- **Primzahlen** (niedrige density): Weniger negative Energie → Potentialbarrieren

→ Glattheit wirkt als **anziehende Kraft** auf die Wellenfunktion.

## Implementation

### Module

#### 1. `src/smooth_integration.py`

Kernmodul für Smooth-Numbers-Funktionalität:

```python
from src.smooth_integration import (
    is_k_smooth,              # Prüft k-Glattheit
    count_k_smooth,           # Zählt k-glatte Zahlen
    smooth_density_fast,      # Berechnet Glattheitsdichte
    smooth_potential_landscape,  # Generiert Potentiallandschaft
    analyze_smooth_statistics   # Statistische Analyse
)
```

**Hauptfunktionen:**

```python
# Beispiel 1: Ist 12 glatt für k=3?
is_k_smooth(12, 3)  # → True (12 = 2² × 3)

# Beispiel 2: Glattheitsdichte einer Zahl
smooth_density_fast(12, max_k=20)  # → 0.84 (sehr glatt)
smooth_density_fast(97, max_k=20)  # → 0.05 (Primzahl, rau)

# Beispiel 3: Potentiallandschaft für N Zahlen
landscape = smooth_potential_landscape(N=1000, max_k=20)
# landscape[n-1] = Glattheitsdichte von n
```

#### 2. `src/hamiltonian.py` - Erweitert

Neue Klasse `MultiLayerHamiltonian`:

```python
from src.hamiltonian import MultiLayerHamiltonian

# Beispiel: Nur Glattheitspotential (ohne Primzahlen)
H1 = MultiLayerHamiltonian(
    N=1000,
    eta=0.5,                # Glattheitspotential-Stärke
    use_primes=False,
    use_smooth=True,
    smooth_max_k=20         # Maximaler k-Wert
)

# Beispiel: Primzahlen + Glattheit
H2 = MultiLayerHamiltonian(
    N=1000,
    gamma=1.5,              # Primzahl-Defekte
    eta=0.5,                # Glattheitspotential
    use_primes=True,
    use_smooth=True
)

# Beispiel: Alle Schichten (Primzahlen + Collatz + Glattheit)
H3 = MultiLayerHamiltonian(
    N=1000,
    gamma=1.5,
    eta=0.5,
    use_primes=True,
    use_collatz=True,       # Collatz-Gewichte
    use_smooth=True
)

# Spektrum berechnen
eigenvalues = H3.compute_spectrum(k=500)
```

**Parameter:**
- `eta`: Stärke des Glattheitspotentials (default: 0.5)
- `use_smooth`: Glattheitspotential aktivieren (default: False)
- `smooth_max_k`: Maximaler k-Wert für Glattheitsdichte (default: 20)

#### 3. `compare_layers.py` - Systematischer Vergleich

Skript für vollständige Layer-Analyse:

```bash
cd eabc-qubit
python compare_layers.py
```

**Vergleicht folgende Szenarien:**
1. Baseline (nur TB + χ)
2. Primes only
3. Smooth only
4. Primes + EABC
5. Primes + Collatz
6. Primes + Collatz + Smooth
7. All layers

**Output:**
- `results/layer_comparison.csv` - Metriken-Tabelle
- `results/layer_comparison.json` - JSON-Daten
- `figures/layer_comparison.png` - Visualisierung

## Die zentrale Forschungsfrage

**Wirkt Glattheit verstärkend oder dämpfend auf das Chaos im Spektrum?**

### Hypothesen

**Hypothese A: Glättung**
- Glattheit glättet auch das Spektrum
- Erwartung: Brody-Parameter `q` sinkt
- Interpretation: Smooth-Potential unterdrückt Chaos

**Hypothese B: Verstärkung**
- Glattheit + Primzahlen = destruktive Interferenz
- Erwartung: `q` steigt
- Interpretation: Zusätzliche Struktur verstärkt Chaos

**Hypothese C: Orthogonalität**
- Glattheit ist orthogonal zu Primzahl-Chaos
- Erwartung: `q` bleibt konstant
- Interpretation: Kein Effekt auf Spektralstatistik

### Metriken

**1. Brody-Parameter q**
- `q = 0`: Poisson-Verteilung (integrabel)
- `q = 1`: GOE/GUE-Verteilung (chaotisch)
- Zwischenwerte: Level-Repulsion

**2. Level Spacing Ratio ⟨r⟩**
- `⟨r⟩ = 0.386`: Poisson
- `⟨r⟩ = 0.530`: GOE
- `⟨r⟩ = 0.603`: GUE

**3. Spectral Rigidity Σ²(L)**
- Maß für spektrale Korrelationen
- Höhere Werte → mehr Rigidität

## Workflow

### 1. C++ Daten generieren (optional)

Falls Sie neue Smooth-Daten generieren möchten:

```bash
cd /Users/thomashoffbauer/Projects/smooth-numbers
make demo-smooth-export

# Generiert:
# - smooth_triangle.csv
# - smooth_triangle.json
# - dreieck_visualisierung.html
```

### 2. Python Integration testen

```bash
cd eabc-qubit

# Test Smooth-Integration-Modul
python -m pytest tests/test_smooth_integration.py -v

# Test MultiLayerHamiltonian
python -c "from src.hamiltonian import MultiLayerHamiltonian; \
           H = MultiLayerHamiltonian(N=100, use_smooth=True); \
           H.info()"
```

### 3. Vollständiger Layer-Vergleich

```bash
cd eabc-qubit
python compare_layers.py
```

**Erwartete Ausgabe:**
```
╔═══════════════════════════════════════════════════════════════════╗
║  SMOOTH INTEGRATION - Systematischer Layer-Vergleich             ║
╚═══════════════════════════════════════════════════════════════════╝

Konfiguration:
  Gittergröße N:    1000
  Eigenwerte k:     500
  Smooth max_k:     20

==================================================================
LAYER COMPARISON - Spektrale Metriken
==================================================================

Scenario                       │      q │    ⟨r⟩ │     Σ² │ P C S
──────────────────────────────┼────────┼────────┼────────┼──────
Baseline (nur TB+χ)            │  0.215 │  0.412 │  0.134 │ ✗ ✗ ✗
Primes only                    │  0.653 │  0.502 │  0.287 │ ✓ ✗ ✗
Smooth only                    │  0.318 │  0.445 │  0.189 │ ✗ ✗ ✓
Primes + EABC                  │  0.687 │  0.515 │  0.301 │ ✓ ✗ ✗
Primes + Collatz               │  0.712 │  0.521 │  0.315 │ ✓ ✓ ✗
Primes + Collatz + Smooth      │  0.678 │  0.508 │  0.295 │ ✓ ✓ ✓
All layers                     │  0.678 │  0.508 │  0.295 │ ✓ ✓ ✓
==================================================================
```

### 4. Ergebnisse analysieren

Die Plots zeigen:
1. **Brody q** für alle Szenarien
2. **Level Spacing Ratio ⟨r⟩**
3. **Δq**: Effekt von Glattheit (grün = dämpfend, rot = verstärkend)

## Beispiele

### Beispiel 1: Glattheitsdichte einzelner Zahlen

```python
from src.smooth_integration import smooth_density_fast, largest_prime_factor

test_numbers = [1, 2, 12, 30, 97, 128, 210, 997]

for n in test_numbers:
    density = smooth_density_fast(n, max_k=20)
    p_max = largest_prime_factor(n)
    print(f"n = {n:4d}: größter Primfaktor = {p_max:3d}, Dichte = {density:.3f}")

# Output:
# n =    1: größter Primfaktor =   1, Dichte = 1.000
# n =    2: größter Primfaktor =   2, Dichte = 1.000
# n =   12: größter Primfaktor =   3, Dichte = 0.895
# n =   30: größter Primfaktor =   5, Dichte = 0.789
# n =   97: größter Primfaktor =  97, Dichte = 0.000
# n =  128: größter Primfaktor =   2, Dichte = 1.000
# n =  210: größter Primfaktor =   7, Dichte = 0.684
# n =  997: größter Primfaktor = 997, Dichte = 0.000
```

### Beispiel 2: Potentiallandschaft visualisieren

```python
import matplotlib.pyplot as plt
from src.smooth_integration import smooth_potential_landscape

# Generiere Landschaft
landscape = smooth_potential_landscape(N=200, max_k=20)

# Plot
plt.figure(figsize=(12, 4))
plt.plot(range(1, 201), landscape, 'o-', markersize=2, alpha=0.7)
plt.xlabel('n')
plt.ylabel('Glattheitsdichte')
plt.title('Smooth Potential Landscape (N=200)')
plt.grid(alpha=0.3)
plt.show()
```

### Beispiel 3: Vergleich mit/ohne Smooth

```python
from src.hamiltonian import MultiLayerHamiltonian
from src.level_spacing import estimate_brody_q, compute_level_spacings

# Ohne Smooth
H1 = MultiLayerHamiltonian(N=1000, use_primes=True, use_smooth=False)
E1 = H1.compute_spectrum(k=500)
q1 = estimate_brody_q(compute_level_spacings(E1))

# Mit Smooth
H2 = MultiLayerHamiltonian(N=1000, use_primes=True, use_smooth=True, eta=0.5)
E2 = H2.compute_spectrum(k=500)
q2 = estimate_brody_q(compute_level_spacings(E2))

print(f"Ohne Smooth: q = {q1:.3f}")
print(f"Mit Smooth:  q = {q2:.3f}")
print(f"Δq = {q2 - q1:+.3f}")

# Interpretation:
# Δq < 0 → Glattheit dämpft Chaos
# Δq > 0 → Glattheit verstärkt Chaos
# Δq ≈ 0 → Kein Effekt
```

## Wissenschaftliche Bedeutung

Falls Glattheit messbare Effekte zeigt:

→ **Arithmetische Struktur (nicht nur Primzahlen) ist spektral relevant!**

Dies würde bedeuten, dass nicht nur Primzahl-Defekte, sondern auch die **Faktorisierungsstruktur** (Glattheit) einen direkten Einfluss auf die Quantendynamik hat.

### Mögliche Interpretationen

**Falls Δq < 0 (Glättung):**
- Glattheit wirkt als "regularisierende Kraft"
- Smooth-Zahlen erzeugen geordnetere Spektren
- Analogie: Glattheit = niedrigere Frequenzen in Signal

**Falls Δq > 0 (Verstärkung):**
- Interferenz zwischen Primzahl- und Glattheitspotential
- Zusätzliche Struktur verstärkt Chaos
- Analogie: Mehrfache Potentiale → komplexere Dynamik

**Falls Δq ≈ 0 (Orthogonalität):**
- Glattheit und Primzahlen sind spektral entkoppelt
- Smooth-Potential beeinflusst nur Energieskala, nicht Statistik

## Tests

Vollständige Test-Suite:

```bash
cd eabc-qubit
python -m pytest tests/test_smooth_integration.py -v

# Tests:
# - TestSmoothNumbers: Grundlegende Smooth-Number-Funktionen
# - TestMultiLayerHamiltonian: MultiLayerHamiltonian-Klasse
# - TestSmoothPrimeInteraction: Interaktion Smooth ↔ Primes
# - test_integration_example: Vollständiges Integrationsbeispiel
```

## Erwartete Dateien

Nach vollständiger Ausführung:

```
eabc-qubit/
├── src/
│   ├── smooth_integration.py      # Neu: Smooth-Integration
│   └── hamiltonian.py              # Erweitert: MultiLayerHamiltonian
├── tests/
│   └── test_smooth_integration.py  # Neu: Tests
├── compare_layers.py               # Neu: Vergleichsskript
├── results/
│   ├── layer_comparison.csv        # Generiert: Metriken
│   └── layer_comparison.json       # Generiert: JSON-Daten
└── figures/
    └── layer_comparison.png        # Generiert: Visualisierung
```

## Nächste Schritte

1. **Parameter-Sweep**: Variiere `eta` und `smooth_max_k` systematisch
2. **Größen-Skalierung**: Teste verschiedene `N` (100, 500, 1000, 2000)
3. **Entfaltung**: Vergleiche gefaltete vs. ungefaltete Spektren
4. **Eigenzustände**: Analysiere Lokalisierung in glatten vs. rauen Bereichen
5. **Zeitentwicklung**: Studiere Dynamik unter H_smooth

## Referenzen

- **EABC-Modell**: `EABC_MODEL.md`
- **Collatz-Integration**: `eabc-qubit/docs/collatz_integration.md`
- **Smooth Numbers (C++)**: `smooth_numbers.cpp`, `smooth_numbers_extended.cpp`
- **Export-Funktionen**: `export.h`

## Kontakt & Issues

Bei Fragen oder Problemen zur Smooth-Integration:
- Siehe `README.md` im Hauptverzeichnis
- Prüfe Tests: `pytest tests/test_smooth_integration.py -v`
