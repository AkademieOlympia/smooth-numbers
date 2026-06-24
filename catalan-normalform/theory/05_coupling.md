# Kapitel 5: Tensorprodukt und Kopplung

## 5.1 Motivation

Die **vollständige Theorie** muss lokale und globale Ebene verbinden:

$$\text{EABC (lokal)} \quad \otimes \quad \text{Catalan (global)} \quad = \quad \text{Gekoppeltes System}$$

---

## 5.2 Tensorprodukt-Hilbertraum

### Definition 5.1: Gekoppelter Zustandsraum

Für eine gegebene Faktoranzahl $k = \Omega(n)$ ist der Zustandsraum:

$$\mathcal{H}_k = \mathcal{H}_{\mathrm{loc}} \otimes \ell^2(\mathcal{T}_k)$$

**Dimension:**

$$\dim \mathcal{H}_k = \phi(m) \cdot C_{k-1}$$

wobei:

- $\phi(m)$: Anzahl der EABC-Restklassen
- $C_{k-1}$: Anzahl der Catalan-Bäume

---

### Beispiel 5.1: Dimensionen

| $k$ | $\phi(420)$ | $C_{k-1}$ | $\dim \mathcal{H}_k$ |
|-----|-------------|-----------|----------------------|
| 2   | 96          | 1         | 96                   |
| 3   | 96          | 2         | 192                  |
| 4   | 96          | 5         | 480                  |
| 5   | 96          | 14        | 1344                 |
| 10  | 96          | 4862      | 466752               |

Das System skaliert **superpolynomiell** mit $k$.

---

## 5.3 Ungekoppelter Operator

### Definition 5.2: Ungekoppelter Hamiltonian

Ohne Kopplung ist der Operator:

$$H_0 = \alpha \, D_{\mathrm{loc}} \otimes I + \beta \, I \otimes L_C^{(k)}$$

wobei:

- $D_{\mathrm{loc}}$: Lokaler Dirac-Operator (EABC)
- $L_C^{(k)}$: Catalan-Laplace-Operator
- $\alpha, \beta \geq 0$: Kopplungskonstanten

**Eigenwerte:**

$$E_{i,j} = \alpha \lambda_i^{\mathrm{loc}} + \beta \lambda_j^{(k)}$$

Tensorprodukt-Struktur: Die Eigenzustände faktorisieren.

---

## 5.4 Kopplungsterm

### Definition 5.3: Arithmetischer Kopplungsoperator

$$V_{\mathrm{couple}}: \mathcal{H}_k \to \mathcal{H}_k$$

muss die **EABC-Signatur** der Blätter mit der **Baumstruktur** verbinden.

---

### Ansatz 5.1: Interne-Knoten-Kopplung

Für einen Baum $T \in \mathcal{T}_k$ mit internen Knoten $\mathrm{Internal}(T)$ definieren wir:

$$V_{\mathrm{couple}}(T) = \sum_{v \in \mathrm{Internal}(T)} F(\sigma_{12}(L_v), \sigma_{12}(R_v))$$

wobei:

- $L_v$: Linker Teilbaum an Knoten $v$
- $R_v$: Rechter Teilbaum an Knoten $v$
- $\sigma_{12}(L_v)$: EABC-Signatur der Blätter im linken Teilbaum
- $F: \{E,A,B,C\}^{*} \times \{E,A,B,C\}^{*} \to \mathbb{R}$: Kopplungsfunktion

---

### Ansatz 5.2: Faktorprodukt-Kopplung

$$V_{\mathrm{couple}}(T) = \sum_{v \in \mathrm{Internal}(T)} \left|\log\left(\prod_{p \in L_v} p\right) - \log\left(\prod_{p \in R_v} p\right)\right|$$

**Interpretation:** Belohnt balancierte Teilprodukte.

---

### Ansatz 5.3: EABC-Distanz-Kopplung

Für jeden internen Knoten $v$ berechnen wir die **EABC-Distanz** zwischen linkem und rechtem Teilbaum:

$$d_{\mathrm{EABC}}(L_v, R_v) = \sum_{p \in L_v} \sum_{q \in R_v} d(\sigma_{12}(p), \sigma_{12}(q))$$

