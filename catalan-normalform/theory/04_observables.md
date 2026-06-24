# Kapitel 4: Observablen und Catalan-Magic

## 4.1 Motivation

Wir definieren jetzt **messbare Größen**, die die Catalan-Hierarchie quantifizieren.

**Ziel:** Observable, die:

1. **Geometrisch interpretierbar** sind
2. **Numerisch berechenbar** sind
3. **Arithmetische Information** enthalten

---

## 4.2 Distanz-basierte Magic

### Definition 4.1: Geometrische Catalan-Magic

Für eine Kanonisierung $\kappa: \mathbb{N}_{\geq 2} \to \bigcup_k \mathcal{T}_k$ definieren wir:

$$M_C^\kappa(n) = \min_{B \in \mathcal{B}_{\Omega(n)}} d_C(\kappa(n), B)$$

**Interpretation:**

- $M_C^\kappa(n) = 0$: $\kappa(n)$ ist bereits balanciert
- Großes $M_C^\kappa(n)$: stark asymmetrische Hierarchie

**Normierung:**

$$\tilde{M}_C^\kappa(n) = \frac{M_C^\kappa(n)}{\operatorname{diam}(\Gamma_{\Omega(n)})} = \frac{M_C^\kappa(n)}{\binom{\Omega(n)}{2}}$$

---

### Beispiel 4.1: $k=4$ Faktoren

Für $\Omega(n) = 4$ gibt es $C_3 = 5$ Bäume:

1. $T_1 = ((((ab)c)d)) \quad \leadsto \quad d_C(T_1, \mathcal{B}_4) = ?$
2. $T_2 = (((a(bc))d)) \quad \leadsto \quad d_C(T_2, \mathcal{B}_4) = ?$
3. $T_3 = ((ab)(cd)) \quad \leadsto \quad d_C(T_3, \mathcal{B}_4) = 0$ (balanciert!)
4. $T_4 = ((a((bc)d))) \quad \leadsto \quad d_C(T_4, \mathcal{B}_4) = ?$
5. $T_5 = (a(b(cd))) \quad \leadsto \quad d_C(T_5, \mathcal{B}_4) = ?$

---

## 4.3 Ensemble-Magic

### Definition 4.2: Ensemble-Mittelung

Da die Kanonisierung willkürlich ist, definieren wir die **Ensemble-Magic:**

$$\overline{M}_C(k) = \frac{1}{|\mathcal{T}_k|} \sum_{T \in \mathcal{T}_k} \min_{B \in \mathcal{B}_k} d_C(T, B)$$

**Eigenschaften:**

- Hängt nur von $k = \Omega(n)$ ab, **nicht** von den konkreten Primfaktoren
- Baseline-Term für strukturelle Komplexität
- Kann vorab für alle $k$ berechnet werden

---

### Definition 4.3: Residuale Catalan-Magic

$$M_C^{\mathrm{res}}(n) = M_C^\kappa(n) - \mathbb{E}[M_C^\kappa(n) \mid \Omega(n)]$$

Dies ist die **arithmetische Abweichung** vom Erwartungswert bei gegebenem $\Omega(n)$.

**Zentrale Frage:**

$$\boxed{M_C^{\mathrm{res}}(n) \stackrel{?}{\neq} 0 \quad \text{und enthält arithmetische Information?}}$$

---

## 4.4 Gewichtete Catalan-Magic

### Definition 4.4: Gewichte

Um die konkreten Primfaktoren einzubeziehen, definiert man ein Gewicht:

$$w_n: \mathcal{T}_k \to \mathbb{R}_{\geq 0}, \qquad \sum_{T \in \mathcal{T}_k} w_n(T) = 1$$

basierend auf der Faktorstruktur von $n$.

---

### Definition 4.5: Gewichtete Catalan-Magic

$$M_C^w(n) = \sum_{T \in \mathcal{T}_k} w_n(T) \cdot \min_{B \in \mathcal{B}_k} d_C(T, B)$$

**Natürliche Gewichtungen:**

#### 1. Gleichverteilung (Ensemble)

$$w_n^{\mathrm{unif}}(T) = \frac{1}{|\mathcal{T}_k|}$$

Liefert $\overline{M}_C(k)$.

#### 2. EABC-Energie-Gewichtung

