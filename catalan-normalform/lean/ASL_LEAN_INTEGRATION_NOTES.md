# ASL Lean Integration Notes

Stand: 2026-06-24  
Scope: `catalan-normalform/lean`

## Consolidated Status

- Root-Importkette in `CatalanNormalform.lean` bleibt konsistent und bindet alle relevanten Stränge ein:  
  `EABCFermat`, `ASLConnections`, `ASLArchitecture`, `KeplerTupleV2`, `ReachabilityPhi`, `FibonacciZetaBridge`, `BernoulliBridge`.
- Die kanonische Kernlinie bleibt: witness-basiertes `Phi` in `EABCFermat`, mit stabilen Projektionen (`H`, `iota`) und ASL-Schichtrahmen (`PhiASL`, `Phi_ASL_K`-Kompatibilitaet).
- Parallele Notationen sind defensiv gekoppelt statt brechend ersetzt (Legacy-Paar `<->` neue `PhiASL`-Notation via `toLegacyPair`/`fromLegacyPair`).

## Boundary Results

- **EABC/Phi/H/mod-12:** `n=1`-Basis, 2/3-Schalen (`OmegaEABC=0`), Null-Komponenten und alle 8 Paritaetsrandfaelle `a,b,c in {0,1}` sind formal als Theoreme explizit abgedeckt.
- **ASL^(K):** Kern-/Gamma-Projektionen und Legacy-Kompatibilitaet sind als stabile Projektionstheoreme formalisiert.
- **Kepler v2:** Zentrumspunkt-nichtdegeneriert, voll-degenerierter Fall und `r_core > 0` als eigenes Prädikat (`HasPositiveCore`) sind explizit abgedeckt.
- **Reachability/State-space:** kleine `N`/`B`-Grenzfaelle (leer/nichtleer) plus Monotonie von `R_add` sind formal ergänzt.
- **Fib/Zeta/Bernoulli:** triviale `n=0/1`-Basen sind formal ergänzt; analytische Vollbrücken bleiben bewusst als Statements markiert.
- Vollständige Modul-Checkliste: `LEAN_BOUNDARY_CHECKLIST.md`.

## Neu integriert

- **ASL-Architektur als eigene Formalschicht** in `CatalanNormalform/ASLArchitecture.lean`  
  Neue Begriffe `GammaK`, `PhiASL`, `PhiASLOfNat`, `coreProj`, `gammaProj` mit Projektionstheoremen auf den existierenden Kern `Phi`.
- **Kepler-Tupelachse v2** in `CatalanNormalform/KeplerTupleV2.lean`  
  Formale Definitionen fuer `c`, `d_i` (als quadratische euklidische Distanzen), `r_core`, `r_edge`, `a`, `e`, `R_v`, `T` inkl. explizitem All-Zero-Sonderfall.
- **Reachability + State-Space Anschluss** in `CatalanNormalform/ReachabilityPhi.lean`  
  Definitionen fuer `R_mult`, `R_add`, `nMin`, Zustand `X_n` und Uebergangsrelation `Transition`; notwendige Bedingung `nMin phi <= N` als theorem umgesetzt.
- **Importkette erweitert** in `CatalanNormalform.lean`  
  Neue Module werden zentral geladen: `ASLArchitecture`, `KeplerTupleV2`, `ReachabilityPhi`.

## Noch offen (bewusst)

- **Witness-freie globale `Phi : Nat -> PhiCounter`-Version** bleibt offen; aktueller Kern ist bewusst witness-basiert.
- **`GammaK`-Semantik als konkrete Zahlkoerper-/Splittingdaten** ist absichtlich defensiv als Platzhalter modelliert.
- **Reachability-Hinrichtung/Umkehrsaetze** sind nur als Kernbedingung + TODO-Prop vorbereitet, nicht vollstaendig klassifiziert.
- **Kepler-v2 physikalische Interpretation** ist nur als mathematischer Observable-Rahmen formalisiert, ohne weitergehende Dynamikbeweise.

## 1) Integrierte Kernsaetze (Lean)

### Vollstaendig bewiesen

