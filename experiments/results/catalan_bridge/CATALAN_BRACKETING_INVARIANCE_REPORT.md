# Catalan Bracketing Invariance Probe (EABC/Hurwitz)

## Ziel

- Pruefen, ob `H(n)=(E,A,B,C)` gegen Catalan-Klammerung invariant bleibt.
- Parallel eine explizit nicht-kanonische Toy-Observable auswerten,
  die baumabhaengige Rekonstruktionspfade sichtbar machen kann.

## Methodik (defensiv)

- Fuer jedes `n` mit `Omega_tot(n)=k` gibt es theoretisch `C_{k-1}` Klammerungen.
- Bei moderatem `C_{k-1}`: exhaustive Auswertung aller vollen Binaerbaeume.
- Bei grossem `C_{k-1}`: deterministische Stichprobe (`sampled`) als Machbarkeitsmodus.
- `H(n)` wird rein additiv ueber Blattbeitraege aggregiert.
- Toy-Observable: Summe lokaler Balancing-Kosten `|log(L)-log(R)|` ueber innere Knoten.

## Ergebnisueberblick

- Globales Invarianzresultat fuer `H(n)`: `ja`.
- Sichtbare Baumabhaengigkeit der Toy-Observable: `ja`.
- Exhaustive Faelle: `8`, sampled Faelle: `0`.

## Detail je n

- `n=60`, `k=4`, `C_(k-1)=5`, mode=`exhaustive`, trees=`5`, `H`-invariant=`ja`, toy-range=`4.070628`, toy-distinct=`5`.
- `n=72`, `k=5`, `C_(k-1)=14`, mode=`exhaustive`, trees=`14`, `H`-invariant=`ja`, toy-range=`5.780744`, toy-distinct=`12`.
- `n=84`, `k=4`, `C_(k-1)=5`, mode=`exhaustive`, trees=`5`, `H`-invariant=`ja`, toy-range=`5.416517`, toy-distinct=`5`.
- `n=90`, `k=4`, `C_(k-1)=5`, mode=`exhaustive`, trees=`5`, `H`-invariant=`ja`, toy-range=`3.401197`, toy-distinct=`5`.
- `n=120`, `k=5`, `C_(k-1)=14`, mode=`exhaustive`, trees=`14`, `H`-invariant=`ja`, toy-range=`6.802395`, toy-distinct=`12`.
- `n=180`, `k=5`, `C_(k-1)=14`, mode=`exhaustive`, trees=`14`, `H`-invariant=`ja`, toy-range=`8.018790`, toy-distinct=`14`.
- `n=210`, `k=4`, `C_(k-1)=5`, mode=`exhaustive`, trees=`5`, `H`-invariant=`ja`, toy-range=`4.710947`, toy-distinct=`5`.
- `n=360`, `k=6`, `C_(k-1)=42`, mode=`exhaustive`, trees=`42`, `H`-invariant=`ja`, toy-range=`11.748492`, toy-distinct=`37`.

## Einordnung

- Das positive Invarianzresultat fuer `H(n)` ist konsistent mit Additivitaet/Assoziativitaet,
  aber als numerische Probe kein formaler Vollbeweis.
- Die Toy-Observable dient nur als Demonstrator fuer rekonstruktionspfadabhaengige Groessen,
  nicht als kanonische EABC- oder Hurwitz-Metrik.

## Artefakte

- `experiments/results/catalan_bridge/catalan_bracketing_invariance.csv`
- `experiments/results/catalan_bridge/CATALAN_BRACKETING_INVARIANCE_REPORT.md`
- `experiments/results/catalan_bridge/catalan_bracketing_invariance.png` (optional)

Plot erzeugt: `ja`
