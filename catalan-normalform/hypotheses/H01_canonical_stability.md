# Hypothese C1: Kanonische Stabilität

## Formulierung

Für natürliche Kanonisierungen $\kappa_1, \kappa_2 \in \{T_L, T_R, T_B\}$ gilt **im Mittel** über große Ensembles:

$$M_C^{\kappa_1}(n) \approx a_{\kappa_1,\kappa_2} \cdot M_C^{\kappa_2}(n) + b_{\kappa_1,\kappa_2}$$

mit Konstanten $a, b \in \mathbb{R}$.

---

## Interpretation

Die Catalan-Magic darf **nicht völlig** von der willkürlichen Kanonisierung abhängen.

Falls die Wahl von $\kappa$ das Signal dominiert, ist die Observable nicht robust genug.

---

## Nullmodell

**H0:** Verschiedene Kanonisierungen sind **unkorreliert**:

$$\operatorname{corr}(M_C^{\kappa_1}, M_C^{\kappa_2}) \approx 0$$

---

## Teststatistik

Für ein Ensemble $\mathcal{N} = \{n_1, \ldots, n_N\}$ berechne:

$$\rho = \operatorname{corr}\left(\{M_C^{T_L}(n_i)\}, \{M_C^{T_R}(n_i)\}\right)$$

$$\rho' = \operatorname{corr}\left(\{M_C^{T_L}(n_i)\}, \{M_C^{T_B}(n_i)\}\right)$$

**Kriterium:**

$$\rho > 0.5 \quad \text{oder} \quad \rho' > 0.5$$

---

## Implementierung

```python
def test_canonical_stability(numbers):
    M_left = [catalan_magic(n, canon='left') for n in numbers]
    M_right = [catalan_magic(n, canon='right') for n in numbers]
    M_balanced = [catalan_magic(n, canon='balanced') for n in numbers]
    
    corr_LR = np.corrcoef(M_left, M_right)[0,1]
    corr_LB = np.corrcoef(M_left, M_balanced)[0,1]
    corr_RB = np.corrcoef(M_right, M_balanced)[0,1]
    
    return {
        'corr_LR': corr_LR,
        'corr_LB': corr_LB,
        'corr_RB': corr_RB,
        'stable': min(corr_LR, corr_LB, corr_RB) > 0.5
    }
```

---

## Erwartetes Resultat

- Falls **stabil:** $\rho \gtrsim 0.7$ (moderate Korrelation trotz unterschiedlicher Kanonisierung)
- Falls **instabil:** $\rho \lesssim 0.3$ (Kanonisierung dominiert Signal)

---

## Konsequenzen

- **Stabil:** Catalan-Magic enthält kanonisierungs-invariante Information
- **Instabil:** Man muss Ensemble-Mittelung verwenden ($\overline{M}_C$)
