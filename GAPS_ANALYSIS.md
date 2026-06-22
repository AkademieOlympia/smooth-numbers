# Gap-Verteilungs-Analyse und mechanistische Erklärung des Orientierungsbias

**Status:** ✓ Mechanismus identifiziert  
**Datum:** Juni 2026

---

## Zusammenfassung

Der beobachtete Orientierungsbias in vollständigen EABC-Primzahlquadrupeln ist **keine topologische Eigenschaft**, sondern wird durch eine asymmetrische konditionale Gap-Verteilung modulo 12 induziert.

---

## Die fundamentale Relation

Für konsekutive Primzahlen `p_n ≡ a (mod 12)` und `p_{n+1} ≡ b (mod 12)` gilt:

```
b ≡ a + g (mod 12)
```

wobei `g = p_{n+1} - p_n` die Primzahllücke ist.

Daraus folgt unmittelbar:

```
P(p_{n+1} ≡ b | p_n ≡ a) = P(g ≡ b - a (mod 12) | p_n ≡ a)
```

Die Übergangsmatrix P(a→b) ist also eine **umkodierte Gap-Verteilung modulo 12**.

---

## Zyklische Pfade und Gap-Klassen

### EABC-Zyklus (positiv orientiert)

Der EABC-Zyklus verwendet folgende Übergänge:

| Übergang | Residuen | Gap mod 12 | P(g\|a) |
|----------|----------|------------|---------|
| E → A    | 1 → 5    | g ≡ 4      | 0.3242  |
| A → B    | 5 → 7    | g ≡ 2      | 0.3581  |
| B → C    | 7 → 11   | g ≡ 4      | 0.3254  |
| C → E    | 11 → 1   | g ≡ 2      | 0.3537  |

**Gap-Klassen:** {4, 2, 4, 2}

**Produkt:**
```
P(EABC) = P_E(4) · P_A(2) · P_B(4) · P_C(2)
        = 0.3242 × 0.3581 × 0.3254 × 0.3537
        = 0.013360
```

### ECBA-Zyklus (negativ orientiert)

Der ECBA-Zyklus verwendet folgende Übergänge:

| Übergang | Residuen | Gap mod 12 | P(g\|a) |
|----------|----------|------------|---------|
| E → C    | 1 → 11   | g ≡ 10     | 0.2554  |
| C → B    | 11 → 7   | g ≡ 8      | 0.2251  |
| B → A    | 7 → 5    | g ≡ 10     | 0.2570  |
| A → E    | 5 → 1    | g ≡ 8      | 0.2235  |

**Gap-Klassen:** {10, 8, 10, 8}

**Produkt:**
```
P(ECBA) = P_E(10) · P_C(8) · P_B(10) · P_A(8)
        = 0.2554 × 0.2251 × 0.2570 × 0.2235
        = 0.003302
```

---

## Die mechanistische Formel

```
P(EABC)     P_E(4) · P_A(2) · P_B(4) · P_C(2)
────────  = ───────────────────────────────────
P(ECBA)     P_E(10) · P_C(8) · P_B(10) · P_A(8)
```

**Empirischer Wert (100.000 Primzahlen):** 4.046

---

## Gap-Asymmetrie

Die zentrale Beobachtung ist:

```
P(g ≡ 2,4 | p_n ≡ a)  >  P(g ≡ 8,10 | p_n ≡ a)
```

für alle EABC-Klassen a ∈ {E, A, B, C}.

### Detaillierte Verhältnisse (100.000 Primzahlen)

| Start | P(g≡2,4) | P(g≡8,10) | Ratio |
|-------|----------|-----------|-------|
| E(1)  | 0.3242   | 0.2554    | 1.269 |
| A(5)  | 0.3581   | 0.2235    | 1.602 |
| B(7)  | 0.3254   | 0.2570    | 1.266 |
| C(11) | 0.3537   | 0.2251    | 1.571 |

Die Gap-Klassen {2, 4} treten **durchweg häufiger** auf als die Gap-Klassen {8, 10}.

---

## Die vollständige kausale Kette

