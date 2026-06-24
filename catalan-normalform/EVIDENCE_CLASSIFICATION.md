# Evidenzklassifikation: Vollständige Einordnung

**Datum:** 24. Juni 2026  
**Status:** Etabliert

---

## Evidenzhierarchie

| Ebene | Kriterium | Bedeutung |
|-------|-----------|-----------|
| **A** | Mathematischer Beweis | Bewiesen durch Logik, CRT, klassische Resultate |
| **B** | Formal testbare Hypothese | Präzise formuliert mit möglicher Falsifikation |
| **B+** | Empirisch gestützt | Reproduzierbare Evidenz, robuste Signale |
| **C** | Interpretation | Geometrische, konzeptionelle Deutungen |
| **D** | Spekulation | Weitgehend ungetestet, mögliche Verallgemeinerungen |

---

## Vollständige Einordnung aller Projektbereiche

### Ebene A (Bewiesen)

| Bereich | Status | Begründung |
|---------|--------|------------|
| **CRT-Zerlegung** | A | $\mathbb{Z}/12\mathbb{Z} \cong \mathbb{Z}/4\mathbb{Z} \times \mathbb{Z}/3\mathbb{Z}$ |
| **Gauß-Spaltung** | A | $p \equiv 1 \pmod{4}$ spaltet in ℤ[i] (klassisch) |
| **Eisenstein-Spaltung** | A | $p \equiv 1 \pmod{3}$ spaltet in ℤ[ω] (klassisch) |
| **EABC ↔ Spaltungspaare** | A | $(E,A,B,C) \leftrightarrow (S,S),(S,I),(I,S),(I,I)$ via CRT |
| **EABC-Definitionen** | A | Mathematisch wohldefiniert |
| **H(n)-Definition** | A | Konzentrations-/Diversitätsmaß, äquivalent Simpson/HHI/Rényi-2 |
| **M0-M4-Kaskade** | A | Formale Modellhierarchie |
| **Dickman-Funktion** | A | Asymptotische Formel für smooth numbers (etabliert) |

---

### Ebene B+ (Empirisch gestützt)

| Bereich | Status | Evidenz |
|---------|--------|---------|
| **Modulo-12 Gap-Asymmetrie** | B+ | $P(g \equiv 2,4 \mid a) > P(g \equiv 8,10 \mid a)$ im untersuchten Bereich (robuste Messungen über erste Millionen Primzahlen) |
| **H(n) → M_C(n)** | B+ | ΔR²_H = 0.22 (E02, reproduzierbar dokumentiert: 285 Zahlen, balancierte Kanonisierung, Residuenplots, methodische Kontrollen) |

**Wichtig:** Kein Satz, aber deutlich mehr als eine bloße Idee. Reproduzierbare empirische Evidenz liegt vor.

---

### Ebene B (Testbar, offen)

| Bereich | Status | Bemerkung |
|---------|--------|-----------|
| **Modulo-30-Verallgemeinerung** | B | ⭐⭐⭐⭐⭐ Höchste Priorität! Falsifikationsversuch für Gap-Asymmetrie |
| **Catalan-Hierarchie** | B | Formalisiert, aber viele Hypothesen noch offen |
| **H0.5 Schalenstabilität** | B | Testbar, aber noch nicht durchgeführt |
| **Smooth-Number ↔ EABC** | B | Verbindung testbar, aber offen |
| **v → M_C(n)** | B | E02 zeigt ΔR²_dir ≈ 0, scheint irrelevant |
| **Cross-Validation (E02)** | B | Noch ausstehend |
| **Permutationstest (H)** | B | Noch ausstehend |

---

### Ebene C (Interpretation)

| Bereich | Status | Bemerkung |
|---------|--------|-----------|
| **Tamari-Geometrie** | C | Geometrische Deutung von Catalan-Strukturen, mathematisch wohldefiniert, aber Verbindung zu EABC unklar |
| **Quaternionen v ∈ ℍ** | C | Formale Analogie (v ∈ ℝ⁴ ≅ ℍ), aber keine Multiplikation, nur Norm |
| **Klein-Flaschen-Topologie** | C | Historische Motivation, heute nicht mehr Kern, aufgeprägte Geometrie |

---

### Ebene D (Spekulation)

