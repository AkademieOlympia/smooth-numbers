# LEAN_HYPOTHESIS_AUDIT

Stand: 2026-06-25

## Scope und Reproduzierbarkeit

Dieser Audit gleicht Hypothesen gegen den tatsaechlich vorhandenen Lean-Stand im aktuellen Checkout ab.
Bewertung strikt defensiv:

- `LEAN_PROVED`: als Theorem bewiesen (ohne Axiom-Abhaengigkeit fuer die jeweilige Aussage).
- `LEAN_PARTIAL`: teilweise formalisiert (z. B. Definitionen + Teiltheoreme), aber zentrale Aussage noch offen/axiomatisch/stub.
- `LEAN_STATEMENT_ONLY`: nur als Statement/Prop/Stub vorhanden.
- `NOT_IN_LEAN`: im Lean-Bestand nicht modelliert.

Gesichtete Hauptquellen:

- `HYPOTHESES_REGISTER.md`
- `PROJECT_TRUTH_MAP.md`
- `RESEARCH_CONTRACT.md`
- `docs/EABC_FIBONACCI_GOLDEN_RATIO.md`
- `catalan-normalform/lean/README.md`
- `catalan-normalform/lean/ASL_LEAN_INTEGRATION_NOTES.md`
- `LEAN_SECURED_CORE.md`
- `catalan-normalform/lean/CatalanNormalform/*.lean`

Build-Validierung:

- Befehl: `cd catalan-normalform/lean && lake build`
- Ergebnis: erfolgreich (`exit code 0`, "Build completed successfully (11 jobs)")

Hinweis zur Artefaktlage: Mehrere in Registern referenzierte Experiment-Reports (insb. Stage/H10/H12/H13 Rohreports) sind in diesem Checkout nicht vorhanden; der Audit nutzt daher die kanonischen Register-/Map-Eintraege als Quelle.

## Konsolidierte Hypothesenmatrix

