# Roadmap: Offene Fragen und Nächste Schritte

**Stand:** Juni 2026  
**Status:** Beide Projekte publikationsreif, aber mit klaren nächsten Forschungsfragen

---

## 🧭 Research Architecture v2 (Superseding Priority Layer)

Diese Prioritätslage ergänzt die bestehenden Inhalte und ist für Stage-6-Entscheidungen führend.

- **Kontrollachsen (Invarianten):** `M_C`, `Omega`, `S=v2+v3` (Koordinaten/Hintergrund)
- **Signalachsen (Symmetriebrüche):** `DeltaH_cramer`, `H(Delta-r)`, `Q_cramer` (primäre Stage-6-Signale)
- **Stage-6-Ziel:** Out-of-sample HL/Singular-Series-Familien auf den drei Signalachsen
- **Pflichtprotokoll:** Train/Holdout, `Delta-r`-Holdout, Skalen-Holdout, AIC/BIC (sekundär), Residualdiagnostik, Wheel-210-Vergleich

### Führende nächste Schritte (1-5)
1. Signalachsen-Baseline in Stage 6 finalisieren (`DeltaH_cramer`, `H(Delta-r)`, `Q_cramer`)
2. Vollständigen `Delta-r`-Holdout inklusive Residualdiagnostik durchlaufen
3. Skalen-Holdout (`N`) durchführen und Gewinnerstabilität prüfen
4. Wheel-210-Benchmarkvergleich für alle Top-Familien ausführen
5. Nur cross-holdout-stabile Familien in Stage 7 mechanistisch interpretieren

---

## Primzahl-Projekt: Bedingte Gap-Asymmetrien

### 🎯 Die zentrale offene Frage

**Kritischste Frage überhaupt:**
```
lim[X→∞] R(X) = ?
```

wobei `R(X) = P(EABC) / P(ECBA)`.

**Drei Szenarien:**

1. **Vorasymptotik:** `R(X) → 1` mit `R(X) = 1 + c/(log X)^α + ...`
   - Gap-Asymmetrie verschwindet asymptotisch
   - Beobachteter Bias ist ein Kleinzahleneffekt
   - Aktueller Datensatz (R: 6.14 → 4.59 → 4.05 → 3.59) deutet darauf hin

2. **Persistente Asymmetrie:** `R(X) → c > 1`
   - Gap-Asymmetrie bleibt bestehen
   - Fundamentale Struktur der Primzahlübergänge
   - Würde Hardy-Littlewood-Heuristiken erweitern

3. **Oszillation:** `R(X)` zeigt Prime-Race-artiges Verhalten
   - Verbindung zu Chebyshev-Bias-Phänomenen
   - Komplexe Dynamik der Restklassenübergänge

**Plausibelste Interpretation (aktuell):** Szenario 1 (R(X) → 1 mit sehr langsamer Konvergenz)

---

## 🔥 Priorität 1: Tests, die über die Natur des Phänomens entscheiden

### Test 1: Modulo 30 Verallgemeinerung ⭐⭐⭐

**Warum kritisch:**
- Modulo 12 = 2² · 3 enthält nur die kleinsten Primzahlen
- Modulo 30 = 2 · 3 · 5 ist die erste ernsthafte Verallgemeinerung
- **Entscheidet:** Allgemeines Phänomen vs. mod-12-Spezialeffekt

**Frage:**
Existieren analoge Gap-Asymmetrien für die 8 Restklassen modulo 30?
```
{1, 7, 11, 13, 17, 19, 23, 29}
```

**Erwartete Ergebnisse:**

| **Szenario** | **Implikation** |
|--------------|-----------------|
| Ähnliche zyklische Präferenzen | Allgemeines Phänomen lokaler Primzahlübergänge |
| Nur symmetrische Verteilung | Spezielle Konsequenz kleiner Moduli (2,3) |
| Andere Zyklenstruktur | Komplexere Dynamik, modulabhängig |

**Implementation:**
- `mod30_analysis.cpp` (analog zu `gap_distribution.cpp`)
- Gap-Verteilung `P(g mod 30 | a)` für alle 8 Klassen
- Übergangsmatrix 8×8: `P(a→b)`
- Suche nach bevorzugten Zyklen

**Zeitaufwand:** 1-2 Stunden Implementation, dann Rechnung über Nacht

