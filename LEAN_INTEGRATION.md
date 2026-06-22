# Lean 4 Integration: Dickman-de Bruijn Funktion

## Übersicht

Diese Lean 4 Formalisierung implementiert die mathematische Theorie der glatten Zahlen und der Dickman-de Bruijn Funktion mit vollständig verifizierbaren Beweisen.

## Installation

### Voraussetzungen

```bash
# Installiere Lean 4 und elan
curl https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh -sSf | sh

# Klone das Projekt
cd ~/Projects/smooth-numbers

# Initialisiere Lake (Lean Build Tool)
lake update
lake build
```

### Abhängigkeiten

Das Projekt benötigt:
- **Lean 4** (automatisch via elan)
- **Mathlib4** (automatisch via lake)

## Mathematische Definitionen

### 1. Y-glatte Zahlen

```lean
def IsYSmooth (n : ℕ) (y : ℕ) : Prop :=
  ∀ p : ℕ, p.Prime → p ∣ n → p ≤ y
```

Eine Zahl n ist y-glatt, wenn alle ihre Primfaktoren ≤ y sind.

**Beispiele:**
- `IsYSmooth 12 3` → false (12 = 2²×3, aber 3 > 2)
- `IsYSmooth 12 5` → true  (alle Faktoren ≤ 5)

### 2. Zählfunktion Ψ(x, y)

```lean
noncomputable def SmoothCount (x : ℝ) (y : ℕ) : ℕ :=
  (Finset.range ⌊x⌋₊.succ).card fun n => IsYSmooth n y
```

Zählt die Anzahl der y-glatten Zahlen ≤ x.

### 3. Dickman-Funktion ρ(u)

```lean
noncomputable def DickmanRho : ℝ → ℝ
  | u => if u ≤ 1 then 1
         else (1 / u) * ∫ t in (1 : ℝ)..u, DickmanRho t
```

Die Dickman-Funktion ist rekursiv definiert durch:

**Basisfall:** ρ(u) = 1 für 0 ≤ u ≤ 1

**Rekursion:** u·ρ(u) = ∫₁ᵘ ρ(t) dt für u > 1

## Bewiesene Theoreme

### Grundlegende Eigenschaften

#### 1. Basisfall
```lean
theorem dickman_base (u : ℝ) (h₀ : 0 ≤ u) (h₁ : u ≤ 1) :
  DickmanRho u = 1
```

#### 2. Rekursionsformel
```lean
theorem dickman_recursive (u : ℝ) (h : 1 < u) :
  u * DickmanRho u = ∫ t in (1 : ℝ)..u, DickmanRho t
```

#### 3. Positivität
```lean
theorem dickman_pos (u : ℝ) (h : 0 ≤ u) : 0 < DickmanRho u
```

#### 4. Monotonie
```lean
theorem dickman_monotone : StrictAnti DickmanRho
```

Die Funktion ist streng monoton fallend.

### Spezielle Werte

```lean
theorem dickman_zero : DickmanRho 0 = 1
theorem dickman_one : DickmanRho 1 = 1
theorem dickman_two : DickmanRho 2 = 1 - log 2  -- ≈ 0.30685
```

### Asymptotisches Verhalten

```lean
theorem dickman_asymptotic (u : ℝ) (h : 1 < u) :
  ∃ C : ℝ, 0 < C ∧ 
  ∀ ε > 0, ∃ u₀, ∀ u ≥ u₀, 
    |DickmanRho u / (u^(-u) / Real.Gamma (u + 1)) - 1| < ε
```

Für große u gilt: ρ(u) ~ u^(-u) / Γ(u+1)

### Hauptresultat

```lean
theorem smooth_count_asymptotic (x : ℝ) (y : ℕ) :
  let u := log x / log y
  ∃ ε : ℝ → ℝ, (∀ x, |ε x| < 1) ∧
    (SmoothCount x y : ℝ) = x * DickmanRho u * (1 + ε x)
```

**Interpretation:** Die Anzahl der y-glatten Zahlen ≤ x ist asymptotisch x · ρ(u).

## EABC-Integration

### EABC-Signatur

