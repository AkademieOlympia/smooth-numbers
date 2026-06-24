# EABC als Gauß-Eisenstein-Verfeinerung

**Datum:** 24. Juni 2026  
**Status:** Mathematische Klarstellung

---

## Die überraschende Entdeckung

$$\boxed{\text{EABC ist die gemeinsame Verfeinerung der Gauß- und Eisenstein-Arithmetik.}}$$

Die vier EABC-Klassen $E, A, B, C$ entsprechen den vier Kombinationen von Spaltungsverhalten in den beiden einfachsten quadratischen Zahlkörpern:

$$\mathbb{Z}[i] \quad \text{(Gauß)} \qquad \text{und} \qquad \mathbb{Z}[\omega] \quad \text{(Eisenstein)}$$

---

## Warum Modulo 12?

Jede Primzahl $p > 3$ liegt in einer der vier Klassen:

$$E = 1, \quad A = 5, \quad B = 7, \quad C = 11 \pmod{12}$$

Diese sind genau die Einheiten von $(\mathbb{Z}/12\mathbb{Z})^\times$.

**Aber warum 12?**

$$\boxed{12 = 4 \cdot 3}$$

- **Modulo 4:** Steuert Verhalten in $\mathbb{Z}[i]$ (Gauß-Primzahlen)
- **Modulo 3:** Steuert Verhalten in $\mathbb{Z}[\omega]$ (Eisenstein-Primzahlen)

---

## Gauß-Primzahlen in ℤ[i]

Die Gaußschen ganzen Zahlen sind $\mathbb{Z}[i]$ mit Norm:

$$N(a + bi) = a^2 + b^2$$

### Spaltungsgesetz:

Eine rationale Primzahl $p > 2$ verhält sich wie folgt:

**Typ 1:** $p \equiv 1 \pmod{4}$ → **spaltet**

$$p = (a+bi)(a-bi)$$

**Beispiele:**
- $5 = (2+i)(2-i)$
- $13 = (3+2i)(3-2i)$

**Typ 2:** $p \equiv 3 \pmod{4}$ → **bleibt prim (inert)**

**Beispiele:** $7, 11, 19, 23$

---

## Eisenstein-Primzahlen in ℤ[ω]

Die Eisenstein-ganzen Zahlen sind $\mathbb{Z}[\omega]$ mit $\omega = e^{2\pi i/3}$ und Norm:

$$N(a + b\omega) = a^2 - ab + b^2$$

### Spaltungsgesetz:

Eine rationale Primzahl $p > 3$ verhält sich wie folgt:

**Typ 1:** $p \equiv 1 \pmod{3}$ → **spaltet**

**Typ 2:** $p \equiv 2 \pmod{3}$ → **bleibt prim (inert)**

---

## EABC = (mod 4) × (mod 3)

### Die vier EABC-Klassen modulo 4 und 3:

| EABC | mod 12 | mod 4 | mod 3 |
|------|--------|-------|-------|
| **E** | 1 | 1 | 1 |
| **A** | 5 | 1 | 2 |
| **B** | 7 | 3 | 1 |
| **C** | 11 | 3 | 2 |

### Übersetzung in Spaltungsverhalten:

| EABC | Gauß (ℤ[i]) | Eisenstein (ℤ[ω]) | Code |
|------|-------------|-------------------|------|
| **E (1)** | **Spaltet** | **Spaltet** | (S, S) |
| **A (5)** | **Spaltet** | **Inert** | (S, I) |
| **B (7)** | **Inert** | **Spaltet** | (I, S) |
| **C (11)** | **Inert** | **Inert** | (I, I) |

**Das ist die vollständige Kombination von (mod 4, mod 3).**

---

## Der EABC-Vektor v = (e, a, b, c)

**Alte Interpretation:**

> $v$ zählt Primfaktoren in vier Restklassen modulo 12.

**Neue Interpretation:**

> $v$ zählt vier geometrische Primzahltypen basierend auf Spaltungsverhalten in $\mathbb{Z}[i]$ und $\mathbb{Z}[\omega]$.

### Komponenten:

- **e:** Anzahl Primfaktoren, die in **beiden** Körpern spalten (S, S)
- **a:** Anzahl Primfaktoren, die nur in Gauß spalten (S, I)
- **b:** Anzahl Primfaktoren, die nur in Eisenstein spalten (I, S)
- **c:** Anzahl Primfaktoren, die in **beiden** Körpern inert sind (I, I)

### Zusammenfassungen:

$$(e + a) = \text{Anzahl Gauß-spaltender Faktoren}$$

