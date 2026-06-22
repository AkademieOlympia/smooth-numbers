# Beispiele und Visualisierungen

## Beispiel 1: Hamming-Zahlen (s = 3)

### Primzahlen
p₁ = 2, p₂ = 3, p₃ = 5

### Sequenz der ersten 30 Hamming-Zahlen
```
 n  |  S(3, n)  | Faktorisierung
----|-----------|------------------
  1 |     1     | 1
  2 |     2     | 2
  3 |     3     | 3
  4 |     4     | 2²
  5 |     5     | 5
  6 |     6     | 2·3
  7 |     8     | 2³
  8 |     9     | 3²
  9 |    10     | 2·5
 10 |    12     | 2²·3
 11 |    15     | 3·5
 12 |    16     | 2⁴
 13 |    18     | 2·3²
 14 |    20     | 2²·5
 15 |    24     | 2³·3
 16 |    25     | 5²
 17 |    27     | 3³
 18 |    30     | 2·3·5
 19 |    32     | 2⁵
 20 |    36     | 2²·3²
 21 |    40     | 2³·5
 22 |    45     | 3²·5
 23 |    48     | 2⁴·3
 24 |    50     | 2·5²
 25 |    54     | 2·3³
 26 |    60     | 2²·3·5
 27 |    64     | 2⁶
 28 |    72     | 2³·3²
 29 |    75     | 3·5²
 30 |    80     | 2⁴·5
```

### Visualisierung des Algorithmus für S(3, 6)

**Schritt-für-Schritt:**

```
Initialisierung:
S = [1, _, _, _, _, _]
index = [1, 1, 1]  (für p₁=2, p₂=3, p₃=5)
next  = [2, 3, 5]  (S[1]×2, S[1]×3, S[1]×5)

Iteration 2:
S = [1, 2, _, _, _, _]
min(next) = 2
index = [2, 1, 1]  (erhöhe index[1])
next  = [4, 3, 5]  (S[2]×2, S[1]×3, S[1]×5)

Iteration 3:
S = [1, 2, 3, _, _, _]
min(next) = 3
index = [2, 2, 1]  (erhöhe index[2])
next  = [4, 6, 5]  (S[2]×2, S[2]×3, S[1]×5)

Iteration 4:
S = [1, 2, 3, 4, _, _]
min(next) = 4
index = [3, 2, 1]  (erhöhe index[1])
next  = [6, 6, 5]  (S[3]×2, S[2]×3, S[1]×5)

Iteration 5:
S = [1, 2, 3, 4, 5, _]
min(next) = 5
index = [3, 2, 2]  (erhöhe index[3])
next  = [6, 6, 10] (S[3]×2, S[2]×3, S[2]×5)

Iteration 6:
S = [1, 2, 3, 4, 5, 6]
min(next) = 6 (beide index[1] und index[2])
index = [4, 3, 2]  (erhöhe beide)
next  = [8, 9, 10] (S[4]×2, S[3]×3, S[2]×5)

Ergebnis: S(3, 6) = 6
```

## Beispiel 2: Dreieck T(n, k) für n=1..20, k=1..10

```
     k=  1   2   3   4   5   6   7   8   9  10
   ┌────────────────────────────────────────────
 1 │    1   1   1   1   1   1   1   1   1   1
 2 │    1   2   2   2   2   2   2   2   2   2
 3 │    1   2   3   3   3   3   3   3   3   3
 4 │    1   3   4   4   4   4   4   4   4   4
 5 │    1   3   4   4   5   5   5   5   5   5
 6 │    1   3   5   5   6   6   6   6   6   6
 7 │    1   3   5   5   6   6   7   7   7   7
 8 │    1   4   6   6   7   7   8   8   8   8
 9 │    1   4   7   7   8   8   9   9   9   9
10 │    1   4   7   7   9   9  10  10  10  10
11 │    1   4   7   7   9   9  10  10  10  10
12 │    1   4   8   8  10  10  11  11  11  11
13 │    1   4   8   8  10  10  11  11  11  11
14 │    1   4   8   8  10  10  12  12  12  12
15 │    1   4   8   8  11  11  13  13  13  13
16 │    1   5   9   9  12  12  14  14  14  14
17 │    1   5   9   9  12  12  14  14  14  14
18 │    1   5  10  10  13  13  15  15  15  15
19 │    1   5  10  10  13  13  15  15  15  15
20 │    1   5  10  10  14  14  16  16  16  16
```

