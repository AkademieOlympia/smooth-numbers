# LEAN Boundary Checklist

Stand: 2026-06-24  
Scope: `catalan-normalform/lean`

## 1) EABC/ASL-Kern (Phi, H, mod-12, Quaternion)

- Randfall: `n = 1` (kanonischer leerer Witness)  
  - Status: **bewiesen**  
  - Theoreme: `witnessOne`, `Phi_one_witnessOne`, `H_Phi_one_witnessOne`
- Randfall: reine 2/3-Schalen (`OmegaEABC = 0`)  
  - Status: **bewiesen**  
  - Theoreme: `IsTwoThree`, `OmegaEABC_signature6_two_three_zero`, `OmegaEABC_Phi_two_three_shell_zero`
- Randfall: Null-Komponenten in Projektion `H`  
  - Status: **bewiesen**  
  - Theorem: `H_of_v2_v3_only`
- Randfall: mod-12 Paritaetsgrenzen fuer `a,b,c in {0,1}`  
  - Status: **bewiesen**  
  - Theoreme: `mod12_parity_000`, `mod12_parity_100`, `mod12_parity_010`, `mod12_parity_001`, `mod12_parity_110`, `mod12_parity_101`, `mod12_parity_011`, `mod12_parity_111`
- Randfall: Quaternion-Bruecke nur additiv (kein Multiplikations-Overclaim)  
  - Status: **bewiesen / begrenzt**  
  - Theoreme: `iota_additive`, `iota_injective`, `iota_H_bridge_additive`

## 2) ASL^(K)-Architektur und Projektionen

- Randfall: Legacy-Paar `<->` neue `PhiASL`-Notation  
  - Status: **bewiesen**  
  - Theoreme: `toLegacyPair_fromLegacyPair`, `fromLegacyPair_toLegacyPair`
- Randfall: Kernprojektion bleibt unter Schichtwahl invariant  
  - Status: **bewiesen**  
  - Theoreme: `core_of_PhiASLOfNat`, `core_matches_legacy_Phi_ASL_K`, `gamma_matches_legacy_Phi_ASL_K`
- Offener Punkt: konkrete Zahlkoerper-Semantik fuer `GammaK`  
  - Status: **TODO / Statement-Niveau**

## 3) Kepler-Tupelachse v2

- Randfall: Zentrumspunkt enthalten (`d_i = 0`), aber nicht degeneriert  
  - Status: **bewiesen**  
  - Theoreme: `sampleCenterNonDegenerate_has_center_distance`, `sampleCenterNonDegenerate_not_degenerate`, `sampleCenterNonDegenerate_rCore`
- Randfall: degeneriert (`alle d_i = 0`)  
  - Status: **bewiesen**  
  - Theoreme: `allDistancesZero_sampleDegenerate`, `sampleDegenerate_rEdge_zero`, `sampleDegenerate_e_zero`, `sampleDegenerate_T_zero`
- Randfall: `r_core > 0` klar als Prädikat  
  - Status: **bewiesen (als Prädikat/Beispiel)**  
  - Definition/Theorem: `HasPositiveCore`, `sampleCenterNonDegenerate_hasPositiveCore`

## 4) Reachability / State-Space

- Randfall: kleine `N`-Grenze (`N = 0`) nichtleer  
  - Status: **bewiesen**  
  - Theorem: `R_mult_zero_nonempty`
- Randfall: kleine `N`-Grenze (`N = 1`) mit Basispunkt  
  - Status: **bewiesen**  
  - Theorem: `R_mult_one_contains_phi_one`
- Randfall: kleine `B`-Grenze (`B = 0`) leer/nichtleer  
  - Status: **bewiesen**  
  - Theoreme: `R_add_zero_contains_zero`, `R_add_zero_excludes_positive_v2`
- Randfall: Schrankenstabilitaet bei wachsendem `B`  
  - Status: **bewiesen**  
  - Theorem: `R_add_monotone`
- Offener Punkt: `nMin`-Vollcharakterisierung  
  - Status: **TODO / Axiom-basiert**  
  - Referenz: `n_min_le_N_necessary`

## 5) Fibonacci/Zeta/Bernoulli Bridges

- Randfall Fib/Zeta: `n = 0` und `n = 1` Basen  
  - Status: **bewiesen**  
  - Theoreme: `zetaLikeTerm_zero_index`, `zetaLikeTerm_one_index`, `Phi_FibZeta_n0_gamma`, `Phi_FibZeta_n1_gamma`
- Randfall Bernoulli: triviale Potenzsummen-/Layer-Basis (`n = 0/1`)  
  - Status: **bewiesen**  
  - Theoreme: `powerSum_one`, `bernoulliLikeLayer_zero`, `Phi_Bernoulli_n0_gamma`, `Phi_Bernoulli_n1_gamma`
- Offener Punkt Fib/Zeta: analytische Wachstumsbruecke  
  - Status: **Statement**  
  - Referenz: `fibonacciZetaGrowthBridgeStatement`
- Offener Punkt Bernoulli: Faulhaber/Bernoulli-Vollbeweis  
  - Status: **Statement**  
  - Referenz: `bernoulliFaulhaberBridgeStatement`