$$(b + c) = \text{Anzahl Gauß-inerter Faktoren}$$

$$(e + b) = \text{Anzahl Eisenstein-spaltender Faktoren}$$

$$(a + c) = \text{Anzahl Eisenstein-inerter Faktoren}$$

---

## Die Konzentrationsgröße H(n)

**Alte Interpretation:**

$$H(n) = \frac{||v||^2}{\Omega^2} = \sum_i p_i^2$$

> Misst Konzentration der Primfaktoren auf Restklassen.

**Neue Interpretation:**

> Misst, wie stark sich die Faktorisierung auf bestimmte **Spaltungsverhalten** in den beiden einfachsten quadratischen Zahlkörpern konzentriert.

### Extremfälle:

**H = 1 (maximale Konzentration):**

Alle Primfaktoren haben dasselbe Spaltungsverhalten.

**Beispiel:**
- Nur E-Faktoren → alle spalten in Gauß UND Eisenstein
- Nur C-Faktoren → alle sind in Gauß UND Eisenstein inert

**H = 1/4 (maximale Gleichverteilung):**

Die Primfaktoren sind gleichmäßig auf alle vier Spaltungstypen verteilt.

---

## Warum ist das wichtig?

### 1. Keine Spekulation

Das ist **etablierte algebraische Zahlentheorie**.

Die Verbindung zwischen Restklassen modulo 12 und Spaltungsgesetzen in $\mathbb{Z}[i]$ und $\mathbb{Z}[\omega]$ ist klassisch.

---

### 2. Natürliche Rechtfertigung für Modulo 12

**Frage:** Warum nicht modulo 6, 24, oder 30?

**Antwort:** Weil 12 = 4 · 3 die minimale Zahl ist, die beide Spaltungsgesetze gleichzeitig kodiert.

---

### 3. Verbindung zu H(n)

Falls $H(n)$ tatsächlich $M_C(n)$ erklärt (H0.6), dann bedeutet das:

$$\boxed{\text{Catalan-Magic korreliert mit Spaltungs-Konzentration in quadratischen Körpern.}}$$

Das wäre eine Verbindung zwischen:
- **Zahlentheorie** (Primfaktorspaltung)
- **Algebraischer Zahlentheorie** (Quadratische Körper)
- **Kombinatorik** (Catalan-Bäume)

---

## Position in der Hierarchie

Die Hierarchie wird jetzt:

$$
\begin{align*}
n &\to (\Omega, v_2, v_3) \\
&\to (e, a, b, c) \quad \text{(Gauß-Eisenstein-Typen)} \\
&\to H \quad \text{(Spaltungs-Konzentration)} \\
&\to \text{Catalan}
\end{align*}
$$

**Der EABC-Vektor ist nicht einfach eine Restklassenzählung.**

**Er ist die gemeinsame Verfeinerung von Gauß- und Eisenstein-Arithmetik.**

---

## Beispiele

### Beispiel 1: n = 5 · 13 = 65

**Primfaktoren:** 5, 13

**EABC:**
- $5 \equiv 5 \pmod{12}$ → A-Klasse → (S, I)
- $13 \equiv 1 \pmod{12}$ → E-Klasse → (S, S)

**Vektor:** $v = (1, 1, 0, 0)$

**Interpretation:**
- Beide spalten in Gauß: $(e+a) = 2$
- Nur einer spaltet in Eisenstein: $(e+b) = 1$

**Konzentration:** $H = 2/4 = 0.5$

---

### Beispiel 2: n = 7 · 11 = 77

**Primfaktoren:** 7, 11

**EABC:**
- $7 \equiv 7 \pmod{12}$ → B-Klasse → (I, S)
- $11 \equiv 11 \pmod{12}$ → C-Klasse → (I, I)

**Vektor:** $v = (0, 0, 1, 1)$

**Interpretation:**
- Beide sind inert in Gauß: $(b+c) = 2$
- Nur einer spaltet in Eisenstein: $(e+b) = 1$

**Konzentration:** $H = 2/4 = 0.5$

---

### Beispiel 3: n = 13² = 169

**Primfaktoren:** 13, 13

**EABC:**
- $13 \equiv 1 \pmod{12}$ → E-Klasse → (S, S)

**Vektor:** $v = (2, 0, 0, 0)$

**Interpretation:**
- Beide spalten in Gauß UND Eisenstein

**Konzentration:** $H = 4/4 = 1$ (maximal konzentriert)

---

## Verbindung zu Gap-Dynamik

