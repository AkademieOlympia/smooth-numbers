# Kepler-Tupelachse v2 (formales Analogiemodell)

## Scope und Haltung

Dieses Dokument definiert die Kepler-Tupelachse als **rein formale** Geometrie auf admissiblen Offsetmengen.  
Die Kepler-Sprache ist nur eine Analogie fuer Form-/Skalenbeziehungen im Offsetraum; es gibt **keinen** physikalischen Orbit-Claim ueber Primzahlen.

## v2-Definition (robust)

Sei `O = {o_1, ..., o_k}` eine admissible Offsetform.

- Zentrum:
  - `c = (1/k) * sum_{i=1..k} o_i`
- Abstandsliste:
  - `d_i = |o_i - c|`
- Kernradius:
  - `r_core = min_{d_i>0} d_i`  (kleinster positiver Abstand)
- Randradius:
  - `r_edge = max_i d_i`
- Halbachse:
  - `a = (r_core + r_edge)/2`
- Tupel-Exzentrizitaet:
  - `e = (r_edge - r_core)/(r_edge + r_core)`
- Radiusverhaeltnis:
  - `R_v = r_edge/r_core`
- Perioden-Analogie:
  - `T = 2*pi*a^(3/2)`

### Degeneratbehandlung

- Einzelne zentrische Punkte (`d_i=0`) erzeugen **keine** Singularitaet.
- Nur wenn **alle** `d_i=0` gilt, wird der degenerierte Sonderfall explizit markiert.

## Warum nicht peri/apo als Primardefinition?

- Peri/Apo ist hier lediglich eine Sprachmetapher.
- Mit `r_peri = min_i d_i` entsteht bei zentrischen Punkten sofort `r_peri=0`, was zu instabilen Quotienten fuehrt.
- v2 trennt diese Faelle sauber: zentrale Punkte bleiben erlaubt, waehrend `r_core` immer positiv bleibt (ausser im echten Total-Degeneratfall).
- Damit sind `e` und `R_v` fuer regulaere Tupel robust und numerisch stabil.

## Signatur

Die v2-Signatur lautet:

- `kappa(T) = (r_core, r_edge, a, e, R_v, T)`

## Beispiele (Pflichtvalidierung)

- `(0,2)`:
  - `c=1`, `r_core=1`, `r_edge=1`, `e=0`
- `(0,2,6)`:
  - `c=8/3`, `r_core=2/3`, `r_edge=10/3`, `e=2/3`
- `(0,2,6,8)`:
  - `c=4`, `r_core=2`, `r_edge=4`, `e=1/3`
- `(0,4,6,10,12)`:
  - `c=6.4`
  - `r_core=0.4=2/5`
  - `r_edge=6.4=32/5`
  - `a=3.4=17/5`
  - `e=15/17 ≈ 0.8823529`
  - `R_v=16`

## Numerische Reproduktion

- Script:
  - `python3 code/experiments/kepler_tuple_axis_numeric.py`
- Artefakte:
  - `experiments/results/kepler/kepler_tuple_table.csv`
  - `experiments/results/kepler/kepler_tuple_eabc_families.csv`
  - `experiments/results/kepler/kepler_tuple_plots.png`
  - `experiments/results/kepler/KEPLER_TUPLE_NUMERIC_REPORT.md`
