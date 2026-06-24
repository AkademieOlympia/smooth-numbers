/-
Copyright (c) 2026 Thomas Hoffbauer. All rights reserved.
Released under Apache 2.0 license.
Authors: Thomas Hoffbauer

# Catalan-Normalform: Hauptmodul

Spektrale Catalan-Geometrie der EABC-Arithmetik.

Dieses Projekt formalisiert die kombinatorische Grundstruktur
der Catalan-Normalform-Theorie in Lean 4.

## Struktur

- `CTree`: Binäre Bäume mit k Blättern (Lean-Stufe 1)
- `Rotation`: Tamari-Rotation zwischen Bäumen (Lean-Stufe 2)
- `TamariGraph`: Der Tamari-Graph als SimpleGraph (Lean-Stufe 3)
- `Magic`: Catalan-Magic und Observablen (Lean-Stufe 4)
- `Arithmetic`: Verbindung zu Primfaktorzerlegungen
- `Hypotheses`: Formale Hypothesen, insbesondere H10 (Null-Modell)

## Philosophie

Lean formalisiert die **kombinatorische Architektur**.
Python testet die **empirischen Hypothesen**.

Die zentrale Forschungsfrage:

> Bleibt nach Entfernung der trivialen Ω(n)- und Kanonisierungs-Effekte
> ein arithmetischer Rest in der Catalan-Hierarchie?

Diese Frage wird in `Hypotheses.lean` als H10-Null-Modell formalisiert.
-/

import CatalanNormalform.CTree
import CatalanNormalform.Rotation
import CatalanNormalform.TamariGraph
import CatalanNormalform.Magic
import CatalanNormalform.Arithmetic
import CatalanNormalform.ShellVectorNorm
import CatalanNormalform.GaussEisenstein
import CatalanNormalform.Hypotheses

/-!
## Beispiele und Tests
-/

namespace CatalanNormalform

open CTree

/-!
### Beispiel 1: Die fünf Catalan-Bäume mit k=4
-/

/-- Baum 1: Linksbaum ((((•)(•))(•))(•)) -/
def t4_1 : CTree 4 := four_left

/-- Baum 2: (((•)(•))((•)(•))) -/
def t4_2 : CTree 4 := four_balanced

/-- Baum 3: (((•)((•)(•)))(•)) -/
def t4_3 : CTree 4 := node (node leaf (node leaf leaf)) leaf

/-- Baum 4: ((•)(((•)(•))(•))) -/
def t4_4 : CTree 4 := node leaf (node (node leaf leaf) leaf)

/-- Baum 5: Rechtsbaum ((•)((•)((•)(•)))) -/
def t4_5 : CTree 4 := node leaf (node leaf (node leaf leaf))

/-- Alle 5 Bäume sind verschieden. -/
example : t4_1 ≠ t4_2 := by decide
example : t4_2 ≠ t4_3 := by decide
example : t4_3 ≠ t4_4 := by decide
example : t4_4 ≠ t4_5 := by decide

/-!
### Beispiel 2: Tamari-Rotationen

t4_1 und t4_2 sind durch eine Rotation verbunden.
-/

example : TamariAdj t4_1 t4_3 := by
  left
  constructor

/-!
### Beispiel 3: Balancierte Bäume

t4_2 ist der einzige balancierte Baum mit k=4.
-/

example : is_balanced t4_2 := by
  unfold is_balanced four_balanced height
  norm_num

example : ¬is_balanced t4_1 := by
  unfold is_balanced t4_1 four_left height left_tree
  norm_num

/-!
### Beispiel 4: Magic-Werte

Der balancierte Baum hat Magic 0.
Der Linksbaum hat hohe Magic.
-/

-- theorem : catalan_magic t4_2 = 0 := balanced_has_zero_magic t4_2 (by decide)

/-!
## Nächste Schritte

Die Lean-Formalisierung ist jetzt bei **Stufe 5**: Objektstatus und H10.

**TODO:**

1. Vollständige Enumeration von CTree k für kleine k
2. Konstruktion aller Tamari-Rotationen explizit
3. Berechnung von tamari_dist für kleine Beispiele
4. Beweis von tamariAdj_irrefl (aktuell sorry)
5. Integration mit Mathlib.Combinatorics.Enumerative.Catalan

**Python-Seite:**

1. E01: Tamari-Baseline implementieren
2. E02: Kanonisierungstest
3. E03: Residualisierung und H10-Test (Go/No-Go)
4. E04-E05: Falls H10 falsifiziert
-/

end CatalanNormalform
