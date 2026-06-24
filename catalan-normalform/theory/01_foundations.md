# Kapitel 1: Mathematische Grundlagen

## 1.1 Ausgangspunkt

**Zentrale Dichotomie:**

$$\text{lokal: Welche Faktoren?} \quad \leftrightarrow \quad \text{global: Wie sind diese Faktoren hierarchisch verschaltet?}$$

**Leitidee:**

$$\boxed{\text{Arithmetische Komplexität ist nicht nur Faktorinhalt, sondern auch Faktorarchitektur.}}$$

---

## 1.2 Grundbegriffe

### Definition 1.1: Primfaktorzerlegung mit Vielfachheit

Für $n \in \mathbb{N}_{\geq 2}$ sei

$$n = \prod_{i=1}^k p_i$$

die Primfaktorzerlegung **mit Vielfachheit**, wobei

$$\Omega(n) = k$$

die Anzahl der Primfaktoren mit Vielfachheit zählt (additive Funktion).

**Konvention:** Wir schreiben die Faktoren in aufsteigender Reihenfolge:

$$p_1 \leq p_2 \leq \cdots \leq p_k$$

und behandeln gleiche Primfaktoren als unterscheidbare Objekte:

$$2^3 \cdot 5 \quad \leadsto \quad (2_1, 2_2, 2_3, 5)$$

---

### Definition 1.2: Erweiterte Normalform

Eine Zahl $n$ besitzt die **erweiterte Normalform:**

$$\boxed{n = (G(n), P(n), E(n), T(n))}$$

wobei:

| Komponente | Name | Typ | Bedeutung |
|------------|------|-----|-----------|
| $G(n)$ | Glatte Struktur | $\mathbb{N}$ | Größenordnung, glatte Faktoren |
| $P(n)$ | Primfaktorinhalt | Multiset | $\{p_1, \ldots, p_k\}$ mit Vielfachheit |
| $E(n)$ | EABC-Signatur | $\{E,A,B,C\}^k$ | Restklassensignatur |
| $T(n)$ | Catalan-Hierarchie | $\mathcal{T}_k$ | Binäre Klammerungsstruktur |

---

## 1.3 Catalan-Zahlen und binäre Bäume

### Definition 1.3: Catalan-Zahl

Die $k$-te Catalan-Zahl ist:

$$C_k = \frac{1}{k+1}\binom{2k}{k} = \frac{(2k)!}{(k+1)! \, k!}$$

Für $k$ Faktoren gibt es $C_{k-1}$ vollständig binäre Klammerungen.

**Beispiel:** Für $k=4$ Faktoren $(a,b,c,d)$ gibt es $C_3 = 5$ Klammerungen:

1. $(((ab)c)d)$
2. $((a(bc))d)$
3. $((ab)(cd))$
4. $(a((bc)d))$
5. $(a(b(cd)))$

---

### Definition 1.4: Menge der binären Bäume

$$\mathcal{T}_k = \{\text{vollständig binäre Bäume mit } k \text{ Blättern}\}$$

mit

$$|\mathcal{T}_k| = C_{k-1}$$

Jeder Baum $T \in \mathcal{T}_k$ besitzt:

- $k$ Blätter (externe Knoten)
- $k-1$ interne Knoten
- Höhe $h(T) \in [\lceil \log_2 k \rceil, k-1]$

---

## 1.4 Kanonisierungsproblem

### Problem 1.1: Nicht-Eindeutigkeit

Eine Zahl $n = p_1 p_2 \cdots p_k$ besitzt **von sich aus** keine eindeutige Klammerung.

Die Multiplikation ist assoziativ:

$$(ab)c = a(bc)$$

Daher existiert keine intrinsische Auszeichnung eines bestimmten Baumes $T \in \mathcal{T}_k$.

**Konsequenz:** Wir müssen eine **Kanonisierung** wählen oder über alle Bäume mitteln.

---

### Definition 1.5: Kanonische Abbildung

Eine **Kanonisierung** ist eine Abbildung

$$\kappa: \mathbb{N}_{\geq 2} \to \bigcup_{k=2}^\infty \mathcal{T}_k$$

mit

$$\kappa(n) \in \mathcal{T}_{\Omega(n)}$$

die jeder Zahl einen bestimmten Baum zuordnet.

---

## 1.5 Drei natürliche Kanonisierungen

### Linksbaum

$$T_L(p_1, \ldots, p_k) = ((\cdots((p_1 p_2) p_3) \cdots) p_k)$$

Maximale Linkslastigkeit, Höhe $h = k-1$.

**Rekursion:**

$$T_L(p_1, \ldots, p_k) = (T_L(p_1, \ldots, p_{k-1}), p_k)$$

---

### Rechtsbaum

$$T_R(p_1, \ldots, p_k) = (p_1 (p_2 (\cdots (p_{k-1} p_k))))$$

Maximale Rechtslastigkeit, Höhe $h = k-1$.

**Rekursion:**

$$T_R(p_1, \ldots, p_k) = (p_1, T_R(p_2, \ldots, p_k))$$

---

### Balancierter Baum

$$T_B(p_1, \ldots, p_k) = (T_B(p_1, \ldots, p_m), T_B(p_{m+1}, \ldots, p_k))$$

wobei $m = \lfloor k/2 \rfloor$.

Minimale Höhe $h = \lceil \log_2 k \rceil$.

**Problem:** Bei ungeradem $k$ gibt es mehrere fast-balancierte Varianten.

---

### Definition 1.6: Menge balancierter Bäume

$$\mathcal{B}_k \subseteq \mathcal{T}_k$$

ist die Menge aller Bäume mit **minimaler Höhe**:

$$\mathcal{B}_k = \{T \in \mathcal{T}_k : h(T) = \lceil \log_2 k \rceil\}$$

---

## 1.6 Nächste Schritte

Die folgenden Kapitel definieren:

- **Kapitel 2:** Lokale EABC-Geometrie ($E(n)$)
- **Kapitel 3:** Globale Catalan-Geometrie ($T(n)$)
- **Kapitel 4:** Observablen und Catalan-Magic
- **Kapitel 5:** Tensorprodukt und Kopplung

---

## Literatur

- Stanley, R. P. (2015). *Catalan Numbers*. Cambridge University Press.
- Knuth, D. E. (1997). *The Art of Computer Programming, Volume 1*. Section 2.3.4.4.
