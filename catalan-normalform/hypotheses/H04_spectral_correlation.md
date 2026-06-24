# Hypothese C4: Spektrale Korrelation

## Formulierung

Die spektrale Catalan-Magic korreliert mit vorhandenen EABC-Spektralobservablen:

$$\operatorname{corr}\left(M_{C,\varepsilon}^{\mathrm{spec}}(n), M_{\mathrm{near-zero}}(D_{420}, n)\right) \neq 0$$

wobei:

- $M_{C,\varepsilon}^{\mathrm{spec}}$: Niedrigfrequente Projektion auf Catalan-Laplace-Operator
- $M_{\mathrm{near-zero}}(D_{420})$: Near-zero-magic des EABC-Dirac-Operators

---

## Interpretation

Falls die spektralen Strukturen beider Ebenen **korreliert** sind, deutet das auf eine tiefere Verbindung hin.

---

## Nullmodell

**H0:** Beide Observablen sind **unabhängig**:

$$\operatorname{corr}(M_C^{\mathrm{spec}}, M_{\mathrm{near-zero}}) = 0$$

**Permutationstest:**

1. Behalte $M_C^{\mathrm{spec}}(n)$ fest
2. Permutiere $M_{\mathrm{near-zero}}(n)$ zufällig (bei gleichem $\Omega(n)$)
3. Berechne Korrelation

---

## Teststatistik

Für ein Ensemble $\mathcal{N}$:

$$\rho = \operatorname{corr}\left(\{M_C^{\mathrm{spec}}(n_i)\}, \{M_{\mathrm{near-zero}}(n_i)\}\right)$$

**Bootstrap-Konfidenzintervall:**

Resample $\mathcal{N}$ mit Zurücklegen, berechne $\rho^*$, wiederhole $N_{\mathrm{boot}}$ mal.

**Kriterium:**

$$|\rho| > 0.15 \quad \text{und} \quad p < 0.05$$

---

## Implementierung

```python
def test_spectral_correlation(numbers, epsilon=0.1, n_permutations=1000):
    # Berechne beide Observablen
    M_catalan_spec = [catalan_spectral_magic(n, epsilon) for n in numbers]
    M_near_zero = [near_zero_magic_420(n) for n in numbers]
    
    # Originale Korrelation
    rho_original = np.corrcoef(M_catalan_spec, M_near_zero)[0,1]
    
    # Permutationstest
    rho_permuted = []
    for _ in range(n_permutations):
        M_near_zero_perm = permute_within_omega_class(M_near_zero, numbers)
        rho_perm = np.corrcoef(M_catalan_spec, M_near_zero_perm)[0,1]
        rho_permuted.append(rho_perm)
    
    # p-Wert (zweiseitig)
    p_value = np.mean([abs(rho_perm) >= abs(rho_original) 
                       for rho_perm in rho_permuted])
    
    return {
        'rho': rho_original,
        'rho_permuted_mean': np.mean(rho_permuted),
        'rho_permuted_std': np.std(rho_permuted),
        'p_value': p_value,
        'significant': abs(rho_original) > 0.15 and p_value < 0.05
    }
```

---

## Erwartetes Resultat

- **Falls korreliert:** $|\rho| \gtrsim 0.2$, $p < 0.01$
- **Falls unkorreliert:** $|\rho| \lesssim 0.05$, $p \gtrsim 0.3$

---

## Konsequenzen

- **Signifikant:** Die spektralen Strukturen von EABC und Catalan sind gekoppelt
- **Nicht signifikant:** Beide Ebenen besitzen unabhängige spektrale Eigenschaften

---

## Erweiterte Tests

### Test 4a: Hochfrequente Korrelation

Teste auch:

$$\operatorname{corr}\left(M_{C,\varepsilon}^{\mathrm{high}}(n), M_{\mathrm{high-freq}}(D_{420}, n)\right)$$

**Erwartung:** Negative oder keine Korrelation (komplementäre Information).

---

### Test 4b: IPR-Korrelation

Falls ein gekoppelter Operator $H_{\mathrm{tot}}$ konstruiert ist:

$$\operatorname{corr}(\mathrm{IPR}(H_{\mathrm{tot}}), M_C^{\mathrm{res}})$$

---

## Literatur

- Near-zero magic: Siehe `../theory/02_local_geometry.md`
- Spectral correlation: Newman (2018), *Networks*, Chapter 7.