| ID | Kurzname | Aktuelle mathematische Formulierung (kurz) | Lean-Status | Lean-Referenzen | Gap to proof (konkreter naechster Schritt) |
|---|---|---|---|---|---|
| `H10` | Conditional-MI-Zusatzsignal | `I(M_C; S \| Omega) > 0` | `NOT_IN_LEAN` | - | Falls gewuenscht: erst formale Definition der Informationsgroessen in Lean modellieren; aktuell rein empirische Hypothese. |
| `H12` | Architekturachsen fuer `M_C` | `M_C` naeher an D/B als an Entropie-/Shellachsen | `NOT_IN_LEAN` | - | Zunaechst formale Objekte fuer Achsen-/Distanzbegriffe spezifizieren, dann theoremfeste Zielaussage definieren. |
| `H13` | Pivot-40-Distanzsignatur | "Pivot 40 ist strukturell besonders" (defensiv/offen) | `NOT_IN_LEAN` | - | Exakte mathematische Zielaussage (Invarianz/Extremalitaet) fixieren, erst dann Lean-Modell. |
| `H14` | Alternative Targets | Anschlusshypothesen zu `E(n)`, `H(n)`, `L(n)`, `chi(n)` | `NOT_IN_LEAN` | - | Eine priorisierte Zielaussage auswaehlen und formal definieren; aktuell kein Lean-Objekt. |
| `H16` | Offen, nicht operationalisiert | ID vorhanden, aber keine saubere operative Definition im Bestand | `NOT_IN_LEAN` | - | Erst kanonische Definition + Falsifikationskriterium in Doku festschreiben, dann Lean-Statement anlegen. |
| `H17` | Offen, nicht operationalisiert | ID vorhanden, aber keine saubere operative Definition im Bestand | `NOT_IN_LEAN` | - | Wie H16: zuerst formale Spezifikation, danach Lean-Einstieg. |
| `H18-A` | Fibonacci/phi Nulltest | Kein robustes `phi`-Signal in Ratio-Observablen | `NOT_IN_LEAN` | - | Wenn gewuenscht: Ratio-/Distanzmetriken in Lean definieren; aktuell nur als empirischer Testplan. |
| `H18-B` | Fibonacci/phi Stabilitaet | Moegliche `phi`-Naehe bleibt nicht stabil ueber Holdouts/Skalen | `NOT_IN_LEAN` | - | Stabilitaetsbegriff formal definieren (z. B. ueber Sequenz-/Grenzbedingungen), dann theorematisch aufbauen. |
| `H18-C` | Fibonacci-Mehrwerttest | Fibonacci-Partitionen liefern (oder nicht) OOS-Mehrwert | `NOT_IN_LEAN` | - | Zusatznutzen formal als Vergleichsrelation modellieren; derzeit keine Lean-Formalisierung. |
| `H18-D` | Rekurrenztest | Ohne Rekurrenz-/Eigenwertnachweis kein struktureller `phi`-Claim | `NOT_IN_LEAN` | - | Lineare Rekurrenzklasse und Eigenwertbezug in Lean definieren; danach Implikationssatz beweisen. |
| `STAGE-5.5` | Holdout-Familienranking 5.5 | Stage5.5 empirische Ranking-/Drift-Aussagen | `NOT_IN_LEAN` | - | Keine direkte Lean-Abbildung vorhanden; nur ueber neue formale Modellierung der Metriken moeglich. |
| `STAGE-5.6` | Holdout-Familienranking 5.6 | Stage5.6 empirische Brems-/Methodik-Aussagen | `NOT_IN_LEAN` | - | Wie Stage-5.5, zuerst formale Definitionsebene erstellen. |
| `STAGE-6` | Holdout-Protokoll 6 | OOS-Aussagen zu Signalachsen und Modellfamilienvergleich | `NOT_IN_LEAN` | - | Erst mathematische Kernaussage aus dem Protokoll extrahieren, dann Lean-Statement. |
| `REACHABILITY-BRIDGE` | Notwendigkeit `nMin phi <= N` | Fuer `R_mult N phi` soll `nMin phi <= N` notwendig sein | `LEAN_PARTIAL` | `ReachabilityPhi.lean`: `R_mult`, `nMin`, `n_min_le_N_necessary` (axiom), `nMin_le_of_reachable` | `nMin` konstruktiv (nicht konstant `0`) definieren und `n_min_le_N_necessary` als echtes Theorem beweisen. |
| `GLOBAL-PHI-HOM` | Witness-freie globale Additivitaet | `exists Phi : Nat -> PhiCounter, Phi(n*m)=Phi n + Phi m` | `LEAN_STATEMENT_ONLY` | `EABCFermat.lean`: `additiveCoreGlobalStatement`, `Phi_global_monoid_hom_statement` | Kanonische Faktorisierungswahl anbinden und vorhandene witness-basierte Additivitaet auf globale Funktion transportieren. |
| `FIB-ZETA-GROWTH-BRIDGE` | Fibonacci/Zeta-Wachstumsbruecke | Existenzaussage `forall s, exists C, ...` fuer Fib/Zeta-Terme | `LEAN_STATEMENT_ONLY` | `FibonacciZetaBridge.lean`: `fibonacciZetaGrowthBridgeStatement` | Entweder präzisieren und beweisen oder als reines Interface belassen; fuer Beweis Mathlib-Analyseschicht anbinden. |
| `BERNOULLI-FAULHABER-BRIDGE` | Bernoulli/Faulhaber-Bruecke | Existenzaussage fuer Potenzsummen-Darstellung | `LEAN_STATEMENT_ONLY` | `BernoulliBridge.lean`: `bernoulliFaulhaberBridgeStatement` | Bernoulli-Zahlen/Faulhaber in Lean integrieren und Statement durch theorematische Identitaeten ersetzen. |
| `ASL-GAMMA-CONCRETE` | Konkrete `Gamma_K`-Semantik | `Phi_ASL^(K)`-Rahmen soll mit inhaltlicher K-Schicht gefuellt werden | `LEAN_PARTIAL` | `ASLArchitecture.lean` (Rahmen), `ASLConnections.lean` (`Phi_G_stub`, `Phi_Eisenstein_stub`, `Phi_Dickman_stub`) | Stub-Carriers (`Unit`/Proxy) durch konkrete Datentypen ersetzen und Kompatibilitaetslemmas fuer reale Schichten beweisen. |

