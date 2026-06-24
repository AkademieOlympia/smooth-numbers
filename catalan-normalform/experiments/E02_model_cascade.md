# Experiment E02: Modellkaskade M0-M4

**Status:** Geplant  
**Priorität:** Hoch  
**Typ:** Eliminationsarchitektur

---

## Zielsetzung

Systematisches Testen, wie viel der Varianz von Catalan-Magic $M_C(n)$ durch sukzessive reichere arithmetische Koordinaten erklärt wird.

**Kernfrage:**

$$\boxed{\text{Wie viel von } M_C(n) \text{ ist durch SVN-Koordinaten erklärbar?}}$$

---

## Die Modellhierarchie

Wir testen sechs sukzessive reichere Modelle:

$$
\begin{align*}
\text{M0:} \quad & M_C(n) \sim \Omega(n) \\
\text{M0b:} \quad & M_C(n) \sim \Omega(n) + \Omega(n)^2 \\
\text{M1:} \quad & M_C(n) \sim \Omega(n) + \Omega(n)^2 + \sigma(n) \\
\text{M2:} \quad & M_C(n) \sim \Omega(n) + \Omega(n)^2 + (v_2(n), v_3(n)) \\
\text{M3:} \quad & M_C(n) \sim \Omega(n) + \Omega(n)^2 + (v_2(n), v_3(n)) + ||v_{\text{fac}}(n)||^2 \\
\text{M4:} \quad & M_C(n) \sim \Omega(n) + \Omega(n)^2 + (v_2(n), v_3(n)) + v_{\text{fac}}(n)
\end{align*}
$$

### Warum M0b kritisch ist

**Problem:** Viele kombinatorische Größen wachsen nicht linear in $\Omega$.

Catalan-Strukturen könnten mit der Anzahl möglicher Faktorisierungsbäume zusammenhängen, wo oft Terme wie

$$\Omega^2, \quad \Omega \log \Omega, \quad C_\Omega$$

auftreten.

**Ohne M0b:** Man könnte einen scheinbaren Normeffekt messen, der in Wahrheit nur ein nichtlinearer $\Omega$-Effekt ist.

**Mit M0b:** Schließt aus, dass $\Delta R^2_{\text{norm}}$ nur nichtlineare $\Omega$-Abhängigkeiten misst.

---

## Arithmetische Koordinaten

**Ω(n):** Anzahl Primfaktoren mit Vielfachheit

**σ(n):** Summe der Teiler (alternative Komplexitätsmaß)

**(v₂(n), v₃(n)):** Schalen-Basis
- $v_2(n)$: 2-adische Bewertung
- $v_3(n)$: 3-adische Bewertung

**v_fac(n) = (e, a, b, c):** EABC-Faktor-Vektor für Primfaktoren $p > 3$
- $e$: Anzahl Faktoren mit $p \equiv 1 \pmod{12}$
- $a$: Anzahl Faktoren mit $p \equiv 5 \pmod{12}$
- $b$: Anzahl Faktoren mit $p \equiv 7 \pmod{12}$
- $c$: Anzahl Faktoren mit $p \equiv 11 \pmod{12}$

**||v_fac(n)||²:** Quadrierte euklidische Norm
$$||v_{\text{fac}}(n)||^2 = e^2 + a^2 + b^2 + c^2$$

**H(n):** Dimensionslose Konzentration (bevorzugt für M3*)
$$H(n) = \frac{||v_{\text{fac}}(n)||^2}{(e+a+b+c)^2}$$

Dies ist ein **Konzentrationsmaß** äquivalent zu:
- Simpson-Index (Ökologie)
- Herfindahl-Hirschman-Index (Ökonomie)
- Rényi-Entropie Ordnung 2 (Informationstheorie)

**Wertebereich:** $H \in [1/4, 1]$
- $H = 1$: Maximale Konzentration (alle Faktoren in einer Klasse)
- $H = 1/4$: Maximale Gleichverteilung

**Siehe:** `theory/concentration_measure.md` für Details.

**H(n):** Dimensionslose Konzentration (optional)
$$H(n) = \frac{||v_{\text{fac}}(n)||^2}{\Omega_{\text{EABC}}(n)^2}$$

wobei $\Omega_{\text{EABC}} = e + a + b + c$.

**Interpretation:** $H(n)$ misst die Konzentration der Primfaktoren auf Restklassen.
- $H = 1$: Maximal konzentriert (alle in einer Klasse)
- $H = 1/4$: Maximal verteilt (Gleichverteilung)

