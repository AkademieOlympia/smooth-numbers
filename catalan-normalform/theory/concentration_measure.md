# Die Konzentrationsgröße H(n)

**Autor:** Thomas Hoffbauer  
**Datum:** 24. Juni 2026  
**Status:** Theoretische Grundlage

---

## Die zentrale Beobachtung

Die EABC-Vektornorm $||v_{\text{fac}}(n)||^2$ misst nicht primär die "Größe" der Faktorisierung.

Sie misst die **Konzentration der Primfaktoren auf Restklassen**.

---

## Definition

Für eine Zahl $n$ mit EABC-Faktorvektor $v_{\text{fac}}(n) = (e, a, b, c)$ definieren wir:

$$\boxed{H(n) := \frac{||v_{\text{fac}}(n)||^2}{\Omega_{\text{EABC}}(n)^2}}$$

wobei $\Omega_{\text{EABC}}(n) = e + a + b + c$ die Anzahl der Primfaktoren $p > 3$ (mit Vielfachheit) zählt.

---

## Interpretation als Konzentration

### Normierte Anteile

Definiere die normierten Anteile:

$$p_E = \frac{e}{\Omega_{\text{EABC}}}, \quad p_A = \frac{a}{\Omega_{\text{EABC}}}, \quad p_B = \frac{b}{\Omega_{\text{EABC}}}, \quad p_C = \frac{c}{\Omega_{\text{EABC}}}$$

mit $p_E + p_A + p_B + p_C = 1$.

### Dann gilt:

$$H(n) = p_E^2 + p_A^2 + p_B^2 + p_C^2$$

Dies ist mathematisch äquivalent zu bekannten Konzentrationsmaßen:

**Simpson-Index** (Ökologie):
$$\lambda = \sum_i p_i^2$$

**Herfindahl-Hirschman-Index** (Ökonomie):
$$\text{HHI} = \sum_i p_i^2$$

**Rényi-Entropie** (Ordnung 2):
$$H_2 = -\log\left(\sum_i p_i^2\right)$$

---

### Algebraisch-zahlentheoretische Interpretation

**Die vier EABC-Komponenten kodieren Spaltungsverhalten:**

| Komponente | Gauß ($\mathbb{Z}[i]$, mod 4) | Eisenstein ($\mathbb{Z}[\omega]$, mod 3) |
|------------|-------------------------------|-------------------------------------------|
| **e** | Spaltet (S) | Spaltet (S) |
| **a** | Spaltet (S) | Inert (I) |
| **b** | Inert (I) | Spaltet (S) |
| **c** | Inert (I) | Inert (I) |

**Dann misst H(n):**

> Wie stark konzentriert sich die Faktorisierung auf bestimmte **Spaltungsverhalten** in den beiden einfachsten quadratischen Zahlkörpern?

**Das ist etablierte algebraische Zahlentheorie, keine Spekulation.**

**Siehe:** `GAUSS_EISENSTEIN.md` für vollständige Details.

---

## Extremfälle

### Maximal konzentriert:

Alle Faktoren in einer Klasse:

$$v = (\Omega_{\text{EABC}}, 0, 0, 0)$$

$$\Rightarrow \quad H = 1$$

**Interpretation:** Alle Primfaktoren $p > 3$ liegen in derselben Restklasse modulo 12.

---

### Maximal verteilt:

Gleichverteilung:

$$v = \left(\frac{\Omega_{\text{EABC}}}{4}, \frac{\Omega_{\text{EABC}}}{4}, \frac{\Omega_{\text{EABC}}}{4}, \frac{\Omega_{\text{EABC}}}{4}\right)$$

$$\Rightarrow \quad H = \frac{1}{4}$$

**Interpretation:** Die Primfaktoren sind gleichmäßig auf E, A, B, C verteilt.

---

## Wertebereich

$$\frac{1}{4} \leq H(n) \leq 1$$

- **$H = 1$:** Maximale Konzentration
- **$H = 1/4$:** Maximale Gleichverteilung
- **$H \in (1/4, 1)$:** Partielle Konzentration

---

## Warum H statt ||v||²?

### Problem der rohen Norm:

$$||v||^2 = e^2 + a^2 + b^2 + c^2$$

wächst mit $\Omega_{\text{EABC}}^2$, selbst bei Gleichverteilung.

**Beispiel:**

- $v_1 = (4, 0, 0, 0) \Rightarrow ||v_1||^2 = 16$
- $v_2 = (40, 0, 0, 0) \Rightarrow ||v_2||^2 = 1600$

Beide sind maximal konzentriert, aber die Norm ist sehr unterschiedlich.

### Vorteil der dimensionslosen Version:

$$H(n_1) = H(n_2) = 1$$

**Das normierte Maß $H$ ist invariant unter Skalierung.**

---

## Verbindung zur Informationstheorie

Die Shannon-Entropie ist:

$$H_{\text{Shannon}} = -\sum_i p_i \log p_i$$

Die Rényi-Entropie (Ordnung 2) ist:

$$H_2 = -\log\left(\sum_i p_i^2\right) = -\log H(n)$$

**Zusammenhang:**