- `Phi_mul_additive_with_witnesses` in `CatalanNormalform/EABCFermat.lean`  
  Witness-basierte Additivitaet von `Phi` auf Produkten:
  `Phi (n*m) = Phi n + Phi m` fuer explizite Faktorisierungszeugen.
- `H_mul_additive_with_witnesses` in `CatalanNormalform/EABCFermat.lean`  
  4D-Projektion `H` erbt Additivitaet direkt aus `Phi`.
- `mod12_kernel_depends_only_on_parity` in `CatalanNormalform/EABCFermat.lean`  
  Mod-12-Kern fuer `(5^a)*(7^b)*(11^c)` haengt nur von Paritaeten `(a,b,c) mod 2` ab.
- `iota_additive`, `iota_injective` in `CatalanNormalform/EABCFermat.lean`  
  Quaternionischer Zielraum als additive Platzhalter-Struktur, `iota` ist additive Einbettung.
- Brueckenlemma `iota_H_bridge_additive` in `CatalanNormalform/ASLConnections.lean`  
  Additivitaet bleibt entlang `Phi -> H -> iota` erhalten.

### Als strukturierte Statements / Stubs vorbereitet

- `Phi_global_monoid_hom_statement` in `CatalanNormalform/EABCFermat.lean`  
  Globale witness-freie Form `Phi : Nat -> PhiCounter` als Monoid-Hom-Statement.
- `Phi_G`, `Phi_ASL_K` in `CatalanNormalform/EABCFermat.lean`  
  ASL-kompatible Kernnotation mit Schichtkomponente (`Gamma`).
- `Phi_G_stub`, `Phi_Eisenstein_stub`, `Phi_Dickman_stub` in `CatalanNormalform/ASLConnections.lean`  
  Explizite Integrationshaeuser fuer spaetere Gauss/Eisenstein/Dickman-Formalmodule.

## 2) TODO-Grenzen fuer Vollbeweise

1. **Globale kanonische Faktorisierungswahl**  
   Fuer witness-freies `Phi : Nat -> PhiCounter` wird eine kanonische Primfaktorzerlegung in Lean benoetigt (oder ein bestehendes UFD-Interface).
2. **Konkrete `Gamma_K`-Modelle**  
   `Phi_ASL_K` ist formal bereits als Rahmen da; es fehlen konkrete Schichtdefinitionen fuer `Q(i)` / Eisenstein etc.
3. **Quaternionen als echtes Algebraobjekt**  
   Aktuell nur additive Platzhalterstruktur (`HQuaternion`) ohne Multiplikationsanspruch.
4. **Dickman-/Smoothness-Verknuepfung**  
   Aktuell nur Stub-Carriers; es fehlen formale Definitionen (z. B. `rho(u)`-nahes Objekt und Nachweis, wie es mit `Phi` interagiert).

## 3) Anschluss-Matrix (priorisiert)

1. **P1: `CatalanNormalform/EABCFermat.lean` -> `Phi_global_monoid_hom_statement`**  
   Verbindungspunkt: witness-basierte Additivitaet (`Phi_mul_additive_with_witnesses`).  
   Integrationsplan:  
   - Schritt 1: kanonische Faktorisierungsfunktion bereitstellen.  
   - Schritt 2: Witness-Theorem auf globale Funktion transportieren.

2. **P2: `CatalanNormalform/EABCFermat.lean` -> mod-12-Block**  
   Verbindungspunkt: `fermat_parity_projection_mod12`, `mod12_kernel_depends_only_on_parity`.  
   Integrationsplan:  
   - Schritt 1: finite Klassifikation fuer 8 Paritaetsklassen als Tabelle/Lemmafamilie.  
   - Schritt 2: als Kerninterface fuer spaetere Fermat/Catalan-Filter verwenden.

3. **P3: `CatalanNormalform/ASLConnections.lean` -> Gauss-Schicht (`Phi_G_stub`)**  
   Verbindungspunkt: `Phi_ASL_K`-Rahmen, Kernprojektionstheoreme.  
   Integrationsplan:  
   - Schritt 1: `GammaQ_i_stub` durch konkretes Datentyp-Modell ersetzen.  
   - Schritt 2: Kompatibilitaetslemma `Phi_G` vs. Kernadditivitaet ausbauen.

