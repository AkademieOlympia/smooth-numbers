# Hypothese H0: Kanonisierung (fundamental)

**Status:** Offenes Problem - muss vor H1-H10 gelöst werden!  
**Priorität:** Kritisch  
**Mathematische Qualität:** Kernproblem der Theorie

---

## Das fundamentale Problem

Für eine Zahl wie:

$$60 = 2^2 \cdot 3 \cdot 5 = (2, 2, 3, 5)$$

existieren **mehrere** binäre Bäume:

1. $((2 \cdot 2) \cdot 3) \cdot 5$ - Linksbaum
2. $(2 \cdot 2) \cdot (3 \cdot 5)$ - Teilweise balanciert
3. $2 \cdot (2 \cdot (3 \cdot 5))$ - Rechtsbaum
4. $(2 \cdot (2 \cdot 3)) \cdot 5$
5. $2 \cdot ((2 \cdot 3) \cdot 5)$

Jeder dieser Bäume hat **unterschiedliche** Catalan-Magic $M_C$.

**Problem:** Ohne kanonische Wahl ist $M_C(n)$ **nicht eindeutig definiert**.

---

## H0: Existenz einer kanonischen Abbildung

**Formulierung:**

Es existiert eine kanonische Abbildung

$$\kappa: \mathbb{N}_{\geq 2} \to \bigcup_{k=1}^\infty \mathcal{T}_k$$

mit

$$n \mapsto T(n) \in \mathcal{T}_{\Omega(n)}$$

die folgende Eigenschaften besitzt:

### 1. Determinismus

$$\forall n: \kappa(n) \text{ ist eindeutig}$$

### 2. Faktorisierungsinvarianz

$$\text{Gleiche Primfaktoren (mit Vielfachheit)} \Rightarrow \text{gleicher Baum}$$

Formal:
$$\text{factors}(n_1) = \text{factors}(n_2) \Rightarrow \kappa(n_1) = \kappa(n_2)$$

### 3. Stabilität unter kleinen Änderungen

$$d_{\text{factors}}(n_1, n_2) \text{ klein} \Rightarrow d_C(\kappa(n_1), \kappa(n_2)) \text{ klein}$$

wobei $d_{\text{factors}}$ eine geeignete Metrik auf Faktorlisten ist.

---

## Warum H0 fundamental ist

**Ohne H0:**

- $M_C(n)$ ist nicht wohldefiniert
- H1 (Kanonische Stabilität) ist zirkulär
- H10-Test nicht durchführbar

**Mit H0:**

- $M_C(n) = M_C(\kappa(n))$ ist eindeutig
- H1 testet verschiedene kanonische Wahlen
- Alle folgenden Hypothesen werden testbar

---

## Drei natürliche Kandidaten

### Kandidat 1: Linksbaum $\kappa_L$

```
kappa_L([p1, p2, ..., pk]) = (((...((p1, p2), p3), ...), pk)
```

**Vorteile:**
- Deterministisch ✓
- Einfach zu definieren ✓

**Nachteile:**
- Maximal unbalanciert (Höhe = k-1)
- Keine Stabilität unter Faktoränderungen

---

### Kandidat 2: Rechtsbaum $\kappa_R$

```
kappa_R([p1, p2, ..., pk]) = (p1, (p2, (..., (pk-1, pk)...)))
```

**Vorteile:**
- Deterministisch ✓
- Einfach zu definieren ✓

**Nachteile:**
- Maximal unbalanciert (Höhe = k-1)
- Keine Stabilität

---

### Kandidat 3: Balancierter Baum $\kappa_B$

```
def kappa_B(factors):
    if len(factors) == 1:
        return Leaf
    mid = len(factors) // 2
    return Node(kappa_B(factors[:mid]), kappa_B(factors[mid:]))
```

**Vorteile:**
- Deterministisch ✓
- Minimale Höhe (balanciert)
- Bessere Stabilität

**Nachteile:**
- Bei ungeradem k: Asymmetrie (links vs. rechts)
- Willkürliche Entscheidung bei Tie

---

## Erweiterte Kandidaten

### Kandidat 4: Größen-basierter Baum $\kappa_{\text{size}}$

Ordne Faktoren nach Größe, balanciere dann:

```
def kappa_size(factors):
    sorted_factors = sorted(factors)
    return kappa_B(sorted_factors)
```

**Problem:** Sortierung ist bereits kanonisch (aufsteigend), aber $2^3 \cdot 5$ vs. $2 \cdot 2^2 \cdot 5$?

---

### Kandidat 5: Produktbalancierter Baum $\kappa_{\text{prod}}$

Minimiere Ungleichgewicht der Teilprodukte:

```
def kappa_prod(factors):
    # Finde Split, der log(prod(left)) ≈ log(prod(right)) maximiert
    best_split = argmin(abs(log(prod(left)) - log(prod(right))))
    return Node(kappa_prod(left), kappa_prod(right))
```

**Vorteil:** Berücksichtigt Primgrößen  
**Nachteil:** Rechenaufwändig (NP-schwer für optimale Balance)

---

### Kandidat 6: EABC-informierter Baum $\kappa_{\text{EABC}}$

Nutze EABC-Signatur zur Strukturierung:

```
def kappa_EABC(factors):
    # Gruppiere nach EABC-Klassen
    E_factors = [p for p in factors if eabc(p) == 'E']
    A_factors = [p for p in factors if eabc(p) == 'A']
    # ... balanciere innerhalb Gruppen
```

**Problem:** Zirkulär - setzt EABC-Struktur bereits voraus

---

## Test von H0: Vergleich der Kandidaten

Um H0 zu testen, sollte E02 folgendes messen:

### Test 1: Korrelation zwischen Kanonisierungen

$$\rho = \operatorname{corr}(M_C^{\kappa_L}, M_C^{\kappa_R})$$

**Erwartung:** 
- Falls $\rho > 0.7$: Kanonisierung ist robust → H0 erfüllt
- Falls $\rho < 0.3$: Kanonisierung dominiert → H0 verletzt

---

### Test 2: Ensemble-Konsistenz

Für jedes $n$, berechne:

$$\overline{M}_C(n) = \frac{1}{|\mathcal{T}_{\Omega(n)}|} \sum_{T \in \mathcal{T}_{\Omega(n)}} M_C(T)$$

(Magic über **alle** möglichen Bäume mit den Faktoren von $n$)

Dann teste:

$$\operatorname{Var}(\{\overline{M}_C(n)\}_{n \in \mathcal{N}}) \stackrel{?}{>} 0$$

Falls die Ensemble-Mittelung die Varianz auslöscht, ist die Klammerungswahl irrelevant.

---

### Test 3: Residuen-Korrelation

Für zwei Kanonisierungen $\kappa_1, \kappa_2$:

$$M_C^{\text{res},\kappa_1}(n) = M_C^{\kappa_1}(n) - \mathbb{E}[M_C^{\kappa_1} \mid \Omega(n)]$$

$$M_C^{\text{res},\kappa_2}(n) = M_C^{\kappa_2}(n) - \mathbb{E}[M_C^{\kappa_2} \mid \Omega(n)]$$

**Teste:**

$$\operatorname{corr}(M_C^{\text{res},\kappa_1}, M_C^{\text{res},\kappa_2}) \stackrel{?}{>} 0.5$$

Falls die **Residuen** korreliert sind, gibt es arithmetische Information jenseits der Kanonisierung.

---

## Lean-Formalisierung von H0

```lean
/-- Eine Kanonisierung ist eine deterministische Abbildung von Zahlen zu Bäumen. -/
structure Canonization where
  /-- Ordnet einer Faktorliste einen eindeutigen Baum zu. -/
  canon : (factors : List Nat) → CTree factors.length
  
  /-- Determinismus: Gleiche Faktoren → gleicher Baum. -/
  deterministic : ∀ fs₁ fs₂ : List Nat,
    fs₁ = fs₂ → canon fs₁ = canon fs₂
  
  /-- Permutations-Invarianz (optional, strenger). -/
  permutation_invariant : ∀ fs₁ fs₂ : List Nat,
    fs₁.toFinset = fs₂.toFinset →
    canon fs₁ = canon fs₂

/-- H0: Es existiert eine "gute" Kanonisierung. -/
def H0_CanonizationExists : Prop :=
  ∃ κ : Canonization,
    -- Stabilität (formalisiert als Lipschitz-Bedingung)
    ∀ n₁ n₂ : Nat,
      let fs₁ := prime_factors n₁
      let fs₂ := prime_factors n₂
      factor_distance fs₁ fs₂ < ε →
      tamari_dist (κ.canon fs₁) (κ.canon fs₂) < δ
```

