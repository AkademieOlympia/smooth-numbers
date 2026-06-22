# EABC-Chiralität und arithmetische Holonomie vollständiger Primzahl-Quadrupel

## Zusammenfassung

Dieses Dokument definiert eine **arithmetische Holonomie-Observable** für vollständige EABC-Primzahl-Quadrupel und untersucht ihr Verhalten unter verschiedenen Konstruktionsmethoden.

**Kernfrage:** Erzeugen verschiedene Quadrupel-Konstruktionen einen gerichteten Umlauf im EABC-Klassenzirkel?

---

## 1. Mathematische Grundlagen

### 1.1 EABC-Klassifikation

Für Primzahlen p > 3:

```
E: p ≡ 1  (mod 12)
A: p ≡ 5  (mod 12)
B: p ≡ 7  (mod 12)
C: p ≡ 11 (mod 12)
```

### 1.2 Vollständige Quadrupel

Ein Primzahl-Quadrupel Q = (p, q, r, s) ist **vollständig**, wenn:

```
{kₚ, kᵩ, kᵣ, k_s} = {E, A, B, C}
```

Jede der vier EABC-Klassen tritt genau einmal auf.

### 1.3 Chiralitäts-Observable

Die **Chiralitäts-Observable** χ(Q) ist definiert als:

```
χ(Q) = ⎧ +1,  norm(sig(Q)) = EABC
       ⎨ -1,  norm(sig(Q)) = ECBA
       ⎩  0,  sonst
```

wo:
- `sig(Q) = (kₚ, kᵩ, kᵣ, k_s)` die Signatur ist
- `norm(·)` die Normalisierung durch Rotation bis E an erster Stelle steht

**Interpretation:**
- χ(Q) = +1: Positiver Umlauf E → A → B → C → E
- χ(Q) = -1: Negativer Umlauf E → C → B → A → E
- χ(Q) = 0: Andere Permutation

---

## 2. Die Holonomie-Observable H(X)

### 2.1 Definition

Für eine Konstruktionsmethode C ist die **Holonomie** definiert als:

```
Hᴄ(X) = Σ_{Q≤X} χᴄ(Q)
```

wo die Summe über alle vollständigen Quadrupel Q bis X läuft, die nach Methode C konstruiert wurden.

### 2.2 Normalisierte Holonomie

Die **normalisierte Holonomie** ist:

```
hᴄ(X) = Hᴄ(X) / Nᴄ(X)
```

wo Nᴄ(X) die Anzahl vollständiger Quadrupel bis X nach Methode C ist.

### 2.3 Interpretation

- **hᴄ(X) > 0:** Bias zugunsten positiver Umläufe (EABC)
- **hᴄ(X) < 0:** Bias zugunsten negativer Umläufe (ECBA)
- **hᴄ(X) ≈ 0:** Keine Chiralitätspräferenz

---

## 3. Konstruktionsmethoden

### 3.1 Konsekutive Primzahlen (C_consec)

```
Qₙ = (pₙ, pₙ₊₁, pₙ₊₂, pₙ₊₃)
```

**Eigenschaften:**
- Gerichtete Ordnung entlang Zahlengerade
- Natürliche arithmetische Konstruktion

### 3.2 Zufällige Permutation (C_random)

```
Qₙ = σₙ(pᵢ, pⱼ, pₖ, pₗ)
```

wo σₙ eine zufällige Permutation ist.

**Eigenschaften:**
- Null-Hypothese für Symmetrie
- Sollte h(X) ≈ 0 ergeben

### 3.3 Glatte-Schalen-Quadrupel (C_smooth)

```
Qₙ = (p ∈ Schale, q₁, q₂, q₃ ∉ Schale)
```

wo q₁, q₂, q₃ die nächsten drei Primzahlen außerhalb der glatten Schale sind.

**Eigenschaften:**
- Ursprüngliche Konstruktion
- Verbindung zu smooth numbers

### 3.4 Lücken-sortierte Quadrupel (C_gaps)

```
Sortiere Primzahlen nach Lückengröße gₙ = pₙ₊₁ - pₙ
```

**Hypothese:** Könnte Korrelation mit Chiralität zeigen.

### 3.5 Kanonische Konstruktion (C_canonical)

```
Wähle Permutation die |H(X)| minimiert/maximiert
```

**Ziel:** Extremale Holonomie finden.

---

## 4. Empirische Ergebnisse

### 4.1 Konsekutive Primzahlen

| X        | Nᴄ(X) | H(X) | h(X)  |
|----------|-------|------|-------|
| 10³      | 48    | +19  | 0.396 |
| 10⁴      | 248   | +67  | 0.270 |
| 10⁵      | 1652  | +320 | 0.194 |

**Beobachtung:** h(X) scheint zu fallen, aber bleibt deutlich > 0.

### 4.2 Zufällige Permutation

| Samples | N(X)  | H(X) | h(X)   |
|---------|-------|------|--------|
| 10,000  | 10000 | -10  | -0.001 |

