namespace CatalanNormalform

/-!
KeplerTupleV2:
Formale Observablen auf Offsetlisten (v2-Achse).
Wir arbeiten auf quadratischen euklidischen Distanzen in `Nat`,
damit min/max/degenerate-Faelle robust formalisiert sind.
-/

abbrev Offset2D := Int × Int

def sqDist (c p : Offset2D) : Nat :=
  Int.natAbs ((p.1 - c.1) ^ 2 + (p.2 - c.2) ^ 2)

def minNat? : List Nat → Option Nat
  | [] => none
  | x :: xs => some (xs.foldl Nat.min x)

def maxNat? : List Nat → Option Nat
  | [] => none
  | x :: xs => some (xs.foldl Nat.max x)

structure KeplerTupleV2 where
  c : Offset2D
  offsets : List Offset2D
deriving Repr

def distances (obs : KeplerTupleV2) : List Nat :=
  obs.offsets.map (sqDist obs.c)

def positiveDistances (obs : KeplerTupleV2) : List Nat :=
  (distances obs).filter (fun d => 0 < d)

/-- `r_core = min positive d_i`, explizit optional fuer den All-Zero-Sonderfall. -/
def rCore (obs : KeplerTupleV2) : Option Nat :=
  minNat? (positiveDistances obs)

/-- `r_edge = max d_i` (0 bei leerer Offsetliste). -/
def rEdge (obs : KeplerTupleV2) : Nat :=
  match maxNat? (distances obs) with
  | none => 0
  | some d => d

/-- Sonderfallpraedikat: alle Distanzen sind 0. -/
def allDistancesZero (obs : KeplerTupleV2) : Prop :=
  ∀ d ∈ distances obs, d = 0

/-- Nicht-degenerater Fall: mindestens eine positive Distanz. -/
def hasPositiveDistance (obs : KeplerTupleV2) : Prop :=
  ∃ d ∈ distances obs, 0 < d

/-- Halbe Summenachse `a` auf `Rat` (surrogat fuer semimajor axis). -/
def a (obs : KeplerTupleV2) : Rat :=
  match rCore obs with
  | none => 0
  | some rc => (Rat.ofInt (Int.ofNat (rc + rEdge obs))) / 2

/-- Exzentrizitaets-Surrogat `e = (r_edge - r_core) / r_edge` mit Nullschutz. -/
def e (obs : KeplerTupleV2) : Rat :=
  match rCore obs with
  | none => 0
  | some rc =>
      if _h : rEdge obs = 0 then
        0
      else
        (Rat.ofInt (Int.ofNat (rEdge obs - rc))) / (Rat.ofInt (Int.ofNat (rEdge obs)))

/-- Radialer Beobachter `R_v` als einfache ASL-kompatible Ableitung. -/
def Rv (obs : KeplerTupleV2) : Rat :=
  a obs * (1 + e obs)

/-- Zeit-Perioden-Surrogat `T ~ a^3` (normiert, ohne Physik-Claim). -/
def T (obs : KeplerTupleV2) : Rat :=
  (a obs) ^ (3 : Nat)

/-- Hilfspraedikat fuer explizite Behandlung des all-zero-Falls. -/
def isDegenerateAllZero (obs : KeplerTupleV2) : Bool :=
  match rCore obs with
  | none => true
  | some _ => false

/-- Explizites Prädikat: `r_core` ist definiert und strikt positiv. -/
def HasPositiveCore (obs : KeplerTupleV2) : Prop :=
  ∃ rc : Nat, rCore obs = some rc ∧ 0 < rc

/-! ## H2/H3/H4/H5/H10-Block (Kepler-EABC Ladder) -/

structure PartitionType where
  rCore : Option Nat
  rEdge : Nat
deriving Repr, DecidableEq

def partitionType (obs : KeplerTupleV2) : PartitionType :=
  ⟨rCore obs, rEdge obs⟩

