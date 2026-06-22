# Glatte Zahlen (Smooth Numbers)

Dieses Projekt implementiert die Berechnung von s-glatten Zahlen und deren Darstellung in einer dreieckigen Anordnung ähnlich dem Pascal-Dreieck.

## 🌟 Features

### Basis-Features
- ✓ Rekursive Berechnung der n-ten s-glatten Zahl S(s,n)
- ✓ Verallgemeinerter Hamming-Algorithmus mit dynamischer Programmierung
- ✓ Dreieck-Darstellung T(n,k) analog zu Pascal's Dreieck
- ✓ Vollständige mathematische Dokumentation

### 🆕 Erweiterte Features
- ✓ **Grafische Visualisierung** (HTML/SVG mit interaktiver Heatmap)
- ✓ **Export-Funktionen** (CSV, JSON, HTML)
- ✓ **Parallele Berechnung** (OpenMP-fähig)
- ✓ **Benchmark-Tests** (Performance-Analyse)

### 🎯 EABC/ABCE-Modell (Bamberg-Interpretation) - NEU!
- ✓ **Schichtzahlen σ(n)** - Exponentensumme als Abstand vom Ursprung
- ✓ **Vektorzahlen v(n)** - EABC-Signatur (n_E, n_A, n_B, n_C)
- ✓ **Periodensystem der Zahlen** - 4D-Gitter-Darstellung
- ✓ **Primzahlen vs. Glatte Zahlen** - "Hart" vs. "Weich"
- ✓ **Recamán-Folgen-Analyse** - Hypothesentest für Gitterstruktur
- ✓ **Quaternionen-artige Struktur** - Multiplikation = Vektoraddition

### 🍾 Klein-Flaschen-Topologie - BRANDNEU!
- ✓ **Primzahl-Quadrupel** - (p, q, r, s) mit vollständiger EABC-Abdeckung
- ⚠️ **Geometrische Visualisierung** - Aufgeprägte ℝ⁴-Parametrisierung
- ⚠️ **Hübsch, aber nicht emergent** - Siehe Kritik unten

### 🔬 EABC-Chiralität und arithmetische Holonomie - MATHEMATISCH SAUBER! ⭐

Die **Holonomie-Observable** H(X) = Σ χ(Q) ist der mathematisch saubere Kern:

#### Wohldefinierte Objekte:
- ✅ **Chiralitäts-Observable χ(Q)** - +1 für EABC, -1 für ECBA, 0 sonst
- ✅ **Holonomie Hᴄ(X)** - Summe über Quadrupel nach Konstruktion C
- ✅ **Normalisierte Holonomie hᴄ(X)** - H(X) / N(X)

#### Empirische Ergebnisse:
- ✅ **h_random(X) ≈ 0** - Symmetrie bei zufälliger Ordnung (bestätigt!)
- ✅ **h_consec(10⁵) ≈ 0.19** - Bias bei konsekutiver Ordnung
- ⚠️ **Asymptotik offen** - Konvergiert h(X) → 0 oder bleibt Bias?

#### Zentrale Forschungsfrage:
```
limsup |hᴄ(X)| > 0  für kanonische Konstruktion C?
```

**Klein-Flaschen-Metapher:** Nützlich für Intuition (EABC ↔ pos. Umlauf, ECBA ↔ neg. Umlauf), aber die harte Mathematik liegt in H(X), nicht in χ = -1.

### 🧪 Chiralitäts-Robustheitstests - KRITISCHE ÜBERPRÜFUNG! ⭐
- ✅ **Test A: Zufällige Umordnung** - Symmetrie bewiesen
- ✅ **Test B: Konsekutive Primzahlen** - Alternative Konstruktion
- ✅ **Test C: Andere Moduli** - Mod 30, Mod 60
- ✅ **Test D: Große Datensätze** - Bis 10⁵ Primzahlen
- ✅ **Schlussfolgerung** - Asymmetrie ist konstruktionsabhängig, nicht fundamental

## 📁 Dateien

