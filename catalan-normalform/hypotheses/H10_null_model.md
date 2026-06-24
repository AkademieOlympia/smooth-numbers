# Hypothese C10: Null-Modell (Reduktion auf bekannte Kombinatorik)

## Formulierung

**Null-Hypothese:**

Falls alle arithmetischen Residuen verschwinden, bleibt $M_C(n)$ eine **reine Funktion** von $\Omega(n)$:

$$M_C(n) = f(\Omega(n)) + \varepsilon(n)$$

wobei $\varepsilon(n)$ reines Rauschen ist (unkorreliert mit arithmetischen Eigenschaften).

**Interpretation:**

Falls diese Hypothese zutrifft, ist die Catalan-Geometrie **keine neue Zahlentheorie**, sondern nur eine Reparametrisierung der Faktorkomplexität $\Omega(n)$.

---

## Bedeutung

Dies ist das **wichtigste negative Kontrollmodell**.

Falls H10 zutrifft, sind **alle vorherigen Hypothesen (H1–H9) falsifiziert**.

---

## Teststatistik

### Test 10a: Erklärungskraft von $\Omega(n)$

Berechne den **Determinationskoeffizienten** $R^2$ für:

$$M_C(n) \sim f(\Omega(n))$$

wobei $f$ eine beliebige Funktion ist (z.B. Polynom 3. Grades).

**Kriterium:**

$$R^2 > 0.95$$

Falls $R^2$ sehr hoch ist, erklärt $\Omega(n)$ fast die gesamte Varianz.

---

### Test 10b: Residuen-Analyse

Berechne:

$$\varepsilon(n) = M_C(n) - \hat{f}(\Omega(n))$$

Teste dann:

1. **Normalität:** Kolmogorov-Smirnov-Test für $\varepsilon(n) \sim \mathcal{N}(0, \sigma^2)$
2. **Unabhängigkeit:** Autokorrelation von $\varepsilon(n)$
3. **Arithmetische Korrelation:** $\operatorname{corr}(\varepsilon, E(n)) \approx 0$

**Kriterium:** Alle Tests müssen **nicht signifikant** sein ($p > 0.1$).

---

## Implementierung

```python
def test_null_model(numbers):
    # Catalan-Magic und Omega
    M_C = np.array([catalan_magic(n) for n in numbers])
    omega_vals = np.array([omega(n) for n in numbers])
    
    # Fitte Polynom: M_C ~ poly(Omega, degree=3)
    poly = np.poly1d(np.polyfit(omega_vals, M_C, 3))
    M_pred = poly(omega_vals)
    
    # R^2
    SS_res = np.sum((M_C - M_pred)**2)
    SS_tot = np.sum((M_C - np.mean(M_C))**2)
    R2 = 1 - SS_res / SS_tot
    
    # Residuen
    residuals = M_C - M_pred
    
    # Normalitätstest
    ks_stat, ks_pvalue = kstest(residuals, 'norm', 
                                  args=(np.mean(residuals), np.std(residuals)))
    
    # Korrelation mit EABC-Signatur
    eabc_complexity = [sum(signature_complexity(eabc_signature(n))) 
                       for n in numbers]
    corr_eabc = np.corrcoef(residuals, eabc_complexity)[0,1]
    
    return {
        'R2': R2,
        'ks_statistic': ks_stat,
        'ks_pvalue': ks_pvalue,
        'corr_with_eabc': corr_eabc,
        'null_model_valid': (R2 > 0.95 and 
                             ks_pvalue > 0.1 and 
                             abs(corr_eabc) < 0.1)
    }
```

---

## Erwartetes Resultat

### Szenario A: Null-Modell trifft zu (H10 bestätigt)

- $R^2 > 0.95$
- Residuen sind normalverteilt ($p > 0.1$)
- Keine Korrelation mit EABC ($|\rho| < 0.1$)

**Konsequenz:** Catalan-Geometrie ist **trivial**, nur Funktion von $\Omega(n)$.

---

### Szenario B: Null-Modell trifft nicht zu (H10 falsifiziert)

- $R^2 < 0.85$
- Residuen zeigen Struktur (Nicht-Normalität)
- Korrelation mit EABC vorhanden ($|\rho| > 0.2$)

**Konsequenz:** Catalan-Geometrie enthält **neue arithmetische Information**.

---

## Konsequenzen

### Falls H10 bestätigt

- **Alle Hypothesen H1–H9 sind falsifiziert**
- Die Catalan-Erweiterung ist **redundant**
- Publikationswert: **gering** (negatives Resultat)

---

### Falls H10 falsifiziert

- **Mindestens eine der Hypothesen H1–H9 ist bestätigt**
- Die Catalan-Hierarchie enthält **neue Struktur**
- Publikationswert: **hoch** (neue zahlentheoretische Observable)

---

## Interpretation als Kontrolltest

H10 ist der **härteste Test** für die Theorie.

**Wissenschaftliche Integrität erfordert:**

1. H10 muss **zuerst** getestet werden
2. Nur falls H10 falsifiziert ist, sind H1–H9 relevant
3. Ein negatives Resultat (H10 bestätigt) muss ehrlich berichtet werden

---

## Erweiterte Tests

### Test 10c: Vergleich mit Zufallsmodell

Generiere Zufallszahlen mit **gleichem** $\Omega(n)$, aber zufälligen Primfaktoren.

Teste:

$$\operatorname{dist}(M_C^{\mathrm{real}}, M_C^{\mathrm{random}}) \stackrel{?}{=} 0$$

---

### Test 10d: Informationstheoretischer Test

Berechne die **Mutual Information**:

$$I(M_C; n \mid \Omega(n))$$

Falls $I \approx 0$, ist H10 bestätigt.

---

## Literatur

- Model selection: Akaike (1974), *A new look at statistical model identification*.
- Goodness-of-fit: Kolmogorov-Smirnov test.
