# Experiment 5: Spektralvergleich

## Ziel

Teste **Hypothese C4** (Spektrale Korrelation):

Korreliert die spektrale Catalan-Magic mit vorhandenen EABC-Spektralobservablen?

$$\operatorname{corr}\left(M_{C,\varepsilon}^{\mathrm{spec}}(n), M_{\mathrm{near-zero}}(D_{420}, n)\right) \stackrel{?}{\neq} 0$$

---

## Vorbereitung

### Phase 0: Spektrale Catalan-Magic

Für jedes $k = 3, \ldots, 8$:

1. Berechne Laplace-Operator $L_C^{(k)}$ (aus **Experiment 1**)
2. Berechne Eigenwerte und Eigenvektoren:

   $$L_C^{(k)} \phi_j^{(k)} = \lambda_j^{(k)} \phi_j^{(k)}$$

3. Wähle Schwellenwert:

   $$\varepsilon_k = 0.1 \cdot \lambda_{\max}^{(k)}$$

4. Für jeden Baum $T \in \mathcal{T}_k$ berechne:

   $$M_{C,\varepsilon}^{\mathrm{spec}}(T) = \sum_{\lambda_j^{(k)} < \varepsilon_k} \left|\phi_j^{(k)}(T)\right|^2$$

**Output:** Tabelle `catalan_spectral_magic[k][T]`.

---

## Daten

Ensemble von $N = 100{,}000$ Zahlen mit:

- $M_{C,\varepsilon}^{\mathrm{spec}}(n)$: Spektrale Catalan-Magic
- $M_{\mathrm{near-zero}}(D_{420}, n)$: Near-zero-magic des EABC-Dirac-Operators

---

## Implementierung

### Phase 1: EABC-Spektralobservable

Für jede Zahl $n$:

1. Berechne EABC-Signatur modulo 420
2. Konstruiere lokalen Zustand:

   $$|\psi_n\rangle \in \mathcal{H}_{\mathrm{loc}} = \ell^2(\mathbb{Z}/420\mathbb{Z}^\times)$$

3. Berechne Near-zero-magic:

   $$M_{\mathrm{near-zero}}(n) = \sum_{\lambda_i \in (-\varepsilon, \varepsilon)} \left|\langle \phi_i | \psi_n \rangle\right|^2$$

   wobei $\phi_i$ Eigenvektoren von $D_{420}$ sind.

---

### Phase 2: Korrelationsanalyse

Für das gesamte Ensemble:

1. **Pearson-Korrelation:**

   $$\rho = \operatorname{corr}\left(M_C^{\mathrm{spec}}, M_{\mathrm{near-zero}}\right)$$

2. **Stratifiziert nach $k$:**

   $$\rho_k = \operatorname{corr}\left(M_C^{\mathrm{spec}} \mid_{\Omega = k}, M_{\mathrm{near-zero}} \mid_{\Omega = k}\right)$$

---

### Phase 3: Permutationstest

**Nullhypothese:** $\rho = 0$ (Unabhängigkeit)

**Test:**

1. Berechne originale Korrelation $\rho_0$
2. Für $N_{\text{perm}} = 1000$ Permutationen:
   - Permutiere $M_{\mathrm{near-zero}}$ **innerhalb** jeder $k$-Klasse
   - Berechne $\rho_{\text{perm}}$
3. $p$-Wert (zweiseitig):

   $$p = \frac{1}{N_{\text{perm}}} \sum_{i=1}^{N_{\text{perm}}} \mathbb{1}[|\rho_{\text{perm},i}| \geq |\rho_0|]$$

**Kriterium:** $|\rho_0| > 0.15$ und $p < 0.05$

---

## Code-Skelett

