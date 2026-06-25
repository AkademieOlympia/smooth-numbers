# H16: Diskrete Pfadsumme auf Catalan-Baeumen (defensive Forschungsnotiz)

Stand: 2026-06-25

Ziel dieser Notiz ist eine formal klare, testbare und defensiv formulierte Verbindung zwischen
Catalan-Pfaden der multiplikativen Rekonstruktion und einer Feynman-inspirierten,
rein diskreten Pfadsummen-Schreibweise.

## 1) Formales Setup (streng diskret)

### 1.1 Pfadmenge

Fuer ein fixes `n` mit geordneter Faktorenliste der Laenge `k := Omega_tot(n)` gilt:

- Anzahl voller Binaerbaeume (Klammerungen): `|Pi(n)| = C_{k-1} = C_{Omega_tot(n)-1}`.
- `Pi(n)` bezeichnet die endliche Menge dieser Rechenbaeume.

Wichtig:

- Das ist **kein** Kontinuums-Pfadintegral.
- Es ist eine endliche, explizit auszaehlbare diskrete Summe ueber Rechenbaeume.

### 1.2 Diskrete Pfadsumme

Definiere fuer einen Pfad/Baum `pi in Pi(n)` eine Aktion `S(pi) in R`.

Dann:

- gedaempfte (reell-positive) Variante:
  `Z(n; beta) = sum_{pi in Pi(n)} exp(-beta * S(pi))`, mit `beta >= 0`.
- optional formale oszillatorische Variante:
  `Z_osc(n; beta) = sum_{pi in Pi(n)} exp(i * beta * S(pi))`.

Defensiver Hinweis:

- `Z_osc` wird hier nur als formale Alternative notiert.
- Es wird **keine** physikalische Dynamik oder Quantisierung behauptet.

### 1.3 Zwischenprodukte

Ein Pfad `pi` induziert Zwischenprodukte `q^(k)` an internen Knoten des Rechenbaums.
Alle vorgeschlagenen Aktionen werden entlang dieser diskreten Zwischenprodukte ausgewertet.

## 2) Action-Kandidaten (testbar, austauschbar)

`||.||` ist ein positiv-definiter Normproxy auf den Zwischenprodukten.
`Delta H(q^(k))` bezeichnet den Schrittzuwachs einer additiven Signaturgroesse.

### S1: log-Norm-Akkumulation

`S1(pi) = sum_k log(1 + ||q^(k)||)`

Eigenschaft:

- stets endlich fuer `||q^(k)|| >= 0`,
- robust gegen einzelne grosse Normwerte (log-Daempfung).

### S2: Kruemmungsproxy-Akkumulation

`S2(pi) = sum_k kappa(q^(k))`, mit defensiver Modellwahl `kappa(q) ~ 1 / (||q|| + eps)`, `eps > 0`.

Hinweis:

- `kappa` ist hier ein technischer Proxy, kein geometrischer Krummungsbeweis.

### S3: Signatur-Gradient entlang des Pfads

`S3(pi) = sum_k ||Delta H(q^(k))||_1`

Interpretation:

- misst diskrete Signaturaenderung entlang der Baumtrajektorie,
- ohne physikalische Interpretation.

### Optionale Normalisierung

Zur Vergleichbarkeit ueber unterschiedliche `k`:

- `S1_norm = S1 / (k-1)`,
- `S2_norm = S2 / (k-1)`,
- `S3_norm = S3 / (k-1)`.

## 3) Hypothesenblock H-PI1 .. H-PI8

Alle Hypothesen sind als **testbare Arbeitsannahmen** formuliert.

- `H-PI1 (dominante Pfade)`:
  Fuer geeignete `beta` konzentriert sich das Gewichtsspektrum auf wenige Pfade
  (`w_pi = exp(-beta*S(pi))/Z`), statt nahezu gleichverteilt zu bleiben.

- `H-PI2 (Interferenz-/Klassenidee, formal)`:
  In der formalen oszillatorischen Variante zeigen bestimmte Pfadklassen
  (z. B. nach Baumtiefe/Balancing gruppiert) systematische Ausloeschung oder Verstaerkung.

- `H-PI3 (universelle Aktionsdichte)`:
  Die normierte Aktionsdichte `S(pi)/(k-1)` zeigt ueber verschiedene `n`
  mit gleichem `Omega_tot` eine stabile Verteilungsform.

- `H-PI4 (Pfadentropie)`:
  Die Gewichtsverteilung besitzt eine charakteristische Entropieskalierung
  mit `Omega_tot`, statt rein trivialer Catalan-Skalierung.

