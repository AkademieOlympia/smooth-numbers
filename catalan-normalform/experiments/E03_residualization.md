# Experiment 3: Residualisierung

## Ziel

Teste **Hypothese C2** (Ensemble-Baseline):

Enthält das Residuum $M_C^{\mathrm{res}}(n) = M_C(n) - \overline{M}_C(\Omega(n))$ arithmetische Information?

---

## Vorbereitung

### Phase 0: Baseline-Berechnung

Für jedes $k = 2, \ldots, 12$ berechne die **theoretische Ensemble-Magic:**

$$\overline{M}_C^{\mathrm{theory}}(k) = \frac{1}{|\mathcal{T}_k|} \sum_{T \in \mathcal{T}_k} \min_{B \in \mathcal{B}_k} d_C(T, B)$$

**Input:** Ergebnisse aus **Experiment 1** (Tamari-Baseline).

**Output:** Tabelle `baseline_table.json`:

```json
{
  "2": 0.0,
  "3": 0.5,
  "4": 2.1,
  "5": 3.7,
  ...
}
```

---

## Daten

Ensemble von $N = 100{,}000$ Zahlen:

$$\mathcal{N} = \{n_1, \ldots, n_N\}$$

mit stratifizierter Verteilung über $\Omega(n) \in \{3, 4, 5, 6, 7, 8\}$.

---

## Implementierung

### Phase 1: Residuum-Berechnung

Für jede Zahl $n \in \mathcal{N}$:

1. Berechne $M_C(n)$ (mit gewählter Kanonisierung $\kappa$)
2. Lese Baseline ab: $\overline{M}_C(\Omega(n))$
3. Berechne Residuum:

   $$M_C^{\mathrm{res}}(n) = M_C(n) - \overline{M}_C(\Omega(n))$$

---

### Phase 2: Varianzzerlegung

Berechne:

1. **Within-Stratum Varianz:**

   $$\sigma_{\mathrm{within}}^2 = \frac{1}{|\mathcal{N}|} \sum_{n \in \mathcal{N}} \left(M_C^{\mathrm{res}}(n)\right)^2$$

2. **Between-Stratum Varianz:**

   $$\sigma_{\mathrm{between}}^2 = \sum_k \frac{N_k}{|\mathcal{N}|} \left(\overline{M}_C^{\mathrm{emp}}(k) - \overline{M}_C^{\mathrm{theory}}(k)\right)^2$$

   wobei $N_k = |\{n \in \mathcal{N} : \Omega(n) = k\}|$.

**Ratio:**

$$r = \frac{\sigma_{\mathrm{within}}^2}{\sigma_{\mathrm{between}}^2}$$

**Kriterium:**

- Falls $r \ll 1$: Residuum ist vernachlässigbar (H2 falsifiziert)
- Falls $r \gtrsim 0.1$: Residuum enthält signifikante Information (H2 bestätigt)

---

### Phase 3: Normalitätstest

Teste ob $M_C^{\mathrm{res}}(n)$ **normalverteilt** ist:

1. **Kolmogorov-Smirnov-Test:**

   $$H_0: M_C^{\mathrm{res}} \sim \mathcal{N}(0, \sigma^2)$$

2. **Q-Q-Plot:**

   Vergleiche empirische Quantile mit theoretischen Normalverteilungs-Quantilen.

**Erwartung:** Falls $M_C^{\mathrm{res}}$ **nicht** normalverteilt ist, enthält es Struktur.

---

## Code-Skelett

```python
def experiment_3_residualization(numbers, baseline_table):
    residuals = []
    omega_vals = []
    
    for n in numbers:
        k = omega(n)
        M_C = catalan_magic(n)
        M_baseline = baseline_table[str(k)]
        
        M_res = M_C - M_baseline
        residuals.append(M_res)
        omega_vals.append(k)
    
    # Varianz within
    var_within = np.var(residuals)
    
    # Varianz between (empirische Abweichung von Theorie)
    var_between = 0
    for k in set(omega_vals):
        mask = np.array(omega_vals) == k
        M_emp_mean = np.mean(np.array([catalan_magic(n) for n in numbers])[mask])
        M_theory = baseline_table[str(k)]
        N_k = np.sum(mask)
        var_between += (N_k / len(numbers)) * (M_emp_mean - M_theory)**2
    
    ratio = var_within / var_between if var_between > 0 else np.inf
    
    # Normalitätstest
    from scipy.stats import kstest
    ks_stat, ks_pval = kstest(residuals, 'norm', 
                                args=(np.mean(residuals), np.std(residuals)))
    
    return {
        'var_within': var_within,
        'var_between': var_between,
        'ratio': ratio,
        'ks_statistic': ks_stat,
        'ks_pvalue': ks_pval,
        'significant': ratio > 0.1 and ks_pval < 0.05
    }
```

---

## Erwartete Resultate

### Szenario A: Residuum ist signifikant

- $r \gtrsim 0.2$
- Nicht-normalverteilt ($p < 0.05$)

**Interpretation:** Catalan-Hierarchie enthält Information jenseits von $\Omega(n)$.

---

### Szenario B: Residuum ist trivial

- $r \lesssim 0.05$
- Normalverteilt ($p > 0.1$)

**Interpretation:** Catalan-Magic ist nur eine Funktion von $\Omega(n)$ (H2 falsifiziert).

---

## Visualisierung

1. **Histogram:** Verteilung von $M_C^{\mathrm{res}}(n)$ mit Normalverteilungs-Fit
2. **Q-Q-Plot:** Test auf Normalität
3. **Boxplot:** Residuen stratifiziert nach $k$

---

## Deliverables

1. **Tabelle:** Varianzzerlegung
2. **Plots:** Histogramm und Q-Q-Plot
3. **JSON:** Residuen-Daten `residuals.json`

---

## Zeitaufwand

- **Baseline-Import:** 0.5 Tage
- **Residuum-Berechnung:** 1 Tag
- **Statistik:** 1 Tag
- **Visualisierung:** 0.5 Tage

**Total:** ~3 Tage

---

## Kritisches Kriterium

Falls **Szenario B** eintritt ($r < 0.05$):

→ **STOPP:** Die Catalan-Geometrie ist trivial. Alle weiteren Experimente sind hinfällig.