4. **P4: `CatalanNormalform/ASLConnections.lean` -> Eisenstein-Schicht (`Phi_Eisenstein_stub`)**  
   Verbindungspunkt: gleicher ASL-Rahmen mit neuem `GammaK`.  
   Integrationsplan:  
   - Schritt 1: carrier + Invarianten fuer Eisenstein-Arithmetik definieren.  
   - Schritt 2: Vergleichslemma zu Gauss-Schicht (gemeinsamer `Phi`-Kern) formal machen.

5. **P5: `code/experiments/reachability_phi.py` und `docs/EABC_STATE_SPACE_DYNAMICS.md` -> Lean-Stubs (`Phi_Dickman_stub`)**  
   Verbindungspunkt: existierende 6D-`Phi`-Experimentachsen, jetzt mit Lean-Kernnotation synchronisiert.  
   Integrationsplan:  
   - Schritt 1: Smoothness-/Dickman-Proxies als formale Funktionen mit klarer Dom/CoDom-Signatur in Lean definieren.  
   - Schritt 2: Brueckenlemma zwischen `Phi`-Komponenten und Smoothness-Proxies formulieren.

## 4) Reviewer-defensive Hinweise

- Keine Ueberclaims: `Phi` ist aktuell **formal voll additiv mit Zeugen**, global witness-frei nur als Statementblock markiert.
- Quaternionischer Teil ist **explizit additiv** und absichtlich ohne Multiplikationsbehauptung.
- ASL-Namensschema ist konsistent auf `Phi`, `Phi_G`, `Phi_ASL_K` (Lean-identifier fuer `Phi_ASL^(K)`).

## Fibonacci-Zeta Bridges

- **Bewiesen**  
  - `Phi_FibZeta_core`, `Phi_FibZeta_gamma_fib`, `Phi_FibZeta_gamma_zeta` in `CatalanNormalform/FibonacciZetaBridge.lean`:  
    Die Fib/Zeta-Schicht ist formal sauber als `PhiASL (Nat × Rat)` ueber dem unveraenderten Kern `Phi` eingebettet.  
  - `zetaLikePartialSum_zero`, `zetaLikePartialSum_succ`:  
    Rekursive partielle zeta-nahe Summen sind formell stabil aufgesetzt (inkl. defensivem `n = 0`-Fall in `zetaLikeTerm`).
- **Vorbereitet**  
  - `fibonacciZetaGrowthBridgeStatement`:  
    Wachstums-/Gewichtungs-Bridge als explizites Statement fuer spaetere analytische Abschaetzungen.  
  - `fibZetaASLCompatibilityStatement`:  
    Als benanntes Architektur-Interface fixiert; derzeit durch den aktuellen Konstruktor direkt erfuellt.
- **Naechster Schritt**  
  - Mathlib-Analyseschicht anbinden (Dirichlet-/Zeta-Objekte), dann die derzeit vorbereitete Wachstums-Bridge schrittweise von Statement zu Vollbeweis heben.

## Bernoulli Bridges

- **Bewiesen**  
  - `Phi_Bernoulli_core`, `Phi_Bernoulli_gamma_sum`, `Phi_Bernoulli_gamma_norm` in `CatalanNormalform/BernoulliBridge.lean`:  
    Bernoulli-nahe Daten sind als sekundare ASL-Achse (`Rat × Rat`) sauber an den bestehenden `Phi`-Kern angeschlossen.  
  - `powerSum_zero`, `powerSum_succ`:  
    Rekursive Potenzsummen-Basis ist voll formalisiert.
- **Vorbereitet**  
  - `bernoulliFaulhaberBridgeStatement`:  
    Faulhaber/Bernoulli-Richtung als defensives Bridge-Statement markiert (ohne Overclaim).  
  - `bernoulliASLCompatibilityStatement`:  
    Benannter Anschlussvertrag fuer die Architektur.
- **Naechster Schritt**  
  - Konkrete Mathlib-Bernoulli-Infrastruktur integrieren (Bernoulli-Zahlen/Faulhaber-Formalismen) und die vorbereitete Statement-Ebene in echte Identitaeten ueberfuehren.
