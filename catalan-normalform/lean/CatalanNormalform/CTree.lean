/-
Copyright (c) 2026 Thomas Hoffbauer. All rights reserved.
Released under Apache 2.0 license.
Authors: Thomas Hoffbauer

# Catalan Trees - Lean-Stufe 1

Binäre Bäume mit k Blättern als abhängiger Typ.

Dies ist die kombinatorische Grundlage für die Catalan-Normalform-Theorie.
-/

import Mathlib.Data.Nat.Basic
import Mathlib.Tactic.Basic

/-!
## Definition: Catalan-Baum

Ein Catalan-Baum mit k Blättern ist entweder:
- ein einzelnes Blatt (k=1), oder
- ein Knoten mit linkem Teilbaum (m Blätter) und rechtem Teilbaum (n Blätter),
  wobei k = m + n.

Die Anzahl solcher Bäume für k Blätter ist die (k-1)-te Catalan-Zahl C_{k-1}.
-/

/-- Ein binärer Baum mit genau k Blättern. -/
inductive CTree : Nat → Type where
  /-- Ein einzelnes Blatt. -/
  | leaf : CTree 1
  /-- Ein interner Knoten mit linkem und rechtem Teilbaum. -/
  | node : {m n : Nat} → CTree m → CTree n → CTree (m + n)

namespace CTree

/-! ### Beispiele -/

/-- Baum mit 2 Blättern: ((•)(•)) -/
def two_leaves : CTree 2 := node leaf leaf

/-- Linksbaum mit 3 Blättern: (((•)(•))(•)) -/
def three_left : CTree 3 := node (node leaf leaf) leaf

/-- Rechtsbaum mit 3 Blättern: ((•)((•)(•))) -/
def three_right : CTree 3 := node leaf (node leaf leaf)

/-- Balancierter Baum mit 4 Blättern: (((•)(•))((•)(•))) -/
def four_balanced : CTree 4 := node (node leaf leaf) (node leaf leaf)

/-- Linksbaum mit 4 Blättern: ((((•)(•))(•))(•)) -/
def four_left : CTree 4 := node (node (node leaf leaf) leaf) leaf

/-! ### Grundlegende Funktionen -/

/-- Anzahl der Blätter (als Typ-Index bereits kodiert). -/
def num_leaves {k : Nat} : CTree k → Nat := fun _ => k

/-- Anzahl interner Knoten in einem Baum mit k Blättern ist k-1. -/
def num_internal_nodes : {k : Nat} → CTree k → Nat
  | 1, leaf => 0
  | m + n, node l r => 1 + num_internal_nodes l + num_internal_nodes r

/-- Höhe des Baums. -/
def height : {k : Nat} → CTree k → Nat
  | 1, leaf => 0
  | _, node l r => 1 + max (height l) (height r)

/-! ### Theoreme über Struktur -/

/-- Jeder Baum mit k Blättern hat genau k-1 interne Knoten. -/
theorem internal_nodes_eq_leaves_minus_one {k : Nat} (t : CTree k) (h : k ≥ 1) :
    num_internal_nodes t = k - 1 := by
  induction t with
  | leaf => simp [num_internal_nodes]
  | node l r ihl ihr =>
    simp [num_internal_nodes]
    omega

/-- Die Höhe eines Baums mit k Blättern liegt zwischen ⌈log₂ k⌉ und k-1. -/
theorem height_bounds {k : Nat} (t : CTree k) (h : k ≥ 1) :
    height t ≤ k - 1 := by
  induction t with
  | leaf => simp [height]
  | node l r ihl ihr =>
    simp [height]
    omega

/-! ### Balancierte Bäume -/

/-- Ein Baum heißt balanciert, wenn seine Höhe minimal ist: ⌈log₂ k⌉. -/
def is_balanced {k : Nat} (t : CTree k) : Prop :=
  height t = Nat.clog 2 k

/-- Der balancierte Baum mit 4 Blättern ist tatsächlich balanciert. -/
example : is_balanced four_balanced := by
  unfold is_balanced four_balanced height
  norm_num

/-! ### Lineare und Rechte Bäume -/

/-- Linksbaum: maximal linkslastige Struktur (((•)•)•)...
    Höhe = k-1 -/
def left_tree : (k : Nat) → CTree k
  | 1 => leaf
  | n + 1 => node (left_tree n) leaf

/-- Rechtsbaum: maximal rechtslastige Struktur •(•(•...))
    Höhe = k-1 -/
def right_tree : (k : Nat) → CTree k
  | 1 => leaf
  | n + 1 => node leaf (right_tree n)

/-- Linksbaum hat maximale Höhe. -/
theorem left_tree_max_height (k : Nat) (h : k ≥ 1) :
    height (left_tree k) = k - 1 := by
  induction k with
  | zero => contradiction
  | succ n ih =>
    cases n with
    | zero => rfl
    | succ m =>
      simp [left_tree, height]
      rw [ih (by omega)]
      omega

/-- Rechtsbaum hat maximale Höhe. -/
theorem right_tree_max_height (k : Nat) (h : k ≥ 1) :
    height (right_tree k) = k - 1 := by
  induction k with
  | zero => contradiction
  | succ n ih =>
    cases n with
    | zero => rfl
    | succ m =>
      simp [right_tree, height]
      rw [ih (by omega)]
      omega

/-! ### Gleichheit und Decidability -/

/-- Strukturelle Gleichheit von Bäumen ist entscheidbar. -/
instance {k : Nat} : DecidableEq (CTree k) := by
  intro t₁ t₂
  induction t₁ with
  | leaf =>
    cases t₂ with
    | leaf => exact isTrue rfl
  | node l₁ r₁ ihl ihr =>
    cases t₂ with
    | node l₂ r₂ =>
      cases ihl l₂ with
      | isTrue hl =>
        cases ihr r₂ with
        | isTrue hr =>
          subst hl hr
          exact isTrue rfl
        | isFalse hr =>
          exact isFalse (fun h => by injection h with _ _ hl hr; exact hr hr)
      | isFalse hl =>
        exact isFalse (fun h => by injection h with _ _ hl' hr; exact hl hl')

end CTree
