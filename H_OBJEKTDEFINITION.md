# H(Δr): The Projection-Invariant Arithmetic Observable

**Status**: ✅ **Extrahiert und validiert** (June 23, 2026)  
**Domain**: Δr ∈ {2, 6, 10, 14, 18}  
**Quality**: Mean CV = 18.8%, ρ = 0.965  

---

## Definition

Für den Bereich **Δr ≤ 18** existiert ein **projektionsinvariantes Objekt**:

```
H(Δr) = 1/4 · ∑_i A_i(Δr)
```

wobei die vier Projektionen A_i durch unterschiedliche Gap-Pair-Basis-Offsets definiert sind:
- A_2: {2,4,6} vs {2+Δr, 4+Δr, 6+Δr}
- A_4: {4,6,8} vs {4+Δr, 6+Δr, 8+Δr}
- A_6: {6,8,10} vs {6+Δr, 8+Δr, 10+Δr}
- A_8: {8,10,12} vs {8+Δr, 10+Δr, 12+Δr}

---

## Die Werte von H(Δr)

| Δr | H(Δr) | σ_H   | CV_H(%) | Interpretation |
|----|-------|-------|---------|----------------|
| 2  | 0.834 | 0.139 | 16.6    | Twin-Prime-Enhancement |
| 6  | 0.540 | 0.094 | 17.3    | Strong Short-Gap-Bias |
| 10 | 0.422 | 0.081 | 19.2    | Moderate Short-Gap-Bias |
| 14 | 0.329 | 0.081 | 24.6    | Weak Enhancement |
| 18 | 0.241 | 0.040 | 16.4    | Suppression |

**Mean CV_H = 18.8%** → Projektionsinvariant ✓

---

## Eigenschaften

### 1. Monotonie
```
H(2) > H(6) > H(10) > H(14) > H(18)
```
Streng monoton fallend.

### 2. Dynamischer Bereich
```
H(2) / H(18) = 3.45
```
Starke Δr-Abhängigkeit über den gesamten Bereich.

### 3. Twin-Prime-Enhancement
```
H(2) = 0.834
```
Deutlich über allen anderen Werten → Signatur der Twin-Prime-Anomalie.

### 4. Projektionsinvarianz
```
Mean CV_H = 18.8% < 20%
ρ(A_i, A_j) = 0.965 für alle Paare (i,j)
```

---

## Dekomposition: A_i(Δr) = c_i · H(Δr) + ε_i(Δr)

### Projektionskoeffizienten

| Base | c_i   | Interpretation |
|------|-------|----------------|
| 2    | 0.937 | Leicht unter Durchschnitt |
| 4    | 0.889 | Niedrigste Amplifikation |
| 6    | 0.930 | Nahe Durchschnitt |
| 8    | 1.244 | Höchste Amplifikation |

**Mean**: 1.000  
**Std**: 0.164  
**CV**: 16.4%

Die Projektionsoperatoren haben die **einfachste mögliche Form**:
```
P_i: H(Δr) ↦ c_i · H(Δr)
```
Reine Skalierung, keine Δr-abhängige Verzerrung.

### Dekompositionsqualität

| Base | Korrelation | Rel. Fehler | Qualität |
|------|-------------|-------------|----------|
| 2    | ρ = 0.987   | 11.1%      | Gut      |
| 4    | ρ = 0.996   | 5.1%       | Exzellent |
| 6    | ρ = 0.969   | 10.2%      | Gut      |
| 8    | ρ = 0.995   | 4.4%       | Exzellent |

**Alle Projektionen werden gut approximiert durch c_i · H(Δr).**

### Residuen

| Δr | ε_2    | ε_4    | ε_6    | ε_8    | Max |ε| |
|----|--------|--------|--------|--------|---------|
| 2  |  0.152 |  0.030 | -0.107 | -0.075 | 0.152   |
| 6  | -0.025 |  0.015 |  0.002 |  0.008 | 0.025   |
| 10 | -0.032 | -0.025 |  0.059 | -0.002 | 0.059   |
| 14 |  0.018 | -0.023 | -0.030 |  0.035 | 0.035   |
| 18 | -0.027 |  0.015 |  0.018 | -0.006 | 0.027   |

**Mean max |ε| = 0.060** (klein!)  
**Max max |ε| = 0.152** (bei Δr=2, höchster Wert)

---

## Regime II: Δr ≥ 20 (Outlier)

Für **Δr ≥ 20** existiert **kein projektionsinvariantes H(Δr)**:

| Δr | Mean | Std   | CV(%)  | Status |
|----|------|-------|--------|--------|
| 22 | 0.444 | 0.443 | 99.6   | ✗ Projektionssensitiv |
| 24 | 0.807 | 0.884 | 109.6  | ✗ Projektionssensitiv |

