# Catalan-EABC Bridge (defensive research note)

## Einordnung: drei Catalan-Bilder, ein Zaehlkern

Die Catalan-Zahlen tauchen in mehreren aequivalenten Bildern auf:

- **Formelbild:** klassische geschlossene Formen/rekursive Definitionen fuer `C_m`.
- **Pascal-Differenzbild:** Catalan als Diagonaldifferenzen in der Pascal-Struktur.
- **Triangulierungsbild:** Anzahl von Triangulierungen eines `(m+2)`-Ecks ist `C_m`.

Diese Bilder kodieren denselben kombinatorischen Kern "gleiche Groesse, viele gueltige Klammerungen".

## Bezug zu EABC/Hurwitz

In der EABC-Hurwitz-Sprache gilt fuer `n` mit Primfaktorzerlegung:

- `Omega_tot(n)` = Anzahl Primfaktoren mit Vielfachheit (inkl. `v2`, `v3`, `E`, `A`, `B`, `C`).
- Setze `k := Omega_tot(n)`.

Dann gibt es fuer die rekursive Multiplikationsrekonstruktion von `n` genau
`C_{k-1}` volle Binärbaeume bzw. vollstaendige Binärklammerungen derselben
`k` Faktorenliste (inkl. Wiederholungen als getrennte Blätter).

Wichtig: Das ist primaer ein **Kombinatorik-Statement** ueber Rekonstruktionspfade,
nicht automatisch ein neues strukturelles Theorem ueber EABC-Observablen.
Die fuenf Catalan-Klammerungen beschreiben verschiedene Rechenbaeume derselben
multiplikativen Synthese, nicht verschiedene Endobjekte.

## Methodische Trennung (defensiv)

### 1) Bewiesene Tatsachen

- Catalan-Zahlen zaehlen die Zahl gueltiger vollen Binaerbaeume/Klammerungen.
- Quaternionenmultiplikation (Hurwitz) ist assoziativ.
- Assoziativitaet impliziert identisches Endprodukt fuer alle Klammerungen derselben
  geordneten Faktorenliste.

### 2) Experimentelle Beobachtung

- Pfadabhaengigkeit betrifft Zwischenprodukte `q^(k)` und observables
  `||q^(k)||`, `H(q^(k))`, `kappa(q^(k))`.
- In der 4-Faktoren-Demo sind Endgroessen gleich, waehrend Zwischenverlaeufe
  (Trajektorien) zwischen Catalan-Pfaden differieren.

### 3) Offene Forschungsfrage

- Ob aus dieser Pfadabhaengigkeit neue arithmetische/geometrische Invarianten
  jenseits des Endprodukts entstehen, ist offen.
- Diese Beobachtung ist zunaechst Eigenschaft der gewaehlten
  Quaternion-Repraesentation; weitergehende arithmetische/physikalische
  Invarianten werden hier nicht behauptet.

## Forschungsfrage: Invarianz vs. Pfadabhaengigkeit

### RQ1: Klammerungsinvarianz von `H(n)`

Mit `H(n)=(E(n),A(n),B(n),C(n))` als additiver 4D-Komponente der
EABC-Hurwitz-Normalform ist die Leitfrage:

- bleibt `H(n)` unter allen Catalan-Klammerungen eines festen Faktormultisets invariant?

Arbeitshypothese: ja, weil die Komponenten additiv und damit assoziativ ueber der
Multiplikation aggregieren.

### RQ2: Klammerungsabhaengigkeit rekonstruktiver Geometrie

Parallel bleibt offen:

- koennen **rekonstruktive**, bauminduzierte Geometriegroessen (z. B. tiefegewichtete
  Aggregationen entlang interner Knoten) vom gewaehlten Catalan-Baum abhaengen?

Diese Groessen sind nicht notwendigerweise reine Endzustandsfunktionen von `n`,
sondern koennen den Rekonstruktionspfad kodieren.

## Defensive Interpretation

- Eine numerische Invarianzprobe fuer `H(n)` stuetzt primaer die erwartete
  Assoziativitaetsstruktur.
