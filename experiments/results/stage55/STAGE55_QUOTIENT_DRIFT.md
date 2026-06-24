# Stage 5.5 Quotient-Drift Analyse

## Datenbasis

- Verwendete Runs: `N=1,000,000`, `N=10,000,000`, `N=20,000,000`
- Delta-r Klassen: `2`, `6`, `10`, `14`, `18`
- Quelle: bestehende Stage-5.5-Artefakte (`wheel30_test` Output).

## Kernbefund (defensiv)

- In allen ausgewerteten Skalen gilt konsistent: `H_prime > H_wheel_cramer` und `H_prime > H_wheel_random` fuer alle getesteten Delta-r.
- Der Quotient `Q_cramer = H_prime / H_wheel_cramer` steigt in jeder Skala monoton mit Delta-r (in den vorliegenden Punkten).

## Monotone Drift-Tests pro Skala

| N | Spearman(Delta r, DeltaH_cramer) | p | Spearman(Delta r, Q_cramer) | p | slope DeltaH_cramer | R^2 | slope Q_cramer | R^2 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1,000,000 | 1.000 | 1.4e-24 | 1.000 | 1.4e-24 | 0.1515 | 0.944 | 0.0668 | 0.988 |
| 10,000,000 | 1.000 | 1.4e-24 | 1.000 | 1.4e-24 | 0.0976 | 0.960 | 0.0496 | 0.990 |
| 20,000,000 | 1.000 | 1.4e-24 | 1.000 | 1.4e-24 | 0.0869 | 0.962 | 0.0456 | 0.989 |

## Gepoolte (deskriptive) Drift

- Spearman(Delta r, DeltaH_cramer) = `0.971` (p=`1.83e-09`), lineare slope = `0.1120`, R^2=`0.835`.
- Spearman(Delta r, Q_cramer) = `0.960` (p=`1.43e-08`), lineare slope = `0.0540`, R^2=`0.914`.

## HL-bezogene Heuristik (vorsichtige Einordnung)

- Verfuegbare Proxies aus `reproducibility_stage6_N1M.txt`: `H_k3`, `H_k4` (als einfache Korrektur-Kandidaten).
- Bewertet wurde, ob ein lineares Modell fuer `DeltaH_cramer` die Intercept-only-Baseline verbessert.

| N | k3 R2-Gewinn | k4 R2-Gewinn | Einordnung |
|---:|---:|---:|---|
| 1,000,000 | 0.858 | 0.849 | Proxy erklaert Teilvarianz (vorsichtig) |
| 10,000,000 | 0.886 | 0.875 | Proxy erklaert Teilvarianz (vorsichtig) |
| 20,000,000 | 0.891 | 0.880 | Proxy erklaert Teilvarianz (vorsichtig) |

- Einschraenkung: sehr kleine Stichprobe pro Skala (nur 5 Delta-r Punkte), daher nur als Interface/Screening zu interpretieren.

## Reproduzierbarkeit

- Tabelle: `experiments/results/stage55/stage55_quotient_table.csv`
- Plot: `experiments/results/stage55/stage55_quotient_plots.png`
- Skript: `code/experiments/stage55_quotient_drift.py`

## Methodische Hinweise

- Statistik ist bewusst defensiv: Spearman (monotone Drift) + lineare Trends nur deskriptiv.
- Keine starke kausale HL-Behauptung aus den Proxy-Fits.
- Fuer publizierbaren naechsten Test: gleiche Pipeline auf `N=1e8`/`N=1e9` plus explizites HL-k-Tupel-Modell mit klarer Likelihood/Fit-Guete.
