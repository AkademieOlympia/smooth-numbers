# Mathematische Dokumentation: Rekursive Formel für s-glatte Zahlen

## 1. Grundlegende Definitionen

### 1.1 s-glatte Zahlen

**Definition:** Eine positive ganze Zahl n ist **s-glatt** (oder p_s-glatt), wenn alle ihre Primfaktoren kleiner oder gleich der s-ten Primzahl p_s sind.

Formal: n ist s-glatt ⟺ P(n) ≤ p_s

wobei P(n) der größte Primfaktor von n ist und p_s die s-te Primzahl bezeichnet:
- p₁ = 2
- p₂ = 3
- p₃ = 5
- p₄ = 7
- p₅ = 11
- ...

### 1.2 Darstellung

Jede s-glatte Zahl kann eindeutig dargestellt werden als:

n = p₁^(a₁) × p₂^(a₂) × ... × p_s^(a_s)

wobei a₁, a₂, ..., a_s ≥ 0 nicht-negative ganze Zahlen sind.

## 2. Rekursive Formel S(s, n)

### 2.1 Definition von S(s, n)

S(s, n) bezeichnet die n-te s-glatte Zahl in aufsteigender Reihenfolge.

**Basisfall:**
```
S(s, 1) = 1  für alle s ≥ 1
```

**Rekursionsschritt:**
```
S(s, n) = min{S(s, i) × p_j | 1 ≤ i < n, 1 ≤ j ≤ s, S(s, i) × p_j > S(s, n-1)}
```

### 2.2 Intuition

Die Rekursion basiert auf der Beobachtung:
- Wenn m eine s-glatte Zahl ist, dann ist auch m × p_j eine s-glatte Zahl für jede Primzahl p_j ≤ p_s
- Alle s-glatten Zahlen können durch wiederholte Multiplikation mit den ersten s Primzahlen erzeugt werden
- Die n-te s-glatte Zahl ist das Minimum aller Kandidaten, die größer als die (n-1)-te s-glatte Zahl sind

### 2.3 Beispiel: Hamming-Zahlen (s = 3)

Für s = 3 haben wir p₁ = 2, p₂ = 3, p₃ = 5.

Berechnung:
```
S(3, 1) = 1

S(3, 2) = min{1×2, 1×3, 1×5} = 2

S(3, 3) = min{1×3, 1×5, 2×2, 2×3, 2×5} \ {≤2} = 3

S(3, 4) = min{1×5, 2×2, 2×3, 2×5, 3×2, 3×3, 3×5} \ {≤3} = 4

S(3, 5) = min{1×5, 2×3, 2×5, 3×2, 3×3, 3×5, 4×2, 4×3, 4×5} \ {≤4} = 5

S(3, 6) = min{2×3, 2×5, 3×2, 3×3, 3×5, 4×2, 4×3, 4×5, 5×2, 5×3, 5×5} \ {≤5} = 6
```

Sequenz: 1, 2, 3, 4, 5, 6, 8, 9, 10, 12, 15, 16, 18, 20, 24, 25, 27, 30, ...

## 3. Effiziente Berechnung: Dynamische Programmierung

### 3.1 Algorithmus (Verallgemeinerter Dijkstra-Hamming)

Der naive Ansatz würde bei jedem Schritt alle vorherigen Zahlen mit allen Primzahlen multiplizieren. Dies ist ineffizient.

**Optimierter Algorithmus:**

```
Eingabe: s (Anzahl Primzahlen), n (Anzahl zu berechnender Zahlen)
Ausgabe: Array S[1..n] mit den ersten n s-glatten Zahlen

1. Generiere Primzahlen p₁, p₂, ..., p_s
2. Initialisiere:
   - S[1] ← 1
   - Für j = 1 bis s: index[j] ← 1
   - Für j = 1 bis s: next[j] ← p_j

3. Für i = 2 bis n:
   a. S[i] ← min{next[1], next[2], ..., next[s]}
   
   b. Für j = 1 bis s:
      Wenn next[j] = S[i]:
         index[j] ← index[j] + 1
         next[j] ← S[index[j]] × p_j
```

### 3.2 Invarianten

Der Algorithmus erhält folgende Invarianten:
1. S[1..i] enthält die ersten i s-glatten Zahlen in aufsteigender Reihenfolge
2. next[j] = S[index[j]] × p_j
3. next[j] ist die kleinste Zahl der Form S[k] × p_j, die noch nicht in S erschienen ist

### 3.3 Komplexität

- **Zeitkomplexität:** O(n × s)
  - n Iterationen
  - Pro Iteration: O(s) für das Finden des Minimums

- **Raumkomplexität:** O(n + s)
  - O(n) für das Array S
  - O(s) für die Hilfsarrays index und next

## 4. Dreieck-Darstellung T(n, k)

### 4.1 Definition

T(n, k) := Anzahl der k-glatten Zahlen ≤ n

Mit anderen Worten:
```
T(n, k) = #{m ∈ ℕ | 1 ≤ m ≤ n und P(m) ≤ k}
```

### 4.2 Eigenschaften

**Monotonie:**
- T(n, k) ≤ T(n+1, k)  (mehr Zahlen → mehr glatte Zahlen)
- T(n, k) ≤ T(n, k+1)  (mehr Primzahlen erlaubt → mehr glatte Zahlen)