---

### Test 2: R(X) für größere X ⭐⭐

**Ziel:** Entscheidung zwischen Szenario 1, 2, 3

**Datenpunkte benötigt:**
```
R(10^6), R(10^7), R(10^8)
```

**Erwartete Kurvenverläufe:**

| **Szenario** | **Erwartung** |
|--------------|---------------|
| Szenario 1 (Vorasymptotik) | R(10^6) ≈ 3.2, R(10^7) ≈ 2.8, R(10^8) ≈ 2.4 (stetige Abnahme) |
| Szenario 2 (Persistenz) | R(10^6) ≈ 4.0, R(10^7) ≈ 4.0, R(10^8) ≈ 4.0 (Stabilisierung) |
| Szenario 3 (Oszillation) | R schwankt ohne klare Konvergenz |

**Implementation:**
- `ratio_asymptotic.cpp` bereits vorhanden
- Nur längere Rechenzeit erforderlich

**Zeitaufwand:** X=10^6: ~1 Stunde, X=10^7: ~10 Stunden, X=10^8: ~100 Stunden

---

## 📊 Priorität 2: Erweiterte Analysen

### Test 3: Vollständige Signaturverteilung

**Aktuell:** Projektion auf χ ∈ {-1, 0, +1}

**Erweiterung:** Alle 6 möglichen normalisierten Signaturen:
```
(E,A,B,C)  →  +1  (EABC)
(E,A,C,B)  →   0  (andere)
(E,B,A,C)  →   0  (andere)
(E,B,C,A)  →   0  (andere)
(E,C,A,B)  →   0  (andere)
(E,C,B,A)  →  -1  (ECBA)
```

**Frage:** Welche der 4 "anderen" Signaturen sind häufiger?

**Hypothese:** Falls `P(EABC) ≫ P(alle anderen)`, dann ist der Bias nicht nur auf zwei Zyklen beschränkt, sondern EABC ist fundamental bevorzugt.

**Implementation:**
- Erweiterung von `chirality_robustness.cpp`
- Histogramm über alle 6 Klassen

---

### Test 4: Gap-Verteilung nach Primzahllückentyp

**Hypothese:** Die Gap-Asymmetrie könnte von der Größe der Lücke abhängen.

**Analyse:**
```
P(g mod 12 | a, g < 50)
P(g mod 12 | a, 50 ≤ g < 100)
P(g mod 12 | a, g ≥ 100)
```

**Frage:** Verschwindet die Asymmetrie bei größeren Gaps?

---

## 🧮 Priorität 3: Theoretische Erklärung

### Ansatz 1: Siebtheorie

**Ziel:** Vorhersage von `P(g mod 12 | a)` aus Siebmodellen

**Methode:**
- Vergleich mit Moduli 60, 420, 2310 (höhere Primorial-Basen)
- Modellierung via Buchstab-Identität
- Asymptotische Analyse für große Primzahlen

**Erwartung:** Falls Siebtheorie die Asymmetrie vorhersagt, ist die Ursache in lokalen Teilbarkeitsverboten zu finden.

---

### Ansatz 2: Hardy-Littlewood-Konstanten

**Ziel:** Verbindung zu k-Tupel-Konstanten

**Methode:**
- Hardy-Littlewood-Vermutung für Primzahl-k-Tupel
- Zusammenhang mit bedingten Gap-Verteilungen
- Asymptotische Formeln

**Offene Frage:** Sagen Hardy-Littlewood-Konstanten die Gap-Asymmetrie voraus?

---

## 🧪 Quantenfehlerkorrektur-Projekt

### ✅ Abgeschlossen (Juni 2026)
- [[5,1,3]]-Code vollständig dokumentiert
- Rechenbeispiel für Z₁-Fehler
- Mathematische Präzisierungen etabliert

### 🔜 Optional: Erweiterungen

#### Erweiterung 1: Vollständige Syndromtabelle

**Ziel:** Alle 15 nicht-trivialen 1-Qubit-Fehler dokumentieren

**Fehler:**
```
X₁, X₂, X₃, X₄, X₅  (5 Bitflips)
Y₁, Y₂, Y₃, Y₄, Y₅  (5 kombinierte Fehler)
Z₁, Z₂, Z₃, Z₄, Z₅  (5 Phasenfehler)
```

