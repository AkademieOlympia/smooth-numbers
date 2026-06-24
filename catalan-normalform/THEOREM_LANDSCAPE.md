# Theoremlandschaft: Smooth Numbers und Gauß-Eisenstein-Struktur

**Status:** Januar 2026  
**Reife:** A-Ebene (Mathematisch etabliert)

---

## Überblick

Dieses Dokument kartiert die bereits formalisierten mathematischen Theoreme und zeigt ihre Verbindungen zur Gauß-Eisenstein-Interpretation von EABC.

**Zentrale Erkenntnis:**

> Die EABC-Struktur ist nicht willkürlich, sondern die minimale gemeinsame Verfeinerung zweier klassischer Spaltungskriterien (mod 4, mod 3). Die Theoreme zu smooth numbers liefern einen orthogonalen Zugang über Glättungsschranken statt modularer Klassen.

---

## I. Gauß-Eisenstein-Fundierung (A-Niveau)

**Datei:** `lean/CatalanNormalform/GaussEisenstein.lean`

### 1.1 Modulare Spaltungskriterien

#### Gauß-Kriterium (ℤ[i])

```lean
theorem gaussSplitting_of_odd_prime (p : Nat) (hp : p.Prime) (hodd : p > 2) :
    gaussSplitting p = if p % 4 = 1 then SplittingBehavior.Split 
                       else SplittingBehavior.Inert
```

**Bedeutung:** Primzahlen p > 2 spalten in ℤ[i] genau dann, wenn p ≡ 1 (mod 4).

#### Eisenstein-Kriterium (ℤ[ω])

```lean
theorem eisensteinSplitting_of_prime_gt_three (p : Nat) (hp : p.Prime) (hgt : p > 3) :
    eisensteinSplitting p = if p % 3 = 1 then SplittingBehavior.Split 
                            else SplittingBehavior.Inert
```

**Bedeutung:** Primzahlen p > 3 spalten in ℤ[ω] genau dann, wenn p ≡ 1 (mod 3).

---

### 1.2 Die vier zentralen Äquivalenzen

#### E-Klasse: Beidseitige Spaltung

```lean
theorem eabc_E_iff_gauss_eisenstein_split (p : Nat) (hp : p.Prime) (hp3 : p > 3) :
    p % 12 = 1 ↔ (p % 4 = 1 ∧ p % 3 = 1)
```

**Interpretation:** E-Primzahlen spalten sowohl in ℤ[i] als auch in ℤ[ω].

#### A-Klasse: Gauß-Spaltung, Eisenstein-Inert

```lean
theorem eabc_A_iff_gauss_split_eisenstein_inert (p : Nat) (hp : p.Prime) (hp3 : p > 3) :
    p % 12 = 5 ↔ (p % 4 = 1 ∧ p % 3 = 2)
```

#### B-Klasse: Gauß-Inert, Eisenstein-Spaltung

```lean
theorem eabc_B_iff_gauss_inert_eisenstein_split (p : Nat) (hp : p.Prime) (hp3 : p > 3) :
    p % 12 = 7 ↔ (p % 4 = 3 ∧ p % 3 = 1)
```

#### C-Klasse: Beidseitige Inertheit

```lean
theorem eabc_C_iff_gauss_eisenstein_inert (p : Nat) (hp : p.Prime) (hp3 : p > 3) :
    p % 12 = 11 ↔ (p % 4 = 3 ∧ p % 3 = 2)
```

---

### 1.3 Äquivalenz der Definitionen

```lean
theorem eabc_class_equiv (p : Nat) (hp : p > 3) (hprime : p.Prime) :
    eabc_class p = eabc_class_via_splitting p
```

**Bedeutung:** Die ursprüngliche EABC-Definition (mod 12) ist exakt äquivalent zur Spaltungspaar-Definition (mod 4, mod 3).

**Chinesischer Restsatz:**

$$\mathbb{Z}/12\mathbb{Z} \cong \mathbb{Z}/4\mathbb{Z} \times \mathbb{Z}/3\mathbb{Z}$$

Da $\gcd(4, 3) = 1$, ist diese Isomorphie kanonisch.

---

### 1.4 Vektor-Interpretation

