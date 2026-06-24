# Pre-Submission TODO List
## Prioritäten für Experimental Mathematics Einreichung

Erstellt: 23. Juni 2026  
Status: **Publikationswürdig, aber noch nicht eingereicht**

---

## STUFE 1: Statistische Robustheit von A(Δr) [HOHE PRIORITÄT]

### Warum kritisch?
A(Δr) ist jetzt der eigentliche Forschungsgegenstand. Ein Referee wird die statistische Signifikanz der Oszillationen hinterfragen.

### Konkreter Task:
Neues Kapitel im Paper (nach Section 6 oder als Subsection):

**"Statistical Robustness of A(Δr)"**

Inhalt:
- [ ] Bootstrap-Konfidenzintervalle für A(Δr) bei allen getesteten Δr-Werten
- [ ] Formale Standardfehler (bereits teilweise vorhanden aus 20 seeds)
- [ ] Effektgrößen für Regime-Unterschiede
  - Twin enhancement (Δr=2): Ist A(2) > 1 signifikant?
  - Geometric suppression (Δr=6-10): Ist A < 1 signifikant?
  - Large-distance enhancement (Δr≥20): Ist A > 1 signifikant?

### Implementierung:
```cpp
// Bootstrap-Resampling über die 20 Seeds
// Für jeden Δr-Wert:
// 1. Ziehe B=1000 Bootstrap-Samples
// 2. Berechne A(Δr) für jedes Sample
// 3. Bestimme 95%-Konfidenzintervall (2.5%, 97.5% Quantile)
// 4. Teste H0: A(Δr) = 1 (kein arithmetischer Effekt)
```

### Erwartetes Ergebnis:
Falls signifikant → Paper wird deutlich stärker  
Falls nicht signifikant → Wichtiger Hinweis auf Stichprobengröße

**Status**: ❌ Nicht implementiert

---

## STUFE 2: Alternative Vergleichspaare [SEHR HOHE PRIORITÄT]

### Warum kritisch?
Ein kritischer Referee wird fragen: "Warum genau {2,4,6} vs {2+Δr, 4+Δr, 6+Δr}?"

### Konkreter Task:
Test mit verschobenen Gap-Paaren:

**Original**: {2,4,6} vs {2+Δr, 4+Δr, 6+Δr}  
**Alternative 1**: {4,6,8} vs {4+Δr, 6+Δr, 8+Δr}  
**Alternative 2** (optional): {6,8,10} vs {6+Δr, 8+Δr, 10+Δr}

### Erwartung und wissenschaftlicher Wert:

**Fall A**: Struktur von A(Δr) bleibt ähnlich  
→ Robustheit bestätigt, Paper wird enorm gestärkt

**Fall B**: Struktur verschwindet oder ändert sich drastisch  
→ Wichtiger Hinweis auf Selektionsartefakt  
→ Beides wissenschaftlich wertvoll!

### Implementierung:
Modifikation von `phase_diagram_delta_r.cpp`:
```cpp
// Funktion: generate_gap_pairs_for_delta_r
// Parameter hinzufügen: int base_offset = 2
// Dann: low_gaps = {base_offset, base_offset+2, base_offset+4}
//       high_gaps = {base_offset+delta_r, base_offset+2+delta_r, ...}

// Drei separate Runs:
// 1. base_offset=2 (original)
// 2. base_offset=4 (alternative 1)
// 3. base_offset=6 (alternative 2, optional)
```

### Neues Paper-Element:
Subsection: "Robustness with Respect to Gap-Pair Selection"

Table: Vergleich von A(Δr) für verschiedene base offsets

**Status**: ❌ Nicht implementiert

---

## STUFE 3: Modulo 60 [OPTIONAL, aber wertvoll]

### Warum nützlich?
Nicht für neue Resultate, sondern für Universalitätsargument:
"Das Phänomen ist nicht an modulo-12 oder modulo-30 gebunden."

### Konkreter Task:
- [ ] `modulo60_test.cpp` analog zu modulo30_test.cpp
- [ ] 16 prime residue classes modulo 60
- [ ] Gleiche Δr-Variation (2, 4, 6, ..., 24)
- [ ] Vergleich: Sind die drei Regime (Twin/Geometric/Large-distance) stabil?

### Erwartetes Ergebnis:
Falls Regime stabil → Starkes Universalitätsargument  
Falls nicht → Modulus-Abhängigkeit ist selbst interessant

### Zeitaufwand:
~1-2 Tage (Code existiert bereits, nur Anpassung nötig)