### Interpretation der Spalten

- **k=1:** Nur die Zahl 1 → immer T(n,1) = 1
- **k=2:** 2-glatte Zahlen {1,2,4,8,16,...} (Zweierpotenzen)
- **k=3:** 3-glatte Zahlen {1,2,3,4,6,8,9,12,...} (nur Faktoren 2 und 3)
- **k=5:** 5-glatte Zahlen (Hamming-Zahlen)

### Beobachtungen

1. **Zeilen wachsen monoton:** T(n, k) ≤ T(n, k+1)
2. **Spalten wachsen monoton:** T(n, k) ≤ T(n+1, k)
3. **Plateaus:** T(n, k) = T(n+1, k) wenn n+1 nicht k-glatt ist
4. **Diagonale:** T(p, p) = p für Primzahl p

## Beispiel 3: Vergleich verschiedener s-Werte

### Wachstumsrate

```
n  | s=1 | s=2 | s=3 | s=4 | s=5 | s=6 | s=7 | s=8
---|-----|-----|-----|-----|-----|-----|-----|-----
 1 |   1 |   1 |   1 |   1 |   1 |   1 |   1 |   1
 2 |   1 |   2 |   2 |   2 |   2 |   2 |   2 |   2
 3 |   1 |   2 |   3 |   3 |   3 |   3 |   3 |   3
 4 |   1 |   3 |   4 |   4 |   4 |   4 |   4 |   4
 5 |   1 |   3 |   5 |   5 |   5 |   5 |   5 |   5
 6 |   1 |   3 |   6 |   6 |   6 |   6 |   6 |   6
 7 |   1 |   3 |   6 |   7 |   7 |   7 |   7 |   7
 8 |   1 |   4 |   7 |   8 |   8 |   8 |   8 |   8
 9 |   1 |   4 |   8 |   9 |   9 |   9 |   9 |   9
10 |   1 |   4 |   9 |  10 |  10 |  10 |  10 |  10
15 |   1 |   4 |  11 |  12 |  13 |  13 |  13 |  13
20 |   1 |   5 |  14 |  15 |  16 |  17 |  17 |  17
30 |   1 |   5 |  18 |  20 |  22 |  24 |  24 |  24
50 |   1 |   6 |  25 |  29 |  33 |  37 |  40 |  40
```

### Asymptotisches Verhalten

Für wachsendes s konvergiert die Dichte der s-glatten Zahlen:

```
Dichte(s-glatt unter n) ≈ T(n, p_s) / n
```

Beispiel für n = 100:
- s=3: T(100, 5) = 37    → Dichte ≈ 37%
- s=4: T(100, 7) = 45    → Dichte ≈ 45%
- s=5: T(100, 11) = 54   → Dichte ≈ 54%
- s=10: T(100, 29) = 83  → Dichte ≈ 83%

## Beispiel 4: Spezielle Fälle

### Fall s=1: Nur die Zahl 1
```
S(1, 1) = 1
S(1, n) ist nicht definiert für n > 1
```

### Fall s=2: Zweier- und Dreierpotenzen
```
Primzahlen: {2, 3}
S(2, n): 1, 2, 3, 4, 6, 8, 9, 12, 16, 18, 24, 27, 32, 36, ...

Diese sind von der Form 2^a × 3^b
```

