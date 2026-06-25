# HYPOTHESES_REGISTER

Stand: 2026-06-25

Dieses Register fuehrt aktive und relevante Hypothesen mit einheitlicher Ampel:

- `falsifiziert`: durch aktuelle Evidenz klar nicht gestuetzt.
- `nicht gestuetzt`: bisher kein belastbarer positiver Nachweis.
- `offen`: testbar, aber noch ohne robuste Entscheidung.
- `robust`: empirisch robust innerhalb des aktuellen Testdesigns (kein formaler Beweis).

## Hypothesenliste

| ID | Kurzbeschreibung | Aktuelle Evidenzlage | Status | Naechster klarer Test |
|---|---|---|---|---|
| `H10` | `I(M_C; S | Omega) > 0` (zus. Info von `M_C` fuer Schale `S=v2+v3`) | Mehrere Reports mit kleinen/instabilen Delta-R2, Permutation/CV ohne Signifikanz. | `falsifiziert` | Als kanonische Endfassung konsolidieren und H10 nur noch als negatives Ergebnis fuehren. |
| `H12` | Architekturachsen-Hypothese: `M_C` naeher an Baum-/Architekturachsen (`D`,`B`) als an Entropie-/Shellachsen | Grosses Sample bis `n=100000`, klare deskriptive Muster, aber noch keine starke OOS-/nichtlineare Validierung. | `offen` | Nichtlineare und OOS-Modelle mit Kanonisierungsvergleich (`balanced` vs Alternativen). |
| `H13-CAT-INV` | Typ: `theorem` (aktueller Stand: `empirical_robust`). `H(n)=(E,A,B,C)` ist fuer fixes `n` invariant gegen Catalan-Klammerung der `Omega_tot(n)`-Faktorliste. | Neue Catalan-Bridge-Probe zeigt auf testbaren Faellen keine Klammerungsabweichung in `H(n)`. Formale Lean-Fassung als Statement vorbereitet, aber nicht durchbewiesen. | `robust` | Skalenlauf mit hoeheren `Omega_tot` und systematischem Exhaustiv/Sampling-Mix; danach Lean-Lemma von Statement auf Beweisschritte heben. |
| `H14-CAT-GEO` | Typ: `empirical hypothesis`. Rekonstruktive Geometrie-Observablen koennen baum-/klammerungsabhaengig sein, auch wenn `H(n)` invariant bleibt. | Toy-Observable in der Probe zeigt baumabhaengige Werte fuer einzelne `n`; bewusst nicht als kanonische EABC-Groesse interpretiert. | `offen` | Mindestens zwei alternativ definierte rekonstruktive Observablen testen und gegen Null-/Shuffle-Baeume robustifizieren. |
| `H15-CAT-ROB` | Typ: `open method hypothesis`. Falls rekonstruktive Observable baumabhaengig sind, ist die Verteilung ueber alle Catalan-Baeume eine neue Signaturachse. | Konzeptuell plausibel, aber im aktuellen Lauf nur angedeutet (erste Streuungsstatistiken). | `offen` | Fuer ausgewaehlte `n` mit hoeherem `Omega_tot` vollstaendige Baumverteilungen (`mean/std/range`) und Skalierungsverhalten dokumentieren. |
| `H13` | Pivot-40-Distanzstruktur hat besondere EABC-Signatur | Unter strukturierten Pivots stark, gegen zufaellige Pivots nur teilweise extrem; explizite Warnungen vor Overclaim. | `nicht gestuetzt` | Skalierung (`p<1e7`) plus robuste Kontrollfamilien und M_C-Kopplungstest. |
| `H14` | Nachfolgerichtung: `M_C` gegen alternative Targets (`E(n)`, `H(n)`, `L(n)`, `chi(n)`) | In H10/H13-Dokumenten als naechste Hypothesenachse benannt; noch kein harter Ergebnisreport vorhanden. | `offen` | Priorisiert `M_C` vs `E(n)` und `M_C` vs `H(n)` mit Holdout-Protokoll. |
| `H16` | Diskrete Pfadsumme auf Catalan-Baeumen (H-PI1..H-PI8) als testbares Protokoll fuer Pfaddominanz/Entropie/Konzentration | Kanonische Definitionsnotiz neu erstellt; numerische Resultatserie steht noch aus. | `offen` | Baseline-Lauf mit kleinen `Omega_tot` (exhaustiv), dann `beta`-Sweep + Nullchecks (`beta=0`, Permutationscheck, Aktionsvergleich). |
| `H17` | ID in der aktuellen Repo-Leselage nicht sauber operationalisiert | Keine klar referenzierte Definition/Ergebnisdatei im gescannten Hauptbestand. | `offen` | Wie H16: erst testbares Protokoll definieren, dann Ergebnisartefakte erzeugen. |
| `H18-A/B/C/D` | Fibonacci/phi-Achse als Nulltest/Stabilitaetstest/Mehrwerttest/Rekurrenztest | Probe berichtet aktuell kein robustes phi-Signal; Dokumentation ist defensiv und falsifizierbar angelegt. | `nicht gestuetzt` | Mehr OOS-Schnitte, Nullmodelle und explizite Rekurrenzdiagnostik vor jeder positiven Interpretation. |
| `Stage-6` | OOS-Holdout auf Signalachsen (`DeltaH`, `H(Delta-r)`, `Q`) mit Modellfamilienvergleich | Reproduzierbares Holdout-Protokoll vorhanden; `baseline_power` oft vorn, aber Mechanismus bleibt offen. | `robust` | Skalen/Delta-r erweitern, HL-Singular-Series-Features verbessern, Wheel-210 Vergleich halten. |
| `Reachability-Bridge` | Notwendige Bedingung `n_min(phi) <= N` als strukturierende These fuer Erreichbarkeit | Empirisch stark unterstuetzt, in Lean aber noch als Axiom/Stub-Kette. | `offen` | `nMin` konstruktiv in Lean definieren und Axiom eliminieren. |