wobei $d: \{E,A,B,C\}^2 \to \mathbb{R}$ eine Metrik ist.

Dann:

$$V_{\mathrm{couple}}(T) = \sum_{v \in \mathrm{Internal}(T)} d_{\mathrm{EABC}}(L_v, R_v)$$

---

## 5.5 Gekoppelter Hamiltonian

### Definition 5.4: Vollständiger Operator

$$\boxed{H_{\mathrm{tot}}^{(k)} = \alpha \, D_{\mathrm{loc}} \otimes I + \beta \, I \otimes L_C^{(k)} + \gamma \, V_{\mathrm{couple}}}$$

mit $\alpha, \beta, \gamma \geq 0$.

**Grenzfälle:**

| Regime | Werte | Verhalten |
|--------|-------|-----------|
| Rein lokal | $\beta = \gamma = 0$ | Nur EABC-Restklassen |
| Rein global | $\alpha = \gamma = 0$ | Nur Catalan-Struktur |
| Ungekoppelt | $\gamma = 0$ | Tensorprodukt |
| Stark gekoppelt | $\gamma \gg \alpha, \beta$ | Dominante Hierarchie |

---

## 5.6 Spektrale Observablen

### Definition 5.5: Inverse Participation Ratio

Für einen Eigenvektor $|\psi\rangle \in \mathcal{H}_k$ definieren wir:

$$\mathrm{IPR}(\psi) = \frac{\sum_i |\psi_i|^4}{\left(\sum_i |\psi_i|^2\right)^2}$$

**Interpretation:**

- $\mathrm{IPR} \approx 1/\dim \mathcal{H}_k$: maximale Delokalisation
- $\mathrm{IPR} \approx 1$: Lokalisation auf wenige Basiszustände

---

### Definition 5.6: Mittleres IPR

$$\overline{\mathrm{IPR}}(H) = \frac{1}{\dim \mathcal{H}_k} \sum_{j=1}^{\dim \mathcal{H}_k} \mathrm{IPR}(\psi_j)$$

über alle Eigenvektoren von $H$.

**Hypothese:** Bei $\alpha \approx \beta$ tritt **maximale Mischung** auf.

---

## 5.7 Mutual Information

### Definition 5.7: Quantenkorrelation

Für einen Eigenzustand $|\psi\rangle = \sum_{i,j} c_{ij} |i\rangle_{\mathrm{loc}} \otimes |j\rangle_C$ definieren wir:

$$I_{\mathrm{loc:cat}}(\psi) = S(\rho_{\mathrm{loc}}) + S(\rho_C) - S(\rho_{\mathrm{tot}})$$

wobei $S$ die Von-Neumann-Entropie ist.

**Interpretation:** Misst Verschränkung zwischen lokaler und globaler Ebene.

---

## 5.8 Kritische Fragen

### Frage 5.1: Existiert eine natürliche Kopplung?

Ist eine der Kopplungsfunktionen $F$ ausgezeichnet durch:

- **Arithmetische Prinzipien** (z.B. Multiplicativität)
- **Experimentelle Daten** (beste Korrelation mit Observablen)

---

### Frage 5.2: Gibt es Phasenübergänge?

Existiert ein kritisches Verhältnis $\alpha/\beta$ bei dem sich das Spektralverhalten qualitativ ändert?

---

### Frage 5.3: Ist die Kopplung messbar?

Kann man aus empirischen Daten (z.B. Collatz-Stopzeiten, Brody-Parameter) auf $\gamma \neq 0$ schließen?

---

## 5.9 Zusammenfassung

Die Tensorprodukt-Struktur erlaubt:

1. **Systematische Separation** von lokalem und globalem Anteil
2. **Quantitative Kopplungstests** via $\gamma$-Parameter
3. **Spektrale Signaturen** der Wechselwirkung

Die **Hypothesen** (Kapitel 6–15) testen diese Struktur.

---

## Literatur

- Tensor product spaces: Reed & Simon (1980), Methods of Modern Mathematical Physics.
- Spectral coupling: Haake (2010), Quantum Signatures of Chaos.
