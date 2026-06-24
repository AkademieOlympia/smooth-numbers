# Catalan-Normalform: Projektübersicht

**Status:** Initialisierung abgeschlossen ✅  
**Datum:** 24. Juni 2026  
**Nächster Schritt:** E01 Tamari-Baseline (Woche 1-2)

---

## Projektstruktur

```
catalan-normalform/
├── README.md                      # Hauptübersicht
├── UNIFIED_ARCHITECTURE.md        # SVN-Catalan-Hierarchie ✅
├── THREE_LEVELS.md                # Architektur-Ebenen ✅
├── THREE_PILLARS.md               # Methodische Säulen ✅
├── RESEARCH_PHILOSOPHY.md         # Forschungsphilosophie ✅
├── CATALAN_POSITION.md            # Position der Catalan-Zahlen ✅
├── GAUSS_EISENSTEIN.md            # EABC als Gauß-Eisenstein-Verfeinerung ✅
├── CORE_PRINCIPLES.md             # Wissenschaftstheoretische Kernprinzipien ✅
├── EXPLORATORY_METHODOLOGY.md     # Universelles Framework für explorative Mathematik ✅
├── TWO_AXES.md                    # Die zwei Achsen des Fortschritts (Evidenz × Verständnis) ✅
├── THREE_DIMENSIONS.md            # Das 3D-Framework (Evidenz × Verständnis × Generativität) ✅
├── FOUR_DIMENSIONS.md             # Das 4D-Framework (+ Überraschung) ✅
├── FIVE_DIMENSIONS.md             # Das 5D-Framework (epistemische Spannung + Anschlussfähigkeit) ✅ ⭐ STABILE FORM
├── ENDFORM.md                     # Kompakte Zusammenfassung (eine Seite) ✅
├── EVIDENCE_CLASSIFICATION.md     # Vollständige A/B/B+/C/D-Einordnung ✅
├── FUTURE_H11_HURWITZ.md          # H11 Oktonionen ✅
├── theory/                        # 5 theoretische Kapitel ✅
│   ├── 01_foundations.md
│   ├── 02_local_geometry.md
│   ├── 03_global_geometry.md
│   ├── 04_observables.md
│   └── 05_coupling.md
├── hypotheses/                    # Hypothesen ✅
│   ├── H00_canonization.md        # H0: Fundamental
│   ├── H05_shell_stability.md     # H0.5: Schalen
│   ├── H06_norm_dominance.md      # H0.6: Norm
│   ├── H01_canonical_stability.md
│   ├── H02_ensemble_baseline.md
│   ├── H03_eabc_coupling.md
│   ├── H04_spectral_correlation.md
│   ├── H05_chaos_correlation.md
│   ├── H06_collatz_correlation.md
│   ├── H07_scale_law.md
│   ├── H08_curvature.md
│   ├── H09_tensor_spectrum.md
│   └── H10_null_model.md
├── experiments/                   # Experimente
│   ├── E01_tamari_baseline.md     ✅
│   └── E02_model_cascade.md       ✅ (M0-M4)
├── code/                          # Python-Implementierungen
│   ├── create_start_document.py  ✅
│   └── experiments/
│       └── e01_tamari_baseline.py ✅
└── lean/                          # Lean 4 Formalisierung ✅
    ├── lakefile.lean
    ├── README.md
    ├── CatalanNormalform.lean
    └── CatalanNormalform/
        ├── CTree.lean             # Stufe 1: Binäre Bäume
        ├── Rotation.lean          # Stufe 2: Tamari-Rotation
        ├── TamariGraph.lean       # Stufe 3: SimpleGraph
        ├── Magic.lean             # Stufe 4: Observablen
        ├── Arithmetic.lean        # Stufe 5: Primfaktoren, EABC
        ├── ShellVectorNorm.lean   # Stufe 6: SVN-Koordinaten ✅
        └── Hypotheses.lean        # Stufe 7: H10 Kaskade
```

---

## ✅ Was bereits existiert

### 1. Theoretische Grundlagen (Markdown)

Fünf sauber strukturierte Kapitel mit:
- Definitionen (CTree, Tamari-Graph, Catalan-Magic)
- Mathematischen Sätzen
- Literaturverweisen

### 2. Zehn testbare Hypothesen (Markdown)

Jede Hypothese mit:
- Formaler Formulierung
- Nullmodell
- Teststatistik
- Implementierungsvorschlag (Python-Pseudocode)
- Erwarteten Resultaten

**Kritisch:** H10 ist als härtester Test definiert, jetzt verfeinert als Kaskade H10a-c.

