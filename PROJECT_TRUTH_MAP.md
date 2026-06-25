# PROJECT_TRUTH_MAP

Stand: 2026-06-24

Ziel: Sofort sichtbare Trennung zwischen formal gesichertem Kern und offenen Forschungsstraengen.

## Klassen

- `LEAN_PROVED`: In Lean formal bewiesen und baubar.
- `MATH_PROVED_NOT_FORMALIZED`: Mathematisch begruendet, aber nicht als Lean-Theorem formalisiert.
- `EMPIRICAL_ROBUST`: Empirisch robust (mehrere Skalen/Checks), aber kein Beweis.
- `EMPIRICAL_PRELIMINARY`: Erste empirische Signale, aber noch mit methodischen Luecken.
- `HYPOTHESIS`: Explizite testbare Arbeitshypothese.
- `SPECULATIVE`: Konzeptionelle Leitidee ohne belastbare Evidenzbasis.

## Projektweite Einstufung

| Strang / Aussage | Klasse | Evidenztyp | Knappe Begruendung | Referenzen | Naechster notwendiger Schritt |
|---|---|---|---|---|---|
| Witness-basierte Additivitaet `Phi(n*m)=Phi(n)+Phi(m)` auf Faktorisierungszeugen | `LEAN_PROVED` | Lean-Theorem | Direkt formal als Produktadditivitaet ueber Witnesses bewiesen. | `catalan-normalform/lean/CatalanNormalform/EABCFermat.lean`, `catalan-normalform/lean/README.md` | Witness-freie globale Version in Lean aufbauen. |
| 4D-Projektion `H` erbt Additivitaet aus `Phi` | `LEAN_PROVED` | Lean-Theorem | Als theorem aus dem 6D-Kern abgeleitet. | `catalan-normalform/lean/CatalanNormalform/EABCFermat.lean`, `catalan-normalform/lean/CatalanNormalform/ASLConnections.lean` | Als Default-Interface in Docs klar als "bewiesen" markieren (erledigt). |
| Mod-12-Paritaetskern (`A/B/C` nur mod 2 relevant) | `LEAN_PROVED` | Lean-Theorem | Mehrere Lemmas plus Kernsatz formal vorhanden. | `catalan-normalform/lean/CatalanNormalform/EABCFermat.lean` | Optional: endliche 8-Klassen-Klassifikation als explizite Lemmafamilie. |
| Quaternionische Einbettung `iota` ist nur additiv genutzt | `LEAN_PROVED` | Lean-Theorem + definitorische Grenze | Additivitaet und Injektivitaet bewiesen; kein Multiplikationsclaim implementiert. | `catalan-normalform/lean/CatalanNormalform/EABCFermat.lean`, `docs/EABC_HURWITZ_PATTERN_THEOREM.md` | Falls gewuenscht: eigene formale Multiplikationsstruktur definieren, sonst explizit so belassen. |
| ASL-Architektur (`PhiASL`, Projektionen, Legacy-Kompatibilitaet) | `LEAN_PROVED` | Lean-Definitionen + Theoreme | Kern-/Schichtprojektionen und Kompatibilitaet formal abgesichert. | `catalan-normalform/lean/CatalanNormalform/ASLArchitecture.lean`, `catalan-normalform/lean/ASL_LEAN_INTEGRATION_NOTES.md` | Konkrete `Gamma_K`-Instanzen statt Platzhaltern formalisieren. |
| Fibonacci/Zeta-Bridge: ASL-Einbettung und rekursive Summenbasis | `LEAN_PROVED` | Lean-Theoreme | Kernprojektion und rekursive Basis (partielle Summen) formal bewiesen. | `catalan-normalform/lean/CatalanNormalform/FibonacciZetaBridge.lean` | Echte Zeta/Dirichlet-Objekte aus Mathlib anbinden. |
| Bernoulli-Bridge: ASL-Einbettung und Potenzsummenbasis | `LEAN_PROVED` | Lean-Theoreme | Kernprojektion und rekursive Potenzsummen formal bewiesen. | `catalan-normalform/lean/CatalanNormalform/BernoulliBridge.lean` | Bernoulli/Faulhaber mit Mathlib formal vervollstaendigen. |
| KeplerTupleV2-Observable-Definitionen (inkl. Degeneratfall) | `LEAN_PROVED` | Lean-Definitionen + Beispiele | Definitionen/Beispiele und zentrale Hilfssatzaussagen formal vorhanden. | `catalan-normalform/lean/CatalanNormalform/KeplerTupleV2.lean` | Physikalische Deutung weiterhin defensiv als nicht-behauptet halten. |
| Reachability-Notwendigkeitssatz `nMin phi <= N` fuer `R_mult N phi` | `HYPOTHESIS` | Lean-Axiom/Stub | Der Kernsatz ist aktuell als `axiom` eingebracht, nicht bewiesen. | `catalan-normalform/lean/CatalanNormalform/ReachabilityPhi.lean` | `nMin` konstruktiv definieren und Axiom durch Beweis ersetzen. |
| Witness-freies globales `Phi : Nat -> PhiCounter` als Monoid-Hom | `HYPOTHESIS` | Statement-Stub | Nur als Prop-Statement vorhanden, ohne kanonische Faktorisierungswahl. | `catalan-normalform/lean/CatalanNormalform/EABCFermat.lean` | Kanonische Zerlegung in Lean integrieren, dann Vollbeweis. |
| Klassischer Split/Inert-Bezug (`1,5 mod 12` vs `7,11 mod 12`) in der Doku | `MATH_PROVED_NOT_FORMALIZED` | Mathematische Standardtheorie + Textbegruendung | Mathematisch plausibel dokumentiert, aber die vollen Zahlkoerper-Resultate sind nicht als Lean-Theorem kodiert. | `docs/EABC_HURWITZ_PATTERN_THEOREM.md`, `docs/snippets/EABC_FERMAT_THEOREM_BOX.md` | Entweder klar als mathematischer Hintergrund labeln oder in Lean formal anbinden. |
| Reachability-Experiment (`R_mult`/`R_add`, `n_min`-Konsistenzcheck) | `EMPIRICAL_ROBUST` | Reproduzierbares OOS-nahes Experiment | Mehrere N/B/Slices, klare numerische Kriterien, konsistente Ergebnisse. | `code/experiments/reachability_phi.py`, `experiments/results/reachability/REACHABILITY_PHI_REPORT.md` | Weitere Skalen und Unsicherheitsanalyse dokumentieren; dann Lean-Bruecke priorisieren. |
| Fibonacci/phi-Achse zeigt robustes phi-Signal | `EMPIRICAL_PRELIMINARY` | Exploratives Baseline-Experiment | Aktueller Bericht findet gerade kein robustes Signal; Befund ist negativ/defensiv. | `code/experiments/fibonacci_phi_probe.py`, `experiments/results/fibonacci_phi/FIBONACCI_PHI_PROBE.md`, `docs/EABC_FIBONACCI_GOLDEN_RATIO.md` | H18-Tests explizit als Nulltests weiterfuehren, keine positiven Claims. |
| State-Space-Dynamics (A-Prozess, Entropie-/Divergenz-Proxies) | `EMPIRICAL_PRELIMINARY` | Explorative Probe | Methodisch sauber beschrieben, aber Prozess B/C und Nullmodelle noch unvollstaendig. | `code/experiments/state_space_dynamics_probe.py`, `docs/EABC_STATE_SPACE_DYNAMICS.md`, `experiments/results/dynamics/DYNAMICS_STAGE_PROBE.md` | Nullmodelle + Holdouts + Sensitivitaetstests vervollstaendigen. |
| KeplerTuple-v2 Numerik/Offsetachsen | `EMPIRICAL_PRELIMINARY` | Numerischer Report mit defensiver Methodik | Klare v2-Definitionen und reproduzierbare Tabellen, aber kein theoretischer Mechanismusbeweis. | `experiments/results/kepler/KEPLER_TUPLE_NUMERIC_REPORT.md`, `experiments/results/kepler/KEPLER_AXIS_V2_CHANGELOG.md` | Script- und Datenpipeline konsistent versionieren, dann externe Robustheitschecks. |
| Stage55/Stage56/Stage6 Holdout-Familienranking | `EMPIRICAL_ROBUST` | Mehrfach-Run + Holdout-Protokoll | Defensive Modellvergleiche ueber Skalen/Folds vorhanden; weiterhin kein Mechanismusbeweis. | `experiments/results/stage55/STAGE55_QUOTIENT_DRIFT.md`, `experiments/results/stage56/STAGE56_METHOD_BRAKES.md`, `experiments/results/stage6/STAGE6_HL_HOLDOUT_PROTOCOL.md` | Delta-r- und N-Raum erweitern, HL-Features praezisieren. |
| Noether-Invariance-Klassifikation von Achsen | `EMPIRICAL_PRELIMINARY` | Heuristischer Transformationsscan | Nutzbare Diagnostik, aber explizit als noether-inspiriert und nicht als Theorem markiert. | `experiments/results/noether/noether_invariance_report.md` | Formale Begriffsgrenzen und robuste Sensitivitaetschecks nachziehen. |
| ASL-Notation/Hierarchie als Governance-Rahmen | `MATH_PROVED_NOT_FORMALIZED` | Architektur-/Notationstext | Klarer, defensiver Schreibvertrag fuer `Phi subset Phi_G subset Phi_ASL^(K)`, aber kein eigener Lean-Beweis der Vollsemantik. | `docs/ASL_NOTATION_REFACTOR.md`, `docs/EABC_HURWITZ_PATTERN_THEOREM.md`, `docs/CATALAN_EABC_BRIDGE.md` | Notationstext weiter mit theorem-genauen Lean-Referenzen synchron halten. |
| H10 zu `I(M_C;S|Omega)>0` | `EMPIRICAL_ROBUST` | Mehrere Datensaetze + Permutation + CV | Mehrfach negativ getestet; kein belastbares Zusatzsignal fuer S gegeben Omega. | `catalan-normalform/experiments/results/h10/H10_FINAL_SUMMARY.md`, `catalan-normalform/experiments/results/h10_final/H10_FINAL_REPORT.md` | Final konsolidierte Version in ein einziges kanonisches H10-Dokument ueberfuehren. |
| H12 Architekturachsen fuer `M_C` (D/B stark, H schwach) | `EMPIRICAL_PRELIMINARY` | Bivariat + partiell/multivariat | Starkes Muster, aber derzeit deskriptiv und linear modelllastig. | `catalan-normalform/experiments/results/h12/H12B_ARCHITECTURE_AXES.md` | Nichtlineare/OOS-Validierung und Kanonisierungsrobustheit. |
| H13 Pivot-40 "besonders" | `HYPOTHESIS` | Explorative Distanzanalyse | Dokumente zeigen teils moderate Effekte, teils Warnung vor Ueberinterpretation. | `catalan-normalform/experiments/results/h13/PIVOT_DISTANCE_ANALYSIS.md`, `catalan-normalform/experiments/results/h13/README.md` | Grossere Skalen + robustere Kontrollen + M_C-Kopplungstest. |
| H16 Diskrete Catalan-Pfadsumme (`H-PI1..H-PI8`) | `HYPOTHESIS` | Definitions-/Protokollnotiz | Diskretes Pfadsummen-Setup und testbare Hypothesen sind kanonisch definiert; Evidenzklasse bleibt offen bis reproduzierbare Ergebnisserie vorliegt. | `docs/H16_PATH_INTEGRAL_CATALAN.md` | Exhaustive Klein-`Omega`-Runs + `beta`-Sweep + Nullchecks (`beta=0`, Permutationskontrolle, Aktionssensitivitaet). |
| "Einzigartige 40-Magie" oder starke ontologische Claims | `SPECULATIVE` | Keine formale/robuste Evidenz | Durch aktuelle H13-Lage nicht gedeckt; nur als offene Erkundung legitim. | `catalan-normalform/experiments/results/h13/PIVOT_DISTANCE_ANALYSIS.md` | Strikt als Spekulation labeln, bis robuste Evidenz vorliegt. |

