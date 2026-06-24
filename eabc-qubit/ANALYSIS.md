# EABC-Qubit: Kritische Analyse der Ergebnisse

**Datum**: 23. Juni 2026  
**Status**: Laufende Berechnungen

## Zusammenfassung der bisherigen Erkenntnisse

### 1. γ-Sweep: Quanten-Phasenübergang bestätigt ✓

**Ergebnis**: Das System zeigt einen kontinuierlichen Übergang von integrabel (Poisson) zu partiell chaotisch (Brody/GOE).

```
γ = 0.0:  q = 0.000  →  Perfektes Poisson (Berry-Tabor ✓)
γ = 0.1:  q = 0.265  →  Schwache Störung
γ = 0.5:  q = 0.638  →  Partielles Chaos
γ = 1.0:  q = 0.707  →  Maximum! (Fast GOE)
γ = 2.0:  GOE        →  Vollständiges Chaos
γ > 2.0:  q ≈ 0.5    →  Abfall (Lokalisierung?)
```

**Interpretation**:
- ✅ Berry-Tabor-Theorem bei γ=0 perfekt bestätigt
- ✅ Kontinuierlicher Phasenübergang für 0 < γ < 1
- ✅ Maximum bei γ ≈ α (Resonanz zwischen Hopping und Defekt-Stärke)
- ⚠️ Abfall für γ >> α deutet auf Anderson-Lokalisierung hin

**Physikalische Bedeutung**: Die Primzahl-Defekte brechen systematisch die Integrabilität. Bei optimaler Kopplungsstärke (γ ≈ α) erreicht das System maximales Quantenchaos.

---

### 2. Finite-Size-Scaling: ÜBERRASCHENDE Nicht-Monotonie! 🚨

**Erwartung**: q(N) → 1.0 für N → ∞ (einfache Konvergenz zu GOE)

**Beobachtung**: **Oszillierendes Muster**!

```
N =  500:  POISSON      (q klein)
N = 1000:  BRODY        (q = 0.707)  ← MAXIMUM
N = 2000:  POISSON      (q klein)
N = 3000:  BRODY        (q = 0.621)
N = 5000:  [läuft...]
```

**Dies ist NICHT das erwartete Verhalten!**

#### Drei mögliche Erklärungen:

##### A) Optimale Systemgröße (Resonanz-Phänomen)

Es gibt eine **kritische Längenskala** L_c ≈ 1000, bei der die Primzahl-Dichte, die chirale Kohärenzlänge und die Systemgröße optimal balanciert sind.

**Mechanismus**:
- Bei N << L_c: Zu wenige Primzahlen → statistisch irrelevant
- Bei N ≈ L_c: Perfekte Balance → maximales Chaos
- Bei N >> L_c: Zu viele Defekte → System "friert ein"

**Analogie**: Wie bei der **Mobility Edge** in Anderson-Lokalisierung, aber als Funktion der Systemgröße statt Energie.

##### B) Kommensurabilitäts-Effekte (Diskrete Längenskalen)

Die mittlere Primzahl-Abstände λ_p ≈ ln(N) wächst logarithmisch.

Die chirale Kohärenzlänge ξ_χ ∼ α/β ist fest.

Bei bestimmten N könnten diese beiden Skalen **kommensurabel** werden:

```
λ_p / ξ_χ ≈ rational  →  Chaos (Resonanz)
λ_p / ξ_χ ≈ irrational  →  Poisson (Störung interferiert destruktiv)
```

**Analogie**: Ähnlich zu **Quasikristallen** oder **Fibonacci-Ketten**.

##### C) Bandstruktur-Artefakt (Trimming-Problem)

Die Energiebandbreite skaliert wie:

```
ΔE ∼ 2α (für 1D tight-binding)
```

Aber die **lokale Zustandsdichte** variiert über das Band (Van-Hove-Singularitäten an den Rändern).

Unser **40%-Trimming** schneidet unterschiedliche Regionen bei verschiedenen N:

- Bei N=1000: Wir erwischen vielleicht die "chaotischste" Region
- Bei N=2000: Wir schneiden vielleicht mehr integrable Bereiche

**Test**: Wiederhole mit verschiedenen Trimming-Prozenten (20%, 30%, 40%, 50%).

---

### 3. Chiralitäts-Test (β-Sweep): Noch ausstehend

**Erwartung**: 
- β = 0: Kein Chaos (Primzahl-Positionen allein reichen nicht)
- β > 0: Chaos kehrt zurück

