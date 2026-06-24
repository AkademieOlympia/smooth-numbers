# Kapitel 3: Globale Catalan-Geometrie

## 3.1 Motivation

Die **globale Ebene** beschreibt die **Architektur** einer Zahl:

- Wie sind die Primfaktoren hierarchisch verschaltet?
- Welche Baumstruktur bilden sie?

---

## 3.2 Tamari-Gitter

### Definition 3.1: Tamari-Rotation

Zwei binäre Bäume $T_1, T_2 \in \mathcal{T}_k$ sind durch eine **Tamari-Rotation** verbunden, wenn sie sich durch eine Neuassoziierung unterscheiden:

$$((AB)C) \quad \longleftrightarrow \quad (A(BC))$$

**Lokal:** An einem internen Knoten wird die Klammerung umgedreht.

---

### Definition 3.2: Tamari-Graph

Der **Tamari-Graph** ist:

$$\Gamma_k = (\mathcal{T}_k, E_k)$$

wobei:

- **Knoten:** $\mathcal{T}_k$ (alle binären Bäume mit $k$ Blättern)
- **Kanten:** $E_k = \{(T_1, T_2) : T_1 \leftrightarrow T_2 \text{ durch Rotation}\}$

---

### Satz 3.1: Eigenschaften des Tamari-Graphen

1. $|\mathcal{T}_k| = C_{k-1}$ (Catalan-Zahl)
2. $\Gamma_k$ ist **zusammenhängend**
3. $\Gamma_k$ ist das Hasse-Diagramm einer **Partialordnung** (Tamari-Ordnung)
4. $\Gamma_k$ ist das **1-Skelett des Associahedrons** $K_{k-1}$

---

### Definition 3.3: Tamari-Metrik

Die **Tamari-Metrik** ist die Graphdistanz:

$$d_C(T_1, T_2) = \operatorname{dist}_{\Gamma_k}(T_1, T_2)$$

minimale Anzahl von Rotationen, um $T_1$ in $T_2$ zu überführen.

**Eigenschaften:**

- $d_C(T_1, T_2) \geq 0$
- $d_C(T_1, T_2) = 0 \iff T_1 = T_2$
- Dreiecksungleichung erfüllt

---

## 3.3 Extremale Bäume

### Definition 3.4: Linksbaum und Rechtsbaum

Der **Linksbaum** $T_L \in \mathcal{T}_k$ ist maximal linkslastig:

$$T_L = ((\cdots((p_1 p_2) p_3) \cdots) p_k)$$

Der **Rechtsbaum** $T_R \in \mathcal{T}_k$ ist maximal rechtslastig:

$$T_R = (p_1 (p_2 (\cdots (p_{k-1} p_k))))$$

---

### Satz 3.2: Durchmesser von $\Gamma_k$

$$d_C(T_L, T_R) = \binom{k}{2} = \frac{k(k-1)}{2}$$

Dies ist der **Durchmesser** von $\Gamma_k$:

$$\operatorname{diam}(\Gamma_k) = \binom{k}{2}$$

---

### Definition 3.5: Balancierte Bäume

Ein Baum $T \in \mathcal{T}_k$ heißt **balanciert**, wenn seine Höhe minimal ist:

$$h(T) = \lceil \log_2 k \rceil$$

Die Menge balancierter Bäume ist:

$$\mathcal{B}_k = \{T \in \mathcal{T}_k : h(T) = \lceil \log_2 k \rceil\}$$

**Eigenschaft:**

$$|\mathcal{B}_k| \geq 1$$

mit Gleichheit nur für $k = 2^m$.

---

## 3.4 Spektrale Struktur

### Definition 3.6: Catalan-Laplace-Operator

Der **Laplace-Operator** auf $\Gamma_k$ ist:

$$L_C^{(k)} = D_k - A_k$$

wobei:

- $A_k$: Adjazenzmatrix von $\Gamma_k$
- $D_k$: Gradmatrix ($D_{ii} = \deg(T_i)$)

Dimension:

$$L_C^{(k)}: \mathbb{R}^{C_{k-1}} \to \mathbb{R}^{C_{k-1}}$$

---

### Definition 3.7: Spektrum

Das **Spektrum** von $L_C^{(k)}$ ist:

$$\operatorname{Spec}(L_C^{(k)}) = \{0 = \lambda_0^{(k)} \leq \lambda_1^{(k)} \leq \cdots \leq \lambda_{C_{k-1}-1}^{(k)}\}$$

mit orthonormalen Eigenfunktionen:

$$\phi_j^{(k)}: \mathcal{T}_k \to \mathbb{R}$$

---

### Satz 3.3: Spektrallücke

Da $\Gamma_k$ zusammenhängend ist, gilt:

$$\lambda_0^{(k)} = 0 \quad \text{(einfach)}$$

$$\lambda_1^{(k)} > 0 \quad \text{(Spektrallücke)}$$

Die **Spektrallücke** $\lambda_1^{(k)}$ misst die Konnektivität von $\Gamma_k$.

---

## 3.5 Associahedron

### Definition 3.8: Associahedron

Das **Associahedron** $K_{k-1}$ ist ein $(k-2)$-dimensionales konvexes Polytop mit:

- **Ecken:** binäre Bäume ($\mathcal{T}_k$)
- **Kanten:** Tamari-Rotationen
- **2-Flächen:** Assoziativitäts-Pentagone

$\Gamma_k$ ist das 1-Skelett von $K_{k-1}$.

---

### Satz 3.4: Geometrische Realisierung

$K_{k-1}$ kann als konvexes Polytop im $\mathbb{R}^{k-1}$ realisiert werden.

**Koordinaten:** Jeder Baum $T$ erhält einen Punkt im Raum basierend auf Teilprodukten.

---

## 3.6 Diskrete Krümmung

### Definition 3.9: Ollivier-Ricci-Krümmung

Für eine Kante $(T_1, T_2) \in E_k$ definieren wir die **Ollivier-Ricci-Krümmung**:

$$\kappa_{OR}(T_1, T_2) = 1 - \frac{W(\mu_1, \mu_2)}{d_C(T_1, T_2)}$$

wobei $W$ die Wasserstein-Distanz zwischen lokalen Wahrscheinlichkeitsmaßen ist.

**Interpretation:**

- $\kappa > 0$: positive Krümmung (sphärisch)
- $\kappa = 0$: flach
- $\kappa < 0$: negative Krümmung (hyperbolisch)

---

### Definition 3.10: Forman-Ricci-Krümmung

Alternativ kann man die **Forman-Ricci-Krümmung** verwenden:

$$\kappa_F(e) = w(e) - \sum_{e' \sim e} \frac{w(e')}{\sqrt{\deg(e) \deg(e')}}$$

für Kanten $e \in E_k$.

---

## 3.7 Nächste Schritte

Die globale Catalan-Geometrie liefert die **Raumstruktur**.

**Kapitel 4** definiert die **Observablen**, die diese Struktur mit arithmetischen Eigenschaften verbinden.

---

## Literatur

- Huang, S., & Tamari, D. (1972). Problems of associativity.
- Loday, J.-L. (2004). Realization of the Stasheff polytope.
- Ollivier, Y. (2009). Ricci curvature of Markov chains on metric spaces.
- Forman, R. (2003). Bochner's method for cell complexes.
