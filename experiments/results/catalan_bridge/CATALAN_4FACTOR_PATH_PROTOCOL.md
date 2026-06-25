# Catalan 4-Factor Path Protocol

Defensive Demo-Auswertung fuer 4 Faktoren und 5 Catalan-Klammerungen.
Die Auswertung ist rein algebraisch (`H` additiv, `norm` multiplikativ).

## Demo-Faktoren

- `q1`: `H=(1,0,0,0)`, `norm=2`, `kappa=0.5`
- `q2`: `H=(0,0,0,0)`, `norm=1`, `kappa=1`
- `q3`: `H=(0,1,0,0)`, `norm=3`, `kappa=0.333333`
- `q4`: `H=(0,0,1,0)`, `norm=5`, `kappa=0.2`

Endzustand fuer alle Pfade:
- `H_end=(1,1,1,0)`
- `norm_end=30`
- `kappa_end=0.033333`

## Pfadprotokolle

### P1: `(((q1*q2)*q3)*q4)`

- Schritt 1: `(q1*q2)` -> `H=(1, 0, 0, 0)`, `norm=2.000000`, `kappa=0.500000`
- Schritt 2: `((q1*q2)*q3)` -> `H=(1, 1, 0, 0)`, `norm=6.000000`, `kappa=0.166667`
- Schritt 3: `(((q1*q2)*q3)*q4)` -> `H=(1, 1, 1, 0)`, `norm=30.000000`, `kappa=0.033333`
- Pfadsequenz `norm`: `2.000000, 6.000000, 30.000000`
- Pfadsequenz `kappa`: `0.500000, 0.166667, 0.033333`
- Endcheck: `H_end=(1, 1, 1, 0)`, `norm_end=30.000000`, `kappa_end=0.033333`

### P2: `((q1*(q2*q3))*q4)`

- Schritt 1: `(q2*q3)` -> `H=(0, 1, 0, 0)`, `norm=3.000000`, `kappa=0.333333`
- Schritt 2: `(q1*(q2*q3))` -> `H=(1, 1, 0, 0)`, `norm=6.000000`, `kappa=0.166667`
- Schritt 3: `((q1*(q2*q3))*q4)` -> `H=(1, 1, 1, 0)`, `norm=30.000000`, `kappa=0.033333`
- Pfadsequenz `norm`: `3.000000, 6.000000, 30.000000`
- Pfadsequenz `kappa`: `0.333333, 0.166667, 0.033333`
- Endcheck: `H_end=(1, 1, 1, 0)`, `norm_end=30.000000`, `kappa_end=0.033333`

### P3: `(q1*(q2*(q3*q4)))`

- Schritt 1: `(q3*q4)` -> `H=(0, 1, 1, 0)`, `norm=15.000000`, `kappa=0.066667`
- Schritt 2: `(q2*(q3*q4))` -> `H=(0, 1, 1, 0)`, `norm=15.000000`, `kappa=0.066667`
- Schritt 3: `(q1*(q2*(q3*q4)))` -> `H=(1, 1, 1, 0)`, `norm=30.000000`, `kappa=0.033333`
- Pfadsequenz `norm`: `15.000000, 15.000000, 30.000000`
- Pfadsequenz `kappa`: `0.066667, 0.066667, 0.033333`
- Hinweis P3: vor dem letzten Merge liegen Teilsysteme mit `norm=2` und `norm=15` vor.
- Endcheck: `H_end=(1, 1, 1, 0)`, `norm_end=30.000000`, `kappa_end=0.033333`

### P4: `((q1*q2)*(q3*q4))`

- Schritt 1: `(q1*q2)` -> `H=(1, 0, 0, 0)`, `norm=2.000000`, `kappa=0.500000`
- Schritt 2: `(q3*q4)` -> `H=(0, 1, 1, 0)`, `norm=15.000000`, `kappa=0.066667`
- Schritt 3: `((q1*q2)*(q3*q4))` -> `H=(1, 1, 1, 0)`, `norm=30.000000`, `kappa=0.033333`
- Pfadsequenz `norm`: `2.000000, 15.000000, 30.000000`
- Pfadsequenz `kappa`: `0.500000, 0.066667, 0.033333`
- Endcheck: `H_end=(1, 1, 1, 0)`, `norm_end=30.000000`, `kappa_end=0.033333`

### P5: `(q1*((q2*q3)*q4))`

- Schritt 1: `(q2*q3)` -> `H=(0, 1, 0, 0)`, `norm=3.000000`, `kappa=0.333333`
- Schritt 2: `((q2*q3)*q4)` -> `H=(0, 1, 1, 0)`, `norm=15.000000`, `kappa=0.066667`
- Schritt 3: `(q1*((q2*q3)*q4))` -> `H=(1, 1, 1, 0)`, `norm=30.000000`, `kappa=0.033333`
- Pfadsequenz `norm`: `3.000000, 15.000000, 30.000000`
- Pfadsequenz `kappa`: `0.333333, 0.066667, 0.033333`
- Endcheck: `H_end=(1, 1, 1, 0)`, `norm_end=30.000000`, `kappa_end=0.033333`

## Defensiver Befund

- Die fuenf Catalan-Klammerungen beschreiben verschiedene Rechenbaeume derselben multiplikativen Synthese, nicht verschiedene Endobjekte.
- Assoziativitaet impliziert identisches Endprodukt.
- Endsignatur/-norm sind in dieser Demo klammerungsinvariant.
- Zwischenverlaeufe der Geometrieproxies (`norm`, `kappa`) sind pfadabhaengig.
- Pfadabhaengigkeit betrifft Zwischenprodukte `q^(k)` und observables `||q^(k)||`, `H(q^(k))`, `kappa(q^(k))`.
- Diese Beobachtung ist zunaechst Eigenschaft der gewaehlten Quaternion-Repraesentation; weitergehende arithmetische/physikalische Invarianten sind offen.
- Die Demo zeigt numerische Evidenz, aber keinen Vollbeweis fuer allgemeine Observable-Klassen.

## Artefakte

- `experiments/results/catalan_bridge/catalan_4factor_path_protocol.csv`
- `experiments/results/catalan_bridge/CATALAN_4FACTOR_PATH_PROTOCOL.md`
