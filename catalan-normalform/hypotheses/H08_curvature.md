# Hypothese C8: Krümmung des Catalan-Raums

## Formulierung

Der Tamari-Graph $\Gamma_k$ besitzt eine **diskrete Krümmung** (z.B. Ollivier-Ricci oder Forman-Ricci).

**Hypothese:**

$$\operatorname{corr}(M_C(T), -\kappa_C(T)) > 0$$

**Interpretation:** Stark asymmetrische Bäume liegen in geometrisch **negativ gekrümmten** Regionen des Catalan-Raums.

---

## Interpretation

**Negative Krümmung** ist typisch für hyperbolische Geometrie:

- Große Abstände
- Exponentielles Volumenwachstum
- "Weitläufigkeit"

**Positive Krümmung** ist typisch für sphärische Geometrie:

- Kleine Abstände
- Kompaktheit
- "Gebundenheit"

**Hypothese:** Asymmetrische Bäume (große $M_C$) sind in negativ gekrümmten Regionen.

---

## Nullmodell

**H0:** Krümmung und Catalan-Magic sind **unabhängig**:

$$\operatorname{corr}(M_C, \kappa_C) = 0$$

**Test:** Berechne Krümmung für alle Bäume in $\mathcal{T}_k$ und teste Korrelation.

---

## Teststatistik

Für $k \in \{3, 4, 5, 6\}$ (kleine Werte für Vollständigkeit):

1. Berechne für jeden Baum $T \in \mathcal{T}_k$:

   - $M_C(T) = \min_{B \in \mathcal{B}_k} d_C(T, B)$
   - $\kappa_C(T)$: mittlere Ollivier-Ricci-Krümmung an den Nachbarn von $T$

2. Berechne Korrelation:

   $$\rho_k = \operatorname{corr}\left(\{M_C(T)\}_{T \in \mathcal{T}_k}, \{-\kappa_C(T)\}_{T \in \mathcal{T}_k}\right)$$

**Kriterium:**

$$\rho_k > 0.5 \quad \text{für alle } k$$

---

## Implementierung

```python
def test_curvature_correlation(k_max=6):
    results = {}
    
    for k in range(3, k_max+1):
        # Alle Bäume mit k Blättern
        trees = generate_all_trees(k)
        
        # Tamari-Graph
        G = construct_tamari_graph(trees)
        
        # Catalan-Magic
        M_C = [min_distance_to_balanced(T) for T in trees]
        
        # Ollivier-Ricci-Krümmung
        kappa = ollivier_ricci_curvature(G)
        
        # Mittlere Krümmung pro Baum (über Nachbarn)
        kappa_mean = []
        for T in trees:
            neighbors = G.neighbors(T)
            kappa_T = np.mean([kappa[(T, N)] for N in neighbors])
            kappa_mean.append(kappa_T)
        
        # Korrelation
        rho = np.corrcoef(M_C, [-k for k in kappa_mean])[0,1]
        
        results[k] = {
            'rho': rho,
            'significant': rho > 0.5
        }
    
    # Durchschnittliche Korrelation
    avg_rho = np.mean([results[k]['rho'] for k in range(3, k_max+1)])
    
    return {
        'results_by_k': results,
        'avg_rho': avg_rho,
        'valid': avg_rho > 0.5
    }
```

---

## Erwartetes Resultat

- **Falls korreliert:** $\rho > 0.5$ (asymmetrische Bäume haben negative Krümmung)
- **Falls unkorreliert:** $\rho \approx 0$

---

## Konsequenzen

- **Signifikant:** Die Catalan-Hierarchie ist ein **geometrisches** Phänomen (Krümmung erklärt Komplexität)
- **Nicht signifikant:** Krümmung ist unabhängig von der Balance-Struktur

---

## Erweiterte Tests

### Test 8a: Forman-Ricci-Krümmung

Teste auch mit **Forman-Krümmung**:

$$\kappa_F(T) = \sum_{e \in \mathrm{Edges}(T)} \kappa_F(e)$$

---

### Test 8b: Lokale vs. globale Krümmung

Unterscheide:

- **Lokale Krümmung:** Krümmung der Kanten um $T$
- **Globale Krümmung:** Mittlere Krümmung auf geodätischen Pfaden von $T$ zu $\mathcal{B}_k$

---

## Literatur

- Ollivier-Ricci curvature: Ollivier (2009), *Ricci curvature of Markov chains*.
- Forman curvature: Forman (2003), *Bochner's method for cell complexes*.
- Discrete curvature on graphs: Lim et al. (2019), *Hodge Laplacians on graphs*.