**Neu:** H0 (Kanonisierung), H0.5 (Schalenstabilität), H0.6 (Norm-Vorhersagekraft).

### 3. Experimentplan

**E01:** Tamari-Baseline (kombinatorischer Atlas)  
**E02:** M0-M4 Modellkaskade (zentrale Eliminationsarchitektur) ✅

Die M0-M4-Kaskade testet systematisch, wie viel von $M_C(n)$ durch SVN-Koordinaten erklärbar ist:
- M0: nur $\Omega$
- M1: $\Omega + \sigma$
- M2: $\Omega + (v_2, v_3)$
- M3: $\Omega + (v_2, v_3) + ||v_{\text{fac}}||^2$
- M4: $\Omega + (v_2, v_3) + v_{\text{fac}}$

### 4. Lean-Formalisierung

Vollständige kombinatorische Struktur in Lean 4:
- `CTree k`: Abhängiger Typ für Bäume
- Tamari-Rotation und Graph
- Catalan-Magic, EABC-Signatur
- **SVN-Koordinaten:** `shellHeight`, `shellBase`, `factorEABCVector`, `SVNCoordinates`
- **H10-Kaskade:** H10a (Ω), H10b (Ω + Schale), H10c (Ω + Schale + Norm)
- H10 als formales `Prop`

### 5. Start-Dokument (PDF)

Professionelles 7-seitiges PDF mit:
- Executive Summary
- Hypothesen-Übersicht
- Zielprojektion (2/6/12 Monate)
- Erfolgskriterien
- Risiken und Ressourcen

---

## 🔄 Aktuelle Entwicklungen

### Konzeptionelle Vereinheitlichung (Juni 2026) ✅

Die größte Entwicklung seit Projektstart:

**Integration der Schale-Vektor-Norm-Struktur:**

$$n \longmapsto \Bigl(\Omega(n),\, (v_2(n), v_3(n)),\, v_{\text{EABC}}(n),\, ||v_{\text{EABC}}(n)||^2\Bigr) \longmapsto T(n)$$

**Das transformiert das Projekt:**

1. **H0* (neu):** Kanonisierung nutzt SVN-Koordinaten statt nackte Faktoren
2. **H0.5 (neu):** Schalenstabilität – Zahlen gleicher Schale haben ähnliche Bäume
3. **H0.6 (neu):** Norm-Vorhersagekraft – $||v_{\text{fac}}||^2$ liefert Zusatzinfo
4. **H10-Kaskade:** H10a (Ω) → H10b (Ω + Schale) → H10c (Ω + Schale + Norm)
5. **Hurwitz natürlich:** Die Norm-Geometrie lädt zu algebraischer Fortsetzung ein

**Dokumentiert in:**
- `UNIFIED_ARCHITECTURE.md`: Die 6-Ebenen-Hierarchie
- `lean/CatalanNormalform/ShellVectorNorm.lean`: Formale Definitionen
- `experiments/E02_model_cascade.md`: M0-M4 Testkaskade
- `GAUSS_EISENSTEIN.md`: **EABC als Gauß-Eisenstein-Verfeinerung** ✅

### Mathematische Fundierung: Gauß-Eisenstein-Interpretation (24. Juni 2026) ✅

**Durchbruch:**

Die EABC-Klassifikation ist nicht willkürlich, sondern die **gemeinsame Verfeinerung zweier klassischer Spaltungskriterien** aus der algebraischen Zahlentheorie:

$$\text{EABC} \leftrightarrow (\text{Gauß-Spaltung mod 4}, \text{Eisenstein-Spaltung mod 3})$$

**Die vier Klassen:**

| EABC | mod 12 | ℤ[i] (Gauß) | ℤ[ω] (Eisenstein) |
|------|--------|-------------|-------------------|
| E    | 1      | Spaltet     | Spaltet           |
| A    | 5      | Spaltet     | Inert             |
| B    | 7      | Inert       | Spaltet           |
| C    | 11     | Inert       | Inert             |

**Warum 12 = 4 × 3?**

Chinesischer Restsatz: $\mathbb{Z}/12\mathbb{Z} \cong \mathbb{Z}/4\mathbb{Z} \times \mathbb{Z}/3\mathbb{Z}$

**Konsequenzen:**

1. **v = (e, a, b, c)** zählt nicht nur Restklassen, sondern **Spaltungstypen**
2. **H(n) = ||v||²/Ω²** misst **Konzentration von Spaltungsverhalten**
3. **Etablierte Mathematik (A-Niveau)**, keine Spekulation
4. **Lean-formalisiert** in `GaussEisenstein.lean` (13 Theoreme)