def partitionTypeOfDistances (ds : List Nat) : PartitionType :=
  ⟨minNat? (ds.filter (fun d => 0 < d)), (match maxNat? ds with | none => 0 | some d => d)⟩

def aOfPartitionType (pt : PartitionType) : Rat :=
  match pt.rCore with
  | none => 0
  | some rc => (Rat.ofInt (Int.ofNat (rc + pt.rEdge))) / 2

def eOfPartitionType (pt : PartitionType) : Rat :=
  match pt.rCore with
  | none => 0
  | some rc =>
      if _h : pt.rEdge = 0 then
        0
      else
        (Rat.ofInt (Int.ofNat (pt.rEdge - rc))) / (Rat.ofInt (Int.ofNat pt.rEdge))

def RvOfPartitionType (pt : PartitionType) : Rat :=
  aOfPartitionType pt * (1 + eOfPartitionType pt)

@[simp] theorem e_eq_eOfPartitionType (obs : KeplerTupleV2) :
    e obs = eOfPartitionType (partitionType obs) := by
  rfl

@[simp] theorem Rv_eq_RvOfPartitionType (obs : KeplerTupleV2) :
    Rv obs = RvOfPartitionType (partitionType obs) := by
  rfl

/-- H2 (praktikable Form): gleiche Partitionstypen implizieren gleiches `e`. -/
theorem H2_e_invariant_on_partitionType
    (obs1 obs2 : KeplerTupleV2)
    (hpt : partitionType obs1 = partitionType obs2) :
    e obs1 = e obs2 := by
  simpa [e_eq_eOfPartitionType] using congrArg eOfPartitionType hpt

/-- H2 (praktikable Form): gleiche Partitionstypen implizieren gleiches `R_v`. -/
theorem H2_Rv_invariant_on_partitionType
    (obs1 obs2 : KeplerTupleV2)
    (hpt : partitionType obs1 = partitionType obs2) :
    Rv obs1 = Rv obs2 := by
  simpa [Rv_eq_RvOfPartitionType] using congrArg RvOfPartitionType hpt

/-- H2-TODO: vollstaendige Permutationsinvarianz auf Distanzlistenebene. -/
def H2_permutation_invariance_statement : Prop :=
  ∀ ds1 ds2 : List Nat, ds1.Perm ds2 →
    partitionTypeOfDistances ds1 = partitionTypeOfDistances ds2

/-- H3: Kreis-Kriterium wird definitorisch ueber `e = 0` gefasst. -/
def IsCircle (obs : KeplerTupleV2) : Prop :=
  e obs = 0

theorem H3_circle_criterion (obs : KeplerTupleV2) :
    IsCircle obs ↔ e obs = 0 := Iff.rfl

/-- H4: Exzentrizitaets-Kriterium wird definitorisch ueber `0 < e` gefasst. -/
def IsEccentric (obs : KeplerTupleV2) : Prop :=
  0 < e obs

theorem H4_eccentricity_criterion (obs : KeplerTupleV2) :
    IsEccentric obs ↔ 0 < e obs := Iff.rfl

/-- H5 (defensiv): Zeitachse `T` bleibt ein definitorischer Surrogatkanal. -/
def H5_time_surrogate_statement : Prop :=
  ∀ obs : KeplerTupleV2, T obs = (a obs) ^ (3 : Nat)

theorem H5_time_surrogate_definitional : H5_time_surrogate_statement := by
  intro obs
  rfl

/-- H10: orientierungsnahe Signatur als Summenvektor relativ zum Zentrum. -/
def orientationSignature (obs : KeplerTupleV2) : Int × Int :=
  obs.offsets.foldl
    (fun acc p => (acc.1 + (p.1 - obs.c.1), acc.2 + (p.2 - obs.c.2)))
    (0, 0)

/-- H10: betragsnahe Signatur ueber den radialen Randwert. -/
def magnitudeSignature (obs : KeplerTupleV2) : Nat :=
  rEdge obs