### Fall s=4: Primzahlen {2, 3, 5, 7}
```
S(4, n): 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 15, 16, 18, 20, 21, ...

Nicht s=4-glatt sind:
11 (Primzahl > 7)
13 (Primzahl > 7)
17 (Primzahl > 7)
19 (Primzahl > 7)
22 = 2×11 (Faktor 11 > 7)
26 = 2×13 (Faktor 13 > 7)
```

## Beispiel 5: Große s-glatte Zahlen

### s=8 (Primzahlen bis 19)

Erste 50 8-glatte Zahlen:
```
  1,  2,  3,  4,  5,  6,  7,  8,  9, 10,
 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
 21, 22, 24, 25, 26, 27, 28, 30, 32, 33,
 34, 35, 36, 38, 39, 40, 42, 44, 45, 48,
 49, 50, 51, 52, 54, 55, 56, 57, 60, 63
```

**Nicht enthalten:**
- 23 (Primzahl > 19)
- 29 (Primzahl > 19)
- 31 (Primzahl > 19)
- 37 (Primzahl > 19)
- 41 (Primzahl > 19)
- 43 (Primzahl > 19)
- 46 = 2×23 (Faktor 23 > 19)
- 47 (Primzahl > 19)
- 53 (Primzahl > 19)
- 58 = 2×29 (Faktor 29 > 19)
- 59 (Primzahl > 19)
- 61 (Primzahl > 19)
- 62 = 2×31 (Faktor 31 > 19)

## Beispiel 6: Praktische Anwendung - FFT Größen

### Bevorzugte FFT-Größen (kleine Primfaktoren)

Für s=5 (Primfaktoren ≤ 11):

```
Gute FFT-Größen:
  32 = 2⁵
  64 = 2⁶
  96 = 2⁵×3
 128 = 2⁷
 192 = 2⁶×3
 256 = 2⁸
 384 = 2⁷×3
 512 = 2⁹
 768 = 2⁸×3
1024 = 2¹⁰
1536 = 2⁹×3
2048 = 2¹¹

Schlechte FFT-Größen (enthalten große Primfaktoren):
 97 (Primzahl)
101 (Primzahl)
103 (Primzahl)
107 (Primzahl)
```

## Beispiel 7: Rekursionsbaum-Visualisierung

### Berechnung von S(3, 8) = 9

```
                        S(3,8) = ?
                            |
            ┌───────────────┼───────────────┐
            │               │               │
      1×2=2  ?         1×3=3  ?        1×5=5  ?
        │                   │               │
    2×2=4  ?           3×3=9 ✓          5×5=25
        │
    4×2=8  ?
```

Kandidaten: {2, 3, 4, 5, 6, 8, 9, 10, 12, ...}

Sortiert: 1, 2, 3, 4, 5, 6, 8, 9, ...

S(3, 8) = 9 (die achte Zahl)

## Beispiel 8: Vergleich mit anderen Zahlenfolgen

| Position | s=1 | s=2 | s=3 (Hamming) | s=4 | Fibonacci | Primzahlen |
|----------|-----|-----|---------------|-----|-----------|------------|
|     1    |  1  |  1  |       1       |  1  |     1     |     2      |
|     2    |  -  |  2  |       2       |  2  |     1     |     3      |
|     3    |  -  |  3  |       3       |  3  |     2     |     5      |
|     4    |  -  |  4  |       4       |  4  |     3     |     7      |
|     5    |  -  |  6  |       5       |  5  |     5     |    11      |
|     6    |  -  |  8  |       6       |  6  |     8     |    13      |
|     7    |  -  |  9  |       8       |  7  |    13     |    17      |
|     8    |  -  | 12  |       9       |  8  |    21     |    19      |
|     9    |  -  | 16  |      10       |  9  |    34     |    23      |
|    10    |  -  | 18  |      12       | 10  |    55     |    29      |

**Beobachtung:** Glatte Zahlen wachsen langsamer als Fibonacci, aber schneller als Primzahlen.