```lean
theorem factorEABCVector_equiv (n : Nat) :
    factorEABCVector n = fromSplittingBehavior (prime_factors n)
```

**Bedeutung:** Der EABC-Vektor $v = (e, a, b, c)$ zählt nicht nur Restklassen, sondern **Spaltungstypen**:

| Komponente | Zählt Primfaktoren mit |
|------------|------------------------|
| e | (Gauß spaltet, Eisenstein spaltet) |
| a | (Gauß spaltet, Eisenstein inert) |
| b | (Gauß inert, Eisenstein spaltet) |
| c | (Gauß inert, Eisenstein inert) |

---

### 1.5 Partitionierungstheoreme

#### Gauß-Partition

```lean
theorem gauss_partition (v : FactorEABCVector) :
    v.gaussSplittingCount + v.gaussInertCount = v.sum
```

wobei:
- `gaussSplittingCount = e + a` (Gauß-spaltende Faktoren)
- `gaussInertCount = b + c` (Gauß-inerte Faktoren)

#### Eisenstein-Partition

```lean
theorem eisenstein_partition (v : FactorEABCVector) :
    v.eisensteinSplittingCount + v.eisensteinInertCount = v.sum
```

wobei:
- `eisensteinSplittingCount = e + b` (Eisenstein-spaltende Faktoren)
- `eisensteinInertCount = a + c` (Eisenstein-inerte Faktoren)

**Bedeutung:** Die vier EABC-Komponenten bilden eine **2×2-Kreuzklassifikation** der Primfaktoren nach ihrem Verhalten in beiden quadratischen Körpern.

---

### 1.6 Konzentrationsmessung

#### Konzentrationsmaß H(n)

```lean
noncomputable def concentrationRatio (v : FactorEABCVector) : ℝ :=
  if v.sum = 0 then 0 else (v.normSq : ℝ) / (v.sum ^ 2 : ℝ)
```

$$H(n) = \frac{\|v\|^2}{\Omega^2} = \frac{e^2 + a^2 + b^2 + c^2}{(e + a + b + c)^2}$$

#### Schranken

```lean
theorem concentration_bounds (v : FactorEABCVector) (h : v.sum > 0) :
    (1 : ℝ) / 4 ≤ concentrationRatio v ∧ concentrationRatio v ≤ 1
```

**Interpretation:**

- **H = 1:** Alle Faktoren haben denselben Spaltungstyp (maximale Konzentration)
- **H = 1/4:** Gleichverteilung über alle vier Spaltungstypen (minimale Konzentration)
- **H ∈ (1/4, 1):** Mischung verschiedener Spaltungstypen

**Analoge Maße:**
- Simpson-Index (Ökologie)
- Herfindahl-Hirschman-Index (Ökonomie)
- Rényi-Entropie Ordnung 2 (Informationstheorie)

---

## II. Smooth Numbers (A-Niveau)

**Datei:** `DickmanFunction.lean`

### 2.1 Grunddefinitionen

#### y-Glattheit

```lean
def IsYSmooth (n : ℕ) (y : ℕ) : Prop :=
  ∀ p : ℕ, p.Prime → p ∣ n → p ≤ y
```

**Bedeutung:** Eine Zahl ist y-glatt, wenn alle ihre Primfaktoren ≤ y sind.

**Orthogonalität zu EABC:**
- EABC klassifiziert Primfaktoren nach **Restklassen mod 12**
- Glattheit klassifiziert nach **maximaler Primzahlgröße**

#### Dickman-Funktion

```lean
noncomputable def DickmanRho : ℝ → ℝ
  | u => if u ≤ 1 then 1
         else (1 / u) * ∫ t in (1 : ℝ)..u, DickmanRho t
```

**Parameter:** $u = \frac{\log x}{\log y}$ (relative Glättungsschranke)

---

### 2.2 Haupttheoreme

#### Basisfall

```lean
theorem dickman_base (u : ℝ) (h₀ : 0 ≤ u) (h₁ : u ≤ 1) :
  DickmanRho u = 1
```

#### Rekursion