- **Hohe Konzentration** ($H \to 1$) $\Rightarrow$ **Niedrige Entropie** ($H_2 \to 0$)
- **Gleichverteilung** ($H \to 1/4$) $\Rightarrow$ **Hohe Entropie** ($H_2 \to \log 4$)

---

## Beispiele

### Beispiel 1: Maximale Konzentration

$$n = 13^4 = 28561$$

$$v_{\text{fac}} = (4, 0, 0, 0) \quad (\text{da } 13 \equiv 1 \pmod{12})$$

$$\Omega_{\text{EABC}} = 4$$

$$H(n) = \frac{16}{16} = 1$$

---

### Beispiel 2: Gleichverteilung

$$n = 13 \cdot 5 \cdot 7 \cdot 11 = 5005$$

$$v_{\text{fac}} = (1, 1, 1, 1)$$

$$\Omega_{\text{EABC}} = 4$$

$$H(n) = \frac{4}{16} = \frac{1}{4}$$

---

### Beispiel 3: Partielle Konzentration

$$n = 5 \cdot 5 \cdot 7 = 175$$

$$v_{\text{fac}} = (0, 2, 1, 0)$$

$$\Omega_{\text{EABC}} = 3$$

$$H(n) = \frac{5}{9} \approx 0.556$$

---

## Hypothese H0.6*: Konzentrations-Dominanz

**Stärkere Version:**

Die dimensionslose Konzentration $H(n)$ liefert zusätzliche Vorhersagekraft für $M_C(n)$ über $\Omega(n)$ und $(v_2(n), v_3(n))$ hinaus.

**Formale Teststatistik:**

$$\Delta R^2_H = R^2(\Omega, (v_2, v_3), H) - R^2(\Omega, (v_2, v_3)) > \eta$$

**Modellvergleich:**

```
M2:  M_C ~ Ω + (v₂, v₃)
M3*: M_C ~ Ω + (v₂, v₃) + H
```

**Vorteil gegenüber ||v||²:**

$H$ ist dimensionslos und vergleicht Zahlen mit unterschiedlichem $\Omega_{\text{EABC}}$ sauberer.

---

## Verbindung zu Catalan-Bäumen

### Hypothese:

**Konzentrierte Faktoren** ($H \to 1$) könnten zu **unbalancierten Bäumen** führen.

**Verteilte Faktoren** ($H \to 1/4$) könnten zu **balancierten Bäumen** führen.

**Begründung:**

Wenn alle Primfaktoren in derselben EABC-Klasse liegen, gibt es weniger "Diversität" in der arithmetischen Struktur. Das könnte sich in asymmetrischeren Catalan-Bäumen widerspiegeln.

---

## Implementierung

```python
def compute_concentration(n):
    """
    Berechnet die dimensionslose Konzentration H(n).
    
    H(n) = ||v_fac||² / Ω_EABC²
    
    Wertebereich: [1/4, 1]
    - H = 1: Maximal konzentriert
    - H = 1/4: Maximal gleichverteilt
    """
    factors = prime_factors(n, with_multiplicity=True)
    
    # Nur p > 3
    factors_gt3 = [p for p in factors if p > 3]
    
    if len(factors_gt3) == 0:
        return None  # Keine EABC-Faktoren
    
    # EABC-Vektor
    e = sum(1 for p in factors_gt3 if p % 12 == 1)
    a = sum(1 for p in factors_gt3 if p % 12 == 5)
    b = sum(1 for p in factors_gt3 if p % 12 == 7)
    c = sum(1 for p in factors_gt3 if p % 12 == 11)
    
    Omega_EABC = e + a + b + c
    norm_sq = e**2 + a**2 + b**2 + c**2
    
    H = norm_sq / (Omega_EABC**2)
    
    return H

def compute_renyi_entropy_order2(n):
    """
    Berechnet die Rényi-Entropie (Ordnung 2).
    
    H₂ = -log(H(n))
    """
    H = compute_concentration(n)
    if H is None or H == 0:
        return None
    return -np.log(H)
```

---

## Verwandte Maße

### Gini-Koeffizient:

$$G = 1 - \sum_i p_i^2 = 1 - H$$

Wertebereich: $[0, 3/4]$

### Diversitäts-Index:

$$D = \frac{1}{H}$$

Wertebereich: $[1, 4]$

- $D = 1$: Keine Diversität (eine Klasse)
- $D = 4$: Maximale Diversität (Gleichverteilung)

---

## Zusammenfassung

Die dimensionslose Konzentration $H(n)$ ist:

1. **Mathematisch fundiert:** Äquivalent zu bekannten Konzentrationsmaßen
2. **Dimensionslos:** Vergleichbar über verschiedene $\Omega$
3. **Interpretierbar:** Misst Ungleichverteilung auf Restklassen
4. **Testbar:** Kann in M0-M4-Kaskade integriert werden

**Die zentrale Frage:**

$$\boxed{\text{Ist Catalan-Magic eine Funktion der arithmetischen Konzentration?}}$$

Falls ja, wäre das eine fundamentale Verbindung zwischen Zahlentheorie und kombinatorischer Hierarchie.
