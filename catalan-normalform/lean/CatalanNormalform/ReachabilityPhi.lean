import CatalanNormalform.EABCFermat

namespace CatalanNormalform

/-!
ReachabilityPhi:
Formale Definitionen fuer Reachability und State-Space-Anschluss.
-/

/-- `phi` ist durch `n` erreichbar, wenn es einen Faktorisierungszeugen mit `Phi n = phi` gibt. -/
def RealizesPhi (n : Nat) (phi : PhiCounter) : Prop :=
  ∃ hn : FactorizationWitness n, Phi n hn = phi

/-- Multiplikative Erreichbarkeitsmenge bis Grenze `N`: `{ Phi n | n <= N }`. -/
def R_mult (N : Nat) (phi : PhiCounter) : Prop :=
  ∃ n : Nat, ∃ hn : FactorizationWitness n, n ≤ N ∧ Phi n hn = phi

/-- Additives, endliches Raster mit Koordinatenschranke `B`. -/
def R_add (B : Nat) (phi : PhiCounter) : Prop :=
  phi.v2 ≤ B ∧ phi.v3 ≤ B ∧
  phi.e ≤ B ∧ phi.a ≤ B ∧ phi.b ≤ B ∧ phi.c ≤ B

/-- TODO-Platzhalter: `n_min(phi)` als Zielinterface fuer minimale Erreichbarkeitsindizes. -/
def nMin (phi : PhiCounter) : Nat :=
  let _ := phi
  0

theorem mem_R_mult_has_bounded_witness
    {N : Nat} {phi : PhiCounter}
    (hreach : R_mult N phi) :
    ∃ n : Nat, n ≤ N ∧ RealizesPhi n phi := by
  rcases hreach with ⟨n, hn, hnN, hphi⟩
  exact ⟨n, hnN, ⟨hn, hphi⟩⟩

/--
TODO-Theorem (bewusst als Stub):
Wenn `phi` in `R_mult N` liegt, dann ist `n_min(phi) <= N` eine notwendige Bedingung.
-/
axiom n_min_le_N_necessary
    {N : Nat} {phi : PhiCounter} :
    R_mult N phi → nMin phi ≤ N

/-- Hilfssatz: aus der TODO-Bedingung folgt direkt eine numerische obere Schranke. -/
theorem nMin_le_of_reachable
    {N : Nat} {phi : PhiCounter}
    (hreach : R_mult N phi) :
    nMin phi ≤ N := by
  exact n_min_le_N_necessary hreach

/-- Formale Zustandsdefinition `X_n`. -/
structure StateX where
  idx : Nat
  phi : PhiCounter
deriving Repr

/-- Kanonischer Zustand aus `n` und Witness. -/
def Xn (n : Nat) (hn : FactorizationWitness n) : StateX :=
  ⟨n, Phi n hn⟩

/-- Uebergangsrelation-Placeholder fuer Dynamics-Probes. -/
def Transition (x y : StateX) : Prop :=
  y.idx = x.idx + 1 ∧ ∃ hy : FactorizationWitness y.idx, y.phi = Phi y.idx hy

theorem transition_from_Xn
    (n : Nat) (hn : FactorizationWitness n) (hn1 : FactorizationWitness (n + 1)) :
    Transition (Xn n hn) (Xn (n + 1) hn1) := by
  refine ⟨rfl, ?_⟩
  exact ⟨hn1, rfl⟩

/-- TODO-Stub: stärkere Vollstaendigkeit (wenn gewuenscht spaeter als Beweis ausbauen). -/
def transitionCompletenessTodo : Prop :=
  ∀ y : StateX, (∃ hy : FactorizationWitness y.idx, y.phi = Phi y.idx hy) →
    ∃ x : StateX, Transition x y

/-! ## Boundary-Lemmas (kleine N/B, leer/nichtleer) -/

def witnessZero : FactorizationWitness 0 := ⟨[0], by simp⟩

def witnessOneReach : FactorizationWitness 1 := witnessOne

theorem R_mult_zero_nonempty :
    ∃ phi : PhiCounter, R_mult 0 phi := by
  refine ⟨Phi 0 witnessZero, ?_⟩
  exact ⟨0, witnessZero, by simp, rfl⟩

theorem R_mult_one_contains_phi_one :
    R_mult 1 (Phi 1 witnessOneReach) := by
  exact ⟨1, witnessOneReach, by simp, rfl⟩

theorem R_add_zero_contains_zero :
    R_add 0 (0 : PhiCounter) := by
  simp [R_add]

theorem R_add_zero_excludes_positive_v2 :
    ¬ R_add 0 ⟨1, 0, 0, 0, 0, 0⟩ := by
  simp [R_add]

theorem R_add_monotone
    {B1 B2 : Nat} (hB : B1 ≤ B2) {phi : PhiCounter} :
    R_add B1 phi → R_add B2 phi := by
  intro h
  rcases h with ⟨hv2, hv3, he, ha, hb, hc⟩
  exact ⟨Nat.le_trans hv2 hB, Nat.le_trans hv3 hB, Nat.le_trans he hB,
    Nat.le_trans ha hB, Nat.le_trans hb hB, Nat.le_trans hc hB⟩

end CatalanNormalform