def orientationMagnitudePair (obs : KeplerTupleV2) : (Int × Int) × Nat :=
  (orientationSignature obs, magnitudeSignature obs)

theorem H10_orientation_magnitude_pair_definitional (obs : KeplerTupleV2) :
    orientationMagnitudePair obs = (orientationSignature obs, magnitudeSignature obs) := rfl

/-- H10-TODO: starker Entkopplungsclaim bleibt als offenes Statement markiert. -/
def H10_orientation_vs_magnitude_decoupling_statement : Prop :=
  ∀ obs1 obs2 : KeplerTupleV2,
    orientationSignature obs1 = orientationSignature obs2 →
    magnitudeSignature obs1 = magnitudeSignature obs2

theorem hasPositiveDistance_iff_exists_positiveDistance (obs : KeplerTupleV2) :
    hasPositiveDistance obs ↔ ∃ d, d ∈ distances obs ∧ 0 < d := by
  constructor
  · intro h
    rcases h with ⟨d, hd, hpos⟩
    exact ⟨d, hd, hpos⟩
  · intro h
    rcases h with ⟨d, hd, hpos⟩
    exact ⟨d, hd, hpos⟩

def sampleStandard : KeplerTupleV2 :=
  { c := (0, 0), offsets := [(1, 0), (0, 2), (-2, 0)] }

def sampleDegenerate : KeplerTupleV2 :=
  { c := (0, 0), offsets := [(0, 0), (0, 0)] }

/-- Randfall: Zentrumspunkt enthalten (`d_i = 0`), aber insgesamt nicht degeneriert. -/
def sampleCenterNonDegenerate : KeplerTupleV2 :=
  { c := (0, 0), offsets := [(0, 0), (1, 0)] }

theorem allDistancesZero_sampleDegenerate : allDistancesZero sampleDegenerate := by
  intro d hd
  simpa [sampleDegenerate, distances, sqDist] using hd

theorem sampleCenterNonDegenerate_has_center_distance :
    0 ∈ distances sampleCenterNonDegenerate := by
  simp [sampleCenterNonDegenerate, distances, sqDist]

theorem sampleCenterNonDegenerate_not_degenerate :
    isDegenerateAllZero sampleCenterNonDegenerate = false := by
  simp [sampleCenterNonDegenerate, isDegenerateAllZero, rCore, positiveDistances, distances, minNat?, sqDist]

theorem sampleCenterNonDegenerate_rCore :
    rCore sampleCenterNonDegenerate = some 1 := by
  simp [sampleCenterNonDegenerate, rCore, positiveDistances, distances, minNat?, sqDist]

theorem sampleCenterNonDegenerate_hasPositiveCore :
    HasPositiveCore sampleCenterNonDegenerate := by
  refine ⟨1, ?_, by decide⟩
  exact sampleCenterNonDegenerate_rCore

theorem sampleDegenerate_rEdge_zero : rEdge sampleDegenerate = 0 := by
  simp [sampleDegenerate, rEdge, distances, maxNat?, sqDist]

theorem sampleDegenerate_e_zero : e sampleDegenerate = 0 := by
  simp [sampleDegenerate, e, rCore, positiveDistances, distances, minNat?, sqDist]

theorem sampleDegenerate_T_zero : T sampleDegenerate = 0 := by
  native_decide

example : distances sampleStandard = [1, 4, 4] := rfl
example : rCore sampleStandard = some 1 := rfl
example : rEdge sampleStandard = 4 := rfl

example : distances sampleDegenerate = [0, 0] := rfl
example : rCore sampleDegenerate = none := rfl
example : isDegenerateAllZero sampleDegenerate = true := rfl
example : rCore sampleCenterNonDegenerate = some 1 := rfl
example : isDegenerateAllZero sampleCenterNonDegenerate = false := rfl

#eval distances sampleStandard
#eval rCore sampleStandard
#eval rEdge sampleStandard
#eval T sampleStandard

end CatalanNormalform
