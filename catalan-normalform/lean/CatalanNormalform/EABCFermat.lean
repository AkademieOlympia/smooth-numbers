namespace CatalanNormalform

/-
EABC-Zaehlung fuer Prime-Residuenklassen modulo 12.
E := 1 mod 12, A := 5 mod 12, B := 7 mod 12, C := 11 mod 12.
-/
structure EABCCounter where
  e : Nat
  a : Nat
  b : Nat
  c : Nat
deriving DecidableEq, Repr

instance : Zero EABCCounter where
  zero := ⟨0, 0, 0, 0⟩

instance : Add EABCCounter where
  add x y := ⟨x.e + y.e, x.a + y.a, x.b + y.b, x.c + y.c⟩

@[simp] theorem zero_eabc : (0 : EABCCounter) = ⟨0, 0, 0, 0⟩ := rfl

@[simp] theorem add_eabc_fields (x y : EABCCounter) :
    x + y = ⟨x.e + y.e, x.a + y.a, x.b + y.b, x.c + y.c⟩ := rfl

def residueClassCounter (r : Nat) : EABCCounter :=
  match r % 12 with
  | 1 => ⟨1, 0, 0, 0⟩
  | 5 => ⟨0, 1, 0, 0⟩
  | 7 => ⟨0, 0, 1, 0⟩
  | 11 => ⟨0, 0, 0, 1⟩
  | _ => 0

def signatureOfFactors : List Nat → EABCCounter
  | [] => 0
  | p :: ps => residueClassCounter p + signatureOfFactors ps

@[simp] theorem signature_nil : signatureOfFactors [] = 0 := rfl

@[simp] theorem signature_cons (p : Nat) (ps : List Nat) :
    signatureOfFactors (p :: ps) = residueClassCounter p + signatureOfFactors ps := rfl

theorem signature_append_additive (xs ys : List Nat) :
    signatureOfFactors (xs ++ ys) = signatureOfFactors xs + signatureOfFactors ys := by
  induction xs with
  | nil =>
      simp [signatureOfFactors]
  | cons x xs ih =>
      simp [signatureOfFactors, ih, Nat.add_left_comm, Nat.add_comm]

