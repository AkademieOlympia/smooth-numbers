# README Umstrukturierung - Zusammenfassung

**Datum:** 24. Juni 2026
**Zweck:** Fokussierung auf wissenschaftlichen Kern, Abgrenzung historischer/spekulativer Teile

---

## 1. Hauptänderungen

### 1.1 Neuer Titel

**Alt:** "Glatte Zahlen (Smooth Numbers)"
**Neu:** "Conditional Gap Dynamics in Prime Number Residue Classes"

**Begründung:** Der Kern ist nicht mehr smooth numbers, sondern bedingte Gap-Dynamik.

### 1.2 Eröffnung

**Hinzugefügt:** Klarer Eröffnungssatz, der ehrlich die Evolution des Projekts beschreibt:

> "Dieses Repository begann als Implementierung glatter Zahlen, entwickelte sich aber zu einem experimentellen Zahlentheorie-Projekt über bedingte Gap-Dynamiken konsekutiver Primzahlen..."

**Wirkung:** Schützt vor Overclaiming, zeigt Ehrlichkeit, macht Evolution transparent.

### 1.3 Struktur

**Alt:** Features → Dateien → Dokumentation (unstrukturiert)
**Neu:** Kern → Mathematik → Resultate → Offene Fragen → Programme → Dokumentation (strukturiert)

---

## 2. Inhaltliche Verschiebungen

### 2.1 Kern-Fokus

**Primäres Phänomen jetzt klar benannt:**
- $P(g \equiv 2,4 \bmod 12 \mid p_n \equiv a) > P(g \equiv 8,10 \bmod 12 \mid p_n \equiv a)$

**Vier-Ebenen-Hierarchie prominent:**
```
P(g mod 12 | a) → P(a→b) → R(X) → H_C(X)
```

**Metapher "Thermometer, nicht Temperatur"** direkt im Kern-Abschnitt.

### 2.2 Gauß-Eisenstein-Interpretation

**Neu:** Eigener Abschnitt 2.3, prominent platziert

**Tabelle hinzugefügt:**

| EABC | mod 12 | $\mathbb{Z}[i]$ | $\mathbb{Z}[\omega]$ |
|------|--------|------------------|----------------------|
| E | 1 | Spaltet (S) | Spaltet (S) |
| A | 5 | Spaltet (S) | Inert (I) |
| B | 7 | Inert (I) | Spaltet (S) |
| C | 11 | Inert (I) | Inert (I) |

**Explizit betont:** "Dies ist ein Satz der algebraischen Zahlentheorie (quadratisches Reziprozitätsgesetz), keine Spekulation."

### 2.3 Nullmodell-Hierarchie

**Sprachliche Präzisierung:**

**Alt:** "THEORETISCH ERKLÄRT" (übertrieben)

**Neu:** 
- "Ein geometrisches Nullmodell erklärt einen wesentlichen Anteil der beobachteten Asymmetrie."
- "Für konstante Bernoulli-Prozesse ist der geometrische Kurzgap-Bias exakt herleitbar."
- "Diese Hierarchie ist ein empirisches Nullmodellresultat im untersuchten Bereich, keine asymptotische Aussage."

**Begründung:** Die Primzahlfrage selbst ist NICHT gelöst. Vorsichtige, wissenschaftlich korrekte Sprache.

---

## 3. Was verschoben wurde

### 3.1 Smooth Numbers

**Alt:** Hauptfeature im Feature-Block
**Neu:** Abschnitt 2.1 "Ursprung", dann direkt weiter zu EABC

**Status:** Als technische Grundlage anerkannt, aber nicht mehr inhaltlicher Kern.

### 3.2 Klein-Flasche

**Alt:** "BRANDNEU!" im Feature-Block
**Neu:** Abschnitt 6.2 "Historical", klar markiert als "historische Motivation, heute nicht mehr Kern"

**Explizite Einordnung:**
- "Aufgeprägte Geometrie, keine emergente Struktur"
- "Historisch wertvoll, aber mathematisch nicht rigoros"

### 3.3 EABC-Modell (Schichtzahlen, Vektorzahlen)

**Alt:** Prominent im Feature-Block
**Neu:** Abschnitt 6.2 "Historical"

**Begründung:** Die Schichtzahlen-Interpretation ist nicht Teil des Gap-Dynamik-Kerns.

### 3.4 Lean 4 Formalisierung

**Alt:** Eigener großer Abschnitt mit Installation
**Neu:** Abschnitt 6.2 "Historical", als "optional, nicht weiterverfolgt"

**Begründung:** Nicht Teil des aktuellen Forschungsprogramms.

---

## 4. Was gekürzt wurde

### 4.1 Feature-Listen

**Alt:** Drei große Feature-Blöcke (Basis, Erweitert, EABC, Klein-Flasche, Chirality)
**Neu:** Fokus auf Gap-Dynamik-Kern, Features nur im Programm-Abschnitt

