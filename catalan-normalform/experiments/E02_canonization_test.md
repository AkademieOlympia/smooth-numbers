# Experiment 2: Kanonisierungstest

## Ziel

Teste **Hypothese C1** (Kanonische Stabilität):

Sind verschiedene Kanonisierungen $\kappa \in \{T_L, T_R, T_B\}$ korreliert oder unabhängig?

---

## Daten

Generiere Ensemble von Zahlen:

$$\mathcal{N} = \{n_1, \ldots, n_N\}$$

mit $N = 100{,}000$.

**Stratifizierung:**

- Für jedes $k = \Omega(n) \in \{3, 4, 5, 6, 7, 8\}$: mindestens 10{,}000 Zahlen
- Maximale Größe: $n \leq 10^{15}$

---

## Implementierung

### Phase 1: Kanonisierungen

Für jede Zahl $n \in \mathcal{N}$:

1. Berechne Primfaktorzerlegung:

   $$n = p_1 \cdot p_2 \cdots p_k$$

   mit $p_1 \leq p_2 \leq \cdots \leq p_k$

2. Konstruiere drei kanonische Bäume:

   - $T_L(n)$: Linksbaum
   - $T_R(n)$: Rechtsbaum
   - $T_B(n)$: Balancierter Baum

3. Berechne für jede Kanonisierung die Catalan-Magic:

   $$M_C^L(n), \quad M_C^R(n), \quad M_C^B(n)$$

---

### Phase 2: Korrelationsanalyse

Für das gesamte Ensemble:

1. **Pearson-Korrelation:**

   $$\rho_{LR} = \operatorname{corr}(M_C^L, M_C^R)$$
   $$\rho_{LB} = \operatorname{corr}(M_C^L, M_C^B)$$
   $$\rho_{RB} = \operatorname{corr}(M_C^R, M_C^B)$$

2. **Stratifiziert nach $k$:**

   Für jedes $k$ separat:

   $$\rho_{LR}^{(k)}, \quad \rho_{LB}^{(k)}, \quad \rho_{RB}^{(k)}$$

---

### Phase 3: Affine Beziehungen

Teste ob:

$$M_C^L(n) \approx a_{LR} \cdot M_C^R(n) + b_{LR}$$

via linearer Regression.

**Bestimmtheitsmaß:**

$$R^2 = 1 - \frac{\sum_i (M_C^L(n_i) - \hat{M}_i)^2}{\sum_i (M_C^L(n_i) - \bar{M})^2}$$

---

## Code-Skelett

```python
def experiment_2_canonization(numbers):
    results = {
        'left': [],
        'right': [],
        'balanced': [],
        'omega': []
    }
    
    for n in numbers:
        # Primfaktorzerlegung
        factors = prime_factorization(n)
        k = len(factors)
        
        # Kanonische Bäume
        T_L = construct_left_tree(factors)
        T_R = construct_right_tree(factors)
        T_B = construct_balanced_tree(factors)
        
        # Catalan-Magic
        M_L = catalan_magic(T_L, k)
        M_R = catalan_magic(T_R, k)
        M_B = catalan_magic(T_B, k)
        
        results['left'].append(M_L)
        results['right'].append(M_R)
        results['balanced'].append(M_B)
        results['omega'].append(k)
    
    # Gesamtkorrelationen
    rho_LR = np.corrcoef(results['left'], results['right'])[0,1]
    rho_LB = np.corrcoef(results['left'], results['balanced'])[0,1]
    rho_RB = np.corrcoef(results['right'], results['balanced'])[0,1]
    
    # Stratifiziert nach k
    rho_by_k = {}
    for k in set(results['omega']):
        mask = np.array(results['omega']) == k
        rho_by_k[k] = {
            'LR': np.corrcoef(
                np.array(results['left'])[mask],
                np.array(results['right'])[mask]
            )[0,1],
            'LB': np.corrcoef(
                np.array(results['left'])[mask],
                np.array(results['balanced'])[mask]
            )[0,1],
            'RB': np.corrcoef(
                np.array(results['right'])[mask],
                np.array(results['balanced'])[mask]
            )[0,1]
        }
    
    return {
        'rho_LR': rho_LR,
        'rho_LB': rho_LB,
        'rho_RB': rho_RB,
        'rho_by_k': rho_by_k,
        'stable': min(rho_LR, rho_LB, rho_RB) > 0.5
    }
```

---

## Erwartete Resultate

### Szenario A: Kanonisch stabil

$$\rho_{LR} \gtrsim 0.7, \quad \rho_{LB} \gtrsim 0.6, \quad \rho_{RB} \gtrsim 0.6$$

**Interpretation:** Die Catalan-Magic ist robust gegenüber Kanonisierungswahl.

---

### Szenario B: Kanonisch instabil

$$\rho_{LR} \lesssim 0.3, \quad \rho_{LB} \lesssim 0.3, \quad \rho_{RB} \lesssim 0.3$$

**Interpretation:** Die Kanonisierung dominiert das Signal. Man muss Ensemble-Mittelung verwenden.

---

## Visualisierung

1. **Scatterplot:** $M_C^L$ vs. $M_C^R$ (farbkodiert nach $k$)
2. **Boxplot:** Verteilung von $\rho$ über verschiedene $k$
3. **Heatmap:** Korrelationsmatrix für alle drei Kanonisierungen

---

## Deliverables

1. **Tabelle:** Korrelationen für jedes $k$
2. **Plot:** Scatterplots der drei Paare
3. **JSON:** Rohdaten für weitere Analyse

---

## Zeitaufwand

- **Datengeneration:** 1 Tag
- **Analyse:** 1 Tag
- **Visualisierung:** 1 Tag

**Total:** ~3 Tage

---

## Fallback

Falls **instabil** ($\rho < 0.5$):

→ Verwende **gewichtete Ensemble-Mittelung** für alle weiteren Experimente.