## Kepler-EABC Zuordnung H0-H12

Kanonische Quelle:
- `HYPOTHESES_KEPLER_EABC.md`

| Strang / Aussage | Klasse | Evidenztyp | Knappe Begruendung | Referenzen | Naechster notwendiger Schritt |
|---|---|---|---|---|---|
| H0 Additiver Kern (`Phi` mit Witnesses) | `LEAN_PROVED` | Lean-Theorem | Der additive Kern ist als witness-basierter Produktsatz formal bewiesen. | `catalan-normalform/lean/CatalanNormalform/EABCFermat.lean` | Globale witness-freie Variante als Folgeschritt formal anbinden. |
| H1 Mod-12-Paritaetsprojektion (`A/B/C`, `E` neutral) | `LEAN_PROVED` | Lean-Theorem | Paritaetsreduktion und Abhaengigkeit nur von `mod 2` sind formalisiert. | `catalan-normalform/lean/CatalanNormalform/EABCFermat.lean` | Endliche Klassenabbildung als kompakte API-Lemmas ausbauen. |
| H2 Partitionstyp-Invarianz fuer `e`,`R_v` | `HYPOTHESIS` | Lean-Definition + Teillemma | Invarianz auf Partitionstyp-Ebene ist formal als Struktur-Lemma vorhanden, Permutationsvollsatz noch offen. | `catalan-normalform/lean/CatalanNormalform/KeplerTupleV2.lean` | Echte Permutationsinvarianz fuer Distanzlisten beweisen. |
| H3 Kreis-Kriterium (`IsCircle <-> e=0`) | `HYPOTHESIS` | Lean-Definition + Def.-Lemma | Kriterium ist definitorisch abgesichert, aber kein starker globaler Strukturbeweis notwendig/gegeben. | `catalan-normalform/lean/CatalanNormalform/KeplerTupleV2.lean` | Zusatzaussagen fuer nichttriviale Klassen einziehen. |
| H4 Exzentrizitaets-Kriterium (`IsEccentric <-> 0<e`) | `HYPOTHESIS` | Lean-Definition + Def.-Lemma | Defensiv als definitorischer Schwellenbegriff formal gefasst. | `catalan-normalform/lean/CatalanNormalform/KeplerTupleV2.lean` | Robuste Charakterisierung ueber weitere Invarianten entwickeln. |
| H5 Zeitachse `T=a^3` (ohne Physik-Claim) | `SPECULATIVE` | Lean-Definition | Nur als Surrogatdefinition vorhanden, keine physikalische oder asymptotische Behauptung formalisiert. | `catalan-normalform/lean/CatalanNormalform/KeplerTupleV2.lean` | Monotonie-/Skalierungslemmas testen und ggf. beweisen. |
| H6 Asymptotik-I (Shape-Stabilisierung) | `HYPOTHESIS` | Empirischer Testplan | Im Lean-Stand nicht modelliert; als asymptotische Arbeitshypothese offen. | `HYPOTHESES_KEPLER_EABC.md` | Mehrskalen-Holdout mit festen Driftkriterien fahren. |
| H7 Asymptotik-II (`e`-Grenzgesetz) | `HYPOTHESIS` | Empirischer Testplan | Kein Lean-Objekt fuer statistische Grenzgesetze vorhanden. | `HYPOTHESES_KEPLER_EABC.md` | Quantil-/Konvergenztests gegen Nullmodelle ausrollen. |
| H8 Asymptotik-III (`rCore/rEdge` robust) | `HYPOTHESIS` | Empirischer Testplan | Derzeit nur als testbare Asymptotik formuliert. | `HYPOTHESES_KEPLER_EABC.md` | Bootstrap-/Permutationstests bei groesseren Skalen. |
| H9 Zentrierter Vektor als additive Bruecke | `HYPOTHESIS` | Lean-Definition + Teillemma | Additive Brueckenstruktur ist formal vorbereitet, noch nicht als globaler Vollsatz abgeschlossen. | `catalan-normalform/lean/CatalanNormalform/EABCFermat.lean` | Bruecke auf witness-freies/globales `Phi` uebertragen. |
| H10 Orientierung vs Betrag | `SPECULATIVE` | Lean-Struktur + Statement | Trennung als Objekte definierbar; starke Entkopplungsbehauptung bleibt offen. | `catalan-normalform/lean/CatalanNormalform/KeplerTupleV2.lean` | OOS-Entkopplungstest (MI/Korrelation) mit Nullmodellen. |
| H11 Cluster-Reproduzierbarkeit | `HYPOTHESIS` | Empirischer Testplan | Lean-seitig nicht modelliert, empirisch offen. | `HYPOTHESES_KEPLER_EABC.md` | Stabilitaetsmetriken und Nullmodellvergleich standardisieren. |
| H12 Prime-race entlang Cluster/Achsen | `HYPOTHESIS` | Empirischer Testplan | Kein formaler Nachweis, nur testbarer empirischer Claim. | `HYPOTHESES_KEPLER_EABC.md` | OOS-Protokoll mit Multiple-Testing-Korrektur umsetzen. |

## Reviewer-Defensivregeln fuer diese Map

- Nur `LEAN_PROVED` darf als formal gesichert bezeichnet werden.
- `MATH_PROVED_NOT_FORMALIZED` ist mathematischer Hintergrund, nicht Lean-Claim.
- Empirische Klassen sind keine Beweise, sondern Reproduktions- und Robustheitsstufen.
- Jede Aufwertung einer Klasse braucht explizite neue Evidenz (Theorem oder reproduzierbaren OOS-Test).