Siehe `theory/concentration_measure.md` für Details.

---

## Teststatistiken

Für jedes Modell **Mi** berechnen wir:

1. **R²(Mi):** Bestimmtheitsmaß (erklärte Varianz)
2. **RMSE(Mi):** Root Mean Squared Error
3. **AIC(Mi):** Akaike Information Criterion

### Die zentralen Δ-Werte:

$$\Delta_{\Omega^2} = R^2(\text{M0b}) - R^2(\text{M0})$$

$$\Delta_{\sigma} = R^2(\text{M1}) - R^2(\text{M0b})$$

$$\Delta_{\text{shell}} = R^2(\text{M2}) - R^2(\text{M0b})$$

$$\Delta_{\text{norm}} = R^2(\text{M3}) - R^2(\text{M2})$$

$$\Delta_{\text{dir}} = R^2(\text{M4}) - R^2(\text{M3})$$

**Interpretation:**

- $\Delta_{\Omega^2} > 0.05$: Catalan-Magic wächst nichtlinear in $\Omega$ (wichtig!)
- $\Delta_{\text{norm}} > 0.05$: H0.6 bestätigt (Norm hat Zusatzinfo über $\Omega, \Omega^2, (v_2, v_3)$ hinaus)
- $\Delta_{\text{dir}} > \Delta_{\text{norm}}$: Vektorrichtung wichtiger als Norm
- $R^2(\text{M4}) < 0.95$: Echte Catalan-Residuen bleiben

---

## Implementierung

