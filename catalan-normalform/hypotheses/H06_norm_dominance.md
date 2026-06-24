# Hypothese H0.6: Vektornorm-Dominanz

**Status:** Neue Hypothese (geometrische Vereinheitlichung)  
**Priorität:** Fundamental  
**Typ:** Vereinfachungshypothese

---

## Die zentrale Frage

Ist Catalan-Magic eine Funktion der **geometrischen Struktur** $(S, v, ||v||)$ statt der rohen Faktorisierung?

$$\boxed{M_C(n) \stackrel{?}{=} F(S(n), v(n), ||v(n)||)}$$

---

## Formulierung

Die EABC-Vektornorm $||v_{\text{EABC}}(n)||^2$ liefert **zusätzliche Vorhersagekraft** für Catalan-Magic über $\Omega(n), \sigma(n), (v_2, v_3)$ hinaus.

### Präzise Teststatistik

$$\Delta R^2_{\text{norm}} = R^2_{\Omega, (v_2,v_3), ||v||^2} - R^2_{\Omega, (v_2,v_3)} > \eta$$

wobei:

$$||v_{\text{EABC}}(n)||^2 = e(n)^2 + a(n)^2 + b(n)^2 + c(n)^2$$

und $v(n) = (e, a, b, c)$ der EABC-Vektor für Primfaktoren $p > 3$ ist.

---

## Was ist der EABC-Vektor?

**Definition:**

Für $n = \prod_i p_i$ mit Primfaktoren:

$$v(n) = (e, a, b, c) \in \mathbb{N}^4$$

wobei:

- $e$: Anzahl Faktoren mit $p \equiv 1 \pmod{12}$
- $a$: Anzahl Faktoren mit $p \equiv 5 \pmod{12}$
- $b$: Anzahl Faktoren mit $p \equiv 7 \pmod{12}$
- $c$: Anzahl Faktoren mit $p \equiv 11 \pmod{12}$

**Beispiel 1:**

$$n = 5 \cdot 7 \cdot 13 \cdot 23 = A \cdot B \cdot E \cdot C$$

$$v_{\text{fac}}(n) = (1, 1, 1, 1) \quad \Rightarrow \quad ||v(n)||^2 = 4$$

**Beispiel 2:**

$$n = 60 = 2^2 \cdot 3 \cdot 5$$

Hier: $(v_2, v_3) = (2, 1)$ gehören zur Schale, nur die 5 zählt für EABC:

$$v_{\text{fac}}(60) = (0, 1, 0, 0) \quad \Rightarrow \quad ||v(60)||^2 = 1$$

---

## Die Norm als zentrale Größe

**Interpretation:**

$$||v(n)|| = \text{geometrische Größe des EABC-Vektors}$$

Dies ist ein **makroskopisches Maß** für die EABC-Komplexität.

**Analogi zu Physik:**

- Vektor $\vec{v}$: Richtung
- Norm $||\vec{v}||$: Größe
- Catalan $T$: Hierarchie

---

## Hypothese H0.6

**Kernaussage:**

$$\boxed{||v_{\text{fac}}||^2 \text{ liefert zusätzliche Vorhersagekraft gegenüber } \Omega, \sigma, (v_2, v_3)}$$

**Formale Version:**

$$\Delta R^2_{\text{norm}} = R^2(\text{M3}) - R^2(\text{M2}) > \eta$$

wobei:
- **M2:** $M_C \sim \Omega + (v_2, v_3)$
- **M3:** $M_C \sim \Omega + (v_2, v_3) + ||v_{\text{fac}}||^2$
- $\eta$: Schwellenwert (z.B. 0.05)

**Interpretation:** Die Norm ist nicht redundant zu bereits vorhandenen Koordinaten.

---

## Nullmodell

**H0.6-Null:**

$$M_C(n)$$ ist **unabhängig** von $N_{\text{EABC}}(n)$ nach Kontrolle für $\Omega(n)$.

**Test:** Permutiere EABC-Vektoren bei festem $\Omega$ und prüfe, ob Korrelation verschwindet.

---

## Teststatistik

Für ein Ensemble $\mathcal{N}$:

1. Berechne $M_C(n)$ und $N_{\text{EABC}}(n)$ für alle $n \in \mathcal{N}$
2. Residualisiere beide gegen $\Omega(n)$:
   $$M_C^{\text{res}}(n) = M_C(n) - \mathbb{E}[M_C \mid \Omega(n)]$$
   $$N_{\text{EABC}}^{\text{res}}(n) = N_{\text{EABC}}(n) - \mathbb{E}[N_{\text{EABC}} \mid \Omega(n)]$$

3. Berechne Korrelation:
   $$\rho = \operatorname{corr}(M_C^{\text{res}}, N_{\text{EABC}}^{\text{res}})$$

**Kriterium:**

- $\Delta R^2 > 0.10$: **Stark** - Norm ist wichtige Größe
- $0.05 < \Delta R^2 < 0.10$: **Moderat** - Norm hat Zusatzinfo
- $\Delta R^2 < 0.05$: **Schwach** - Norm ist redundant (H0.6 verletzt)

---

## Implementierung

```python
def compute_eabc_norm(n):
    """Berechnet die EABC-Vektornorm."""
    factors = prime_factors(n)
    e = sum(1 for p in factors if p > 3 and p % 12 == 1)
    a = sum(1 for p in factors if p > 3 and p % 12 == 5)
    b = sum(1 for p in factors if p > 3 and p % 12 == 7)
    c = sum(1 for p in factors if p > 3 and p % 12 == 11)
    return np.sqrt(e**2 + a**2 + b**2 + c**2)

def test_H0_6_norm_dominance(numbers, canonization='balanced'):
    """
    Testet H0.6: Vektornorm liefert zusätzliche Vorhersagekraft.
    """
    # Berechne Observablen
    M_C = np.array([catalan_magic(n, canonization) for n in numbers])
    omega_vals = np.array([omega(n) for n in numbers])
    shell_bases = np.array([shell_base(n) for n in numbers])  # (v₂, v₃)
    norm_sq = np.array([compute_eabc_norm(n)**2 for n in numbers])
    
    # M2: Ω + (v₂, v₃)
    X_M2 = np.column_stack([omega_vals, shell_bases])
    R2_M2 = compute_R2(M_C, X_M2)
    
    # M3: Ω + (v₂, v₃) + ||v||²
    X_M3 = np.column_stack([omega_vals, shell_bases, norm_sq])
    R2_M3 = compute_R2(M_C, X_M3)
    
    # Delta R²
    Delta_R2 = R2_M3 - R2_M2
    
    # Bootstrap-Konfidenzintervall
    Delta_R2_bootstrap = []
    for _ in range(1000):
        idx = np.random.choice(len(numbers), len(numbers), replace=True)
        M_C_boot = M_C[idx]
        X_M2_boot = X_M2[idx]
        X_M3_boot = X_M3[idx]
        R2_M2_boot = compute_R2(M_C_boot, X_M2_boot)
        R2_M3_boot = compute_R2(M_C_boot, X_M3_boot)
        Delta_R2_bootstrap.append(R2_M3_boot - R2_M2_boot)
    
    # Konfidenzintervall
    CI_lower = np.percentile(Delta_R2_bootstrap, 2.5)
    CI_upper = np.percentile(Delta_R2_bootstrap, 97.5)
    
    return {
        'R2_M2': R2_M2,
        'R2_M3': R2_M3,
        'Delta_R2': Delta_R2,
        'CI_95': (CI_lower, CI_upper),
        'H0_6_fulfilled': Delta_R2 > 0.05 and CI_lower > 0,
        'strength': 'strong' if Delta_R2 > 0.10 else 'moderate' if Delta_R2 > 0.05 else 'weak'
    }
```

---

## Erwartetes Resultat

### Szenario A: Starke Zusatzinformation ($\Delta R^2 > 0.10$)

$$\boxed{M_C(n) \approx F(\Omega, (v_2, v_3), ||v_{\text{fac}}||^2)}$$

**Konsequenz:** Die Norm ist eine wichtige geometrische Größe.

Catalan-Magic nutzt die SVN-Koordinaten direkt.

**Dann:** Kanonisierung sollte Norm einbeziehen:

$$\kappa: (\Omega, (v_2, v_3), ||v||) \to T$$

---

### Szenario B: Moderate Zusatzinformation ($0.05 < \Delta R^2 < 0.10$)

**Konsequenz:** Die Norm trägt bei, ist aber nicht dominant.

Möglicherweise ist die volle Vektorrichtung $v$ relevanter.

