# Catalan-Normalform: Die drei methodischen Säulen

**Datum:** 24. Juni 2026  
**Status:** Etabliert

---

## Das zentrale Motto

$$\boxed{\text{Das Projekt untersucht nicht neue Objekte, sondern zusätzliche Informationsstufen.}}$$

Dies ist die **reife Form** des Forschungsprogramms.

---

## Die drei Säulen des methodischen Durchbruchs

### Säule 1: M0b — Schutz vor Artefakten

$$\boxed{M0b: \Omega + \Omega^2}$$

**Problem:**

Viele kombinatorische Größen wachsen **nicht linear** in $\Omega(n)$. Wenn Catalan-Magic mit der Anzahl möglicher Faktorisierungsbäume korreliert, könnten Terme wie $\Omega^2$, $\Omega \log \Omega$, oder $C_\Omega$ auftreten.

**Ohne M0b** könnte man einen scheinbaren Normeffekt messen, der in Wahrheit nur ein nichtlinearer $\Omega$-Effekt ist.

**Lösung:**

Teste explizit:

$$\Delta_{\Omega^2} = R^2(M0b) - R^2(M0)$$

Falls $\Delta_{\Omega^2}$ signifikant ist, muss $\Omega^2$ in allen weiteren Modellen kontrolliert werden.

**Status:**
- ✅ In E02 implementiert
- ✅ Als M0b in Modellkaskade integriert

---

### Säule 2: H(n) — Dimensionslose Konzentration

$$\boxed{H(n) = \frac{||v_{\text{fac}}(n)||^2}{\Omega_{\text{EABC}}(n)^2}}$$

**Problem:**

Die rohe Norm $||v_{\text{fac}}||^2 = e^2 + a^2 + b^2 + c^2$ wächst mit $\Omega_{\text{EABC}}^2$, selbst bei Gleichverteilung.

**Beispiel:**
- $v_1 = (4, 0, 0, 0) \Rightarrow ||v_1||^2 = 16$
- $v_2 = (40, 0, 0, 0) \Rightarrow ||v_2||^2 = 1600$

Beide sind maximal konzentriert, aber die Norm ist sehr unterschiedlich.

**Lösung:**

Normiere die Norm:

$$H(n) = \frac{||v||^2}{\Omega^2} = \sum_i p_i^2$$

wobei $p_i = v_i / \Omega$ die normierten Anteile sind.

**Interpretation:**

$H$ misst **Konzentration vs. Verteilung** der Primfaktoren auf Restklassen.

**Mathematische Äquivalenz:**
- **Simpson-Index** (Ökologie): $\lambda = \sum_i p_i^2$
- **Herfindahl-Hirschman-Index** (Ökonomie): $\text{HHI} = \sum_i p_i^2$
- **Rényi-Entropie** (Ordnung 2): $H_2 = -\log(\sum_i p_i^2)$

**Wertebereich:**

$$H \in \left[\frac{1}{4}, 1\right]$$

- **$H = 1$:** Maximale Konzentration (alle Faktoren in einer Klasse)
- **$H = 1/4$:** Maximale Gleichverteilung

**Vorteil:**

$H$ ist **dimensionslos** und vergleicht Zahlen mit unterschiedlichem $\Omega$ sauber.

**Status:**
- ✅ Vollständig dokumentiert in `theory/concentration_measure.md`
- ✅ Als M3* in E02 integriert

---

### Säule 3: ΔR²_X — Universeller Standard

$$\boxed{\Delta R^2_X = R^2(X \text{ hinzugefügt}) - R^2(\text{Basis}) > \eta}$$

**Problem:**

Früher: "Korreliert X mit Y?"

Das ist gefährlich, weil praktisch alles mit genügend Freiheitsgraden irgendwann korreliert.

**Lösung:**

**Jetzt:** "Erklärt X zusätzliche Varianz über Y hinaus?"

**Die Modellkaskade M0-M4:**

```
M0:  M_C ~ Ω
M0b: M_C ~ Ω + Ω²
M1:  M_C ~ Ω + Ω² + σ
M2:  M_C ~ Ω + Ω² + (v₂, v₃)
M3:  M_C ~ Ω + Ω² + (v₂, v₃) + ||v||²
M3*: M_C ~ Ω + Ω² + (v₂, v₃) + H
M4:  M_C ~ Ω + Ω² + (v₂, v₃) + v
```

**Die Δ-Werte:**

$$\Delta_{\text{quad}} = R^2(\text{M0b}) - R^2(\text{M0})$$

$$\Delta_{\text{shell}} = R^2(\text{M2}) - R^2(\text{M0b})$$

$$\Delta_{\text{norm}} = R^2(\text{M3}) - R^2(\text{M2})$$

$$\Delta_H = R^2(\text{M3*}) - R^2(\text{M2})$$

$$\Delta_{\text{dir}} = R^2(\text{M4}) - R^2(\text{M3})$$

**Interpretation:**

