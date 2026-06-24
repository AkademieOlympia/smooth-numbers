# EABC-TEST-INFRASTRUKTUR

**Datum:** 2026-06-24  
**Status:** Design & Implementierung  
**Kontext:** H10/H11 Experimente

---

## 1. MOTIVATION

### Problem
Die aktuelle EABC-Implementierung (`code/utils/eabc.py`) berechnet bei jedem Aufruf eine vollständige Primfaktorzerlegung. Dies ist ineffizient für:

- Große Test-Suites mit wiederholten Berechnungen
- Statistische Analysen über große Wertebereiche
- Batch-Processing von EABC-Klassifikationen
- Reproduzierbarkeit von Experimenten

### Lösung
Eine **ladbare, gecachte EABC-Testklasse** mit:

- **Lazy Generation:** Berechnung nur bei Bedarf
- **Persistent Caching:** Speicherung in HDF5-Datei
- **O(1) Lookup:** Schneller Zugriff auf vorberechnete Werte
- **Skalierbarkeit:** Bis n=10^7 (10 Millionen Einträge)

---

## 2. PERFORMANCE-ANALYSE

### Benchmark-Ergebnisse

```
Bereich               | Ø Zeit/Wert  | Ø Ω(n)
----------------------|--------------|-------
n = 2..100            | 0.010 ms     | 2.4
n = 100..10,000       | 0.026 ms     | 3.2
n = 10,000..100,000   | 0.053 ms     | 3.5
n = 100,000..1,000,000| 0.144 ms     | 3.7
```

### Hochrechnung für n=10^7

- **Gesamtzeit:** ~24 Minuten (vollständige Generierung)
- **Speicherbedarf:** ~760 MB (uncomprimiert)
- **Komprimiert (HDF5):** ~300-400 MB (geschätzt)

### Fazit
✓ Machbar für einmalige Generierung  
✓ Speicherbedarf moderat  
✓ Caching lohnt sich ab ~100 Berechnungen

---

## 3. DATENMODELL

### Pro Eintrag (n)

```python
{
    'n': int64,                    # Zahl selbst
    'omega': int32,                # Ω(n) - Anzahl Primfaktoren (mit Vielfachheit)
    'sigma': int64,                # σ(n) - Summe der Teiler
    'v2': int32,                   # v₂(n) - 2-adische Bewertung
    'v3': int32,                   # v₃(n) - 3-adische Bewertung
    'shell': int32,                # S(n) = v₂ + v₃
    'e': int32,                    # Anzahl E-Faktoren (≡ 1 mod 12)
    'a': int32,                    # Anzahl A-Faktoren (≡ 5 mod 12)
    'b': int32,                    # Anzahl B-Faktoren (≡ 7 mod 12)
    'c': int32,                    # Anzahl C-Faktoren (≡ 11 mod 12)
    'omega_eabc': int32,           # Ω_EABC = e + a + b + c
    'norm_sq': float64,            # ||v||² = e² + a² + b² + c²
    'H': float64,                  # H(n) - Konzentrationsmessung
    'eabc_signature': str (var),   # "EEAB" etc. (optional)
}
```

**Speicherbedarf pro Eintrag:** ~80 bytes (+ ~20 bytes für Signatur-String)

---

## 4. API-DESIGN

### 4.1 Haupt-Klasse: `EABCTestData`

```python
from eabc_test_data import EABCTestData

# Initialisierung mit Cache
data = EABCTestData(
    max_n=10**7,
    cache_file="eabc_cache.h5",
    auto_generate=False  # Lazy: nur bei Bedarf
)

# Single lookup (O(1))
eabc_vec = data.get_eabc(12345)          # → (e, a, b, c)
omega = data.get_omega(12345)            # → Ω(n)
H = data.get_concentration(12345)        # → H(n)
signature = data.get_signature(12345)    # → "EEAB"

# Batch lookup (effizient)
eabc_batch = data.get_eabc_batch([100, 200, 300])
coords_batch = data.get_coordinates_batch([100, 200, 300])

# Vollständige Koordinaten
coords = data.get_coordinates(12345)
# → {'omega': 5, 'e': 2, 'a': 1, 'b': 0, 'c': 0, 'H': 0.64, ...}
```

### 4.2 Generierung

```python
# Vollständige Generierung (einmalig)
from generate_eabc_cache import generate_cache

generate_cache(
    max_n=10**7,
    output_file="eabc_cache.h5",
    chunk_size=100_000,      # Speichere alle 100k Werte
    show_progress=True,      # Tqdm Progress-Bar
    compression='gzip'       # HDF5 Kompression
)
```