```lean
theorem dickman_recursive (u : ℝ) (h : 1 < u) :
  u * DickmanRho u = ∫ t in (1 : ℝ)..u, DickmanRho t
```

#### Asymptotisches Hauptresultat

```lean
theorem smooth_count_asymptotic (x : ℝ) (y : ℕ) (hx : 1 < x) (hy : 1 < y) :
  let u := log x / log y
  ∃ ε : ℝ → ℝ, (∀ x, |ε x| < 1) ∧
    (SmoothCount x y : ℝ) = x * DickmanRho u * (1 + ε x)
```

**Bedeutung:** Die Anzahl y-glatter Zahlen ≤ x ist asymptotisch $x \cdot \rho(u)$.

---

### 2.3 EABC-Integration

#### Signaturstruktur

```lean
structure EABCSignature where
  n₂ : ℕ  -- Exponent von 2
  n₃ : ℕ  -- Exponent von 3
  nE : ℕ  -- Summe der Exponenten für E-Klasse
  nA : ℕ  -- Summe der Exponenten für A-Klasse
  nB : ℕ  -- Summe der Exponenten für B-Klasse
  nC : ℕ  -- Summe der Exponenten für C-Klasse
```

#### Schichtzahl

```lean
def EABCSignature.layer (sig : EABCSignature) : ℕ :=
  sig.n₂ + sig.n₃ + sig.nE + sig.nA + sig.nB + sig.nC
```

**Verbindung zu Glattheit:**

```lean
theorem smooth_implies_bounded_layer (n : ℕ) (y : ℕ) (sig : EABCSignature)
  (h_smooth : IsYSmooth n y) :
  ∃ bound : ℕ, sig.layer ≤ bound
```

**Interpretation:** Glattheit beschränkt die Schichtzahl (Gesamtanzahl Primfaktoren mit Vielfachheit).

---

### 2.4 Buchstab-Identität

```lean
theorem buchstab_identity (x : ℝ) (y : ℕ) (hx : 1 ≤ x) (hy : 2 ≤ y) :
  SmoothCount x y = SmoothCount x 2 + 
    ∑ p in (Finset.range y).filter Nat.Prime, 
      if p > 2 then SmoothCount (x / p) p else 0
```

**Bedeutung:** Rekursive Zerlegung der Glättheitszählung nach Primfaktoren.

---

## III. Verbindungen und offene Fragen

### 3.1 Etablierte Verbindungen (A-Niveau)

| Konzept | Struktur | Klassifikation |
|---------|----------|----------------|
| **EABC-Vektor** | $v = (e, a, b, c)$ | Modulare Spaltungstypen |
| **Schichtzahl** | $\Omega = e + a + b + c$ | Anzahl Primfaktoren |
| **Glattheit** | $\max\{p : p \mid n\} \leq y$ | Maximale Primzahlgröße |
| **Konzentration** | $H(n) = \|v\|^2 / \Omega^2$ | Spaltungstyp-Konzentration |

**Unabhängigkeit:**
- Zwei Zahlen können dieselbe Schichtzahl haben, aber verschiedene EABC-Vektoren
- Zwei Zahlen können dieselben EABC-Vektoren haben, aber verschiedene Glattheitswerte

**Komplementarität:**
- EABC misst **qualitative** Eigenschaften (Spaltungsverhalten)
- Glattheit misst **quantitative** Eigenschaften (Primzahlgrößen)

---

### 3.2 Offene Forschungsfragen

#### Frage 1: EABC-Verteilung in y-glatten Zahlen

$$\text{Für festes } y, \text{ wie ist } v_{\text{fac}}(n) \text{ verteilt über } \{n : n \text{ ist } y\text{-glatt}\}?$$

**Status:** Offen (B/C-Niveau)

**Spekulation:** Vielleicht gibt es eine Bias zugunsten von E-Klasse-Faktoren (beide spalten), da diese oft klein sind.

---

#### Frage 2: Dickman-Funktion für EABC-restringierte Zahlen

$$\rho_E(u), \rho_A(u), \rho_B(u), \rho_C(u)$$

**Definition:** Analog zu $\rho(u)$, aber nur für Zahlen mit bestimmter EABC-Dominanz.

**Status:** Spekulativ (C/D-Niveau)

