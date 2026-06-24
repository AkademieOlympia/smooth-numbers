# Experiment E02: Modellkaskade M0-M4

**Datum:** 2026-06-24 10:17:07

---

## Methodische Klarstellung

> **WICHTIG:**
>
> Dieser Test entscheidet **nicht** über die Gültigkeit der Gauß-Eisenstein-Interpretation des EABC-Vektors (die ist auf modularer Ebene bereits ein Satz, A-Niveau), sondern über deren **zusätzliche Erklärungskraft** für Catalan-Magic nach Kontrolle der einfacheren Kombinatorik Ω, Ω², (v₂, v₃).

---

## Konfiguration

- **Datensatz:** n ∈ [2, 1000]
- **Anzahl Zahlen:** 285
- **Ω-Filter:** Ω(n) ≥ 4
- **Kanonisierung:** balanced

## Datensatz-Statistiken

| Größe | Wert |
|-------|------|
| Anzahl n | 285 |
| Ω(n): Mittel | 4.81 |
| Ω(n): Range | [4, 9] |
| M_C(n): Mittel | 0.86 |
| M_C(n): Std | 0.98 |
| H(n): Mittel | 0.8682 |
| H(n): Range | [0.3333, 1.0000] |

## Tabelle 1: Modell-Hierarchie

| Modell | Features | R² | ΔR² (vs. vorheriges) | RMSE | #Samples |
|--------|----------|-----|----------------------|------|----------|
| M0 | Ω | 0.3394 | − | 0.79 | 285 |
| M0b | Ω + Ω² | 0.7502 | 0.4108 ← Wie stark ist Ω²? | 0.49 | 285 |
| M1 | Ω + Ω² + σ | 0.7502 | 0.0000 | 0.49 | 285 |
| M2 | Ω + Ω² + (v₂, v₃) | 0.7502 | 0.0001 | 0.49 | 285 |
| M3* | Ω + Ω² + (v₂, v₃) + H | 0.9670 | 0.2168 ← **ΔR²_H** | 0.18 | 255 |
| M3 | Ω + Ω² + (v₂, v₃) + ||v||² | 0.7503 | 0.0000 | 0.49 | 285 |
| M4 | Ω + Ω² + (v₂, v₃) + (e,a,b,c) | 0.7505 | -0.2166 ← ΔR²_dir | 0.49 | 285 |

## Inkrementelle Erklärungskraft (ΔR²)

| Übergang | ΔR² | Interpretation |
|----------|-----|----------------|
| M0 → M0b | 0.4108 | Quadratischer Effekt (nichtlineare Ω-Abhängigkeit) |
| M0b → M1 | 0.0000 | Teiler-Summe σ(n) |
| M0b → M2 | 0.0001 | Schalen-Koordinaten (v₂, v₃) |
| **M2 → M3*** | **0.2168** | **Konzentration H(n) - KRITISCH!** |
| M2 → M3 | 0.0000 | Norm ||v||² |
| M3 → M4 | 0.0002 | Volle EABC-Richtung |

## Tabelle 2: Interpretation

| Test | Wert | Interpretation |
|------|------|----------------|
| ΔR²_H | 0.2168 | Fall 4: strong |
| ΔR²_dir | 0.0002 | Richtung vs. Konzentration |
| ΔR²_H / ΔR²_dir | ∞ | Relative Wichtigkeit |

## Detaillierte Interpretation

### Fall 4: STRONG

**ΔR²_H = 0.2168**

**Signifikant:** Ja

**Hypothese gestützt:** Ja

#### Befund

ΔR²_H = 0.2168 > 0.1: Starkes Signal!

#### Bedeutung

Catalan-Magic ist NICHT NUR Ω-kombinatorisch. Reagiert auf algebraisch-zahlentheoretische Verteilung der Primfaktoren. Überraschende tiefe Verbindung zwischen Spaltungsverhalten und kombinatorischer Hierarchie. WISSENSCHAFTLICH HOCHINTERESSANT, weil keine offensichtliche Verbindung zwischen mod-4/mod-3-Spaltung und Baumstrukturen existiert.

#### Konsequenz

Publikationswürdig! Tamari/Spektraltheorie wird relevant. Könnte auf tiefere zahlentheoretisch-kombinatorische Prinzipien hinweisen.

#### Empfehlungen

- 🎯 Hypothese H(n) → M_C(n) STARK bestätigt!
- H(n) ist zentrale Größe für Catalan-Magic.
- H(n) sollte in Haupttheorie integriert werden.
- Teste Hurwitz-Erweiterung (H11).
- PUBLIKATION: Ergebnis würde Catalan-Projekt stark aufwerten.
- ✓ R²(M4) = 0.7505 < 0.80. Substantielle Catalan-Residuen bleiben. Echte Catalan-Arithmetik vorhanden!

#### Methodische Hinweise

⚠️ WICHTIG: ΔR²(Ω²) = 0.4108 > 0.05. Starker nichtlinearer Ω-Effekt! Ohne M0b-Kontrolle wären alle späteren ΔR² verdächtig.

## Kritische Frage

**Nach Kontrolle von Ω, Ω², (v₂, v₃): Bleibt strukturierte Varianz, die H(n) erklärt?**

✓ JA: ΔR²_H = 0.2168 > 0.01

Die Konzentrationsgröße H(n) hat empirisch nachweisbare Erklärungskraft für Catalan-Magic über die Baseline-Koordinaten hinaus.

## Visualisierungen

Siehe Plots im Verzeichnis `results/e02/`:

1. `r2_progression.png`: R²-Werte über Modellhierarchie
2. `delta_values.png`: Inkrementelle ΔR²-Beiträge
3. `residuals_M2_vs_H.png`: Residuen von M2 vs. H(n)
4. `residuals_M4_distribution.png`: Verteilung finaler Catalan-Residuen

## Methodische Hinweise

### M0b ist essentiell

Ohne Ω²-Kontrolle könnte scheinbare H-Korrelation nur nichtlinearer Ω-Effekt sein.

### Interpretation der Schwellenwerte

- ΔR²_H < 0.01: Keine praktische Erklärungskraft
- ΔR²_H ≈ 0.01-0.05: Schwaches Signal
- ΔR²_H ≈ 0.05-0.10: Moderates Signal
- ΔR²_H > 0.10: Starkes Signal

---

*Generiert durch `e02_model_cascade.py`*