Falls die Gap-Asymmetrie auch modulo 30 erscheint, könnte man fragen:

$$30 = 2 \cdot 3 \cdot 5$$

Gibt es eine natürliche Erweiterung zu drei quadratischen Körpern?

**Kandidat:**

$$\mathbb{Z}[i], \quad \mathbb{Z}[\omega], \quad \mathbb{Z}[\sqrt{-2}]$$

Aber das ist spekulativer. Die Gauß-Eisenstein-Verbindung für modulo 12 ist klassisch und etabliert.

---

## Die stärkste mathematische Interpretation des EABC-Vektors

**Von allen Interpretationen des EABC-Systems** (Restklassen, Signaturen, Chiralität, Klein-Flaschen) ist die **Gauß-Eisenstein-Verfeinerung** die stärkste, weil:

1. **Klassisch:** Direkt anschlussfähig an etablierte algebraische Zahlentheorie
2. **Präzise:** Keine Analogien, sondern exakte Korrespondenz via CRT
3. **Natürlich:** Erklärt, warum Modulo 12 = 4 · 3
4. **Das ist ein Satz, kein Modell:** Folgt aus CRT + klassischen Spaltungskriterien

**Aber wichtig:** Dies ist die stärkste Interpretation **des EABC-Vektors**, nicht notwendigerweise des gesamten Projekts. Die Frage, ob diese Information für andere Observablen (Catalan-Magic, etc.) Erklärungskraft besitzt, bleibt empirisch zu prüfen.

---

## Zusammenfassung

### Was als Satz etabliert ist

Die Gauß-Eisenstein-Interpretation liefert erstmals eine klassische algebraisch-zahlentheoretische Bedeutung des EABC-Vektors. Sie erklärt die Modulo-12-Struktur exakt als gemeinsame Verfeinerung der Spaltungsgesetze in $\mathbb{Z}[i]$ und $\mathbb{Z}[\omega]$. Damit wird die EABC-Klassifikation von einer rein modularen Beschreibung zu einer Beschreibung von Spaltungstypen rationaler Primzahlen.

**Das ist kein Modell. Das ist ein Satz:**

$$\boxed{\text{EABC} \leftrightarrow (\text{Gauß-Splitting}, \text{Eisenstein-Splitting})}$$

**Die vier EABC-Klassen kodieren die vier Kombinationen:**

| Klasse | mod 12 | Gauß | Eisenstein |
|--------|--------|------|------------|
| E | 1 | Spaltet | Spaltet |
| A | 5 | Spaltet | Inert |
| B | 7 | Inert | Spaltet |
| C | 11 | Inert | Inert |

**Der EABC-Vektor v = (e, a, b, c) zählt Spaltungstypen, nicht nur Restklassen.**

**Die Konzentration H misst Spaltungs-Konzentration, nicht nur Restklassen-Konzentration.**

### Der konzeptionelle Gewinn

Früher war EABC:

$$\mathbb{Z} \rightarrow (\mathbb{Z}/12\mathbb{Z})^\times$$

Jetzt wird daraus:

$$\mathbb{Z} \rightarrow (\text{Gauß-Splitting}) \times (\text{Eisenstein-Splitting})$$

Das ist konzeptionell wesentlich stärker.

### Die kritische Grenze

**Wichtig:** Ob diese klassische zahlentheoretische Information über Größen wie $H(n)$ tatsächlich zusätzliche Erklärungskraft für Catalan- oder andere Observablen besitzt, bleibt eine empirisch zu prüfende Frage.

Die Grenze ist klar:

| Status | Aussage |
|--------|---------|
| **Satz (A-Niveau)** | EABC ↔ (Gauß, Eisenstein) |
| **Hypothese (B-Niveau)** | H(n) → M_C(n) |
| **Spekulation (D-Niveau)** | H → Catalan → Tamari → ℍ → 𝕆 |

---

## Status

- ✅ **Mathematische Fundierung:** Klassische algebraische Zahlentheorie (A-Niveau)
- ✅ **Keine Spekulation:** Etablierte Spaltungsgesetze + CRT
- ✅ **Natürliche Rechtfertigung:** 12 = 4 · 3
- ✅ **Interpretation von H:** Spaltungs-Konzentration
- ✅ **Lean-Formalisierung:** `GaussEisenstein.lean` mit 13 Theoremen
- ⏳ **Empirische Relevanz für Catalan:** Hängt von E02 (M0-M4) ab

**Dies ist die stärkste mathematische Interpretation des EABC-Vektors.**