**Neue Dokumente:**
- `GAUSS_EISENSTEIN.md`: Mathematische Details
- `THEOREM_LANDSCAPE.md`: Übersicht aller formalisierten Theoreme
- `THREE_LEVELS_ABC.md`: Methodische Drei-Ebenen-Trennung (A: Sätze, B: Hypothesen, C: Interpretationen)
- `lean/CatalanNormalform/GaussEisenstein.lean`: 13 Theoreme

**Die kritische Grenze:**

$$\boxed{\text{EABC} \leftrightarrow (\text{Gauß}, \text{Eisenstein})} \quad \text{ist A-Niveau (Satz).}$$

$$H(n) \to M_C(n) \quad \text{ist B-Niveau (Hypothese, testbar via E02).}$$

**Verbindung zu Smooth Numbers:**

Orthogonale Klassifikationen:
- **EABC:** Qualitativ (Spaltungsverhalten)
- **Glattheit:** Quantitativ (Primzahlgrößen)

Siehe `THEOREM_LANDSCAPE.md` für Details.

---

### Methodischer Durchbruch: Drei-Ebenen-Struktur (24. Juni 2026) ✅

**Der entscheidende Fortschritt** ist nicht die Einführung einzelner Konzepte, sondern die **klare Trennung** von:

| Ebene | Status | Art | Prüfung |
|-------|--------|-----|---------|
| **A** | Mathematische Sätze | Beweisbar | Logik, CRT, klassische Resultate |
| **B** | Empirische Hypothesen | Testbar | ΔR², Statistik, Experimente |
| **C** | Interpretationen | Plausibel, optional | Analogien, geometrische Bilder |

**Das vermeidet den größten Fehler vieler alternativer Zahlentheorie-Projekte:**

> Dass Beobachtung, Hypothese und Interpretation vermischt werden.

**Siehe:** `THREE_LEVELS_ABC.md` für vollständige Details.

**Der zentrale Satz:**

$$\boxed{\text{Das Projekt untersucht nicht Objekte, sondern Informationsstufen.}}$$

Dieser Satz beschreibt sowohl das Gap-Programm (Modulo-30-Test) als auch das Catalan-Programm (M0-M4-Kaskade) präzise.

---

### Wissenschaftliche Präzisierungen (24. Juni 2026) ✅

**Korrigiert:**
1. **v(60)-Berechnung:** Nur $p > 3$ zählen für EABC-Vektor
2. **H0.6-Formulierung:** "Zusätzliche Vorhersagekraft" statt "Norm schlägt Rohfaktoren"
3. **Architektur:** Explizite SVN-Koordinaten $(\Omega, (v_2, v_3), v_{\text{EABC}}, ||v||^2)$
4. **M0-M4 Kaskade:** Systematische Testarchitektur als E02
5. **Hurwitz:** Quaternionen-Struktur erst bei Produkten relevant, nicht nur Norm

### Methodischer Durchbruch (24. Juni 2026) ✅

**Von Objekten zu Informationsstufen:**

Das Projekt hat den entscheidenden Übergang geschafft:

$$\boxed{\text{Theorie über Objekte} \longrightarrow \text{Theorie über Informationsstufen}}$$

**Neue Elemente:**

1. **M0b (nichtlineare Kontrolle):**  
   $M_C \sim \Omega + \Omega^2$ — schließt aus, dass Normeffekte nur $\Omega^2$-Effekte sind

2. **Konzentrationsgröße H(n):**  
   $$H(n) = \frac{||v_{\text{fac}}||^2}{\Omega_{\text{EABC}}^2}$$
   
   **Dimensionslos**, mathematisch äquivalent zu:
   - Simpson-Index (Ökologie)
   - Herfindahl-Hirschman-Index (Ökonomie)
   - Rényi-Entropie Ordnung 2 (Informationstheorie)
   
   **Interpretation:** Konzentration vs. Verteilung der Primfaktoren auf Restklassen
   
   **Wertebereich:** $H \in [1/4, 1]$
   - $H = 1$: Maximale Konzentration
   - $H = 1/4$: Maximale Gleichverteilung

3. **Kumulatives Forschungsprogramm:**  
   Jede neue Idee wird am Standard gemessen:
   
   $$\boxed{\text{Erklärt sie zusätzliche Varianz?}}$$

**Dokumentiert in:**
- `theory/concentration_measure.md`: Vollständige mathematische Analyse von $H(n)$
- `experiments/E02_model_cascade.md`: Erweitert um M0b und M3* (mit $H$)
- `../PRIORITIES.md`: Strategische Forschungsprioritäten

---

## 🎯 Das zentrale Motto (erweiterte Version)