## Kepler-EABC H0-H12 Matrix (neu)

Kanonische Referenz fuer Formulierungen:
- `HYPOTHESES_KEPLER_EABC.md`

| ID | Kurzname | Aktuelle mathematische Formulierung (kurz) | Lean-Status | Lean-Referenzen | Gap to proof (konkreter naechster Schritt) |
|---|---|---|---|---|---|
| `H0` | Additiver Kern | witness-basierte Produktadditivitaet von `Phi` und 4D-Projektion `H` | `LEAN_PROVED` | `EABCFermat.lean`: `Phi_mul_additive_with_witnesses`, `H0_additive_core_phi`, `H0_additive_core_H` | witness-freie globale Variante in Lean schliessen (`Phi_global_monoid_hom_statement`). |
| `H1` | Mod-12-Paritaetsprojektion | Kern modulo 12 haengt nur von den Paritaeten `A,B,C` ab (`E` neutral) | `LEAN_PROVED` | `EABCFermat.lean`: `fermat_parity_projection_with_e_mod12`, `H1_mod12_parity_projection`, `H1_mod12_kernel_depends_only_on_parity` | kompakte API fuer 8 Paritaetsklassen als Zusatzlemmas. |
| `H2` | Partitionstyp-Invarianz | `e` und `R_v` sind durch den Partitionstyp bestimmt | `LEAN_PARTIAL` | `KeplerTupleV2.lean`: `PartitionType`, `partitionType`, `H2_e_invariant_on_partitionType`, `H2_Rv_invariant_on_partitionType` | volle Permutationsinvarianz (`List.Perm`) als Theorem statt Statement. |
| `H3` | Kreis-Kriterium | `IsCircle <-> e = 0` | `LEAN_PARTIAL` | `KeplerTupleV2.lean`: `IsCircle`, `H3_circle_criterion` | staerkere Charakterisierung fuer nichtdegenerate Klassen. |
| `H4` | Exzentrizitaets-Kriterium | `IsEccentric <-> 0 < e` | `LEAN_PARTIAL` | `KeplerTupleV2.lean`: `IsEccentric`, `H4_eccentricity_criterion` | weitere Strukturlemmas fuer robuste Klassengrenzen. |
| `H5` | Zeit-Surrogat | `T = a^3` (defensiv, ohne Physik-Claim) | `LEAN_STATEMENT_ONLY` | `KeplerTupleV2.lean`: `T`, `H5_time_surrogate_statement`, `H5_time_surrogate_definitional` | monotone/skalenbezogene Folgesaetze als echte Theoreme ergaenzen. |
| `H6` | Asymptotik I | Shape-Stabilisierung im Grossskalenlimit | `LEAN_STATEMENT_ONLY` | `HypothesisLadder.lean`: `H6_asymptotic_shape_stabilization_statement` | empirisches Mehrskalenprotokoll und spaeter formale Konvergenzbegriffe. |
| `H7` | Asymptotik II | Grenzprofil fuer Exzentrizitaet | `LEAN_STATEMENT_ONLY` | `HypothesisLadder.lean`: `H7_eccentricity_limit_profile_statement` | zuerst statistische Zielgroesse belastbar fixieren. |
| `H8` | Asymptotik III | robuste Core/Edge-Separation im Large-Scale-Regime | `LEAN_STATEMENT_ONLY` | `HypothesisLadder.lean`: `H8_core_edge_large_scale_separation_statement` | robuste Nullmodelle + Konvergenzkriterium spezifizieren. |
| `H9` | Zentrierte Bruecke | zentrierte EABC-Darstellung plus additive Brueckenobjekte | `LEAN_PARTIAL` | `EABCFermat.lean`: `CenteredVector`, `centeredByE`, `liftABC`, `H9_liftABC_additive`, `H9_centeredByE_additive_statement` | zentrierte Additivitaet von Statement zu Theorem heben. |
| `H10` | Orientierung vs Betrag | getrennte Strukturdefinitionen fuer Orientierung und Betrag | `LEAN_STATEMENT_ONLY` | `KeplerTupleV2.lean`: `orientationSignature`, `magnitudeSignature`, `orientationMagnitudePair`, `H10_orientation_vs_magnitude_decoupling_statement` | Entkopplungsclaim nur nach OOS-Evidenz und formaler Praezisierung aufwerten. |
| `H11` | Cluster-Reproduzierbarkeit | empirischer Cluster-Claim als Lean-Statement-Placeholder | `LEAN_STATEMENT_ONLY` | `HypothesisLadder.lean`: `H11_cluster_reproducibility_statement` | Operationalisierung + reproduzierbare Experimente vor jeder Aufwertung. |
| `H12` | Prime-race entlang Cluster/Achsen | empirischer Prime-race-Claim als Lean-Statement-Placeholder | `LEAN_STATEMENT_ONLY` | `HypothesisLadder.lean`: `H12_prime_race_cluster_statement` | OOS-Prime-race-Protokoll mit Multipletest-Korrektur etablieren. |

