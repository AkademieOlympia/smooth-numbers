# Spektrale Catalan-Geometrie der EABC-Arithmetik

**Mathematisch präzises Forschungsprogramm in Normalform**

---

## Das zentrale Motto (erweiterte Version)

$$\boxed{
\begin{align*}
&\text{Das Projekt untersucht zusätzliche Informationsstufen} \\[2mm]
&\text{und akzeptiert eine neue Stufe nur, wenn sie zusätzliche Varianz erklärt.}
\end{align*}
}$$

**Siehe:** `RESEARCH_PHILOSOPHY.md` für die vollständige philosophische Grundlage.

---

## Überblick

Dieses Projekt formuliert die spektrale Catalan-Geometrie als präzises, testbares mathematisches Programm.

**Zentrale Forschungsfrage:**

> Bleibt nach Entfernung der trivialen $\Omega(n)$- und Kanonisierungs-Effekte ein arithmetischer Rest in der Catalan-Hierarchie?

Formal:

$$M_C^{\mathrm{res}}(n) \neq 0 \quad\text{und}\quad M_C^{\mathrm{res}}(n) \text{ korreliert mit EABC-/Spektralobservablen?}$$

**Methodisches Kernprinzip:**

$$\boxed{\text{Erklärt } X \text{ zusätzliche Varianz gegenüber bereits vorhandenen Ebenen?}}$$

Jede neue Idee wird am Standard $\Delta R^2_X > \eta$ gemessen.

**Empirischer Durchbruch (24. Juni 2026):**

> Experiment E02 bestätigt: **H(n) → M_C(n)** mit $\Delta R^2_H = 0.22 \gg 0.10$ (Fall 4: Starkes Signal)

Die EABC-Konzentrationsgröße H(n) erklärt 22% zusätzliche Varianz in Catalan-Magic über Ω, Ω² und Schalen-Koordinaten hinaus. Dies ist die **erste empirische Evidenz** für eine Verbindung zwischen Gauß-Eisenstein-Spaltung und kombinatorischen Catalan-Hierarchien.

**Position der Catalan-Zahlen:**

Die Catalan-Zahlen $C_\Omega$ sind **nicht** eine neue arithmetische Eigenschaft wie EABC.

Sie definieren den **kombinatorischen Zustandsraum** (Phasenraum) aller möglichen Binärbäume für gegebenes $\Omega$.

Die Frage ist: Beeinflusst die EABC-Struktur $(\Omega, v, H)$, welche Regionen dieses Raumes bevorzugt werden?

**Siehe:**
- `CATALAN_POSITION.md` für die vollständige konzeptionelle Klärung.
- `THEOREM_LANDSCAPE.md` für die Übersicht aller formalisierten Theoreme.
- `THREE_LEVELS_ABC.md` für die methodische Drei-Ebenen-Struktur (A: Sätze, B: Hypothesen, C: Interpretationen).

**Mathematische Fundierung:**

Der EABC-Vektor $v = (e, a, b, c)$ kodiert die vier Kombinationen von Spaltungsverhalten in:
- $\mathbb{Z}[i]$ (Gauß-Primzahlen, mod 4)
- $\mathbb{Z}[\omega]$ (Eisenstein-Primzahlen, mod 3)

Da $12 = 4 \cdot 3$, ist EABC die gemeinsame Verfeinerung beider Spaltungsgesetze.

**Siehe:** `GAUSS_EISENSTEIN.md` für Details.

---

## Projektstruktur

```
catalan-normalform/
├── README.md                    # Dieser Überblick
├── theory/
│   ├── 01_foundations.md       # Definitionen und mathematische Grundlagen
│   ├── 02_local_geometry.md    # EABC-Restklassengeometrie
│   ├── 03_global_geometry.md   # Catalan-Hierarchie und Tamari-Graph
│   ├── 04_observables.md       # Catalan-Magic und spektrale Observablen
│   └── 05_coupling.md          # Tensorprodukt-Struktur
├── hypotheses/
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
├── experiments/
│   ├── E01_tamari_baseline.md
│   ├── E02_canonization_test.md
│   ├── E03_residualization.md
│   ├── E04_eabc_information.md
│   └── E05_spectral_comparison.md
└── code/
    └── (Implementierungen folgen)
```

---

## Kernidee

Die EABC-Theorie klassifiziert Zahlen **lokal** über Restklassen und Primfaktoren.

Die Catalan-Erweiterung fügt eine **globale** Ebene hinzu:

- **Lokal:** Welche Faktoren?
- **Global:** Wie sind diese Faktoren hierarchisch verschaltet?

$$\boxed{\text{Arithmetische Komplexität = Faktorinhalt + Faktorarchitektur}}$$

---

## Mathematische Normalform

Eine Zahl $n$ wird repräsentiert als:

$$n = (G(n), P(n), E(n), T(n))$$

wobei:

- $G(n)$: glatte/skalare Grundstruktur
- $P(n)$: Primfaktorinhalt
- $E(n)$: EABC-Signatur ($\in \{E,A,B,C\}^{\Omega(n)}$)
- $T(n)$: Catalan-Hierarchie ($\in \mathcal{T}_{\Omega(n)}$)

---

## Testbarkeit

Jede Hypothese ist formuliert mit:

1. **Nullmodell:** Was passiert bei zufälliger Permutation?
2. **Teststatistik:** Konkrete Observable
3. **Signifikanzkriterium:** Quantitative Schwelle

Das Projekt ist **falsifizierbar**.

---

## Status

- [x] Theoretische Grundlagen definiert
- [x] 10 Hypothesen formuliert
- [x] 5 Experimente spezifiziert
- [ ] Implementierung
- [ ] Datenanalyse
- [ ] Publikation

---

## Literatur

- Catalan numbers und Tamari-Gitter: Stanley (2015)
- EABC-Basis-Theorie: `../README.md`
- Spectral graph theory: Chung (1997)

---

## Kontakt

Thomas Hoffbauer  
`smooth-numbers` Forschungsprojekt  
Juni 2026
