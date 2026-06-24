# E02 Zusatztest: Kanonisierungs-Stabilität

## Zielsetzung

Teste, ob das ΔR²_H-Signal robust über verschiedene Kanonisierungen n → T(n) ist.

Falls ΔR²_H stark variiert, wäre das Signal ein Kanonisierungs-Artefakt.

---

## Ergebnisse

| Kanonisierung | R²(M2) | R²(M3*) | ΔR²_H |
|---------------|--------|---------|-------|
| left          | 1.0000 | 1.0000 | 0.0000 |
| right         | 1.0000 | 1.0000 | 0.0000 |
| balanced      | 0.7502 | 0.9670 | 0.2168 |

**Mittelwert ΔR²_H:** 0.0723

**Standardabweichung:** 0.1022

**Variationskoeffizient:** 1.41

---

## Korrelationen zwischen M_C

| Vergleich | Korrelation |
|-----------|-------------|
| Left ↔ Right | 1.0000 |
| Left ↔ Balanced | 0.4656 |
| Right ↔ Balanced | 0.4656 |

---

## Interpretation

⚠️ **INSTABIL**: Das ΔR²_H-Signal variiert stark zwischen Kanonisierungen.

**Konsequenz:** Die Erklärungskraft von H(n) könnte ein Kanonisierungs-Artefakt sein.

**H0 (Existenz kanonischer Abbildung):** Verletzt - weitere Tests erforderlich.

---

*Generiert durch `e02_canonization_stability.py`*