### H0-H12 Statuszaehlung

- `LEAN_PROVED`: 2 (`H0`, `H1`)
- `LEAN_PARTIAL`: 4 (`H2`, `H3`, `H4`, `H9`)
- `LEAN_STATEMENT_ONLY`: 7 (`H5`, `H6`, `H7`, `H8`, `H10`, `H11`, `H12`)
- `NOT_IN_LEAN`: 0 innerhalb dieser H0-H12-Ladder

## Gesamtzahlen je Lean-Statusklasse

- `LEAN_PROVED`: 2
- `LEAN_PARTIAL`: 6
- `LEAN_STATEMENT_ONLY`: 10
- `NOT_IN_LEAN`: 13
- Summe: 31

## Top 10 Prioritaeten fuer naechsten Lean-Schritt

Priorisiert nach "hoher Hebel auf `LEAN_PROVED` bei ueberschaubarem PR-Risiko":

1. `REACHABILITY-BRIDGE` - Axiom entfernen (`n_min_le_N_necessary`) und `nMin` nichttrivial definieren.
2. `GLOBAL-PHI-HOM` - witness-freies globales `Phi` von Statement zu Beweis heben.
3. `FIB-ZETA-GROWTH-BRIDGE` - Statement auf beweisbare Teilform reduzieren und als erstes Theorem absichern.
4. `BERNOULLI-FAULHABER-BRIDGE` - analog: beweisbaren Kern extrahieren und formalisieren.
5. `ASL-GAMMA-CONCRETE` - mindestens eine konkrete `Gamma_K`-Instanz ohne Stub einziehen.
6. `H18-D` - Rekurrenzbegriff formal fixieren, um Bruecke zur bestehenden Fib-Schicht zu schaffen.
7. `H16` - fehlende Operationsdefinition schliessen; sonst kein Lean-Einstieg moeglich.
8. `H17` - wie H16.
9. `STAGE-6` - aus OOS-Protokoll eine klar formalisierbare Kernaussage destillieren.
10. `H12` - Distanz-/Achsenbegriff mathematisch praezisieren als Voraussetzung fuer jede Lean-Modellierung.

## Drei konkrete Empfehlungen (1-2 PRs, maximaler Zuwachs bei `LEAN_PROVED`)

1. PR 1 "Axiom-Rueckbau + globaler Kern": `REACHABILITY-BRIDGE` und `GLOBAL-PHI-HOM` gemeinsam angehen. Das entfernt eine zentrale Unsicherheit (Axiom) und wandelt den wichtigsten Statement-Block in Beweise um.
2. PR 2 "Statement-Hardening fuer Bridges": `FIB-ZETA-GROWTH-BRIDGE` und `BERNOULLI-FAULHABER-BRIDGE` in kleinere, beweisbare Teiltheoreme schneiden; zuerst triviale/rekursive Kernsaetze beweisen, dann Analytik schrittweise.
3. In beiden PRs eine harte Regel erzwingen: jede neue Hypothese bekommt sofort einen Lean-Status-Eintrag + theoremgenaue Referenz, damit `NOT_IN_LEAN` nicht weiter anwachsen kann.

