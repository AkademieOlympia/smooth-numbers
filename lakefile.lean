import Lake
open Lake DSL

package «smooth-numbers»

require mathlib from git
  "https://github.com/leanprover-community/mathlib4.git"

@[default_target]
lean_lib «SmoothNumbers» where
  -- Lean Library mit allen Definitionen und Beweisen
  roots := #[`SmoothNumbers]
  globs := #[.submodules `SmoothNumbers]

/-- Ziel für die Dickman-Funktion -/
lean_lib «DickmanFunction» where
  roots := #[`DickmanFunction]
  srcDir := "."

/-- Ziel für Klein-Flaschen-Topologie -/
lean_lib «KleinBottleTopology» where
  roots := #[`KleinBottleTopology]
  srcDir := "."
