# Kapitel 2: Lokale EABC-Restklassengeometrie

## 2.1 Motivation

Die **lokale Ebene** beschreibt den **Inhalt** einer Zahl:

- Welche Primfaktoren sind vorhanden?
- Welchen Restklassen gehören sie an?

---

## 2.2 EABC-Klassifikation

### Definition 2.1: EABC-Klassen modulo 12

Für Primzahlen $p > 3$ definieren wir:

$$\begin{align}
E &= \{p : p \equiv 1 \pmod{12}\} \\
A &= \{p : p \equiv 5 \pmod{12}\} \\
B &= \{p : p \equiv 7 \pmod{12}\} \\
C &= \{p : p \equiv 11 \pmod{12}\}
\end{align}$$

**Notation:**

$$\sigma_{12}: p \mapsto \{E, A, B, C\}$$

ist die Restklassenabbildung.

---

### Definition 2.2: EABC-Signatur

Für eine Zahl

$$n = \prod_{i=1}^k p_i$$

ist die **EABC-Signatur** das Wort

$$E(n) = \sigma_{12}(n) = (\sigma_{12}(p_1), \ldots, \sigma_{12}(p_k)) \in \{E,A,B,C\}^k$$

**Beispiel:**

$$n = 5 \cdot 7 \cdot 13 \cdot 23$$

$$\sigma_{12}(5) = A, \quad \sigma_{12}(7) = B, \quad \sigma_{12}(13) = E, \quad \sigma_{12}(23) = C$$

$$E(n) = (A, B, E, C)$$

---

## 2.3 Feinere Siebstruktur

### Definition 2.3: EABC-Klassen modulo 420

Für höhere Auflösung kann man

$$m = 420 = 2^2 \cdot 3 \cdot 5 \cdot 7$$

verwenden.

Die Restklassen $\pmod{420}$ bilden einen 96-dimensionalen Raum:

$$\phi(420) = 96$$

---

### Definition 2.4: EABC-Klassen modulo 60060

Für maximale Auflösung:

$$m = 60060 = 2^2 \cdot 3 \cdot 5 \cdot 7 \cdot 11 \cdot 13$$

mit

$$\phi(60060) = 5760$$

Restklassen.

---

## 2.4 Lokaler Hilbertraum

### Definition 2.5: EABC-Zustandsraum

Der lokale Zustandsraum ist:

$$\mathcal{H}_{\mathrm{loc}} = \ell^2(\mathbb{Z}/m\mathbb{Z}^\times)$$

wobei $m \in \{12, 420, 60060\}$.

Dimension:

$$\dim \mathcal{H}_{\mathrm{loc}} = \phi(m)$$

---

### Definition 2.6: Lokaler Dirac-Operator

Auf $\mathcal{H}_{\mathrm{loc}}$ definieren wir einen selbstadjungierten Operator:

$$D_{\mathrm{loc}}: \mathcal{H}_{\mathrm{loc}} \to \mathcal{H}_{\mathrm{loc}}$$

**Konstruktion (Beispiel $m=420$):**

$$D_{420} = \sum_{i < j} w_{ij} (P_i - P_j)^2$$

wobei $P_i$ Projektoren auf Restklassen sind.

---

## 2.5 EABC-Observablen

### Definition 2.7: EABC-Komplexität

Für eine Signatur $E(n) = (s_1, \ldots, s_k)$ definieren wir:

$$C_{\mathrm{EABC}}(n) = \sum_{i < j} d(s_i, s_j)$$

wobei $d: \{E,A,B,C\}^2 \to \mathbb{R}_{\geq 0}$ eine Metrik auf den vier Klassen ist.

**Beispiel:** Cyclische Metrik auf $\mathbb{Z}/4\mathbb{Z}$:

$$\{E, A, B, C\} \cong \{0, 1, 2, 3\} \pmod{4}$$

$$d(s_i, s_j) = \min(|i-j|, 4 - |i-j|)$$

---

## 2.6 Wichtige Eigenschaften

### Satz 2.1: Dichtigkeit der EABC-Klassen

Nach dem Primzahlsatz in arithmetischen Progressionen gilt:

$$\pi_E(x) \sim \pi_A(x) \sim \pi_B(x) \sim \pi_C(x) \sim \frac{x}{4 \log x}$$

für $x \to \infty$.

**Konsequenz:** Jede EABC-Klasse hat asymptotisch gleiche Dichte.

---

### Satz 2.2: Unabhängigkeit der Faktoren

Für typische Zahlen sind die EABC-Signaturen der Primfaktoren näherungsweise **unabhängig identisch verteilt**:

$$E(n) \sim \text{Uniform}(\{E,A,B,C\}^k)$$

im probabilistischen Modell.

**Wichtig:** Echte Korrelationen zwischen Faktoren sind **arithmetische Signale**.

---

## 2.7 Verbindung zur globalen Ebene

Die lokale Ebene liefert **Labels** für die Blätter des Catalan-Baums:

$$T(n) \in \mathcal{T}_k \quad \text{mit Blattbeschriftung} \quad E(n) \in \{E,A,B,C\}^k$$

Die **Kopplung** zwischen lokaler und globaler Ebene ist Gegenstand von **Kapitel 5**.

---

## Literatur

- Hardy, G. H., & Littlewood, J. E. (1923). Some problems of 'Partitio numerorum'; III.
- Davenport, H. (2000). *Multiplicative Number Theory*. Chapter 4.