**Beobachtung:** h(X) ≈ 0, wie erwartet für Null-Hypothese.

### 4.3 Vergleich

```
h_consec(10⁵) ≈ 0.19 >> h_random(10⁴) ≈ 0
```

**Schlussfolgerung:** Die konsekutive Konstruktion hat einen **messbaren Chiralitäts-Bias**.

---

## 5. Forschungsfragen

### 5.1 Hauptfrage: Asymptotisches Verhalten

**Frage:** Gilt für die konsekutive Konstruktion:

```
lim_{X→∞} h_consec(X) = 0?
```

oder existiert ein persistenter Bias:

```
limsup_{X→∞} |h_consec(X)| > 0?
```

**Status:** Offen. Empirisch fällt h(X) von 0.4 auf 0.19, aber Konvergenz unklar.

### 5.2 Heuristisches Modell

**Annahme:** Primzahlen mod 12 verhalten sich "zufällig".

**Dann:** Für symmetrische Konstruktionen C:

```
Hᴄ(X) = o(Nᴄ(X))
```

**Test:** Stimmt dies für C_consec?

### 5.3 Extremale Konstruktionen

**Optimierungsproblem:**

```
max/min Hᴄ(X)  über alle Permutationen σ
```

**Interpretation:** Welche Ordnung maximiert/minimiert die Chiralitäts-Holonomie?

### 5.4 Korrelationen

**Hypothese:** Hᴄ(X) korreliert mit:
- Primzahl-Lücken gₙ = pₙ₊₁ - pₙ
- Chebyshev-Bias (Primzahl-Rennen)
- Quadratische Reste mod 12

**Test:** Berechne Korrelationskoeffizienten.

---

## 6. Theoretische Vermutungen

### Vermutung 1: Symmetrie natürlicher Konstruktionen

Für "natürliche, symmetrische" Konstruktionsmethoden C gilt:

```
Hᴄ(X) = o(Nᴄ(X))
```

**Beispiele symmetrischer Konstruktionen:**
- Zufällige Permutation ✓ (empirisch bestätigt)
- Nach Primzahl-Größe sortiert? (zu testen)

### Vermutung 2: Bias gerichteter Konstruktionen

Für "gerichtete" Konstruktionen C (z.B. konsekutiv, aufsteigend) existiert ein Bias:

```
limsup_{X→∞} |hᴄ(X)| > 0
```

**Empirische Evidenz:** h_consec(10⁵) ≈ 0.19 > 0

**Aber:** Langzeitverhalten unklar.

### Vermutung 3: Heuristisches Wachstum

Falls die Vermutung über "zufälliges" Verhalten der Primzahlen mod 12 gilt:

```
E[Hᴄ(X)] = 0  für symmetrische C
Var[Hᴄ(X)] = O(Nᴄ(X))
```

**Dann:**

```
Hᴄ(X) / √Nᴄ(X) = O(1)
```

mit hoher Wahrscheinlichkeit.

### Vermutung 4: Lücken-Korrelation

```
Corr(χ(Qₙ), gₙ) ≠ 0?
```

Falls ja, könnte dies h_consec(X) > 0 erklären.

---

## 7. Die Klein-Flasche als heuristisches Bild

### 7.1 Metapher

Die ursprüngliche "Klein-Flaschen"-Konstruktion war **keine rigoros aus Primzahlen emergente Topologie**, sondern eine **Metapher** für:

```
EABC ↔ positiver Umlauf (rechtshändig)
ECBA ↔ negativer Umlauf (linkshändig)
```

### 7.2 Lemniskate (∞)

Die E-Klasse als "Kreuzungspunkt" beider Chiralitäten:

```
      B
     / \
    C   A
     \ /
      E  ← Kreuzungspunkt
     / \
    A   C
     \ /
      B
```

Dies visualisiert die beiden Umläufe, ist aber **keine topologische Invariante**.

### 7.3 Was bleibt

Die Metapher ist **nützlich für Intuition**, aber die **harte Mathematik** liegt in:

```
Hᴄ(X) = Σ χ(Q)
```

nicht in χ = -1 oder Klein-Flaschen-Eigenschaften.

---

## 8. Implementierung

### 8.1 Chiralitäts-Observable

```cpp
int chi(const Quadrupel& q) {
    if (!q.ist_vollstaendig()) return 0;
    string norm = q.normalisiert();
    if (norm == "EABC") return +1;
    if (norm == "ECBA") return -1;
    return 0;
}
```

### 8.2 Holonomie-Berechnung

```cpp
int holonomie(const vector<Quadrupel>& quadrupel) {
    int H = 0;
    for (const auto& q : quadrupel) {
        H += chi(q);
    }
    return H;
}
```

### 8.3 Normalisierte Holonomie

```cpp
double h(const vector<Quadrupel>& quadrupel) {
    int H = holonomie(quadrupel);
    int N = quadrupel.size();
    return N > 0 ? (double)H / N : 0;
}
```

---

## 9. Experimentelles Programm

