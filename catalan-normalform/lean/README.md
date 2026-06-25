# Lean-Block: EABC/Fermat

Dieses Verzeichnis enthaelt eine minimale Lean-Formalisierung fuer den EABC/Fermat-Kern:

- Datei: `CatalanNormalform/EABCFermat.lean`
- Root-Import: `CatalanNormalform.lean`

## Abgedeckte Aussagen

- Additiver Kern auf Faktorenlisten:
  - `signature_append_additive`
  - `signature_mul_additive_under_factorizations`
- Produktkonsistenz unter Faktorisierungszeugen:
  - `prod_append_of_witnesses`
- mod-12-Paritaetsprojektion:
  - `pow_mod12_parity_of_square_one`
  - `fermat_parity_projection_mod12`
  - `one_class_neutral_mod12`
  - `fermat_parity_projection_with_e_mod12`

## Vorbereiteter starker Statement-Block

- `additiveCoreGlobalStatement : Prop`
  - formuliert die globale Multiplikativitaet `H (n*m) = H n + H m`
  - bewusst als Statement vorbereitet (ohne kanonische globale Faktorisierungsfunktion)

## Build

```bash
cd catalan-normalform/lean
lake build
```