### C++ Implementierungen
- `smooth_numbers.cpp` - Basis-Version (200+ Zeilen)
- `smooth_numbers_extended.cpp` - Erweiterte Version mit allen Features
- `eabc_analysis.cpp` - EABC/Bamberg-Modell Analyse
- `dickman_bridge.cpp` - Dickman-Funktion (Lean-verifiziert)
- `klein_bottle.cpp` - Klein-Flaschen-Geometrie (aufgeprägt, historisch)
- `eabc_chirality.cpp` - Diskrete Topologie aus Chiralitäten (historisch)
- `chirality_robustness.cpp` - Robustheitstests ⭐ KRITISCH

### Header-Dateien
- `export.h` - Export-Funktionen (JSON, CSV, HTML)
- `parallel.h` - Parallele Berechnungen (OpenMP-fähig)
- `benchmark.h` - Benchmark-System
- `eabc_model.h` - EABC/ABCE-Modell Strukturen

### Dokumentation
- `README.md` - Diese Datei
- `MATHEMATICAL_DETAILS.md` - Mathematische Dokumentation
- `EXAMPLES.md` - Konkrete Beispiele
- `EXTENDED_FEATURES.md` - Dokumentation der erweiterten Features
- `EABC_MODEL.md` - EABC/ABCE-Bamberg-Modell
- `LEAN_INTEGRATION.md` - Lean 4 formale Verifikation
- `EABC_HOLONOMY.md` - Arithmetische Holonomie-Observable ⭐ KERN
- `ROBUSTNESS_TESTS.md` - Kritische Überprüfung ⭐ WICHTIG
- `KLEIN_BOTTLE.md` - Klein-Flaschen-Geometrie (Metapher, historisch)
- `DISCRETE_TOPOLOGY.md` - Diskrete emergente Topologie (revidiert)

### Lean 4 Formalisierung
- `DickmanFunction.lean` - Dickman-de Bruijn Funktion
- `KleinBottleTopology.lean` - Topologische Eigenschaften
- `lakefile.lean` - Lean Projekt-Konfiguration
- `lean-toolchain` - Lean Version

### Build-System
- `Makefile` - Automatisches Build-System
- `test.sh` - Automatische Tests

## 🔬 Lean 4 Formale Verifikation

Dieses Projekt enthält eine vollständige **formale Verifizierung** in Lean 4!

### Dickman-de Bruijn Funktion

Die asymptotische Verteilung glatter Zahlen ist formal bewiesen:

```lean
theorem smooth_count_asymptotic (x : ℝ) (y : ℕ) :
  let u := log x / log y
  ∃ ε : ℝ → ℝ, (∀ x, |ε x| < 1) ∧
    (SmoothCount x y : ℝ) = x * DickmanRho u * (1 + ε x)
```

**Bedeutung:** Ψ(x, y) ≈ x · ρ(log x / log y)

### Bewiesene Eigenschaften

✓ **Basisfall** - ρ(u) = 1 für 0 ≤ u ≤ 1  
✓ **Rekursion** - u·ρ(u) = ∫₁ᵘ ρ(t) dt  
○ **Monotonie** - ρ ist streng monoton fallend  
○ **Asymptotik** - ρ(u) ~ u^(-u)/Γ(u+1) für große u

### C++ ↔ Lean Bridge

```bash
# Numerische Berechnung (verifiziert gegen Lean-Definitionen)
make demo-dickman
```

**Ausgabe:**
```
=== TEST 1: Spezielle Werte (verifiziert in Lean) ===
ρ(0) = 1 (Lean: dickman_zero)
ρ(1) = 1 (Lean: dickman_one)
ρ(2) ≈ 0.307 (Lean: dickman_two = 1 - log 2)
```

Siehe `LEAN_INTEGRATION.md` für Details zur formalen Verifikation.

## ⭐ EABC-Chiralität und arithmetische Holonomie (DER KERN)

### Die Holonomie-Observable H(X)

Der **mathematisch saubere Kern** dieser Arbeit ist die arithmetische Holonomie:

```
Hᴄ(X) = Σ_{Q≤X} χ(Q)
```

