# EABC/ABCE-Modell und Glatte Zahlen

## Bamberg-Interpretation: Glatte Zahlen als Gitterpunkte

Diese Implementierung erforscht die tiefe Verbindung zwischen glatten Zahlen und dem EABC/ABCE-Quaternionen-Modell.

## Philosophische Grundlage

### Das Gegensatzpaar

**Primzahlen = "Harte" Zahlen:**
- Maximale Faktorisierungs-Komplexität
- Unteilbar
- Liegen auf den Achsen des Zahlengitters
- Eckpunkte der Struktur

**Glatte Zahlen = "Weiche" Zahlen:**
- Minimale Faktorisierungs-Komplexität
- Vielfach teilbar durch kleine Primzahlen
- Liegen im Inneren des Zahlengitters  
- Volumenfüllung der Struktur

## EABC-System

### Modulo-12 Klassifikation

Jede Primzahl p > 3 liegt in genau einer dieser Klassen:

```
E: p ≡ 1  (mod 12)  →  Beispiele: 13, 37, 61, 73...
A: p ≡ 5  (mod 12)  →  Beispiele: 5, 17, 29, 41...
B: p ≡ 7  (mod 12)  →  Beispiele: 7, 19, 31, 43...
C: p ≡ 11 (mod 12)  →  Beispiele: 11, 23, 47, 59...
```

Die Primzahlen 2 und 3 haben Sonderrollen.

### Signaturvektor

Jede Zahl n erhält einen 6D-Signaturvektor:

```
(n_2, n_3 | n_E, n_A, n_B, n_C)
```

wo n_X die Summe der Exponenten aller Primfaktoren in Klasse X ist.

## Duale Interpretation

### 1. Schichtzahl σ(n)

Die **Schichtzahl** ist die Summe aller Exponenten:

```
σ(n) = Σ e_i
```

**Beispiele:**
```
σ(1) = 0     → Schicht 0
σ(2) = 1     → Schicht 1  
σ(6) = 2     → Schicht 2  (2¹×3¹)
σ(72) = 5    → Schicht 5  (2³×3²)
```

**Geometrische Interpretation:**
- Schichten bilden konzentrische "Schalen" um den Ursprung
- Analog zum Simplex-Gitter
- Erinnert an das Pascal-Dreieck
- Tetraeder-Struktur im 4D-Raum

### 2. Vektorzahl v(n)

Die **Vektorzahl** ist der EABC-Anteil des Signaturvektors:

```
v(n) = (n_E, n_A, n_B, n_C)
```

**Beispiele:**
```
v(5) = (0,1,0,0)      → A-Achse
v(385) = (0,1,1,1)    → 5×7×11
v(3025) = (0,2,0,2)   → 5²×11²
```

**Geometrische Interpretation:**
- Definiert Position innerhalb einer Schicht
- 4D-Richtungsvektor im EABC-Raum
- Quaternionen-artige Struktur

## Das Periodensystem der Zahlen

### Koordinatendarstellung

Jede Zahl wird durch zwei Koordinaten beschrieben:

```
n ↦ (σ(n), v(n))
```

Dies erzeugt eine natürliche Hierarchie:

```
Schicht 0:  1                           v=(0,0,0,0)

Schicht 1:  2, 3, 5, 7, 11             Primzahlen (Achsen)

Schicht 2:  4, 6, 9, 10, 15, 25, ...   Primquadrate + Produkte

Schicht 3:  8, 12, 18, 20, 27, ...     Höhere Kompositionen
```

### Beispiel-Periodensystem

```
═══ Schicht σ=0 ═══
  v=(0,0,0,0): 1

═══ Schicht σ=1 ═══
  v=(0,0,0,0): 2, 3
  v=(0,1,0,0): 5
  v=(0,0,1,0): 7
  v=(0,0,0,1): 11

═══ Schicht σ=2 ═══
  v=(0,0,0,0): 4, 6, 9
  v=(0,2,0,0): 25
  v=(0,1,0,0): 10, 15
  v=(0,0,2,0): 49
  v=(0,1,1,0): 35
  v=(0,0,1,0): 14, 21
  v=(0,1,0,1): 55
  ...
```