**Output:** Tabelle mit allen 16 Syndromen σ ∈ {0,1}⁴

**Nutzen:** Vollständige Referenz für [[5,1,3]]-Code

**Zeitaufwand:** ~2 Stunden (manuelle Berechnung + LaTeX-Tabelle)

---

#### Erweiterung 2: Weitere Fehlerbeispiele im Paper

**Beispiel 1:** Bitflip X₁
- Syndrom berechnen
- Recovery-Operation

**Beispiel 2:** Kombinierter Fehler Y₁ = iX₁Z₁
- Zeigen, dass Y₁ ebenfalls korrigierbar ist
- Syndrom: Kombination aus X₁- und Z₁-Syndromen

**Zeitaufwand:** ~1 Stunde pro Beispiel

---

#### Erweiterung 3: Clifford-Gruppe und binäre Ikosaedergruppe

**Thema:** Verbindung zwischen:
- Pauli-Gruppe (16 Elemente auf 1 Qubit)
- Clifford-Gruppe (normalizer der Pauli-Gruppe)
- Binäre Ikosaedergruppe 2I ≅ SL(2,5) (120 Elemente)

**Frage:** Welche Rolle spielt 2I in der Fehlerkorrektur?

**Status:** Spekulativ, keine unmittelbare Anwendung für [[5,1,3]]-Code

---

## 📅 Empfohlene Reihenfolge

### Kurzfristig (nächste Woche)
1. ⭐⭐⭐ **Modulo 30 Test** (Primzahlen) — entscheidet über Allgemeinheit
2. ⭐⭐ **R(10^6)** (Primzahlen) — erste Indikation für asymptotisches Verhalten

### Mittelfristig (nächste Monate)
3. **Vollständige Signaturverteilung** (Primzahlen)
4. **R(10^7), R(10^8)** (Primzahlen) — definitive Klärung
5. **Vollständige Syndromtabelle** (QEC) — falls Projekt weiterverfolgt wird

### Langfristig (nächste Jahre)
6. **Siebtheorie-Vergleich** (Primzahlen) — theoretische Erklärung
7. **Hardy-Littlewood-Verbindung** (Primzahlen) — asymptotische Formeln
8. **Publikation** in Fachzeitschrift (z.B. *Experimental Mathematics* oder *Journal of Number Theory*)

---

## 🎓 Publikationsstrategie

### Option A: Preprint (arXiv)
**Pro:**
- Sofortige Veröffentlichung
- Etabliert Priorität
- Community-Feedback

**Contra:**
- Kein Peer-Review
- Weniger Prestige

**Empfehlung:** Falls Modulo 30 Test positiv → sofort auf arXiv

---

### Option B: Peer-reviewed Journal
**Zielzeitschriften:**
- *Experimental Mathematics* (empirische Zahlentheorie)
- *Journal of Number Theory* (falls theoretische Erklärung gefunden)
- *International Journal of Number Theory* (Alternative)
- *Mathematics of Computation* (falls numerische Innovationen)

**Anforderungen:**
- Modulo 30 Test abgeschlossen
- R(X) bis mindestens 10^7
- Theoretische Diskussion (Siebtheorie oder Hardy-Littlewood)

**Empfehlung:** Nach Modulo 30 + R(10^7) → Einreichung bei *Experimental Mathematics*

---

## 🛠️ Technische Schulden

### Code-Qualität
- [ ] Unit-Tests für alle Programme
- [ ] Dokumentation der Algorithmen (Doxygen)
- [ ] Optimierung für sehr große X (≥10^8)

### Reproduzierbarkeit
- [ ] Seed-basierte Zufallsgeneratoren dokumentieren
- [ ] Exakte Compiler-Flags und Versionen dokumentieren
- [ ] Docker-Container für reproduzierbare Builds

### Datenmanagement
- [ ] Rohdaten für P(g mod 12 | a) archivieren
- [ ] R(X)-Zeitreihe in CSV exportieren
- [ ] Übergangsmatrizen für verschiedene X speichern

---

## 💡 Wilde Spekulationen (niedrige Priorität)

### Spekulation 1: Verbindung zu Primzahl-Rennen
Falls R(X) oszilliert → Verbindung zu klassischen Prime-Race-Phänomenen?