**Umfang:** Von ~350 Zeilen Features auf ~50 Zeilen Kern reduziert

### 4.2 Detaillierte Code-Beispiele

**Alt:** Viele Code-Snippets und Ausgaben im Haupt-README
**Neu:** Verweis auf separate Dokumentation

**Beispiel entfernt:**
- Recamán-Folgen-Analyse (Details → `EABC_MODEL.md`)
- Klein-Flaschen-Installationsanleitung (Details → `KLEIN_BOTTLE.md`)

### 4.3 Redundante Abschnitte

**Entfernt/zusammengeführt:**
- Doppelte Erklärung von $\chi(Q)$ und $H_C(X)$
- Mehrfache Erwähnung der Robustheitstests
- Wiederholungen der Evolution des Projekts

---

## 5. Neue Abschnitte

### 5.1 "Offene Fragen" (Abschnitt 4)

**Struktur:**
- 4.1 Modulo 30 (höchste Priorität)
- 4.2 $R(X)$-Asymptotik
- 4.3 Sieb-/Hardy-Littlewood-Modelle

**Begründung:** Klarheit über Grenzen des aktuellen Wissens.

### 5.2 "Dokumentation" (Abschnitt 6)

**Dreifache Gliederung:**
- 6.1 Current Core
- 6.2 Historical
- 6.3 Exploratory

**Mit expliziten Statusangaben:**
- ⭐ für Kern-Dokumente
- 🔬 für spekulative Dokumente
- Klare Warnungen bei Exploratory-Abschnitt

### 5.3 "Status und nächste Schritte" (Abschnitt 7)

**Neue Unterabschnitte:**
- 7.1 Aktueller Stand (Gesichert vs. Offen)
- 7.2 Prioritäten (klar nummeriert)
- 7.3 Wissenschaftlicher Status
- 7.4 Methodische Erkenntnis

---

## 6. Sprachliche Korrekturen

### 6.1 Vorsichtige Sprache bei Nullmodellen

**Alt:**
- ❌ "THEORETISCHE LÖSUNG"
- ❌ "Wir haben die Asymmetrie erklärt"

**Neu:**
- ✅ "Geometrisches Nullmodell erklärt einen wesentlichen Anteil"
- ✅ "Für konstante Bernoulli-Prozesse ist der geometrische Kurzgap-Bias exakt herleitbar"
- ✅ "Empirisches Nullmodellresultat im untersuchten Bereich, keine asymptotische Aussage"

### 6.2 Klare Trennung: Satz vs. Beobachtung vs. Spekulation

**Beispiele:**

**Satz (algebraische Zahlentheorie):**
- Gauß-Eisenstein-Interpretation: "Dies ist ein Satz der algebraischen Zahlentheorie"

**Empirische Beobachtung:**
- Gap-Asymmetrie: "Empirischer Befund (bis $X = 5 \times 10^5$)"
- $R(X)$-Sequenz: "Datensequenz: 6.14 → 4.59 → 4.05 → 3.59"

**Offene Frage:**
- Asymptotik: "Drei Szenarien: $R(X) \to 1$ (plausibelst), $R(X) \to c > 1$, $R(X)$ oszilliert"

**Spekulation (klar markiert):**
- Gödel-Universum: "Hochspekulativ, metaphorisch, keine formale Abbildung"

### 6.3 Ehrlichkeit bei Limitierungen

**Neu hinzugefügt:**

"Diese Hierarchie ist ein empirisches Nullmodellresultat im untersuchten Bereich, keine asymptotische Aussage. Die Primzahlfrage selbst ist damit nicht theoretisch gelöst."

**Wirkung:** Schützt vor Missverständnissen, zeigt wissenschaftliche Integrität.

---

## 7. Strukturelle Verbesserungen

### 7.1 Klarere Hierarchie

**Alt:** Flache Struktur, alles auf gleicher Ebene
**Neu:** Hierarchische Struktur:
1. Kern (Gap-Dynamik)
2. Mathematische Koordinaten (EABC, Gauß-Eisenstein)
3. Hauptresultate
4. Offene Fragen
5. Programme
6. Dokumentation (mit Untergliederung)
7. Status

### 7.2 Explizite Priorisierung

**Programme:**
- ⭐-System eingeführt (1-7 Sterne)
- Kern-Programme klar markiert

**Offene Fragen:**
- Modulo 30: ⭐⭐⭐⭐⭐ HÖCHSTE PRIORITÄT
- $R(X)$-Asymptotik: ⭐⭐⭐⭐⭐

**Dokumentation:**
- Current Core vs. Historical vs. Exploratory

### 7.3 Navigationshilfen

**Verweise hinzugefügt:**
- "Siehe [Historische Dokumente](#72-historical)"
- "Status: Separates Projekt" (für QEC)
- "Verweis: Subprojekt `catalan-normalform/`" (für Catalan)

