# H10: Catalan-Magic Information Test

**Datum:** 2026-06-24 15:15:58

---

## Zentrale Frage

> **H10:** Trägt M_C(n) zusätzliche Information über S(n) = v₂ + v₃ hinaus,
> die nicht bereits in Ω(n) enthalten ist?

> Formal: **I(M_C; S | Ω) > 0 ?**

---

## Konfiguration

- **Datensatz:** n ∈ [2, 1000]
- **Anzahl Zahlen:** 532
- **Ω-Filter:** Ω(n) ≥ 3
- **Kanonisierung:** balanced
- **Permutationen:** 500
- **CV-Folds:** 5

## 🎯 ANTWORT

### NEIN

**Stärke:** none

**Statistisch signifikant:** Nein

---

## Modell-Ergebnisse

| Modell | Formel | R² | RMSE | #Samples |
|--------|--------|-----|------|----------|
| M0 | S(n) ~ 1 | 0.000000 | 1.6053 | 532 |
| M1 | S(n) ~ Ω(n) | 0.800544 | 0.7169 | 532 |
| M2 | S(n) ~ Ω(n) + M_C(n) | 0.800832 | 0.7164 | 532 |

## ΔR²-Analyse

| Übergang | ΔR² | Interpretation |
|----------|-----|----------------|
| M0 → M1 | 0.800544 | Ω-Gewinn |
| **M1 → M2** | **0.000288** | **M_C-Gewinn über Ω hinaus** |

## Interpretation

### Befund

ΔR²₂ = 0.000288 < 0.01: M_C trägt KEINE zusätzliche Information über S(n) hinaus, die nicht bereits in Ω(n) enthalten ist.

### Bedeutung

M_C(n) ist praktisch redundant zu Ω(n) für die Vorhersage von S(n). Es gibt keine erkennbare informationstheoretische Verbindung zwischen Catalan-Struktur und Schalen-Koordinaten über Ω hinaus.

### Empfehlungen

- H10 ist zurückgewiesen: I(M_C; S | Ω) ≈ 0
- Catalan-Magic und Schalen sind konditionell unabhängig gegeben Ω.

## Robustheitstests

### Permutationstest

- **ΔR²₂ (beobachtet):** 0.000288
- **ΔR²₂ (permutiert, Mittel):** 0.000363
- **ΔR²₂ (permutiert, Std):** 0.000514
- **p-Wert:** 0.4000
- **Signifikant (α = 0.05):** Nein

### Cross-Validation

- **CV R²₁ (Mittel):** 0.795977 ± 0.047851
- **CV R²₂ (Mittel):** 0.796122 ± 0.048200
- **CV ΔR² (Mittel):** 0.000145 ± 0.000562
- **Paired t-test:** t = 0.5148, p = 0.6338
- **Signifikant (α = 0.05):** Nein

### Residuenanalyse

- **Korrelation:** ρ(Residuen M1, M_C) = 0.036120
- **p-Wert:** 0.405731
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
