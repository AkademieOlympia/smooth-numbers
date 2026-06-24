# Hypothese H0.5: Schalenstabilität

**Status:** Neue Hypothese (geometrische Vereinheitlichung)  
**Priorität:** Zwischen H0 und H1  
**Typ:** Strukturhypothese

---

## Formulierung

Für zwei Zahlen in derselben **Schale**:

$$S(n_1) = S(n_2)$$

sollte die Tamari-Distanz ihrer Catalan-Bäume **typischerweise klein** sein:

$$\mathbb{E}[d_C(T(n_1), T(n_2)) \mid S(n_1) = S(n_2)] < \mathbb{E}[d_C(T(n_1), T(n_2))]$$

---

## Was ist eine Schale?

**Definition:**

$$S(n) = \Omega(n) \quad \text{(Anzahl Primfaktoren mit Vielfachheit)}$$

oder allgemeiner ein Maß für Faktorisierungskomplexität:

- $S(n) = \log(n)$ (logarithmische Schale)
- $S(n) = \sigma(n)$ (glatte Komponente)
- $S(n) = \omega(n)$ (distinkte Primfaktoren)

**Interpretation:** Die Schale ist die **radiale Koordinate** der Zahl - sie misst "Abstand vom Ursprung" in logarithmischer Skala.

---

## Interpretation

### Falls H0.5 erfüllt:

$$\text{Schale} = \text{makroskopische Koordinate}$$

- Catalan-Hierarchie **respektiert** Schalenstruktur
- Zahlen gleicher Komplexität haben ähnliche Bäume
- Renormalization-Group-artige Beschreibung möglich

### Falls H0.5 verletzt:

- Schale ist **irrelevant** für Catalan
- Nur Mikro-Details (exakte Primfaktoren) zählen
- Keine Vereinfachung durch Grobkörnung möglich

---

## Nullmodell

**H0.5-Null:**

$$d_C(T(n_1), T(n_2))$$ ist **unabhängig** von $S(n_1), S(n_2)$.

**Test:** Permutiere Schalen-Zuordnungen und vergleiche.

---

## Teststatistik

Für ein Ensemble $\mathcal{N}$, stratifiziert nach Schalen $S = 1, 2, \ldots, S_{\max}$:

$$\text{Var}_{\text{within}} = \frac{1}{|\mathcal{N}|} \sum_{n_1, n_2: S(n_1) = S(n_2)} d_C(T(n_1), T(n_2))^2$$

$$\text{Var}_{\text{between}} = \frac{1}{|\mathcal{N}|} \sum_{n_1, n_2: S(n_1) \neq S(n_2)} d_C(T(n_1), T(n_2))^2$$

**Kriterium:**

$$\frac{\text{Var}_{\text{within}}}{\text{Var}_{\text{between}}} < 0.8$$

Falls die intra-Schalen-Varianz signifikant kleiner ist, ist H0.5 erfüllt.

---

## Implementierung

```python
def test_H0_5_shell_stability(numbers, canonization='balanced'):
    """
    Testet H0.5: Schalenstabilität.
    """
    # Berechne Schalen und Bäume
    shells = [omega(n) for n in numbers]
    trees = [construct_tree(n, canonization) for n in numbers]
    
    # Grupiere nach Schalen
    shell_groups = {}
    for n, s, t in zip(numbers, shells, trees):
        shell_groups.setdefault(s, []).append((n, t))
    
    # Intra-Schalen-Distanz
    dist_within = []
    for s, group in shell_groups.items():
        if len(group) < 2:
            continue
        for i, (n1, t1) in enumerate(group):
            for n2, t2 in group[i+1:]:
                dist_within.append(tamari_distance(t1, t2))
    
    # Inter-Schalen-Distanz
    dist_between = []
    shell_list = list(shell_groups.items())
    for i, (s1, group1) in enumerate(shell_list):
        for s2, group2 in shell_list[i+1:]:
            for n1, t1 in group1:
                for n2, t2 in group2:
                    dist_between.append(tamari_distance(t1, t2))
                    if len(dist_between) > 10000:  # Sample
                        break
    
    # Statistik
    var_within = np.var(dist_within)
    var_between = np.var(dist_between)
    ratio = var_within / var_between
    
    return {
        'var_within': var_within,
        'var_between': var_between,
        'ratio': ratio,
        'H0_5_fulfilled': ratio < 0.8,
        'mean_within': np.mean(dist_within),
        'mean_between': np.mean(dist_between)
    }
```

---

## Erwartetes Resultat

**Falls H0.5 erfüllt:**
- $\text{Var}_{\text{within}} \ll \text{Var}_{\text{between}}$
- Zahlen gleicher Schale haben ähnliche Catalan-Hierarchie
- Schale ist relevante makroskopische Variable

**Falls H0.5 verletzt:**
- $\text{Var}_{\text{within}} \approx \text{Var}_{\text{between}}$
- Schale enthält keine Information über Hierarchie
- Volle Faktorisierung nötig

---

## Verbindung zu H0 (Kanonisierung)

H0.5 **verbessert** H0, indem es eine geometrisch informierte Kanonisierung ermöglicht:

**Ohne H0.5 (alt):**
$$\kappa: n \to T(n)$$

**Mit H0.5 (neu):**
$$\kappa: (S(n), v(n)) \to T(n)$$

Die Kanonisierung kann die **Schale nutzen** als erste Grobkörnung.

---

## Lean-Formalisierung

```lean
/-- Schale einer Zahl als Komplexitätsmaß. -/
def shell (n : Nat) : Nat :=
  omega n  -- oder andere Maße

/-- H0.5: Schalenstabilität. -/
def H0_5_ShellStability : Prop :=
  ∃ δ : ℝ, ∀ n₁ n₂ : Nat,
    shell n₁ = shell n₂ →
    𝔼[tamari_dist (T n₁) (T n₂)] < δ

/-- Stärkere Version: Geometrische Kanonisierung. -/
structure ShellAwareCanonization extends Canonization where
  respects_shell : ∀ n₁ n₂ : Nat,
    shell n₁ = shell n₂ →
    tamari_dist (canon n₁) (canon n₂) <
    tamari_dist (canon n₁) (canon n₃)  -- n₃ aus anderer Schale
```

---

## Konsequenzen

### Falls H0.5 bestätigt:

- **Vereinfachung:** Catalan-Magic ist Funktion von $(S, \ldots)$
- **RG-Struktur:** Schalen sind Grobkörnung
- **Interpretierbarkeit:** Makroskopische Variable

### Falls H0.5 falsifiziert:

- **Komplexität:** Volle Mikrostruktur nötig
- **Keine Vereinfachung:** Schale ist Artefakt
- **Schwierigere Theorie:** Mehr Parameter

---

## Zusammenfassung

H0.5 testet, ob die **Schalenstruktur** aus der EABC-Arbeit für Catalan-Hierarchien relevant ist.

**Priorität:** Sehr hoch - fundamentale Strukturfrage  
**Test:** E02b (nach E02a Kanonisierung)  
**Kriterium:** Varianz-Ratio < 0.8
