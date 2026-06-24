# Projektübersicht: Catalan-Normalform

## Executive Summary

Dieses Projekt formuliert die **spektrale Catalan-Geometrie der EABC-Arithmetik** als präzises, testbares mathematisches Forschungsprogramm.

**Kernfrage:**

> Enthält die hierarchische Verschaltung von Primfaktoren (Catalan-Struktur) arithmetische Information jenseits der bloßen Faktoranzahl $\Omega(n)$?

**Formale Hypothese:**

$$M_C^{\mathrm{res}}(n) = M_C(n) - \mathbb{E}[M_C(n) \mid \Omega(n)] \stackrel{?}{\neq} 0$$

und korreliert mit EABC-/Spektral-/Chaos-Observablen.

---

## Projektstruktur

```
catalan-normalform/
├── README.md                          # Projektübersicht (diese Datei oben)
├── OVERVIEW.md                        # Diese Datei
├── theory/                            # Mathematische Grundlagen (5 Kapitel)
│   ├── 01_foundations.md             # Catalan-Zahlen, Bäume, Kanonisierung
│   ├── 02_local_geometry.md          # EABC-Restklassengeometrie
│   ├── 03_global_geometry.md         # Tamari-Graph, Associahedron, Krümmung
│   ├── 04_observables.md             # Catalan-Magic und spektrale Observablen
│   └── 05_coupling.md                # Tensorprodukt, gekoppelter Hamiltonian
├── hypotheses/                        # 10 testbare Hypothesen
│   ├── H01_canonical_stability.md    # Kanonisierung ist robust
│   ├── H02_ensemble_baseline.md      # Residuum ist signifikant
│   ├── H03_eabc_coupling.md          # EABC beeinflusst Catalan
│   ├── H04_spectral_correlation.md   # Spektrale Observablen korrelieren
│   ├── H05_chaos_correlation.md      # Brody-Parameter korreliert
│   ├── H06_collatz_correlation.md    # Collatz-Stopzeit korreliert
│   ├── H07_scale_law.md              # Skalengesetz ~ (log log X)^θ
│   ├── H08_curvature.md              # Krümmung korreliert mit Magic
│   ├── H09_tensor_spectrum.md        # Übergangsregime bei α ≈ β
│   └── H10_null_model.md             # WICHTIG: Negatives Kontrollmodell
├── experiments/                       # 5 experimentelle Fahrpläne
│   ├── E01_tamari_baseline.md        # Reine Catalan-Geometrie
│   ├── E02_canonization_test.md      # Test Hypothese C1
│   ├── E03_residualization.md        # Test Hypothese C2 (KRITISCH!)
│   ├── E04_eabc_information.md       # Test Hypothese C3
│   └── E05_spectral_comparison.md    # Test Hypothese C4
└── code/                              # Implementierungen (folgen)
    ├── catalan_trees.py              # Baumgenerierung
    ├── tamari_graph.py               # Graph-Konstruktion
    ├── observables.py                # Catalan-Magic-Berechnungen
    └── experiments.py                # Experimentskripte
```

---

## Abhängigkeiten zwischen Komponenten

### Theorie-Hierarchie

```
01_foundations.md
    ↓
02_local_geometry.md → 03_global_geometry.md
    ↓                       ↓
    ↓→→→→→→ 04_observables.md →→→→→
                    ↓
            05_coupling.md
```

### Experiment-Abhängigkeiten

```
E01_tamari_baseline (unabhängig, muss zuerst laufen)
    ↓
E02_canonization_test (parallel zu E03)
    ↓
E03_residualization (KRITISCHER STOPP-PUNKT)
    ↓
    ├─→ E04_eabc_information
    └─→ E05_spectral_comparison
```

**WICHTIG:** Falls **E03** negativ ausfällt (Residuum ist trivial), **STOPP**.

### Hypothesen-Testfolge

```
H10 (Null-Modell)  ← ZUERST TESTEN!
    ↓ (falsifiziert)
    ├─→ H01 (Kanonisierung)     → E02
    ├─→ H02 (Residuum)          → E03
    ├─→ H03 (EABC-Kopplung)     → E04
    ├─→ H04 (Spektralkorr.)     → E05
    ├─→ H05 (Chaos)             → (benötigt eabc-qubit)
    ├─→ H06 (Collatz)           → (benötigt Collatz-Daten)
    ├─→ H07 (Skalengesetz)      → (benötigt große Ensembles)
    ├─→ H08 (Krümmung)          → (benötigt E01)
    └─→ H09 (Tensorspektrum)    → (benötigt vollständige Implementierung)
```

---

## Kritischer Pfad

### Phase 1: Grundlagen (Woche 1-2)

