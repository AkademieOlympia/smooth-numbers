# Interessante Beispiele: EABC/Catalan-Parameter (n = 1..100)

Automatisch generiert durch `comparison_n1_100.py`

---

## 1. Hohe Konzentration H(n) ≈ 1

Zahlen, bei denen alle EABC-Faktoren (fast) zur selben Klasse gehören.

| n | Faktorisierung | Ω | EABC-Sig | v(n) | H(n) |
|---|---|---|---|---|---|
| 5 | 5 | 1 | A | (0,1,0,0) | 1.0000 |
| 78 | 2·3·13 | 3 | EEE | (1,0,0,0) | 1.0000 |
| 75 | 3·5² | 3 | EAA | (0,2,0,0) | 1.0000 |
| 74 | 2·37 | 2 | EE | (1,0,0,0) | 1.0000 |
| 73 | 73 | 1 | E | (1,0,0,0) | 1.0000 |
| 71 | 71 | 1 | C | (0,0,0,1) | 1.0000 |
| 69 | 3·23 | 2 | EC | (0,0,0,1) | 1.0000 |
| 68 | 2²·17 | 3 | EEA | (0,1,0,0) | 1.0000 |
| 67 | 67 | 1 | B | (0,0,1,0) | 1.0000 |
| 66 | 2·3·11 | 3 | EEC | (0,0,0,1) | 1.0000 |

## 2. Niedrige Konzentration H(n) ≈ 0.25

Zahlen mit gleichverteilten EABC-Faktoren über alle vier Klassen.

| n | Faktorisierung | Ω | EABC-Sig | v(n) | H(n) |
|---|---|---|---|---|---|
| 35 | 5·7 | 2 | AB | (0,1,1,0) | 0.5000 |
| 55 | 5·11 | 2 | AC | (0,1,0,1) | 0.5000 |
| 95 | 5·19 | 2 | AB | (0,1,1,0) | 0.5000 |
| 91 | 7·13 | 2 | BE | (1,0,1,0) | 0.5000 |
| 65 | 5·13 | 2 | AE | (1,1,0,0) | 0.5000 |
| 77 | 7·11 | 2 | BC | (0,0,1,1) | 0.5000 |
| 70 | 2·5·7 | 3 | EAB | (0,1,1,0) | 0.5000 |
| 76 | 2²·19 | 3 | EEB | (0,0,1,0) | 1.0000 |
| 75 | 3·5² | 3 | EAA | (0,2,0,0) | 1.0000 |
| 74 | 2·37 | 2 | EE | (1,0,0,0) | 1.0000 |

## 3. Hohe Shell-Werte S(n) = v₂(n) + v₃(n)

Zahlen mit vielen Faktoren 2 und 3 (smooth numbers).

| n | Faktorisierung | S(n) | v₂ | v₃ | Ω |
|---|---|---|---|---|---|
| 96 | 2⁵·3 | 6 | 5 | 1 | 6 |
| 64 | 2⁶ | 6 | 6 | 0 | 6 |
| 32 | 2⁵ | 5 | 5 | 0 | 5 |
| 48 | 2⁴·3 | 5 | 4 | 1 | 5 |
| 72 | 2³·3² | 5 | 3 | 2 | 5 |
| 16 | 2⁴ | 4 | 4 | 0 | 4 |
| 54 | 2·3³ | 4 | 1 | 3 | 4 |
| 80 | 2⁴·5 | 4 | 4 | 0 | 5 |
| 24 | 2³·3 | 4 | 3 | 1 | 4 |
| 81 | 3⁴ | 4 | 0 | 4 | 4 |

## 4. Hohe Primfaktoranzahl Ω(n)

Zahlen mit vielen Primfaktoren (mit Vielfachheit).

| n | Faktorisierung | Ω(n) | C_{Ω-1} | EABC-Sig |
|---|---|---|---|---|
| 96 | 2⁵·3 | 6 | 42 | EEEEEE |
| 64 | 2⁶ | 6 | 42 | EEEEEE |
| 32 | 2⁵ | 5 | 14 | EEEEE |
| 72 | 2³·3² | 5 | 14 | EEEEE |
| 80 | 2⁴·5 | 5 | 14 | EEEEA |
| 48 | 2⁴·3 | 5 | 14 | EEEEE |
| 16 | 2⁴ | 4 | 5 | EEEE |
| 56 | 2³·7 | 4 | 5 | EEEB |
| 24 | 2³·3 | 4 | 5 | EEEE |
| 81 | 3⁴ | 4 | 5 | EEEE |

## 5. Vielfältige EABC-Signaturen

Zahlen mit langen, vielfältigen EABC-Signaturen (viele verschiedene Klassen).

| n | Faktorisierung | EABC-Sig | Vielfalt | v(n) | H(n) |
|---|---|---|---|---|---|
| 70 | 2·5·7 | EAB | 3/4 | (0,1,1,0) | 0.5000 |
| 80 | 2⁴·5 | EEEEA | 2/4 | (0,1,0,0) | 1.0000 |
| 40 | 2³·5 | EEEA | 2/4 | (0,1,0,0) | 1.0000 |
| 56 | 2³·7 | EEEB | 2/4 | (0,0,1,0) | 1.0000 |
| 60 | 2²·3·5 | EEEA | 2/4 | (0,1,0,0) | 1.0000 |
| 84 | 2²·3·7 | EEEB | 2/4 | (0,0,1,0) | 1.0000 |
| 88 | 2³·11 | EEEC | 2/4 | (0,0,0,1) | 1.0000 |
| 90 | 2·3²·5 | EEEA | 2/4 | (0,1,0,0) | 1.0000 |
| 100 | 2²·5² | EEAA | 2/4 | (0,2,0,0) | 1.0000 |
| 20 | 2²·5 | EEA | 2/4 | (0,1,0,0) | 1.0000 |

---

## Statistiken

- **Anzahl Zahlen mit H definiert:** 80/100
- **Durchschnitt H(n):** 0.9563
- **Median H(n):** 1.0000
- **Min H(n):** 0.5000 (n=35)
- **Max H(n):** 1.0000 (mehrere Zahlen)
- **Durchschnitt Ω(n):** 2.39
- **Max Ω(n):** 6 (n=64)
- **Durchschnitt S(n):** 1.45
- **Max S(n):** 6 (n=64)
- **Anzahl verschiedener EABC-Signaturen:** 30
- **Häufigste Signatur:** 'E' (7×)