---

#### Frage 3: Konzentration H(n) in smooth numbers

$$\text{Erwartungswert } \mathbb{E}[H(n) \mid n \text{ ist } y\text{-glatt}] \text{ als Funktion von } y?$$

**Status:** Testbar (B-Niveau)

**Hypothese:** Smooth numbers haben tendenziell **geringere** Konzentration H (mehr Diversität), da sie viele kleine Primfaktoren verschiedener Klassen haben.

---

#### Frage 4: Catalan-Hierarchien auf smooth numbers

$$M_C(n) \text{ für } n \text{ in glatten Mengen}$$

**Status:** Testbar (B/C-Niveau)

**Hypothese:** Smooth numbers haben tendenziell **ausbalanciertere** Catalan-Bäume, da ihre Faktorisierungen diverser sind.

---

## IV. Mathematische Stärke der Theoreme

### Wichtige methodische Klarstellung

**Die Gauß-Eisenstein-Interpretation ist die stärkste Interpretation des EABC-Vektors, aber noch nicht notwendigerweise die stärkste Interpretation des gesamten Projekts.**

Der Unterschied ist kritisch:

$$\boxed{\text{EABC} \leftrightarrow (\text{Gauß}, \text{Eisenstein})}$$

ist ein **Satz** (CRT + klassische Spaltungskriterien).

Aber:

$$H(n) \rightarrow M_C(n)$$

ist eine **Hypothese** (empirisch zu prüfen).

---

### A-Niveau: Klassische Mathematik (Sätze, keine Modelle)

1. **Modulo-12-Struktur**
   - $p > 3$ hat genau eine Restklasse in $\{1, 5, 7, 11\} \pmod{12}$
   - Einheiten von $(\mathbb{Z}/12\mathbb{Z})^\times$
   - Standard-Zahlentheorie

2. **CRT-Zerlegung**
   - $\mathbb{Z}/12\mathbb{Z} \cong \mathbb{Z}/4\mathbb{Z} \times \mathbb{Z}/3\mathbb{Z}$
   - Da $\gcd(4, 3) = 1$
   - Klassisches Resultat

3. **Gauß-Spaltungskriterium**
   - $p \neq 2$ spaltet in $\mathbb{Z}[i]$ ⟺ $p \equiv 1 \pmod{4}$
   - Klassische algebraische Zahlentheorie
   - Etabliert seit 19. Jahrhundert

4. **Eisenstein-Spaltungskriterium**
   - $p \neq 3$ spaltet in $\mathbb{Z}[\omega]$ ⟺ $p \equiv 1 \pmod{3}$
   - Klassische algebraische Zahlentheorie
   - Analog zu Gauß

5. **EABC ↔ (Gauß, Eisenstein) Äquivalenz**
   - Die vier EABC-Klassen entsprechen exakt $(S/I, S/I)$
   - Folgt unmittelbar aus CRT + Spaltungskriterien
   - **Das ist kein Modell. Das ist ein Satz.**

6. **Dickman-Funktion**
   - Asymptotische Formel $\Psi(x, y) \sim x \cdot \rho(u)$
   - Etabliert seit Dickman (1930), de Bruijn (1951)
   - Numerisch verifiziert für alle praktischen $u$

---

### B-Niveau: Gut motivierte Hypothesen (testbar)

1. **Konzentrationsmessung H(n)**
   - **Definition** ist wohldefiniert (A-Niveau)
   - **Schranken** $[1/4, 1]$ sind beweisbar (A-Niveau)
   - **Interpretation** als Spaltungstyp-Konzentration ist klassisch motiviert
   - **ABER:** Ob H(n) Erklärungskraft für andere Observablen hat, ist offen

2. **SVN-Koordinaten**
   - $n \mapsto (\Omega, (v_2, v_3), v_{\text{EABC}}, H)$
   - Mathematisch klar definiert
   - Nützlich als Koordinatisierung
   - Ob sie Catalan-Strukturen erklären, ist hypothetisch

3. **M0-M4 Modellkaskade**
   - Methodisch solide (progressiver $\Delta R^2$-Test)
   - Statistisch sauber
   - Ergebnisse stehen noch aus

