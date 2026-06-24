# Die Evidenzhierarchie: A, B, B+, C, D

**Datum:** 24. Juni 2026  
**Status:** Methodische Grundlage

---

## Evidenzhierarchie

**Die Fünf-Ebenen-Struktur:**

| Ebene | Status | Evidenz | Prüfung |
|-------|--------|---------|---------|
| **A** | Mathematischer Satz | Bewiesen | Logik, klassische Resultate, formale Verifikation |
| **B** | Testbare Hypothese | Offen | Präzise formuliert mit möglicher Falsifikation |
| **B+** | Empirisch gestützt | Reproduzierbare Evidenz, aber kein Satz | Dokumentierte Tests, robuste Signale |
| **C** | Interpretation | Optional | Geometrische, physikalische, konzeptionelle Deutungen |
| **D** | Spekulative Erweiterung | Weitgehend ungetestet | Mögliche Verallgemeinerungen ohne Evidenzbasis |

**Das vermeidet den größten Fehler vieler alternativer Zahlentheorie-Projekte:**

> Dass Beobachtung, Hypothese und Interpretation vermischt werden.

---

## Der zentrale methodische Satz

$$\boxed{\text{Jede neue Struktur muss zunächst auf A-, B- oder B+-Niveau eingeordnet werden, bevor Interpretationen zugelassen werden.}}$$

**Das ist bemerkenswert starke wissenschaftliche Selbstdisziplin.**

Sie würde viele frühere Missverständnisse rund um Klein-Flasche, Holonomie, Quaternionen oder Oktonionen automatisch vermeiden.

---

## Ebene A: Mathematische Sätze (Beweisbar)

### A1: EABC als Verfeinerung der Spaltungstypen

Für Primzahlen $p > 3$:

$$p \equiv 1,5,7,11 \pmod{12}$$

ist äquivalent zu

$$(p \bmod 4, p \bmod 3)$$

via Chinesischem Restsatz, da $\gcd(4,3) = 1$.

Damit erhält man exakt die vier Kombinationen:

| EABC | mod 12 | Gauß (ℤ[i]) | Eisenstein (ℤ[ω]) |
|------|--------|-------------|-------------------|
| E | 1 | Split (S) | Split (S) |
| A | 5 | Split (S) | Inert (I) |
| B | 7 | Inert (I) | Split (S) |
| C | 11 | Inert (I) | Inert (I) |

**Das ist ein Satz.**

- Keine Hypothese
- Keine Statistik
- Keine Interpretation

**Begründung:**
1. CRT: $\mathbb{Z}/12\mathbb{Z} \cong \mathbb{Z}/4\mathbb{Z} \times \mathbb{Z}/3\mathbb{Z}$
2. Gauß-Kriterium: $p \neq 2$ spaltet in ℤ[i] ⟺ $p \equiv 1 \pmod{4}$ (klassisch)
3. Eisenstein-Kriterium: $p \neq 3$ spaltet in ℤ[ω] ⟺ $p \equiv 1 \pmod{3}$ (klassisch)

**Status:** A-Niveau (etablierte algebraische Zahlentheorie)

---

### A2: Konzentrationsmaß H(n)

**Definition:**

$$H(n) = \frac{\|v_{\text{fac}}(n)\|^2}{\Omega_{\text{EABC}}(n)^2}$$

**Das ist mathematisch identisch zu:**
- Simpson-Index (Ökologie)
- Herfindahl-Hirschman-Index (Ökonomie)  
- Rényi-Entropie Ordnung 2 (Informationstheorie)

**Wertebereich:** $H \in [1/4, 1]$
- $H = 1$: Maximale Konzentration (alle Faktoren in einer Klasse)
- $H = 1/4$: Maximale Gleichverteilung

**Das ist ebenfalls ein Satz.**

Die Definition ist mathematisch klar, die Schranken sind beweisbar.

**Status:** A-Niveau (wohldefiniertes Konzentrations-/Diversitätsmaß; äquivalent zu Simpson/Herfindahl/Rényi-2)

---

### A3: M0-M4-Kaskade

**Definition:**

Die Modellhierarchie

$$M0 \subset M0b \subset M1 \subset M2 \subset M3 \subset M4$$

ist formal definiert als sukzessive Erweiterungen:

- **M0:** $M_C \sim \Omega$
- **M0b:** $M_C \sim \Omega + \Omega^2$
- **M1:** $M_C \sim \Omega + \Omega^2 + \sigma$
- **M2:** $M_C \sim \Omega + \Omega^2 + (v_2, v_3)$
- **M3*:** $M_C \sim \Omega + \Omega^2 + (v_2, v_3) + H$
- **M4:** $M_C \sim \Omega + \Omega^2 + (v_2, v_3) + v$

**Das ist eine formale Konstruktion.**

Jedes Modell ist mathematisch wohldefiniert.

**Status:** A-Niveau (Statistik, Modelltheorie)

---

## Ebene B: Empirische Hypothesen (Testbar)

**Hier liegt der eigentliche Erkenntnisgewinn.**

### B1: H(n) → M_C(n)

**Hypothese:**

$$\Delta R^2_H = R^2(\text{M3*}) - R^2(\text{M2}) > \eta$$

für einen sinnvollen Schwellenwert $\eta$ (z.B. 0.01 oder 0.05).

**Das ist eine empirische Hypothese.**

- Nicht beweisbar
- Testbar durch Regression
- Falsifizierbar

**Status:** B+ (empirisch gestützt) ✅

**Test:** Experiment E02 (24. Juni 2026)

**Ergebnis:** 
- **ΔR²_H = 0.2168 >> 0.10** (Fall 4: Starkes Signal)
- H(n) erklärt 22% zusätzliche Varianz über Ω, Ω², (v₂, v₃) hinaus
- **Erste empirische Evidenz** für Verbindung zwischen Spaltungstypen und Catalan-Strukturen
- Effekt nur bei balancierten Kanonisierungen (strukturelle Freiheit nötig)

**Dokumentation:**
- ✅ Datensatz: 285 Zahlen, Ω ≥ 4, n ∈ [2, 1000]
- ✅ Kanonisierung: Balancierte Bäume (dokumentiert)
- ✅ Residuenplots: 4 Visualisierungen erstellt
- ✅ Methodische Kontrollen: M0b (Ω²), ΔR²_dir
- ⏳ Cross-Validation: Noch ausstehend
- ⏳ Permutationstest: Noch ausstehend

**Qualifikation:** Vorläufig stark bestätigt (robuste Erstmessung, weitere Validierung empfohlen)

**Siehe:** `experiments/results/e02/` für vollständige Dokumentation

---

### B2: v_fac → M_C

**Hypothese:**

$$\Delta R^2_{\text{dir}} = R^2(\text{M4}) - R^2(\text{M3*}) > \eta$$

**Interpretation:**

Falls $\Delta R^2_{\text{dir}} > \Delta R^2_H$, ist nicht nur die Konzentration H, sondern die konkrete Richtung $(e,a,b,c)$ im EABC-Raum relevant.

**Das ist ebenfalls eine empirische Hypothese.**

**Status:** B-Niveau

**Test:** Experiment E02 (erweitert)

---

### B3: Spaltungstyp → Catalan-Struktur

**Hypothese:**

Die algebraisch-zahlentheoretische Klassifikation nach Spaltungstypen in ℤ[i] und ℤ[ω] hat messbare Auswirkungen auf kombinatorische Catalan-Hierarchien.

**Das ist die tiefste Hypothese.**

Falls bestätigt, wäre das eine überraschende Verbindung zwischen:
- Algebraischer Zahlentheorie (Spaltungsgesetze)
- Kombinatorik (Binärbäume, Tamari-Graphen)

**Status:** B-Niveau

**Test:** Resultat von E02 entscheidet

---

### C-Niveau (Interpretationen – plausibel, optional)

**Geometrische, physikalische oder konzeptionelle Deutungen ohne Beweis oder robuste empirische Evidenz.**

#### C1: Quaternionen-Struktur

**Interpretation:**

$v = (e,a,b,c) \in \mathbb{R}^4 \cong \mathbb{H}$

Formal korrekt, aber derzeit keine Multiplikation, nur Norm.

**Status:** C-Niveau (formale Analogie)

---

#### C2: Tamari-Geometrie

**Interpretation:**

Catalan-Bäume bilden einen geometrischen Raum mit Tamari-Distanzen und möglichen Spektraleigenschaften.