**Dann:** Teste M4 vs. M3 (Vektor vs. Norm):

$$\Delta_{\text{dir}} = R^2(\text{M4}) - R^2(\text{M3})$$

---

### Szenario C: Keine Zusatzinformation ($\Delta R^2 < 0.05$)

**Konsequenz:** Die Norm ist redundant.

$\Omega$ und $(v_2, v_3)$ reichen aus.

**Dann:** Vereinfachte Kanonisierung:

$$\kappa: (\Omega, (v_2, v_3)) \to T$$

---

## Verbindung zu Hurwitz

Falls H0.6 erfüllt ist, wird die **Hurwitz-Erweiterung natürlich**:

### Die EABC-Norm ist quaternionisch kompatibel

Der EABC-Vektor $v = (e, a, b, c) \in \mathbb{R}^4 \cong \mathbb{H}$ besitzt die Quaternionen-Norm:

$$||v||^2_{\mathbb{H}} = e^2 + a^2 + b^2 + c^2$$

**Aber:** Die volle Hurwitz-Struktur beginnt erst bei **Produkten** und **Assoziatoren**, nicht nur bei Normen.

Solange wir nur $||v||$ betrachten, arbeiten wir in $\mathbb{R}^4$ mit euklidischer Norm.

**Die Quaternionenstruktur wird erst relevant bei:**

- Produkten: $v_L \cdot v_R$ in $\mathbb{H}$
- Assoziatoren: $[v_L, v_M, v_R]$ in $\mathbb{O}$

**Dann wird die Hierarchie:**

```
EABC-Vektor v ∈ ℝ⁴ ≅ ℍ
  ↓
Norm ||v|| (Quaternionen-kompatibel)
  ↓
Catalan T (Hierarchie)
  ↓
Produkte v₁ · v₂ in ℍ
  ↓
Assoziatoren [·,·,·] in 𝕆
```

**Hurwitz ist algebraische Fortsetzung der Normgeometrie!**

---

## Lean-Formalisierung

```lean
/-- EABC-Vektor als 4-Tupel. -/
structure EABCVector where
  e : Nat
  a : Nat
  b : Nat
  c : Nat

/-- Norm des EABC-Vektors. -/
def eabc_norm (v : EABCVector) : ℝ :=
  Real.sqrt (v.e^2 + v.a^2 + v.b^2 + v.c^2 : ℝ)

/-- H0.6: Vektornorm-Dominanz. -/
def H0_6_NormDominance : Prop :=
  ∃ F : Nat → (Nat × Nat) → ℝ → ℝ, ∀ n : Nat,
    let omega := omega n
    let base := shellBase n
    let norm_sq := (factorEABCVector n).normSq
    |catalan_magic n - F omega base norm_sq| < ε

/-- Schwächere Version: Zusätzliche Vorhersagekraft. -/
def H0_6_Incremental : Prop :=
  ∃ η > 0, ΔR²_norm > η  -- Norm trägt Information bei
```

---

## Konsequenzen

### Falls H0.6 bestätigt ($\Delta R^2 > \eta$):

- **Geometrische Größe:** Norm ist relevant für Catalan-Magic
- **SVN-Integration:** Catalan nutzt EABC-Koordinaten
- **Hurwitz-Kompatibilität:** Algebraische Fortsetzung möglich
- **Testbare Vorhersage:** M3 erklärt mehr als M2

### Falls H0.6 verletzt ($\Delta R^2 < \eta$):

- **Redundante Norm:** $||v||^2$ ist nicht informativ
- **Vereinfachte Basis:** Nur $\Omega$ und $(v_2, v_3)$ nötig
- **Hurwitz weniger natürlich:** Norm ist nicht zentral

---

## Zusammenfassung

H0.6 ist die **zentrale Zusatzinformations-Hypothese**:

$$\boxed{\text{Liefert } ||v_{\text{fac}}||^2 \text{ Vorhersagekraft über } \Omega, (v_2, v_3) \text{ hinaus?}}$$

**Priorität:** Sehr hoch - fundamentale Strukturfrage  
**Test:** Teil der M0-M4-Kaskade  
**Kriterium:** $\Delta R^2_{\text{norm}} > 0.05$

Falls bestätigt: Die Norm ist eine eigenständige geometrische Größe und die Hurwitz-Fortsetzung wird natürlich!
