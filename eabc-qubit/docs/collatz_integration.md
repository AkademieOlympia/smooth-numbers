# Collatz-Dynamik-Integration in EABC-Qubit

## Überblick

Diese Erweiterung integriert die theoretischen Collatz-Kontraktionsraten aus **Paper C: "Conditional Collatz via G2 Log-Drift Axiom"** in das EABC-Qubit-Framework. Statt uniformer Primzahl-Defekte werden die Defekte nach den physikalisch motivierten lokalen log(r)-Raten der Collatz-Dynamik gewichtet.

## Theoretischer Hintergrund

### EABC-Klassifikation und Collatz-Dynamik

Die Collatz-Abbildung definiert eine Iteration:

```
C(n) = { n/2       falls n gerade
       { (3n+1)/2  falls n ungerade
```

Die **lokale Wachstumsrate** log(r) quantifiziert, wie schnell eine Trajektorie bei Passage durch eine bestimmte Restklasse (mod 12) wächst oder schrumpft.

### Log-Raten nach EABC-Klasse

| Klasse | n mod 12 | log(r)                      | Wert    | Typ                   |
|--------|----------|-----------------------------|---------|-----------------------|
| **E**  | ≡ 1      | -log(2)                     | -0.693  | Starker Kontraktor    |
| **A**  | ≡ 5      | -log(2) + log(3)/2          | -0.143  | Schwacher Kontraktor  |
| **B**  | ≡ 7      | +log(2)                     | +0.693  | Starker Expander      |
| **C**  | ≡ 11     | +log(3) - log(2)            | +0.405  | Mittlerer Expander    |

### G2-Axiom (Log-Drift-Neutralität)

Das **G2-Axiom** aus Paper C besagt:

```
⟨log(r)⟩ ≈ 0
```

Die mittlere Wachstumsrate über alle Restklassen sollte näherungsweise null sein. Dies ist eine notwendige Bedingung für die Collatz-Konvergenz: Expander und Kontraktoren balancieren sich im Mittel aus.

## Implementierung

### Neues Modul: `collatz_weights.py`

Das Modul stellt folgende Funktionen bereit:

#### `collatz_log_rate(n: int) -> float`

Berechnet die theoretische log(r)-Rate für eine Zahl n basierend auf ihrer EABC-Klasse.

```python
>>> collatz_log_rate(13)  # E: Kontraktor
-0.6931471805599453
>>> collatz_log_rate(7)   # B: Expander
0.6931471805599453
```

#### `collatz_log_rate_prime(p: int) -> float`

Spezialisierte Version für Primzahlen (nutzt `eabc_classification`).

#### `collatz_weights_array(n_max: int, primes: List[int]) -> np.ndarray`

Erzeugt ein NumPy-Array mit den Collatz-Gewichten für alle gegebenen Primzahlen.

#### `random_soup_weights(n_primes: int, seed: int = 42) -> np.ndarray`

**Falsifikations-Test**: Erzeugt zufällig permutierte Gewichte mit derselben Verteilung wie die echten Collatz-Raten. Dies dient als Kontroll-Experiment:

- Wenn Collatz-Gewichte keine besseren Eigenschaften zeigen als eine zufällige Permutation → Theorie nicht haltbar
- Wenn Collatz-Gewichte charakteristische Signaturen zeigen → Evidenz für physikalische Relevanz

### Erweiterte Hamiltonian-Klasse: `CollatzEABCHamiltonian`

Die neue Klasse `CollatzEABCHamiltonian` erweitert `EABCHamiltonian` und überschreibt den Primzahl-Defekt-Term:

```python
H_p^Collatz = γ · Σ_p log(r(p)) · |p⟩⟨p| ⊗ |σ(p)⟩⟨σ(p)|
```

#### Verwendung

```python
from src import CollatzEABCHamiltonian

# Echte Collatz-Gewichte
H = CollatzEABCHamiltonian(N=1000, gamma=1.5)
E = H.compute_spectrum(k=500)

# Random Soup (Kontrolle)
H_soup = CollatzEABCHamiltonian(N=1000, gamma=1.5, use_random_soup=True)
E_soup = H_soup.compute_spectrum(k=500)
```

#### Parameter

- `N`: Gittergröße
- `alpha`: Hopping-Stärke (Standard: 1.0)
- `beta`: Chirale Kopplung (Standard: 0.5)
- `gamma`: Globaler Skalierungsfaktor für Collatz-Gewichte (Standard: 1.5)
- `use_random_soup`: Falls `True`, verwende permutierte Gewichte (Standard: `False`)
- `random_seed`: Seed für Random Soup (Standard: 42)

#### Neue Methode: `compare_with_uniform(k=500)`

Vergleicht das Collatz-gewichtete Spektrum mit dem uniform-gewichteten Referenz-Spektrum:

```python
comparison = H.compare_with_uniform(k=500)
print(comparison['delta_spectrum'])  # Spektrale Differenz
```

## Demo-Skript: `demo_collatz.py`

Das Demo-Skript führt umfassende Vergleichstests durch:

### Test 1: Drei-Szenarien-Vergleich

Vergleicht die Level Spacing Distribution für:

1. **Standard-EABC** (uniforme Defekte γ · 1.0)
2. **Collatz-gewichtet** (echte log(r)-Raten)
3. **Random Soup** (permutierte Gewichte)

```bash
python demo_collatz.py
```

Erzeugt einen Plot mit drei Histogrammen und theoretischen Referenzkurven (Poisson, GUE).

### Test 2: γ-Parameter-Sweep

Untersucht die Abhängigkeit der Spektralstatistik von γ ∈ [0, 3]:

- Kolmogorov-Smirnov-Statistiken (Abweichung von Poisson/GUE)
- Mittlerer Level Spacing ⟨s⟩
- Standardabweichung σ(s)

Zentrale Frage: **Zeigen Collatz-Gewichte bei bestimmten γ-Werten stabilere oder charakteristischere Eigenschaften?**

## Erwartete Resultate

### Szenario A: Collatz = Uniform

Falls die Collatz-Gewichte keine signifikanten Unterschiede zu uniformen Defekten zeigen:

→ Die EABC-Struktur der Collatz-Dynamik ist **nicht physikalisch relevant** für die spektrale Statistik  
→ Primzahlen wirken wie generisches Rauschen

### Szenario B: Collatz ≠ Uniform und Collatz ≠ Random Soup

Falls die Collatz-Gewichte charakteristische Signaturen zeigen:

→ **Evidenz** für physikalische Relevanz der Collatz-Struktur  
→ Mögliche Verbindung zu tieferen zahlentheoretischen Symmetrien

### Szenario C: Resonanz-Peak bei bestimmtem γ*

Falls bei einem charakteristischen γ-Wert ein qualitativer Übergang (z.B. Poisson → GUE-ähnlich) auftritt:

→ **Kritischer Punkt** der Collatz-Kopplung  
→ Mögliche Analogie zu Phasenübergängen in der Festkörperphysik

## Falsifikations-Kriterium

Das Design folgt dem Popper-Kriterium der Falsifizierbarkeit:

**Hypothese**: Die Collatz-Gewichte aus Paper C enthalten physikalisch relevante Struktur.

**Test**: Vergleiche Collatz vs. Random Soup (permutierte Gewichte mit gleicher Verteilung).

**Falsifikation**: Falls Random Soup äquivalente oder bessere spektrale Eigenschaften zeigt → Hypothese verworfen.

**Bestätigung**: Falls Collatz systematisch stabilere, klarere oder charakteristischere Spektralstatistiken zeigt → Hypothese gestützt.

## Quantitative Metriken

### Kolmogorov-Smirnov-Statistik

```
D = sup_s |F_empirisch(s) - F_theorie(s)|
```

Misst maximale Abweichung zwischen empirischer und theoretischer Verteilung (Poisson oder GUE).

**Klein ist besser**: Kleinere Werte → bessere Übereinstimmung mit theoretischer Vorhersage.

### Mittlerer Level Spacing

```
⟨s⟩ = (1/N) Σ s_n
```

Sollte nach Normierung ⟨s⟩ ≈ 1 sein. Abweichungen deuten auf systematische Verzerrungen hin.

### Standardabweichung

```
σ(s) = √[⟨s²⟩ - ⟨s⟩²]
```

Charakterisiert die Breite der Verteilung:

- Poisson: σ ≈ 1
- GUE: σ ≈ 0.52

## Physikalische Interpretation

### Tight-Binding-Analogie

Das System ist analog zu:

- **Elektron in 1D-Kette** mit internem Pseudospin (EABC)
- **Magnetische Verunreinigungen** an Primzahlpositionen
- **Collatz-Gewichte** als physikalisch motivierte Potentiallandschaft

### Anderson-Lokalisierung

Zentrale Frage: Führen die Collatz-Defekte zu:

- **Anderson-Lokalisierung** (Poisson-Statistik)?
- **Ausgedehnten Zuständen** (GUE-Statistik)?
- **Intermediärem Verhalten** (Mobilitätskante)?

### Riemannsche Nullstellen-Analogie

Falls GUE-Statistik auftritt:

→ Mögliche Analogie zu den Riemannschen ζ-Nullstellen (Montgomery-Dyson-Vermutung)  
→ Die Primzahlen würden eine kohärente Quantenstruktur bilden

## Weitere Untersuchungen

### Erweiterungen

1. **Eigenvektoren**: Lokalisierung vs. Delokalisierung analysieren
2. **Berry-Phase**: Z₄-Orbit-Topologie untersuchen
3. **Entanglement-Entropie**: Verschränkung zwischen Orts- und Chirali-Freiheitsgrad
4. **Größenabhängigkeit**: Scaling-Verhalten für N → ∞

### Theoretische Fragen

- Gibt es einen **kritischen Wert γ***, an dem ein Phasenübergang auftritt?
- Sind die Collatz-Gewichte **RMT-kompatibel** (Random Matrix Theory)?
- Existiert eine **Verbindung zur L-Funktion** der Collatz-Graphen?

## Literatur

### Collatz-Dynamik

- Tao, T. (2019): "Almost all orbits of the Collatz map attain almost bounded values"
- Lagarias, J. C. (2010): "The 3x+1 Problem: An Annotated Bibliography"

### Spektralstatistik

- Bohigas, Giannoni, Schmit (1984): "Characterization of Chaotic Quantum Spectra"
- Haake, F. (2010): "Quantum Signatures of Chaos"

### Random Matrix Theory

- Mehta, M. L. (2004): "Random Matrices" (3rd Edition)
- Guhr, Müller-Groeling, Weidenmüller (1998): "Random Matrix Theories in Quantum Physics"

### Primzahlen und Quantenchaos

- Montgomery, H. L. (1973): "The Pair Correlation of Zeros of the Zeta Function"
- Berry, M. V., Keating, J. P. (1999): "The Riemann Zeros and Eigenvalue Asymptotics"

---

**Autor**: Thomas Hoffbauer  
**Datum**: 23. Juni 2026  
**Version**: 1.0  
**Status**: Experimentell
