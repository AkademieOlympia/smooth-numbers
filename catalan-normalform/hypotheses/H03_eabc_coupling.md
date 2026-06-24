# Hypothese C3: EABC-Kopplung

## Formulierung

Die EABC-Signatur $E(n) = (\sigma_{12}(p_1), \ldots, \sigma_{12}(p_k))$ beeinflusst die bevorzugte Catalan-Hierarchie.

**Mutual Information:**

$$I(M_C^{\mathrm{res}}(n); E(n) \mid \Omega(n)) > 0$$

**Interpretation:** Nach Kontrolle für $\Omega(n)$ bleibt eine messbare Korrelation zwischen Catalan-Magic und EABC-Signatur.

---

## Nullmodell

**H0:** EABC-Signatur und Catalan-Hierarchie sind **unabhängig**:

$$I(M_C^{\mathrm{res}}(n); E(n) \mid \Omega(n)) = 0$$

**Test:** Permutiere zufällig die EABC-Labels der Primfaktoren bei festem $\Omega(n)$ und festem Baum.

---

## Teststatistik

Für jedes $k = \Omega(n)$:

1. Berechne die empirische Verteilung:

   $$P(M_C^{\mathrm{res}} \mid E, k)$$

2. Vergleiche mit der Nullverteilung:

   $$P(M_C^{\mathrm{res}} \mid k)$$

   (unabhängig von $E$)

**Divergenz:**

$$D_{\mathrm{KL}}(P(M_C^{\mathrm{res}} \mid E, k) \| P(M_C^{\mathrm{res}} \mid k))$$

**Kriterium:**

$$\overline{D_{\mathrm{KL}}} > \text{threshold}$$

gemittelt über $k$ und gewichtet nach Häufigkeit.

---

## Permutationstest

```python
def test_eabc_coupling(numbers, n_permutations=1000):
    # Originale Mutual Information
    I_original = mutual_information(
        [catalan_magic_residual(n) for n in numbers],
        [eabc_signature(n) for n in numbers],
        [omega(n) for n in numbers]
    )
    
    # Permutationstest
    I_permuted = []
    for _ in range(n_permutations):
        # Permutiere EABC-Labels bei festem Omega
        numbers_perm = permute_eabc_labels(numbers)
        I_perm = mutual_information(
            [catalan_magic_residual(n) for n in numbers_perm],
            [eabc_signature(n) for n in numbers_perm],
            [omega(n) for n in numbers_perm]
        )
        I_permuted.append(I_perm)
    
    # p-Wert
    p_value = np.mean([I_perm >= I_original for I_perm in I_permuted])
    
    return {
        'I_original': I_original,
        'I_permuted_mean': np.mean(I_permuted),
        'I_permuted_std': np.std(I_permuted),
        'p_value': p_value,
        'significant': p_value < 0.05
    }
```

---

## Erwartetes Resultat

- **Falls gekoppelt:** $I > 0.01$ bits, $p < 0.05$
- **Falls ungekoppelt:** $I \approx 0$, $p \gtrsim 0.5$

---

## Konsequenzen

- **Signifikant:** EABC-Restklassen beeinflussen die Hierarchiebildung
- **Nicht signifikant:** Lokale und globale Ebene sind separierbar

---

## Varianten

### Stärkere Version (Chi-Quadrat-Test)

Teste für jede EABC-Signaturklasse:

$$\chi^2 = \sum_{\text{bins}} \frac{(O_i - E_i)^2}{E_i}$$

wobei $O_i$ die beobachtete und $E_i$ die erwartete Häufigkeit von $M_C^{\mathrm{res}}$ ist.

---

## Literatur

- Mutual Information: Cover & Thomas (2006), *Elements of Information Theory*.