$$\boxed{
\begin{align*}
&\text{Das Projekt untersucht zusätzliche Informationsstufen} \\[2mm]
&\text{und akzeptiert eine neue Stufe nur, wenn sie zusätzliche Varianz erklärt.}
\end{align*}
}$$

**Schutzregel gegen Feature-Hunting:**

$$\boxed{\text{Neue Variable erst dann aufnehmen, wenn sie unabhängig motiviert ist.}}$$

**Siehe:** `RESEARCH_PHILOSOPHY.md` für die Entwicklung von Objekten → Strukturen → Informationsstufen.

---

## Zentrale Forschungsfrage

```
┌─────────────────────────────────────────────────────────────────┐
│ Bleibt nach Entfernung der trivialen Ω(n)- und                 │
│ Kanonisierungs-Effekte ein arithmetischer Rest?                │
│                                                                 │
│ M_C^res(n) ≠ 0 und korreliert mit EABC/Spektralobservablen?   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📊 Go/No-Go-Entscheidung (Woche 3)

Nach E03 (Residualisierung) muss H10 getestet werden:

| Kriterium | Schwelle | H10-Status |
|-----------|----------|------------|
| R² | > 0.95 | bestätigt → STOP |
| Varianz-Ratio | < 0.05 | bestätigt → STOP |
| Normalität (p) | > 0.1 | bestätigt → STOP |
| EABC-Korrelation | < 0.1 | bestätigt → STOP |

**Falls H10 empirisch plausibel:** Projekt abbrechen, ehrliches Nullresultat berichten.  
**Falls H10 empirisch zurückgewiesen:** Weiter mit E04-E05 und H1-H9.

---

## 🔬 Methodische Stärken

1. **Falsifizierbarkeit:** H10 ist das Null-Modell
2. **Klare Teststatistiken:** Jede Hypothese hat Nullmodell + p-Wert
3. **Kombinatorischer Kern:** Tamari-Graph ist formal sauber
4. **Lean-Formalisierung:** Typsicherheit für Baumstrukturen
5. **Ehrliche Risikobewertung:** Negatives Resultat ist eingeplant

---

## 📅 Zeitplan

| Phase | Dauer | Inhalt |
|-------|-------|--------|
| **Woche 1-2** | 2 Wochen | E01: Tamari-Baseline (Graph-Konstruktion k≤12) |
| **Woche 3** | 1 Woche | E02: Kanonisierungstest + E03: Residualisierung |
| **Woche 3** | - | **Go/No-Go: H10-Test** |
| **Woche 4-6** | 3 Wochen | E04: EABC-Information, E05: Spektralvergleich |
| **Woche 7-8** | 2 Wochen | Erweiterte Tests (H7-H9), Visualisierungen |
| **Monat 3-6** | - | Publikationsvorbereitung, Preprint |

---

## 🛠️ Implementierungsstatus

### Lean (100% Struktur fertig)

✅ CTree-Datentyp mit abhängigen Indizes  
✅ Tamari-Rotation und SimpleGraph  
✅ Catalan-Magic, Ensemble-Magic  
✅ EABC-Signatur, Normalform  
✅ H10 als formales Prop  
⚠️ Einige Beweise mit `sorry` (Irreflexivität)  
⚠️ Axiome: Konnektivität, Catalan-Zahlen  

### Python (TODO)

⬜ E01: Tamari-Graph-Konstruktion  
⬜ E02: Kanonisierungstest  
⬜ E03: Residualisierung  
⬜ E04: EABC-Information  
⬜ E05: Spektralvergleich  
⬜ Visualisierungen (NetworkX, Matplotlib)  

### C++ (Optional)

⬜ Schnelle Primfaktorisierung (falls Python zu langsam)  
⬜ Graph-Enumeration (falls k > 12)  

---

## 📚 Kernliteratur

**Catalan-Zahlen:**
- Stanley, R. P. (2015). *Catalan Numbers*. Cambridge University Press.

**Tamari-Gitter:**
- Huang, S., & Tamari, D. (1972). Problems of associativity.
- Sleator, D., Tarjan, R., & Thurston, W. (1988). Rotation distance.

**Spektrale Graphentheorie:**
- Chung, F. (1997). *Spectral Graph Theory*. AMS.

**Diskrete Krümmung:**
- Ollivier, Y. (2009). Ricci curvature of Markov chains.
- Forman, R. (2003). Bochner's method for cell complexes.

**EABC-Basis:**
- Siehe `../README.md` im Hauptprojekt

---

## 🎓 Wissenschaftliche Integrität

Das Projekt ist methodisch sauber, weil:

1. **H10 wird zuerst getestet:** Null-Modell vor spekulativen Tests
2. **Go/No-Go ist explizit:** Klare Abbruchkriterien
3. **Negatives Resultat ist wertvoll:** Auch Falsifikation wird publiziert
4. **Lean diszipliniert Definitionen:** Keine handwaving
5. **Reproduzierbarkeit:** Code + Daten + Dokumentation

---

## 🚀 Nächster unmittelbarer Schritt

**E01: Tamari-Baseline implementieren**

```python
# catalan-normalform/code/experiments/e01_tamari_baseline.py