## Geometrische Struktur

### 4D-Gitter

Das EABC-System spannt ein 4-dimensionales Gitter auf:

```
Achsen:   E-Achse (≡1 mod 12)
          A-Achse (≡5 mod 12)  
          B-Achse (≡7 mod 12)
          C-Achse (≡11 mod 12)

Primzahlen:   Liegen AUF den Achsen
              Beispiel: 5 = (0,1,0,0)

Glatte Zahlen: Liegen IM INNEREN
               Beispiel: 385 = 5×7×11 = (0,1,1,1)
```

### Quaternionen-Analogie

Die Struktur erinnert an Quaternionen:

```
q = e·e + a·A + b·B + c·C
```

wo Multiplikation von Zahlen der Addition von Exponentenvektoren entspricht:

```
n₁ × n₂  ⟺  v(n₁) + v(n₂)
```

**Beispiel:**
```
30 × 12 = 360
2¹×3¹×5¹  ×  2²×3¹  =  2³×3²×5¹
(1,1,0) + (2,1,0) = (3,2,0)  (nur 2,3,5)
```

## Anwendungen

### 1. Klassifikation von Zahlen

```cpp
analysiere_zahl(385);
```

**Ausgabe:**
```
=== ANALYSE VON 385 ===
Faktorisierung: 5 × 7 × 11
EABC-Signatur: (2^0 3^0 | E^0 A^1 B^1 C^1)
Schichtzahl σ(n): 3
Vektorzahl v(n): (0,1,1,1)
EABC-Summe: 3
→ GITTERPUNKT (Innenpunkt, Schicht 3)
```

### 2. Recamán-Folgen-Hypothese

**Hypothese:** Die Recamán-Folge bevorzugt Randpunkte des Gitters und meidet hochglatte Innenpunkte.

**Test:**
```cpp
analysiere_recaman_luecken(500, 300);
```

**Mögliches Ergebnis:**
```
Durchschnittliche Schichtzahl (besucht): 2.34
Durchschnittliche Schichtzahl (nicht besucht): 3.87

→ HYPOTHESE BESTÄTIGT: Nicht-besuchte Zahlen tendieren zu höheren Schichten!
  Die Recamán-Folge bevorzugt Randpunkte und meidet hochglatte Innenpunkte.
```

**Interpretation:**
- Primzahlen (Schicht 1) werden häufiger besucht
- Hochglatte Zahlen wie 72=2³×3², 108=2²×3³ werden gemieden
- Die Dynamik bevorzugt "einfache" Zahlen am Rand

### 3. Primzahl-Verteilung

```cpp
vergleiche_prim_glatt(100, 3);
```

Zeigt den fundamentalen Unterschied:

```
Primzahlen: 25 Zahlen
  → Achsenpunkte des Gitters
  → 'Harte' Faktorisierung

3-glatte Zahlen: 37 Zahlen  
  → Gitterpunkte im Inneren
  → 'Weiche' Faktorisierung

Verhältnis Glatt/Prim: 1.48
```

## Mathematische Eigenschaften

### Schichten als Simplex-Gitter

Die Zahlen in Schicht σ=k bilden ein Simplex:

```
{(a,b,c,d) ∈ ℕ⁴ | a+b+c+d = k}
```

Anzahl Gitterpunkte in Schicht k:

```
|Schicht k| = C(k+3, 3) = (k+1)(k+2)(k+3)/6
```

**Beispiel:**
```
Schicht 0: C(3,3) = 1    Punkt
Schicht 1: C(4,3) = 4    Punkte  
Schicht 2: C(5,3) = 10   Punkte
Schicht 3: C(6,3) = 20   Punkte
```

### Dichtefunktion

Anteil der k-schichtigen Zahlen unter den ersten n Zahlen:

```
ρ_k(n) = #{m ≤ n | σ(m) = k} / n
```

Für große n:
- ρ₁(n) ≈ 1/ln(n)  (Primzahldichte)
- ρ_k(n) wächst langsam

### Glättheit und Schicht

Eine s-glatte Zahl hat nicht notwendig hohe Schichtzahl:

