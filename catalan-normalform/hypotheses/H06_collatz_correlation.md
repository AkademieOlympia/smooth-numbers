# Hypothese C6: Collatz-Catalan-Korrelation

## Formulierung

Sei $\tau(n)$ die **Collatz-Stopzeit**. Nach Entfernung der trivialen Größenabhängigkeit gilt:

$$\operatorname{corr}\left(M_C^{\mathrm{res}}(n), \tau^{\mathrm{res}}(n)\right) \neq 0$$

wobei:

$$\tau^{\mathrm{res}}(n) = \tau(n) - \mathbb{E}[\tau(n) \mid \log_2 n, \Omega(n)]$$

---

## Interpretation

Die Collatz-Stopzeit ist eine **dynamische** Observable, die die iterative Struktur einer Zahl misst.

**Hypothese:** Die **statische** Faktorhierarchie (Catalan) korreliert mit der **dynamischen** Collatz-Komplexität.

---

## Nullmodell

**H0:** Beide Größen sind **unabhängig** nach Kontrolle für $\log n$ und $\Omega(n)$:

$$\operatorname{corr}(\tau^{\mathrm{res}}, M_C^{\mathrm{res}}) = 0$$

**Permutationstest:** Permutiere Catalan-Bäume bei festem $\Omega(n)$ und fester Signatur.

---

## Teststatistik

Für ein Ensemble $\mathcal{N}$:

$$\rho = \operatorname{corr}\left(\{M_C^{\mathrm{res}}(n_i)\}, \{\tau^{\mathrm{res}}(n_i)\}\right)$$

**Residualisierung:**

1. Fitte $\tau(n) \sim f(\log n, \Omega(n))$ via Regression
2. Berechne $\tau^{\mathrm{res}}(n) = \tau(n) - \hat{f}(n)$
3. Analog für $M_C$

**Kriterium:**

$$|\rho| > 0.15 \quad \text{und} \quad p < 0.05$$

---

## Implementierung

```python
def test_collatz_correlation(numbers, n_permutations=1000):
    # Berechne Collatz-Stopzeiten
    tau = [collatz_stopping_time(n) for n in numbers]
    
    # Residualisierung: tau ~ log(n) + Omega(n)
    X = np.column_stack([np.log2(numbers), [omega(n) for n in numbers]])
    model = LinearRegression().fit(X, tau)
    tau_res = tau - model.predict(X)
    
    # Catalan-Residuen
    M_catalan_res = [catalan_magic_residual(n) for n in numbers]
    
    # Originale Korrelation
    rho_original = np.corrcoef(M_catalan_res, tau_res)[0,1]
    
    # Permutationstest
    rho_permuted = []
    for _ in range(n_permutations):
        M_perm = permute_catalan_trees(M_catalan_res, numbers)
        rho_perm = np.corrcoef(M_perm, tau_res)[0,1]
        rho_permuted.append(rho_perm)
    
    # p-Wert
    p_value = np.mean([abs(rho_perm) >= abs(rho_original) 
                       for rho_perm in rho_permuted])
    
    return {
        'rho': rho_original,
        'p_value': p_value,
        'significant': abs(rho_original) > 0.15 and p_value < 0.05
    }
```

---

## Erwartetes Resultat

**Zwei Szenarien:**

### Szenario A: Positive Korrelation

$$\rho > 0$$

**Interpretation:** Asymmetrische Hierarchie → längere Collatz-Stopzeit

---

### Szenario B: Negative Korrelation

$$\rho < 0$$

**Interpretation:** Asymmetrische Hierarchie → kürzere Collatz-Stopzeit (schnellerer Kollaps)

---

## Konsequenzen

- **Signifikant:** Die Faktorarchitektur beeinflusst die Collatz-Dynamik
- **Nicht signifikant:** Collatz-Stopzeit hängt nur von lokalen Eigenschaften ab

---

## Erweiterte Tests

### Test 6a: Gleitzeit-Korrelation

Teste auch die **Gleitzeit** (gliding time):

$$\operatorname{corr}(M_C^{\mathrm{res}}, T_{\mathrm{glide}}^{\mathrm{res}})$$

---

### Test 6b: Stratifizierung nach 2-adischer Bewertung

Da Collatz stark von $v_2(n)$ abhängt, stratifiziere nach:

$$v_2(n) = \max\{k : 2^k \mid n\}$$

Teste die Korrelation **innerhalb** jeder $v_2$-Klasse.

---

## Literatur

- Collatz conjecture: Lagarias (1985), *The 3x+1 problem and its generalizations*.
- Collatz-EABC-Verbindung: Siehe `../eabc-qubit/collatz_quantum_paper.pdf`.