---

## Entscheidung für E02

**E02 sollte testen:**

1. Korrelation $\rho(\kappa_L, \kappa_R, \kappa_B)$
2. Ensemble-Mittelung $\overline{M}_C(n)$
3. Residuen-Korrelation

**Kriterium für H0:**

Falls **mindestens zwei** der drei natürlichen Kanonisierungen ($\kappa_L, \kappa_R, \kappa_B$) 
Residuen mit $\rho > 0.5$ liefern, ist H0 erfüllt.

Falls alle drei unkorreliert sind ($\rho < 0.3$), ist H0 verletzt → Projekt abbrechen.

---

## Konsequenzen

### Falls H0 verletzt:

Das gesamte Programm kollabiert:
- $M_C(n)$ ist nicht wohldefiniert
- Kanonisierung dominiert arithmetische Struktur
- **Ehrliches Nullresultat:** "Catalan-Hierarchie ist Kanonisierungs-Artefakt"

### Falls H0 erfüllt:

- Wähle die stabilste Kanonisierung (vermutlich $\kappa_B$)
- Fahre fort mit H10-Test
- Alle folgenden Hypothesen werden testbar

---

## Implementierung in E02

```python
def test_H0(numbers, n_permutations=1000):
    """
    Testet H0: Existenz robuster Kanonisierung.
    """
    # Berechne Magic für drei Kanonisierungen
    M_left = [catalan_magic(n, canon='left') for n in numbers]
    M_right = [catalan_magic(n, canon='right') for n in numbers]
    M_balanced = [catalan_magic(n, canon='balanced') for n in numbers]
    
    # Korrelationen
    corr_LR = np.corrcoef(M_left, M_right)[0, 1]
    corr_LB = np.corrcoef(M_left, M_balanced)[0, 1]
    corr_RB = np.corrcoef(M_right, M_balanced)[0, 1]
    
    # Residuen
    omega_vals = [omega(n) for n in numbers]
    M_left_res = residualize(M_left, omega_vals)
    M_right_res = residualize(M_right, omega_vals)
    M_balanced_res = residualize(M_balanced, omega_vals)
    
    corr_LR_res = np.corrcoef(M_left_res, M_right_res)[0, 1]
    corr_LB_res = np.corrcoef(M_left_res, M_balanced_res)[0, 1]
    corr_RB_res = np.corrcoef(M_right_res, M_balanced_res)[0, 1]
    
    # Entscheidung
    H0_fulfilled = (corr_LR_res > 0.5 or 
                    corr_LB_res > 0.5 or 
                    corr_RB_res > 0.5)
    
    return {
        'corr_raw': (corr_LR, corr_LB, corr_RB),
        'corr_residual': (corr_LR_res, corr_LB_res, corr_RB_res),
        'H0_fulfilled': H0_fulfilled,
        'best_canonization': 'balanced' if corr_LB_res > max(corr_LR_res, corr_RB_res) else 'left'
    }
```

---

## Status: Offenes Problem

H0 ist **nicht gelöst**, aber **testbar**.

**Nächster Schritt:**

E02 muss erweitert werden zu:
- **E02a:** Kanonisierungstest (H0)
- **E02b:** Stabilität der gewählten Kanonisierung (H1)

---

## Zusammenfassung

$$\boxed{\text{H0 ist fundamental: Ohne kanonische Abbildung } n \mapsto T(n) \text{ ist } M_C(n) \text{ nicht wohldefiniert}}$$

**Priorität:** Vor H1-H10  
**Test:** E02a  
**Kriterium:** Residuen-Korrelation $\rho > 0.5$ zwischen mindestens zwei Kanonisierungen

Falls H0 verletzt: **Projekt abbrechen** (Kanonisierungs-Artefakt)  
Falls H0 erfüllt: **Weiter mit H10** (arithmetische Struktur vorhanden)