```python
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error
from scipy import stats

def compute_svn_coordinates(n):
    """Berechnet SVN-Koordinaten für Zahl n."""
    omega = count_prime_factors(n, with_multiplicity=True)
    v2 = padicval(n, 2)
    v3 = padicval(n, 3)
    sigma = sum_of_divisors(n)
    
    # EABC-Vektor (nur p > 3)
    factors = prime_factors(n, with_multiplicity=True)
    e = sum(1 for p in factors if p > 3 and p % 12 == 1)
    a = sum(1 for p in factors if p > 3 and p % 12 == 5)
    b = sum(1 for p in factors if p > 3 and p % 12 == 7)
    c = sum(1 for p in factors if p > 3 and p % 12 == 11)
    v_fac = np.array([e, a, b, c])
    norm_sq = e**2 + a**2 + b**2 + c**2
    
    return {
        'omega': omega,
        'sigma': sigma,
        'v2': v2,
        'v3': v3,
        'v_fac': v_fac,
        'norm_sq': norm_sq
    }

def test_model_cascade(numbers, canonization='balanced'):
    """
    Testet Modellkaskade M0-M4.
    
    Args:
        numbers: Liste von Zahlen
        canonization: Kanonisierungsmethode für Catalan-Bäume
        
    Returns:
        Dictionary mit R²-Werten und Δ-Statistiken
    """
    # Berechne Catalan-Magic für alle Zahlen
    M_C = np.array([catalan_magic(n, canonization) for n in numbers])
    
    # Extrahiere SVN-Koordinaten
    coords = [compute_svn_coordinates(n) for n in numbers]
    omega = np.array([c['omega'] for c in coords])
    sigma = np.array([c['sigma'] for c in coords])
    v2 = np.array([c['v2'] for c in coords])
    v3 = np.array([c['v3'] for c in coords])
    v_fac = np.array([c['v_fac'] for c in coords])
    norm_sq = np.array([c['norm_sq'] for c in coords])
    
    # M0: nur Ω
    X_M0 = omega.reshape(-1, 1)
    model_M0 = LinearRegression().fit(X_M0, M_C)
    R2_M0 = r2_score(M_C, model_M0.predict(X_M0))
    
    # M0b: Ω + Ω² (nichtlineare Kontrolle!)
    omega_sq = omega ** 2
    X_M0b = np.column_stack([omega, omega_sq])
    model_M0b = LinearRegression().fit(X_M0b, M_C)
    R2_M0b = r2_score(M_C, model_M0b.predict(X_M0b))
    
    # M1: Ω + Ω² + σ
    X_M1 = np.column_stack([omega, omega_sq, sigma])
    model_M1 = LinearRegression().fit(X_M1, M_C)
    R2_M1 = r2_score(M_C, model_M1.predict(X_M1))
    
    # M2: Ω + (v₂, v₃)
    X_M2 = np.column_stack([omega, v2, v3])
    model_M2 = LinearRegression().fit(X_M2, M_C)
    R2_M2 = r2_score(M_C, model_M2.predict(X_M2))
    
    # M3: Ω + (v₂, v₃) + ||v||²
    X_M3 = np.column_stack([omega, v2, v3, norm_sq])
    model_M3 = LinearRegression().fit(X_M3, M_C)
    R2_M3 = r2_score(M_C, model_M3.predict(X_M3))
    
    # M4: Ω + (v₂, v₃) + v (voller Vektor)
    X_M4 = np.column_stack([omega, v2, v3, v_fac])
    model_M4 = LinearRegression().fit(X_M4, M_C)
    R2_M4 = r2_score(M_C, model_M4.predict(X_M4))
    
    # Berechne Δ-Werte
    Delta_sigma = R2_M1 - R2_M0
    Delta_shell = R2_M2 - R2_M0
    Delta_norm = R2_M3 - R2_M2
    Delta_dir = R2_M4 - R2_M3
    
    # Bootstrap-Konfidenzintervalle für Δ-Werte
    def bootstrap_delta(X_lower, X_upper, M_C, n_bootstrap=1000):
        deltas = []
        for _ in range(n_bootstrap):
            idx = np.random.choice(len(M_C), len(M_C), replace=True)
            M_boot = M_C[idx]
            X_lower_boot = X_lower[idx]
            X_upper_boot = X_upper[idx]
            
            R2_lower = r2_score(M_boot, 
                                LinearRegression().fit(X_lower_boot, M_boot).predict(X_lower_boot))
            R2_upper = r2_score(M_boot, 
                                LinearRegression().fit(X_upper_boot, M_boot).predict(X_upper_boot))
            deltas.append(R2_upper - R2_lower)
        return np.array(deltas)
    
    Delta_norm_CI = bootstrap_delta(X_M2, X_M3, M_C)
    Delta_dir_CI = bootstrap_delta(X_M3, X_M4, M_C)
    
    # Residuen von M4
    M_C_pred_M4 = model_M4.predict(X_M4)
    residuals_M4 = M_C - M_C_pred_M4
    
    return {
        'R2': {
            'M0': R2_M0,
            'M0b': R2_M0b,
            'M1': R2_M1,
            'M2': R2_M2,
            'M3': R2_M3,
            'M3*': R2_M3_star,
            'M4': R2_M4
        },
        'Delta': {
            'quad': Delta_quad,
            'sigma': Delta_sigma,
            'shell': Delta_shell,
            'norm': Delta_norm,
            'norm_H': Delta_norm_H,
            'dir': Delta_dir
        },
        'CI_95': {
            'norm': (np.percentile(Delta_norm_CI, 2.5), 
                     np.percentile(Delta_norm_CI, 97.5)),
            'dir': (np.percentile(Delta_dir_CI, 2.5), 
                    np.percentile(Delta_dir_CI, 97.5))
        },
        'residuals_M4': {
            'mean': np.mean(residuals_M4),
            'std': np.std(residuals_M4),
            'min': np.min(residuals_M4),
            'max': np.max(residuals_M4)
        },
        'hypotheses': {
            'H0_6_fulfilled': Delta_norm > 0.05 and np.percentile(Delta_norm_CI, 2.5) > 0,
            'direction_matters': Delta_dir > Delta_norm,
            'catalan_residual': R2_M4 < 0.95
        },
        'models': {
            'M0': model_M0,
            'M1': model_M1,
            'M2': model_M2,
            'M3': model_M3,
            'M4': model_M4
        }
    }
```

---

## Erwartete Szenarien

### Szenario A: SVN-Trivialität ($R^2(\text{M4}) > 0.95$)

$$\boxed{M_C(n) \approx F(\Omega, (v_2, v_3), v_{\text{fac}})}$$

**Interpretation:** Catalan-Magic ist vollständig durch SVN-Koordinaten erklärbar.

**Konsequenz:** Keine echten Catalan-Residuen, Theorie reduziert sich auf EABC-Geometrie.

**Dann:** Das ist ein **negatives Resultat** für eigenständige Catalan-Arithmetik, aber ein **starkes Resultat** für die SVN-Struktur!

---

### Szenario B: Norm-Relevanz ($\Delta_{\text{norm}} > 0.05$, $R^2(\text{M4}) < 0.95$)

**Interpretation:** Die Norm $||v_{\text{fac}}||^2$ trägt Information bei, aber es bleiben echte Catalan-Residuen.

**Konsequenz:** 
- H0.6 bestätigt
- SVN-Struktur ist relevant, aber nicht vollständig
- Catalan-Magic hat arithmetischen Eigenanteil

