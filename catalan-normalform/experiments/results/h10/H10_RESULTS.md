# H10: Catalan-Magic Information Test

**Datum:** 2026-06-24 15:15:18

---

## Zentrale Frage

> **H10:** Trägt M_C(n) zusätzliche Information über S(n) = v₂ + v₃ hinaus,
> die nicht bereits in Ω(n) enthalten ist?

> Formal: **I(M_C; S | Ω) > 0 ?**

---

## Konfiguration

- **Datensatz:** n ∈ [2, 500]
- **Anzahl Zahlen:** 251
- **Ω-Filter:** Ω(n) ≥ 3
- **Kanonisierung:** balanced
- **Permutationen:** 1000
- **CV-Folds:** 5

## 🎯 ANTWORT

### NEIN

**Stärke:** none

**Statistisch signifikant:** Nein

---

## Modell-Ergebnisse

| Modell | Formel | R² | RMSE | #Samples |
|--------|--------|-----|------|----------|
| M0 | S(n) ~ 1 | 0.000000 | 1.5479 | 251 |
| M1 | S(n) ~ Ω(n) | 0.804870 | 0.6838 | 251 |
| M2 | S(n) ~ Ω(n) + M_C(n) | 0.805154 | 0.6833 | 251 |

## ΔR²-Analyse

| Übergang | ΔR² | Interpretation |
|----------|-----|----------------|
| M0 → M1 | 0.804870 | Ω-Gewinn |
| **M1 → M2** | **0.000284** | **M_C-Gewinn über Ω hinaus** |

## Interpretation

### Befund

ΔR²₂ = 0.000284 < 0.01: M_C trägt KEINE zusätzliche Information über S(n) hinaus, die nicht bereits in Ω(n) enthalten ist.

### Bedeutung

M_C(n) ist praktisch redundant zu Ω(n) für die Vorhersage von S(n). Es gibt keine erkennbare informationstheoretische Verbindung zwischen Catalan-Struktur und Schalen-Koordinaten über Ω hinaus.

### Empfehlungen

- H10 ist zurückgewiesen: I(M_C; S | Ω) ≈ 0
- Catalan-Magic und Schalen sind konditionell unabhängig gegeben Ω.

## Robustheitstests

### Permutationstest

- **ΔR²₂ (beobachtet):** 0.000284
- **ΔR²₂ (permutiert, Mittel):** 0.000777
- **ΔR²₂ (permutiert, Std):** 0.001091
- **p-Wert:** 0.5510
- **Signifikant (α = 0.05):** Nein

### Cross-Validation

- **CV R²₁ (Mittel):** 0.777083 ± 0.066959
- **CV R²₂ (Mittel):** 0.775461 ± 0.065578
- **CV ΔR² (Mittel):** -0.001622 ± 0.002258
- **Paired t-test:** t = -1.4366, p = 0.2242
- **Signifikant (α = 0.05):** Nein

### Residuenanalyse

- **Korrelation:** ρ(Residuen M1, M_C) = 0.036632
- **p-Wert:** 0.563494
- **Systematische Struktur:** Nein

## Visualisierungen

Siehe: `h10_visualizations.png`

1. R²-Progression über Modelle
2. ΔR²-Barplot
3. Permutationstest-Histogramm
4. Residuenanalyse (M1 vs. M_C)
5. Cross-Validation Scores
6. Scatter-Matrix (S vs. Prädiktoren)

## Daten

Siehe: `h10_delta_r2_test.csv`

---

*Generiert durch `h10_mc_information_test.py`*