```
Primzahllücken g haben eine Verteilung modulo 12
                ↓
Diese Verteilung ist konditional auf p_n ≡ a
                ↓
P(g ≡ 2,4 | a) > P(g ≡ 8,10 | a)
                ↓
Durch b ≡ a + g entsteht P(a→b)
                ↓
EABC benötigt g ≡ {2,4}, ECBA benötigt g ≡ {8,10}
                ↓
P(EABC) / P(ECBA) ≈ 4.046
                ↓
Orientierungsbias H_C(X) > 0
```

---

## Paper-Formulierung

**The observed orientation bias is not a topological phenomenon. It is induced by an asymmetric conditional gap distribution modulo 12. The EABC cycle uses gap classes {4,2,4,2}, whereas the reverse ECBA cycle uses {10,8,10,8}. In the investigated range, the former conditional gap classes occur with substantially higher probability, yielding a transition-product ratio of approximately 4.046.**

---

## Offene Frage: Ursache der Gap-Asymmetrie

Die zentrale noch offene theoretische Frage lautet:

**Warum ist P(g ≡ 2,4) > P(g ≡ 8,10)?**

### Vermutung: Lokale Siebeffekte

Eine plausible Hypothese sind lokale Siebeffekte durch kleine Primmoduli:

- Primzahlen > 3 erfüllen bereits p ≡ 1, 5, 7, 11 (mod 12)
- Kleine Primzahlen (5, 7, 11, 13, ...) erzeugen Siebmuster in der Gap-Verteilung
- Diese Muster könnten die Gap-Klassen {2, 4} gegenüber {8, 10} bevorzugen

**Status:** Hypothese, nicht bewiesen

### Nächster theoretischer Schritt

Vergleich der empirischen Gap-Verteilung gegen Vorhersagen eines einfachen Siebmodells modulo:

- 60 = lcm(12, 5)
- 420 = lcm(12, 5, 7)  
- 2310 = lcm(12, 5, 7, 11)

**Test:**
```
Falls Siebmodell den Faktor ~4 teilweise reproduziert
  → Mechanismus durch Siebeffekte erklärt
Sonst
  → Tieferer Restklassen- oder Prime-Race-Effekt
```

---

## Implementierung

**Programm:** `gap_distribution.cpp`

**Verwendung:**
```bash
make gap
./gap_distribution 100000      # 100K Primzahlen
./gap_distribution 1000000     # 1M Primzahlen (empfohlen)
```

**Ausgaben:**

1. Vollständige Gap-Verteilungsmatrix P(g mod 12 | p_n ≡ a)
2. Gap-Asymmetrie-Analyse: {2,4} vs {8,10}
3. Zyklische Pfade: EABC vs ECBA
4. Mechanistische Formel und Ratio

---

## Referenzen

- **CHIRALITY_OBSERVABLES_v2.md:** Definition der Bias-Funktion H_C(X)
- **transition_matrix.cpp:** Übergangsmatrix P(a→b)
- **autocorrelation_analysis.cpp:** Robustheit gegen Autokorrelation

---

## Chronologie der Erkenntnis

1. **Ursprung:** Klein-Flaschen-Metapher (geometrisch, heuristisch)
2. **Erste Revision:** Chiralitätsfunktion χ(Q), Holonomie H(X)
3. **Kritische Tests:** Robustheit, Autokorrelation → Bias bestätigt
4. **Theoretischer Durchbruch:** Übergangsmatrix P(a→b) asymmetrisch
5. **Mechanistische Erklärung:** Gap-Verteilung mod 12 → geschlossene Formel

Die Entwicklung führte von metaphorischer Topologie zu **präziser zahlentheoretischer Mechanik**.

---

**Fazit:** Der Orientierungsbias ist ein **arithmetisches Phänomen**, das durch die konditionale Gap-Verteilung konsekutiver Primzahlen modulo 12 vollständig beschrieben wird. Die zugrunde liegende Ursache der Gap-Asymmetrie bleibt offen und ist vermutlich auf lokale Siebeffekte zurückzuführen.
