# Hypothese C5: Chaos-Korrelation

## Formulierung

Für die EABC-Qubit-Hamiltonianfamilie gilt:

$$\operatorname{corr}\left(M_C^{\mathrm{res}}(n), q_{\mathrm{Brody}}(n)\right) \neq 0$$

wobei:

- $M_C^{\mathrm{res}}(n)$: Residuale Catalan-Magic
- $q_{\mathrm{Brody}}(n)$: Brody-Parameter der Level-Spacing-Verteilung des zugehörigen Qubit-Hamiltonians

---

## Interpretation

Der Brody-Parameter $q$ misst den Grad der **spektralen Unordnung**:

- $q \approx 0$: Poisson-Statistik (integrabel)
- $q \approx 1$: Wigner-Dyson-Statistik (chaotisch)

**Hypothese:** Die Catalan-Hierarchie beeinflusst die Chaos-Signaturen.

---

## Nullmodell

**H0:** Beide Größen sind **unabhängig**:

$$\operatorname{corr}(M_C^{\mathrm{res}}, q_{\mathrm{Brody}}) = 0$$

**Permutationstest:** Permutiere $q_{\mathrm{Brody}}$ bei festem $\Omega(n)$ und fester Signatur.

---

## Teststatistik

Für ein Ensemble $\mathcal{N}$ von Zahlen mit zugehörigen Qubit-Hamiltonians:

$$\rho = \operatorname{corr}\left(\{M_C^{\mathrm{res}}(n_i)\}, \{q_{\mathrm{Brody}}(n_i)\}\right)$$

**Stratifizierung:** Kontrolliere für $\Omega(n)$ und Systemgröße des Hamiltonians.

**Kriterium:**

$$|\rho| > 0.2 \quad \text{und} \quad p < 0.05$$

---

## Implementierung

```python
def test_chaos_correlation(numbers, n_permutations=1000):
    # Berechne beide Observablen
    M_catalan_res = [catalan_magic_residual(n) for n in numbers]
    q_brody = [brody_parameter(construct_hamiltonian(n)) for n in numbers]
    
    # Originale Korrelation
    rho_original = np.corrcoef(M_catalan_res, q_brody)[0,1]
    
    # Permutationstest (stratifiziert nach Omega)
    rho_permuted = []
    for _ in range(n_permutations):
        q_brody_perm = permute_within_omega_class(q_brody, numbers)
        rho_perm = np.corrcoef(M_catalan_res, q_brody_perm)[0,1]
        rho_permuted.append(rho_perm)
    
    # p-Wert
    p_value = np.mean([abs(rho_perm) >= abs(rho_original) 
                       for rho_perm in rho_permuted])
    
    return {
        'rho': rho_original,
        'p_value': p_value,
        'significant': abs(rho_original) > 0.2 and p_value < 0.05,
        'direction': 'positive' if rho_original > 0 else 'negative'
    }
```

---

## Erwartetes Resultat

**Zwei Szenarien:**

### Szenario A: Positive Korrelation

$$\rho > 0$$

**Interpretation:** Größere Catalan-Magic (asymmetrische Hierarchie) → mehr Chaos

---

### Szenario B: Negative Korrelation

$$\rho < 0$$

**Interpretation:** Größere Catalan-Magic → weniger Chaos (strukturierte Hierarchie unterdrückt Chaos)

---

## Konsequenzen

- **Signifikant:** Catalan-Hierarchie ist ein **Prädiktor** für spektrale Chaos-Eigenschaften
- **Nicht signifikant:** Chaos-Eigenschaften sind unabhängig von der Faktorhierarchie

---

## Erweiterte Tests

### Test 5a: Level-Statistik direkt

Statt Brody-Parameter teste:

$$\operatorname{corr}(M_C^{\mathrm{res}}, \langle r \rangle)$$

wobei $\langle r \rangle$ der mittlere Level-Spacing-Ratio ist.

---

### Test 5b: Stratifizierung nach EABC-Signatur

Teste die Korrelation **innerhalb** jeder EABC-Klasse separat:

$$\rho_E, \rho_A, \rho_B, \rho_C$$

**Hypothese:** Die Korrelation ist **heterogen** über EABC-Klassen.

---

## Literatur

- Brody distribution: Brody (1973), *Lettere al Nuovo Cimento*.
- Chaos in quantum systems: Haake (2010), *Quantum Signatures of Chaos*.
- EABC-Qubit-Hamiltonians: Siehe `../eabc-qubit/` Projekt.