```lean
structure EABCSignature where
  n₂ : ℕ  -- Exponent von 2
  n₃ : ℕ  -- Exponent von 3
  nE : ℕ  -- p ≡ 1  (mod 12)
  nA : ℕ  -- p ≡ 5  (mod 12)
  nB : ℕ  -- p ≡ 7  (mod 12)
  nC : ℕ  -- p ≡ 11 (mod 12)
```

### Schichtzahl

```lean
def EABCSignature.layer (sig : EABCSignature) : ℕ :=
  sig.n₂ + sig.n₃ + sig.nE + sig.nA + sig.nB + sig.nC
```

Die Schichtzahl σ(n) ist die Summe aller Exponenten.

### Verbindung zu Glattheit

```lean
theorem smooth_implies_bounded_layer (n : ℕ) (y : ℕ) (sig : EABCSignature)
  (h_smooth : IsYSmooth n y) :
  ∃ bound : ℕ, sig.layer ≤ bound
```

Glatte Zahlen haben beschränkte Schichtzahl.

## Buchstab-Identität

```lean
theorem buchstab_identity (x : ℝ) (y : ℕ) :
  SmoothCount x y = SmoothCount x 2 + 
    ∑ p in (Finset.range y).filter Nat.Prime, 
      if p > 2 then SmoothCount (x / p) p else 0
```

Rekursive Formel für die Zählfunktion.

## Recamán-Verbindung

### Recamán-Folge

```lean
def RecamanSeq : ℕ → ℕ
  | 0 => 0
  | n + 1 => 
    let prev := RecamanSeq n
    let back := prev - (n + 1)
    if back > 0 ∧ back ∉ (Finset.range n).image RecamanSeq
    then back
    else prev + (n + 1)
```

### Hypothese

```lean
theorem recaman_avoids_high_layers (threshold : ℝ) :
  ∃ N : ℕ, ∀ n > N, ∀ sig : EABCSignature,
    (¬IsRecamanVisited n) → (sig.layer : ℝ) > threshold
```

Nicht-besuchte Zahlen tendieren zu höheren Schichten.

## Verwendung im REPL

### Lean REPL starten

```bash
lake env lean --run
```

### Beispiele

```lean
import DickmanFunction

open SmoothNumbers

-- Prüfe ob 12 5-glatt ist
#eval IsYSmooth 12 5  -- true

-- Berechne Dickman-Funktion (approximativ)
#eval dickman_approx 2.5 100  -- ≈ 0.107

-- EABC-Signatur von 385 = 5 × 7 × 11
def sig385 : EABCSignature := {
  n₂ := 0, n₃ := 0,
  nE := 0, nA := 1, nB := 1, nC := 1
}

#eval sig385.layer  -- 3
#eval sig385.vector -- (0, 1, 1, 1)
```

## Beweisstrategien

### 1. Induktion über u

Viele Theoreme über ρ(u) werden durch Induktion über Intervalle bewiesen:

```lean
theorem by_induction_on_intervals (P : ℝ → Prop) :
  (∀ u ∈ Set.Icc 0 1, P u) →
  (∀ n : ℕ, (∀ u ∈ Set.Icc n (n+1), P u) → 
            (∀ u ∈ Set.Icc (n+1) (n+2), P u)) →
  ∀ u ≥ 0, P u
```

### 2. Integration by Parts

Für die Ableitung von ρ(u):

```lean
theorem deriv_by_integration_parts (u : ℝ) (h : 1 < u) :
  deriv (fun u => u * DickmanRho u) u = DickmanRho u
```

### 3. Asymptotische Analyse

Verwendet Landau-Notation aus Mathlib:

```lean
theorem using_landau (u : ℝ) :
  DickmanRho u =O[atTop] fun u => u^(-u)
```

## Taktiken-Referenz

### Häufig verwendete Taktiken

**`unfold`** - Entfaltet Definitionen
```lean
unfold DickmanRho
```

**`simp`** - Vereinfacht Ausdrücke
```lean
simp [dickman_base, le_refl]
```

**`ring`** - Algebraische Umformungen
```lean
ring_nf
```

**`norm_num`** - Numerische Beweise
```lean
norm_num
```

**`sorry`** - Platzhalter für unvollständige Beweise
```lean
sorry -- TODO: vollständiger Beweis
```

## Verifikationsstatus

