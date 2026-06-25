import CatalanNormalform.EABCFermat

namespace CatalanNormalform

/-!
ASLArchitecture:
Formale Schicht fuer ASL^(K)-Terminologie auf dem existierenden Phi-Kern.
-/

/-- Defensive Huelle fuer Splitting-Daten einer K-Schicht. -/
structure GammaK (K : Type) where
  splitData : K

/-- ASL^(K)-Objekt: additiver Kern `Phi` plus Schichtdaten `GammaK K`. -/
abbrev PhiASL (K : Type) : Type := PhiCounter × GammaK K

/-- Konstruktor fuer ASL^(K) aus Kern und Schichtdaten. -/
def mkPhiASL (K : Type) (phi : PhiCounter) (gamma : K) : PhiASL K :=
  (phi, ⟨gamma⟩)

/-- Kanonische ASL^(K)-Auswertung entlang `Phi` und externer Schichtfunktion. -/
def PhiASLOfNat (K : Type) (Gamma : Nat → K) (n : Nat) (hn : FactorizationWitness n) : PhiASL K :=
  mkPhiASL K (Phi n hn) (Gamma n)

/-- Projektion auf den additiven Kern. -/
def coreProj {K : Type} (x : PhiASL K) : PhiCounter := x.1

/-- Projektion auf die Schichtdaten. -/
def gammaProj {K : Type} (x : PhiASL K) : K := x.2.splitData

/-- Kompatibilitaetsabbildung zur bisherigen Paar-Notation `(PhiCounter × K)`. -/
def toLegacyPair {K : Type} (x : PhiASL K) : PhiCounter × K :=
  (coreProj x, gammaProj x)

/-- Rueckabbildung von `(PhiCounter × K)` in die neue ASL-Notation. -/
def fromLegacyPair {K : Type} (x : PhiCounter × K) : PhiASL K :=
  mkPhiASL K x.1 x.2

@[simp] theorem coreProj_mkPhiASL (K : Type) (phi : PhiCounter) (gamma : K) :
    coreProj (mkPhiASL K phi gamma) = phi := rfl

@[simp] theorem gammaProj_mkPhiASL (K : Type) (phi : PhiCounter) (gamma : K) :
    gammaProj (mkPhiASL K phi gamma) = gamma := rfl

@[simp] theorem toLegacyPair_fromLegacyPair {K : Type} (x : PhiCounter × K) :
    toLegacyPair (fromLegacyPair x) = x := by
  cases x
  rfl

@[simp] theorem fromLegacyPair_toLegacyPair {K : Type} (x : PhiASL K) :
    fromLegacyPair (toLegacyPair x) = x := by
  cases x with
  | mk phi gamma =>
      cases gamma with
      | mk g =>
          rfl

/-- Die neue ASL-Schicht verfeinert den existierenden witness-basierten `Phi`-Kern. -/
@[simp] theorem core_of_PhiASLOfNat
    (K : Type) (Gamma : Nat → K) (n : Nat) (hn : FactorizationWitness n) :
    coreProj (PhiASLOfNat K Gamma n hn) = Phi n hn := rfl

/-- Die bestehende Kernadditivitaet bleibt auf der ASL-Schicht erhalten. -/
theorem PhiASL_core_mul_additive
    (K : Type) (Gamma : Nat → K)
    {n m : Nat} (hn : FactorizationWitness n) (hm : FactorizationWitness m) :
    coreProj (PhiASLOfNat K Gamma (n * m) (mulWitness hn hm))
      = coreProj (PhiASLOfNat K Gamma n hn) + coreProj (PhiASLOfNat K Gamma m hm) := by
  simpa [coreProj, PhiASLOfNat, mkPhiASL] using Phi_mul_additive_with_witnesses (n := n) (m := m) hn hm

/-- Projektion auf den Kern reproduziert exakt die alte Paar-Definition `Phi_ASL_K`. -/
@[simp] theorem core_matches_legacy_Phi_ASL_K
    (K : Type) (Gamma : Nat → K) (n : Nat) (hn : FactorizationWitness n) :
    coreProj (PhiASLOfNat K Gamma n hn) = (Phi_ASL_K K Gamma n hn).1 := rfl

/-- Schichtprojektion reproduziert die zweite Komponente von `Phi_ASL_K`. -/
@[simp] theorem gamma_matches_legacy_Phi_ASL_K
    (K : Type) (Gamma : Nat → K) (n : Nat) (hn : FactorizationWitness n) :
    gammaProj (PhiASLOfNat K Gamma n hn) = (Phi_ASL_K K Gamma n hn).2 := rfl

end CatalanNormalform