**Dann:** Das ist das **beste Szenario** – sowohl SVN als auch Catalan sind interessant!

---

### Szenario C: Catalan-Dominanz ($\Delta_{\text{norm}} < 0.05$, $R^2(\text{M4}) < 0.80$)

**Interpretation:** Weder Norm noch Vektor erklären viel. Die meiste Varianz ist in Catalan-Residuen.

**Konsequenz:**
- H0.6 verletzt
- SVN-Koordinaten sind nicht zentral
- Catalan-Magic benötigt volle Faktorisierung

**Dann:** Die ursprüngliche Kanonisierung $\kappa: n \to T(n)$ bleibt fundamental.

---

## Interpretation der Resultate

**Methodische Klarstellung:**

Dieser Test entscheidet **nicht** über die Gültigkeit der Gauß-Eisenstein-Interpretation des EABC-Vektors (die ist auf modularer Ebene bereits ein Satz, A-Niveau), sondern über deren **zusätzliche Erklärungskraft** für Catalan-Magic nach Kontrolle der einfacheren Kombinatorik $(\Omega, \Omega^2, (v_2, v_3))$.

### Primäre Testgröße: ΔR²_H

$$\Delta R^2_H = R^2(\text{M3*}) - R^2(\text{M2})$$

wobei **M3*** das Modell mit dem dimensionslosen Konzentrationsmaß H(n) ist (bevorzugt über ||v||²).

**Interpretationsschema:**

| ΔR²_H | Befund | Bedeutung | Konsequenz |
|-------|--------|-----------|------------|
| < 0.01 | **Redundant** | H ist für M_C praktisch irrelevant. M_C ≈ F(Ω, Ω², v₂, v₃). Catalan ist rein kombinatorisch. Gauß-Eisenstein bleibt starke EABC-Interpretation, aber ohne Brücke zu Catalan. | Projekt fokussiert auf EABC selbst, nicht Catalan. |
| 0.01-0.05 | **Schwaches Signal** | Nicht ignorieren, aber vorsichtig. Weitere Tests nötig: größere Stichprobe, Cross-Validation, Permutationstests, stratifizierte Analyse. | Weitere Experimente, keine klare Aussage. |
| 0.05-0.10 | **Moderates Signal** | Spaltungskonzentration hat messbare Erklärungskraft. Erste echte Brücke zwischen algebraischer Zahlentheorie und Catalan-Hierarchie. H0.6 empirisch gestützt. | Publikationswürdig, H0.6 bestätigt. |
| > 0.10 | **Starkes Signal** | Catalan-Magic reagiert auf algebraisch-zahlentheoretische Verteilung. Überraschende tiefe Verbindung. | Hochinteressant, Tamari/Spektraltheorie relevant. |

### Sekundäre Testgröße: ΔR²_dir

$$\Delta R^2_{\text{dir}} = R^2(\text{M4}) - R^2(\text{M3*})$$

**Vergleich ΔR²_H vs. ΔR²_dir:**

- **Falls ΔR²_dir < ΔR²_H:** Konzentration (H) ist wichtiger als Richtung (v)
- **Falls ΔR²_dir > ΔR²_H:** Nicht nur Konzentration, sondern volle EABC-Richtung relevant
- **Falls beide klein:** Catalan ist Ω-dominiert, EABC irrelevant

**Die eigentlich spannende Frage:**

$$\boxed{\text{Ist nur die Konzentration relevant oder die konkrete Richtung im EABC-Raum?}}$$

**Beispiel:** Zwei Zahlen mit v = (4,0,0,0) und v = (0,4,0,0) haben beide H = 1 (maximale Konzentration), aber völlig verschiedene Spaltungstypen. Falls Catalan-Magic zwischen diesen unterscheidet, ist ΔR²_dir groß.

### Szenario 5: Richtung ohne Konzentration

$$\Delta R^2_H \approx 0 \quad \text{aber} \quad \Delta R^2_{\text{dir}} \gg 0$$

**Befund:** Die Konzentration H ist irrelevant, aber die Orientierung (e,a,b,c) selbst ist relevant.

**Interpretation:** Nicht die Konzentration auf Spaltungstypen, sondern **welche** Spaltungstypen dominieren, ist entscheidend.

**Mögliche natürliche Größen:**

Statt H könnten **Projektionen** relevant sein:

