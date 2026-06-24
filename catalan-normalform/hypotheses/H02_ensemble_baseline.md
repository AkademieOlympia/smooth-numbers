# Hypothese C2: Ensemble-Baseline

## Formulierung

Die Ensemble-Magic

$$\overline{M}_C(k) = \mathbb{E}_{T \sim \text{Unif}(\mathcal{T}_k)}\left[\min_{B \in \mathcal{B}_k} d_C(T, B)\right]$$

erklärt **nur** den trivialen Anteil, der von $\Omega(n) = k$ abhängt.

Der **arithmetische Rest** ist:

$$M_C^{\mathrm{res}}(n) = M_C(n) - \overline{M}_C(\Omega(n))$$

**Hypothese:** $M_C^{\mathrm{res}}(n)$ enthält arithmetische Information.

---

## Interpretation

$\overline{M}_C(k)$ ist eine rein kombinatorische Baseline.

Falls $M_C^{\mathrm{res}}(n) \approx 0$ für alle $n$, ist Catalan-Magic keine neue Zahlentheorie.

---

## Nullmodell

**H0:** $M_C^{\mathrm{res}}(n)$ ist reines Rauschen:

$$M_C^{\mathrm{res}}(n) \sim \mathcal{N}(0, \sigma^2)$$

unabhängig von arithmetischen Eigenschaften.

---

## Teststatistik

Für ein Ensemble $\mathcal{N}$ stratifiziert nach $k = \Omega(n)$:

$$\sigma_{\mathrm{within}}^2 = \frac{1}{|\mathcal{N}|} \sum_{n \in \mathcal{N}} \left(M_C^{\mathrm{res}}(n)\right)^2$$

$$\sigma_{\mathrm{between}}^2 = \frac{1}{K} \sum_{k} N_k \left(\overline{M}_C^{\mathrm{emp}}(k) - \overline{M}_C^{\mathrm{theory}}(k)\right)^2$$

**Kriterium:**

$$\frac{\sigma_{\mathrm{within}}^2}{\sigma_{\mathrm{between}}^2} \ll 1$$

Falls das Residuum **klein** ist im Vergleich zur Baseline-Variation, ist die Hypothese falsifiziert.

---

## Implementierung

```python
def test_ensemble_baseline(numbers):
    # Berechne theoretische Baseline für jedes k
    k_values = [omega(n) for n in numbers]
    baseline = {k: ensemble_catalan_magic(k) for k in set(k_values)}
    
    # Berechne Residuen
    residuals = []
    for n in numbers:
        k = omega(n)
        M_obs = catalan_magic(n)
        M_base = baseline[k]
        residuals.append(M_obs - M_base)
    
    # Statistik
    var_within = np.var(residuals)
    
    # Baseline-Variation (sollte strukturiert sein)
    baseline_vals = [baseline[omega(n)] for n in numbers]
    var_between = np.var(baseline_vals)
    
    ratio = var_within / var_between
    
    return {
        'var_within': var_within,
        'var_between': var_between,
        'ratio': ratio,
        'significant': ratio > 0.1  # Residuen sind nicht vernachlässigbar
    }
```

---

## Erwartetes Resultat

- **Falls arithmetisch relevant:** $\sigma_{\mathrm{within}}^2 \gtrsim 0.1 \cdot \sigma_{\mathrm{between}}^2$
- **Falls trivial:** $\sigma_{\mathrm{within}}^2 \ll \sigma_{\mathrm{between}}^2$

---

## Konsequenzen

- **Signifikant:** Catalan-Hierarchie trägt neue Information bei
- **Trivial:** Catalan-Magic ist nur Reparametrisierung von $\Omega(n)$
