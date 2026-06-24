# Hypothese C7: Skalengesetz

## Formulierung

Für typische Zahlen $n \leq X$ gilt:

$$\mathbb{E}[M_C^w(n)] \sim A (\log\log X)^\theta$$

mit Konstanten $A > 0$ und $\theta > 0$.

---

## Interpretation

Da nach Hardy–Ramanujan:

$$\mathbb{E}[\Omega(n)] \sim \log\log n$$

für $n \to \infty$, ist ein **logarithmisch-logarithmisches** Wachstum plausibel.

**Hypothese:** $\theta \approx 1$ (lineares Skalengesetz).

---

## Nullmodell

**H0:** Kein Wachstum oder alternatives Skalengesetz:

$$\mathbb{E}[M_C^w(n)] \sim \text{const.} \quad \text{oder} \quad \sim (\log X)^\alpha$$

---

## Teststatistik

Für mehrere Größenordnungen $X_1 < X_2 < \cdots < X_K$:

1. Berechne empirische Mittelwerte:

   $$\bar{M}_C(X_i) = \frac{1}{N_i} \sum_{n \leq X_i} M_C^w(n)$$

2. Fitte Potenzgesetz:

   $$\log \bar{M}_C(X_i) = \log A + \theta \log(\log\log X_i)$$

   via linearer Regression.

**Kriterium:**

$$0.8 \leq \theta \leq 1.2 \quad \text{und} \quad R^2 > 0.95$$

---

## Implementierung

```python
def test_scale_law(X_values):
    M_means = []
    log_log_log_X = []
    
    for X in X_values:
        # Zahlen bis X
        numbers = generate_numbers_up_to(X, sample_size=10000)
        
        # Mittlere Catalan-Magic
        M_mean = np.mean([catalan_magic_weighted(n) for n in numbers])
        M_means.append(M_mean)
        
        # log(log log X)
        log_log_log_X.append(np.log(np.log(np.log(X))))
    
    # Lineare Regression: log(M) ~ theta * log(log log X)
    X_fit = np.array(log_log_log_X).reshape(-1, 1)
    y_fit = np.log(M_means)
    
    model = LinearRegression().fit(X_fit, y_fit)
    theta = model.coef_[0]
    A = np.exp(model.intercept_)
    R2 = model.score(X_fit, y_fit)
    
    return {
        'theta': theta,
        'A': A,
        'R2': R2,
        'valid': 0.8 <= theta <= 1.2 and R2 > 0.95
    }
```

---

## Erwartetes Resultat

- **Falls lineares Skalengesetz:** $\theta \approx 1.0 \pm 0.1$
- **Falls konstant:** $\theta \approx 0$
- **Falls polynomiell in $\log X$:** $\theta \gg 1$

---

## Konsequenzen

- **$\theta \approx 1$:** Catalan-Magic skaliert mit der typischen Faktoranzahl
- **$\theta \approx 0$:** Catalan-Magic ist größenunabhängig (normiert)
- **$\theta > 1$:** Catalan-Komplexität wächst schneller als Faktoranzahl

---

## Erweiterte Tests

### Test 7a: Varianzskalengesetz

Teste auch die Varianz:

$$\operatorname{Var}[M_C^w(n)] \sim B (\log\log X)^\alpha$$

**Hypothese:** $\alpha \approx 2 \theta$ (Gausssche Fluktuation).

---

### Test 7b: Stratifizierung nach EABC-Klassen

Teste das Skalengesetz **separat** für jede EABC-Klasse:

$$\mathbb{E}[M_C^w(n) \mid E(n) = E] \sim A_E (\log\log X)^{\theta_E}$$

**Hypothese:** $\theta_E \approx \theta_A \approx \theta_B \approx \theta_C$ (universell).

---

## Literatur

- Hardy–Ramanujan: Hardy & Ramanujan (1917), *The normal number of prime factors*.
- Asymptotic analysis: de Bruijn (1981), *Asymptotic Methods in Analysis*.
