# LEAN_SECURED_CORE

Stand: 2026-06-24

Dieses Dokument trennt strikt zwischen:

1. formal bewiesenen Lean-Fakten,
2. vorbereiteten Statements/Stubs/Axiomen.

## Reproduzierbarkeit und Build-Status

- Repo-Pfad: `catalan-normalform/lean`
- Letzter verifizierter Build in dieser Ueberarbeitung: erfolgreich
- Befehl:

```bash
cd catalan-normalform/lean
lake build
```

## Gesicherter Lean-Kern (`LEAN_PROVED`)

### A) Additiver Kern in `EABCFermat.lean`

- `signature_append_additive`
- `signature_mul_additive_under_factorizations`
- `prod_append_of_witnesses`
- `Phi_mul_additive_with_witnesses`
- `H_mul_additive_with_witnesses`
- `H_additive`

Bedeutung: Die witness-basierte 6D-Signatur (`Phi`) und ihre 4D-Projektion (`H`) sind formal additiv unter Multiplikation mit expliziten Faktorisierungszeugen.

### B) Mod-12-Paritaetsblock in `EABCFermat.lean`

- `pow_mod12_parity_of_square_one`
- `fermat_parity_projection_mod12`
- `one_class_neutral_mod12`
- `fermat_parity_projection_with_e_mod12`
- `mod12_kernel_depends_only_on_parity`

Bedeutung: Die mod-12-Kernprojektion fuer die `5/7/11`-Teile haengt formal nur von Exponentenparitaeten ab; `E` ist neutral.

### C) Quaternionische Bruecke (additiv) in `EABCFermat.lean` und `ASLConnections.lean`

- `iota_additive`
- `iota_injective`
- `iota_H_bridge_additive`

Bedeutung: Quaternionische Nutzung ist formal als additive Einbettung abgesichert. Es gibt keinen multiplikativen Quaternionenclaim.

### D) ASL-Architektur in `ASLArchitecture.lean`

- `coreProj_mkPhiASL`
- `gammaProj_mkPhiASL`
- `toLegacyPair_fromLegacyPair`
- `fromLegacyPair_toLegacyPair`
- `core_of_PhiASLOfNat`
- `PhiASL_core_mul_additive`
- `core_matches_legacy_Phi_ASL_K`
- `gamma_matches_legacy_Phi_ASL_K`

Bedeutung: Die Architektur `Phi_ASL^(K)` ist formal konsistent mit dem bisherigen Kern und dessen Additivitaet.

### E) Neue Brueckenmodule

#### `FibonacciZetaBridge.lean`

- `Phi_FibZeta_core`
- `Phi_FibZeta_gamma_fib`
- `Phi_FibZeta_gamma_zeta`
- `zetaLikePartialSum_zero`
- `zetaLikePartialSum_succ`
- `fibZetaASLCompatibilityStatement_holds`

#### `BernoulliBridge.lean`

- `Phi_Bernoulli_core`
- `Phi_Bernoulli_gamma_sum`
- `Phi_Bernoulli_gamma_norm`
- `powerSum_zero`
- `powerSum_succ`
- `bernoulliASLCompatibilityStatement_holds`

#### `KeplerTupleV2.lean`

- zentrale Definitionen sind formal typisiert und auswertbar
- u.a. `hasPositiveDistance_iff_exists_positiveDistance`
- Beispieldaten/Theorem fuer Degeneratfall (`allDistancesZero_sampleDegenerate`)

## Nicht gesichert: Statements, Stubs, Axiome

### 1) Globale witness-freie Kernform

- `additiveCoreGlobalStatement`
- `Phi_global_monoid_hom_statement`

Status: nur als Prop-Statements definiert; kein Lean-Beweis.

### 2) Platzhalter-Schichten (ASL-Integration)

- `Phi_G_stub`
- `Phi_Eisenstein_stub`
- `Phi_Dickman_stub`
- zugehoerige Stub-Carriers und Gamma-Stubs

Status: definierte Anschlussstellen, keine inhaltliche Zahlkoerper-/Smoothness-Formalisierung.

### 3) Reachability-Luecken in `ReachabilityPhi.lean`

- `nMin` ist aktuell ein TODO-Platzhalter (`0`).
- `n_min_le_N_necessary` ist ein `axiom` (nicht bewiesen).
- `transitionCompletenessTodo` ist nur ein Prop-Stub.

Status: nicht formal abgesichert als Theorem.

### 4) Analytische Bruecken nur als Statements

- `fibonacciZetaGrowthBridgeStatement`
- `bernoulliFaulhaberBridgeStatement`

Status: absichtlich vorbereitete Statements; keine Vollbeweise.

## Gesichert vs vorbereitet (Kurzmatrix)

| Modul | Gesichert | Vorbereitet / offen |
|---|---|---|
| `EABCFermat.lean` | witness-basierte Additivitaet, mod-12-Paritaet, additive `iota` | globale witness-freie Hom-Form |
| `ASLArchitecture.lean` | Kern-/Schichtprojektionen, Legacy-Isomorphie, Kernadditivitaet | konkrete `Gamma_K`-Inhalte |
| `ASLConnections.lean` | Brueckenlemmas zum Kern | `Phi_G/Eisenstein/Dickman` nur Stub |
| `ReachabilityPhi.lean` | Basisdefinitionen + einfache Erreichbarkeitsableitung | `nMin`-Theorie, Notwendigkeitssatz als Axiom |
| `FibonacciZetaBridge.lean` | Kern-/Schichtkonsistenz, rekursive Summenbasis | Wachstums-/Analytik-Bridge |
| `BernoulliBridge.lean` | Kern-/Schichtkonsistenz, Potenzsummenbasis | Faulhaber/Bernoulli-Vollbruecke |
| `KeplerTupleV2.lean` | formale Observablen + Beispiele | keine physikalische Dynamikformalisation |

## Prioritaet fuer mehr `LEAN_PROVED`

1. `n_min_le_N_necessary` von Axiom zu Theorem heben.
2. witness-freies globales `Phi` formal konstruieren.
3. `Gamma_K` konkretisieren (Gauss/Eisenstein) statt Unit-Stubs.
4. Zeta/Faulhaber-Statements mit Mathlib-Beweisen ersetzen.
5. Dokumente nur mit theorem-genauen Labels synchronisieren.
