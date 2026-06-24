# Gauß-Eisenstein-Formalisierung in Lean

**Status:** Strukturell vollständig, Build-Konfiguration benötigt Anpassung  
**Datum:** 24. Juni 2026

---

## Übersicht

Die neue Datei `CatalanNormalform/GaussEisenstein.lean` formalisiert die Verbindung zwischen EABC-Klassen und modularen Spaltungskriterien.

## Methodischer Fokus

**Was formalisiert ist:**
- ✅ Modulare Spaltungskriterien (p mod 4, p mod 3)
- ✅ Die vier zentralen Äquivalenzen (E, A, B, C ↔ Spaltungspaare)
- ✅ Alternative Definition von `factorEABCVector`
- ✅ Konzentrationsverhältnis H(n)

**Was NICHT formalisiert ist:**
- ❌ Volle Algebra von ℤ[i] oder ℤ[ω]
- ❌ Idealtheorie in quadratischen Körpern
- ❌ Explizite Normen oder Faktorisierungen

**Begründung:** Die modularen Kriterien sind mathematisch ausreichend und Lean-kompatibel.

---

## Kernstrukturen

### Spaltungsverhalten

```lean
inductive SplittingBehavior where
  | Split : SplittingBehavior
  | Inert : SplittingBehavior
  | Ramified : SplittingBehavior
```

### Modulare Kriterien

```lean
def gaussSplitting (p : Nat) : SplittingBehavior :=
  if p = 2 then Ramified
  else if p % 4 = 1 then Split
  else if p % 4 = 3 then Inert
  else Inert

def eisensteinSplitting (p : Nat) : SplittingBehavior :=
  if p = 3 then Ramified
  else if p % 3 = 1 then Split
  else if p % 3 = 2 then Inert
  else Inert
```

### Boolesche Prädikate

```lean
def gaussSplits (p : Nat) : Bool := p > 2 && p % 4 = 1
def gaussInert (p : Nat) : Bool := p > 2 && p % 4 = 3
def eisensteinSplits (p : Nat) : Bool := p > 3 && p % 3 = 1
def eisensteinInert (p : Nat) : Bool := p > 3 && p % 3 = 2
```

---

## Die vier zentralen Äquivalenzen

Diese Theoreme formalisieren die exakte Korrespondenz zwischen EABC-Klassen und modularen Spaltungspaaren:

```lean
theorem eabc_E_iff_gauss_eisenstein_split (p : Nat) (hp : p.Prime) (hp3 : p > 3) :
    p % 12 = 1 ↔ (p % 4 = 1 ∧ p % 3 = 1)

theorem eabc_A_iff_gauss_split_eisenstein_inert (p : Nat) (hp : p.Prime) (hp3 : p > 3) :
    p % 12 = 5 ↔ (p % 4 = 1 ∧ p % 3 = 2)

theorem eabc_B_iff_gauss_inert_eisenstein_split (p : Nat) (hp : p.Prime) (hp3 : p > 3) :
    p % 12 = 7 ↔ (p % 4 = 3 ∧ p % 3 = 1)

theorem eabc_C_iff_gauss_eisenstein_inert (p : Nat) (hp : p.Prime) (hp3 : p > 3) :
    p % 12 = 11 ↔ (p % 4 = 3 ∧ p % 3 = 2)
```

**Mathematische Grundlage:** Chinesischer Restsatz (ℤ/12ℤ ≅ ℤ/4ℤ × ℤ/3ℤ)

---

## Erweiterte FactorEABCVector-Definition

```lean
namespace FactorEABCVector

def fromSplittingBehavior (factors : List Nat) : FactorEABCVector :=
  let countSplitting := fun (f : Nat → SplittingPair) (g_split e_split : Bool) =>
    factors.count (fun p => 
      p > 3 && 
      (f p).gauss = (if g_split then Split else Inert) &&
      (f p).eisenstein = (if e_split then Split else Inert))
  { e := countSplitting SplittingPair.ofPrime true true,    -- (S, S)
    a := countSplitting SplittingPair.ofPrime true false,   -- (S, I)
    b := countSplitting SplittingPair.ofPrime false true,   -- (I, S)
    c := countSplitting SplittingPair.ofPrime false false } -- (I, I)

theorem factorEABCVector_equiv (n : Nat) :
    factorEABCVector n = fromSplittingBehavior (prime_factors n)
```

---

## Interpretation der Komponenten

Der EABC-Vektor v = (e, a, b, c) zählt Primfaktoren nach modularem Spaltungsverhalten:

| Komponente | Bedeutung | Gauß (mod 4) | Eisenstein (mod 3) |
|------------|-----------|--------------|---------------------|
| **e** | Beide spalten | Spaltet (1) | Spaltet (1) |
| **a** | Nur Gauß spaltet | Spaltet (1) | Inert (2) |
| **b** | Nur Eisenstein spaltet | Inert (3) | Spaltet (1) |
| **c** | Beide inert | Inert (3) | Inert (2) |

**Partitionierungen:**
- `gaussSplittingCount = e + a` (Gauß-spaltende Faktoren)
- `gaussInertCount = b + c` (Gauß-inerte Faktoren)
- `eisensteinSplittingCount = e + b` (Eisenstein-spaltende Faktoren)
- `eisensteinInertCount = a + c` (Eisenstein-inerte Faktoren)

---

## Konzentrationsverhältnis

```lean
noncomputable def concentrationRatio (v : FactorEABCVector) : ℝ :=
  if v.sum = 0 then 0 else (v.normSq : ℝ) / (v.sum ^ 2 : ℝ)

theorem concentration_bounds (v : FactorEABCVector) (h : v.sum > 0) :
    (1 : ℝ) / 4 ≤ concentrationRatio v ∧ concentrationRatio v ≤ 1
```

**Interpretation:**
- H(n) = 1: Maximale Konzentration (alle Faktoren haben denselben Spaltungstyp)
- H(n) = 1/4: Gleichverteilung über alle vier Spaltungstypen

---

## Beispiele

### n = 65 = 5 · 13

```
5:  mod 4 = 1 (spaltet), mod 3 = 2 (inert) → A
13: mod 4 = 1 (spaltet), mod 3 = 1 (spaltet) → E

v = (1, 1, 0, 0)
H = 2/4 = 0.5
```

### n = 77 = 7 · 11

```
7:  mod 4 = 3 (inert), mod 3 = 1 (spaltet) → B
11: mod 4 = 3 (inert), mod 3 = 2 (inert) → C

v = (0, 0, 1, 1)
H = 2/4 = 0.5
```

### n = 169 = 13²

```
13: mod 4 = 1 (spaltet), mod 3 = 1 (spaltet) → E
13: (wiederholt)

v = (2, 0, 0, 0)
H = 4/4 = 1 (maximal konzentriert)
```

---

## Verbindung zu H0.7

Falls Catalan-Magic mit ||v||² korreliert (H0.7), bedeutet dies:

> **Catalan-Strukturen sind sensitiv auf modulare Spaltungs-Konzentration.**

Dies wäre eine Verbindung zwischen:
- Kombinatorik (Catalan-Bäume)
- Modularer Arithmetik (p mod 4, p mod 3)
- Primfaktorzerlegung (EABC-Signatur)

---

## Offene Beweise (mit sorry markiert)

1. **Chinesischer Restsatz:** Die vollständigen Beweise der vier Äquivalenzen
2. **Primzahl-Charakterisierung:** `p > 3 ⇒ p % 12 ∈ {1, 5, 7, 11}`
3. **Konzentrationsgrenzen:** Beweis von 1/4 ≤ H ≤ 1
4. **Beispiel-Berechnungen:** Explizite Faktoren für 65, 77, 169

Diese Beweise sind mathematisch standard, aber erfordern zusätzliche Mathlib-Lemmata.

---

## Build-Status

**Aktuelles Problem:** Mathlib-Versionsinkompatibilität mit Lean 4.3.0

**Nächste Schritte:**
1. Mathlib-Version an Lean 4.3.0 anpassen
2. Lakefile-Konfiguration finalisieren
3. Fehlende Beweise vervollständigen
4. Integration mit bestehenden Modulen testen

---

## Dokumentations-Updates

- ✅ `CatalanNormalform.lean`: Import von `GaussEisenstein` hinzugefügt
- ✅ `lean/README.md`: Stufe 5c dokumentiert
- ✅ Methodische Klarstellungen in allen Kommentaren
- ✅ Keine Overclaims bezüglich Idealtheorie

---

## Mathematische Referenzen

- **Spaltungskriterien:** Ireland & Rosen, "A Classical Introduction to Modern Number Theory"
- **Chinesischer Restsatz:** Standard-Resultat der Zahlentheorie
- **EABC-Klassifikation:** Originalarbeit GAUSS_EISENSTEIN.md

---

## Zusammenfassung

Die Gauß-Eisenstein-Formalisierung ist **strukturell vollständig** und fokussiert konsequent auf modulare Kriterien. Die Beweise sind teilweise mit `sorry` markiert, aber die mathematische Struktur ist etabliert und präzise.

**Stärken:**
- Klare methodische Abgrenzung
- Keine Overclaims
- Mathematisch präzise Korrespondenz
- Erweiterbar für zukünftige Hypothesentests

**Nächste Priorität:** Build-Konfiguration und Vervollständigung der offenen Beweise.