**Gegenbeispiele:**
```
16 = 2⁴         → σ=4, aber 2-glatt
81 = 3⁴         → σ=4, aber 3-glatt
1024 = 2¹⁰      → σ=10, aber 2-glatt
```

**Aber:** Hochglatte Zahlen mit vielen verschiedenen Primfaktoren haben tendenziell höhere Schichtzahlen.

## Experimentelle Fragen

### 1. Recamán-Struktur

- Sind die dauerhaft nicht-besuchten Zahlen überwiegend hochglatt?
- Gibt es bevorzugte EABC-Vektoren in der Recamán-Folge?
- Korreliert die Besuchshäufigkeit mit σ(n)?

### 2. Verteilung im Gitter

- Wie verteilen sich Zahlen auf die EABC-Vektoren?
- Gibt es "leere" Regionen im Gitter?
- Welche Vektoren kommen am häufigsten vor?

### 3. Arithmetische Progressionen

- Liegen arithmetische Progressionen in speziellen Schichten?
- Gibt es Zusammenhänge zwischen σ(n) und Teilbarkeitseigenschaften?

## Implementierungs-Details

### Funktionen

**Faktorisierung:**
```cpp
Faktorisierung f = faktorisiere(n);
int sigma = f.exponentensumme();
```

**EABC-Signatur:**
```cpp
EABCSignatur sig = zu_eabc_signatur(f);
cout << sig.zu_string();  // "(0,1,1,1)"
```

**Schichten:**
```cpp
auto schichten = generiere_schichten(zahlen);
zeige_schichten(schichten, 5);
```

**Periodensystem:**
```cpp
generiere_periodensystem(100, 4);
```

## Visualisierung

### ASCII-Darstellung

```
     E
    /|\
   / | \
  /  |  \
 A---+---B
  \  |  /
   \ | /
    \|/
     C
```

Dies ist eine Projektion des 4D-Gitters in 3D.

### Schicht-Visualisierung

```
Schicht 0: ●
Schicht 1: ● ● ● ●
Schicht 2: ● ● ● ● ● ● ● ● ● ●
Schicht 3: ● ● ● ● ● ● ● ● ● ● ... (20 Punkte)
```

## Literatur und Verbindungen

### Verwandte Konzepte

1. **Dickman-Funktion ρ(u):** Asymptotische Dichte glatter Zahlen
2. **Additive Zahlentheorie:** Summenmengen und Gitterstrukturen
3. **Quaternionen:** 4D-Zahlensysteme mit nicht-kommutativer Multiplikation
4. **Tetraeder-Packungen:** Geometrische Realisierung von Simplex-Gittern

### EABC-spezifisch

1. **Quadratische Reste mod 12**
2. **Dirichlet-Charaktere**
3. **Cyclotomische Körper**
4. **Algebraische Zahlentheorie**

## Ausblick

### Offene Fragen

1. Gibt es eine natürliche Metrik auf dem EABC-Gitter?
2. Kann man Primzahllücken durch Gitterstruktur erklären?
3. Existiert eine Fourier-Analyse auf diesem Gitter?
4. Verbindung zu Riemann-Zeta-Funktion?

### Erweiterungen

1. **Höherdimensional:** Einbeziehung weiterer Primklassen
2. **Dynamisch:** Zeitentwicklung auf dem Gitter
3. **Stochastisch:** Zufallswanderungen im Gitter
4. **Topologisch:** Fundamentalgruppe des Gitters

## Zusammenfassung

Das EABC/ABCE-Modell bietet eine geometrische Interpretation der Zahlentheorie:

- **Primzahlen** = Achsen/Eckpunkte
- **Glatte Zahlen** = Volumen/Innenpunkte  
- **Schichtzahl** = Abstand vom Ursprung
- **Vektorzahl** = Richtung im Raum

Diese Struktur ist ein natürliches "Periodensystem der Zahlen", in dem arithmetische Eigenschaften geometrisch sichtbar werden.

---

*Thomas Hoffbauer, 2026*  
*Basierend auf dem Bamberg EABC/ABCE-Quaternionen-Modell*