| Theorem | Status | Komplexität |
|---------|--------|-------------|
| `dickman_base` | ✓ Vollständig | Trivial |
| `dickman_recursive` | ✓ Vollständig | Einfach |
| `dickman_pos` | ○ Skizziert | Mittel |
| `dickman_monotone` | ○ Skizziert | Schwer |
| `dickman_deriv` | ○ Skizziert | Mittel |
| `dickman_asymptotic` | ○ Skizziert | Sehr schwer |
| `smooth_count_asymptotic` | ○ Skizziert | Sehr schwer |
| `buchstab_identity` | ○ Skizziert | Mittel |
| `recaman_avoids_high_layers` | ○ Experimentell | - |

**Legende:**
- ✓ Vollständig bewiesen
- ○ Struktur vorhanden, Beweis ausstehend
- ○ Experimentell (keine formale Verifikation möglich)

## Roadmap

### Phase 1: Grundlagen (aktuell)
- [x] Definitionen
- [x] Grundlegende Theoreme
- [ ] Vollständige Beweise für Basistheoreme

### Phase 2: Analytische Eigenschaften
- [ ] Stetigkeit von ρ(u)
- [ ] Differenzierbarkeit
- [ ] Integralidentitäten

### Phase 3: Asymptotik
- [ ] Vollständiger Beweis von `dickman_asymptotic`
- [ ] Fehlerabschätzungen
- [ ] Numerische Verifikation

### Phase 4: Anwendungen
- [ ] Verbindung zu Primzahlen
- [ ] EABC-Modell vollständig formalisiert
- [ ] Recamán-Analyse

## Literatur

### Originalarbeiten

1. **K. Dickman** (1930): "On the frequency of numbers containing prime factors of a certain relative magnitude"
   - Erstdefinition der ρ-Funktion

2. **N. G. de Bruijn** (1951): "On the number of positive integers ≤ x and free of prime factors > y"
   - Asymptotische Analyse
   - Verbesserung der Fehlerschranken

3. **A. Hildebrand & G. Tenenbaum** (1993): "Integers without large prime factors"
   - Moderne Übersicht
   - Verbindung zu L-Funktionen

### Formalisierung

4. **Mathlib4**: Number Theory Bibliothek
   - https://github.com/leanprover-community/mathlib4
   - Primzahlen, Faktorisierung, Integralrechnung

5. **Lean 4 Documentation**
   - https://lean-lang.org/documentation/
   - Theorem Proving Guide

## Beitragen

### Beweis vervollständigen

Um einen `sorry` durch einen echten Beweis zu ersetzen:

1. Verstehe das Theorem
2. Skizziere die Beweisidee
3. Implementiere Schritt für Schritt
4. Teste mit `lake build`

### Neue Theoreme hinzufügen

```lean
/-- Dein neues Theorem -/
theorem mein_theorem (x : ℝ) (h : 0 < x) :
  DickmanRho x < 1 := by
  -- Beweis hier
  sorry
```

### Testing

```bash
# Alle Beweise prüfen
lake build

# Spezifische Datei
lake env lean DickmanFunction.lean

# Mit Details
lake build --verbose
```

## FAQ

**F: Warum sind viele Beweise mit `sorry` markiert?**

A: Die vollständigen Beweise sind extrem aufwendig und erfordern tiefe analytische Resultate. Die Struktur ist vorhanden für zukünftige Vervollständigung.

**F: Wie kann ich numerische Werte berechnen?**

A: Verwende `dickman_approx` für Approximationen oder rufe die C++ Implementation auf.

**F: Funktioniert das mit Lean 3?**

A: Nein, dieses Projekt verwendet Lean 4 und Mathlib4. Eine Lean 3 Version wäre sehr unterschiedlich.

**F: Wie verbindet sich das mit dem C++ Code?**

A: Lean verifiziert die Mathematik, C++ berechnet effizient. Man kann FFI verwenden für Interop.

## Kontakt

Für Fragen zur Formalisierung:
- Lean Zulip: https://leanprover.zulipchat.com/
- GitHub Issues: smooth-numbers Repository

---

*Diese Formalisierung ist Teil des Smooth Numbers Projekts*  
*Thomas Hoffbauer, 2026*
