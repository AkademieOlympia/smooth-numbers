# Stage 5.5 Wheel-30 Test - Quick Start

## Was das Skript macht

Das Python-Skript `stage5_5_wheel30_test.py` führt den entscheidenden Test durch, ob H(Δr) primzahlspezifisch oder eine Wheel-30-Eigenschaft ist.

**Es vergleicht**:
1. **H_Prime**: Echte Primzahlen
2. **H_WheelRandom**: Zufällige Ausdünnung von Wheel-30-Zahlen
3. **H_WheelCramér**: Cramér-Dichte auf Wheel-30 beschränkt

**Verwendet exakt dieselbe Pipeline** wie die bisherigen Tests:
```
Sequence → Gaps → Gap-Pairs → A_i(Δr) → H(Δr)
```

## Voraussetzungen

```bash
pip install numpy matplotlib scipy
```

(scipy ist optional, aber empfohlen für erweiterte Statistik)

## Verwendung

### Standard-Run (N=1,000,000, 10 Seeds)

```bash
python3 stage5_5_wheel30_test.py
```

**Laufzeit**: ~2-5 Minuten (je nach Rechner)

### Parameter anpassen

Öffne das Skript und ändere die Konfiguration am Anfang:

```python
N = 1_000_000          # Range (höher = genauer, aber langsamer)
NUM_SEEDS = 10         # Anzahl Random-Realisationen (höher = stabiler)
DELTA_R_VALUES = [2, 6, 10, 14, 18]  # Regime I Werte
PROJECTIONS = [2, 4, 6, 8]           # Base offsets
```

### Schneller Test (zum Debuggen)

```python
N = 100_000
NUM_SEEDS = 3
```

### Produktions-Run (höhere Genauigkeit)

```python
N = 5_000_000
NUM_SEEDS = 20
```

## Output

Das Skript erzeugt:

### 1. Terminal-Output

```
==================================================================
RESULTS: H(Δr) COMPARISON
==================================================================

Δr       H_Prime      H_WheelRand  H_WheelCramér
------------------------------------------------
2        0.8340       0.8215       0.8187
6        0.5400       0.5312       0.5298
10       0.4220       0.4156       0.4142
14       0.3290       0.3245       0.3231
18       0.2410       0.2378       0.2365

==================================================================
STATISTICAL COMPARISON
==================================================================
Correlation H_Prime vs H_WheelRandom:  ρ = 0.9987
Correlation H_Prime vs H_WheelCramér:  ρ = 0.9992

Mean absolute difference (Prime vs WheelRandom): 0.0085
Mean absolute difference (Prime vs WheelCramér): 0.0091

==================================================================
INTERPRETATION
==================================================================

⚠️  HIGH CORRELATION DETECTED

Result: H_Prime ≈ H_Wheel

Interpretation:
  H(Δr) appears to be primarily a property of Wheel-30 arithmetic
  rather than a prime-specific phenomenon.
```

### 2. Visualisierung

`stage5_5_wheel30_comparison.png` mit:
- **Links**: H(Δr) Verlauf für alle drei Modelle
- **Rechts**: Scatter-Plot H_Prime vs. H_Wheel

## Interpretation der Ergebnisse

### Hohe Korrelation (ρ > 0.9)

**H_Prime ≈ H_Wheel**

→ H(Δr) ist primär eine Wheel-30-Eigenschaft  
→ Nicht primzahlspezifisch im engeren Sinne  
→ Modulo-Arithmetik-Interpretation

**Paper-Framing**: "Wheel-30 residue-class property"

### Niedrige Korrelation (ρ < 0.3)

**H_Prime ≠ H_Wheel**

→ H(Δr) enthält primzahlspezifische Information  
→ Nach Elimination von Wheel bleibt Signal übrig  
→ HL k-tuple Tests (k≥3) motiviert

**Paper-Framing**: "Prime-specific residual signal"

### Mittlere Korrelation (0.3 < ρ < 0.9)

**Ambiguous**

→ Mischung aus Wheel + Prime?  
→ N erhöhen für bessere Statistik  
→ Detailliertere Analyse nötig

## Troubleshooting

### "All H values are NaN"

**Problem**: Zu wenige Gap-Pairs gefunden  
**Lösung**: N erhöhen (z.B. N = 5_000_000)

### "Zu langsam"

**Problem**: N zu groß oder zu viele Seeds  
**Lösung**: 
- N reduzieren auf 500_000
- NUM_SEEDS reduzieren auf 5

### "Memory Error"

**Problem**: N zu groß für RAM  
**Lösung**: 
- N schrittweise reduzieren
- Oder: Chunking implementieren (Skript anpassen)

## Nächste Schritte nach dem Test

### Falls H_Prime ≈ H_Wheel

1. Paper umschreiben: "Wheel-30 property"
2. Modulo-arithmetische Interpretation
3. Keine HL k≥3 Tests nötig
4. **Publikation möglich** (mit korrekter Framing)

### Falls H_Prime ≠ H_Wheel

1. Paper stärken: "Prime-specific after Wheel elimination"
2. HL k-tuple Tests (k=3,4,5)
3. Residue-class-specific HL
4. **Publikation stärker** (primzahltheoretisch)

## Datei-Struktur nach Ausführung

```
smooth-numbers/
├── stage5_5_wheel30_test.py           ← Das Skript
├── stage5_5_wheel30_comparison.png    ← Visualisierung (generiert)
└── STAGE5.5_RESULTS.txt               ← Optional: Output umleiten
```

## Output umleiten

```bash
python3 stage5_5_wheel30_test.py | tee STAGE5.5_RESULTS.txt
```

Speichert Terminal-Output in Datei für spätere Analyse.

## Performance-Hinweise

**Typische Laufzeiten** (MacBook Pro, M1):

- N = 100,000, Seeds = 3:    ~20 Sekunden
- N = 1,000,000, Seeds = 10:  ~2-3 Minuten
- N = 5,000,000, Seeds = 20:  ~15-20 Minuten

**Hauptflaschenhals**: Bernoulli-Baseline-Berechnung (100 Trials)

**Optimierung**: Baseline cachen (einmal berechnen, speichern, wiederverwenden)

## Kontakt

Bei Problemen oder Fragen: Siehe `PROJECT_FINAL_STATUS.md` für Kontext.

---

**Stage 5.5 ist der letzte kritische Test vor Publikation.**

**Beide Ergebnisse sind wissenschaftlich wertvoll.**
