# Conditional Gap Dynamics in Prime Number Residue Classes

## Projekt in einem Satz

Dieses Repository begann als Implementierung glatter Zahlen, entwickelte sich aber zu einem experimentellen Zahlentheorie-Projekt über bedingte Gap-Dynamiken konsekutiver Primzahlen. Der aktuelle Kern ist die Analyse von $P(g \bmod m \mid p_n \equiv a)$, aus der Übergangsmatrizen, Zyklusgewichte und Orientierungsobservablen abgeleitet werden. Historische geometrische Metaphern wie Klein-Flaschen wurden zugunsten testbarer Nullmodelle und reproduzierbarer Übergangsdynamik zurückgestellt.

---

## 1. Aktueller Kern: Bedingte Primzahl-Gap-Dynamik

### Das elementarste Statement

Der **primäre empirische Befund** dieser Arbeit:

$$P(g \equiv 2,4 \bmod 12 \mid p_n \equiv a) > P(g \equiv 8,10 \bmod 12 \mid p_n \equiv a)$$

für alle $a \in \{E, A, B, C\}$ im untersuchten Bereich (bis $X = 5 \times 10^5$).

**Dies ist keine eigenständiges Phänomen, sondern eine tieferliegende Asymmetrie der Gap-Verteilung modulo 12.**

### Vier-Ebenen-Hierarchie

Die wichtigste methodische Erkenntnis:

```
Ebene 0: P(g mod 12 | a)    ← Arithmetische Rohdaten (direkt beobachtbar)
              ↓
Ebene 1: P(a→b)             ← Übergangsdynamik (Bild der Gap-Verteilung)
              ↓
Ebene 2: R(X)               ← Zyklusgewichte (abgeleitet)
              ↓
Ebene 3: H_C(X)             ← Observable (Messinstrument)
```

**Kernkenntnis:**
- **$H_C(X)$ ist nicht das Objekt**
- **Es ist ein Thermometer**
- **Die Temperatur ist $R(X)$**
- **Die Physik dahinter ist $P(g \bmod 12 \mid a)$**

Der Orientierungsbias folgt mechanistisch aus der Gap-Asymmetrie und ist eine abgeleitete Observable.

### Exakt definierte Objekte

**Primär (direkt beobachtbar):**
- ✅ **Bedingte Gap-Verteilung** $P(g \bmod 12 \mid p_n \equiv a)$ - Empirisch gemessen
- ✅ **Gap-Asymmetrie** $P(g \equiv 2,4) > P(g \equiv 8,10)$ - Robust über mehrere Bereiche

**Sekundär (abgeleitet):**
- ✅ **Übergangsmatrix** $P(a \to b)$ - Asymmetrisch, erklärt durch Gap-Verteilung
- ✅ **Zyklusverhältnis** $R(X) = P(EABC)/P(ECBA)$ - Daten: 6.14 → 4.59 → 4.05 → 3.59
- ✅ **Orientierungsobservable** $\chi(Q)$ - Auf vollständigen EABC-Quadrupeln
- ✅ **Bias-Funktion** $H_C(X) = \sum \chi(Q)$ - "Thermometer, nicht Temperatur"

---

## 2. Mathematische Koordinaten

### 2.1 Smooth Numbers (Ursprung)

Dieses Repository begann als Implementierung **s-glatter Zahlen**: positive ganze Zahlen, deren Primfaktoren alle $\leq p_s$ sind.

**Beispiele:**
- 3-glatte Zahlen (Hamming-Zahlen): Primfaktoren $\in \{2, 3, 5\}$
- Algorithmische Basis: Verallgemeinerter Hamming-Algorithmus mit dynamischer Programmierung

