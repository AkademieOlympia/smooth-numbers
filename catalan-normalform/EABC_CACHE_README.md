# EABC-Cache: Schnellstart-Anleitung

**Datum:** 2026-06-24  
**Kontext:** H10/H11 EABC-Testinfrastruktur

---

## Überblick

Die EABC-Test-Infrastruktur bietet **effizienten, gecachten Zugriff** auf EABC-Vektoren und zugehörige Daten für große Wertebereiche.

### Performance

```
Bereich        | Cached Lookup | Uncached  | Speedup
---------------|---------------|-----------|--------
n = 2..10k     | 0.012 ms      | 0.026 ms  | 2.3×
n = 2..100k    | 0.006 ms      | 0.053 ms  | 8.8×
n = 2..1M      | ~0.003 ms     | ~0.144 ms | ~48×
```

**Generierung:**
- 10k Werte: ~0.2 Sekunden
- 100k Werte: ~3.2 Sekunden (0.84 MB)
- 1M Werte: ~35 Sekunden (geschätzt, ~8 MB)
- 10M Werte: ~24 Minuten (geschätzt, ~760 MB)

---

## Installation

```bash
# Erforderliche Pakete
pip install h5py tqdm numpy
```

---

## Schnellstart

### 1. Cache generieren

```bash
# Kleiner Test-Cache (10k)
python code/generate_eabc_cache.py --max-n 10000 --output test_cache.h5

# Mittelgroßer Cache (100k)
python code/generate_eabc_cache.py --max-n 100000 --output eabc_100k.h5

# Großer Cache (1M)
python code/generate_eabc_cache.py --max-n 10^6 --output eabc_1M.h5
```

### 2. Cache verwenden

```python
from utils.eabc_test_data import EABCTestData

# Lade Cache
data = EABCTestData(cache_file="eabc_100k.h5")

# Einzelne Lookups
eabc = data.get_eabc(12345)           # → (e, a, b, c)
omega = data.get_omega(12345)         # → Ω(n)
H = data.get_concentration(12345)     # → H(n)
coords = data.get_coordinates(12345)  # → vollständiges Dict

# Batch-Lookups (effizient!)
import numpy as np
n_values = np.arange(1000, 2000)
eabc_batch = data.get_eabc_batch(n_values)
omega_batch = data.get_omega_batch(n_values)

# Schließen
data.close()
```

### 3. Demo ausführen

```bash
python code/examples/demo_eabc_cache.py
```

---

## API-Referenz

### Klasse: `EABCTestData`

```python
EABCTestData(
    cache_file: str | Path,
    auto_load: bool = True,
    readonly: bool = True
)
```

**Methoden:**

- `get_coordinates(n)` → Dict mit allen Koordinaten
- `get_eabc(n)` → np.array [e, a, b, c]
- `get_omega(n)` → Ω(n) (Primfaktoranzahl)
- `get_concentration(n)` → H(n) (Konzentration)
- `get_shell(n)` → S(n) = v₂ + v₃
- `get_sigma(n)` → σ(n) (Teilersumme)

**Batch-Methoden:**

- `get_coordinates_batch(n_values)` → List[Dict]
- `get_eabc_batch(n_values)` → np.array (n, 4)
- `get_omega_batch(n_values)` → np.array (n,)
- `get_concentration_batch(n_values)` → np.array (n,)

### Funktion: `create_cache`

```python
create_cache(
    max_n: int,
    output_file: str | Path,
    chunk_size: int = 100_000,
    show_progress: bool = True,
    compression: str = 'gzip'
)
```

---

## Datenmodell

Pro Eintrag (n):

```python
{
    'n': int,              # Zahl selbst
    'omega': int,          # Ω(n) - Primfaktoranzahl
    'sigma': int,          # σ(n) - Teilersumme
    'v2': int,             # v₂(n) - 2-adische Bewertung
    'v3': int,             # v₃(n) - 3-adische Bewertung
    'shell': int,          # S(n) = v₂ + v₃
    'e': int,              # Anzahl E-Faktoren (≡ 1 mod 12)
    'a': int,              # Anzahl A-Faktoren (≡ 5 mod 12)
    'b': int,              # Anzahl B-Faktoren (≡ 7 mod 12)
    'c': int,              # Anzahl C-Faktoren (≡ 11 mod 12)
    'omega_eabc': int,     # Ω_EABC = e + a + b + c
    'norm_sq': float,      # ||v||² = e² + a² + b² + c²
    'H': float,            # H(n) - Konzentration
}
```

---

## Anwendungsbeispiele

### Statistische Analyse

```python
from utils.eabc_test_data import EABCTestData
import numpy as np
import matplotlib.pyplot as plt

data = EABCTestData(cache_file="eabc_100k.h5")

# Alle Werte laden
n_values = np.arange(2, 100_001)
H_values = data.get_concentration_batch(n_values)

# Statistiken
valid_H = H_values[~np.isnan(H_values)]
print(f"Durchschnitt H(n): {np.mean(valid_H):.4f}")
print(f"Median H(n): {np.median(valid_H):.4f}")

# Plot
plt.figure(figsize=(12, 6))
plt.scatter(n_values, H_values, alpha=0.3, s=1)
plt.xlabel('n')
plt.ylabel('H(n)')
plt.title('Konzentration H(n)')
plt.savefig('H_distribution.png', dpi=300)

data.close()
```