- `H-PI5 (Noether-analoge Invarianzen im Baumraum)`:
  Bestimmte diskrete Baumtransformationen lassen gewichtete Summen observabler
  Groessen invariant (analoger Symmetriebegriff, kein Noether-Theorem-Claim).

- `H-PI6 (beta-Konzentrationsuebergaenge)`:
  Es existieren Schwellenbereiche in `beta`, in denen die effektive Zahl
  relevanter Pfade abrupt sinkt (Cross-over, nicht als Phasenuebergang behauptet).

- `H-PI7 (EABC/ASL-Kopplung bei invariantem Endzustand)`:
  Trotz invariantem Endzustand (`H_end`) koennen pfadgewichtete Mittel
  bestimmter rekonstruktiver Groessen systematisch mit EABC/ASL-Merkmalen variieren.

- `H-PI8 (Tuple-Sensitivitaet)`:
  Das Gewichtsspektrum reagiert unterschiedlich auf Faktormuster
  (Zwillinge, Drillinge, Vierlinge, gemischte Cluster) bei vergleichbarem `Omega_tot`.

## 4) Minimales numerisches Protokoll

### 4.1 Inputs

- Menge von `n` mit kleinen bis mittleren `Omega_tot` (z. B. `3..8`).
- Pro `n`: geordnete Faktorenliste, definierte Aktion (`S1`/`S2`/`S3`), `beta`-Raster.

### 4.2 Enumerationsstrategie (kleine Omega)

- Fuer kleine `Omega_tot`: exhaustive Enumeration aller `C_{Omega_tot-1}` Baeume.
- Fuer groessere `Omega_tot`: reproduzierbares Sampling mit Seed und klarer Budgetgrenze.
- Immer reporten: `mode in {exhaustive, sampled}`.

### 4.3 Messgroessen

- Gewichtsspektrum: `{w_pi}`.
- Effektive Pfadanzahl: `N_eff = 1 / sum_pi w_pi^2`.
- Entropie: `H_w = -sum_pi w_pi log(w_pi)`.
- Top-k-Gewichtsanteil (z. B. `k=1,3,5`).
- Optional: Klassengewichte nach Baumtopologie-Features.

### 4.4 Null-/Robustheitschecks

- `beta=0` als Flachverteilungskontrolle.
- Label-/Leaf-Permutationscheck bei fixem Faktormultiset.
- Alternative Aktionen (`S1/S2/S3`) gegeneinander.
- Sensitivitaet gegen Normdefinition (`||.||`) und `eps` in `S2`.
- Reproduzierbarkeit ueber Seeds (im Sampling-Modus).

### 4.5 Reporting-Template (Beobachtung vs Interpretation)

Empfohlenes Schema pro Experiment:

1. **Setup:** `n`-Menge, `Omega`-Bereich, Aktion, `beta`-Raster, Enumerationsmodus.
2. **Beobachtung:** rein deskriptive Kennzahlen (`N_eff`, Entropie, Top-k, Verteilungen).
3. **Interpretation (defensiv):** nur als kompatible Lesart, keine Mechanismusbehauptung.
4. **Limitierung:** Enumerationsgrenzen, Proxy-Wahl, Sampling-Unsicherheit.
5. **Naechster Test:** klarer, falsifizierbarer Folgeschritt.

## 5) Einordnung und Grenzen

- Diese Notiz erweitert die Catalan-Pfadperspektive um eine **diskrete Gewichtung**.
- Sie ersetzt keine bestehenden Invarianzresultate fuer Endzustandsgroessen.
- Sie liefert eine testbare Sprache fuer Pfaddominanz/Pfadentropie bei fester Endsignatur.
- Es werden bewusst keine physikalischen Overclaims erhoben.

## 6) Offene Fragen

- Welche Aktionsfamilien bleiben numerisch stabil unter Norm-/Skalenwechsel?
- Welche Topologie-Features von Baeumen tragen die meiste Varianz in `S(pi)`?
- Gibt es robuste universelle Reskalierungen ueber `Omega_tot` hinaus?
- Wie stark koppeln die Effekte an konkrete Faktormuster (Tuple-Sensitivitaet)?
- Welche Teile lassen sich spaeter formal (nicht nur empirisch) absichern?

## 7) Minimaler Code-Starter

- Script-Skelett (TODO-basiert, nicht-invasive Basis):
  `code/experiments/h16_path_integral_catalan.py`
- Erwartete Stub-Outputs beim Lauf:
  - `experiments/results/h16_path_integral/h16_run_config.json`
  - `experiments/results/h16_path_integral/h16_stub_output.json`