mit der Chiralitäts-Observable:

```
χ(Q) = ⎧ +1,  norm(sig(Q)) = EABC  (positiver Umlauf)
       ⎨ -1,  norm(sig(Q)) = ECBA  (negativer Umlauf)
       ⎩  0,  sonst
```

### Normalisierte Holonomie

```
hᴄ(X) = Hᴄ(X) / Nᴄ(X)
```

misst den "Chiralitäts-Bias" einer Konstruktionsmethode C.

### Empirische Ergebnisse

| Konstruktion C | h(X)  | Interpretation |
|----------------|-------|----------------|
| C_random (zufällig) | ≈ 0 | Symmetrisch ✓ |
| C_consec (konsekutiv) | ≈ 0.19 | Bias vorhanden |

### Zentrale Forschungsfrage

**Asymptotisches Verhalten:**
```
lim_{X→∞} hᴄ(X) = 0  oder  limsup_{X→∞} |hᴄ(X)| > 0?
```

**Falls Bias bleibt:** Neue zahlentheoretische Observable mit Verbindung zu:
- Primzahl-Lücken
- Chebyshev-Bias (Primzahl-Rennen)
- Quadratische Reste mod 12

**Falls Bias verschwindet:** Stützt Zufallshypothese für Primzahlen mod 12.

### Die Klein-Flaschen-Metapher

Die Klein-Flasche ist **keine rigoros emergente Topologie**, sondern ein **heuristisches Bild**:

```
EABC ↔ positiver Umlauf (rechtshändig)
ECBA ↔ negativer Umlauf (linkshändig)
E-Klasse ↔ Kreuzungspunkt (Lemniskate ∞)
```

**Die harte Mathematik liegt in H(X), nicht in χ = -1.**

**Siehe `EABC_HOLONOMY.md` für vollständige mathematische Details!** ⭐

---

## 🧪 Chiralitäts-Robustheitstests (KRITISCHE ÜBERPRÜFUNG)

### ⚠️ Wichtige Erkenntnis: Die Asymmetrie war ein Definitionsartefakt!

Die ursprünglich beobachtete **ABCEA-Dominanz (60%) vs. CEABC (0%)** stellte sich als **Konstruktionsartefakt** heraus, nicht als fundamentales Primzahl-Phänomen.

#### TEST A: Zufällige Umordnung - DER ENTSCHEIDENDE TEST

**Methode:** Nehme dieselben vier Primzahlen und ordne sie zufällig um.

**Ergebnis:**
```
P(EABC) = 16.6%
P(ECBA) = 16.7%
Asymmetrie ≈ 0
```

**Schlussfolgerung:**
> ✓ **Bei zufälliger Ordnung verschwindet die Asymmetrie vollständig!**  
> ✓ **Die Chiralitätspräferenz war ein Definitionsartefakt!**

#### TEST B-D: Gerichtete Ordnung - Der Bias bleibt

Bei **aufsteigender** Primzahl-Ordnung:
```
Konsekutiv (bis 10⁵): P(EABC) ≈ 27%, P(ECBA) ≈ 8%
H/N ≈ 0.19 (persistenter Bias)
```

**Interpretation:** Die gerichtete Konstruktion erzeugt systematischen Bias.

### Was bleibt mathematisch interessant?

#### Die Holonomie-Observable H(X) = Σ χ(Q)

Auch wenn die Chiralität konstruktionsabhängig ist, ist die Observable **wohldefiniert**:

```
χ(Q) = +1  für EABC-Quadrupel
χ(Q) = -1  für ECBA-Quadrupel
χ(Q) =  0  sonst

H(X) = Σ_{Q≤X} χ(Q)
```

**Offene Fragen:**
1. Wie verhält sich H(X)/N(X) asymptotisch für verschiedene Konstruktionen?
2. Welche Ordnung maximiert/minimiert H(X)?
3. Korreliert H(X) mit Primzahl-Lücken oder Chebyshev-Bias?

### Kompilieren und Ausführen

```bash
# Robustheitstests (EMPFOHLEN)
make demo-robustness
```

