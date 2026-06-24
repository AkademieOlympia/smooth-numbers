# Zeit-, Raum- und Richtungs-Aequivalente im EABC/Catalan/Gap-Programm

## Ziel und Rahmen

Dieses Dokument legt fuer den aktuellen Forschungsraum eine defensiv-mathematische Abbildung von Zeit, Raum und Richtung fest. Die Begriffe werden so definiert, dass daraus unmittelbar falsifizierbare Tests folgen.

- **Kontrollachsen (invariant orientiert):** `M_C`, `Omega`, `S`
- **Signalachsen (symmetry-breaking orientiert):** `DeltaH_cramer`, `H(Delta-r)`, `Q_cramer`
- **Status:** Stage 5.5/5.6 positiv, Stage 6 Holdout aktiv

Notation:

- Skalenmenge `N_set = {10^6, 10^7, 2*10^7}`
- Gap-Klassen `G = {2,6,10,14,18}`
- Signalvektor pro Skala `x_N(dr) = (DeltaH_cramer(N,dr), Q_cramer(N,dr))`

---

## 1) Zeit-Aequivalente

### T1: Skalenzeit `t_scale = log10(N)`

- **Formale Definition:** `t_scale` ordnet jeder Auswertungsskala `N` einen geordneten Zeitparameter zu.
- **Plausibilitaet:** Das Programm arbeitet bereits explizit skalenweise (`10^6 -> 10^7 -> 2*10^7`). Diese Ordnung ist der natuerliche "Evolutionsindex" der Statistik.
- **Messbarkeit:** Direkt aus `N` in `experiments/results/stage56/stage56_summary_table.csv` und `experiments/results/stage6/stage6_holdout_table.csv`.
- **Invarianz / Symmetriebruch:**
  - Invarianz-konsistent: `M_C`, `Omega`, `S` bleiben strukturstabil ueber `t_scale`.
  - Symmetriebruch-konsistent: Grad/Amplitude von `DeltaH_cramer`, `Q_cramer` darf sich mit `t_scale` geordnet veraendern, ohne die Drift-Richtung zu verlieren.

### T2: Delta-r-Schrittzeit `t_gap = i`, mit `dr_i in G`

- **Formale Definition:** `t_gap` ist der Positionsindex innerhalb der geordneten Gap-Klassen.
- **Plausibilitaet:** Mehrere bestehende Tests behandeln `dr` als geordnete Klasse; damit entsteht eine diskrete "interne Zeit" entlang der Gap-Struktur.
- **Messbarkeit:** Aus den `delta_r`-Feldern in Stage 5.6/6 Outputs.
- **Invarianz / Symmetriebruch:**
  - Invarianz: Permutationsinvarianz wuerde geringe Sensitivitaet gegen Index-Umsortierungen bedeuten.
  - Beobachtet: Noether-Scan klassifiziert Gap-Permutationen fuer `H(Delta-r)`, `DeltaH_cramer`, `Q_cramer` als `strong_symmetry_breaking`; damit ist `t_gap` ein aktiver Signalparameter.

### T3: Fit-/Holdout-Zeit `t_fit = (protocol, fold)`

- **Formale Definition:** `t_fit` indiziert den Lern-/Validierungszustand ueber Fold-Sequenzen (`delta_r_leave_one_out`, `cross_scale_leave_one_scale_out`).
- **Plausibilitaet:** Stage-6-Entscheidungen werden entlang dieser Sequenz getroffen; damit ist dies operative Zeit im Modellvergleich.
- **Messbarkeit:** Aus `protocol`, `fold_id`, `rank`, `test_rmse` in `stage6_holdout_table.csv`.
- **Invarianz / Symmetriebruch:**
  - Invarianz: Gewinnerfamilie bleibt ueber Folds stabil.
  - Symmetriebruch: Rank-Inversionen oder starke Fold-Sensitivitaet markieren gebrochene Modellsymmetrie.

---

## 2) Raum-Aequivalente

### S1: Diskreter Gap-Raum `R_gap = (G, d_gap)`

- **Formale Definition:** Raum der Gap-Klassen mit Metrik `d_gap(dr_i, dr_j) = |dr_i - dr_j|`.
- **Plausibilitaet:** `dr` ist bereits zentrale Strukturvariable der Signalachsen.
- **Messbarkeit:** Distanz- und Nachbarschaftstests direkt aus Stage-5.6-Werten je `dr`.
- **Invarianz / Symmetriebruch:**
  - Invarianz: Signal waere unabhaengig von `d_gap`.
  - Symmetriebruch: Amplitude oder Quotient variiert systematisch mit `d_gap`.

### S2: Beobachtungsraum `R_obs subset R^k`

- **Formale Definition:** Punktwolke pro `(N,dr)` in Features wie `(DeltaH_30_cramer, Q_30_cramer, DeltaH_210_cramer, R_210)`.
- **Plausibilitaet:** Das ist der reale "Datenraum", in dem Stage-6-Familien fitten.
- **Messbarkeit:** Aus `stage56_summary_table.csv` und `stage6_holdout_table.csv`.
- **Invarianz / Symmetriebruch:**
  - Invarianz: stabile Cluster-/Projektionsstruktur ueber `N`.
  - Symmetriebruch: anisotrope Geometrie (z. B. dominant entlang einer Achse) oder skalenabhaengige Deformation.