**Status**: Test läuft noch (nach N=5000 Finite-Size).

**Entscheidende Frage**: Ist die EABC-Klassifikation (mod 12) **physikalisch entscheidend**?

---

## Nächste Schritte (Priorisiert)

### KRITISCH (Sofort):

1. **β-Sweep abwarten**: Läuft gerade
2. **N=5000 Ergebnis analysieren**: Läuft gerade

### HOCH (Nächste Sitzung):

3. **Trimming-Variation**: Wiederhole Finite-Size mit 20%, 30%, 50% Trimming
4. **Dichtere N-Sampling**: N = 800, 900, 1000, 1100, 1200 um das Maximum zu lokalisieren
5. **Spektrum-Position**: Nutze verschiedene `which` Parameter (SA, LM, SM) in eigsh

### MITTEL:

6. **Längenskalen-Analyse**: 
   - Messe λ_p (mittlere Primzahl-Abstände)
   - Messe ξ_χ (chirale Korrelationslänge aus Wellenfunktionen)
   - Teste λ_p/ξ_χ Hypothese

7. **Explizites H₀-Vergleich**: 
   - Berechne H₀ (γ=0) für alle N
   - Zeige, dass Finite-Size-Oszillationen NICHT bei γ=0 auftreten

### NIEDRIG:

8. **Modulo-30-Vergleich**: Teste, ob mod-12 vs. mod-30 unterschiedlich sind
9. **Größere Systeme**: N = 10.000 (falls Rechner es schafft)

---

## Vorläufige Schlussfolgerungen

### Was gesichert ist:

✅ **Quanten-Phasenübergang**: γ-Sweep zeigt klaren Übergang integrabel → chaotisch  
✅ **Berry-Tabor-Theorem**: γ=0 → Poisson perfekt bestätigt  
✅ **Resonanz-Maximum**: γ ≈ α zeigt maximales Chaos  
✅ **Keine GUE**: System ist GOE (reell-symmetrisch, Zeitumkehr-invariant)

### Was überraschend ist:

🚨 **Finite-Size-Oszillationen**: NICHT monoton q(N) → 1  
🚨 **Optimale Größe**: N ≈ 1000 scheint speziell zu sein  
🚨 **Lokalisierung**: γ >> α zeigt Abfall von q (Anderson-ähnlich)

### Was noch offen ist:

❓ **β=0 Test**: Ist Chiralität entscheidend?  
❓ **N=5000**: Bestätigt es das Oszillations-Muster?  
❓ **Trimming-Artefakt**: Ist die Nicht-Monotonie ein Mess-Effekt?  
❓ **Physikalischer Mechanismus**: Was verursacht die Längenskalen-Resonanz?

---

## Mögliche Paper-Aussagen (vorsichtig formuliert)

**SICHER (für Paper geeignet)**:

> "We observe a continuous quantum phase transition from integrable (Poisson) to partially chaotic (Brody/GOE) dynamics as the prime-defect strength γ is varied, with a maximum Brody parameter q ≈ 0.7 at γ ≈ α."

> "The integrable limit (γ=0) shows perfect Poisson statistics, confirming the Berry-Tabor theorem."

**VORSICHTIG (weitere Tests nötig)**:

> "Finite-size scaling reveals non-monotonic behavior, suggesting a critical system size N_c ≈ 1000 where quantum chaos is maximized. This could indicate commensurability effects between prime number spacing and chiral coherence length."

**SPEKULATIV (Diskussions-Sektion)**:

> "The observed oscillations in q(N) may be related to Anderson localization in the strong-disorder limit (γ >> α) or to discrete length-scale resonances analogous to quasicrystals."

---

## Technische Notizen

### Numerische Stabilität:

- Sparse CSR-Format funktioniert einwandfrei
- Lanczos (eigsh) konvergiert zuverlässig für N ≤ 3000
- N=5000 braucht >12 Min (20k × 20k Matrix, 1500 Eigenwerte)

### Unfolding-Qualität:

- Polynom-Grad 7 scheint robust
- Mittlere Dichte ρ̄ ≈ 1.02 (gut)
- Bandkanten-Trimming (40%) reduziert Artefakte

### Brody-Fit Probleme:

- Bei sehr kleinen oder sehr großen q gibt es numerische Warnungen
- `RuntimeWarning: invalid value encountered in power` bei extremen Parametern
- Fit ist aber insgesamt stabil für 0.2 < q < 0.9

---

**Status**: Dokument wird aktualisiert sobald N=5000 und β-Sweep abgeschlossen sind.
