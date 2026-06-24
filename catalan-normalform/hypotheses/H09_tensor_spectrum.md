# Hypothese C9: Tensor-Spektrum

## Formulierung

Für den gekoppelten Operator

$$H_{\mathrm{tot}}^{(k)} = \alpha \, D_{\mathrm{loc}} \otimes I + \beta \, I \otimes L_C^{(k)} + \gamma \, V_{\mathrm{couple}}$$

gibt es ein **Übergangsregime** bei $\alpha \approx \beta$, in dem spektrale Mischungen maximal sind.

**Hypothese:** Das Inverse Participation Ratio (IPR) hat ein **Extremum** bei:

$$\frac{\alpha}{\beta} \approx 1$$

---

## Interpretation

- Bei $\alpha \gg \beta$: Spektrum dominiert von lokaler EABC-Struktur
- Bei $\beta \gg \alpha$: Spektrum dominiert von Catalan-Struktur
- Bei $\alpha \approx \beta$: **Maximale Mischung** beider Ebenen

**Analogie:** Phasenübergang in gekoppelten Systemen.

---

## Nullmodell

**H0:** Kein Extremum, monotones Verhalten:

$$\mathrm{IPR}(\alpha/\beta) \text{ ist monoton}$$

---

## Teststatistik

Für ein festes $k$ und $\gamma = 1$:

1. Variiere $\alpha/\beta \in [0.01, 0.1, 0.5, 1, 2, 10, 100]$
2. Berechne für jeden Wert:

   $$\overline{\mathrm{IPR}}(\alpha/\beta) = \frac{1}{\dim \mathcal{H}_k} \sum_j \mathrm{IPR}(\psi_j)$$

3. Finde Minimum oder Maximum:

   $$\left(\frac{\alpha}{\beta}\right)^* = \arg\min_{\alpha/\beta} \overline{\mathrm{IPR}}(\alpha/\beta)$$

**Kriterium:**

$$0.5 \leq \left(\frac{\alpha}{\beta}\right)^* \leq 2$$

---

## Implementierung

```python
def test_tensor_spectrum(k=4, gamma=1.0):
    # Operatoren
    D_loc = construct_local_operator()
    L_C = construct_catalan_laplacian(k)
    V_couple = construct_coupling_operator(k)
    
    # Hilbertraum
    dim_loc = D_loc.shape[0]
    dim_cat = L_C.shape[0]
    
    ratios = [0.01, 0.1, 0.5, 1.0, 2.0, 10.0, 100.0]
    IPR_values = []
    
    for ratio in ratios:
        alpha = ratio
        beta = 1.0
        
        # Gekoppelter Hamiltonian
        H_tot = (alpha * np.kron(D_loc, np.eye(dim_cat)) +
                 beta * np.kron(np.eye(dim_loc), L_C) +
                 gamma * V_couple)
        
        # Eigenvektoren
        eigvals, eigvecs = np.linalg.eigh(H_tot)
        
        # Mittleres IPR
        IPR_mean = np.mean([
            np.sum(eigvecs[:, j]**4) / np.sum(eigvecs[:, j]**2)**2
            for j in range(eigvecs.shape[1])
        ])
        
        IPR_values.append(IPR_mean)
    
    # Finde Extremum
    idx_min = np.argmin(IPR_values)
    ratio_opt = ratios[idx_min]
    
    return {
        'ratios': ratios,
        'IPR_values': IPR_values,
        'optimal_ratio': ratio_opt,
        'valid': 0.5 <= ratio_opt <= 2.0
    }
```

---

## Erwartetes Resultat

- **Falls Übergangsregime existiert:** IPR-Minimum bei $\alpha/\beta \approx 1$
- **Falls nicht:** Monotones Verhalten

---

## Konsequenzen

- **Signifikant:** Die beiden Ebenen sind optimal gekoppelt bei gleicher Gewichtung
- **Nicht signifikant:** Eine Ebene dominiert stets

---

## Erweiterte Tests

### Test 9a: Variation von $\gamma$

Teste das Phasendiagramm in $(\alpha/\beta, \gamma)$-Ebene:

- Für $\gamma = 0$: ungekoppeltes System
- Für $\gamma \gg 1$: stark gekoppeltes System

**Hypothese:** Übergangsregime wird bei größerem $\gamma$ schärfer.

---

### Test 9b: Spektrale Lücke

Teste auch die **Spektrallücke**:

$$\Delta(\alpha/\beta) = \lambda_1 - \lambda_0$$

**Hypothese:** Minimum bei $\alpha/\beta \approx 1$ (kritischer Punkt).

---

### Test 9c: Von-Neumann-Entropie

Berechne die **Verschränkungsentropie** zwischen lokaler und globaler Ebene:

$$S_{\mathrm{ent}}(\alpha/\beta) = S(\rho_{\mathrm{loc}})$$

für den Grundzustand.

**Hypothese:** Maximum bei $\alpha/\beta \approx 1$.

---

## Literatur

- Inverse Participation Ratio: Evers & Mirlin (2008)
- Quantum phase transitions: Sachdev (2011), *Quantum Phase Transitions*.