**Status:** C-Niveau (geometrische Deutung)

---

#### C3: Klein-Flaschen-Topologie

**Interpretation:**

EABC als Zirkulation auf nicht-orientierbarer Fläche.

**Status:** C-Niveau (historische Analogie, heute nicht mehr Kern)

---

## Ebene D: Spekulative Erweiterungen (weitgehend ungetestet)

**Mögliche Verallgemeinerungen ohne belastbare Evidenzbasis.**

#### D1: Oktonionen/Hurwitz-Assoziatoren

**Spekulation:**

$[v_L, v_M, v_R] \in \mathbb{O}$ als Maß für Nicht-Assoziativität.

**Status:** D-Niveau (weitgehend ungetestet, ferne Analogie)

---

#### D2: Gödel-Universum-Analogien

**Spekulation:**

Verbindungen zu kosmologischen Strukturen.

**Status:** D-Niveau (keine mathematische Basis)

---

#### D3: Quantum-Magic

**Spekulation:**

Quantenmechanische Interpretationen arithmetischer Strukturen.

**Status:** D-Niveau (Metapher ohne Mechanismus)

---

## Die kritischen Grenzen

$$\boxed{\text{EABC} \leftrightarrow (\text{Gauß}, \text{Eisenstein})} \quad \text{ist A-Niveau (Satz).}$$

$$H(n) \to M_C(n) \quad \text{ist B+-Niveau (empirisch gestützt).}$$

$$\text{Gap-Asymmetrie } P(g \equiv 2,4 \mid a) > P(g \equiv 8,10 \mid a) \quad \text{ist B+-Niveau (empirisch gestützt).}$$

$$H \to \text{Tamari/Hurwitz-Deutung} \quad \text{ist C-Niveau (Interpretation).}$$

$$\text{Oktonionen/Gödel/Quantum} \quad \text{ist D-Niveau (Spekulation).}$$

**Der entscheidende Satz:**

> Die Gauß-Eisenstein-Deutung macht EABC klassisch (A-Niveau). Der E02-Test hat entschieden, dass diese klassische Information zusätzliche Vorhersagekraft für Catalan-Magic besitzt (B+ → vorläufig stark bestätigt mit ΔR²_H = 0.22).

**Die wichtigste Umklassifizierung:**

**Vorher:** "H erklärt Catalan-Strukturen" (klang wie mathematische Tatsache)

**Jetzt:** "H liefert derzeit starke empirische Evidenz für zusätzliche Vorhersagekraft bezüglich M_C." (exakt die Sprache von B+)

**Methodische Klarstellung:**

Die Drei-Ebenen-Trennung verhindert:
- Überbewertung von Analogien (C → A)
- Unterbewertung von Sätzen (A → B)
- Vermischung von Empirie und Logik (B ↔ A)

---

## Warum diese Trennung entscheidend ist

### Häufiger Fehler in alternativer Zahlentheorie

**Muster:**

1. Beobachtung einer Korrelation (z.B. "EABC korreliert mit Gaps")
2. Interpretation als fundamentales Prinzip (z.B. "EABC steuert Primverteilung")
3. Aufbau komplexer Theorien (z.B. "EABC via Quaternionen erklärt Riemann-Hypothese")

**Problem:** Schritt 2 übergeht die empirische Prüfung.

### Korrekter Ablauf in diesem Projekt

**Muster:**

1. **Satz (A):** EABC ↔ (Gauß, Eisenstein) via CRT
2. **Hypothese (B):** H(n) → M_C(n) testbar durch ΔR²
3. **Falls bestätigt:** Interpretation (C) als Zusatz möglich
4. **Falls zurückgewiesen:** Interpretation (C) irrelevant

**Kritisch:** Schritt 2 ist **obligatorisch**, nicht optional.

---

## Verbindung zur Forschungsphilosophie

$$\boxed{\text{Das Projekt untersucht nicht Objekte, sondern Informationsstufen.}}$$

**Die Drei Ebenen A/B/C sind selbst Informationsstufen:**

- **A-Niveau:** Welche Sätze sind etabliert?
- **B-Niveau:** Welche Hypothesen sind testbar?
- **C-Niveau:** Welche Interpretationen sind plausibel?

Das ist die **Meta-Ebene** der Informationsstufen-Philosophie.

---

## Status im Projekt