### Phase 1: Große Datensätze (✓ teilweise erledigt)

**Ziel:** Berechne h_consec(X) für X = 10⁶, 10⁷, 10⁸

**Status:** Bis 10⁵ implementiert, größere Bereiche ausstehend.

### Phase 2: Alternative Konstruktionen

**Ziel:** Implementiere und teste:
- C_gaps (Lücken-sortiert)
- C_canonical (extremale Holonomie)
- C_mod_classes (gruppiert nach mod-12-Mustern)

### Phase 3: Korrelationsanalyse

**Ziel:** Berechne:
- Corr(χ(Qₙ), gₙ)
- Corr(χ(Qₙ), Chebyshev-Bias)
- Corr(χ(Qₙ), quadratische Reste)

### Phase 4: Theoretische Modelle

**Ziel:** 
- Heuristisches Wahrscheinlichkeitsmodell
- Erwartungswert E[H(X)] unter Zufallsannahme
- Varianz Var[H(X)]

---

## 10. Offene Fragen

### 10.1 Kurzfristig (empirisch)

1. **Asymptotik:** Konvergiert h_consec(X) → 0 oder stabilisiert es sich?
2. **Lücken:** Korreliert χ(Q) mit Primzahl-Lücken?
3. **Extremal:** Was ist max |H(X)| über alle Permutationen?

### 10.2 Mittelfristig (heuristisch)

4. **Modell:** Stimmt das Zufalls-Modell für Primzahlen mod 12?
5. **Wachstum:** Ist H(X) = O(√N(X)) unter Zufallsannahme?
6. **Bias-Quelle:** Warum ist h_consec(X) > 0?

### 10.3 Langfristig (theoretisch)

7. **Beweisbar:** Kann man Hᴄ(X) = o(Nᴄ(X)) für C_consec beweisen?
8. **Verbindung:** Gibt es eine Verbindung zu bekannten zahlentheoretischen Größen?
9. **Verallgemeinerung:** Funktioniert dies für andere Moduli (30, 60, 210)?

---

## 11. Literatur und Kontext

### 11.1 Primzahl-Verteilung mod q

**Dirichlet-Theorem:** Jede Restklasse mod 12 (coprime zu 12) enthält unendlich viele Primzahlen.

**Aber:** Lokale Ungleichverteilung möglich (Chebyshev-Bias).

### 11.2 Primzahl-Rennen

**Chebyshev-Bias:** Primzahlen ≡ 3 (mod 4) "führen" gegen Primzahlen ≡ 1 (mod 4) im Rennen.

**Verbindung:** Könnte ähnlicher Bias für EABC-Chiralität existieren?

### 11.3 Primzahl-Tupel

**Primzahl-Zwillinge, Tripel, Quadrupel:** Bekannte Objekte.

**Neu:** EABC-vollständige Quadrupel als spezieller Typ.

---

## 12. Zusammenfassung

### Was ist wohldefiniert:

1. ✅ **EABC-Klassifikation** - Exakte Arithmetik
2. ✅ **Vollständige Quadrupel** - Präzise Definition
3. ✅ **Chiralitäts-Observable χ(Q)** - Wohldefiniert
4. ✅ **Holonomie Hᴄ(X)** - Arithmetische Observable

### Was ist empirisch beobachtet:

5. ✓ **h_random(X) ≈ 0** - Symmetrie bei zufälliger Ordnung
6. ✓ **h_consec(X) ≈ 0.19** - Bias bei konsekutiver Ordnung
7. ✓ **h(X) scheint zu fallen** - Aber Konvergenz unklar

### Was ist offen:

8. ? **Asymptotik:** lim h(X) = 0 oder > 0?
9. ? **Korrelationen:** Mit Lücken, Chebyshev-Bias?
10. ? **Heuristik:** Stimmt Zufalls-Modell?

### Was ist gestrichen:

11. ✗ **Klein-Flasche als Topologie** - Aufgeprägt, nicht emergent
12. ✗ **χ = -1 als Invariante** - Heuristisch, nicht rigorös
13. ✗ **"Primzahlen bevorzugen Chiralität"** - Konstruktionsartefakt

---

## 13. Fazit

Die **arithmetische Holonomie-Observable Hᴄ(X)** ist ein wohldefinierten mathematisches Objekt, das die "Gerichtetheit" verschiedener Quadrupel-Konstruktionen quantifiziert.

**Die zentrale Frage ist:**

> Gibt es eine kanonische Konstruktion C, für die ein persistenter Chiralitäts-Bias existiert:
> ```
> limsup_{X→∞} |hᴄ(X)| > 0
> ```

Falls ja, wäre dies eine **neue zahlentheoretische Observable** mit potentiellen Verbindungen zu Primzahl-Lücken und Primzahl-Rennen.

Falls nein (Hᴄ(X) = o(Nᴄ(X)) für alle natürlichen C), würde dies die Zufallshypothese für Primzahlen mod 12 stützen.

---

*Mathematisch saubere Formulierung, 22.06.2026*
