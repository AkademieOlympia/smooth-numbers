# Stage 5.6 Method Brakes

## Datenbasis und Scope

- Verwendete Stage-5.5-Skalen: `N=1,000,000`, `N=10,000,000`, `N=20,000,000`
- Δr-Klassen: `2`, `6`, `10`, `14`, `18`
- Methodik defensiv: kleine Δr-Stichprobe (`n=5` je Skala), daher keine starken Extrapolationen.

## A) Quotienten-Skalierung `R(Δr)=H_prime/H_wheel_cramer`

- Modelle: linear `R=a+b·Δr` sowie Potenz (`a·Δr^alpha` oder `1+c·Δr^alpha`).
- Reported: Parameter ± Unsicherheit (SE), `R²`, `AIC`, `BIC`, Residuen.

| Skala | Modell | Parameter | R² | AIC | BIC |
|---|---|---|---:|---:|---:|
| 1000000 | linear | a=0.87900±0.04894, b=0.06681±0.00426 | 0.988 | -27.76 | -28.55 |
| 1000000 | power_one_plus | c=0.02218±0.00381, alpha=1.35751±0.06303 | 0.997 | -35.57 | -36.35 |
| 10000000 | linear | a=0.91839±0.03328, b=0.04963±0.00290 | 0.990 | -31.62 | -32.40 |
| 10000000 | power_one_plus | c=0.01926±0.00386, alpha=1.30488±0.07373 | 0.996 | -36.53 | -37.32 |
| 20000000 | linear | a=0.92699±0.03151, b=0.04564±0.00274 | 0.989 | -32.17 | -32.95 |
| 20000000 | power_one_plus | c=0.01812±0.00383, alpha=1.29787±0.07763 | 0.996 | -36.78 | -37.56 |
| pooled | linear | a=0.90812±0.05293, b=0.05403±0.00461 | 0.914 | -66.95 | -65.53 |
| pooled | power_one_plus | c=0.01981±0.00925, alpha=1.32405±0.17142 | 0.921 | -68.22 | -66.81 |

- Bewertungslogik: niedrigeres `AIC/BIC` ist besser; bei sehr kleinem `n` nur als robuste Tendenz lesen, nicht als harte Modellselektion.

## B) Wheel-210 Nulltest

- Wheel-210 Kontrollmodelle (`2·3·5·7`): `H_wheel210_random` und `H_wheel210_cramer` mit je `6`/`6` Seeds.
- Kenngroessen je Δr: `ΔH_210 = H_prime - H_wheel210_*`, `R_210 = H_prime / H_wheel210_*`.

| N | Modell | mean(R_210) ueber Δr | min(R_210) | max(R_210) |
|---:|---|---:|---:|---:|
| 1,000,000 | wheel210_random | 2.820 | 0.630 | 5.800 |
| 1,000,000 | wheel210_cramer | 3.075 | 0.636 | 6.723 |
| 10,000,000 | wheel210_random | 2.280 | 0.610 | 4.283 |
| 10,000,000 | wheel210_cramer | 2.419 | 0.611 | 4.681 |
| 20,000,000 | wheel210_random | 2.188 | 0.631 | 3.999 |
| 20,000,000 | wheel210_cramer | 2.292 | 0.611 | 4.347 |

- Defensiver Prüfpunkt: Falls `R_210` nahe `1` und deutlich kleiner als Stage-5.5-Quotienten wird, spricht das fuer starken mod-7-Anteil; bleibt `R_210` signifikant > 1, bleibt ein substanzieller Prime-vs-Control-Abstand.

## C) HL-nahe Referenzanalyse (defensiv)

- HL-nahe Proxies (`k3`, `k4`) aus bestehender Stage-6-Reprodatei wurden als Zusatzregressoren getestet.
- Zielvariable: `ΔH(Δr)=H_prime-H_wheel_cramer`; Baseline: `ΔH ~ 1 + Δr`.
- Vergleich: Proxy-augmentierte Modelle via `AIC`-Gewinn und `R²`-Gewinn.

| N | k3 AIC gain | k3 R² gain | k4 AIC gain | k4 R² gain |
|---:|---:|---:|---:|---:|
| 1,000,000 | -1.474 | 0.006 | -1.974 | 0.000 |
| 10,000,000 | -1.743 | 0.002 | -1.998 | 0.000 |
| 20,000,000 | -1.798 | 0.001 | -1.991 | 0.000 |

- Methodische Einschränkung: Proxies sind heuristisch und nicht skalenspezifisch rekalibriert; Ergebnis als Interface-Test, nicht als Theoriebeweis.

## Artefakte

- Skript: `code/experiments/stage56_method_brakes.py`
- Markdown: `experiments/results/stage56/STAGE56_METHOD_BRAKES.md`
- Summary-CSV: `experiments/results/stage56/stage56_summary_table.csv`
- Plots: `experiments/results/stage56/stage56_plots.png`
- Fit-Details (JSON): `experiments/results/stage56/stage56_fit_details.json`

## Reviewer-sichere Einordnung

- Keine Kausalclaims aus 5-Punkt-Δr-Reihen.
- Modellvergleiche nur als Konsistenz-/Robustheitschecks.
- Stage 6 sollte den naechsten publizierbaren Test auf echte HL-Singular-Series-Konstruktion mit klaren out-of-sample Kriterien fokussieren.