---

## 8. Exploratory-Abschnitt

### 8.1 Explizite Warnung

**Hinzugefügt:**

"Diese Dokumente sind mathematisch interessant, aber hochspekulativ und nicht validiert. Sie sollten NICHT als etablierte Resultate missverstanden werden."

### 8.2 QEC-Projekt

**Einordnung:**
- Klar als "separates Projekt" markiert
- Vollständige Beschreibung beibehalten (5 Seiten Paper ist solide)
- Aber: "nicht ausbreiten im Haupt-README"

### 8.3 Catalan, Gödel, Hurwitz

**Status-Angaben:**
- Catalan: 🔬 "Mathematisch wohldefiniert, empirisch ungetestet"
- Gödel: 🔬🔬 "Hochspekulativ, metaphorisch, keine formale Abbildung"
- Hurwitz: Nur im QEC-Kontext erwähnt

---

## 9. Umfangsvergleich

### 9.1 Zeilen

**Alt:** 1014 Zeilen (altes README)
**Neu:** ~650 Zeilen (neues README)

**Reduktion:** ~36%, aber vollständige Information erhalten durch Verweis auf separate Dokumente

### 9.2 Fokus-Ratio

**Alt:**
- Kern (Gap-Dynamik): ~20%
- Historisches/Spekulatives: ~50%
- Features/Code: ~30%

**Neu:**
- Kern (Gap-Dynamik): ~40%
- Hauptresultate/Offene Fragen: ~25%
- Programme/Dokumentation: ~25%
- Historisches (abgegrenzt): ~10%

---

## 10. Wichtigste Verbesserungen

### 10.1 Für Außenstehende

**Vorher:** "Wirkt zu spekulativ, Klein-Flaschen klingen nach Crankery"
**Nachher:** "Klarer wissenschaftlicher Kern, Gap-Asymmetrie als Primärphänomen, Gauß-Eisenstein als Fundierung"

### 10.2 Für Experten

**Vorher:** "Vermischung von Beobachtung, Spekulation, historischen Metaphern"
**Nachher:** "Klare Trennung: Was ist Satz, was ist Beobachtung, was ist offene Frage, was ist Spekulation"

### 10.3 Für das Projekt selbst

**Vorher:** "Gefahr von Overclaiming, 'theoretische Lösung'"
**Nachher:** "Vorsichtige Sprache, Nullmodell erklärt wesentlichen Anteil, Primzahlfrage nicht gelöst"

---

## 11. Was beibehalten wurde

### 11.1 Alle Informationen

**Wichtig:** Keine Information wurde gelöscht, nur verschoben oder umformuliert.

- Klein-Flasche → Historical
- Lean 4 → Historical
- QEC → Exploratory
- Catalan, Gödel → Exploratory

### 11.2 Alle Programme

Vollständige Liste der C++-Programme beibehalten, mit klarerer Priorisierung.

### 11.3 Alle Dokumente

Vollständige Dokumentationsliste, aber strukturiert nach Current/Historical/Exploratory.

---

## 12. Empfehlungen für weiteres Vorgehen

### 12.1 Sofort

1. **Feedback einholen:** Zeigen Sie beide Versionen einem externen Leser
2. **Entscheidung:** Alt vs. Neu oder Hybrid?
3. **Falls Neu akzeptiert:** `mv README_NEW.md README.md`

### 12.2 Kurzfristig

1. **Modulo 30:** Höchste Priorität, entscheidet über Allgemeinheit
2. **$R(X)$-Asymptotik:** Messungen bei $10^6, 10^7$
3. **ArXiv-Submission:** `paper_geometric_origin.pdf` ist preprint-ready

### 12.3 Mittelfristig

1. **Dokumentation:** Aktualisierung der separaten Markdown-Files entsprechend der neuen Struktur
2. **Catalan-Subprojekt:** Falls verfolgt, klar als separates Repository
3. **QEC-Projekt:** Entweder separates Repository oder klar als Subprojekt markieren

---

## 13. Fazit

**Hauptziel erreicht:** Das neue README kommuniziert den wissenschaftlichen Kern klar und ehrlich, ohne spekulative Elemente zu verstecken (sie sind klar als "Exploratory" markiert).

**Wichtigste Stärken:**
- Vorsichtige, wissenschaftlich korrekte Sprache
- Klare Trennung: Kern / Historical / Exploratory
- Gauß-Eisenstein-Interpretation prominent
- Nullmodelle korrekt eingeordnet ("erklärt wesentlichen Anteil", nicht "löst")
- Offene Fragen explizit benannt

**Ton:** Ehrlich, stark, fokussiert, wissenschaftlich sauber.

**Für Außenstehende:** "Das ist ein seriöses Forschungsprogramm über bedingte Gap-Dynamiken, nicht geometrische Spekulation."