**Status:** Technische Grundlage, nicht mehr der inhaltliche Kern. Siehe [Historische Dokumente](#72-historical).

### 2.2 EABC-Koordinaten

Jede natürliche Zahl $n > 1$ wird dargestellt als:

$$n \mapsto (v_2(n), v_3(n), v_{\text{EABC}}(n))$$

mit $v_{\text{EABC}} = (e, a, b, c)$ für Primfaktoren $p > 3$.

**EABC-Klassifikation** (Primzahlen $p > 3$ modulo 12):

| Klasse | $p \bmod 12$ | Beispiele |
|--------|--------------|-----------|
| **E** | 1 | 13, 37, 61, 73... |
| **A** | 5 | 5, 17, 29, 41... |
| **B** | 7 | 7, 19, 31, 43... |
| **C** | 11 | 11, 23, 47, 59... |

### 2.3 Gauß-Eisenstein-Interpretation ⭐

**Die stärkste algebraische Fundierung:**

Die EABC-Klassen entsprechen **exakt** dem Spaltungsverhalten in den quadratischen Zahlkörpern $\mathbb{Z}[i]$ (Gauß) und $\mathbb{Z}[\omega]$ (Eisenstein):

$$E, A, B, C \leftrightarrow (S,S), (S,I), (I,S), (I,I)$$

| EABC | mod 12 | $\mathbb{Z}[i]$ (Gauß) | $\mathbb{Z}[\omega]$ (Eisenstein) |
|------|--------|-------------------------|-----------------------------------|
| **E** | 1 | **Spaltet** (S) | **Spaltet** (S) |
| **A** | 5 | **Spaltet** (S) | **Inert** (I) |
| **B** | 7 | **Inert** (I) | **Spaltet** (S) |
| **C** | 11 | **Inert** (I) | **Inert** (I) |

**Dies ist ein Satz der algebraischen Zahlentheorie (quadratisches Reziprozitätsgesetz), keine Spekulation.**

Die EABC-Klassifikation ist somit die natürliche arithmetische Struktur, die aus dem Verhalten von Primzahlen in $\mathbb{Q}(i)$ und $\mathbb{Q}(\omega)$ entsteht.

---

## 3. Hauptresultate

### 3.1 Gap-Asymmetrie modulo 12

**Empirischer Befund (bis $X = 5 \times 10^5$):**

Für alle Startklassen $a \in \{E, A, B, C\}$ gilt:

$$P(g \equiv 2,4 \bmod 12 \mid p_n \equiv a) > P(g \equiv 8,10 \bmod 12 \mid p_n \equiv a)$$

**Status:** Robust über mehrere Bereichsfenster ($10^4, 5 \times 10^4, 10^5, 5 \times 10^5$) gemessen.

### 3.2 Übergangsmatrix $P(a \to b)$

**Empirisch gemessen:**

Die Übergangswahrscheinlichkeiten $P(a \to b)$ zwischen EABC-Klassen konsekutiver Primzahlen sind asymmetrisch.

**Mechanistische Formel:**

$$\frac{P(EABC)}{P(ECBA)} = \frac{P_E(4) \cdot P_A(2) \cdot P_B(4) \cdot P_C(2)}{P_E(10) \cdot P_C(8) \cdot P_B(10) \cdot P_A(8)}$$

wobei $P_a(g)$ die bedingte Wahrscheinlichkeit $P(g \bmod 12 \mid p_n \equiv a)$ ist.

**Struktur und Zyklusgewichte:**
- EABC-Zyklus (E→A→B→C→E) ist bevorzugt gegenüber ECBA-Zyklus (E→C→B→A→E)
- Dies folgt direkt aus der Gap-Asymmetrie

### 3.3 Orientierung als abgeleitete Observable

**Orientierungsobservable** $\chi(Q)$ auf vollständigen EABC-Quadrupeln:

$$\chi(Q) = \begin{cases} +1, & \text{norm}(\text{sig}(Q)) = EABC \\ -1, & \text{norm}(\text{sig}(Q)) = ECBA \\ 0, & \text{sonst} \end{cases}$$

**Bias-Funktion:**

$$H_C(X) = \sum_{Q \leq X} \chi(Q)$$

**Wichtig:** $H_C(X)$ ist ein Thermometer für die tieferliegende Gap-Dynamik, nicht das primäre Phänomen.

**Empirische Beobachtungen:**
- $h_{\text{random}}(X) \approx 0$ - Symmetrie bei zufälliger Ordnung (Kontrolltest bestanden)
- $h_{\text{consec}}(X) \approx 0.19$ bei $X = 10^5$ (konstruktionsabhängiger Bias)
- Bias überlebt Autokorrelationskorrektur ($Z_{\text{eff}} = 16.5$ für nichtüberlappende Fenster)

### 3.4 Nullmodell-Hierarchie

**Empirischer Befund (konsistent über 10 Seeds, N=100.000):**

$$R_{\text{Poisson}} \approx 1.83 \quad > \quad R_{\text{Prime}} \approx 1.58 \quad > \quad R_{\text{Cramér}} \approx 1.36$$

**Interpretation:**

Ein geometrisches Nullmodell erklärt einen wesentlichen Anteil der beobachteten Asymmetrie. Für konstante Bernoulli-Prozesse mit Akzeptanzwahrscheinlichkeit $p$ ist der geometrische Kurzgap-Bias exakt herleitbar:

$$R_{\text{Poisson}} \approx (1-p)^{-6}$$

**Zweistufige Regularisierung:**
```
Poisson → [log-Dichte überdämpft] → Cramér → [Sieb verstärkt zurück] → Prime
  1.83                (-28%)           1.36          (+16%)            1.58
```

Die Primzahlen erzeugen **strukturierte Unordnung** zwischen Chaos und naiver Ordnung.

**WICHTIGE SPRACHPRÄZISIERUNG:**

Diese Hierarchie ist ein **empirisches Nullmodellresultat im untersuchten Bereich**, keine asymptotische Aussage. Die Primzahlfrage selbst ist damit nicht theoretisch gelöst.

**Status:** Die Gap-Asymmetrie ist **nicht primzahl-spezifisch**, sondern entsteht wesentlich aus der geometrischen Struktur sparse sets mit Kurzgap-Bias.

---

## 4. Offene Fragen

### 4.1 Modulo 30 ⭐⭐⭐⭐⭐ HÖCHSTE PRIORITÄT

**Warum mod 12 gefährlich ist:**
- $12 = 2^2 \cdot 3$ (kleinste Primzahlen wirken bereits)
- Beobachtete Struktur könnte aus Verboten durch 2 und 3 entstehen

**Warum mod 30 kritisch ist:**
- $30 = 2 \cdot 3 \cdot 5$ (erste ernsthafte Verallgemeinerung)
- 8 Restklassen: $\{1, 7, 11, 13, 17, 19, 23, 29\}$

**Entscheidungsfrage:**
- Falls ähnliche Zyklen → allgemeines Phänomen
- Falls nur mod 12 → spezielle mod-12-Vorasymptotik

**Dies ist der wichtigste Falsifikationsversuch.**

### 4.2 $R(X)$-Asymptotik

**Die interessanteste Grafik des gesamten Projekts:**

Datensequenz: $R(10^4) = 6.14 \to R(5 \times 10^4) = 4.59 \to R(10^5) = 4.05 \to R(5 \times 10^5) = 3.59$

**Drei Szenarien:**

1. **$R(X) \to 1$:** Vorasymptotik (z.B. $R(X) = 1 + c/(\log X)^\alpha$) ← **PLAUSIBELST**
2. **$R(X) \to c > 1$:** Persistente Asymmetrie
3. **$R(X)$ oszilliert:** Prime-Race-Phänomen

**Kritische Frage:**

$$\lim_{X \to \infty} R(X) = \, ?$$

**Entscheidend:** Messungen bei $X = 10^6, 10^7$

Falls $R(X) \to 1$: Konvergenzgeschwindigkeit messen
Falls $R(X) \to c > 1$: Vergleich mit etablierter Theorie notwendig

### 4.3 Sieb-/Hardy-Littlewood-Modelle

Falls persistente Asymmetrie: Vergleich mit Siebmodellen und Hardy-Littlewood-Heuristiken zur Einordnung des Phänomens.

---

## 5. Programme und Reproduzierbarkeit

### 5.1 Hauptprogramme (C++)

**Kern-Analyse (⭐ Publikationsrelevant):**
- `gap_distribution.cpp` - Bedingte Gap-Verteilung $P(g \bmod 12 \mid a)$ ⭐⭐⭐⭐
- `transition_matrix.cpp` - Übergangsmatrix $P(a \to b)$ ⭐⭐⭐
- `ratio_asymptotic.cpp` - $R(X)$-Asymptotik-Analyse ⭐⭐⭐⭐⭐
- `gap_distribution_windowed.cpp` - Fensterstabilität der Gap-Asymmetrie ⭐⭐⭐⭐⭐

**Nullmodell-Vergleiche:**
- `poisson_cramer_hierarchy.cpp` - Poisson-Cramér-Prime-Hierarchie ⭐⭐⭐⭐⭐⭐
- `verify_poisson_formula.cpp` - Verifikation: $R = (1-p)^{-6}$ ⭐⭐⭐⭐⭐⭐
- `cramer_comparison.cpp` - Cramér-Nullmodell-Vergleich ⭐⭐⭐⭐⭐

**Robustheitstests:**
- `chirality_robustness.cpp` - Konstruktionsabhängigkeit (random vs. consec)
- `autocorrelation_analysis.cpp` - Autokorrelationsanalyse und $Z_{\text{eff}}$

**EABC-Modell:**
- `eabc_analysis.cpp` - EABC-Klassifikation und Schichtzahlen

**Glatte Zahlen (Basis):**
- `smooth_numbers.cpp` - Basis-Implementierung
- `smooth_numbers_extended.cpp` - Erweiterte Features

### 5.2 Build und Ausführung

```bash
# Build-System
make                          # Alle Programme kompilieren

# Kern-Analysen ausführen
make demo-gaps                # Gap-Verteilung
make demo-transition          # Übergangsmatrix
make demo-ratio               # R(X)-Asymptotik

# Nullmodell-Hierarchie
make demo-poisson-hierarchy   # Poisson-Cramér-Prime-Vergleich

# Robustheitstests
make demo-robustness          # Konstruktionsabhängigkeit
make demo-autocorr            # Autokorrelation

# Vollständige Demo
make demo                     # Alle Demos
```

### 5.3 Voraussetzungen

- C++11 oder höher
- g++ oder clang++
- Optional: OpenMP für Parallelisierung

### 5.4 Datensätze

**Primzahlen:**
- Bis $10^5$ Primzahlen: Standard für Robustheitstests
- Bis $5 \times 10^5$: Asymptotik-Analysen
- Primzahl-Generierung via Sieb des Eratosthenes (eingebaut)

---

## 6. Dokumentation

### 6.1 Current Core

**Primäre Dokumente:**

- **`CHIRALITY_OBSERVABLES_v2.md`** ⭐⭐⭐ - Vollständige mathematische Formulierung (Research Note)
  - Bedingte Gap-Asymmetrien als primäres Phänomen
  - Vier-Ebenen-Hierarchie: $P(g \bmod 12 \mid a) \to P(a \to b) \to R(X) \to H_C(X)$
  - Orientierungsbias als abgeleitete Observable
  
- **`GAPS_ANALYSIS.md`** ⭐⭐⭐⭐ - Mechanistische Erklärung via Gap-Verteilung
  - Wie Gap-Asymmetrie die Übergangsmatrix erzeugt
  - Empirische Daten und Visualisierungen

- **`POISSON_ASYMMETRY_THEORY.md`** ⭐⭐⭐⭐⭐⭐ - Geometrischer Ursprung der Asymmetrie
  - Herleitung $R_{\text{Poisson}} \approx (1-p)^{-6}$ für konstante Bernoulli-Prozesse
  - Nullmodell erklärt wesentlichen Anteil der Asymmetrie

- **`NULL_MODEL_HIERARCHY.md`** ⭐⭐⭐⭐⭐⭐ - Poisson-Cramér-Prime-Hierarchie
  - Zweistufige Regularisierung: Poisson → Cramér → Prime
  - Strukturierte Unordnung zwischen Chaos und Ordnung

**Papers (PDF):**

- **`paper_geometric_origin.pdf`** ⭐⭐⭐⭐⭐⭐⭐ - Preprint (8 Seiten, 23. Juni 2026)
  - *The Geometric Origin of Residue-Class Gap Asymmetry in Sparse Arithmetic Point Processes*
  - Zentrale Formel: $R = (1-p)^{-6}$ (exakte Herleitung)
  - Empirische Hierarchie: $R_{\text{Poisson}} > R_{\text{Prime}} > R_{\text{Cramér}}$
  - Status: Preprint-ready für ArXiv/Journal-Submission

- **`paper.pdf`** ⭐⭐⭐ - Vollständiges Paper (12 Seiten, historisch)
  - *Bedingte Gap-Asymmetrien und Orientierungsbias in konsekutiven Primzahlrestklassen modulo 12*
  - Historische Entwicklung, vollständige Robustheitstests
  - Offene Fragen klar formuliert

**Robustheitstests:**

- **`ROBUSTNESS_TESTS.md`** - Dokumentation der kritischen Überprüfungen
  - Konstruktionsabhängigkeit (random vs. consec)
  - Autokorrelationsanalyse
  - Nichtüberlappende Fenster

**Roadmap:**

- **`ROADMAP.md`** - Offene Fragen und nächste Schritte
  - Priorisierung: Modulo 30 > $R(X)$-Asymptotik > Sieb-Modelle

### 6.2 Historical

**Smooth Numbers (Ursprung):**

- **`MATHEMATICAL_DETAILS.md`** - Mathematische Grundlagen glatter Zahlen
  - Dickman-de Bruijn-Funktion
  - Verallgemeinerter Hamming-Algorithmus
  - Dreieck-Darstellung

**EABC-Modell:**

- **`EABC_MODEL.md`** - EABC/ABCE-Bamberg-Modell
  - Schichtzahlen $\sigma(n)$, Vektorzahlen $v(n)$
  - 4D-Gitterstruktur
  - Primzahlen vs. Glatte Zahlen ("Hart" vs. "Weich")

**Klein-Flasche (historische Motivation, heute nicht mehr Kern):**

- **`KLEIN_BOTTLE.md`** - Klein-Flaschen-Metapher
  - Ursprüngliche geometrische Intuition
  - **Status:** Aufgeprägte Geometrie, keine emergente Struktur
  - Historisch wertvoll, aber mathematisch nicht rigoros
  
- `klein_bottle.cpp` - Geometrische Visualisierung (historisch)

**Diskrete Topologie (Phase 1-2):**

- **`DISCRETE_TOPOLOGY.md`** - Früher topologischer Ansatz
  - $\chi = -1$ als "Euler-Charakteristik" (heuristisch)
  - Revidiert zugunsten Gap-Dynamik
  
- `eabc_chirality.cpp` - Diskrete Topologie aus Chiralitäten (historisch)

**Holonomie (Phase 2-3):**

- **`EABC_HOLONOMY.md`** - Frühere Holonomie-Formulierung
  - Vor Umbenennung in "Bias Function"
  - Konzeptionell überholt durch Vier-Ebenen-Hierarchie

**Lean 4 Formalisierung (optional, nicht weiterverfolgt):**

- **`LEAN_INTEGRATION.md`** - Formale Verifikation
  - Dickman-de Bruijn-Funktion in Lean 4
  - C++ ↔ Lean Bridge
- `DickmanFunction.lean` - Lean-Implementierung
- `dickman_bridge.cpp` - C++ Bridge

### 6.3 Exploratory

**Diese Dokumente sind mathematisch interessant, aber hochspekulativ und nicht validiert. Sie sollten NICHT als etablierte Resultate missverstanden werden.**

**Quantum Error Correction (separates Projekt):**

- **`quantum_error_correction.pdf`** - [[5,1,3]]-Stabilisatorcode (5 Seiten)
  - Vollständiges Rechenbeispiel für Z₁-Fehler
  - Syndrommessung, Fehlerdiagnose, Recovery-Operation
  - Präzisierung: Code-Projektor ≠ Fehlerkorrektur
  - Hurwitz-Einheiten = binäre Tetraedergruppe 2T (24 Elemente)
  - DMN/ECN-Metapher: Diskretisierung kontinuierlicher Störungen
  - **Status:** Vollständig dokumentiert als technische Referenz, separates Projekt

**Catalan-Hierarchien:**

- **`CATALAN_HIERARCHIES.md`** 🔬 - Catalan-Strukturen und arithmetische Baumhierarchien (23.06.2026)
  - Erweiterte EABC-Normalform mit Konstruktionshierarchie
  - Tamari-Gitter, arithmetische Baum-Komplexität $M_{\text{arith}}$
  - Spekulative Verbindung zu Quantum-Magic
  - **Status:** Mathematisch wohldefiniert, empirisch ungetestet
  - **Verweis:** Subprojekt `catalan-normalform/` für Details

**Gödel-Universum:**

- **`EMERGENT_STRUCTURES.md`** 🔬🔬 - Gödel-Universum und arithmetische Zyklen (23.06.2026)
  - Strukturelle Analogie: Gödel's rotierendes Universum ↔ EABC-Chiralität
  - Emergente Zeit ↔ Emergente Primzahlordnung
  - Geschlossene zeitartige Kurven (CTCs) ↔ EABC-Zyklen
  - **Status:** Hochspekulativ, metaphorisch, keine formale Abbildung
  - Philosophisch interessant, mathematisch nicht rigoros

**Hurwitz-Quaternionen:**

- Erwähnt im QEC-Kontext (Hurwitz-Einheiten = binäre Tetraedergruppe 2T)
- Keine eigenständige Dokumentation im Haupt-Repository

---

## 7. Status und nächste Schritte

### 7.1 Aktueller Stand (Juni 2026)

**Gesichert:**
- ✅ EABC-Klassifikation (exakte Arithmetik)
- ✅ Gauß-Eisenstein-Interpretation (algebraische Fundierung, Satz)
- ✅ Bedingte Gap-Asymmetrien modulo 12 im untersuchten Bereich
- ✅ Asymmetrische Übergangsmatrix $P(a \to b)$
- ✅ Erklärung des Orientierungsbias durch Gap-Dynamik
- ✅ Nullmodell-Hierarchie: Geometrischer Bias erklärt wesentlichen Anteil
- ✅ Robustheitstests bestanden (Konstruktionsabhängigkeit, Autokorrelation)

**Offen:**
- ❓ Konvergenz von $R(X)$ (Vorasymptotik vs. persistente Asymmetrie)
- ❓ Modulo-30-Verallgemeinerung (kritischer Falsifikationsversuch)
- ❓ Asymptotisches Verhalten von $P(g \bmod 12 \mid a)$
- ❓ Zusammenhang mit Siebmodellen und Hardy-Littlewood-Heuristiken

### 7.2 Prioritäten

**1. Modulo 30 ⭐⭐⭐⭐⭐ WICHTIGER ALS WEITERE X-VERGRÖSSERUNG**

Entscheidet: Allgemeines Phänomen vs. spezieller mod-12-Effekt

**2. $R(X)$-Asymptotik ⭐⭐⭐⭐⭐**

Messungen bei $X = 10^6, 10^7$ zur Entscheidung zwischen Vorasymptotik, persistenter Struktur oder Prime-Race-Phänomen

**3. Falls $R(X) \to 1$:**

Geschwindigkeit der Konvergenz messen (Form: $1 + c/(\log X)^\alpha$?)

**4. Falls $R(X) \to c > 1$:**

Siebmodell-Vergleich und Verbindung zu Prime Races etablieren

**5. Vollständige Verteilung:**

Alle 6 Signaturen, nicht nur $\chi$-Projektion

### 7.3 Wissenschaftlicher Status

**Das Projekt hat eine Form erreicht, die man ernst nehmen kann:**

✅ Die Definitionsbasis ist klar
✅ Metaphorische Elemente sind sauber von mathematischen Aussagen getrennt
✅ Die Beobachtungen sind reproduzierbar
✅ Die offenen Fragen sind explizit benannt
✅ Die kritischen Falsifikationspfade sind formuliert

**Gute Forschungsprogramme zeichnen sich nicht dadurch aus, dass sie bereits alle Antworten besitzen, sondern dadurch, dass sie klar sagen können:**
- Welche Beobachtungen gesichert sind
- Welche Mechanismen plausibel erscheinen
- Welche Fragen noch offen sind

**Von spekulativem Narrativ zu sauber definiertem Forschungsprogramm.**

### 7.4 Methodische Erkenntnis

**Die Evolution dieser Forschung:**

**Ausgangshypothese (Anfang 2026):**
"Vielleicht steckt eine geometrische oder topologische Struktur hinter den Primzahlen"

**Aktuelle Frage (Juni 2026):**
"Welche lokalen statistischen Gesetze erfüllen die Restklassenübergänge konsekutiver Primzahlen?"

**Dies ist ein großer methodischer Fortschritt.**

Von Objekten zu Dynamik, von Metaphern zu messbaren Observablen, von geometrischer Spekulation zu testbaren Nullmodellen.

---

## 8. Referenzen

### Etablierte Zahlentheorie

- **Dickman, K.** (1930): "On the frequency of numbers containing prime factors of a certain relative magnitude"
- **de Bruijn, N. G.** (1951): "On the number of positive integers ≤ x and free of prime factors > y"
- **Rubinstein-Sarnak** (1994): Prime Number Races (Chebyshev-Bias)
- **Hardy-Littlewood**: Heuristiken für Primzahltupel

### Smooth Numbers

- **Bernstein, D. J.** (2004): "How to find smooth parts of integers"
- **OEIS Sequence A080786**: Triangle of smooth number counts

### Algebraische Zahlentheorie

- **Quadratisches Reziprozitätsgesetz**: Spaltungsverhalten in $\mathbb{Z}[i]$ und $\mathbb{Z}[\omega]$

---

## 9. Anwendungen (Smooth Numbers)

Glatte Zahlen haben wichtige Anwendungen in:

- **Kryptographie:** Integer-Faktorisierung und diskrete Logarithmen
- **Algorithmik:** FFT-Algorithmen (Fast Fourier Transform)
- **Zahlentheorie:** Analyse von Primfaktorzerlegungen
- **Computergrafik:** Effiziente Bildauflösungen

---

## Lizenz

Dieses Projekt steht zur freien Verfügung für Bildungs- und Forschungszwecke.