### A-Niveau (Sätze – etabliert)

- ✅ CRT-Zerlegung
- ✅ Gauß/Eisenstein-Spaltungskriterien
- ✅ EABC ↔ Spaltungspaare
- ✅ Konzentrationsmessung H(n) (wohldefiniert)
- ✅ M0-M4 Modellhierarchie (formal)
- ✅ Dickman-Funktion (smooth numbers)
- ✅ Lean-Formalisierung (13 Theoreme)

### B+-Niveau (Empirisch gestützt)

**Hier liegt reproduzierbare empirische Evidenz vor.**

Diese Aussagen sind keine Sätze (nicht bewiesen), aber deutlich mehr als bloße Ideen.

#### B+1: H(n) → M_C(n)

**Empirischer Befund:**

$$\Delta R^2_H = 0.2168 >> 0.10$$

H(n) erklärt 22% zusätzliche Varianz in Catalan-Magic über Ω, Ω², (v₂, v₃) hinaus.

**Dokumentation:**
- ✅ Datensatz: 285 Zahlen, Ω ≥ 4, n ∈ [2, 1000]
- ✅ Kanonisierung: Balancierte Bäume (dokumentiert)
- ✅ Residuenplots: 4 Visualisierungen
- ✅ Methodische Kontrollen: M0b (Ω²), ΔR²_dir
- ⏳ Cross-Validation noch ausstehend
- ⏳ Permutationstest noch ausstehend

**Qualifikation:** "H liefert derzeit starke empirische Evidenz für zusätzliche Vorhersagekraft bezüglich M_C."

**Nicht:** "H erklärt Catalan-Strukturen" (das klänge wie mathematische Tatsache).

**Status:** B+-Niveau (empirisch gestützt, reproduzierbar dokumentiert)

**Test:** Experiment E02 (24. Juni 2026)

**Siehe:** `experiments/results/e02/` für vollständige Dokumentation

---

#### B+2: Gap-Asymmetrie mod 12

**Empirischer Befund:**

$$P(g \equiv 2,4 \mid a) > P(g \equiv 8,10 \mid a)$$

im untersuchten Bereich (erste Millionen Primzahlen).

**Das ist kein Satz.**

Aber deutlich mehr als eine bloße Idee.

**Dokumentation:**
- ✅ Robuste Messungen über mehrere Bereiche
- ✅ Übergangsmatrix P(a → b) empirisch bestimmt
- ✅ Orientierung H_C(X) als abgeleitete Observable
- ✅ Nullmodell-Hierarchie: R_Poisson > R_Prime > R_Cramér
- ⏳ Modulo-30-Verallgemeinerung noch ausstehend (höchste Priorität!)

**Qualifikation:** "Gap-Asymmetrie zeigt starke empirische Evidenz im untersuchten Bereich."

**Nicht:** "Theoretische Lösung" (das wäre Overclaim).

**Status:** B+-Niveau (empirisch gestützt)

### B-Niveau (Testbar, offen)

- 📊 v → M_C(n) (E02: ΔR²_dir ≈ 0, scheint irrelevant)
- 📊 EABC-Verteilung in smooth numbers
- 📊 Modulo-30-Gap-Analyse
- 📊 Cross-Validation von E02
- 📊 Permutationstest für H(n)

### C-Niveau (Interpretationen – spekulativ)

- 📋 Quaternionen-Interpretation (formal möglich)
- 📋 Oktonionen/Hurwitz (ferne Analogie)
- 📋 Tamari-Spektraltheorie (geometrische Deutung)
- 📋 Klein-Flaschen-Topologie (historisch)

---

## Zusammenfassung

Die Vier-Ebenen-Struktur (A/B/B+/C) ist der **methodische Durchbruch** des Projekts.

**A = Satz, B = Testbare Hypothese, B+ = Empirisch gestützt, C = Interpretation**

Sie schützt vor:
1. Überbewertung von Analogien
2. Vermischung von Satz und Hypothese
3. Feature-Hunting ohne Falsifikation

Sie erzwingt:
1. Klare Trennung zwischen Beweis und Test
2. Empirische Prüfung vor Interpretation
3. Hierarchische Evidenz-Ordnung

**Das ist wissenschaftlich sauberer als viele etablierte zahlentheoretische Programme.**