### Spekulation 2: Quantenmechanische Analogie
Gap-Asymmetrie ↔ Symmetriebrechung in Quantensystemen?

### Spekulation 3: Kategorientheorie
Übergangsmatrix als Morphismus in einer Kategorie von Restklassen?

### Spekulation 4: Catalan-Hierarchien und arithmetische Baumstrukturen ⭐ NEU (23.06.2026)
**Dokument:** `CATALAN_HIERARCHIES.md`

**Kernidee:** Primfaktorzerlegung ist ein Multiset, kein Baum. Catalan-Strukturen kodieren die Konstruktionshierarchie.

**Erweiterte EABC-Normalform:**
```
n = T(G, P, E)
```
wobei T ein Catalan-Baum ist.

**Arithmetische Magic:** M_arith(n, T) = Tamari-Distanz zum balancierten Baum

**Status:** 
- ✅ Mathematisch wohldefiniert (Catalan-Zahlen, Tamari-Gitter)
- ⚠️ Verbindung zu Quantum-Magic spekulativ (Metapher, keine formale Abbildung)
- 🔬 Empirisch ungetestet

**Nächster Schritt (falls Exploration gewünscht):**
1. Implementation `catalan_hierarchies.cpp`
2. Empirische Tests: Verteilung von M_arith über Zahlenklassen
3. Test: Korreliert EABC-Chiralität mit Tamari-Orientierung?

### Spekulation 5: Gödel-Universum und emergente Strukturen ⭐⭐ NEU (23.06.2026)
**Dokument:** `EMERGENT_STRUCTURES.md`

**Kernidee:** Strukturelle Analogie zwischen Gödel's rotierendem Universum und EABC-Chiralität.

**Gödel (1949):**
- Globale Rotation ω ≠ 0
- Gekippte Lichtkegel
- Kritischer Radius r_c → CTCs (Zeitreisen)
- Zeit ist emergent, nicht fundamental

**EABC-Analogie:**
- Chiraler Bias H_C(X) > 0
- Asymmetrische Übergangsmatrix P(a→b)
- Kritische Wigner-Zellen (D₁₁=+4, D₁₉₁=-12)
- Primzahlordnung emergent, nicht fundamental?

**Gemeinsames Muster:**
```
Globale Symmetrie + Lokale Asymmetrie
              ↓
    Emergente Struktur mit Chiralität
              ↓
         Kritische Übergänge
              ↓
      Topologische Phänomene
```

**Status:**
- ✅ Gödel-Lösung ist gesicherte Physik (exakte Lösung der Feldgleichungen)
- ✅ EABC-Bias ist gesicherte Empirie (bis X = 5·10⁵)
- ⚠️ **Analogie ist metaphorisch, keine formale Abbildung**
- ❌ Keine mathematische Äquivalenz konstruierbar (kontinuierlich ≠ diskret)
- ❌ Keine testbaren Konsequenzen

**Philosophische These:**
> "Falls Zeit im Gödel-Universum emergent ist, könnte Primzahlordnung in EABC emergent sein?"

**Wert:** Konzeptionell anregend, heuristisch für neue Fragen, philosophisch interessant

---

## 📞 Kontakt & Kollaboration

**Interessante potenzielle Kollaborationspartner:**
- Andrew Granville (Université de Montréal) — Prime Number Races
- Greg Martin (University of British Columbia) — Chebyshev Bias
- Terence Tao (UCLA) — Analytische Zahlentheorie
- Kannan Soundararajan (Stanford) — Hardy-Littlewood-Konstanten

**Konferenzen:**
- *Journées Arithmétiques* (alle 2 Jahre)
- *Analytic and Probabilistic Methods in Number Theory* (Vilnius)
- *Integers Conference* (jährlich in Georgia, USA)

---

## ✅ Zusammenfassung: Die wichtigsten nächsten Schritte

1. ⭐⭐⭐ **Modulo 30 Test** (höchste wissenschaftliche Priorität)
2. ⭐⭐ **R(10^6)** (schneller Durchlauf möglich)
3. ⭐ **Paper auf arXiv** (falls Modulo 30 positiv)

**Falls nur ein einziger Test durchgeführt wird: Modulo 30.**

---

**Letzter Update:** 22. Juni 2026  
**Status:** Beide Projekte pausiert, aber mit klarer Roadmap für Fortsetzung