**Status**: ❌ Nicht implementiert  
**Priorität**: Niedrig, aber wertvoll falls Zeit vorhanden

---

## Cover Letter Revision [SOFORT]

### Problem:
Section "Potential Concerns and Responses" wirkt für viele Editoren ungewöhnlich.

### Lösung:
Entfernen und implizit einbauen.

**Neuer Absatz statt "Potential Concerns"**:

> "We emphasize that the present work does not provide a theoretical derivation of A(Δr). Rather, it isolates this factor empirically through systematic null model comparison (N=10^6, 20 independent seeds) and proposes it as a quantitative target for future Hardy-Littlewood-type analysis. The robustness of our numerical findings is established through error bars and consistent behavior across multiple moduli (12, 30), though formal significance testing and alternative gap-pair selection remain valuable directions for strengthening the statistical foundation."

Dies adressiert implizit:
1. Hardy-Littlewood als offene Frage
2. Statistische Robustheit (aber ehrlich über Grenzen)
3. Gap-Pair-Auswahl (aber als "valuable direction" statt Schwäche)

**Status**: ❌ Noch nicht geändert

---

## Zusammenfassung: Was das Paper NICHT tun sollte

❌ Behaupten, Primzahlen zu erklären  
❌ Hardy-Littlewood-Verbindung als gelöst darstellen  
❌ Über statistische Signifikanz ohne formale Tests spekulieren  
❌ A(Δr)-Struktur als universell behaupten ohne Robustheitstests  

## Was das Paper JETZT leistet

✅ **Zerlegung**: R_Prime(Δr) = R_Bernoulli(Δr) · A(Δr)  
✅ **Exakte Formel** für Bernoulli-Baseline: (1-p)^(-Δr)  
✅ **Systematische Nullmodell-Hierarchie**  
✅ **Empirische Isolation** des arithmetischen Faktors A(Δr)  
✅ **Drei robuste Regime** (mit Fehlerbalken aus 20 seeds)  
✅ **Klare Kennzeichnung** offener Fragen  
✅ **Umformulierung der wissenschaftlichen Frage**:  
   - Früher: "Warum haben Primzahlen diese Asymmetrie?" (zu vage)  
   - Heute: "Welche Struktur steckt in A(Δr)?" (präzise, testbar)

## Der eigentliche wissenschaftliche Fortschritt

**Nicht die Bernoulli-Formel R = (1-p)^(-Δr)**, sondern:

**Die Erkenntnis, dass die ursprüngliche Fragestellung falsch formuliert war.**

Die Isolation der richtigen mathematischen Größe A(Δr) ist der entscheidende Schritt.

**Historische Analogie**: Gute Forschung beginnt mit der Isolation der richtigen Größe, nicht mit ihrer sofortigen Erklärung:
- Ramanujan → τ(n) → Modulformen
- Birch-Swinnerton-Dyer → L(E,1) → BSD-Vermutung
- Mazur → Torsion → Modularität  

---

## Zeitplan (konservativ)

| Task | Priorität | Zeitaufwand | Status |
|------|-----------|-------------|--------|
| Cover Letter Revision | SOFORT | 1h | ❌ |
| Statistical Robustness (Bootstrap) | HOCH | 2-3 Tage | ❌ |
| Alternative Gap-Pairs | SEHR HOCH | 2-3 Tage | ❌ |
| Modulo 60 | OPTIONAL | 1-2 Tage | ❌ |
| Paper-Revision (neue Sections) | HOCH | 1-2 Tage | ❌ |
| **Gesamtaufwand** | — | **~1-2 Wochen** | — |

---

## Die nächste große wissenschaftliche Frage

Nach erfolgreicher Einreichung:

**Kann A(Δr) aus Hardy-Littlewood-Heuristiken quantitativ hergeleitet werden?**

Das ist vermutlich der Punkt, an dem die eigentliche mathematische Geschichte beginnt.

---

## Lessons Learned

**Die größte Stärke des Projekts**: Bereitschaft, Interpretationen nach Robustheitstests zu verwerfen.

Modulo-12 → Hypothese ("intermediate regime")  
↓  
Modulo-30 → Widerlegung  
↓  
Neue Hypothese (Δr-dependent competition)

Das ist wissenschaftlich gesund und ungewöhnlich positiv für experimentelle Mathematik.

**Die größte Gefahr jetzt**: Overclaiming.

Nicht mehr mathematische Schwäche, sondern zu starke Behauptungen ohne vollständige statistische Absicherung.