$$w_n^{\mathrm{EABC}}(T) \propto \exp\left(-\lambda \, E_{\mathrm{EABC}}(T)\right)$$

wobei $E_{\mathrm{EABC}}(T)$ die EABC-Signatur der Teilbäume bewertet.

#### 3. Multiplikative Energie

$$w_n^{\log}(T) \propto \exp\left(-\lambda \, E_{\log}(T)\right)$$

wobei

$$E_{\log}(T) = \sum_{v \in \mathrm{Internal}(T)} \left|\log\left(\prod_{p \in L_v} p\right) - \log\left(\prod_{p \in R_v} p\right)\right|$$

die Balance der Teilprodukte misst.

---

## 4.5 Spektrale Catalan-Magic

### Definition 4.6: Spektrale Projektion

Für einen Baum $T \in \mathcal{T}_k$ und einen Schwellenwert $\varepsilon > 0$ definieren wir:

$$M_{C,\varepsilon}^{\mathrm{spec}}(T) = \sum_{\lambda_j^{(k)} < \varepsilon} \left|\phi_j^{(k)}(T)\right|^2$$

**Interpretation:**

- Misst, wie stark $T$ in **niedrigfrequenten Moden** des Laplace-Operators $L_C^{(k)}$ repräsentiert ist
- Große $M_{C,\varepsilon}^{\mathrm{spec}}(T)$: $T$ liegt in global kohärenten Regionen

---

### Definition 4.7: Hochfrequente spektrale Magic

$$M_{C,\varepsilon}^{\mathrm{high}}(T) = \sum_{\lambda_j^{(k)} > \varepsilon} \left|\phi_j^{(k)}(T)\right|^2$$

**Interpretation:**

- Misst **lokale Komplexität**
- Große $M_{C,\varepsilon}^{\mathrm{high}}(T)$: $T$ liegt in lokal irregulären Regionen

---

## 4.6 Höhen-basierte Observable

### Definition 4.8: Normierte Baumhöhe

$$h_{\mathrm{norm}}(T) = \frac{h(T) - \lceil \log_2 k \rceil}{\binom{k}{2}}$$

wobei:

- Zähler: Abweichung von minimaler Höhe
- Nenner: Durchmesser von $\Gamma_k$

**Eigenschaften:**

$$0 \leq h_{\mathrm{norm}}(T) \leq 1$$

mit:

- $h_{\mathrm{norm}}(T_B) = 0$ (balanciert)
- $h_{\mathrm{norm}}(T_L) = h_{\mathrm{norm}}(T_R) \approx 1$ (maximal unbalanciert)

---

## 4.7 Krümmungs-Observable

### Definition 4.9: Mittlere Krümmung

Für einen Baum $T \in \mathcal{T}_k$ definieren wir:

$$\bar{\kappa}(T) = \frac{1}{|\mathrm{Edges}(T)|} \sum_{e \in \mathrm{Edges}(T)} \kappa(e)$$

wobei $\kappa$ die Ollivier-Ricci- oder Forman-Krümmung ist.

**Hypothese:** Asymmetrische Bäume haben **negativere** mittlere Krümmung.

---

## 4.8 Zusammenfassung der Observablen

| Observable | Symbol | Typ | Interpretation |
|------------|--------|-----|----------------|
| Geometrische Magic | $M_C^\kappa(n)$ | Distanz | Abstand zu balancierten Bäumen |
| Ensemble-Magic | $\overline{M}_C(k)$ | Erwartungswert | Baseline für $\Omega(n) = k$ |
| Residuale Magic | $M_C^{\mathrm{res}}(n)$ | Residuum | Arithmetische Abweichung |
| Spektrale Magic | $M_{C,\varepsilon}^{\mathrm{spec}}(T)$ | Projektion | Niedrigfrequente Moden |
| Normierte Höhe | $h_{\mathrm{norm}}(T)$ | Skaliert | Balance-Maß |
| Mittlere Krümmung | $\bar{\kappa}(T)$ | Geometrisch | Lokale Geometrie |

---

## 4.9 Nächste Schritte

**Kapitel 5** definiert die **Kopplung** zwischen lokaler EABC-Geometrie und globaler Catalan-Geometrie.

---

## Literatur

- Inverse Participation Ratio: Evers & Mirlin (2008)
- Spectral graph theory: Chung (1997)