### S3: Transformationsraum `R_sym`

- **Formale Definition:** Endliche Transformationsfamilien `T` aus Noether-Scan (Zyklen, Spiegelungen, Transpositionen, wheel30/wheel210-Permutationen).
- **Plausibilitaet:** Das ist die explizite Symmetriegruppe des Programms.
- **Messbarkeit:** `I_norm`, `classification` je `(Observable, T)` in `experiments/results/noether/noether_invariance_table.csv`.
- **Invarianz / Symmetriebruch:**
  - Invarianz: kleine `I_norm` (z. B. `M_C`, `Omega`, `S`).
  - Symmetriebruch: grosse `I_norm` bei Gap-Observablen.

---

## 3) Richtungs-Aequivalente

### D1: Drift-Richtung im Gap-Raum

- **Formale Definition:** Vorzeichen/Slope von `dr -> Q_cramer(N,dr)` (oder `R_210` als robuste Kontrollvariante).
- **Plausibilitaet:** Stage 5.5 zeigt monotone Quotientendrift; Richtung ist damit zentraler Signaltraeger.
- **Messbarkeit:** Spearman `rho`, lineare Slope, Vorzeichenstabilitaet der Differenzen `Q(dr_{i+1})-Q(dr_i)`.
- **Invarianz / Symmetriebruch:**
  - Invarianz: keine bevorzugte Richtung (`rho ~ 0`).
  - Symmetriebruch: robuste gerichtete Drift (`rho > 0` mit stabiler Orientierung).

### D2: Modellrichtungsvektor im Fehlerraum

- **Formale Definition:** Differenzvektor der Holdout-Fehler zwischen Modellfamilien, z. B. `Delta e = RMSE_power - RMSE_linear`.
- **Plausibilitaet:** Richtung im Fehlerraum kodiert, welche Familien systematisch besser sind.
- **Messbarkeit:** `summary.leaderboard` und `by_target_leaderboard` in `stage6_model_params.json`.
- **Invarianz / Symmetriebruch:**
  - Invarianz: keine konsistente Vorteilrichtung.
  - Symmetriebruch: konsistenter Vorteil einer Familie entlang derselben Fehler-Richtung.

### D3: Spektralrichtung (Fiedler/PC1) auf Gap-Graph

- **Formale Definition:** Projektion eines Signals `y(dr)` auf die Fiedler-Richtung des Pfadgraphen ueber `G` oder auf die erste PCA-Richtung im Beobachtungsraum.
- **Plausibilitaet:** Verdichtet gerichtete Struktur in eine reproduzierbare Achse statt punktweiser Vergleiche.
- **Messbarkeit:** Korrelations-/Projektionskoeffizienten zwischen `y` und Fiedler-Vektor bzw. PC1-Loadings.
- **Invarianz / Symmetriebruch:**
  - Invarianz: Projektion nahe Null, instabiles Vorzeichen.
  - Symmetriebruch: signifikante Projektion mit stabilem Vorzeichen ueber `N`.

---

## 4) Priorisierte Hypothesen (H16-Style)

### H16-T (Zeit: Skalenpfeil)

Fuer `N in {10^6, 10^7, 2*10^7}` bleibt die Drift-Richtung in `dr -> Q_cramer(N,dr)` bzw. `dr -> R_210(N,dr)` gleichgerichtet (`rho > 0` auf jeder Skala), auch wenn die Amplitude variiert.

### H16-T2 (Zeit: Holdout-Stabilitaet)

Die Top-2-Modellfamilien nach Holdout-RMSE bleiben ueber beide Protokolle konsistent; insbesondere bleibt eine strukturierte Familie (`linear` oder `power`) vor `constant`.

### H16-S (Raum: Distanzabhaengigkeit)

Die Symmetriebruch-Amplitude `|DeltaH_cramer|` waechst im Mittel mit `d_gap` (positiver Zusammenhang zwischen `dr` und Signalstaerke), statt raeumlich homogen zu sein.

### H16-S2 (Raum: Geometrische Anisotropie)

Im Beobachtungsraum liegt eine dominante erste Richtung (PC1/Fiedler-Projektion) vor, die einen substanziellen Anteil der Signalvarianz traegt.

### H16-D (Richtung: robuste Vorzugsrichtung)

Die Quotientensignale besitzen eine robuste Vorzugsrichtung: positive lokale Differenzen `Q(dr_{i+1})-Q(dr_i)` sind in klarer Mehrheit und das Vorzeichen der Spektralprojektion bleibt ueber `N` stabil.

---

## 5) Sofort testbare Operationalisierung

Direkt mit vorhandenen Outputs:

- `experiments/results/stage56/stage56_summary_table.csv`
- `experiments/results/stage6/stage6_holdout_table.csv`
- `experiments/results/stage6/stage6_model_params.json`
- `experiments/results/noether/noether_invariance_table.csv`

Empfohlene minimale Probe ist in `code/experiments/stage6_equivalent_axes_probe.py` implementiert und schreibt:

- `experiments/results/stage6/stage6_equivalent_axes_probe.csv`

Diese Probe liefert bereits Kennzahlen zu:

- Zeitpfeil (Skalen- und Fold-Stabilitaet),
- Raumabhaengigkeit (Gap-Distanz vs. Signalgeometrie),
- Richtungsstabilitaet (monotone Drift, Fiedler/PC1-nahe Indikatoren).
