# Experiment 4: EABC-Information

## Ziel

Teste **Hypothese C3** (EABC-Kopplung):

Ist die Catalan-Hierarchie mit der EABC-Signatur korreliert?

$$I(M_C^{\mathrm{res}}; E(n) \mid \Omega(n)) \stackrel{?}{>} 0$$

---

## Daten

Ensemble von $N = 100{,}000$ Zahlen mit:

- Stratifizierung nach $\Omega(n) \in \{3, 4, 5, 6, 7, 8\}$
- Für jedes $n$:
  - $M_C^{\mathrm{res}}(n)$: Residuale Catalan-Magic
  - $E(n) = (\sigma_{12}(p_1), \ldots, \sigma_{12}(p_k))$: EABC-Signatur

---

## Implementierung

### Phase 1: EABC-Kodierung

Für jede Zahl $n$ mit $\Omega(n) = k$:

1. Berechne EABC-Signatur:

   $$E(n) = (\sigma_{12}(p_1), \ldots, \sigma_{12}(p_k)) \in \{E, A, B, C\}^k$$

2. Kodiere als Integer:

   $$\text{EABC}_{\text{code}}(n) = \sum_{i=1}^k \sigma_i \cdot 4^{i-1}$$

   wobei $\sigma_i \in \{0, 1, 2, 3\}$ für $\{E, A, B, C\}$.

---

### Phase 2: Mutual Information

Für jedes $k$ separat berechne:

$$I(M_C^{\mathrm{res}}; E \mid \Omega = k)$$

**Diskretisierung:**

- Binne $M_C^{\mathrm{res}}$ in 10 Quantile
- EABC-Signatur ist bereits diskret

**Formel:**

$$I(X; Y) = \sum_{x, y} P(x, y) \log \frac{P(x, y)}{P(x) P(y)}$$

---

### Phase 3: Permutationstest

**Nullhypothese:** $I = 0$ (Unabhängigkeit)

**Test:**

1. Berechne originale Mutual Information $I_0$
2. Für $N_{\text{perm}} = 1000$ Permutationen:
   - Permutiere EABC-Labels **innerhalb** jeder $k$-Klasse
   - Berechne $I_{\text{perm}}$
3. $p$-Wert:

   $$p = \frac{1}{N_{\text{perm}}} \sum_{i=1}^{N_{\text{perm}}} \mathbb{1}[I_{\text{perm},i} \geq I_0]$$

**Kriterium:** $I_0 > 0.01$ bits und $p < 0.05$

---

## Code-Skelett

```python
from sklearn.metrics import mutual_info_score

def experiment_4_eabc_information(numbers, residuals):
    results_by_k = {}
    
    for k in range(3, 9):
        # Filter nach Omega
        mask = np.array([omega(n) for n in numbers]) == k
        n_k = np.array(numbers)[mask]
        res_k = np.array(residuals)[mask]
        
        # EABC-Signatur
        eabc_codes = [eabc_signature_code(n) for n in n_k]
        
        # Diskretisiere Residuen
        res_binned = pd.cut(res_k, bins=10, labels=False)
        
        # Mutual Information
        I_original = mutual_info_score(res_binned, eabc_codes)
        
        # Permutationstest
        I_permuted = []
        for _ in range(1000):
            eabc_perm = np.random.permutation(eabc_codes)
            I_perm = mutual_info_score(res_binned, eabc_perm)
            I_permuted.append(I_perm)
        
        # p-Wert
        p_value = np.mean([I_p >= I_original for I_p in I_permuted])
        
        results_by_k[k] = {
            'I': I_original,
            'I_perm_mean': np.mean(I_permuted),
            'I_perm_std': np.std(I_permuted),
            'p_value': p_value,
            'significant': I_original > 0.01 and p_value < 0.05
        }
    
    # Gewichteter Durchschnitt über k
    I_weighted = np.average(
        [results_by_k[k]['I'] for k in range(3, 9)],
        weights=[np.sum(np.array([omega(n) for n in numbers]) == k) 
                 for k in range(3, 9)]
    )
    
    return {
        'results_by_k': results_by_k,
        'I_weighted': I_weighted,
        'significant': I_weighted > 0.01
    }
```

---

## Erwartete Resultate

### Szenario A: EABC-gekoppelt

- $I \gtrsim 0.02$ bits
- $p < 0.05$

**Interpretation:** Die EABC-Signatur beeinflusst die Catalan-Hierarchie.

---

### Szenario B: EABC-ungekoppelt

- $I \lesssim 0.005$ bits
- $p \gtrsim 0.3$

**Interpretation:** Lokale und globale Ebene sind separierbar.

---

## Visualisierung

1. **Barplot:** $I(k)$ für jedes $k$ mit Fehlerbalken (Permutationsverteilung)
2. **Heatmap:** $P(M_C^{\mathrm{res}}, E)$ für ein repräsentatives $k$
3. **Scatterplot:** $M_C^{\mathrm{res}}$ vs. EABC-Komplexität

---

## Erweiterte Tests

### Test 4a: Chi-Quadrat-Test

Für jede EABC-Klasse teste:

$$\chi^2 = \sum_{\text{bins}} \frac{(O_i - E_i)^2}{E_i}$$

wobei $O_i$ die beobachtete Häufigkeit von $M_C^{\mathrm{res}}$ ist.

---

### Test 4b: Konditionaler Erwartungswert

Berechne:

$$\mathbb{E}[M_C^{\mathrm{res}} \mid E(n) = s]$$

für jede Signatur $s \in \{E, A, B, C\}^k$.

**Test:** Variieren die Erwartungswerte signifikant über $s$?

---

## Deliverables

1. **Tabelle:** Mutual Information für jedes $k$
2. **Plots:** Barplot und Heatmap
3. **JSON:** `eabc_coupling.json` mit allen $p$-Werten

---

## Zeitaufwand

- **EABC-Kodierung:** 1 Tag
- **Mutual Information:** 1 Tag
- **Permutationstest:** 1 Tag
- **Visualisierung:** 1 Tag

**Total:** ~4 Tage

---

## Kritisches Kriterium

Falls **Szenario B** eintritt ($I < 0.005$):

→ Die lokale und globale Ebene sind **entkoppelt**. Tensorprodukt-Ansatz ist nicht gerechtfertigt.