def construct_tamari_graph(k):
    """Konstruiert Γ_k für k Blätter."""
    trees = enumerate_all_trees(k)
    edges = []
    for t1 in trees:
        for t2 in trees:
            if is_tamari_adjacent(t1, t2):
                edges.append((t1, t2))
    return networkx.Graph(edges)

def compute_ensemble_magic(k):
    """Berechnet E[M_C | k]."""
    G = construct_tamari_graph(k)
    balanced = find_balanced_trees(k)
    magics = []
    for t in G.nodes():
        dist = min(nx.shortest_path_length(G, t, b) for b in balanced)
        magics.append(dist)
    return np.mean(magics)
```

**Lieferables:**
- Tabelle: |T_k|, diam(Γ_k), |B_k|, E[M_C(k)] für k=2,...,12
- Spektrum von L_C^(k) (Python NumPy)
- Visualisierung von Γ_4, Γ_5

---

## 📧 Kontakt

Thomas Hoffbauer  
smooth-numbers Forschungsprojekt  
Juni 2026

---

---

## 📝 Präzise Einordnung

```
┌──────────────────────────────────────────────────────────┐
│  Projekt- und methodenreif, aber noch nicht ergebnisreif │
└──────────────────────────────────────────────────────────┘
```

**Das bedeutet:**

✅ **Projekt-reif:** Struktur, Plan, Hypothesen sind vollständig  
✅ **Methoden-reif:** Teststatistiken, Nullmodelle, Lean-Scaffold fertig  
❌ **Noch nicht ergebnis-reif:** Keine empirischen Daten, H10 nicht getestet  

Dies ist **kein Nachteil** - es verhindert Overclaiming.

---

**Zusammenfassung:**

Das Catalan-Normalform-Projekt ist nun **strukturell vollständig initialisiert** mit:

- ✅ Theoretischer Grundlage (5 Kapitel Markdown)
- ✅ 10 testbaren Hypothesen
- ✅ Experimentplan
- ✅ Lean-Formalisierung (kombinatorischer Kern)
- ✅ Professionellem Start-Dokument (PDF)

**Nächster Schritt:** E01 Tamari-Baseline (Python-Implementierung).

**Kritischer Meilenstein:** Woche 3 - H10-Test (Go/No-Go-Entscheidung).

---

## 🔗 Vereinheitlichte Architektur (fundamentale Erkenntnis!)

**Schale-Vektor-Norm-Catalan** (siehe `UNIFIED_ARCHITECTURE.md`)

Die EABC-Arbeit besitzt bereits eine fundamentale Struktur, die **vor** Catalan kommt:

$$\text{Schale } S(n) \to \text{Vektor } v(n) \to \text{Norm } ||v|| \to \text{Catalan } T(n)$$

**Kernidee:** Kanonisierung sollte nicht $n \to T(n)$ sein, sondern:

$$\kappa: (S, v, ||v||) \to T$$

**Neue Hypothesen:**
- **H0.5:** Schalenstabilität - Bäume respektieren Schalen
- **H0.6:** Vektornorm-Dominanz - $M_C$ korreliert mit $||v||$

**Falls H0.6 erfüllt:** $M_C(n) = F(S(n), v(n), ||v(n)||)$ - massive Vereinfachung!

---

## 🔮 Zukünftige Erweiterung (nach H10!)

**H11: Hurwitz-Catalan-Hierarchie** (siehe `FUTURE_H11_HURWITZ.md`)

Falls H10 empirisch zurückgewiesen wird und H1-H9 erfolgreich sind,
könnte die natürliche algebraische Verfeinerung über die **Hurwitz-Algebren** laufen:

$$\mathbb{R} \subset \mathbb{C} \subset \mathbb{H} \subset \mathbb{O}$$

**Kernidee:** Bei Oktonionen wird $(ab)c \neq a(bc)$, daher werden Catalan-Bäume **algebraisch relevant**.

**Wichtig:** Dies ist eine **zukünftige** Erweiterung, nicht Teil des aktuellen Programms.
