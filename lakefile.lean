import Lake
open Lake DSL

package «smooth-numbers» where
  -- Einstellungen für das Paket
  version := v!"0.1.0"
  keywords := #["number-theory", "smooth-numbers", "dickman-function"]
  leanOptions := #[
    ⟨`pp.unicode.fun, true⟩,
    ⟨`pp.proofs.withType, false⟩
  ]

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
