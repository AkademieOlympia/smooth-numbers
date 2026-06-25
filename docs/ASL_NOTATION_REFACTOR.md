# ASL Notation Refactor (alt -> neu)

Ziel dieses Mappings ist eine langfristig konsistente, reviewer-defensive Schreibweise ohne Overclaims.

## 1) Kernobjekte

- Alt: `Phi_ASL = (v2,v3;E,A,B,C;Gamma)`
- Neu: `Phi_ASL^(K) = (Phi, Gamma_K)`

- Alt: impliziter Kern in der ASL-Schreibweise
- Neu: expliziter additiver Kern
  - `(N,*)` mit neutralem Element `1`
  - `(N_0^6,+)` mit neutralem Element `0`
  - `Phi = (v2,v3;E,A,B,C)`
  - `Phi:(N,*)->(N_0^6,+)` ist Monoid-Homomorphismus (aus eindeutiger Primfaktorzerlegung)
  - `Phi_G = (Phi, Gamma_{Q(i)})`
  - `Phi_ASL^(K) = (Phi, Gamma_K)`

## 2) Hierarchie

- Neu explizit: `Phi subset Phi_G subset Phi_ASL^(K)`.
- Interpretation: Die Additivitaet liegt auf `Phi`; `Gamma`-Schichten sind Verfeinerungen.
- Praezisierung: `Gamma_K` ist eine family of splitting layers indexed by number field `K` (kein Funktor-Claim ohne kategoriale Infrastruktur).

## 3) Quaternionen-Terminologie

- Alt: "Quaternionenprojektion" / "Hurwitz-Projektion"
- Neu: "quaternionische Einbettung der additiven EABC-Signatur"

Formell:

- `iota: N_0^4 -> H`
- `iota(E,A,B,C)=E+Ai+Bj+Ck`
- `q(n)=iota(H(n))`

Defensive Klarstellung:

- Kein Multiplikationsclaim auf Quaternionenseite, solange keine kompatible Ziel-Multiplikation explizit definiert und verwendet wird.

## 4) ASL-Terminologie

- Bevorzugt: **Arithmetic Splitting Layer (ASL)**.
- Grund: Der Name beschreibt die arithmetische Splitting-Rolle von `Gamma_K` explizit.
- Alias-Hinweis: fruehere Bezeichnungen koennen als historische Alias-Notiz erhalten bleiben, sind aber nicht mehr Leitterminus.

## 5) Vier Ebenen (I-IV)

I. `Phi:(N,*)->(N_0^6,+)` als Monoid-Homomorphismus.  
II. `iota: N_0^4 -> H` mit `iota(E,A,B,C)=E+Ai+Bj+Ck` als additive Einbettung.  
III. `Gamma_K` als family of splitting layers indexed by number field `K`.  
IV. `Phi_ASL^(K)=(Phi,Gamma_K)` als integrierte Normalform.

Kompositionssicht:

- `N --Phi--> N_0^6 --pi4--> N_0^4 --iota--> H`
- `N --Gamma_K--> SplittingData(K)`

Integrationssicht:

- `Phi_ASL^(K)=(Phi,Gamma_K)`

## 6) Neuheitsrahmen

- Bekannt (klassisch): `AE` split / `BC` inert in `Z[i]`.
- Projektneu (begrenzt): additive Basissprache `Phi` plus modulare Schichtenarchitektur `Gamma_K`.
- Kein Overclaim: Neuheit betrifft Darstellung/Architektur, nicht den klassischen Split/Inert-Satz selbst.

## 7) Verweis auf finale Kovariatenhierarchie

- Offizielle Endfassung fuer die dynamische Regressionsfamilie: `M0..M4` mit
  `eta_i = (M_pert/M_i) * (a_i/x)^3` und
  `dot_varpi_i = c0 + c1*eta_i + c2*g(Phi_i) + c3*eta_i*g(Phi_i) + c4*H_i`.
- Hierarchie: `M0: c0`, `M1: c0 + c1*eta_i`, `M2: M1 + c2*g(Phi_i)`,
  `M3: M2 + c3*eta_i*g(Phi_i)`, `M4: M3 + c4*H_i`.
- Defensive Leitplanke: EABC/ASL wird nicht als neue Kraft eingefuehrt, sondern als
  diskrete Kovariate gegen klassische Tidenkopplung und Siebgroessen getestet.

## 8) Verweis auf Catalan-EABC-Bruecke

- Fuer die Frage "gleiche Zahl, viele Klammerungen" ist die kanonische Notiz:
  `docs/CATALAN_EABC_BRIDGE.md`.
- Neu ergaenzt: systematische 5-Pfade-Auswertung fuer 4 Faktoren mit expliziten
  Zwischenprodukten (`H`-Signatur, `norm`, `kappa`) als defensive Bruecke zwischen
  Endinvarianz und pfadabhaengiger Zwischengeometrie.
- Methodischer Kern dort explizit:
  - bewiesen: Catalan zaehlt Klammerungen/Baeume und Assoziativitaet sichert identisches Endprodukt,
  - beobachtet: Pfadabhaengigkeit nur in Zwischenprodukten/Trajektorien,
  - offen: moegliche neue Invarianten jenseits des Endprodukts.
- Dort wird getrennt zwischen
  - klammerungsinvarianten Endzustandsgroessen (insb. `H(n)` als additive 4D-Komponente) und
  - potenziell klammerungsabhaengigen rekonstruktiven Baum-Observablen.