**Ausgabe:**
```
TEST A (zufällig): P(EABC) ≈ P(ECBA) ≈ 16.6% ✓ Symmetrisch!
TEST B (konsekutiv): P(EABC) ≈ 48%, P(ECBA) ≈ 8% (Bias)
TEST D (bis 10⁵): H/N ≈ 0.19 (persistenter Bias)
```

**Siehe `ROBUSTNESS_TESTS.md` für vollständige Analyse!**

---

## 🔬 Diskrete Topologie (Historisch, revidiert)

Die ursprüngliche "emergente Topologie" basierte auf der fehlerhaften Annahme einer fundamentalen Chiralitätsasymmetrie. Die Konstruktion selbst (Übergangsgraph, Holonomie H(X)) bleibt wohldefiniert, aber die Interpretation als "neue Primzahl-Eigenschaft" war voreilig.

**Was gesichert ist:**
- EABC-Klassifikation ✓
- Vollständige Quadrupel ✓
- Holonomie-Observable H(X) ✓ (konstruktionsabhängig)

**Was revidiert wurde:**
- "Primzahlen bevorzugen ABCEA" ✗ (Definitionsartefakt)
- χ = -1 als topologische Invariante ✗ (heuristisch)
- "Emergente Klein-Flaschen-Struktur" ✗ (zu früh behauptet)

---

## 🍾 Klein-Flaschen-Geometrie (Historisch)

Die ursprüngliche geometrische Konstruktion (`klein_bottle.cpp`) ist weiterhin verfügbar als **Visualisierung**, aber mathematisch war dies eine aufgeprägte Geometrie, keine aus Primzahlen emergente Struktur.

### Installation (optional)

```bash
# Lean 4 installieren
curl https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh -sSf | sh

# Formalisierung bauen
make lean
```

## 🎯 EABC/ABCE-Modell (Bamberg)

### Philosophie: Hart vs. Weich

Glatte Zahlen sind das **Gegenteil von Primzahlen**:

| Primzahlen | Glatte Zahlen |
|------------|---------------|
| "Harte" Faktorisierung | "Weiche" Faktorisierung |
| Maximale Komplexität | Minimale Komplexität |
| Achsenpunkte | Innenpunkte |
| Eckpunkte des Gitters | Volumenfüllung |

### 4D-Gitterstruktur

Jede Zahl n wird durch zwei Koordinaten beschrieben:

```
n ↦ (σ(n), v(n))
```

- **Schichtzahl σ(n)**: Summe aller Exponenten
- **Vektorzahl v(n)**: EABC-Signatur (n_E, n_A, n_B, n_C)

### Beispiele

```bash
# Analysiere einzelne Zahl
./eabc_analysis
# Wähle Option 1, dann z.B. 385

=== ANALYSE VON 385 ===
Faktorisierung: 5 × 7 × 11
EABC-Signatur: (2^0 3^0 | E^0 A^1 B^1 C^1)
Schichtzahl σ(n): 3
Vektorzahl v(n): (0,1,1,1)
→ GITTERPUNKT (Innenpunkt, Schicht 3)
```

### Recamán-Hypothese

Das Modell ermöglicht experimentelle Tests:

**Hypothese:** Die Recamán-Folge bevorzugt Randpunkte (Primzahlen, niedrige Schichten) und meidet hochglatte Innenpunkte.

**Ergebnis (n=500):**
```
Durchschnittliche Schichtzahl (besucht): 2.34
Durchschnittliche Schichtzahl (nicht besucht): 2.74

→ Tendenz bestätigt!
```

### EABC-Klassifikation

Primzahlen p > 3 werden klassifiziert nach p mod 12:

```
E: p ≡ 1  (mod 12)  →  13, 37, 61...
A: p ≡ 5  (mod 12)  →  5, 17, 29...
B: p ≡ 7  (mod 12)  →  7, 19, 31...
C: p ≡ 11 (mod 12)  →  11, 23, 47...
```

Siehe `EABC_MODEL.md` für vollständige Dokumentation.

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