def FactorizationWitness (n : Nat) := {fs : List Nat // fs.prod = n}

theorem signature_mul_additive_under_factorizations
    {n m : Nat} (hn : FactorizationWitness n) (hm : FactorizationWitness m) :
    signatureOfFactors (hn.1 ++ hm.1) = signatureOfFactors hn.1 + signatureOfFactors hm.1 := by
  exact signature_append_additive hn.1 hm.1

theorem prod_append_of_witnesses
    {n m : Nat} (hn : FactorizationWitness n) (hm : FactorizationWitness m) :
    (hn.1 ++ hm.1).prod = n * m := by
  rcases hn with ⟨fs, hfs⟩
  rcases hm with ⟨gs, hgs⟩
  simp [List.prod_append, hfs, hgs]

/-
Vorbereiteter starker Statement-Block:
Eine globale, kanonische Signaturfunktion H : Nat -> EABCCounter
mit H (n*m) = H n + H m benoetigt eine festgelegte Faktorisierungswahl.
-/
def additiveCoreGlobalStatement : Prop :=
  ∃ H : Nat → EABCCounter, ∀ n m : Nat, H (n * m) = H n + H m

/-
6D-Kern (Phi) mit expliziten Faktorisierungszeugen.
Diese Version ist bewusst lokal/witness-basiert und vermeidet eine globale kanonische Faktorisierungswahl.
-/
structure PhiCounter where
  v2 : Nat
  v3 : Nat
  e : Nat
  a : Nat
  b : Nat
  c : Nat
deriving DecidableEq, Repr

instance : Zero PhiCounter where
  zero := ⟨0, 0, 0, 0, 0, 0⟩

instance : Add PhiCounter where
  add x y := ⟨x.v2 + y.v2, x.v3 + y.v3, x.e + y.e, x.a + y.a, x.b + y.b, x.c + y.c⟩

@[simp] theorem zero_phi : (0 : PhiCounter) = ⟨0, 0, 0, 0, 0, 0⟩ := rfl

@[simp] theorem add_phi_fields (x y : PhiCounter) :
    x + y = ⟨x.v2 + y.v2, x.v3 + y.v3, x.e + y.e, x.a + y.a, x.b + y.b, x.c + y.c⟩ := rfl

def residueClassCounter6 (p : Nat) : PhiCounter :=
  if p = 2 then
    ⟨1, 0, 0, 0, 0, 0⟩
  else if p = 3 then
    ⟨0, 1, 0, 0, 0, 0⟩
  else
    match p % 12 with
    | 1 => ⟨0, 0, 1, 0, 0, 0⟩
    | 5 => ⟨0, 0, 0, 1, 0, 0⟩
    | 7 => ⟨0, 0, 0, 0, 1, 0⟩
    | 11 => ⟨0, 0, 0, 0, 0, 1⟩
    | _ => 0

def signature6OfFactors : List Nat → PhiCounter
  | [] => 0
  | p :: ps => residueClassCounter6 p + signature6OfFactors ps

@[simp] theorem signature6_nil : signature6OfFactors [] = 0 := rfl

@[simp] theorem signature6_cons (p : Nat) (ps : List Nat) :
    signature6OfFactors (p :: ps) = residueClassCounter6 p + signature6OfFactors ps := rfl

theorem signature6_append_additive (xs ys : List Nat) :
    signature6OfFactors (xs ++ ys) = signature6OfFactors xs + signature6OfFactors ys := by
  induction xs with
  | nil =>
      simp [signature6OfFactors]
  | cons x xs ih =>
      simp [signature6OfFactors, ih, Nat.add_left_comm, Nat.add_comm]

def Phi (n : Nat) (hn : FactorizationWitness n) : PhiCounter :=
  signature6OfFactors hn.1

def mulWitness {n m : Nat} (hn : FactorizationWitness n) (hm : FactorizationWitness m) :
    FactorizationWitness (n * m) :=
  ⟨hn.1 ++ hm.1, prod_append_of_witnesses hn hm⟩

theorem Phi_mul_additive_with_witnesses
    {n m : Nat} (hn : FactorizationWitness n) (hm : FactorizationWitness m) :
    Phi (n * m) (mulWitness hn hm) = Phi n hn + Phi m hm := by
  simp [Phi, mulWitness, signature6_append_additive]

/-! ## H0-Block: Additiver Kern (formal) -/

/-- H0 (Kernsatz): witness-basierte Additivitaet von `Phi` auf Produkten. -/
theorem H0_additive_core_phi
    {n m : Nat} (hn : FactorizationWitness n) (hm : FactorizationWitness m) :
    Phi (n * m) (mulWitness hn hm) = Phi n hn + Phi m hm :=
  Phi_mul_additive_with_witnesses hn hm

/-- TODO-Grenze: globale kanonische Faktorisierungsfunktion fuer witness-freies `Phi : Nat -> PhiCounter`. -/
def Phi_global_monoid_hom_statement : Prop :=
  ∃ Φ : Nat → PhiCounter, ∀ n m : Nat, Φ (n * m) = Φ n + Φ m

def H (x : PhiCounter) : EABCCounter := ⟨x.e, x.a, x.b, x.c⟩

@[simp] theorem H_additive (x y : PhiCounter) :
    H (x + y) = H x + H y := rfl

theorem H_mul_additive_with_witnesses
    {n m : Nat} (hn : FactorizationWitness n) (hm : FactorizationWitness m) :
    H (Phi (n * m) (mulWitness hn hm)) = H (Phi n hn) + H (Phi m hm) := by
  calc
    H (Phi (n * m) (mulWitness hn hm)) = H (Phi n hn + Phi m hm) := by
      simpa using congrArg H (Phi_mul_additive_with_witnesses hn hm)
    _ = H (Phi n hn) + H (Phi m hm) := rfl

/-- H0 (4D-Projektion): Additivitaet erbt auf `H`. -/
theorem H0_additive_core_H
    {n m : Nat} (hn : FactorizationWitness n) (hm : FactorizationWitness m) :
    H (Phi (n * m) (mulWitness hn hm)) = H (Phi n hn) + H (Phi m hm) :=
  H_mul_additive_with_witnesses hn hm

/-
Quaternionische Einbettung als additive Platzhalter-Struktur:
ohne Multiplikationsclaim auf der Zielseite.
-/
structure HQuaternion where
  re : Nat
  i : Nat
  j : Nat
  k : Nat
deriving DecidableEq, Repr

instance : Zero HQuaternion where
  zero := ⟨0, 0, 0, 0⟩

instance : Add HQuaternion where
  add x y := ⟨x.re + y.re, x.i + y.i, x.j + y.j, x.k + y.k⟩

def iota (x : EABCCounter) : HQuaternion := ⟨x.e, x.a, x.b, x.c⟩

@[simp] theorem iota_additive (x y : EABCCounter) :
    iota (x + y) = iota x + iota y := rfl

theorem iota_injective : Function.Injective iota := by
  intro x y h
  cases x
  cases y
  cases h
  rfl

def GammaQ_i : Nat → Unit := fun _ => ()

def Phi_G (n : Nat) (hn : FactorizationWitness n) : PhiCounter × Unit :=
  (Phi n hn, GammaQ_i n)

def Phi_ASL_K (K : Type) (GammaK : Nat → K) (n : Nat) (hn : FactorizationWitness n) :
    PhiCounter × K :=
  (Phi n hn, GammaK n)

@[simp] theorem Phi_G_core (n : Nat) (hn : FactorizationWitness n) :
    (Phi_G n hn).1 = Phi n hn := rfl

@[simp] theorem Phi_ASL_K_core (K : Type) (GammaK : Nat → K) (n : Nat) (hn : FactorizationWitness n) :
    (Phi_ASL_K K GammaK n hn).1 = Phi n hn := rfl

theorem sq_mod12_5 : (5 ^ 2) % 12 = 1 := by decide
theorem sq_mod12_7 : (7 ^ 2) % 12 = 1 := by decide
theorem sq_mod12_11 : (11 ^ 2) % 12 = 1 := by decide

theorem pow_mod12_of_base_mod_one (x q : Nat) (hx : x % 12 = 1) :
    (x ^ q) % 12 = 1 := by
  induction q with
  | zero =>
      simp
  | succ q ih =>
      calc
        (x ^ (q + 1)) % 12 = ((x ^ q) * x) % 12 := by simp [Nat.pow_succ]
        _ = (((x ^ q) % 12) * (x % 12)) % 12 := by
              simp [Nat.mul_mod]
        _ = 1 := by simp [ih, hx]

theorem pow_mod12_parity_of_square_one (b n : Nat) (hsq : (b ^ 2) % 12 = 1) :
    (b ^ n) % 12 = (b ^ (n % 2)) % 12 := by
  let q := n / 2
  let r := n % 2
  have hn : n = 2 * q + r := by
    dsimp [q, r]
    exact (Nat.div_add_mod n 2).symm
  have hpowOne : ((b ^ 2) ^ q) % 12 = 1 := pow_mod12_of_base_mod_one (b ^ 2) q hsq
  have hleft :
      b ^ n = (b ^ 2) ^ q * b ^ r := by
    calc
      b ^ n = b ^ (2 * q + r) := by simp [hn]
      _ = b ^ (2 * q) * b ^ r := by simp [Nat.pow_add]
      _ = (b ^ 2) ^ q * b ^ r := by simp [Nat.pow_mul]
  have hright : (((b ^ 2) ^ q) * b ^ r) % 12 = (b ^ r) % 12 := by
    calc
      (((b ^ 2) ^ q) * b ^ r) % 12
          = ((((b ^ 2) ^ q) % 12) * ((b ^ r) % 12)) % 12 := by simp [Nat.mul_mod]
      _ = (1 * ((b ^ r) % 12)) % 12 := by simp [hpowOne]
      _ = (b ^ r) % 12 := by simp
  calc
    (b ^ n) % 12 = ((b ^ 2) ^ q * b ^ r) % 12 := by simp [hleft]
    _ = (b ^ r) % 12 := hright
    _ = (b ^ (n % 2)) % 12 := by
      simp [r]

theorem mul_mod12_congr {x x' y y' : Nat}
    (hx : x % 12 = x' % 12) (hy : y % 12 = y' % 12) :
    (x * y) % 12 = (x' * y') % 12 := by
  calc
    (x * y) % 12 = ((x % 12) * (y % 12)) % 12 := by simp [Nat.mul_mod]
    _ = ((x' % 12) * (y' % 12)) % 12 := by simp [hx, hy]
    _ = (x' * y') % 12 := by simp [Nat.mul_mod]

theorem one_class_neutral_mod12 (e a b c : Nat) :
    ((1 ^ e) * (5 ^ a) * (7 ^ b) * (11 ^ c)) % 12 = ((5 ^ a) * (7 ^ b) * (11 ^ c)) % 12 := by
  simp

theorem fermat_parity_projection_mod12 (a b c : Nat) :
    ((5 ^ a) * (7 ^ b) * (11 ^ c)) % 12 =
      ((5 ^ (a % 2)) * (7 ^ (b % 2)) * (11 ^ (c % 2))) % 12 := by
  have h5 : (5 ^ a) % 12 = (5 ^ (a % 2)) % 12 :=
    pow_mod12_parity_of_square_one 5 a sq_mod12_5
  have h7 : (7 ^ b) % 12 = (7 ^ (b % 2)) % 12 :=
    pow_mod12_parity_of_square_one 7 b sq_mod12_7
  have h11 : (11 ^ c) % 12 = (11 ^ (c % 2)) % 12 :=
    pow_mod12_parity_of_square_one 11 c sq_mod12_11
  have h57 :
      ((5 ^ a) * (7 ^ b)) % 12 = ((5 ^ (a % 2)) * (7 ^ (b % 2))) % 12 :=
    mul_mod12_congr h5 h7
  exact mul_mod12_congr h57 h11

theorem fermat_parity_projection_with_e_mod12 (e a b c : Nat) :
    ((1 ^ e) * (5 ^ a) * (7 ^ b) * (11 ^ c)) % 12 =
      ((5 ^ (a % 2)) * (7 ^ (b % 2)) * (11 ^ (c % 2))) % 12 := by
  calc
    ((1 ^ e) * (5 ^ a) * (7 ^ b) * (11 ^ c)) % 12
        = ((5 ^ a) * (7 ^ b) * (11 ^ c)) % 12 := one_class_neutral_mod12 e a b c
    _ = ((5 ^ (a % 2)) * (7 ^ (b % 2)) * (11 ^ (c % 2))) % 12 := fermat_parity_projection_mod12 a b c

/-! ## H1-Block: Mod-12-Paritaetsprojektion (formal) -/

/-- H1: Mod-12-Kern wird durch die Paritaeten von `a,b,c` getragen; `e` ist neutral. -/
theorem H1_mod12_parity_projection (e a b c : Nat) :
    ((1 ^ e) * (5 ^ a) * (7 ^ b) * (11 ^ c)) % 12 =
      ((5 ^ (a % 2)) * (7 ^ (b % 2)) * (11 ^ (c % 2))) % 12 :=
  fermat_parity_projection_with_e_mod12 e a b c

theorem mod12_kernel_depends_only_on_parity
    (a b c a' b' c' : Nat)
    (ha : a % 2 = a' % 2)
    (hb : b % 2 = b' % 2)
    (hc : c % 2 = c' % 2) :
    ((5 ^ a) * (7 ^ b) * (11 ^ c)) % 12 = ((5 ^ a') * (7 ^ b') * (11 ^ c')) % 12 := by
  calc
    ((5 ^ a) * (7 ^ b) * (11 ^ c)) % 12
        = ((5 ^ (a % 2)) * (7 ^ (b % 2)) * (11 ^ (c % 2))) % 12 := fermat_parity_projection_mod12 a b c
    _ = ((5 ^ (a' % 2)) * (7 ^ (b' % 2)) * (11 ^ (c' % 2))) % 12 := by
        have h57 :
            ((5 ^ (a % 2)) * (7 ^ (b % 2))) % 12 = ((5 ^ (a' % 2)) * (7 ^ (b' % 2))) % 12 :=
          mul_mod12_congr (by simp [ha]) (by simp [hb])
        exact mul_mod12_congr h57 (by simp [hc])
    _ = ((5 ^ a') * (7 ^ b') * (11 ^ c')) % 12 := by
        symm
        exact fermat_parity_projection_mod12 a' b' c'

/-- H1 (Aequivalenzform): gleiche Paritaeten implizieren gleichen Mod-12-Kern. -/
theorem H1_mod12_kernel_depends_only_on_parity
    (a b c a' b' c' : Nat)
    (ha : a % 2 = a' % 2)
    (hb : b % 2 = b' % 2)
    (hc : c % 2 = c' % 2) :
    ((5 ^ a) * (7 ^ b) * (11 ^ c)) % 12 = ((5 ^ a') * (7 ^ b') * (11 ^ c')) % 12 :=
  mod12_kernel_depends_only_on_parity a b c a' b' c' ha hb hc

/-! ## Boundary-Lemmas (Kern + mod-12) -/

/-- Kanonischer Witness fuer `n = 1`. -/
def witnessOne : FactorizationWitness 1 := ⟨[], by simp⟩

@[simp] theorem Phi_one_witnessOne : Phi 1 witnessOne = 0 := rfl

@[simp] theorem H_Phi_one_witnessOne : H (Phi 1 witnessOne) = 0 := rfl

/-- EABC-Masse (`Omega`) als Summe der 4D-Kernkoordinaten. -/
def OmegaEABC (x : PhiCounter) : Nat :=
  x.e + x.a + x.b + x.c

@[simp] theorem OmegaEABC_zero : OmegaEABC (0 : PhiCounter) = 0 := rfl

@[simp] theorem OmegaEABC_add (x y : PhiCounter) :
    OmegaEABC (x + y) = OmegaEABC x + OmegaEABC y := by
  simp [OmegaEABC, Nat.add_left_comm, Nat.add_comm]

/-- Reine 2/3-Schalen tragen keine EABC-Masse. -/
def IsTwoThree (p : Nat) : Prop := p = 2 ∨ p = 3

theorem OmegaEABC_residue_two_three (p : Nat) (hp : IsTwoThree p) :
    OmegaEABC (residueClassCounter6 p) = 0 := by
  rcases hp with rfl | rfl <;> simp [residueClassCounter6, OmegaEABC]

theorem OmegaEABC_signature6_two_three_zero
    (fs : List Nat) (hfs : ∀ p ∈ fs, IsTwoThree p) :
    OmegaEABC (signature6OfFactors fs) = 0 := by
  induction fs with
  | nil =>
      simp [signature6OfFactors, OmegaEABC]
  | cons p ps ih =>
      have hp : IsTwoThree p := hfs p (by simp)
      have hps : ∀ q ∈ ps, IsTwoThree q := by
        intro q hq
        exact hfs q (by simp [hq])
      calc
        OmegaEABC (signature6OfFactors (p :: ps))
            = OmegaEABC (residueClassCounter6 p + signature6OfFactors ps) := rfl
        _ = OmegaEABC (residueClassCounter6 p) + OmegaEABC (signature6OfFactors ps) :=
              OmegaEABC_add _ _
        _ = 0 + 0 := by simp [OmegaEABC_residue_two_three p hp, ih hps]
        _ = 0 := by simp

theorem H_of_v2_v3_only (v2 v3 : Nat) :
    H ⟨v2, v3, 0, 0, 0, 0⟩ = 0 := rfl

theorem OmegaEABC_Phi_two_three_shell_zero
    {n : Nat} (hn : FactorizationWitness n)
    (hfs : ∀ p ∈ hn.1, IsTwoThree p) :
    OmegaEABC (Phi n hn) = 0 := by
  simpa [Phi] using OmegaEABC_signature6_two_three_zero hn.1 hfs

/-! ## H9-Block: Zentrierter Vektor als additive Bruecke -/

structure CenteredVector where
  da : Int
  db : Int
  dc : Int
deriving DecidableEq, Repr

instance : Add CenteredVector where
  add x y := ⟨x.da + y.da, x.db + y.db, x.dc + y.dc⟩

/--
`centeredByE` kodiert die EABC-Komponenten als gegen `e` zentrierte Int-Differenzen.
Dies ist eine rein strukturelle Bruecke, keine statistische Aussage.
-/
def centeredByE (x : EABCCounter) : CenteredVector :=
  ⟨Int.ofNat x.a - Int.ofNat x.e, Int.ofNat x.b - Int.ofNat x.e, Int.ofNat x.c - Int.ofNat x.e⟩

/-- Unzentrierter Int-Lift als additiver Hilfskanal. -/
def liftABC (x : EABCCounter) : CenteredVector :=
  ⟨Int.ofNat x.a, Int.ofNat x.b, Int.ofNat x.c⟩

/-- H9 (teilweise formal): der unzentrierte Lift ist streng additiv. -/
theorem H9_liftABC_additive (x y : EABCCounter) :
    liftABC (x + y) = liftABC x + liftABC y := by
  cases x <;> cases y <;> rfl

/-- H9-Statementgrenze: Additivitaet der e-zentrierten Darstellung bleibt als TODO markiert. -/
def H9_centeredByE_additive_statement : Prop :=
  ∀ x y : EABCCounter, centeredByE (x + y) = centeredByE x + centeredByE y

/-- H9-Statementgrenze: witness-freie globale Zentrierungsadditivitaet als TODO-Interface. -/
def H9_global_centered_statement : Prop :=
  ∃ Hglob : Nat → EABCCounter,
    (∀ n m : Nat, Hglob (n * m) = Hglob n + Hglob m) ∧
    (∀ n m : Nat, centeredByE (Hglob (n * m)) = centeredByE (Hglob n) + centeredByE (Hglob m))

theorem mod12_parity_000 :
    ((5 ^ 0) * (7 ^ 0) * (11 ^ 0)) % 12 = 1 := by decide
theorem mod12_parity_100 :
    ((5 ^ 1) * (7 ^ 0) * (11 ^ 0)) % 12 = 5 := by decide
theorem mod12_parity_010 :
    ((5 ^ 0) * (7 ^ 1) * (11 ^ 0)) % 12 = 7 := by decide
theorem mod12_parity_001 :
    ((5 ^ 0) * (7 ^ 0) * (11 ^ 1)) % 12 = 11 := by decide
theorem mod12_parity_110 :
    ((5 ^ 1) * (7 ^ 1) * (11 ^ 0)) % 12 = 11 := by decide
theorem mod12_parity_101 :
    ((5 ^ 1) * (7 ^ 0) * (11 ^ 1)) % 12 = 7 := by decide
theorem mod12_parity_011 :
    ((5 ^ 0) * (7 ^ 1) * (11 ^ 1)) % 12 = 5 := by decide
theorem mod12_parity_111 :
    ((5 ^ 1) * (7 ^ 1) * (11 ^ 1)) % 12 = 1 := by decide

end CatalanNormalform