1. **E01: Tamari-Baseline**
   - Konstruiere $\Gamma_k$ für $k = 2, \ldots, 12$
   - Berechne Spektren, Distanzen, Krümmung
   - **Output:** `tamari_baseline.json`

2. **Code-Infrastruktur**
   - Baumgenerierung
   - Tamari-Graph
   - Observable-Berechnungen

### Phase 2: Kanonisierung (Woche 3)

3. **E02: Kanonisierungstest**
   - Teste H01
   - **Entscheidung:** Welche Kanonisierung für weitere Experimente?

### Phase 3: Kritischer Test (Woche 4)

4. **E03: Residualisierung**
   - Teste H02 und H10
   - **STOPP-KRITERIUM:** Falls Residuum trivial ist, Ende des Projekts

### Phase 4: Kopplungstests (Woche 5-6, nur falls Phase 3 positiv)

5. **E04: EABC-Information**
   - Teste H03
   - Mutual Information

6. **E05: Spektralvergleich**
   - Teste H04
   - Spektrale Korrelationen

### Phase 5: Erweiterte Tests (Woche 7-8, optional)

7. **H05-H09:** Chaos, Collatz, Skalengesetz, Krümmung, Tensorspektrum

---

## Zeitplan (optimistisch)

| Phase | Dauer | Aktivität |
|-------|-------|-----------|
| 1     | 2 Wochen | Grundlagen (E01, Code) |
| 2     | 1 Woche | Kanonisierung (E02) |
| 3     | 1 Woche | Residualisierung (E03) **← KRITISCH** |
| 4     | 2 Wochen | Kopplungstests (E04, E05) |
| 5     | 2 Wochen | Erweiterte Tests |
| 6     | 2 Wochen | Publikation |

**Total:** ~10 Wochen

---

## Erwartete Resultate

### Szenario A: Triviales Resultat (Wahrscheinlichkeit ~40%)

- **E03 negativ:** Residuum ist trivial ($R^2 > 0.95$)
- **H10 bestätigt:** Catalan-Magic ist nur Funktion von $\Omega(n)$
- **Publikation:** Kurze Note, negatives Resultat

### Szenario B: Schwaches Signal (Wahrscheinlichkeit ~40%)

- **E03 marginal:** Residuum ist klein aber signifikant ($0.05 < R^2 < 0.15$)
- **E04-E05 gemischt:** Einige Korrelationen, aber schwach
- **Publikation:** Technische Note mit Vorbehalt

### Szenario C: Starkes Signal (Wahrscheinlichkeit ~20%)

- **E03 positiv:** Residuum ist groß ($R^2 > 0.2$)
- **E04-E05 positiv:** Klare Korrelationen mit EABC und Spektrum
- **Publikation:** Vollständiges Paper, neue Observable

---

## Publikationsstrategie

### Falls Szenario A

**Titel:** "Catalan Hierarchies in Prime Factorization: A Null Result"

**Journal:** arXiv Preprint + kurze Note in Journal of Integer Sequences

**Botschaft:** Die Faktorhierarchie ist kombinatorisch trivial.

### Falls Szenario B

**Titel:** "Weak Coupling between Factorization Hierarchy and EABC Residues"

**Journal:** Experimental Mathematics

**Botschaft:** Marginales Signal, weitere Untersuchung nötig.

### Falls Szenario C

**Titel:** "Spectral Geometry of Prime Factorization: Catalan Hierarchies and EABC Coupling"

**Journal:** Advances in Mathematics / Journal of Number Theory

**Botschaft:** Neue zahlentheoretische Observable mit spektralen Eigenschaften.

---

## Offene Fragen

1. **Kanonisierung:** Gibt es eine natürliche, ausgezeichnete Kanonisierung?
2. **Kopplung:** Falls H03 bestätigt, welche Kopplungsfunktion ist optimal?
3. **Spektrum:** Falls H04 bestätigt, was erklärt die Korrelation?
4. **Chaos:** Falls H05 bestätigt, kann man Brody-Parameter vorhersagen?
5. **Collatz:** Falls H06 bestätigt, neue Einsicht in Collatz-Vermutung?

---

## Nächste Schritte

1. **Lese alle Theoriekapitel** (theory/01-05)
2. **Studiere H10** (das wichtigste Nullmodell)
3. **Implementiere E01** (Tamari-Baseline)
4. **Entscheide:** Lohnt sich das Projekt? (nach E03)

---

## Kontakt & Diskussion

Bei Fragen oder Diskussionsbedarf:

- Projektleiter: Thomas Hoffbauer
- Hauptprojekt: `/Users/thomashoffbauer/Projects/smooth-numbers/`
- EABC-Qubit: `/Users/thomashoffbauer/Projects/smooth-numbers/eabc-qubit/`