### 4.3 Inkrementelles Update

```python
# Cache erweitern (von 10^6 auf 10^7)
data.extend_cache(new_max_n=10**7)

# Einzelne Werte nachträglich hinzufügen
data.add_value(12345678)
```

---

## 5. STORAGE-FORMAT: HDF5

### Warum HDF5?

✓ Effiziente Kompression (gzip, lzf)  
✓ Inkrementelles Laden (nur benötigte Chunks)  
✓ Numpy-Integration  
✓ Wissenschafts-Standard  
✓ Selbst-beschreibend (Metadaten)

### HDF5-Struktur

```
eabc_cache.h5
├── metadata (attributes)
│   ├── max_n: 10000000
│   ├── version: "1.0"
│   ├── generated: "2026-06-24"
│   └── description: "EABC test data"
│
└── data (datasets)
    ├── n [10000000]              int64
    ├── omega [10000000]          int32
    ├── sigma [10000000]          int64
    ├── v2 [10000000]             int32
    ├── v3 [10000000]             int32
    ├── shell [10000000]          int32
    ├── e [10000000]              int32
    ├── a [10000000]              int32
    ├── b [10000000]              int32
    ├── c [10000000]              int32
    ├── omega_eabc [10000000]     int32
    ├── norm_sq [10000000]        float64
    ├── H [10000000]              float64
    └── eabc_signature [10000000] vlen string (optional)
```

### Alternative: NumPy .npz (einfacher, aber weniger flexibel)

```python
np.savez_compressed(
    'eabc_cache.npz',
    n=n_array,
    omega=omega_array,
    e=e_array,
    # ...
)
```

---

## 6. IMPLEMENTIERUNG

### 6.1 Kernkomponenten

```
code/utils/
├── eabc.py                  # Existing: Basis-Funktionen
├── eabc_test_data.py        # NEU: Klasse mit Cache-Logik
└── eabc_benchmark.py        # NEU: Performance-Tests

code/
└── generate_eabc_cache.py   # NEU: CLI-Tool für Generierung
```

### 6.2 Implementierungs-Checkliste

- [x] Performance-Benchmark (`eabc_benchmark.py`)
- [ ] Haupt-Klasse `EABCTestData` (`eabc_test_data.py`)
- [ ] Generierungs-Skript (`generate_eabc_cache.py`)
- [ ] Unit-Tests (`tests/test_eabc_cache.py`)
- [ ] Dokumentation (dieses Dokument)
- [ ] Beispiel-Notebook (`examples/eabc_cache_demo.ipynb`)

---

## 7. HURWITZ-QUATERNIONEN-ANALYSE

### Aktueller Stand

**Gibt es bereits eine Hurwitz/Quaternionen-Implementierung?**  
→ **NEIN.** Keine Implementierung gefunden.

**Wird EABC bereits auf ℍ (Quaternionen) abgebildet?**  
→ **NEIN.**

### Mathematischer Kontext

Die natürliche Einbettung wäre:

```
E → 1 (reale Einheit)
A → i (imaginäre Einheit 1)
B → j (imaginäre Einheit 2)
C → k (imaginäre Einheit 3)
```

mit der Quaternionen-Algebra ℍ:

```
i² = j² = k² = ijk = -1
```

**ABER:** Laut H10-Erkenntnis ist M_C derzeit **EABC-blind**. Eine Quaternionen-Repräsentation würde nur Sinn machen, wenn:

1. M_C EABC-sensitiv gemacht wird (siehe H10_INTERPRETATION_V3.md)
2. Die algebraische Struktur von EABC-Kombinationen untersucht wird

### Empfehlung für Tests

**Für die aktuelle Testinfrastruktur:**  
→ **NICHT notwendig.** Die EABC-Vektoren (e, a, b, c) als ℤ⁴-Tupel reichen vollständig.

**Für zukünftige Forschung (H12+):**  
→ Eine Quaternionen-Repräsentation könnte interessant sein für:
- EABC-sensitive Metriken
- Algebraische Invarianten
- Faktorisierungs-Geometrie in ℍ ⊂ 𝕆

---

## 8. USAGE-BEISPIELE

### Beispiel 1: Einfacher Lookup