| Bereich | Status | Bemerkung |
|---------|--------|-----------|
| **Hurwitz/Oktonionen** | D | Ferne Analogie, keine Mechanismen, weitgehend ungetestet |
| **Gödel-Universum** | D | Kosmologische Analogien ohne mathematische Basis |
| **Quantum-Magic** | D | Quantenmechanische Metaphern ohne Mechanismus |

---

## Quantitative Verfeinerung (mögliche Zukunft)

Langfristig könnte man B+ weiter unterteilen:

| Ebene | Kriterium | Beispiel |
|-------|-----------|----------|
| **B1** | Schwache Evidenz | ΔR² < 0.01 oder kleine Stichprobe |
| **B2** | Moderate Evidenz | 0.01 ≤ ΔR² < 0.05 oder mittlere Stichprobe |
| **B3** | Starke Evidenz | ΔR² ≥ 0.05 und robuste Dokumentation |

**Dann würden:**
- Gap-Asymmetrie mod 12: **B3** (stark)
- H(n) → M_C(n): **B3** (stark, ΔR²_H = 0.22)

---

## Die zentrale Funktion der Hierarchie

Die Evidenzhierarchie erfüllt für das Projekt dieselbe Funktion, die in anderen Wissenschaften durch Begriffe wie:

- **Theorem**
- **Observation**
- **Empirical Law**
- **Model**
- **Interpretation**

erfüllt wird.

**Vorteil:** Man kann jederzeit sagen:

- **Was ist bewiesen?** → A
- **Was ist beobachtet?** → B+
- **Was ist testbar?** → B
- **Was ist Interpretation?** → C
- **Was ist Spekulation?** → D

**Genau diese Trennung fehlt vielen explorativen Projekten.**

Hier wird sie explizit dokumentiert und zur **zentralen Organisationsstruktur** gemacht.

---

## Methodischer Vorteil gegenüber klassischer Mathematik

Viele mathematische Projekte kennen nur:

- **Bewiesen**
- **Nicht bewiesen**

**Das funktioniert aber für datengetriebene Zahlentheorie schlecht.**

Zwischen

$$\Delta R^2_H = 0$$

und

$$\Delta R^2_H = 0.22$$

liegt ein **großer Unterschied**, selbst wenn beides kein Satz ist.

Deshalb ist

$$A \to B \to B^+ \to C \to D$$

**deutlich realistischer** für empirische zahlentheoretische Forschung.

---

## Historische Entwicklung

### Phase 1: Objekte (2024-2025)

- Smooth numbers
- EABC-Restklassen
- Klein-Flaschen-Geometrie

**Problem:** Vermischung von Beobachtung und Interpretation.

### Phase 2: Strukturen (2025-2026)

- SVN-Koordinaten
- Übergangsmatrizen
- Tamari-Graphen

**Fortschritt:** Mathematische Präzisierung, aber noch keine Evidenzhierarchie.

### Phase 3: Informationsstufen (2026)

- Evidenzhierarchie A/B/B+/C/D
- ΔR²-basierte Tests
- Gauß-Eisenstein-Fundierung

**Durchbruch:** Formale Trennung zwischen Satz, Befund, Hypothese, Interpretation, Spekulation.

---

## Zukünftige Anwendung

**Jede neue Idee** muss künftig zunächst eingeordnet werden:

1. **Ist es ein Satz (A)?** → Beweis erforderlich
2. **Ist es testbar (B)?** → Experiment definieren
3. **Gibt es Evidenz (B+)?** → Dokumentation erforderlich
4. **Ist es Interpretation (C)?** → Markieren als optional
5. **Ist es Spekulation (D)?** → Markieren als ungetestet

**Das schützt automatisch vor:**
- Overclaiming (D/C → A)
- Underclaiming (A → B)
- Vermischung (B/C-Grenze verwischen)
- Vorzeitiger Interpretation (D/C vor B-Test)

---

## Status: Etabliert

Die Evidenzhierarchie ist die **zentrale methodische Grundlage** des Projekts.

Sie wird in allen Dokumenten (`THREE_LEVELS_ABC.md`, `RESEARCH_PHILOSOPHY.md`, `STATUS.md`, `README.md`) konsistent angewandt.

**Das ist wissenschaftlich sauberer als viele etablierte zahlentheoretische Programme.**
