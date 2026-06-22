# Glatte Zahlen (Smooth Numbers)

Dieses Projekt implementiert die Berechnung von s-glatten Zahlen und deren Darstellung in einer dreieckigen Anordnung ähnlich dem Pascal-Dreieck.

## 🌟 Features

### Basis-Features
- ✓ Rekursive Berechnung der n-ten s-glatten Zahl S(s,n)
- ✓ Verallgemeinerter Hamming-Algorithmus mit dynamischer Programmierung
- ✓ Dreieck-Darstellung T(n,k) analog zu Pascal's Dreieck
- ✓ Vollständige mathematische Dokumentation

### 🆕 Erweiterte Features (NEU!)
- ✓ **Grafische Visualisierung** (HTML/SVG mit interaktiver Heatmap)
- ✓ **Export-Funktionen** (CSV, JSON, HTML)
- ✓ **Parallele Berechnung** (OpenMP-fähig)
- ✓ **Benchmark-Tests** (Performance-Analyse)

## 📁 Dateien

- `smooth_numbers.cpp` - Basis-Version (200+ Zeilen)
- `smooth_numbers_extended.cpp` - Erweiterte Version mit allen Features
- `export.h` - Export-Funktionen (JSON, CSV, HTML)
- `parallel.h` - Parallele Berechnungen (OpenMP-fähig)
- `benchmark.h` - Benchmark-System
- `README.md` - Diese Datei
- `MATHEMATICAL_DETAILS.md` - Mathematische Dokumentation
- `EXAMPLES.md` - Konkrete Beispiele
- `EXTENDED_FEATURES.md` - Dokumentation der erweiterten Features

### Definition

Eine **s-glatte Zahl** (oder p_s-glatte Zahl) ist eine positive ganze Zahl, deren Primfaktoren alle kleiner oder gleich der s-ten Primzahl p_s sind.

**Beispiele:**
- 2-glatte Zahlen (p₂=3): 1, 2, 3, 4, 6, 8, 9, 12, 16, 18, ...
- 3-glatte Zahlen (p₃=5): 1, 2, 3, 4, 5, 6, 8, 9, 10, 12, 15, ... (Hamming-Zahlen)
- 8-glatte Zahlen (p₈=19): Alle Zahlen mit Primfaktoren ≤ 19

### Rekursive Formel

Die n-te s-glatte Zahl S(s, n) kann rekursiv berechnet werden:

```
S(s, 1) = 1
S(s, n) = min{S(s, i) × p_j | i < n, j ≤ s, S(s,i) × p_j > S(s, n-1)}
```

wobei p_j die j-te Primzahl ist (p₁=2, p₂=3, p₃=5, ...).

### Algorithmus (Verallgemeinerter Hamming-Algorithmus)

Der Algorithmus verwendet dynamische Programmierung:

1. Initialisiere S(s, 1) = 1
2. Führe für jede Primzahl p_j einen Index i_j
3. Berechne für jede Position n:
   - Kandidaten: S(s, i_j) × p_j für alle j ≤ s
   - S(s, n) = min(alle Kandidaten)
   - Erhöhe i_j für alle j, wo S(s, i_j) × p_j = S(s, n)

**Komplexität:** O(n × s)

### Dreieck-Darstellung

Das Dreieck T(n, k) zählt die Anzahl der k-glatten Zahlen ≤ n:

```
T(n, k) = #{m | m ≤ n, P(m) ≤ k}
```

wobei P(m) der größte Primfaktor von m ist.

**Rekursive Relation (Buchstab-Identität):**

```
Ψ(x, y) = Ψ(x, 2) + Σ(2<p≤y) Ψ(x/p, p)
```

## 🚀 Schnellstart

### Basis-Version

```bash
# Kompilieren
make basic

# Ausführen
./smooth_numbers
```

### Erweiterte Version

```bash
# Kompilieren
make extended

# Vollständige Demo ausführen
make demo

# Oder manuell
./smooth_numbers_extended
# Wählen Sie Option 6 für alle Demos
```

### Kompilierung und Ausführung

### Voraussetzungen
- C++11 oder höher
- g++ oder clang++

### Kompilieren

```bash
# Mit g++
g++ -std=c++11 -O2 -o smooth_numbers smooth_numbers.cpp

# Mit clang++
clang++ -std=c++11 -O2 -o smooth_numbers smooth_numbers.cpp

# Mit Makefile
make
```

### Ausführen

```bash
./smooth_numbers
```

## Programmfunktionen

Das Programm demonstriert:

1. **Hamming-Zahlen (s=3):** Die klassischen 3-glatten Zahlen mit Primfaktoren {2, 3, 5}
2. **5-glatte Zahlen (s=5):** Primfaktoren {2, 3, 5, 7, 11}
3. **8-glatte Zahlen (s=8):** Primfaktoren {2, 3, 5, 7, 11, 13, 17, 19}
4. **Dreieck-Darstellung:** Analog zum Pascal-Dreieck
5. **Interaktive Berechnung:** Eigene Werte für s und n eingeben

## Beispielausgabe

```
=== S-GLATTE ZAHLEN (s = 3) ===
Erlaubte Primzahlen: 2, 3, 5

Die ersten 20 3-glatten Zahlen:
S(3, 1) = 1, S(3, 2) = 2, S(3, 3) = 3, S(3, 4) = 4, S(3, 5) = 5
S(3, 6) = 6, S(3, 7) = 8, S(3, 8) = 9, S(3, 9) = 10, S(3, 10) = 12
S(3, 11) = 15, S(3, 12) = 16, S(3, 13) = 18, S(3, 14) = 20, S(3, 15) = 24
S(3, 16) = 25, S(3, 17) = 27, S(3, 18) = 30, S(3, 19) = 32, S(3, 20) = 36

=== GLATT-DREIECK ===
T(n,k) = Anzahl der k-glatten Zahlen <= n

n\k    1   2   3   4   5   6   7   8   9  10
-----------------------------------------------
  1    1   1   1   1   1   1   1   1   1   1
  2    1   2   2   2   2   2   2   2   2   2
  3    1   2   3   3   3   3   3   3   3   3
  4    1   3   4   4   4   4   4   4   4   4
  5    1   3   5   5   5   5   5   5   5   5
  6    1   4   6   6   6   6   6   6   6   6
```

## Anwendungen

Glatte Zahlen haben wichtige Anwendungen in:

- **Kryptographie:** Integer-Faktorisierung und diskrete Logarithmen
- **Algorithmik:** FFT-Algorithmen (Fast Fourier Transform)
- **Zahlentheorie:** Analyse von Primfaktorzerlegungen
- **Computergrafik:** Effiziente Bildauflösungen

## Mathematische Hintergründe

### Dickman-de Bruijn Funktion ρ(u)

Für große x und festes u = log x / log y gilt:

```
Ψ(x, y) ≈ x · ρ(u)
```

wobei ρ(u) die Dickman-Funktion ist, definiert durch:

```
ρ(u) = 1                    für 0 ≤ u ≤ 1
u·ρ(u) = ∫₁ᵘ ρ(t) dt       für u > 1
```

### Referenzen

- Dickman, K. (1930): "On the frequency of numbers containing prime factors of a certain relative magnitude"
- de Bruijn, N. G. (1951): "On the number of positive integers ≤ x and free of prime factors > y"
- Bernstein, D. J. (2004): "How to find smooth parts of integers"
- OEIS Sequence A080786: Triangle of smooth number counts

## Lizenz

Dieses Projekt steht zur freien Verfügung für Bildungs- und Forschungszwecke.