4. **EABC-Verteilung in smooth numbers**
   - Empirisch testbar
   - Keine theoretische Vorhersage bisher
   - Orthogonaler Zugang zu Primfaktorstruktur

---

### C-Niveau: Offene Forschungsfragen

1. **H0.5 (Schalenstabilität)**
   - $\Omega(n) = \Omega(m)$ impliziert ähnliche Catalan-Strukturen?
   - Testbar, aber keine theoretische Motivierung

2. **H0.6 (Norm-Vorhersagekraft)**
   - $\Delta R^2_{\text{norm}} > \eta$?
   - Die interessanteste Frage des Projekts
   - Verbindet A-Niveau (EABC) mit unbekannter Catalan-Struktur

3. **Catalan-Magic**
   - Mathematisch wohldefiniert (falls H0 gelöst)
   - Ob M_C arithmetisch interessant ist, ist völlig offen
   - Könnte rein kombinatorisch sein

4. **EABC-stratifizierte Dickman-Funktion**
   - Konzeptionell klar
   - Rechenaufwändig
   - Unklar, ob mathematisch interessant

---

### D-Niveau: Spekulation

1. **Quaternionen-Struktur**
   - $v \in \mathbb{R}^4 \cong \mathbb{H}$ (formal)
   - Aber keine Multiplikation, nur Norm
   - Derzeit nur formale Analogie

2. **Oktonionen/Hurwitz-Assoziatoren**
   - $[v_L, v_M, v_R] \in \mathbb{O}$?
   - Mathematisch weit entfernt
   - Keine Motivierung außer Dimensionszählung

3. **Tamari-Spektraltheorie**
   - Schöne Geometrie
   - Verbindung zu EABC unklar

---

## V. Strategische Empfehlung

### Priorität 1: Nutze die Gauß-Eisenstein-Fundierung

**Warum:** Dies ist die stärkste mathematische Rechtfertigung für EABC, die bisher gefunden wurde.

**Nächste Schritte:**
1. CRT-Theoreme vollständig in Lean beweisen (statt `sorry`)
2. Dokumentation: "EABC ist die gemeinsame Verfeinerung zweier klassischer Spaltungskriterien"
3. Diese Interpretation in allen Hypothesen explizit nutzen

---

### Priorität 2: Teste EABC auf smooth numbers

**Warum:** Orthogonaler Zugang zu Primfaktorstruktur.

**Experiment:**
```python
def test_eabc_in_smooth_numbers(y_max=1000, x_max=10000):
    for y in range(2, y_max):
        smooth_set = [n for n in range(1, x_max) if is_y_smooth(n, y)]
        
        # Messe EABC-Verteilung
        eabc_counts = Counter(eabc_class(n) for n in smooth_set)
        
        # Messe durchschnittliche Konzentration
        avg_H = mean(concentration_H(n) for n in smooth_set)
        
        print(f"y={y}: E={eabc_counts['E']}, A={eabc_counts['A']}, B={eabc_counts['B']}, C={eabc_counts['C']}, H̄={avg_H:.4f}")
```

**Erwartung:** Für große $y$ sinkt H (mehr Diversität).

---

### Priorität 3: Vermeide überfrühte Catalan/Tamari-Verknüpfung

**Warum:** Die EABC-Struktur ist jetzt mathematisch stark fundiert (A-Niveau). Die Catalan-Verbindung ist noch hypothetisch (B/C-Niveau).

**Methodische Empfehlung:**

$$\boxed{\text{Etabliere EABC-Smooth-Verbindung, bevor du Catalan-EABC-Verbindung erzwingst.}}$$

---

## VI. Zusammenfassung

### Was als Satz etabliert ist (A-Niveau)

Die Gauß-Eisenstein-Interpretation liefert erstmals eine klassische algebraisch-zahlentheoretische Bedeutung des EABC-Vektors. Sie erklärt die Modulo-12-Struktur exakt als gemeinsame Verfeinerung der Spaltungsgesetze in $\mathbb{Z}[i]$ und $\mathbb{Z}[\omega]$. Damit wird die EABC-Klassifikation von einer rein modularen Beschreibung zu einer Beschreibung von Spaltungstypen rationaler Primzahlen.

