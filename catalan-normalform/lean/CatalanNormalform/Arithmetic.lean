/-
Copyright (c) 2026 Thomas Hoffbauer. All rights reserved.
Released under Apache 2.0 license.
Authors: Thomas Hoffbauer

# Arithmetische Struktur

Verbindung zu Primfaktorzerlegungen und EABC-Signaturen.
-/

import CatalanNormalform.Magic
import Mathlib.Data.Nat.Prime.Basic
import Mathlib.Data.Nat.Factorization.Basic

namespace CatalanNormalform

/-!
## Primfaktorzerlegung

Eine Zahl n ≥ 2 besitzt eine eindeutige Primfaktorzerlegung mit Vielfachheit.
-/

/-- Anzahl der Primfaktoren mit Vielfachheit (Ω(n)). -/
def omega (n : Nat) : Nat :=
  (Nat.factors n).length

/-- Liste der Primfaktoren mit Vielfachheit. -/
def prime_factors (n : Nat) : List Nat :=
  Nat.factors n

/-!
## EABC-Signatur

Klassifikation von Primzahlen p > 3 nach p mod 12.
-/

inductive EABC where
  | E : EABC  -- p ≡ 1 (mod 12)
  | A : EABC  -- p ≡ 5 (mod 12)
  | B : EABC  -- p ≡ 7 (mod 12)
  | C : EABC  -- p ≡ 11 (mod 12)

/-- EABC-Klassifikation einer Primzahl p > 3. -/
def eabc_class (p : Nat) : Option EABC :=
  if p ≤ 3 then none
  else match p % 12 with
    | 1 => some EABC.E
    | 5 => some EABC.A
    | 7 => some EABC.B
    | 11 => some EABC.C
    | _ => none  -- p nicht prim oder p ≤ 3

/-- EABC-Signatur einer Zahl: Liste der EABC-Klassen ihrer Primfaktoren. -/
def eabc_signature (n : Nat) : List EABC :=
  (prime_factors n).filterMap eabc_class

/-!
## Catalan-Normalform

Die vollständige Normalform einer Zahl.
-/

structure CatalanNormalform (n : Nat) where
  /-- Die Zahl selbst. -/
  value : Nat
  /-- Anzahl der Primfaktoren. -/
  omega : Nat
  /-- EABC-Signatur. -/
  signature : List EABC
  /-- Catalan-Baum (für einen gewählten Kanonisierungsalgorithmus). -/
  tree : CTree omega
  /-- Catalan-Magic des Baums. -/
  magic : ℚ
  /-- Residuale Magic. -/
  residual : ℚ

/-!
## Kanonisierung

Eine Kanonisierung ordnet jeder Zahl einen bestimmten Catalan-Baum zu.
-/

/-- Abstrakte Kanonisierungsfunktion. -/
structure Canonization where
  /-- Ordnet einer Faktorliste einen Baum zu. -/
  canon : (ps : List Nat) → CTree ps.length
  /-- Die Kanonisierung ist deterministisch. -/
  deterministic : ∀ ps₁ ps₂, ps₁ = ps₂ → canon ps₁ = canon ps₂

/-- Linksbaum-Kanonisierung. -/
def left_canonization : Canonization where
  canon ps := sorry -- Konstruiert left_tree rekursiv
  deterministic := sorry

/-- Rechtsbaum-Kanonisierung. -/
def right_canonization : Canonization where
  canon ps := sorry
  deterministic := sorry

/-- Balancierte Kanonisierung (bevorzugt balancierte Bäume). -/
def balanced_canonization : Canonization where
  canon ps := sorry
  deterministic := sorry

end CatalanNormalform