## Referenzen

- H10: `catalan-normalform/experiments/results/h10/H10_FINAL_SUMMARY.md`, `catalan-normalform/experiments/results/h10_final/H10_FINAL_REPORT.md`
- H12: `catalan-normalform/experiments/results/h12/H12B_ARCHITECTURE_AXES.md`
- H13-CAT-INV / H14-CAT-GEO / H15-CAT-ROB: `docs/CATALAN_EABC_BRIDGE.md`, `experiments/results/catalan_bridge/CATALAN_BRACKETING_INVARIANCE_REPORT.md`, `experiments/results/catalan_bridge/CATALAN_4FACTOR_PATH_PROTOCOL.md`
- H16: `docs/H16_PATH_INTEGRAL_CATALAN.md`, `code/experiments/h16_path_integral_catalan.py`
- H13: `catalan-normalform/experiments/results/h13/PIVOT_DISTANCE_ANALYSIS.md`
- H18: `docs/EABC_FIBONACCI_GOLDEN_RATIO.md`, `experiments/results/fibonacci_phi/FIBONACCI_PHI_PROBE.md`
- Stage-6: `experiments/results/stage6/STAGE6_HL_HOLDOUT_PROTOCOL.md`, `experiments/results/stage56/STAGE56_METHOD_BRAKES.md`
- Reachability: `experiments/results/reachability/REACHABILITY_PHI_REPORT.md`, `catalan-normalform/lean/CatalanNormalform/ReachabilityPhi.lean`

## Kepler-EABC Ladder (H0-H12, neue Struktur)

Hinweis:
- Diese Ladder ist ein separater Hypothesenstrang gemaess `HYPOTHESES_KEPLER_EABC.md`.
- Semantische Kollisionen mit Legacy-IDs (insb. frueheres `H10`/`H12`) werden bewusst nicht zu einem Claim verschmolzen.

| ID | TYPE | STATUS | Kurzbeschreibung | Naechster klarer Test |
|---|---|---|---|---|
| `H0` | `theorem` | `lean_proved` | Additiver 6D-Kern (`Phi`) unter Multiplikation mit Witnesses. | Lean-Rebuild + Theorem-Referenzen verifizieren. |
| `H1` | `theorem` | `lean_proved` | Mod-12-Paritaetsprojektion (`A/B/C` parity-only, `E` neutral). | Paritaetslemmas in Lean erneut pruefen. |
| `H2` | `theorem` | `lean_partial` | `e`/`R_v` auf Partitionstyp-Ebene invariant. | Echte Permutationsinvarianz als Zusatzlemma formalisieren. |
| `H3` | `theorem` | `lean_partial` | Kreis-Kriterium definitorisch ueber `e = 0`. | Beispiel- und Randfall-Lemmas erweitern. |
| `H4` | `theorem` | `lean_partial` | Exzentrizitaets-Kriterium definitorisch ueber `0 < e`. | Nichtdegenerate Faelle formal staerken. |
| `H5` | `speculative interpretation` | `statement_only` | `T=a^3` als formalisiertes Surrogat ohne Physik-Claim. | Monotonie-/Skalierungslemmas fuer `a,T` entwickeln. |
| `H6` | `asymptotic hypothesis` | `empirical_open` | Asymptotische Stabilisierung von Shape-Klassen. | Mehrskalen-Holdout mit festem Driftkriterium. |
| `H7` | `asymptotic hypothesis` | `empirical_open` | Grenzverhalten der Exzentrizitaetsverteilung. | Quantil-/Konvergenztests gegen Nullmodelle. |
| `H8` | `asymptotic hypothesis` | `empirical_open` | Large-scale-Trennung von `rCore/rEdge` gegen Baselines. | Bootstrap+Permutation auf Gap-Metriken. |
| `H9` | `theorem` | `lean_partial` | Zentrierter Vektor als additive Bruecke. | Additivitaetslemma weiter auf globale Kernfunktion heben. |
| `H10` | `speculative interpretation` | `statement_only` | Orientierung und Betrag als getrennte Objekte (noch keine starke Entkopplung). | Entkopplungsclaim nur nach OOS/MI-Tests aufwerten. |
| `H11` | `empirical hypothesis` | `empirical_open` | Clusterstabilitaet im Kepler-EABC-Raum. | Multi-Seed/Scale-Stability + Nullmodellvergleich. |
| `H12` | `empirical hypothesis` | `empirical_open` | Prime-race-Effekte entlang Cluster/Achsen. | OOS-Prime-Race-Protokoll mit Korrektur fuer Multiple Testing. |

Referenz:
- `HYPOTHESES_KEPLER_EABC.md` (kanonische Definitionsfassung fuer H0-H12).

## Register-Regeln

- Eine Hypothese bleibt `offen`, bis ein reproduzierbares Protokoll plus klares Entscheidungskriterium vorliegt.
- `robust` bedeutet robuste Empirie im gegebenen Design, nicht mathematischer oder Lean-Beweis.
- Aufwertungen muessen als diffbare Evidenz in Resultatsdateien nachvollziehbar sein.