**Interpretation**: Separater physikalischer Mechanismus für große Δr.

---

## Wissenschaftliche Aussage

### Die zentrale Entdeckung

**Für Δr ≤ 18** besitzt die arithmetische Verstärkung A(Δr) eine **projektionsrobuste Kernstruktur H(Δr)**.

Die vollständige Dekomposition lautet:

```
R_Prime(Δr) = R_Bernoulli(Δr) · A_i(Δr)
        = R_Bernoulli(Δr) · [c_i · H(Δr) + ε_i(Δr)]
```

mit:
- **R_Bernoulli(Δr) = (1-p)^(-Δr)**: Geometrische Baseline
- **H(Δr)**: Projektionsinvariante arithmetische Kernstruktur
- **c_i**: Projektionsskalierung (CV = 16.4%)
- **ε_i(Δr)**: Kleine Residuen (< 0.06 mean)

### Physikalische Interpretation

**Regime I (Δr ≤ 18)**:
- Mechanismus: **Sieb-Effekte + Hardy-Littlewood-Korrelationen**
- Eigenschaften: Projektionsinvariant, monoton fallend, Twin-Prime-Peak
- Gap-Pair-Wahl: Spielt geringe Rolle (nur Skalierungsfaktor)

**Regime II (Δr ≥ 20)**:
- Mechanismus: **Unbekannt** (möglicherweise log(p)-Effekte oder Sparsity)
- Eigenschaften: Projektionssensitiv, keine gemeinsame Struktur
- Gap-Pair-Wahl: Beeinflusst Messung stark

**Kritische Grenze**: Δr ≈ 18-20

---

## Stage 4 Status

**Projektionsinvarianz**:

✅ **PASSED (restricted domain)**

| Kriterium | Status | Wert |
|-----------|--------|------|
| Korrelation | ✓ | ρ = 0.965 |
| Variation | ✓ | CV_H = 18.8% |
| Dekomposition | ✓ | ρ > 0.96, Fehler < 12% |
| Domain | ! | Eingeschränkt auf Δr ≤ 18 |

**Objektstatus von H(Δr)**:

```
✓ Stage 1: Existenz
✓ Stage 2: Reproduzierbarkeit
✓ Stage 3: Modellunabhängigkeit
✓ Stage 4: Projektionsinvarianz (Δr ≤ 18)
? Stage 5: Theoretische Anbindung (Hardy-Littlewood)
? Stage 6: Autonomie
```

---

## Nächste Schritte

### A. Stage 5 (Theoretische Anbindung)

**Ziel**: Hardy-Littlewood-Verbindung herstellen

1. **Ableiten**: H_theory(Δr) aus Singulär-Serien
2. **Vergleichen**: H_observed vs. H_theory
3. **Quantifizieren**: Abweichung und Interpretation

**Hypothese**:
```
H(Δr) ∝ weighted sum of HL constants for gaps in range Δr
```

### B. Validierung (Empirisch)

1. **Andere Moduli**: Teste H(Δr) für Modulo 30, 60, 210
2. **Höhere Präzision**: N = 10^6, mehr Seeds für Fehlerbalken
3. **Vollständiger Δr-Scan**: 2, 4, 6, 8, ..., 18 (nicht nur 2, 6, 10, 14, 18)

### C. Regime II (Separates Projekt)

1. **Mechanismus**: Untersuche Δr ≥ 20 separat
2. **log(p)-Hypothese**: Teste ob logarithmische Effekte dominieren
3. **Sparsity-Analyse**: Gap-Distribution wird dünn

---

## Dateien

### Daten
- `H_delta_r.txt` - Extrahierte Werte mit Fehlerbalken
- `H_complete_analysis.txt` - Vollständige Statistik

### Code
- `extract_H.py` - Extraktion und Visualisierung
- `compute_H_complete.py` - Vollständige Analyse

### LaTeX
- `H_table_latex.tex` - Publikationsfertige Tabellen

### Dokumentation
- `H_EXTRACTION.md` - Detaillierte Dokumentation
- `H_OBJEKTDEFINITION.md` - Diese Datei

---

## Zusammenfassung

**H(Δr) ist ein wohldefiniertes, projektionsinvariantes mathematisches Objekt**, das die intrinsische arithmetische Verstärkung von Gap-Asymmetrien für **short-to-medium range** (Δr ≤ 18) charakterisiert.

**Es hat Stage 4 der Objektwerdung bestanden** (eingeschränkte Domäne).

**Die nächste Herausforderung ist Stage 5**: Theoretische Anbindung an Hardy-Littlewood-Konstanten.
