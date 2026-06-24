# Experimentplan-Übersicht

## Experimente-Verzeichnis

Dieser Ordner enthält detaillierte Spezifikationen der 5 Kernexperimente.

### Experimenteller Workflow

```
E01 → E02 → E03 → E04 → E05
 ↓                         ↓
Baseline            Publikation
```

---

## E01: Tamari-Baseline

**Datei:** `E01_tamari_baseline.md`

**Ziel:** Die reine Catalan-Geometrie verstehen (ohne arithmetische Aspekte).

**Aufgaben:**
- Konstruiere Tamari-Graphen $\Gamma_k$ für $k = 2, \ldots, 12$
- Berechne Durchmesser, mittlere Distanz, Spektrum
- Finde balancierte Bäume $\mathcal{B}_k$
- Berechne Ensemble-Magic $\overline{M}_C(k)$

**Lieferbar:**
- Tabelle: $|\mathcal{T}_k|$, $\operatorname{diam}(\Gamma_k)$, $|\mathcal{B}_k|$, $\overline{M}_C(k)$
- Spektren: $\{\lambda_j^{(k)}\}$ für alle $k$

**Dauer:** 2 Wochen

---

## E02: Kanonisierungstest

**Datei:** `E02_canonization_test.md`

**Ziel:** Prüfen, ob Catalan-Magic von der Kanonisierung abhängt.

**Aufgaben:**
- Berechne $M_C^{T_L}(n)$, $M_C^{T_R}(n)$, $M_C^{T_B}(n)$ für $10^6$ Zahlen
- Berechne paarweise Korrelationen
- Entscheide über Hypothese H1

**Lieferbar:**
- Korrelationsmatrix
- Streudiagramme
- Entscheidung: stabil oder instabil?

**Dauer:** 1 Woche

---

## E03: Residualisierung

**Datei:** `E03_residualization.md`

**Ziel:** Trivialen $\Omega(n)$-Effekt entfernen.

**Aufgaben:**
- Stratifiziere Zahlen nach $k = \Omega(n)$
- Berechne $M_C^{\mathrm{res}}(n) = M_C(n) - \overline{M}_C(k)$
- Analysiere Varianzzerlegung

**Lieferbar:**
- Residuen-Verteilung
- Varianz-Verhältnis $\sigma_{\mathrm{within}}^2 / \sigma_{\mathrm{between}}^2$
- Test von Hypothese H2

**Dauer:** 1 Woche

---

## E04: EABC-Information

**Datei:** `E04_eabc_information.md`

**Ziel:** Messen, ob EABC-Signatur die Catalan-Hierarchie beeinflusst.

**Aufgaben:**
- Berechne Mutual Information $I(M_C^{\mathrm{res}}; E(n) \mid \Omega(n))$
- Permutationstest: zufällige EABC-Labels
- Chi-Quadrat-Test pro Signaturklasse

**Lieferbar:**
- Mutual Information (bits)
- p-Wert
- Entscheidung über Hypothese H3

**Dauer:** 2 Wochen

---

## E05: Spektralvergleich

**Datei:** `E05_spectral_comparison.md`

**Ziel:** Korrelation mit bekannten EABC-Observablen testen.

**Aufgaben:**
- Berechne $M_{C,\varepsilon}^{\mathrm{spec}}$ (spektrale Catalan-Magic)
- Korreliere mit $M_{\mathrm{near-zero}}(D_{420})$
- Korreliere mit Brody-Parameter $q_{\mathrm{Brody}}$
- Korreliere mit Collatz-Stopzeit $\tau(n)$

**Lieferbar:**
- Korrelationstabelle (H4, H5, H6)
- Streudiagramme
- p-Werte

**Dauer:** 2 Wochen

---

## Gesamtdauer

**8 Wochen** (Kernexperimente)

Danach: Erweiterte Analysen (H7-H9) und Publikationsvorbereitung.

---

## Kritischer Pfad

**Woche 3:** Nach E03 muss H10 (Null-Modell) getestet werden.

**Go/No-Go Entscheidung:**

- Falls $R^2 > 0.95$ (H10 bestätigt): Projekt abbrechen
- Falls $R^2 < 0.85$ (H10 falsifiziert): Weiter mit E04-E05

---

## Datenmanagement

Alle Experimentdaten werden gespeichert unter:

```
catalan-normalform/
└── data/
    ├── tamari/          # E01: Graph-Daten
    ├── canonization/    # E02: Kanonisierungs-Tests
    ├── residuals/       # E03: Residuen
    ├── eabc_coupling/   # E04: EABC-Information
    └── spectral/        # E05: Spektralvergleiche
```

Format: CSV, NumPy `.npy`, oder JSON für Metadaten.

---

## Reproduzierbarkeit

Jedes Experiment erhält ein zugehöriges Python-Skript in `code/experiments/`:

- `e01_tamari_baseline.py`
- `e02_canonization_test.py`
- `e03_residualization.py`
- `e04_eabc_information.py`
- `e05_spectral_comparison.py`

Alle Skripte verwenden feste Random Seeds für Reproduzierbarkeit.
