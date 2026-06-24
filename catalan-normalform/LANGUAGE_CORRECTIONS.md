# Sprachliche Präzisierungen - Juni 2026

## Kernkorrektur

**Nicht:** "publication-ready als Resultat"  
**Sondern:** 

$$\boxed{\text{projekt- und methodenreif, aber noch nicht ergebnisreif}}$$

---

## Was das bedeutet

### ✅ Projekt-reif
- Struktur vollständig
- Hypothesen formuliert
- Experimentplan definiert
- Ressourcen geplant

### ✅ Methoden-reif
- Teststatistiken spezifiziert
- Nullmodelle definiert
- Lean-Scaffold für Objekte
- Falsifikationskriterien klar

### ❌ Noch nicht ergebnis-reif
- Keine empirischen Daten
- H10 nicht getestet
- Keine Korrelationen gemessen
- Keine Publikation möglich

**Dies ist kein Nachteil - es verhindert Overclaiming.**

---

## Sprachliche Korrekturen in Lean

### 1. `should_continue` → `empirical_go_no_go`

**Alt:**
```lean
def should_continue (criterion : GoNoGoCriterion) : Prop
```

**Neu:**
```lean
/-- Empirische Projektsteuerungs-Regel (keine mathematische Wahrheit). -/
def empirical_go_no_go (criterion : GoNoGoCriterion) : Prop
```

**Warum?** 
- Macht klar: Dies ist **Projektsteuerung**, nicht mathematische Beweisführung
- Vermeidet Missverständnis als "bewiesenes Kriterium"

---

### 2. "Falsifiziert" → "empirisch zurückgewiesen"

**Alt:**
```
Falls H10 falsifiziert: weitermachen
Falls H10 bestätigt: abbrechen
```

**Neu:**
```
Falls H10 empirisch zurückgewiesen: weitermachen
Falls H10 empirisch plausibel: ehrliches Nullresultat
```

**Warum?**
- "Falsifiziert" klingt zu stark (mathematischer Beweis)
- "Empirisch zurückgewiesen" ist ehrlicher (statistische Evidenz)
- "Plausibel" statt "bestätigt" (H0 wird nie bewiesen, nur nicht verworfen)

---

### 3. Lean definiert, Python testet

**Prinzip:**

```
┌─────────────────────────────────────────────────────┐
│ Lean: Objekte definieren (𝒯ₖ, Γₖ, Mₒ, H10)         │
│ Python: Empirisch testen (R², p-Werte, Korrelationen)│
└─────────────────────────────────────────────────────┘
```

**Lean sollte NICHT:**
- R²-Grenze "beweisen"
- Statistische Tests durchführen
- Empirische Schwellenwerte festlegen

**Lean sollte:**
- Typen definieren (`CTree k`)
- Strukturen formalisieren (`TamariGraph`)
- Hypothesen als `Prop` ausdrücken (`H10_NullModel`)
- Entscheidungskriterien als Struktur definieren (`GoNoGoCriterion`)

---

## E01: Nüchterne Formulierung

**Nicht:**
"E01 wird die fundamentale Struktur des arithmetischen Catalan-Raums aufdecken"

**Sondern:**
"E01 vermisst den kombinatorischen Grundatlas ohne arithmetische Aspekte"

**Tabelle sollte enthalten:**

| k | C_{k-1} | edges | diameter | mean dist to balanced | λ_1(L_C) | spectral gap |
|---|---------|-------|----------|----------------------|----------|--------------|

**Das ist alles.** Keine Spekulationen, keine Korrelationen.

Erst wenn dieser Atlas stimmt, lohnt sich EABC.

---

## Die richtige Reihenfolge (wird jetzt erzwungen)

```
1. Reine Catalan-/Tamari-Geometrie (E01)
   ↓
2. Kanonisierungstest (E02)
   ↓
3. Residualisierung gegen Ω(n) (E03)
   ↓
   [CHECKPOINT: H10 empirisch testen]
   ↓
   Falls H10 plausibel → STOP (Nullresultat)
   Falls H10 zurückgewiesen → weiter
   ↓
4. EABC-Informationsmessung (E04)
   ↓
5. Spektrale Korrelationen (E05)
```

**Das verhindert:**
- Zu frühe EABC-Spekulation
- Überinterpretation von Artefakten
- Overclaiming ohne Grundlage

---

## H10: Der harte Check

$$\boxed{\text{Ist } M_C(n) \text{ nach } \Omega(n)\text{-Kontrolle noch arithmetisch informativ?}}$$

**Falls ja:** Weiter zu EABC-Kopplung  
**Falls nein:** Ehrliches Nullresultat berichten

**Wichtig:**
- Dies ist **empirische** Entscheidung (R², Varianzzerlegung)
- Nicht mathematischer **Beweis** (Lean kann das nicht liefern)
- Schwellenwerte (0.95, 0.05, etc.) sind **konventionell**, nicht fundamental

---

## Publikationsfähigkeit

### Jetzt:
- ✅ Struktur publikationsfähig (Methodik, Plan, Hypothesen)
- ❌ Resultate noch nicht vorhanden

### Nach E03 (Woche 3):
- Falls H10 empirisch plausibel: **Negatives Resultat** publikationsfähig
  - Titel: "On the triviality of Catalan-hierarchies in prime factorizations"
  - Resultat: "M_C is a function of Ω(n) alone"
  - Wert: Methodisch sauber, ehrlich

- Falls H10 empirisch zurückgewiesen: **Positives Resultat** möglich
  - Titel: "Catalan-hierarchies in arithmetic: A new observable"
  - Resultat: "M_C contains information beyond Ω(n)"
  - Wert: Neue zahlentheoretische Struktur

### Nach E05 (Woche 8):
- Falls mehrere Hypothesen bestätigt: **Hochwertige Publikation**
  - Journal of Number Theory
  - Discrete Mathematics
  - Combinatorics, Probability and Computing

---

## Kurzformel für Kommunikation

**Intern (unter Forschern):**

> "Das Projekt ist projekt- und methodenreif. H10 wird in Woche 3 getestet. Falls H10 empirisch plausibel ist, brechen wir ab und berichten ein Nullresultat. Falls H10 zurückgewiesen wird, testen wir H1-H9."

**Extern (in Präsentationen):**

> "Wir untersuchen, ob die Faktorarchitektur von Zahlen (Catalan-Hierarchie) über die Faktoranzahl hinaus arithmetische Information enthält. Die Hypothese ist falsifizierbar: Falls nicht, ist das ein sauberes Nullresultat."

---

## Zusammenfassung

Die drei Kernkorrekturen:

1. **should_continue** → **empirical_go_no_go**  
   (Projektsteuerung, nicht Wahrheit)

2. **falsifiziert** → **empirisch zurückgewiesen**  
   (statistisch, nicht logisch)

3. **publication-ready** → **projekt- und methodenreif, aber noch nicht ergebnisreif**  
   (ehrlich über fehlende Daten)

Diese Formulierungen verhindern Overclaiming und halten das Projekt wissenschaftlich integer.