```python
def experiment_5_spectral_comparison(numbers, epsilon=0.1):
    M_catalan_spec = []
    M_near_zero = []
    omega_vals = []
    
    # Berechne Spektralobservablen (cacheable)
    catalan_spectral_table = precompute_catalan_spectral_magic(epsilon)
    D_420_eigvecs = precompute_eabc_eigenvectors()
    
    for n in numbers:
        k = omega(n)
        factors = prime_factorization(n)
        
        # Catalan-spektrale Magic
        T = construct_canonical_tree(factors)
        M_C_spec = catalan_spectral_table[k][T]
        M_catalan_spec.append(M_C_spec)
        
        # EABC-near-zero-magic
        eabc_sig = eabc_signature_420(n)
        psi_n = construct_eabc_state(eabc_sig)
        M_nz = near_zero_magic(psi_n, D_420_eigvecs, epsilon)
        M_near_zero.append(M_nz)
        
        omega_vals.append(k)
    
    # Gesamtkorrelation
    rho_original = np.corrcoef(M_catalan_spec, M_near_zero)[0,1]
    
    # Permutationstest
    rho_permuted = []
    for _ in range(1000):
        M_nz_perm = permute_within_omega_class(M_near_zero, omega_vals)
        rho_perm = np.corrcoef(M_catalan_spec, M_nz_perm)[0,1]
        rho_permuted.append(rho_perm)
    
    # p-Wert (zweiseitig)
    p_value = np.mean([abs(rho_p) >= abs(rho_original) 
                       for rho_p in rho_permuted])
    
    # Stratifiziert nach k
    rho_by_k = {}
    for k in set(omega_vals):
        mask = np.array(omega_vals) == k
        rho_by_k[k] = np.corrcoef(
            np.array(M_catalan_spec)[mask],
            np.array(M_near_zero)[mask]
        )[0,1]
    
    return {
        'rho': rho_original,
        'rho_permuted_mean': np.mean(rho_permuted),
        'rho_permuted_std': np.std(rho_permuted),
        'p_value': p_value,
        'rho_by_k': rho_by_k,
        'significant': abs(rho_original) > 0.15 and p_value < 0.05
    }
```

---

## Erwartete Resultate

### Szenario A: Korreliert

- $|\rho| \gtrsim 0.2$
- $p < 0.01$

**Interpretation:** Die spektralen Strukturen sind gekoppelt.

---

### Szenario B: Unkorreliert

- $|\rho| \lesssim 0.05$
- $p \gtrsim 0.3$

**Interpretation:** EABC- und Catalan-Spektren sind unabhängig.

---

## Visualisierung

1. **Scatterplot:** $M_C^{\mathrm{spec}}$ vs. $M_{\mathrm{near-zero}}$ (farbkodiert nach $k$)
2. **Barplot:** Korrelationen $\rho_k$ für jedes $k$
3. **Histogram:** Permutationsverteilung mit $\rho_0$ markiert

---

## Erweiterte Tests

### Test 5a: Hochfrequente Korrelation

Teste auch:

$$\operatorname{corr}\left(M_{C,\varepsilon}^{\mathrm{high}}(n), M_{\mathrm{high-freq}}(D_{420}, n)\right)$$

**Erwartung:** Komplementäre Information (negative oder keine Korrelation).

---

### Test 5b: IPR-Korrelation

Falls ein gekoppelter Operator konstruiert ist:

$$\operatorname{corr}(\mathrm{IPR}(H_{\mathrm{tot}}), M_C^{\mathrm{spec}})$$

---

## Deliverables

1. **Tabelle:** Korrelationen für jedes $k$
2. **Plots:** Scatterplot, Barplot, Histogram
3. **JSON:** `spectral_correlation.json`

---

## Zeitaufwand

- **Spektralvorbereitung:** 2 Tage
- **Observable-Berechnung:** 2 Tage
- **Permutationstest:** 1 Tag
- **Visualisierung:** 1 Tag

**Total:** ~6 Tage

---

## Literatur

- Near-zero magic: Siehe EABC-Projekt `CATALAN_SPECTRAL_SUMMARY.md`
- Spectral observables: Chung (1997), *Spectral Graph Theory*