- **$\Delta_{\text{quad}} > 0.05$:** Nichtlineare $\Omega$-Effekte sind relevant
- **$\Delta_{\text{norm}} > 0.05$:** Norm hat Zusatzinfo (H0.6 bestätigt)
- **$\Delta_H > 0.05$:** Dimensionslose Konzentration funktioniert
- **$\Delta_{\text{dir}} > \Delta_{\text{norm}}$:** Vektorrichtung wichtiger als Konzentration
- **$R^2(\text{M4}) < 0.95$:** Echte Catalan-Residuen bleiben

**Universelle Anwendung:**

**Jede neue Idee** (Catalan, Tamari, Hurwitz, Collatz, Fibonacci-Zeta, ...) wird am selben Standard gemessen:

$$\text{Erklärt sie } \Delta R^2 > \eta \text{ ?}$$

Falls **nein:** Die Idee ist redundant zu bereits vorhandenen Ebenen.

Falls **ja:** Die Idee wird in die Hierarchie integriert.

**Status:**
- ✅ In E02 als Testkaskade implementiert
- ✅ Als universelles Testprinzip etabliert

---

## Warum diese drei Säulen transformativ sind

### 1. Wissenschaftliche Ehrlichkeit

**Vorher:** Implizite Annahme, dass jede Korrelation interessant ist.

**Nachher:** Expliziter Test, ob Korrelation zusätzliche Information liefert.

---

### 2. Kumulatives Programm

**Vorher:** Sammlung von Hypothesen ohne klare Hierarchie.

**Nachher:** Jede Ebene baut auf der vorherigen auf und wird empirisch validiert.

---

### 3. Falsifizierbarkeit

**Vorher:** "Catalan-Magic korreliert mit Norm" — schwer zu widerlegen.

**Nachher:** "$\Delta R^2_{\text{norm}} > 0.05$" — klar testbar, klar widerlegbar.

---

## Die Informationshierarchie

$$
\begin{align*}
\text{Ebene 0:} \quad & n \in \mathbb{N} \\
\text{Ebene 1:} \quad & \Omega(n), \Omega(n)^2 \\
\text{Ebene 2:} \quad & (v_2(n), v_3(n)) \\
\text{Ebene 3:} \quad & v_{\text{fac}}(n) = (e, a, b, c) \\
\text{Ebene 4:} \quad & H(n) = ||v||^2 / \Omega^2 \\
\text{Ebene 5:} \quad & T(n) \text{ (Catalan-Baum)} \\
\text{Ebene 6:} \quad & M_C(n) \text{ (Catalan-Magic)}
\end{align*}
$$

**Jede Ebene wird gegen die vorherigen getestet:**

$$\Delta R^2_i = R^2(\text{bis Ebene } i) - R^2(\text{bis Ebene } i-1)$$

---

## Anwendung auf andere Ideen

### Beispiel: Fibonacci-Zeta-Kopplung

**Alte Frage:** "Korreliert $M_C$ mit Fibonacci-Zeta-Residuen?"

**Neue Frage:**

$$\Delta R^2_{\text{Fib}} = R^2(M0, ..., M4, \zeta_F) - R^2(M0, ..., M4) > \eta \, ?$$

**Erst wenn $\Delta R^2_{\text{Fib}}$ signifikant ist, wird Fibonacci-Zeta in die Hierarchie integriert.**

---

### Beispiel: Hurwitz-Assoziatoren

**Alte Frage:** "Gibt es eine Oktonionen-Struktur in Catalan-Bäumen?"

**Neue Frage:**

Nach M0-M4, falls Catalan-Residuen bleiben:

$$\Delta R^2_{\text{Hurwitz}} = R^2(..., M_C, [a,b,c]_{\mathbb{O}}) - R^2(..., M_C) > \eta \, ?$$

**Erst wenn M0-M4 überhaupt Residuen lässt, macht Hurwitz Sinn.**

---

## Zusammenfassung

Die drei Säulen transformieren das Projekt von einer **explorativen Sammlung** zu einem **kumulativen Forschungsprogramm**:

1. **M0b:** Schützt vor nichtlinearen Artefakten
2. **H(n):** Dimensionslose, vergleichbare Konzentration
3. **ΔR²:** Universeller Standard für zusätzliche Information

**Das zentrale Prinzip:**

$$\boxed{\text{Erklärt } X \text{ zusätzliche Varianz?}}$$

**Das zentrale Motto:**

$$\boxed{\text{Nicht neue Objekte, sondern zusätzliche Informationsstufen.}}$$

---

## Status

- ✅ **M0b:** In E02 implementiert
- ✅ **H(n):** Vollständig dokumentiert
- ✅ **ΔR²:** Als Testkaskade etabliert
- ✅ **Hierarchie-Axiom:** Etabliert

**Das Programm ist methodisch reif, empirisch noch offen.**

**Die stärkste Idee:** H(n) als dimensionslose Konzentration.

**Der entscheidende Test:** $R^2(\text{M4}) \stackrel{?}{>} 0.95$ oder $< 0.80$