1. **Gauß-Spaltungs-Asymmetrie:**
   $$(e + a) - (b + c) = \#\{\text{Gauß-spaltend}\} - \#\{\text{Gauß-inert}\}$$

2. **Eisenstein-Spaltungs-Asymmetrie:**
   $$(e + b) - (a + c) = \#\{\text{Eisenstein-spaltend}\} - \#\{\text{Eisenstein-inert}\}$$

**Das wäre algebraisch-zahlentheoretisch sogar interessanter**, weil es direkte Verbindungen zu Spaltungsasymmetrien in quadratischen Körpern hätte.

**Test:** Falls Szenario 5 eintritt, teste zusätzliche Modelle:
- **M3a:** $M_C \sim \Omega + \Omega^2 + (v_2, v_3) + (\text{Gauß-Asymmetrie})$
- **M3b:** $M_C \sim \Omega + \Omega^2 + (v_2, v_3) + (\text{Eisenstein-Asymmetrie})$

### Stabilitätsprüfung: M0b

**Kritisch:** $\Delta_{\Omega^2} = R^2(\text{M0b}) - R^2(\text{M0})$ zeigt nichtlinearen Ω-Effekt.

Falls $\Delta_{\Omega^2}$ groß ist (> 0.05), sind spätere ΔR² nur glaubwürdig, wenn M0b als Basis verwendet wird. Ohne Ω²-Kontrolle könnte H(n) nur ein verkappter Ω²-Effekt sein.

---

## Entscheidungskriterien

Nach diesem Experiment:

1. **Falls $\Delta_{\text{norm}} > 0.10$:**
   - H0.6 **stark bestätigt**
   - Weiter mit Hurwitz-Erweiterung (H11)
   - Norm ist zentrale Größe

2. **Falls $0.05 < \Delta_{\text{norm}} < 0.10$:**
   - H0.6 **moderat bestätigt**
   - Teste ob Vektorrichtung dominiert: $\Delta_{\text{dir}} \stackrel{?}{>} \Delta_{\text{norm}}$
   
3. **Falls $\Delta_{\text{norm}} < 0.05$:**
   - H0.6 **verletzt**
   - Norm ist redundant
   - Fokus auf M2: $(\Omega, (v_2, v_3))$ als Basis

4. **Falls $R^2(\text{M4}) > 0.95$:**
   - **Null-Resultat:** Catalan ist SVN-trivialisiert
   - Trotzdem gut: SVN-Struktur ist bestätigt
   - Projekt-Pivot zu reiner EABC-Geometrie

5. **Falls $R^2(\text{M4}) < 0.80$:**
   - **Positiv-Resultat:** Catalan-Residuen sind eigenständig
   - Weiter mit H1-H10-Tests
   - Echte Catalan-Arithmetik

---

## Ausgaben

Das Experiment produziert:

1. **Tabelle:**
   ```
   Model  | R²    | RMSE  | #Params | AIC
   -------|-------|-------|---------|-----
   M0     | 0.45  | 2.3   | 2       | 450
   M1     | 0.48  | 2.2   | 3       | 445
   M2     | 0.62  | 1.9   | 4       | 420
   M3     | 0.71  | 1.6   | 5       | 380
   M4     | 0.75  | 1.5   | 8       | 370
   ```

2. **Δ-Plot:**
   - Balkendiagramm für $\Delta_{\sigma}, \Delta_{\text{shell}}, \Delta_{\text{norm}}, \Delta_{\text{dir}}$
   - Mit Bootstrap-Konfidenzintervallen

3. **Residuen-Verteilung:**
   - Histogramm der M4-Residuen
   - Q-Q-Plot gegen Normalverteilung
   - Top-10 Ausreißer identifizieren

4. **Koeffizientenanalyse:**
   - Welche SVN-Koordinate hat größten Einfluss?
   - Stabilität über verschiedene Kanonisierungen

---

## Zusammenfassung

E02 ist das **zentrale Eliminationsexperiment**:

$$\boxed{\text{Wie viel Catalan ist wirklich Catalan, und wie viel ist SVN?}}$$

**Priorität:** Sehr hoch – entscheidend für Projektarchitektur  
**Aufwand:** Mittel (2-3 Tage)  
**Risiko:** Niedrig (alle Resultate sind wissenschaftlich interessant)

Dieses Experiment trennt:
1. **SVN-Geometrie** (M0-M4)
2. **Catalan-Residuen** (echte Hierarchie)
3. **Null-Modell** (trivialisiert?)

**Nach E02 wissen wir, was das Catalan-Projekt wirklich ist.**