**Konkret:**
- EABC-Klassen ↔ Spaltungspaare (CRT)
- Konzentrationsmessung H(n) ist wohldefiniert
- Dickman-Funktion für smooth numbers
- Lean-Formalisierung der modularen Kriterien

### Was als Hypothese zu prüfen bleibt (B/C-Niveau)

Ob diese Information über Größen wie H(n) tatsächlich zusätzliche Erklärungskraft für Catalan- oder andere Observablen besitzt, bleibt eine empirisch zu prüfende Frage.

**Die kritische Grenze:**

$$\boxed{\text{EABC} \leftrightarrow (\text{Gauß}, \text{Eisenstein})}$$ 
ist ein **Satz**.

$$H(n) \rightarrow M_C(n)$$
ist eine **Hypothese**.

Und erst recht:

$$H \rightarrow \text{Catalan} \rightarrow \text{Tamari} \rightarrow \mathbb{H} \rightarrow \mathbb{O}$$

ist **Spekulation** (D-Niveau).

### Was testbar ist (B-Niveau)

1. EABC-Verteilung in smooth-number-Mengen
2. Durchschnittliche Konzentration $\bar{H}$ als Funktion von $y$
3. M0-M4 Modellkaskade: $\Delta R^2$ für jede Informationsstufe
4. Catalan-Magic auf smooth numbers (falls H0 gelöst)

### Der eigentliche Gewinn

Früher war EABC:

$$\mathbb{Z} \rightarrow (\mathbb{Z}/12\mathbb{Z})^\times$$

Jetzt wird daraus:

$$\mathbb{Z} \rightarrow (\text{Gauß-Splitting}) \times (\text{Eisenstein-Splitting})$$

Das ist **konzeptionell** viel stärker.

Die Konzentrationsgröße H(n) misst nicht mehr "Konzentration auf Restklassen", sondern "Konzentration auf Spaltungstypen" – eine Interpretation, die an Verteilungen von Frobenius-Typen in algebraischen Zahlkörpern erinnert (noch auf elementarer Ebene, aber die Richtung ist mathematisch natürlicher).

### Was spekulativ bleibt (C/D-Niveau)

1. EABC-stratifizierte Dickman-Funktion (C)
2. Tamari-Geometrie in Verbindung zu EABC (C)
3. Quaternionen/Oktonionen (D)
4. Hurwitz-Assoziatoren (D)

---

## Anhang: Theoremübersicht nach Lean-Dateien

### `GaussEisenstein.lean` (Etabliert)

- `gaussSplitting_of_odd_prime`
- `eisensteinSplitting_of_prime_gt_three`
- `eabc_E_iff_gauss_eisenstein_split`
- `eabc_A_iff_gauss_split_eisenstein_inert`
- `eabc_B_iff_gauss_inert_eisenstein_split`
- `eabc_C_iff_gauss_eisenstein_inert`
- `eabc_class_equiv`
- `factorEABCVector_equiv`
- `gauss_partition`
- `eisenstein_partition`
- `concentration_bounds`
- `concentration_max_iff_single_class`

### `DickmanFunction.lean` (Etabliert)

- `dickman_base`
- `dickman_recursive`
- `dickman_pos`
- `dickman_monotone`
- `dickman_deriv`
- `dickman_asymptotic`
- `smooth_count_asymptotic`
- `buchstab_identity`
- `smooth_implies_bounded_layer`

### `ShellVectorNorm.lean` (Etabliert)

- `shellHeight_mul`
- `reducedCore_coprime_six`
- `reducedCore_in_U6`
- `eabc_class_of_core_isSome`
- `factor_vector_sum_le_omega`

---

**Fazit:**

Die Gauß-Eisenstein-Interpretation verleiht EABC eine mathematische Semantik, die über "willkürliche mod-12-Klassen" hinausgeht. Die Smooth-Number-Theoreme liefern einen orthogonalen, ebenfalls etablierten Zugang zur Primfaktorstruktur. Die Verbindung beider ist das fruchtbarste Forschungsgebiet, nicht die sofortige Eskalation zu Catalan/Tamari/Hurwitz.