```python
from utils.eabc_test_data import EABCTestData

# Lade Cache
data = EABCTestData(cache_file="eabc_cache.h5")

# Lookup
n = 30030  # = 2 × 3 × 5 × 7 × 11 × 13
coords = data.get_coordinates(n)

print(f"n = {n}")
print(f"Ω(n) = {coords['omega']}")
print(f"EABC = ({coords['e']}, {coords['a']}, {coords['b']}, {coords['c']})")
print(f"H(n) = {coords['H']:.4f}")
```

### Beispiel 2: Statistische Analyse

```python
import numpy as np
import matplotlib.pyplot as plt

# Lade Cache
data = EABCTestData(cache_file="eabc_cache.h5")

# Alle Werte bis 100,000
n_values = np.arange(2, 100_001)
H_values = data.get_concentration_batch(n_values)

# Plot
plt.figure(figsize=(12, 6))
plt.scatter(n_values, H_values, alpha=0.3, s=1)
plt.xlabel('n')
plt.ylabel('H(n)')
plt.title('Konzentrations-Messung H(n) für n = 2..100,000')
plt.grid(True, alpha=0.3)
plt.savefig('H_concentration_plot.png', dpi=300)
```

### Beispiel 3: Spezifische EABC-Signaturen finden

```python
# Finde alle Zahlen mit Signatur "EABC" (eine von jeder Klasse)
data = EABCTestData(cache_file="eabc_cache.h5")

results = []
for n in range(2, 100_000):
    coords = data.get_coordinates(n)
    if coords['e'] >= 1 and coords['a'] >= 1 and coords['b'] >= 1 and coords['c'] >= 1:
        # Prüfe, ob exakt eine von jeder Klasse
        if coords['omega_eabc'] == 4:
            results.append(n)

print(f"Gefunden: {len(results)} Zahlen mit EABC-Signatur '1111'")
print(f"Kleinste: {min(results)} = {data.get_signature(min(results))}")
```

---

## 9. TESTS & VALIDIERUNG

### Unit-Tests

```python
# tests/test_eabc_cache.py

def test_cache_consistency():
    """Prüfe: Cache-Werte = direkte Berechnung."""
    data = EABCTestData(cache_file="test_cache.h5")
    
    for n in [60, 210, 2310, 30030]:
        cached = data.get_coordinates(n)
        direct = compute_svn_coordinates(n)  # Original-Funktion
        
        assert cached['omega'] == direct['omega']
        assert cached['e'] == direct['e']
        assert np.isclose(cached['H'], direct['H'])

def test_batch_efficiency():
    """Prüfe: Batch ist schneller als einzeln."""
    data = EABCTestData(cache_file="eabc_cache.h5")
    
    n_values = np.arange(1000, 2000)
    
    # Einzeln
    start = time.time()
    for n in n_values:
        _ = data.get_omega(n)
    time_single = time.time() - start
    
    # Batch
    start = time.time()
    _ = data.get_omega_batch(n_values)
    time_batch = time.time() - start
    
    assert time_batch < time_single * 0.5  # Mindestens 2× schneller
```

---

## 10. NÄCHSTE SCHRITTE

### Phase 1: Basis-Implementierung (Heute)
- [x] Performance-Analyse
- [x] Design-Dokument
- [ ] `eabc_test_data.py` implementieren
- [ ] `generate_eabc_cache.py` implementieren
- [ ] Cache für n=10^5 generieren (Test)

### Phase 2: Vollständiger Cache (Optional)
- [ ] Cache für n=10^7 generieren (~24 min)
- [ ] Kompression optimieren
- [ ] Benchmark-Vergleich (cached vs. uncached)

### Phase 3: Integration (Optional)
- [ ] Bestehende Experimente auf Cache umstellen
- [ ] Beispiel-Notebook erstellen
- [ ] Performance-Dokumentation

### Phase 4: Erweiterte Features (Zukunft)
- [ ] EABC-sensitive M_C-Metriken (siehe H10)
- [ ] Quaternionen-Repräsentation (für H12+)
- [ ] SQL-Interface für komplexe Queries
- [ ] Cloud-Storage für geteilte Caches

---

## 11. REFERENZEN

### Interne Dokumente
- `code/utils/eabc.py` - Basis-Implementierung
- `experiments/results/h10_final/H10_INTERPRETATION_V3.md` - M_C ist EABC-blind
- `code/experiments/comparison_n1_100.py` - Beispiel für Batch-Verarbeitung

### Externe Libraries
- h5py (HDF5 für Python)
- numpy (numerische Arrays)
- tqdm (Progress-Bars)
- pytest (Testing)

---

**Ende des Design-Dokuments**
