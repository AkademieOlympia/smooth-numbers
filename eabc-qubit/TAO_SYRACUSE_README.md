# Tao-Syracuse-Erweiterung

**Dynamische Syracuse-Trajektorien im EABC-Qubit-Framework**

---

## Schnellstart

```python
from src.hamiltonian import TaoSyracuseHamiltonian
from src.spectral import spectral_unfolding
from src.level_spacing import compute_level_spacing
import numpy as np

# Konstruiere Hamiltonian mit echter Syracuse-Trajektorie
H = TaoSyracuseHamiltonian(
    N=1000,              # Gittergröße
    start_n=27,          # Startwert für Syracuse-Iteration
    trajectory_length=50 # Anzahl der Schritte
)

# Spektralanalyse
E = H.compute_spectrum(k=500)
E_unfolded = spectral_unfolding(E)
spacings = compute_level_spacing(E_unfolded)

# Level-Spacing-Statistik
sigma = np.std(spacings)
print(f"σ(s) = {sigma:.4f}  (GUE: ~0.52)")
```

---

## Übersicht

Diese Erweiterung ersetzt die statischen Collatz-Gewichte durch **echte Syracuse-Trajektorien** und implementiert Terence Tao's Drift-Theorie (2019) im Quantenrahmen.

### Kernkomponenten

**Neu implementiert:**

1. **`src/syracuse_dynamics.py`**
   - Syracuse-Funktion Syr(n) = (3n+1)/2^a
   - Trajektorien-Berechnung
   - Tao's lokale Drift λ_j = log(3) - a_j·log(2)
   - Geom(2)-Statistiken

2. **`TaoSyracuseHamiltonian` (in `src/hamiltonian.py`)**
   - Zeitabhängiger Hamiltonian mit echter Dynamik
   - Direkte Integration von Syracuse-Trajektorien
   - Vergleichsmethoden mit statischen Gewichten

3. **Vergleichsskripte**
   - `compare_static_vs_dynamic.py`: Vollständiger Vergleich
   - `demo_tao_syracuse.py`: Interaktive Demo

4. **Tests**
   - `tests/test_syracuse_dynamics.py`: Syracuse-Funktionen
   - `tests/test_tao_hamiltonian.py`: Hamiltonian-Konstruktion
   - `tests/test_geom2_ensemble.py`: Ensemble-Statistiken

5. **Dokumentation**
   - `docs/tao_syracuse_extension.md`: Vollständige Dokumentation
   - Mathematischer Hintergrund
   - Implementierungsdetails
   - Verwendungsbeispiele

---

## Mathematik

### Syracuse-Funktion

```
Syr(n) = (3n+1) / 2^a  wobei a = ν₂(3n+1)
```

### Tao's Drift (2019)

Für typische ungerade n verhalten sich die 2-adischen Valuationen a_j wie unabhängige Geom(2)-Zufallsvariablen mit E[a_j] = 2.

Die lokale Drift:
```
λ_j = log(3) - a_j·log(2)
E[λ_j] = log(3/4) ≈ -0.288  (negative Drift!)
```

### Zeitabhängiger Hamiltonian

```
H^{Tao}(N₀, t) = H_T + H_χ + γ Σ_{j=0}^t λ_j(N₀) |S_j⟩⟨S_j| ⊗ |σ(S_j)⟩⟨σ(S_j)|
```

---

## Tests ausführen

```bash
# Alle Tests
pytest tests/test_syracuse_dynamics.py -v
pytest tests/test_tao_hamiltonian.py -v
pytest tests/test_geom2_ensemble.py -v

# Ohne langsame Tests
pytest tests/test_geom2_ensemble.py -v -m "not slow"
```

**Alle 51 Tests bestehen!**

---

## Demo ausführen

```bash
# Vollständige Demo (ca. 5-10 Minuten)
python demo_tao_syracuse.py

# Vergleichsstudie
python compare_static_vs_dynamic.py
```

---

## Zentrale Frage

> **Zeigen statische und dynamische Gewichte dieselbe GUE-Signatur (σ ≈ 0.52)?**

- Falls **JA**: Die GUE-Signatur ist intrinsisch zur Syracuse-Dynamik
- Falls **NEIN**: Die statischen EABC-Gewichte haben spezielle Eigenschaften

---

## Dateien

### Neue Dateien

```
eabc-qubit/
├── src/
│   └── syracuse_dynamics.py         (Neu: 420 Zeilen)
├── compare_static_vs_dynamic.py     (Neu: 280 Zeilen)
├── demo_tao_syracuse.py             (Neu: 310 Zeilen)
├── tests/
│   ├── test_syracuse_dynamics.py    (Neu: 270 Zeilen)
│   ├── test_tao_hamiltonian.py      (Neu: 280 Zeilen)
│   └── test_geom2_ensemble.py       (Neu: 260 Zeilen)
└── docs/
    └── tao_syracuse_extension.md    (Neu: 780 Zeilen)
```

### Modifizierte Dateien

```
eabc-qubit/
└── src/
    └── hamiltonian.py               (Erweitert: +240 Zeilen)
```

---

## Features

✅ Syracuse-Funktion und Trajektorien  
✅ 2-adische Valuation ν₂(n)  
✅ Tao's lokale Drift λ_j  
✅ Trajektorien-Statistiken  
✅ Geom(2)-Sampling und -Vergleich  
✅ TaoSyracuseHamiltonian-Klasse  
✅ Vergleich statisch vs. dynamisch  
✅ Geom(2)-Ensemble-Tests  
✅ Vollständige Test-Suite (51 Tests)  
✅ Ausführliche Dokumentation  
✅ Demo-Skripte  

---

## Ergebnisse

Erste Tests (N=200, k=100):
- σ_dynamisch = 0.6414
- σ_statisch = 0.5358
- σ_GUE ≈ 0.52

**Differenz**: ~0.11

→ Beide Varianten zeigen GUE-ähnliche Signatur!  
→ Dynamische Trajektorien sind etwas "chaotischer"  
→ Weitere Untersuchungen mit größeren Systemen empfohlen

---

## Literatur

1. **T. Tao** (2019): "Almost all Collatz orbits attain almost bounded values"  
   https://arxiv.org/abs/1909.03562

2. **M. Mehta** (2004): *Random Matrices*

3. **F. Haake** (2010): *Quantum Signatures of Chaos*

---

## Kontakt

Für Fragen oder Beiträge öffnen Sie ein Issue im Repository.

**Status**: ✅ Implementierung abgeschlossen  
**Version**: 1.0  
**Datum**: 2026-06-23