- Eine beobachtete Baumabhaengigkeit bei Toy-Observablen ist **kein**
  Widerspruch zu EABC-Additivitaet, sondern zeigt den Unterschied zwischen
  Endzustandsinvarianten und pfadcodierenden Konstruktionen.
- Es werden hier bewusst keine physikalischen oder mechanistischen Overclaims erhoben.

## Systematische 5-Pfade-Auswertung fuer 4 Faktoren

Die folgenden Pfade werden als Paarungs-Protokolle fuer vier geordnete Faktoren
`(q1,q2,q3,q4)` gelesen:

- `P1 = (((q1*q2)*q3)*q4)`
- `P2 = ((q1*(q2*q3))*q4)`
- `P3 = (q1*(q2*(q3*q4)))`
- `P4 = ((q1*q2)*(q3*q4))`
- `P5 = (q1*((q2*q3)*q4))`

### Beispielkonfiguration (explizit, reproduzierbar)

Wir verwenden eine defensive, rein algebraische Demo-Konfiguration:

- `q1`: Signatur `(1,0,0,0)`, `norm=2`, `kappa=1/2=0.5`
- `q2`: Signatur `(0,0,0,0)`, `norm=1`, `kappa=1`
- `q3`: Signatur `(0,1,0,0)`, `norm=3`, `kappa=1/3`
- `q4`: Signatur `(0,0,1,0)`, `norm=5`, `kappa=1/5`

Zwischenprodukte werden mit

- `H(x*y)=H(x)+H(y)` (komponentenweise) und
- `norm(x*y)=norm(x)*norm(y)`

ausgewertet. Damit haben alle Pfade denselben Endzustand:

- Endsignatur `H_end=(1,1,1,0)`
- Endnorm `norm_end=30`
- Endkruemmungsproxy `kappa_end ~= 1/30 ~= 0.0333`

### Beobachtung: Endinvarianten vs. Trajektorien

- **Invarianz:** Endsignatur und Endnorm bleiben ueber alle 5 Pfade identisch.
- **Pfadabhaengigkeit:** Die Folge der Zwischenknoten in
  Signatur-/Normraum (und damit `kappa`) unterscheidet sich je Pfad.
- **Sequentielle Pfade (z. B. `P1`):**
  stufenweiser Kruemmungstransfer `0.5 -> 0.1667 -> 0.0333`.
- **Pfad `P3`:** klare Aufspaltung in zwei Teilsysteme mit Normen `2` und `15`
  unmittelbar vor dem finalen Merge; der finale Knoten zeigt den synchronen
  Kollapseffekt beider Teilkruemmungen in denselben Endzustand.

Assoziativitaet impliziert identisches Endprodukt.
Diese Lesart ist konsistent mit der Trennung:

- Endzustandsinvarianten (`H_end`, `norm_end`) vs.
- pfadabhaengige Zwischengeometrie (z. B. `kappa`, rekonstruktive Radius-/Trajektoriengroessen).

### Forschungsfrage (praezisiert, defensiv)

`RQ-CAT-GEO`: Fuer fixes Faktormultiset mit `k=Omega_tot(n)` und
`C_{k-1}` topologisch erlaubten Binaerpfaden:

- Welche Groessen sind **streng endzustandsinvariant**
  (z. B. `H_end`, ggf. weitere additive Invarianten)?
- Welche abgeleiteten Groessen sind **potenziell pfadabhaengig**
  (`kappa`-Verlauf, `r_core`, `r_edge`, weitere bauminduzierte Funktionale)?

Status:

- Die obige 5-Pfade-Tabelle ist numerische Evidenz/Illustration.
- Sie ersetzt keinen formalen Vollbeweis ueber alle moeglichen Observablenklassen.

### Catalan-Zaehlkern

Die Catalan-Zahl `C_{Omega_tot(n)-1}` quantifiziert die Zahl topologisch
zulaessiger Metrikpfade waehrend multiplikativer Synthese bei fixer Faktorenliste.
Damit ist die Kerntrennung:

- gleiche Endinvarianten moeglich, aber
- unterschiedliche Zwischengeometrie je Pfad.
- Die fuenf Catalan-Klammerungen beschreiben verschiedene Rechenbaeume
  derselben multiplikativen Synthese, nicht verschiedene Endobjekte.
