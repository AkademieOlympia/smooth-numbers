/-
Copyright (c) 2026 Thomas Hoffbauer. All rights reserved.
Released under Apache 2.0 license.
Authors: Thomas Hoffbauer

# Tamari-Rotation - Lean-Stufe 2

Definition der Tamari-Rotation zwischen binären Bäumen.

Die Tamari-Rotation ist die fundamentale Umformung:
  ((A B) C) ↔ (A (B C))

die den Tamari-Graph definiert.
-/

import CatalanNormalform.CTree
import Mathlib.Logic.Relation

namespace CTree

/-!
## Tamari-Rotation

Die Tamari-Rotation ist eine lokale Umstrukturierung eines Baums,
die die Assoziativität der Multiplikation widerspiegelt:

  (ab)c → a(bc)

In Baumform:
```
    ∙               ∙
   / \             / \
  ∙   C    →→    A   ∙
 / \                 / \
A   B               B   C
```
-/

/-- Tamari-Rotation von links nach rechts: ((A B) C) → (A (B C)) -/
inductive TamariStepRight : {k : Nat} → CTree k → CTree k → Prop where
  | assoc {kA kB kC : Nat} (A : CTree kA) (B : CTree kB) (C : CTree kC) :
      TamariStepRight (node (node A B) C) (node A (node B C))

/-- Tamari-Rotation von rechts nach links: (A (B C)) → ((A B) C) -/
inductive TamariStepLeft : {k : Nat} → CTree k → CTree k → Prop where
  | assoc {kA kB kC : Nat} (A : CTree kA) (B : CTree kB) (C : CTree kC) :
      TamariStepLeft (node A (node B C)) (node (node A B) C)

/-!
### Eigenschaften der gerichteten Rotation
-/

/-- Rechts-Rotation ist deterministisch: aus T folgt eindeutiges T'. -/
theorem tamari_right_unique {k : Nat} {t t₁ t₂ : CTree k}
    (h₁ : TamariStepRight t t₁) (h₂ : TamariStepRight t t₂) :
    t₁ = t₂ := by
  cases h₁
  cases h₂
  rfl

/-- Links-Rotation ist deterministisch. -/
theorem tamari_left_unique {k : Nat} {t t₁ t₂ : CTree k}
    (h₁ : TamariStepLeft t t₁) (h₂ : TamariStepLeft t t₂) :
    t₁ = t₂ := by
  cases h₁
  cases h₂
  rfl

/-!
## Ungerichtete Tamari-Adjazenz

Für den Tamari-Graphen brauchen wir die symmetrische Relation.
-/

/-- Zwei Bäume sind Tamari-adjazent, wenn sie durch eine Rotation verbunden sind. -/
def TamariAdj {k : Nat} (t₁ t₂ : CTree k) : Prop :=
  TamariStepRight t₁ t₂ ∨ TamariStepLeft t₁ t₂

/-!
### Eigenschaften der Adjazenz
-/

/-- Tamari-Adjazenz ist symmetrisch. -/
theorem tamariAdj_symm {k : Nat} {t₁ t₂ : CTree k} :
    TamariAdj t₁ t₂ → TamariAdj t₂ t₁ := by
  intro h
  cases h with
  | inl hr =>
    right
    cases hr
    constructor
  | inr hl =>
    left
    cases hl
    constructor

/-- Tamari-Adjazenz ist irreflexiv. -/
theorem tamariAdj_irrefl {k : Nat} (t : CTree k) :
    ¬TamariAdj t t := by
  intro h
  cases h with
  | inl hr =>
    cases hr with
    | assoc A B C =>
      -- ((AB)C) ≠ (A(BC))
      sorry -- Strukturell verschieden
  | inr hl =>
    cases hl with
    | assoc A B C =>
      sorry -- Strukturell verschieden

/-!
### Beispiele
-/

/-- Die drei 3-Blatt-Bäume und ihre Tamari-Verbindungen. -/
example : TamariAdj three_left three_right := by
  left
  constructor

example : TamariAdj three_right three_left := by
  right
  constructor

/-!
### Tamari-Pfade

Ein Tamari-Pfad ist eine Folge von Rotationen.
-/

/-- Ein Pfad im Tamari-Graph. -/
inductive TamariPath : {k : Nat} → CTree k → CTree k → Type where
  | refl {k : Nat} (t : CTree k) : TamariPath t t
  | cons {k : Nat} {t₁ t₂ t₃ : CTree k}
         (h : TamariAdj t₁ t₂) (p : TamariPath t₂ t₃) : TamariPath t₁ t₃

/-- Länge eines Tamari-Pfads. -/
def TamariPath.length {k : Nat} {t₁ t₂ : CTree k} : TamariPath t₁ t₂ → Nat
  | refl _ => 0
  | cons _ p => 1 + p.length

/-!
### Konnektivität (Hypothese)

Der Tamari-Graph ist zusammenhängend (Sleator-Tarjan-Thurston).
Wir formulieren dies als Axiom für jetzt.
-/

/-- Der Tamari-Graph Γ_k ist zusammenhängend. -/
axiom tamari_connected {k : Nat} (t₁ t₂ : CTree k) :
  Nonempty (TamariPath t₁ t₂)

/-!
### Distanz im Tamari-Graph

Die Tamari-Distanz ist die minimale Pfadlänge.
-/

/-- Tamari-Distanz zwischen zwei Bäumen. -/
noncomputable def tamari_dist {k : Nat} (t₁ t₂ : CTree k) : Nat :=
  Nat.find (h := by
    have ⟨p⟩ := tamari_connected t₁ t₂
    use p.length
    intro n hn
    sorry -- Existenz eines Pfads der Länge n
  )

/-!
### Durchmesser des Tamari-Graphen

Der Durchmesser von Γ_k ist die maximale Distanz zwischen zwei Bäumen.
Bekannt: diam(Γ_k) = C(k,2) = k(k-1)/2 (Distanz von Linksbaum zu Rechtsbaum).
-/

/-- Der Durchmesser des Tamari-Graphen. -/
noncomputable def tamari_diameter (k : Nat) : Nat :=
  k * (k - 1) / 2

/-- Hypothese: Distanz von Linksbaum zu Rechtsbaum ist der Durchmesser. -/
axiom tamari_dist_left_right (k : Nat) (h : k ≥ 2) :
  tamari_dist (left_tree k) (right_tree k) = tamari_diameter k

end CTree