**Randwerte:**
- T(n, 1) = 1 für alle n ≥ 1  (nur die Zahl 1 ist 1-glatt)
- T(1, k) = 1 für alle k ≥ 1  (nur die Zahl 1 ist ≤ 1)
- T(n, n) = n für n Primzahl  (alle Zahlen ≤ n sind n-glatt)

**Asymptotik:**
- T(n, n) = n für große n

### 4.3 Rekursive Relation (Buchstab-Identität)

Für die Zählfunktion Ψ(x, y) (Anzahl der y-glatten Zahlen ≤ x) gilt:

```
Ψ(x, y) = 1 + Σ(p≤y, p prim) Ψ(⌊x/p⌋, p)
```

**Beweis-Skizze:**
- Partitioniere die y-glatten Zahlen ≤ x nach ihrem größten Primfaktor p
- Wenn p der größte Primfaktor von n ist, dann ist n/p eine p-glatte Zahl ≤ x/p
- Die 1 steht für die Zahl 1 selbst (die keinen Primfaktor hat)

### 4.4 Dreieck-Struktur

```
n\k    1   2   3   4   5   6   7
----------------------------------
  1    1   1   1   1   1   1   1
  2    1   2   2   2   2   2   2
  3    1   2   3   3   3   3   3
  4    1   3   4   4   4   4   4
  5    1   3   4   4   5   5   5
  6    1   3   5   5   6   6   6
  7    1   3   5   5   6   6   7
  8    1   4   6   6   7   7   8
```

**Interpretation:**
- Zeile n: Anzahl der k-glatten Zahlen für verschiedene k, jeweils ≤ n
- Spalte k: Wachstum der Anzahl k-glatter Zahlen mit wachsendem n

## 5. Vergleich mit Pascal's Dreieck

### 5.1 Ähnlichkeiten

| Pascal's Dreieck | Glatt-Dreieck |
|------------------|---------------|
| Binomialkoeffizienten C(n,k) | Zählfunktion T(n,k) |
| Symmetrisch: C(n,k) = C(n,n-k) | Nicht symmetrisch |
| Rekursion: C(n,k) = C(n-1,k-1) + C(n-1,k) | Rekursion: Buchstab-Identität |
| Summe Zeile n: 2^n | Summe Zeile n: variabel |

### 5.2 Unterschiede

Das Glatt-Dreieck ist **nicht symmetrisch**, da:
- T(n, k) hängt von Primzahleigenschaften ab
- T(n, 2) zählt nur 2-glatte Zahlen (Zweierpotenzen und ihre Vielfachen mit 3)
- T(n, k) konvergiert gegen n für große k

## 6. Anwendungen

### 6.1 FFT-Algorithmen

Fast Fourier Transform-Algorithmen profitieren von glatten Zahlen:
- FFT zerlegt Problem der Größe n in Teilprobleme der Größe seiner Faktoren
- Glatte n garantieren kleine Faktoren
- Effiziente Berechnung möglich

### 6.2 Kryptographie

- Integer-Faktorisierung verwendet glatte Zahlen
- B-smooth numbers in Quadratic Sieve
- Pollard's p-1 Algorithmus

### 6.3 Zahlentheorie

- Studium der Verteilung von glatten Zahlen
- Dickman-de Bruijn-Funktion ρ(u)
- Asymptotische Dichte glatter Zahlen

## 7. Offene Fragen und Weiterführendes

### 7.1 Dickman-de Bruijn Funktion

Für u = log x / log y gilt asymptotisch:

```
Ψ(x, y) ≈ x · ρ(u)
```

wobei ρ(u) definiert ist durch:
```
ρ(u) = 1                    für 0 ≤ u ≤ 1
u·ρ'(u) + ρ(u-1) = 0       für u > 1
```

### 7.2 Verteilung

Für festes u > 1 und x → ∞:
```
ρ(u) ≈ u^(-u) / Γ(u+1)
```

### 7.3 Komplexitätsfragen

- Schnellste Berechnung von Ψ(x, y)?
- Effiziente Enumeration der s-glatten Zahlen in Intervallen?
- Primzahltest für glatte Zahlen?

## 8. Literatur

1. **Dickman, K.** (1930): "On the frequency of numbers containing prime factors of a certain relative magnitude", Ark. Mat. Astr. Fys. 22

2. **de Bruijn, N. G.** (1951): "On the number of positive integers ≤ x and free of prime factors > y", Nederl. Akad. Wetensch. Proc. Ser. A 54

3. **Bernstein, D. J.** (2004): "How to find smooth parts of integers", http://cr.yp.to/papers.html

4. **Granville, A.** (2008): "Smooth numbers: computational number theory and beyond", Algorithmic Number Theory

5. **OEIS** Sequence A080786: Triangle T(n,k) = number of k-smooth numbers <= n

## 9. Implementierungshinweise

### 9.1 Optimierungen

1. **Sieb für Primzahlen:** Verwende Sieb des Eratosthenes für große s
2. **Heap-basiert:** Verwende Priority Queue für sehr große n
3. **Bereichsabfragen:** Segment-Tree für T(n, k) Bereichsabfragen

### 9.2 Numerische Stabilität

- Verwende `long long` oder `__int128` für große Zahlen
- Beachte Überlauf bei Multiplikation
- Eventuell GMP (GNU Multiple Precision) für sehr große s-glatte Zahlen

### 9.3 Parallelisierung

- Berechnung verschiedener s-Werte parallel
- Batch-Berechnung mehrerer T(n, k)-Werte