### Spezifische Signaturen finden

```python
from utils.eabc_test_data import EABCTestData

data = EABCTestData(cache_file="eabc_100k.h5")

# Finde Zahlen mit gleicher Verteilung (e=a=b=c=1)
results = []
for n in range(2, 100_000):
    coords = data.get_coordinates(n)
    if (coords['e'] == 1 and coords['a'] == 1 and 
        coords['b'] == 1 and coords['c'] == 1):
        results.append(n)

print(f"Gefunden: {len(results)} Zahlen")
print(f"Kleinste: {min(results)}")
print(f"EABC: {data.get_eabc(min(results))}")

data.close()
```

### Performance-Vergleich

```python
from utils.eabc_test_data import EABCTestData
from utils.eabc import compute_svn_coordinates
import numpy as np
import time

data = EABCTestData(cache_file="eabc_100k.h5")

n_values = np.random.randint(2, 100_000, size=10_000)

# Cached
start = time.time()
for n in n_values:
    _ = data.get_coordinates(n)
time_cached = time.time() - start

# Uncached
start = time.time()
for n in n_values:
    _ = compute_svn_coordinates(n)
time_uncached = time.time() - start

speedup = time_uncached / time_cached
print(f"Cached:   {time_cached:.2f} s")
print(f"Uncached: {time_uncached:.2f} s")
print(f"Speedup:  {speedup:.1f}×")

data.close()
```

---

## Dateien

```
catalan-normalform/
├── EABC_TEST_INFRASTRUCTURE.md    # Vollständiges Design-Dokument
├── EABC_CACHE_README.md           # Diese Datei (Schnellstart)
├── code/
│   ├── generate_eabc_cache.py     # CLI-Tool zur Cache-Generierung
│   ├── utils/
│   │   ├── eabc.py                # Original EABC-Funktionen
│   │   ├── eabc_test_data.py      # Cache-Klasse
│   │   └── eabc_benchmark.py      # Performance-Tests
│   └── examples/
│       └── demo_eabc_cache.py     # Interaktive Demo
├── test_eabc_cache.h5             # Test-Cache (10k)
└── eabc_cache_100k.h5             # Mittelgroßer Cache (100k)
```

---

## Nächste Schritte

### Für Tests (sofort nutzbar)

1. Verwende `eabc_cache_100k.h5` für Tests bis n=100,000
2. Generiere größere Caches bei Bedarf
3. Integriere in bestehende Experimente

### Für H12+ (zukünftige Erweiterungen)

- **EABC-sensitive M_C-Metrik:** Wie in H10 vorgeschlagen
- **Quaternionen-Repräsentation:** Für algebraische Analysen
- **SQL-Interface:** Für komplexe Queries
- **Cloud-Storage:** Für geteilte Caches

---

## Zusammenhang mit H10/H11

### H10-Erkenntnis: M_C ist EABC-blind

Aus `H10_INTERPRETATION_V3.md`:

> **Die aktuelle Definition von M_C kennt EABC überhaupt nicht.**

Die EABC-Test-Infrastruktur ermöglicht:

1. **Effiziente EABC-Analysen** unabhängig von M_C
2. **Entwicklung EABC-sensitiver Metriken** (H12+)
3. **Statistische Validierung** von EABC-Hypothesen

### Keine Hurwitz-Quaternionen-Implementierung

**Status:** Nicht implementiert (und derzeit nicht notwendig)

**Begründung:**
- EABC-Vektoren als ℤ⁴-Tupel sind ausreichend
- Quaternionen wären nur relevant für EABC-sensitive Algebra
- Kann bei Bedarf später hinzugefügt werden (H12+)

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'h5py'"

```bash
pip install h5py tqdm
```

### "Cache-Datei nicht gefunden"

Generiere zuerst einen Cache:

```bash
python code/generate_eabc_cache.py --max-n 10000 --output test_cache.h5
```

### Warnung "Wert n=X nicht im Cache"

Dieser Wert liegt außerhalb des Cache-Bereichs. Generiere einen größeren Cache oder akzeptiere die direkte Berechnung (Fallback).

### Speicherprobleme bei großen Caches

- Verwende `readonly=True` (Standard)
- HDF5 lädt Daten lazy (nicht alles in Memory)
- Reduziere `chunk_size` bei Generierung

---

## Support & Feedback

- **Design-Dokument:** `EABC_TEST_INFRASTRUCTURE.md`
- **Performance-Tests:** `code/utils/eabc_benchmark.py`
- **Interaktive Demo:** `code/examples/demo_eabc_cache.py`

---

**Happy Testing! 🚀**
